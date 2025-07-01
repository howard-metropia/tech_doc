# Gluon Contrib GAE Memcache Module

## Overview
Google App Engine (GAE) memcache integration module that provides a web2py-compatible caching interface using GAE's memcache service. This module allows web2py applications to use GAE's distributed memcache as both RAM and disk cache replacement.

## Module Information
- **Module**: `gluon.contrib.gae_memcache`
- **Author**: Robin Bhattacharyya
- **License**: LGPL (web2py license)
- **Platform**: Google App Engine
- **Dependencies**: `google.appengine.api.memcache`

## Key Features
- **GAE Integration**: Native Google App Engine memcache support
- **Web2py Compatible**: Drop-in replacement for web2py's default cache
- **Application Scoping**: Automatic key namespacing by application
- **Expiration Control**: Configurable cache expiration times
- **Standard Interface**: Compatible with web2py's cache API

## Classes

### MemcacheClient
Main caching client that wraps GAE's memcache API for web2py compatibility.

**Attributes:**
- `client`: Shared GAE memcache Client instance
- `request`: Web2py request object for application context
- `default_time_expire`: Default cache expiration time (300 seconds)

## Constructor

### MemcacheClient.__init__()
Initialize the memcache client with request context and default expiration.

**Signature:**
```python
def __init__(self, request, default_time_expire=300)
```

**Parameters:**
- `request`: Web2py request object for application context
- `default_time_expire`: Default expiration time in seconds (default: 300)

**Example:**
```python
from gluon.contrib.gae_memcache import MemcacheClient
cache.ram = cache.disk = MemcacheClient(request)
```

## Core Methods

### __call__()
Primary caching method that stores and retrieves cached values.

**Signature:**
```python
def __call__(self, key, f, time_expire=None)
```

**Parameters:**
- `key`: Cache key string
- `f`: Function to execute if cache miss (or None to just retrieve)
- `time_expire`: Expiration time in seconds (None uses default)

**Returns:**
- Cached value if cache hit
- Result of `f()` if cache miss and `f` provided
- None if cache miss and no function provided

**Behavior:**
- Creates namespaced key: `{application}/{key}`
- Stores tuple: `(timestamp, value)`
- Bypasses cache if `time_expire=0`

### increment()
Increment a numeric cached value atomically.

**Signature:**
```python
def increment(self, key, value=1)
```

**Parameters:**
- `key`: Cache key string
- `value`: Increment amount (default: 1)

**Returns:**
- New incremented value

**Behavior:**
- Retrieves current value and adds increment
- Stores updated value with current timestamp
- Creates key with value 1 if key doesn't exist

### incr()
Alias for `increment()` method.

**Signature:**
```python
def incr(self, key, value=1)
```

## Cache Management Methods

### clear()
Clear specific key or flush entire cache.

**Signature:**
```python
def clear(self, key=None)
```

**Parameters:**
- `key`: Specific key to delete (None flushes all)

**Behavior:**
- If key provided: deletes specific namespaced key
- If key is None: flushes entire memcache

### initialize()
Empty initialization method for compatibility.

**Signature:**
```python
def initialize(self)
```

**Purpose:**
- Provides interface compatibility with other cache implementations
- No actual initialization required for GAE memcache

## Direct GAE Memcache Methods

### delete()
Direct proxy to GAE memcache delete method.

**Signature:**
```python
def delete(self, *args, **kwargs)
```

**Parameters:**
- Passes all arguments directly to GAE memcache client

### get()
Direct proxy to GAE memcache get method.

**Signature:**
```python
def get(self, *args, **kwargs)
```

**Parameters:**
- Passes all arguments directly to GAE memcache client

### set()
Direct proxy to GAE memcache set method.

**Signature:**
```python
def set(self, *args, **kwargs)
```

**Parameters:**
- Passes all arguments directly to GAE memcache client

### flush_all()
Flush all cache entries (incorrectly delegates to delete).

**Signature:**
```python
def flush_all(self, *args, **kwargs)
```

**Note:**
- Current implementation incorrectly calls `delete()` instead of `flush_all()`
- Should be: `return self.client.flush_all(*args, **kwargs)`

## Key Features

### Application Namespacing
All cache keys are automatically prefixed with the application name:
```python
key = '%s/%s' % (self.request.application, key)
```

This ensures cache isolation between different web2py applications on the same GAE instance.

### Timestamp Storage
Values are stored as tuples containing timestamp and actual value:
```python
self.client.set(key, (time.time(), value), time=time_expire)
```

This allows for future extension of cache metadata handling.

### Expiration Handling
- Default expiration: 300 seconds (5 minutes)
- Configurable per-instance via constructor
- Override per-call via `time_expire` parameter
- Zero expiration bypasses cache entirely

## Usage Examples

### Basic Setup
```python
from gluon.contrib.gae_memcache import MemcacheClient

# Replace default cache with GAE memcache
cache.ram = cache.disk = MemcacheClient(request)

# With custom default expiration
cache.ram = MemcacheClient(request, default_time_expire=600)
```

### Caching Functions
```python
# Cache function result for 1 hour
@cache('expensive_operation', time_expire=3600)
def expensive_operation():
    # Expensive computation
    return result

# Manual caching
def get_user_data(user_id):
    return cache('user_%s' % user_id, 
                lambda: db(db.user.id==user_id).select().first(),
                time_expire=1800)
```

### Counter Operations
```python
# Increment page views
page_views = cache.ram.increment('page_views')

# Increment by custom amount
score = cache.ram.incr('user_score', 10)
```

### Cache Management
```python
# Clear specific key
cache.ram.clear('user_123')

# Clear all cache
cache.ram.clear()

# Direct GAE memcache operations
cache.ram.set('direct_key', 'value', time=300)
value = cache.ram.get('direct_key')
```

## Integration with Web2py

### Cache Decorator
```python
# Works with web2py's @cache decorator
@cache.action()
def index():
    return dict()

@cache.select()
def get_data():
    return db().select()
```

### Cache Object Usage
```python
# Standard web2py cache usage
def cached_function():
    return cache.ram('key', lambda: expensive_operation(), time_expire=300)
```

## Performance Considerations

### Advantages
- **Distributed**: Shared across all GAE instances
- **Scalable**: Managed by Google's infrastructure
- **Fast**: In-memory storage with network access
- **Automatic**: No manual memory management required

### Limitations
- **Network Latency**: Remote memcache access overhead
- **Size Limits**: GAE memcache value size restrictions
- **Eviction**: Google may evict entries under memory pressure
- **Temporary**: Not persistent storage

## Error Handling

### Memcache Failures
GAE memcache operations may fail silently:
- Network timeouts
- Service unavailability
- Quota limitations
- Memory pressure

The module doesn't implement explicit error handling, relying on GAE's default behavior.

### Fallback Strategy
```python
# Implement fallback for critical operations
def safe_cache_get(key, fallback_func):
    try:
        result = cache.ram(key, None)
        if result is None:
            result = fallback_func()
            cache.ram(key, lambda: result)
        return result
    except:
        return fallback_func()
```

## Best Practices

### Key Design
- Use descriptive, hierarchical keys
- Include version information for cache invalidation
- Avoid very long keys (GAE limits)

### Expiration Strategy
- Short expiration for frequently changing data
- Longer expiration for stable data
- Zero expiration for debugging/testing

### Application Isolation
- Keys are automatically namespaced by application
- Consider additional namespacing for multi-tenant applications

This module provides seamless GAE memcache integration for web2py applications, offering distributed caching capabilities with minimal configuration changes.