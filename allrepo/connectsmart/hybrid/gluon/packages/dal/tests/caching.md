# caching.py

## Overview
This file contains comprehensive tests for PyDAL's caching mechanisms, validating query result caching, cache invalidation, and performance improvements through intelligent caching strategies.

## Purpose
- Tests query result caching functionality
- Validates cache invalidation on data changes
- Verifies cache storage backends
- Measures caching performance impact

## Key Features Tested

### Query Caching
- **SELECT Cache**: Result set caching
- **Count Cache**: Aggregate query caching
- **Join Cache**: Complex query result caching
- **Pagination Cache**: Offset/limit query caching

### Cache Backends
- **RAM Cache**: In-memory caching tests
- **Redis Cache**: Distributed cache testing
- **Disk Cache**: File-based cache validation
- **Custom Cache**: User-defined cache implementations

## Cache Operations

### Cache Management
- **cache.ram**: Memory cache operations
- **cache.disk**: Filesystem cache testing
- **cache.redis**: Redis backend integration
- **cache.clear()**: Cache invalidation testing

### Caching Strategies
```python
# Time-based caching
db(query).select(cache=(cache.ram, 60))

# Model-based caching
db(query).select(cache=(cache.disk, 3600), 
                 cacheable=True)

# Conditional caching
db(query).select(cache=(cache.redis, 300),
                 cache_key='custom_key')
```

## Performance Testing

### Cache Effectiveness
- Query execution time comparison
- Cache hit/miss ratio analysis
- Memory usage monitoring
- Concurrent access testing

This caching test suite ensures PyDAL's caching layer provides reliable performance improvements while maintaining data consistency.