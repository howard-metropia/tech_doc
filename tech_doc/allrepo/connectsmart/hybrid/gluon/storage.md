# Gluon Storage Module

## Overview

The `storage.py` module provides flexible data structure classes for the web2py Gluon framework. It implements dictionary-like containers with attribute-style access, specialized list containers, and persistent storage utilities. These classes serve as the foundation for request/response objects, settings management, and data manipulation throughout the framework.

## Key Features

- **Attribute-Style Access**: Dictionary objects accessible via dot notation
- **Flexible Data Structures**: Enhanced dictionaries with specialized behaviors
- **Persistent Storage**: File-based storage with locking mechanisms
- **List Containers**: Callable lists with bounds checking and type casting
- **Settings Management**: Lockable configuration containers
- **Internationalization Support**: Message containers with translation integration

## Core Components

### Primary Storage Classes

#### `Storage` Class
Enhanced dictionary allowing both `obj.foo` and `obj['foo']` access patterns.

**Key Features:**
- Attribute-style access (`obj.key` equivalent to `obj['key']`)
- Returns `None` for missing keys instead of raising KeyError
- Setting attribute to `None` deletes the key
- Provides specialized list-handling methods

**Basic Usage:**
```python
>>> o = Storage(a=1, b=2)
>>> o.a
1
>>> o['a']
1
>>> o.c  # Returns None instead of KeyError
None
>>> o.c = 3
>>> o.c
3
>>> del o.c
>>> o.c
None
```

**List Handling Methods:**

##### `getlist(key)`
Returns a storage value as a list, handling various data types consistently.

**Behavior:**
- Lists/tuples returned as-is
- `None` returns empty list `[]`
- Single values wrapped in list `[value]`

**Example:**
```python
>>> request.vars = Storage()
>>> request.vars.x = 'abc'
>>> request.vars.y = ['abc', 'def']
>>> request.vars.getlist('x')
['abc']
>>> request.vars.getlist('y')
['abc', 'def']
>>> request.vars.getlist('z')
[]
```

##### `getfirst(key, default=None)`
Returns the first value from a list or the value itself.

**Usage:**
```python
>>> request.vars.getfirst('y')  # ['abc', 'def']
'abc'
>>> request.vars.getfirst('missing')
None
```

##### `getlast(key, default=None)`
Returns the last value from a list or the value itself.

**Usage:**
```python
>>> request.vars.getlast('y')  # ['abc', 'def']
'def'
```

#### `StorageList` Class
Storage variant where missing elements default to empty lists instead of `None`.

**Features:**
- Automatic list creation for missing keys
- Useful for accumulating values
- Maintains Storage attribute access

**Usage:**
```python
>>> sl = StorageList()
>>> sl.items  # Automatically creates empty list
[]
>>> sl.items.append('first')
>>> sl.items
['first']
```

#### `FastStorage` Class
Optimized Storage implementation with direct `__dict__` mapping.

**Performance Benefits:**
- Faster attribute access
- Direct dictionary mapping
- Reduced memory overhead

**Limitations:**
- Causes memory leaks due to Python bug #1469629
- Retained for compatibility but not recommended for production

### Settings Management

#### `Settings` Class
Lockable configuration container extending Storage.

**Features:**
- Key existence enforcement
- Value modification prevention
- Configuration validation

**Usage:**
```python
>>> settings = Settings()
>>> settings.lock_keys = True
>>> settings.database_url = "sqlite://test.db"
>>> settings.debug = True
>>> settings.lock_keys = False  # Only way to add new keys
>>> settings.new_key = "value"  # Would raise SyntaxError if lock_keys=True
```

**Security Features:**
- Prevents accidental configuration changes
- Enforces predefined configuration schema
- Raises `SyntaxError` for violations

#### `Messages` Class
Internationalization-aware settings container.

**Features:**
- Automatic translation of string values
- Integration with web2py's T() function
- Dynamic language switching

**Usage:**
```python
>>> messages = Messages(T)  # T is translation function
>>> messages.welcome = "Welcome to our site"
>>> messages.welcome  # Returns T("Welcome to our site")
```

### List Containers

#### `List` Class
Callable list with enhanced bounds checking and type casting.

**Features:**
- Callable interface: `list(index)`
- Returns `None` for out-of-bounds access
- Type casting with error handling
- Redirect/error handling for validation failures

**Method Signature:**
```python
def __call__(self, i, default=DEFAULT, cast=None, otherwise=None)
```

**Parameters:**
- `i`: List index to access
- `default`: Value to return if index not found
- `cast`: Type casting function (int, str, etc.)
- `otherwise`: Error handling strategy

**Error Handling Options:**
- `None`: Raises HTTP 404
- `str`: Redirects to specified URL
- `callable`: Executes function

**Usage Examples:**
```python
>>> args = List(['1', '2', 'abc'])
>>> args(0, cast=int)  # Returns 1
1
>>> args(5, default=0)  # Returns 0 for out-of-bounds
0
>>> args(2, cast=int, otherwise='http://error.com')  # Redirects on cast failure
```

### Persistent Storage

#### `load_storage(filename)`
Loads Storage object from pickle file with file locking.

**Features:**
- Thread-safe file access using portalocker
- Automatic pickle deserialization
- Exception handling and cleanup

**Usage:**
```python
>>> data = load_storage('config.pkl')
>>> print(data.database_url)
```

#### `save_storage(storage, filename)`
Saves Storage object to pickle file with file locking.

**Features:**
- Atomic write operations
- File locking prevents corruption
- Converts Storage to dict for serialization

**Usage:**
```python
>>> config = Storage(debug=True, port=8000)
>>> save_storage(config, 'config.pkl')
```

## Advanced Features

### Serialization Support

#### Custom Pickle Registration
Storage objects have custom pickle serialization for compatibility.

```python
def pickle_storage(s):
    return Storage, (dict(s),)

copyreg.pickle(Storage, pickle_storage)
```

### Type Compatibility

#### Pickable Types
The module defines compatible types for serialization:

**Python 2:**
```python
PICKABLE = (str, int, long, float, bool, list, dict, tuple, set)
```

**Python 3:**
```python
PICKABLE = (str, int, float, bool, list, dict, tuple, set)
```

## Integration Patterns

### Request/Response Objects
```python
# Typical web2py request object structure
request = Storage()
request.vars = Storage()  # GET/POST parameters
request.args = List()     # URL path components
request.env = Storage()   # Environment variables
```

### Configuration Management
```python
# Application settings
settings = Settings()
settings.database_uri = "mysql://user:pass@host/db"
settings.mail_server = "smtp.gmail.com:587"
settings.lock_keys = True  # Prevent accidental additions
```

### Form Data Processing
```python
# Handle form data with multiple values
form_data = Storage()
form_data.update(request.vars)

# Get all selected checkboxes
selected_items = form_data.getlist('items')

# Get first uploaded file
uploaded_file = form_data.getfirst('file_upload')
```

## Performance Considerations

### Memory Management
- Storage objects have minimal memory overhead
- List objects provide efficient bounds checking
- FastStorage offers performance at cost of memory leaks

### File I/O Optimization
- Atomic write operations prevent corruption
- File locking ensures concurrent access safety
- Pickle protocol optimization for speed

## Error Handling

### Bounds Checking
```python
# Safe list access
args = List(['a', 'b', 'c'])
value = args(10)  # Returns None, no exception
```

### Type Casting Errors
```python
# Graceful type conversion
try:
    user_id = args(0, cast=int, otherwise=lambda: redirect('/error'))
except ValueError:
    # Handle conversion failure
    pass
```

### Configuration Validation
```python
# Prevent configuration errors
try:
    settings.invalid_key = "value"
except SyntaxError:
    # Key not allowed
    pass
```

## Usage Examples

### Web Request Processing
```python
def index():
    # Access URL arguments safely
    page = request.args(0, default=1, cast=int)
    category = request.args(1, default='all')
    
    # Process form data
    search_terms = request.vars.getlist('q')
    sort_order = request.vars.getfirst('sort', 'name')
    
    return dict(page=page, category=category, terms=search_terms)
```

### Configuration Setup
```python
# Initialize application settings
config = Settings()
config.update({
    'db_uri': 'sqlite://app.db',
    'secret_key': 'your-secret-key',
    'debug': False,
    'mail_sender': 'noreply@example.com'
})
config.lock_keys = True  # Prevent modifications

# Save configuration
save_storage(config, 'app_config.pkl')
```

### Internationalization
```python
# Set up translated messages
messages = Messages(T)  # T is translation function
messages.update({
    'welcome': 'Welcome to our application',
    'login_required': 'Please log in to continue',
    'error_occurred': 'An error occurred'
})

# Use in templates
{{=messages.welcome}}  # Automatically translated
```

## Thread Safety

### File Operations
- `load_storage()` and `save_storage()` use file locking
- Prevents corruption during concurrent access
- Automatic cleanup on exceptions

### Memory Operations
- Storage objects are not inherently thread-safe
- Use appropriate locking for shared access
- Consider using thread-local storage for request data

This module provides the foundational data structures that make web2py's flexible and intuitive API possible, enabling clean separation between data access patterns and business logic.