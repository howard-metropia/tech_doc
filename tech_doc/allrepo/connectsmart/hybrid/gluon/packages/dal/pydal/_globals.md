# _globals.py

## Overview
Global constants and threading utilities for PyDAL that provide thread-safe operations and common functional programming primitives.

## Threading Support

### GLOBAL_LOCKER
```python
GLOBAL_LOCKER = threading.RLock()
```
**Reentrant lock** for thread-safe operations across PyDAL:
- **Type**: `threading.RLock()` (reentrant/recursive lock)
- **Purpose**: Protects critical sections that may be called recursively
- **Usage**: Database connection pooling, schema modifications, global state

**Benefits of RLock:**
- Same thread can acquire lock multiple times
- Prevents deadlocks in recursive scenarios
- Essential for database operations that may trigger cascading locks

### THREAD_LOCAL
```python
THREAD_LOCAL = threading.local()
```
**Thread-local storage** for per-thread state management:
- **Type**: `threading.local()` object
- **Purpose**: Stores data unique to each thread
- **Usage**: Database connections, transaction state, caching

**Thread Safety Benefits:**
- Each thread gets isolated storage
- No data sharing between threads
- Automatic cleanup when thread terminates

## Functional Primitives

### DEFAULT
```python
DEFAULT = lambda: None
```
**Null factory function**:
- **Returns**: Always returns `None`
- **Usage**: Default value provider, placeholder function
- **Pattern**: Functional programming default parameter

### IDENTITY
```python
def IDENTITY(x):
    return x
```
**Identity function**:
- **Input**: Any value `x`
- **Output**: Returns `x` unchanged
- **Usage**: No-op transformations, default mappers, functional composition

**Common Use Cases:**
- Default transformation in field definitions
- Placeholder for optional processing functions
- Functional programming identity element

### Logical Operations

#### OR
```python
def OR(a, b):
    return a | b
```
**Bitwise OR operation**:
- **Inputs**: Two values `a` and `b`
- **Output**: Bitwise OR result `a | b`
- **Usage**: Combining flags, permission masks, query filters

#### AND
```python
def AND(a, b):
    return a & b
```
**Bitwise AND operation**:
- **Inputs**: Two values `a` and `b`
- **Output**: Bitwise AND result `a & b`
- **Usage**: Flag checking, permission validation, query filtering

## Usage Patterns in PyDAL

### Thread-Safe Database Operations
```python
with GLOBAL_LOCKER:
    # Critical database operations
    # Schema modifications
    # Connection pool management
```

### Per-Thread State Management
```python
# Store database connection per thread
THREAD_LOCAL.db_connection = connection

# Access thread-specific state
connection = getattr(THREAD_LOCAL, 'db_connection', None)
```

### Functional Composition
```python
# Default field transformer
field_transform = IDENTITY

# Combine query conditions
query_flags = OR(FLAG_A, FLAG_B)
permission_check = AND(user_permissions, required_permissions)
```

## Thread Safety Architecture

### Connection Management
- Each thread maintains its own database connections
- GLOBAL_LOCKER protects shared resources like connection pools
- THREAD_LOCAL stores per-thread connection state

### Transaction Isolation
- Thread-local storage prevents transaction interference
- Each thread can have independent transaction state
- Global lock protects transaction commit/rollback operations

### Schema Operations
- DDL operations protected by GLOBAL_LOCKER
- Prevents concurrent schema modifications
- Ensures data integrity during structural changes

## Functional Programming Support

### Default Values
- DEFAULT provides consistent null value factory
- IDENTITY serves as no-op transformation
- Enables clean functional composition patterns

### Bitwise Operations
- OR/AND functions support flag-based programming
- Enable permission systems and query composition
- Provide functional approach to bitwise logic

## Integration Points

### Database Adapters
- All adapters use GLOBAL_LOCKER for critical sections
- THREAD_LOCAL stores adapter-specific state
- Functions support adapter configuration

### Field Definitions
- IDENTITY used as default field transformer
- DEFAULT provides null value semantics
- Functions enable field-level customization

### Query Engine
- OR/AND support query condition composition
- Thread-local storage maintains query state
- Global locking protects query compilation

## Notes
- Essential for multi-threaded database applications
- Provides foundation for thread-safe PyDAL operations
- Enables functional programming patterns in ORM
- Critical for web application deployment scenarios
- Supports both traditional and async programming models