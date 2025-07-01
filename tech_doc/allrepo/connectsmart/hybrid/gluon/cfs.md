# Gluon Cached File System Module (`cfs.py`)

## Overview
The Cached File System (CFS) module provides intelligent file caching functionality for the Gluon web framework. It's designed to cache filtered file content (typically compiled Python bytecode) based on file modification times, with thread-safe operations optimized for high-performance web applications.

## Architecture

### Core Dependencies
```python
from os import stat
from gluon._compat import thread
from gluon.fileutils import read_file
```

### Global Cache Structure
```python
cfs = {}  # Cache storage dictionary
cfs_lock = thread.allocate_lock()  # Thread safety lock
```

## Cache Implementation

### Cache Data Structure
```
cfs = {
    "cache_key": (modification_time, cached_data),
    # ... additional cache entries
}
```

Each cache entry contains:
- **Key**: Unique identifier for the cached file
- **Modification Time**: File's last modification timestamp
- **Cached Data**: Processed/filtered file content

### Thread Safety
- **Allocation Lock**: `thread.allocate_lock()` for thread-safe operations
- **Acquire/Release Pattern**: Proper lock management around cache operations
- **Atomic Operations**: Ensures cache consistency in multi-threaded environments

## Core Function

### `getcfs(key, filename, filter=None)`
The primary cache function that implements intelligent file caching with modification time tracking.

```python
def getcfs(key, filename, filter=None):
    """
    Caches the *filtered* file `filename` with `key` until the file is
    modified.

    Args:
        key(str): the cache key
        filename: the file to cache
        filter: is the function used for filtering. Normally `filename` is a
            .py file and `filter` is a function that bytecode compiles the file.
            In this way the bytecode compiled file is cached. (Default = None)

    This is used on Google App Engine since pyc files cannot be saved.
    """
```

#### Implementation Logic

##### 1. File Modification Check
```python
try:
    t = stat(filename).st_mtime
except OSError:
    return filter() if callable(filter) else ""
```
- Retrieves file modification time
- Handles missing files gracefully
- Returns filtered result or empty string on error

##### 2. Cache Lookup
```python
cfs_lock.acquire()
item = cfs.get(key, None)
cfs_lock.release()
if item and item[0] == t:
    return item[1]
```
- Thread-safe cache retrieval
- Compares stored modification time with current
- Returns cached data if file unchanged

##### 3. Content Processing
```python
if not callable(filter):
    data = read_file(filename)
else:
    data = filter()
```
- Reads raw file content if no filter provided
- Executes filter function for processed content
- Common use case: bytecode compilation

##### 4. Cache Storage
```python
cfs_lock.acquire()
cfs[key] = (t, data)
cfs_lock.release()
return data
```
- Thread-safe cache update
- Stores modification time and processed data
- Returns processed content

## Use Cases

### Python Bytecode Compilation
```python
def compile_filter():
    return compile(read_file(python_file), python_file, 'exec')

bytecode = getcfs("module_key", "module.py", compile_filter)
```

### Template Caching
```python
def template_filter():
    return parse_template(template_file)

parsed_template = getcfs("template_key", "template.html", template_filter)
```

### Configuration File Caching
```python
def config_filter():
    return json.loads(read_file(config_file))

config = getcfs("config_key", "config.json", config_filter)
```

## Performance Characteristics

### Cache Hit Performance
- **O(1) Lookup**: Dictionary-based cache access
- **Minimal Overhead**: Simple modification time comparison
- **Memory Efficient**: Stores only processed content

### Cache Miss Performance
- **File System Access**: Single `stat()` call for modification time
- **Filter Execution**: Only when file changes detected
- **Thread Synchronization**: Minimal lock contention

### Memory Management
- **Persistent Cache**: Survives across requests
- **No Automatic Cleanup**: Cache grows with unique keys
- **Manual Management**: Application responsible for cache limits

## Threading Considerations

### Thread Safety Features
```python
cfs_lock.acquire()
try:
    # Critical section operations
    item = cfs.get(key, None)
    # or
    cfs[key] = (t, data)
finally:
    cfs_lock.release()
```

### Concurrency Benefits
- **Multi-threaded Web Server**: Safe for concurrent requests
- **Shared Cache**: All threads benefit from cached content
- **Lock Granularity**: Single global lock (simple but effective)

### Performance Implications
- **Lock Contention**: Potential bottleneck with high concurrency
- **Brief Lock Duration**: Minimal impact on performance
- **Read-Heavy Workload**: Optimized for typical web application patterns

## Integration Points

### Google App Engine Optimization
```python
# This is used on Google App Engine since pyc files cannot be saved.
```
- **GAE Constraint**: Cannot write .pyc files to filesystem
- **Memory Compilation**: Caches bytecode in memory
- **Performance Boost**: Avoids repeated compilation

### Web2py Framework Integration
- **Module Loading**: Caches compiled Python modules
- **Template Engine**: Caches parsed templates
- **Configuration**: Caches processed configuration files

### File System Operations
```python
from gluon.fileutils import read_file
```
- **Consistent Interface**: Uses framework's file utilities
- **Cross-platform**: Handles path and encoding issues
- **Error Handling**: Integrates with framework error handling

## Usage Patterns

### Development Environment
```python
# Frequent file changes - cache invalidation ensures fresh content
dev_content = getcfs("dev_key", "development.py", compile_filter)
```

### Production Environment
```python
# Stable files - cache hits provide performance benefits
prod_content = getcfs("prod_key", "production.py", compile_filter)
```

### Dynamic Content
```python
# Files that change based on external factors
dynamic_content = getcfs("dynamic_key", "dynamic.py", 
                        lambda: process_dynamic_file())
```

## Error Handling

### File Access Errors
```python
try:
    t = stat(filename).st_mtime
except OSError:
    return filter() if callable(filter) else ""
```
- **Graceful Degradation**: Returns processed content or empty string
- **No Exception Propagation**: Handles missing files internally
- **Fallback Behavior**: Executes filter function on error

### Filter Function Errors
- **Unhandled Exceptions**: Filter function errors propagate to caller
- **Caller Responsibility**: Application must handle filter failures
- **Clean State**: Cache remains unchanged on filter errors

## Cache Management

### Cache Key Strategy
- **Unique Keys**: Application responsible for unique key generation
- **Hierarchical Keys**: Support for namespace-like key organization
- **String Keys**: Simple string-based key system

### Cache Invalidation
- **Automatic**: Based on file modification time
- **Manual**: No built-in manual invalidation
- **Granular**: Per-file invalidation based on modification time

### Memory Considerations
- **Unbounded Growth**: No automatic cache size limits
- **Memory Monitoring**: Application should monitor cache size
- **Selective Clearing**: No built-in cache eviction policies

## Design Patterns

### Lazy Loading
```python
def lazy_filter():
    # Expensive operation only executed when needed
    return expensive_processing()

content = getcfs("lazy_key", "file.txt", lazy_filter)
```

### Dependency Tracking
```python
def dependency_aware_filter():
    # Check dependencies and invalidate if needed
    if dependencies_changed():
        return reprocess_with_dependencies()
    return cached_result()
```

### Error Recovery
```python
def robust_filter():
    try:
        return primary_processing()
    except Exception:
        return fallback_processing()
```

This module provides a simple yet effective caching mechanism that balances performance, simplicity, and thread safety, making it ideal for web applications that need to cache processed file content efficiently.