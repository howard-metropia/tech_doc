# test_storage.py

## Overview
This file contains unit tests for web2py's storage utilities including Storage objects, List containers, and various data structure implementations used throughout the framework.

## Purpose
- Tests Storage object functionality and attribute access
- Validates List container operations and methods
- Tests thread-safe storage implementations
- Verifies serialization and persistence of storage objects
- Tests storage object inheritance and extensibility

## Key Features Tested

### Storage Objects
- **Attribute Access**: Dictionary-like objects with attribute access
- **Dynamic Properties**: Dynamic attribute creation and modification
- **Serialization**: Pickle and JSON serialization support
- **Thread Safety**: Concurrent access safety

### List Containers
- **Enhanced Lists**: Extended list functionality
- **Method Chaining**: Chainable list operations
- **Type Safety**: Type checking and validation
- **Performance**: Optimized list operations

## Integration with web2py Framework
Storage objects are used throughout web2py for:
- **Request/Response**: HTTP request and response objects
- **Session Management**: Session data storage
- **Configuration**: Application configuration storage
- **Template Variables**: Template context variables

## Usage Example
```python
from gluon.storage import Storage, List

# Storage object usage
data = Storage(name='John', age=30)
print(data.name)  # 'John'
data.email = 'john@example.com'
print(data['email'])  # 'john@example.com'

# List container usage
my_list = List([1, 2, 3])
my_list.append(4)
print(my_list)  # [1, 2, 3, 4]
```

This test suite ensures web2py's storage utilities provide reliable, efficient data structures for framework internal operations and application development.