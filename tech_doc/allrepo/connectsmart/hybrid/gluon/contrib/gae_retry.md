# Gluon Contrib GAE Retry Module

## Overview
Google App Engine (GAE) datastore retry mechanism that automatically handles datastore timeouts and concurrent transaction errors. This module provides low-level retry logic with exponential backoff to improve reliability of GAE datastore operations.

## Module Information
- **Module**: `gluon.contrib.gae_retry`
- **Author**: twitter.com/rcb
- **License**: MIT License
- **Platform**: Google App Engine
- **Dependencies**: `google.appengine.api`, `google.appengine.runtime`, `google.appengine.datastore`

## Key Features
- **Automatic Retry**: Handles datastore timeouts transparently
- **Exponential Backoff**: Configurable retry intervals with exponential growth
- **Low-Level Integration**: Wraps GAE's lowest-level datastore API
- **Minimal Footprint**: No interference with Model internals
- **One-Time Setup**: Single initialization call enables retry for entire application

## Main Function

### autoretry_datastore_timeouts()
Patches GAE's datastore API to automatically retry failed operations.

**Signature:**
```python
def autoretry_datastore_timeouts(attempts=5.0, interval=0.1, exponent=2.0)
```

**Parameters:**
- `attempts`: Maximum number of retry attempts (default: 5.0)
- `interval`: Base sleep interval between retries in seconds (default: 0.1)
- `exponent`: Exponential backoff multiplier (default: 2.0)

**Default Retry Schedule:**
With default parameters (5 attempts):
- Attempt 1: 0.1 seconds
- Attempt 2: 0.2 seconds  
- Attempt 3: 0.4 seconds
- Attempt 4: 0.8 seconds
- Attempt 5: 1.6 seconds

## Implementation Details

### API Patching
The function patches `apiproxy_stub_map.MakeSyncCall`, which is the lowest-level synchronous API call method in GAE:

```python
wrapped = apiproxy_stub_map.MakeSyncCall
apiproxy_stub_map.MakeSyncCall = wrapper
```

### Error Handling
Specifically handles these GAE datastore errors:
- `datastore_pb.Error.TIMEOUT`: Datastore operation timeout
- `datastore_pb.Error.CONCURRENT_TRANSACTION`: Transaction conflict error

### Retry Logic
The wrapper function implements the retry mechanism:

1. **Attempt Operation**: Call original datastore API
2. **Error Detection**: Check for retryable errors
3. **Backoff Calculation**: Calculate sleep time using exponential formula
4. **Logging**: Log retry attempts with details
5. **Sleep**: Wait before retry
6. **Retry or Fail**: Continue retrying or raise original exception

### Exponential Backoff Formula
```python
sleep = (exponent ** count) * interval
```

Where:
- `count`: Current retry attempt number (0-based)
- `exponent`: Exponential multiplier 
- `interval`: Base sleep interval

## Usage

### Basic Initialization
```python
from gluon.contrib.gae_retry import autoretry_datastore_timeouts

# Enable automatic retry with defaults
autoretry_datastore_timeouts()
```

### Custom Configuration
```python
# Custom retry parameters
autoretry_datastore_timeouts(
    attempts=3,     # Maximum 3 attempts
    interval=0.2,   # Start with 0.2 second delay
    exponent=1.5    # Gentler exponential growth
)
```

### Integration with Web2py
```python
# In models/db.py or at application startup
from gluon.contrib.gae_retry import autoretry_datastore_timeouts

# Enable retry for all datastore operations
autoretry_datastore_timeouts()

# Now all database operations will automatically retry on timeout
users = db(db.users).select()  # Will retry if timeout occurs
```

## Benefits

### 1. Small Footprint
- No modification of Model or Query internals
- Compatible with future GAE SDK updates
- Minimal code changes required

### 2. Maximum Performance
- Retries at lowest API level
- No repeated serialization or key formatting
- Preserves original request context

### 3. Transparent Operation
- No changes to existing application code
- Automatic handling of common failures
- Preserves original exception types for non-retryable errors

### 4. Configurable Behavior
- Adjustable retry attempts
- Configurable backoff intervals
- Customizable exponential growth

## Error Scenarios

### Retryable Errors
The module handles these specific GAE datastore errors:

**Timeout Errors:**
- Network timeouts to datastore
- Datastore service overload
- Temporary service unavailability

**Concurrent Transaction Errors:**
- Multiple transactions accessing same entity groups
- High contention scenarios
- Transaction rollbacks due to conflicts

### Non-Retryable Errors
All other errors are passed through unchanged:
- Permission errors
- Quota exceeded errors
- Invalid query errors
- Application logic errors

## Logging

### Retry Attempts
Each retry attempt is logged with warning level:
```
Datastore Timeout: retry #1 in 0.1 seconds.
[Original request details on first retry]
```

### Log Information Includes:
- Error type (Timeout or TransactionFailedError)
- Retry attempt number
- Sleep duration before next attempt
- Original request arguments (first retry only)

## Safety Features

### Single Installation
The function includes protection against multiple installations:
```python
setattr(wrapper, '_autoretry_datastore_timeouts', False)
if getattr(wrapped, '_autoretry_datastore_timeouts', True):
    apiproxy_stub_map.MakeSyncCall = wrapper
```

Subsequent calls to `autoretry_datastore_timeouts()` have no effect.

### Failure Limits
- Maximum retry attempts prevent infinite loops
- Original exceptions are preserved and re-raised
- No masking of permanent failures

## Performance Considerations

### Advantages
- **Reliability**: Automatic handling of transient failures
- **Efficiency**: Minimal overhead for successful operations
- **Scalability**: Better handling of high-load scenarios

### Trade-offs
- **Latency**: Additional delays for failed operations
- **Resource Usage**: Extended API call duration during retries
- **Masking**: May hide underlying datastore performance issues

## Best Practices

### Initialization
```python
# Call once at application startup
if os.environ.get('SERVER_SOFTWARE', '').startswith('Google App Engine'):
    autoretry_datastore_timeouts()
```

### Configuration Tuning
```python
# For high-traffic applications
autoretry_datastore_timeouts(attempts=3, interval=0.05)

# For batch operations
autoretry_datastore_timeouts(attempts=7, interval=0.2, exponent=1.8)
```

### Monitoring
```python
import logging

# Enable warning level logging to monitor retries
logging.getLogger().setLevel(logging.WARNING)
```

## Integration Notes

### Web2py Compatibility
- Fully compatible with web2py's DAL
- Works with all database operations
- No changes required to existing code

### GAE Environment
- Only functional on Google App Engine
- Requires GAE SDK for development
- No effect outside GAE environment

### Development vs Production
```python
# Conditional enabling for GAE only
if os.environ.get('SERVER_SOFTWARE', '').startswith('Google App Engine'):
    from gluon.contrib.gae_retry import autoretry_datastore_timeouts
    autoretry_datastore_timeouts()
```

This module significantly improves the reliability of GAE datastore operations by automatically handling common transient failures with minimal performance impact and no code changes required.