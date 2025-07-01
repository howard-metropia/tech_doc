# Gluon Contrib Redis Utils Module

## Overview
Redis utility functions for web2py applications. Provides helper functions and utilities for common Redis operations, connection management, and integration patterns.

## Module Information
- **Module**: `gluon.contrib.redis_utils`
- **Dependencies**: redis-py
- **Purpose**: Redis utility functions
- **Use Case**: Redis integration helpers

## Key Features
- **Connection Management**: Redis connection utilities
- **Common Operations**: Helper functions for Redis operations
- **Pattern Implementation**: Common Redis patterns
- **Error Handling**: Robust error handling utilities
- **Configuration**: Redis configuration helpers

## Basic Usage

### Connection Utilities
```python
from gluon.contrib.redis_utils import RedisUtils

# Create Redis utilities instance
redis_utils = RedisUtils(
    host='localhost',
    port=6379,
    db=0
)

# Test connection
if redis_utils.test_connection():
    print("Redis connection successful")
```

### Common Operations
```python
# Set with expiration
redis_utils.set_with_expiry('key', 'value', 3600)

# Get with default
value = redis_utils.get_or_default('key', 'default_value')

# Atomic increment
new_value = redis_utils.increment_counter('page_views')

# Distributed lock
with redis_utils.distributed_lock('resource_lock', timeout=30):
    # Critical section
    perform_exclusive_operation()
```

This module provides essential utilities for Redis integration in web2py applications.