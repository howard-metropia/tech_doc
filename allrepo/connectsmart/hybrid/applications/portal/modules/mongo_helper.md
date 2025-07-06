# MongoDB Helper Module Documentation

## Overview
The MongoDB Helper Module provides a singleton connection manager for MongoDB integration in the ConnectSmart Hybrid Portal application. It implements connection pooling and database access using PyMongo with Web2py configuration integration.

## File Location
**Source**: `/home/datavan/METROPIA/metro_combine/allrepo/connectsmart/hybrid/applications/portal/modules/mongo_helper.py`

## Dependencies
- `os`: Environment variable access
- `gluon.current`: Web2py current context
- `pymongo.MongoClient`: MongoDB Python driver

## Classes

### MongoManager

#### Purpose
Singleton pattern implementation for MongoDB connection management with automatic database selection.

#### Class Attributes
- `_instance`: Static instance holder for singleton pattern

#### Methods

##### `get()` (Static Method)
**Purpose**: Get or create MongoDB database connection instance
**Returns**: MongoDB database object

**Connection Logic**:
1. Check if singleton instance exists
2. If not, create new MongoClient connection
3. Use environment variable or configuration for URI
4. Return default database from connection

**Configuration Priority**:
1. **Environment Variable**: `MONGO_CACHE_URI`
2. **Configuration File**: `db.mongo_uri`

## Connection Management

### Singleton Pattern Benefits
- **Resource Efficiency**: Single connection pool
- **Performance**: Reduced connection overhead
- **Consistency**: Shared database instance
- **Memory Usage**: Minimal connection objects

### URI Configuration
```python
# Environment variable (highest priority)
export MONGO_CACHE_URI="mongodb://username:password@host:port/database"

# Configuration file (fallback)
db.mongo_uri = "mongodb://localhost:27017/portal_cache"
```

### Database Selection
- Uses `get_default_database()` from MongoClient
- Database name inferred from connection URI
- No explicit database name required in code

## Usage Examples

### Basic Database Access
```python
from mongo_helper import MongoManager

# Get database instance
mongo_db = MongoManager.get()

# Access collections
users_collection = mongo_db.users
cache_collection = mongo_db.cache
```

### Collection Operations
```python
# Insert document
result = MongoManager.get().events.insert_one({
    'user_id': 123,
    'event_type': 'login',
    'timestamp': datetime.utcnow()
})

# Query documents
user_events = MongoManager.get().events.find({
    'user_id': 123
})
```

### Integration with Web2py
```python
def controller_action():
    mongo_db = MongoManager.get()
    
    # Store session data
    mongo_db.sessions.insert_one({
        'session_id': session.session_id,
        'data': dict(session)
    })
    
    return dict(status='success')
```

## MongoDB Features Used

### PyMongo Client Features
- **Connection Pooling**: Automatic connection management
- **Automatic Reconnection**: Built-in failover handling
- **Thread Safety**: Safe for concurrent access
- **Write Concerns**: Configurable durability guarantees

### Database Operations
- **Collections**: Dynamic collection access
- **CRUD Operations**: Create, Read, Update, Delete
- **Indexing**: Performance optimization support
- **Aggregation**: Complex query operations

## Configuration Examples

### Environment Variable Setup
```bash
# Development
export MONGO_CACHE_URI="mongodb://localhost:27017/portal_dev"

# Production
export MONGO_CACHE_URI="mongodb://user:pass@prod-mongo:27017/portal_prod"

# Replica Set
export MONGO_CACHE_URI="mongodb://host1:27017,host2:27017/portal?replicaSet=rs0"
```

### Web2py Configuration
```python
# In configuration file
db = {
    'mongo_uri': 'mongodb://localhost:27017/portal_cache',
    'connection_options': {
        'maxPoolSize': 100,
        'retryWrites': True
    }
}
```

## Error Handling

### Connection Errors
- PyMongo handles connection failures automatically
- Implements retry logic for transient failures
- Singleton prevents multiple connection attempts

### Common Issues
```python
try:
    mongo_db = MongoManager.get()
    result = mongo_db.collection.find_one()
except Exception as e:
    # Log connection or query errors
    logger.error(f"MongoDB operation failed: {e}")
```

## Performance Considerations

### Connection Pooling
- Single connection pool shared across application
- Reduces connection establishment overhead
- Thread-safe concurrent access

### Memory Management
- Singleton pattern minimizes memory usage
- Connection reuse across requests
- Automatic connection cleanup by PyMongo

## Security Features

### Authentication
- Connection string includes credentials
- Environment variable prevents credential exposure
- Supports various authentication mechanisms

### Network Security
- SSL/TLS support through connection string
- Connection string encryption recommended
- Network-level access controls

## Integration Patterns

### Cache Storage
```python
def cache_user_data(user_id, data):
    mongo_db = MongoManager.get()
    mongo_db.user_cache.replace_one(
        {'user_id': user_id},
        {'user_id': user_id, 'data': data, 'updated': datetime.utcnow()},
        upsert=True
    )
```

### Event Logging
```python
def log_user_event(user_id, event_type, metadata):
    mongo_db = MongoManager.get()
    mongo_db.events.insert_one({
        'user_id': user_id,
        'event_type': event_type,
        'metadata': metadata,
        'timestamp': datetime.utcnow()
    })
```

### Session Management
```python
def store_session_data(session_id, session_data):
    mongo_db = MongoManager.get()
    mongo_db.sessions.update_one(
        {'session_id': session_id},
        {'$set': {'data': session_data, 'last_accessed': datetime.utcnow()}},
        upsert=True
    )
```

## Monitoring and Maintenance

### Connection Status
```python
def check_mongo_status():
    try:
        mongo_db = MongoManager.get()
        # Test connection
        mongo_db.command('ping')
        return True
    except Exception:
        return False
```

### Collection Statistics
```python
def get_collection_stats(collection_name):
    mongo_db = MongoManager.get()
    return mongo_db.command('collStats', collection_name)
```

## Best Practices
- Use environment variables for sensitive configuration
- Implement proper error handling for all operations
- Consider indexing for frequently queried fields
- Monitor connection pool usage in production
- Use appropriate write concerns for data consistency

## Related Components
- SQS Helper for event queuing
- User profile management
- Session caching system
- Event tracking infrastructure