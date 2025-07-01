# Gluon Caching System Documentation

## Overview

The `cache.py` module provides a comprehensive caching framework for the Gluon web framework, offering multiple storage backends including RAM and disk-based caching. It implements thread-safe, process-safe caching mechanisms with support for expiration, statistics tracking, and memory management.

## File Location
`/home/datavan/METROPIA/metro_combine/allrepo/connectsmart/hybrid/gluon/cache.py`

## Dependencies

### Core Dependencies
- **datetime**: Date and time handling for expiration
- **hashlib**: Hash functions for cache keys
- **os**: Operating system interface for file operations
- **pickle**: Object serialization for persistent storage
- **tempfile**: Temporary file operations
- **time**: Time-based operations and measurements
- **thread**: Threading primitives for synchronization

### Framework Dependencies
- **gluon.recfile**: Record file utilities for disk storage
- **gluon._compat**: Compatibility layer for Python versions
- **pydal.contrib.portalocker**: File locking mechanisms
- **pydal.objects.Row**: Database row object handling

### Optional Dependencies
- **psutil**: System resource monitoring for memory management
- **gluon.settings**: Framework settings (GAE detection)

## Architecture Overview

### Cache Hierarchy
```
Cache (Main Interface)
├── CacheInRam (Memory-based caching)
├── CacheOnDisk (Persistent file-based caching)
└── MemcacheClient (GAE/Memcache integration)
```

### Core Classes

#### CacheAbstract
Base abstract class defining the caching interface contract.

```python
class CacheAbstract(object):
    cache_stats_name = "web2py_cache_statistics"
    max_ram_utilization = None
    
    def __call__(self, key, f, time_expire=DEFAULT_TIME_EXPIRE):
        """Main caching interface method"""
        
    def clear(self, regex=None):
        """Clear cache entries matching pattern"""
        
    def increment(self, key, value=1):
        """Increment cached numeric values"""
```

## RAM-Based Caching (CacheInRam)

### Features
- **Global Per-Process Storage**: Shared dictionary across all threads
- **Thread-Safe Operations**: Mutex locks prevent race conditions
- **Memory Management**: Automatic cleanup based on memory utilization
- **Statistics Tracking**: Hit/miss ratio monitoring
- **Application Isolation**: Separate cache spaces per application

### Implementation Details

#### Storage Structure
```python
class CacheInRam(CacheAbstract):
    locker = thread.allocate_lock()
    meta_storage = {}  # Global storage per application
    stats = {}         # Statistics per application
    
    def __init__(self, request=None):
        self.storage = OrderedDict() if HAVE_PSUTIL else {}
        self.app = request.application if request else ""
```

#### Cache Operations
```python
def __call__(self, key, f, time_expire=DEFAULT_TIME_EXPIRE, destroyer=None):
    """
    Core caching method:
    1. Check for existing valid cache entry
    2. Return cached value if valid and not expired
    3. Execute function f() if cache miss or expired
    4. Store new value with timestamp
    5. Optionally clean up old entries
    """
```

#### Memory Management
```python
def remove_oldest_entries(storage, percentage=90):
    """
    Removes oldest cache entries when memory utilization exceeds threshold
    Uses psutil to monitor system memory usage
    """
    old_mem = psutil.virtual_memory().percent
    while storage and old_mem > percentage:
        storage.popitem(last=False)  # Remove oldest entry
        gc.collect(1)                # Force garbage collection
        new_mem = psutil.virtual_memory().percent
        if new_mem >= old_mem:
            break  # Stop if memory didn't decrease
        old_mem = new_mem
```

### Thread Safety
```python
self.locker.acquire()
try:
    # Critical section operations
    item = self.storage.get(key, None)
    self.storage[key] = (now, value)
    self.stats[self.app]["misses"] += 1
finally:
    self.locker.release()
```

## Disk-Based Caching (CacheOnDisk)

### Features
- **Persistent Storage**: Survives application restarts
- **Process-Safe Operations**: File locking prevents corruption
- **Scalable Storage**: No memory limitations
- **Key Filtering**: Platform-specific filename handling
- **Atomic Operations**: Safe concurrent access

### Implementation Architecture

#### PersistentStorage Class
```python
class PersistentStorage(object):
    def __init__(self, folder, file_lock_time_wait=0.1):
        self.folder = folder
        self.key_filter_in = lambda key: key      # Key encoding
        self.key_filter_out = lambda key: key    # Key decoding
        self.file_locks = defaultdict(thread.allocate_lock)
```

#### Windows Compatibility
```python
if sys.platform == "win32":
    import base64
    
    def key_filter_in_windows(key):
        """Windows filename restrictions: encode with base32"""
        return to_native(base64.b32encode(to_bytes(key)))
    
    def key_filter_out_windows(key):
        """Decode keys for regex-based operations"""
        return to_native(base64.b32decode(to_bytes(key)))
```

#### File Operations
```python
def __setitem__(self, key, value):
    """Store value in file with pickle serialization"""
    key = self.key_filter_in(key)
    val_file = recfile.open(key, mode="wb", path=self.folder)
    self.wait_portalock(val_file)  # Process-level file locking
    pickle.dump(value, val_file, pickle.HIGHEST_PROTOCOL)
    val_file.close()

def __getitem__(self, key):
    """Retrieve value from file with pickle deserialization"""
    key = self.key_filter_in(key)
    val_file = recfile.open(key, mode="rb", path=self.folder)
    self.wait_portalock(val_file)
    value = pickle.load(val_file)
    val_file.close()
    return value
```

#### Atomic Operations
```python
def safe_apply(self, key, function, default_value=None):
    """
    Atomically apply function to cached value:
    1. Lock file for exclusive access
    2. Read current value or use default
    3. Apply transformation function
    4. Write new value back to file
    5. Return transformed value
    """
    exists = True
    try:
        val_file = recfile.open(key, mode="r+b", path=self.folder)
    except IOError:
        exists = False
        val_file = recfile.open(key, mode="wb", path=self.folder)
    
    self.wait_portalock(val_file)
    if exists:
        timestamp, value = pickle.load(val_file)
    else:
        value = default_value
    
    new_value = function(value)
    val_file.seek(0)
    pickle.dump((time.time(), new_value), val_file, pickle.HIGHEST_PROTOCOL)
    val_file.truncate()
    val_file.close()
    return new_value
```

## Main Cache Interface

### Cache Class
The primary interface that orchestrates different caching backends.

```python
class Cache(object):
    autokey = ":%(name)s:%(args)s:%(vars)s"
    
    def __init__(self, request):
        """Initialize appropriate cache backends based on environment"""
        if have_settings and settings.global_settings.web2py_runtime_gae:
            # Google App Engine environment
            from gluon.contrib.gae_memcache import MemcacheClient
            self.ram = self.disk = MemcacheClient(request)
        else:
            # Standard environment
            self.ram = CacheInRam(request)
            try:
                self.disk = CacheOnDisk(request)
            except (IOError, AttributeError):
                logger.warning("Cache disk backend unavailable")
```

### Decorator Interface
```python
def __call__(self, key=None, time_expire=DEFAULT_TIME_EXPIRE, cache_model=None):
    """
    Decorator for caching function results
    
    @cache('user_list', 3600, cache.ram)
    def get_users():
        return db().select(db.users.ALL)
    """
    def tmp(func, cache=self, cache_model=cache_model):
        return CacheAction(func, key, time_expire, self, cache_model)
    return tmp
```

### Action Caching
Advanced HTTP-aware caching for web actions with support for conditional caching based on various request parameters.

```python
def action(self, time_expire=DEFAULT_TIME_EXPIRE, cache_model=None, 
           prefix=None, session=False, vars=True, lang=True, 
           user_agent=False, public=True, valid_statuses=None, quick=None):
    """
    HTTP-aware action caching with conditional keys:
    - session: Include session ID in cache key
    - vars: Include query string in cache key  
    - lang: Include accepted language in cache key
    - user_agent: Include user agent info in cache key
    - public: Set Cache-Control header appropriately
    """
```

#### Cache Key Generation
```python
def wrapped_f():
    # Build cache key from request components
    cache_key = [current.request.env.path_info, current.response.view]
    if session_:
        cache_key.append(current.response.session_id)
    if vars_:
        cache_key.append(current.request.env.query_string)
    if lang_:
        cache_key.append(current.T.accepted_language)
    
    cache_key = hashlib_md5("__".join(cache_key)).hexdigest()
    if prefix:
        cache_key = prefix + cache_key
```

#### HTTP Headers Management
```python
# Set appropriate cache headers
if time_expire:
    cache_control = f"max-age={time_expire}, s-maxage={time_expire}"
    expires = (current.request.utcnow + 
              datetime.timedelta(seconds=time_expire)).strftime("%a, %d %b %Y %H:%M:%S GMT")
else:
    cache_control = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0"

cache_control += ", public" if not session_ and public_ else ", private"

headers = {
    "Expires": expires,
    "Cache-Control": cache_control,
}
current.response.headers.update(headers)
```

## Cache Action Wrapper

### CacheAction Class
Wraps functions to provide transparent caching with flexible key generation.

```python
class CacheAction(object):
    def __init__(self, func, key, time_expire, cache, cache_model):
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__
        self.func = func
        self.key = key
        self.time_expire = time_expire
        self.cache = cache
        self.cache_model = cache_model
    
    def __call__(self, *a, **b):
        """Generate cache key and delegate to cache backend"""
        if not self.key:
            key2 = self.__name__ + ":" + repr(a) + ":" + repr(b)
        else:
            key2 = (self.key.replace("%(name)s", self.__name__)
                           .replace("%(args)s", str(a))
                           .replace("%(vars)s", str(b)))
        
        cache_model = self.cache_model
        if not cache_model or isinstance(cache_model, str):
            cache_model = getattr(self.cache, cache_model or "ram")
        
        return cache_model(key2, lambda a=a, b=b: self.func(*a, **b), self.time_expire)
```

## Utility Functions

### Lazy Cache Decorator
```python
def lazy_cache(key=None, time_expire=None, cache_model="ram"):
    """
    Decorator for caching functions that may be called outside request context
    Automatically resolves cache instance from current context
    """
    def decorator(f, key=key, time_expire=time_expire, cache_model=cache_model):
        key = key or repr(f)
        
        def g(*c, **d):
            from gluon import current
            return current.cache(key, time_expire, cache_model)(f)(*c, **d)
        
        g.__name__ = f.__name__
        return g
    return decorator
```

### Prefix Wrapper
```python
@staticmethod
def with_prefix(cache_model, prefix):
    """
    Create cache model wrapper that automatically prefixes all keys
    Useful for namespace isolation
    """
    return lambda key, f, time_expire=DEFAULT_TIME_EXPIRE, prefix=prefix: \
           cache_model(prefix + key, f, time_expire)
```

## Configuration and Settings

### Default Settings
```python
DEFAULT_TIME_EXPIRE = 300  # 5 minutes default expiration
```

### Memory Management Configuration
```python
# Enable memory-based cleanup when psutil is available
if HAVE_PSUTIL:
    CacheInRam.max_ram_utilization = 90  # Percentage threshold
```

### File System Configuration
```python
# Automatic cache directory creation
folder = os.path.join(folder or request.folder, "cache")
if not os.path.exists(folder):
    os.mkdir(folder)
```

## Performance Optimizations

### Memory Usage Optimization
1. **Automatic Cleanup**: Remove oldest entries when memory exceeds threshold
2. **Garbage Collection**: Explicit garbage collection after cache cleanup
3. **Ordered Storage**: Use OrderedDict for LRU-style eviction
4. **Lazy Initialization**: Initialize cache storage only when needed

### Disk I/O Optimization
1. **File Locking**: Efficient process-level file locking
2. **Pickle Protocol**: Use highest protocol for serialization efficiency
3. **Atomic Operations**: Minimize file I/O through atomic updates
4. **Key Filtering**: Optimize filename generation for platform compatibility

### Concurrency Optimization
1. **Thread-Local Locks**: Per-key locking to minimize contention
2. **Lock Hierarchy**: Consistent lock ordering to prevent deadlocks
3. **Fine-Grained Locking**: Separate locks for different cache operations
4. **Lock Timeout**: Configurable timeout for file lock acquisition

## Usage Examples

### Basic Caching
```python
# Function caching
@cache('expensive_function', 3600, cache.ram)
def expensive_function(param1, param2):
    # Expensive computation
    return result

# Manual caching
def get_user_data(user_id):
    key = f"user_data_{user_id}"
    return cache.ram(key, lambda: db.users[user_id], 1800)
```

### Action Caching
```python
# Controller action caching
@cache.action(time_expire=3600, cache_model=cache.ram, session=False, vars=True)
def public_page():
    # Page content generation
    return dict(content=generate_content())

# Quick notation for common patterns
@cache.action(time_expire=1800, quick='VLP')  # Vars, Lang, Public
def multilingual_page():
    return dict(message=T('Welcome'))
```

### Advanced Patterns
```python
# Conditional caching
def get_cached_data(use_cache=True):
    if use_cache:
        return cache.ram('data_key', expensive_operation, 3600)
    else:
        return expensive_operation()

# Cache invalidation
def update_user(user_id, data):
    # Update database
    db.users[user_id] = data
    # Invalidate related cache
    cache.ram(f'user_{user_id}', None)  # Clear cache entry
```

## Error Handling and Debugging

### Exception Handling
```python
try:
    value = cache.ram(key, function, time_expire)
except Exception as e:
    logger.error(f"Cache operation failed: {e}")
    # Fallback to direct function execution
    value = function()
```

### Statistics and Monitoring
```python
# Access cache statistics
stats = cache.ram.stats.get(app_name, {})
hit_rate = stats.get('hit_total', 0) / (stats.get('hit_total', 0) + stats.get('misses', 0))
print(f"Cache hit rate: {hit_rate:.2%}")
```

### Debugging Tools
```python
# Clear specific cache entries
cache.ram.clear('user_.*')  # Clear all keys matching pattern

# Force cache refresh
cache.ram(key, function, -1)  # Negative time_expire forces refresh

# Inspect cache contents
for key in cache.disk.storage:
    print(f"Cached key: {key}")
```

## Security Considerations

### Cache Poisoning Prevention
1. **Key Validation**: Sanitize cache keys to prevent injection
2. **Data Validation**: Validate cached data before use
3. **Access Control**: Implement proper cache access restrictions
4. **Expiration Management**: Use appropriate expiration times

### Data Protection
1. **Encryption**: Consider encryption for sensitive cached data
2. **Access Logs**: Monitor cache access patterns
3. **Cleanup**: Ensure proper cleanup of temporary cache files
4. **Permissions**: Set appropriate file system permissions

## Best Practices

### Cache Strategy
1. **Cache What's Expensive**: Focus on computationally expensive operations
2. **Appropriate Expiration**: Balance freshness with performance
3. **Cache Invalidation**: Implement proper cache invalidation strategies
4. **Monitoring**: Track cache hit rates and performance metrics

### Memory Management
1. **Size Limits**: Implement appropriate cache size limits
2. **Cleanup Policies**: Use LRU or other appropriate eviction policies
3. **Memory Monitoring**: Monitor memory usage in production
4. **Resource Limits**: Set reasonable limits for cache growth

### Error Handling
1. **Graceful Degradation**: Ensure application works without cache
2. **Fallback Strategies**: Implement fallback mechanisms
3. **Error Logging**: Log cache-related errors appropriately
4. **Recovery Procedures**: Plan for cache corruption recovery

This comprehensive caching system provides robust, scalable, and flexible caching capabilities essential for high-performance web applications in the Gluon framework.