# test_cache.py

## Overview
This file contains comprehensive unit tests for the web2py caching system. It tests various caching mechanisms including in-memory caching, disk-based caching, and database query caching with different storage backends and configuration options.

## Purpose
- Tests CacheInRam (in-memory) caching functionality
- Tests CacheOnDisk (file-based) caching functionality
- Validates cache expiration and clearing mechanisms
- Tests cache corruption handling and recovery
- Tests database query caching integration
- Validates cache prefixing and regex-based clearing

## Key Classes and Methods

### Module Setup/Teardown Functions

#### `setUpModule()`
Global setup for all cache tests:
- Changes to appropriate working directory if needed
- Ensures proper test environment setup

#### `tearDownModule()`
Global cleanup after all tests:
- Restores original working directory
- Removes temporary test database files

### TestCache Class
Comprehensive test suite for all caching mechanisms.

#### Test Methods

##### `test_CacheInRam(self)`
Tests in-memory caching functionality.

**Basic Caching Operations:**
- **Cache Storage**: Tests storing values with different expiration times
- **Cache Retrieval**: Validates cached values are returned correctly
- **Cache Expiration**: Tests immediate expiration (time=0) vs. persistent (time=100)
- **Selective Clearing**: Tests clearing specific keys vs. all keys
- **Key Deletion**: Tests explicit key deletion using `cache(key, None)`

**Advanced Features:**
- **Singleton Behavior**: Validates cache instance sharing
- **Increment Operation**: Tests atomic increment functionality
- **Type Handling**: Tests increment with different data types

**Test Sequence:**
```python
cache("a", lambda: 1, 0)      # Returns 1, expires immediately
cache("a", lambda: 2, 100)    # Returns 1 (cached), doesn't expire
cache.clear("a")              # Clears specific key
cache("a", lambda: 2, 100)    # Returns 2 (new value)
cache.increment("a")          # Increments to 3
```

##### `test_CacheOnDisk(self)`
Tests disk-based caching functionality.

**Storage Configuration:**
- Uses Storage object with application and folder settings
- Creates cache files in application's cache directory

**Operations Tested:**
- **File-based Storage**: Tests persistent storage to disk
- **Cache Persistence**: Validates cache survives between instances
- **Same API**: Ensures identical behavior to CacheInRam
- **Singleton Pattern**: Tests disk cache instance sharing

**Test Pattern:**
- Same test sequence as CacheInRam
- Validates disk persistence and file management
- Tests cross-instance cache sharing

##### `test_corrupt_CacheOnDisk(self)`
Tests cache corruption handling and recovery.

**Corruption Scenarios:**
- **Empty Cache File**: Tests recovery from truncated cache files
- **File System Issues**: Validates graceful degradation
- **Automatic Recovery**: Tests cache rebuild after corruption

**Test Process:**
1. Creates valid cache entry
2. Manually corrupts cache file (truncates to 0 bytes)
3. Validates cache recovers and returns fresh data

##### `test_CacheWithPrefix(self)`
Tests cache key prefixing functionality.

**Prefix Operations:**
- **Prefix Creation**: Tests `cache.with_prefix(cache.ram, "prefix")`
- **Key Namespacing**: Validates prefixed keys are separate from unprefixed
- **Prefix Transparency**: Tests that prefixed cache behaves normally

**Test Validation:**
```python
prefix = cache.with_prefix(cache.ram, "prefix")
prefix("a", lambda: 1, 0)           # Stores with prefix
cache.ram("prefixa", lambda: 2, 100) # Same key, returns prefixed value
```

##### `test_Regex(self)`
Tests regex-based cache clearing.

**Pattern Matching:**
- **Wildcard Clearing**: Tests clearing keys matching regex patterns
- **Selective Clearing**: Validates only matching keys are cleared
- **Pattern Flexibility**: Tests various regex patterns

**Test Sequence:**
```python
cache("a1", lambda: 1, 0)    # Create cache entries
cache("a2", lambda: 2, 100)
cache.clear(regex=r"a*")     # Clear keys matching pattern
```

##### `test_DALcache(self)`
Tests database query caching integration.

**Database Setup:**
- Creates SQLite in-memory database
- Defines test table with sample data
- Tests both RAM and disk caching

**Caching Scenarios:**
- **RAM Caching**: Tests `cache=(cache.ram, 60)`
- **Disk Caching**: Tests `cache=(cache.disk, 60)`
- **Cacheable Queries**: Tests `cacheable=True` parameter
- **Non-cacheable Queries**: Tests default caching behavior

**Validation:**
- **Cache Effectiveness**: Ensures repeated queries return cached results
- **Cross-backend Consistency**: Validates RAM and disk caches return same data
- **Result Format**: Tests cache works with different result formats (CSV)

## Dependencies
- `unittest` - Python testing framework
- `os` - File system operations
- `tempfile` - Temporary directory creation
- `gluon.recfile` - Record file operations
- `gluon.cache` - Caching system components
- `gluon.dal` - Database Abstraction Layer
- `gluon.storage` - Storage utilities

## Cache Components Tested

### CacheInRam
- **Memory-based** caching for fast access
- **Singleton pattern** for shared instances
- **Atomic operations** like increment
- **Selective clearing** by key or pattern

### CacheOnDisk
- **File-based** persistent caching
- **Application-scoped** cache storage
- **Corruption recovery** mechanisms
- **Cross-process** cache sharing

### Cache (Combined)
- **Unified interface** for multiple backends
- **Prefixing support** for namespacing
- **Database integration** for query caching
- **Flexible configuration** options

## Usage Example
```python
from gluon.cache import Cache, CacheInRam, CacheOnDisk
from gluon.storage import Storage

# In-memory caching
cache_ram = CacheInRam()
result = cache_ram("key", lambda: expensive_operation(), 300)

# Disk caching
storage = Storage(application="myapp", folder="applications/myapp")
cache_disk = CacheOnDisk(storage)
result = cache_disk("key", lambda: expensive_operation(), 3600)

# Combined cache system
cache = Cache(storage)
result = cache.ram("key", lambda: operation(), 60)
result = cache.disk("key", lambda: operation(), 3600)

# Database query caching
rows = db(query).select(cache=(cache.ram, 300), cacheable=True)
```

## Integration with web2py Framework

### Database Query Caching
- **Automatic Integration**: Seamless integration with DAL queries
- **Result Caching**: Caches query results, not SQL
- **Cacheable Flag**: Controls which queries can be cached
- **Multiple Backends**: Supports both RAM and disk caching

### Application Integration
- **Application-scoped**: Caches are tied to specific applications
- **Folder-based**: Uses application folder structure
- **Configuration**: Integrates with application settings

### Performance Optimization
- **Query Optimization**: Reduces database load
- **Result Reuse**: Avoids repeated expensive operations
- **Memory Management**: Provides both persistent and temporary caching

## Test Coverage
- **Basic Operations**: Store, retrieve, expire, clear
- **Advanced Features**: Increment, prefix, regex clearing
- **Error Handling**: Corruption recovery, file system issues
- **Integration Testing**: Database query caching
- **Performance Testing**: Cache effectiveness validation
- **Configuration Testing**: Different storage backends

## File Structure
```
gluon/tests/
├── test_cache.py         # This file
└── ... (other test files)
```

This test suite ensures the web2py caching system provides reliable, efficient, and robust caching functionality across different storage backends and use cases.