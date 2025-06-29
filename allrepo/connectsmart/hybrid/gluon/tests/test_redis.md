# test_redis.py

## Overview
This file contains unit tests for the web2py Redis integration modules. It tests Redis-based session storage, caching functionality, and database operations using Redis as the backend storage system.

## Purpose
- Tests Redis session storage functionality
- Validates Redis connection and configuration
- Tests Redis-based database operations (insert, update, delete)
- Verifies data serialization and deserialization with Redis
- Tests session data integrity and management

## Key Classes and Methods

### TestRedis Class
Test suite for Redis contrib packages.

#### Setup Method

##### `setUp(self)`
Initializes Redis testing environment.

**Web2py Context Setup:**
- Creates Request, Response, Session objects
- Sets up application context ("a", "c", "f")
- Establishes global current context

**Redis Configuration:**
```python
rconn = RConn(host="localhost")
self.db = RedisSession(redis_conn=rconn, session_expiry=False)
```

#### Test Methods

##### `test_0_redis_session(self)`
Tests basic Redis session read-write operations.

**Table Definition:**
```python
db.define_table(
    self.tname,
    Field("locked", "boolean", default=False),
    Field("client_ip", length=64),
    Field("created_datetime", "datetime", default=datetime.now().isoformat()),
    Field("modified_datetime", "datetime"),
    Field("unique_key", length=64),
    Field("session_data", "blob"),
)
```

**Data Operations:**
- **Insert**: Tests record insertion with pickled session data
- **Retrieve**: Validates data retrieval and integrity
- **Update**: Tests record updates and validation
- **Serialization**: Tests pickle serialization of complex data structures

**Test Data:**
```python
session_data = pickle.dumps(
    {"test": 123, "me": 112312312}, pickle.HIGHEST_PROTOCOL
)
```

##### `test_1_redis_delete(self)`
Tests Redis session deletion functionality.

**Delete Operations:**
- **Batch Retrieval**: Gets all sessions from Redis
- **Individual Deletion**: Tests individual record deletion
- **Cleanup Validation**: Ensures all records are properly removed
- **Empty State**: Validates empty database state after cleanup

## Dependencies
- `unittest` - Python testing framework
- `datetime` - Date and time operations
- `gluon._compat` - Compatibility utilities (pickle, to_bytes)
- `gluon.contrib.redis_cache` - Redis caching module
- `gluon.contrib.redis_session` - Redis session storage
- `gluon.contrib.redis_utils` - Redis utilities (RConn)
- `gluon.globals` - Global context objects
- `gluon.storage` - Storage utilities
- `gluon.utils` - Utility functions (web2py_uuid)

## Redis Components Tested

### RedisSession
- **Session Storage**: Redis-based session storage implementation
- **Field Definition**: Table-like field definitions for session data
- **CRUD Operations**: Create, Read, Update, Delete operations
- **Data Serialization**: Automatic pickle serialization for complex data

### RConn (Redis Connection)
- **Connection Management**: Redis server connection handling
- **Configuration**: Host and connection parameter management
- **Connection Pooling**: Efficient connection management
- **Error Handling**: Connection error management

### Data Types Supported
- **Boolean**: Locked state tracking
- **String**: Client IP and unique key storage
- **DateTime**: Timestamp tracking for sessions
- **Blob**: Serialized session data storage

## Session Data Structure

### Session Table Fields
- **locked** (boolean): Session lock status
- **client_ip** (string, 64): Client IP address
- **created_datetime** (datetime): Session creation timestamp
- **modified_datetime** (datetime): Last modification timestamp
- **unique_key** (string, 64): Unique session identifier
- **session_data** (blob): Pickled session data

### Session Operations
- **Creation**: New session creation with unique keys
- **Modification**: Session data updates and timestamps
- **Locking**: Session locking mechanism for concurrency
- **Deletion**: Session cleanup and removal

## Usage Example
```python
from gluon.contrib.redis_session import RedisSession
from gluon.contrib.redis_utils import RConn
from gluon.utils import web2py_uuid
import pickle

# Setup Redis connection
rconn = RConn(host="localhost", port=6379, db=0)
redis_session = RedisSession(redis_conn=rconn, session_expiry=3600)

# Define session table
redis_session.define_table(
    "sessions",
    Field("locked", "boolean", default=False),
    Field("client_ip", length=64),
    Field("session_data", "blob"),
    Field("unique_key", length=64)
)

# Store session data
session_data = {"user_id": 123, "preferences": {"theme": "dark"}}
unique_key = web2py_uuid()

session_id = redis_session.sessions.insert(
    client_ip="192.168.1.1",
    unique_key=unique_key,
    session_data=pickle.dumps(session_data, pickle.HIGHEST_PROTOCOL)
)

# Retrieve session
session_record = redis_session(redis_session.sessions.id == session_id).select().first()
loaded_data = pickle.loads(session_record.session_data)

# Update session
redis_session(redis_session.sessions.id == session_id).update(
    locked=True,
    modified_datetime=datetime.now()
)

# Delete session
session_record.delete_record()
```

## Integration with web2py Framework

### Session Management
- **Session Storage**: Alternative to file-based or database sessions
- **Scalability**: Distributed session storage for multiple servers
- **Performance**: Fast Redis-based session access
- **Persistence**: Configurable session persistence and expiry

### Caching Integration
- **Application Cache**: Redis-based application caching
- **Query Cache**: Database query result caching
- **Object Cache**: Complex object caching and retrieval
- **Cache Management**: Cache invalidation and cleanup

### Multi-Server Support
- **Session Sharing**: Shared sessions across multiple web2py instances
- **Load Balancing**: Session consistency in load-balanced environments
- **Clustering**: Support for web2py application clustering
- **Fault Tolerance**: Session recovery and backup mechanisms

### Development Benefits
- **Development Tools**: Redis inspection and debugging tools
- **Performance Monitoring**: Session and cache performance metrics
- **Configuration**: Flexible Redis configuration options
- **Testing**: Isolated testing with Redis backends

## Test Coverage
- **Basic Operations**: Insert, update, delete, select operations
- **Data Integrity**: Data serialization and deserialization
- **Session Management**: Session creation, modification, and cleanup
- **Connection Management**: Redis connection handling
- **Error Handling**: Proper error handling and recovery
- **Cleanup Operations**: Proper resource cleanup

## Expected Results
- **Data Persistence**: Session data should persist in Redis
- **Serialization**: Complex data should serialize/deserialize correctly
- **CRUD Operations**: All database operations should work properly
- **Connection Stability**: Redis connections should be stable
- **Data Integrity**: No data corruption during operations
- **Cleanup**: Proper cleanup of test data

## Redis Requirements
- **Redis Server**: Running Redis server on localhost
- **Redis Version**: Compatible Redis version (2.6+)
- **Network Access**: Accessible Redis instance
- **Memory**: Sufficient memory for test data
- **Configuration**: Proper Redis configuration for testing

## File Structure
```
gluon/tests/
├── test_redis.py         # This file
└── ... (other test files)

gluon/contrib/
├── redis_cache.py        # Redis caching implementation
├── redis_session.py      # Redis session storage
└── redis_utils.py        # Redis utilities and connection
```

This test suite ensures web2py's Redis integration provides reliable, scalable session storage and caching capabilities for high-performance web applications.