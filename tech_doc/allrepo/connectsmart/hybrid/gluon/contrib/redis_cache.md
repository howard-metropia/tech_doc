# Gluon Contrib Redis Cache Module

## Overview
Redis-based caching implementation for web2py applications. Provides high-performance, distributed caching using Redis as the backend storage, enabling scalable caching across multiple application instances.

## Module Information
- **Module**: `gluon.contrib.redis_cache`
- **Dependencies**: redis-py, web2py cache framework
- **Purpose**: Distributed caching with Redis
- **Use Case**: High-performance applications, multi-server deployments

## Key Features
- **Distributed Caching**: Shared cache across multiple servers
- **High Performance**: Redis in-memory storage
- **Persistence**: Optional data persistence
- **Scalability**: Horizontal scaling support
- **TTL Support**: Time-to-live for cache entries
- **Atomic Operations**: Redis atomic operations support

## Basic Usage

### Setup and Configuration
```python
from gluon.contrib.redis_cache import RedisCache

# Basic Redis cache setup
cache.redis = RedisCache(
    host='localhost',
    port=6379,
    db=0,
    password=None
)

# Replace default cache
cache.ram = cache.redis
cache.disk = cache.redis
```

### Simple Caching
```python
# Cache function results
@cache('expensive_operation', time_expire=3600)  # 1 hour
def expensive_operation():
    # Simulate expensive computation
    import time
    time.sleep(2)
    return "Computed result"

# Manual caching
def get_user_data(user_id):
    key = f'user_data_{user_id}'
    result = cache.redis(key, lambda: db.users[user_id], time_expire=1800)
    return result
```

### Web2py Integration
```python
# In models/db.py
import redis
from gluon.contrib.redis_cache import RedisCache

# Configure Redis connection
REDIS_CONFIG = {
    'host': os.environ.get('REDIS_HOST', 'localhost'),
    'port': int(os.environ.get('REDIS_PORT', 6379)),
    'db': int(os.environ.get('REDIS_DB', 0)),
    'password': os.environ.get('REDIS_PASSWORD'),
    'decode_responses': True
}

# Initialize Redis cache
cache.redis = RedisCache(**REDIS_CONFIG)

# Use Redis for different cache types
cache.ram = cache.redis      # Fast access cache
cache.disk = cache.redis     # Persistent cache
```

## Advanced Features

### Custom Cache Keys
```python
def custom_cache_key(func_name, *args, **kwargs):
    """Generate custom cache keys"""
    key_parts = [func_name]
    key_parts.extend(str(arg) for arg in args)
    key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
    return ":".join(key_parts)

# Usage with custom keys
def cached_function(param1, param2):
    key = custom_cache_key('cached_function', param1, param2)
    return cache.redis(key, lambda: expensive_computation(param1, param2))
```

### Distributed Session Storage
```python
# Configure Redis for session storage
from gluon.contrib.redis_session import RedisSession

# In models/db.py
if request.env.web2py_runtime_gae:
    # Use default sessions on GAE
    pass
else:
    # Use Redis sessions for scalability
    session.connect(request, response, db=RedisSession(
        redis_conn=redis.Redis(**REDIS_CONFIG)
    ))
```

### Cache Invalidation Patterns
```python
class SmartCache:
    def __init__(self, redis_cache):
        self.cache = redis_cache
        self.redis_client = redis_cache.redis_client
    
    def tag_cache(self, key, value, tags=None, time_expire=None):
        """Cache with tags for group invalidation"""
        # Store the main cache entry
        self.cache(key, lambda: value, time_expire=time_expire)
        
        # Store tag relationships
        if tags:
            for tag in tags:
                tag_key = f"tag:{tag}"
                self.redis_client.sadd(tag_key, key)
                if time_expire:
                    self.redis_client.expire(tag_key, time_expire)
    
    def invalidate_tag(self, tag):
        """Invalidate all cache entries with specific tag"""
        tag_key = f"tag:{tag}"
        keys = self.redis_client.smembers(tag_key)
        
        if keys:
            # Delete all tagged entries
            self.redis_client.delete(*keys)
            # Delete the tag set
            self.redis_client.delete(tag_key)

# Usage
smart_cache = SmartCache(cache.redis)

# Cache with tags
smart_cache.tag_cache(
    'user_profile_123',
    get_user_profile(123),
    tags=['user:123', 'profiles'],
    time_expire=3600
)

# Invalidate all user:123 related cache
smart_cache.invalidate_tag('user:123')
```

This module enables high-performance distributed caching for web2py applications using Redis as the backend storage system.