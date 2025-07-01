# Gluon Contrib SimpleJSON Module

## Overview
SimpleJSON library for web2py applications providing fast JSON encoding and decoding. Offers an alternative to Python's built-in json module with better performance and compatibility across Python versions.

## Module Information
- **Module**: `gluon.contrib.simplejson`
- **Purpose**: JSON serialization/deserialization
- **Performance**: Optimized JSON processing
- **Compatibility**: Python 2/3 compatible

## Key Features
- **High Performance**: Faster than standard library json
- **Unicode Support**: Proper Unicode handling
- **Customizable**: Configurable encoding options
- **Streaming**: Support for large JSON documents
- **Standards Compliant**: RFC 4627 compliant

## Basic Usage

### JSON Encoding
```python
from gluon.contrib.simplejson import dumps

# Basic encoding
data = {'name': 'John', 'age': 30, 'city': 'New York'}
json_string = dumps(data)

# Pretty printing
json_pretty = dumps(data, indent=2, sort_keys=True)
```

### JSON Decoding
```python
from gluon.contrib.simplejson import loads

# Basic decoding
json_string = '{"name": "John", "age": 30}'
data = loads(json_string)
```

### Web2py API Integration
```python
def api_endpoint():
    """JSON API endpoint using simplejson"""
    from gluon.contrib.simplejson import dumps
    
    data = {
        'users': [
            {'id': 1, 'name': 'John', 'email': 'john@example.com'},
            {'id': 2, 'name': 'Jane', 'email': 'jane@example.com'}
        ],
        'total': 2,
        'timestamp': str(datetime.datetime.now())
    }
    
    response.headers['Content-Type'] = 'application/json'
    return dumps(data, indent=2)
```

This module provides enhanced JSON capabilities for web2py applications requiring high-performance JSON processing.