# test_redis.py

## Overview
Unit tests for Redis integration in Web2py, specifically testing Redis-based session storage functionality using the Redis contrib packages.

## Imports
```python
import unittest
from datetime import datetime
from gluon._compat import pickle, to_bytes
from gluon.contrib.redis_cache import RedisCache
from gluon.contrib.redis_session import RedisSession
from gluon.contrib.redis_utils import RConn
from gluon.globals import Request, Response, Session, current
from gluon.storage import Storage
from gluon.utils import web2py_uuid
```

## Test Class: TestRedis

### Description
Tests Redis-based session storage implementation, simulating Web2py's session handling with Redis as the backend.

### Setup

#### setUp()
Initializes a complete Web2py environment with Redis connection:

1. **Request Setup**
   - Creates Request object with basic environment
   - Sets application, controller, function paths
   - Defines application folder

2. **Response/Session Setup**
   - Creates Response object
   - Creates Session object and connects it to request/response

3. **Current Context**
   - Sets up global current object with request/response/session
   - Ensures Web2py context is available for tests

4. **Redis Connection**
   - Creates Redis connection to localhost
   - Initializes RedisSession with no expiry
   - Sets test table name

### Test Methods

#### test_0_redis_session()
Tests basic Redis session read/write operations.

**Table Definition:**
```python
Field('locked', 'boolean', default=False)
Field('client_ip', length=64)
Field('created_datetime', 'datetime', default=datetime.now().isoformat())
Field('modified_datetime', 'datetime')
Field('unique_key', length=64)
Field('session_data', 'blob')
```

**Test Flow:**

1. **Insert Operation**
   - Creates session data with test values
   - Pickles session dictionary for storage
   - Inserts record with unique key
   - Verifies inserted data matches original

2. **Update Operation**
   - Changes locked status from 0 to 1
   - Updates record in Redis
   - Verifies updated data reflects changes

**Key Features:**
- Uses pickle for serializing session data
- ISO format for datetime storage
- UUID generation for unique keys
- Storage object for dict comparison

#### test_1_redis_delete()
Tests session retrieval and deletion from Redis.

**Test Flow:**

1. **Retrieve All Sessions**
   - Selects all records from session table
   - Verifies sessions exist in database

2. **Delete Sessions**
   - Iterates through all sessions
   - Calls `delete_record()` on each
   - Verifies deletion returns None

3. **Verify Cleanup**
   - Queries for remaining sessions
   - Confirms empty result set

## Redis Session Implementation

### RedisSession Class
Provides DAL-like interface for Redis:
- Table definition with fields
- Insert/update/delete operations
- Query syntax similar to Web2py DAL

### Session Data Structure
- **locked**: Boolean flag for session locking
- **client_ip**: Client IP address storage
- **created_datetime**: Session creation timestamp
- **modified_datetime**: Last modification time
- **unique_key**: UUID for session identification
- **session_data**: Pickled Python objects

### Redis Connection
- Uses RConn utility for connection management
- Connects to localhost by default
- Configurable session expiry

## Testing Patterns

### Environment Simulation
- Complete Web2py request/response cycle
- Global current object setup
- Proper context for session handling

### Data Serialization
- Pickle protocol for complex data types
- Binary storage in 'blob' field
- Highest pickle protocol for efficiency

### CRUD Operations
- **Create**: Insert with field validation
- **Read**: Select with query conditions
- **Update**: Modify existing records
- **Delete**: Remove with verification

### Assertions
- Dictionary equality checks
- None value verification
- Empty result validation

## Use Cases

### Session Storage
Redis sessions useful for:
- Distributed web applications
- Load-balanced environments
- Fast session access
- Shared session state

### Benefits over File-based Sessions
- No file locking issues
- Better performance
- Horizontal scalability
- Centralized session management

## Notes
- Tests assume Redis server running on localhost
- No authentication configured for Redis connection
- Session expiry disabled for testing
- Uses Web2py's DAL-like syntax for Redis operations
- Proper cleanup ensures test isolation