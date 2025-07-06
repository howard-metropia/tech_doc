# connection.py

## Overview
Database connection management module for PyDAL that provides connection pooling, thread-safe connection handling, and lifecycle management for database connections across multiple adapters.

## Core Classes

### ConnectionPool
Main class for managing database connections with pooling and thread-safety features.

#### Class Attributes
```python
POOLS = {}                      # Global connection pools by URI
check_active_connection = True  # Enable connection health checks
```

#### Instance Attributes
```python
_first_connection = False       # Flag for first connection setup
```

## Connection Identification

### Thread-Local Naming
Connection and cursor names are unique per adapter instance and process:

#### _connection_uname_
```python
@property
def _connection_uname_(self):
    return "_pydal_connection_%s_%s" % (id(self), os.getpid())
```
**Format**: `_pydal_connection_{adapter_id}_{process_id}`

#### _cursors_uname_
```python
@property  
def _cursors_uname_(self):
    return "_pydal_cursor_%s_%s" % (id(self), os.getpid())
```
**Format**: `_pydal_cursor_{adapter_id}_{process_id}`

**Benefits:**
- Unique identification per adapter instance
- Process isolation for multiprocessing environments
- Thread-local storage separation

## Connection Management

### get_connection(use_pool=True)
Primary method for retrieving database connections with intelligent pooling.

#### Connection Resolution Strategy
1. **Thread-Local Check**: Look for existing connection in current thread
2. **Pool Retrieval**: If pooling enabled, try to get connection from pool
3. **Health Validation**: Test pooled connections before use
4. **New Connection**: Create new connection if none available
5. **Hook Execution**: Run post-connection hooks for new connections

```python
def get_connection(self, use_pool=True):
    # Check thread-local storage
    connection = getattr(THREAD_LOCAL, self._connection_uname_, None)
    if connection is not None:
        return connection
    
    # Try pool if enabled
    if use_pool and self.pool_size:
        with GLOBAL_LOCKER:
            pool = ConnectionPool.POOLS.get(self.uri, [])
            while connection is None and pool:
                connection = pool.pop()
                try:
                    self.set_connection(connection, run_hooks=False)
                except:
                    connection = None
    
    # Create new connection if needed
    if connection is None:
        connection = self.connector()
        self.set_connection(connection, run_hooks=True)
    
    return connection
```

### set_connection(connection, run_hooks=False)
Establishes connection in thread-local storage with optional hooks.

**Process:**
1. **Storage**: Store connection in thread-local storage
2. **Cursor Creation**: Create and store database cursor
3. **Hook Execution**: Run after_connection hooks if requested
4. **Health Check**: Test connection if check_active_connection enabled

```python
def set_connection(self, connection, run_hooks=False):
    setattr(THREAD_LOCAL, self._connection_uname_, connection)
    if connection:
        setattr(THREAD_LOCAL, self._cursors_uname_, connection.cursor())
        if run_hooks:
            self.after_connection_hook()
        if self.check_active_connection:
            self.test_connection()
    else:
        setattr(THREAD_LOCAL, self._cursors_uname_, None)
```

## Connection Pooling

### Pool Architecture
- **Global Pools**: Shared across all instances with same URI
- **URI-Based**: Separate pools for each database connection string
- **Thread-Safe**: Protected by GLOBAL_LOCKER
- **Size-Limited**: Configurable maximum pool size

### Pool Lifecycle
1. **Creation**: Pools created on-demand for each URI
2. **Population**: Connections added when closed (if pool not full)
3. **Retrieval**: Connections popped from pool for reuse
4. **Validation**: Health checks before returning pooled connections
5. **Cleanup**: Failed connections discarded, not returned to pool

### close(action="commit", really=True)
Sophisticated connection closing with pooling and error handling.

#### Parameters
- **action**: Action to perform before closing ("commit", "rollback", or callable)
- **really**: Force actual connection closure even with pooling

#### Process Flow
```python
def close(self, action="commit", really=True):
    # Skip if no connection
    if not hasattr(THREAD_LOCAL, self._connection_uname_):
        return
    
    # Execute action (commit/rollback)
    succeeded = True
    if action:
        try:
            if callable(action):
                action(self)
            else:
                getattr(self, action)()
        except:
            succeeded = False
    
    # Return to pool if successful and pool has space
    if self.pool_size and succeeded:
        with GLOBAL_LOCKER:
            pool = ConnectionPool.POOLS[self.uri]
            if len(pool) < self.pool_size:
                pool.append(self.connection)
                really = False
    
    # Actually close connection if needed
    if really:
        try:
            self.close_connection()
        except:
            pass
    
    # Always clear thread-local storage
    self.set_connection(None)
```

## Cursor Management

### cursor Property
```python
@property
def cursor(self):
    return getattr(THREAD_LOCAL, self._cursors_uname_)
```
Retrieves the database cursor for the current connection.

### reset_cursor()
```python
def reset_cursor(self):
    setattr(THREAD_LOCAL, self._cursors_uname_, self.connection.cursor())
```
Creates a new cursor for the existing connection (useful after certain operations).

## Thread-Local Cleanup

### _clean_tlocals()
```python
def _clean_tlocals(self):
    delattr(THREAD_LOCAL, self._cursors_uname_)
    delattr(THREAD_LOCAL, self._connection_uname_)
```
Removes connection and cursor from thread-local storage.

## Global Operations

### close_all_instances(action)
Static method for cleanly closing all database instances in multi-threaded environments.

**Process:**
1. **Discovery**: Find all DAL instances in thread-local storage
2. **Iteration**: Close each adapter in each database group
3. **Action Execution**: Perform specified action on each adapter
4. **Cleanup**: Clear all instance tracking dictionaries

```python
@staticmethod
def close_all_instances(action):
    dbs = getattr(THREAD_LOCAL, "_pydal_db_instances_", {}).items()
    for db_uid, db_group in dbs:
        for db in db_group:
            if hasattr(db, "_adapter"):
                db._adapter.close(action)
    
    # Clear tracking structures
    getattr(THREAD_LOCAL, "_pydal_db_instances_", {}).clear()
    getattr(THREAD_LOCAL, "_pydal_db_instances_zombie_", {}).clear()
    
    if callable(action):
        action(None)
```

### set_folder(folder)
```python
@staticmethod
def set_folder(folder):
    THREAD_LOCAL._pydal_folder_ = folder
```
Sets the working folder for PyDAL operations in thread-local storage.

## Hook System

### after_connection_hook()
Orchestrates post-connection setup with multiple hook types:

```python
def after_connection_hook(self):
    # First connection only
    if not self._first_connection:
        self._after_first_connection()
        self._first_connection = True
    
    # User-specified hook
    if callable(self._after_connection):
        self._after_connection(self)
    
    # Adapter-specific hook
    self.after_connection()
```

### Hook Types
1. **_after_first_connection()**: One-time setup for first connection
2. **_after_connection**: User-provided callback function
3. **after_connection()**: Adapter-specific override point

## Utility Methods

### _find_work_folder()
```python
def _find_work_folder(self):
    self.folder = getattr(THREAD_LOCAL, "_pydal_folder_", "")
```
Retrieves the working folder from thread-local storage.

### reconnect()
```python
def reconnect(self):
    self.close()
    self.get_connection()
```
Legacy method for connection re-establishment (no longer needed with pooling).

## Thread Safety Features

### Global Locking
- **GLOBAL_LOCKER**: Protects pool operations
- **Thread-Local Storage**: Isolates connections per thread
- **Process Isolation**: Unique naming per process ID

### Concurrency Patterns
- **Connection Isolation**: Each thread gets its own connection
- **Pool Sharing**: Pools shared safely across threads
- **Atomic Operations**: Pool operations are atomic
- **Error Isolation**: Connection failures don't affect other threads

## Error Handling

### Connection Validation
- Automatic health checks for pooled connections
- Graceful handling of dropped connections
- Connection replacement on failure

### Pool Management
- Failed connections excluded from pools
- Automatic pool cleanup on errors
- Graceful degradation when pools are full

## Usage Patterns

### Basic Connection
```python
# Get connection (with pooling)
conn = adapter.get_connection()

# Execute operations
cursor = adapter.cursor
cursor.execute("SELECT * FROM table")

# Close connection (returns to pool if available)
adapter.close()
```

### Custom Actions
```python
# Close with custom action
adapter.close(action=lambda adapter: adapter.custom_cleanup())

# Force real closure (bypass pooling)
adapter.close(really=True)
```

### Global Cleanup
```python
# Close all connections in thread
ConnectionPool.close_all_instances("commit")
```

## Notes
- Essential for PyDAL's thread-safe database operations
- Provides connection pooling for improved performance
- Handles complex lifecycle management across multiple database types
- Supports both single-threaded and multi-threaded applications
- Critical for web application deployment scenarios