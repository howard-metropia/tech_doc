# utils.py

## Overview
Utility functions and deprecation handling for PyDAL, providing tools for managing API evolution and parsing database URI parameters.

## Deprecation Management

### RemovedInNextVersionWarning
```python
class RemovedInNextVersionWarning(DeprecationWarning):
    pass
```

**Purpose**: Custom warning class for PyDAL deprecation notices.

**Configuration**:
```python
warnings.simplefilter("always", RemovedInNextVersionWarning)
```
Ensures deprecation warnings are always displayed to developers.

### warn_of_deprecation()
```python
def warn_of_deprecation(old_name, new_name, prefix=None, stack=2):
```

**Purpose**: Issues structured deprecation warnings with consistent formatting.

**Parameters:**
- **old_name**: Deprecated function/method name
- **new_name**: Replacement function/method name
- **prefix**: Optional class or module prefix
- **stack**: Stack level for warning location (default: 2)

**Message Format:**
```
"%(prefix)s.%(old)s is deprecated, use %(new)s instead."
```

**Examples:**
```python
# Basic deprecation
warn_of_deprecation('old_function', 'new_function')
# Output: "old_function is deprecated, use new_function instead."

# With class prefix
warn_of_deprecation('old_method', 'new_method', 'MyClass')
# Output: "MyClass.old_method is deprecated, use new_method instead."
```

### deprecated Decorator
```python
class deprecated(object):
    def __init__(self, old_method_name, new_method_name, class_name=None, s=0):
```

**Purpose**: Decorator for marking methods as deprecated while maintaining functionality.

**Parameters:**
- **old_method_name**: Name of deprecated method
- **new_method_name**: Name of replacement method
- **class_name**: Optional class name for context
- **s**: Additional stack level adjustment

**Usage Example:**
```python
class MyClass:
    @deprecated('old_method', 'new_method', 'MyClass')
    def old_method(self, arg):
        return self.new_method(arg)
    
    def new_method(self, arg):
        return f"processed: {arg}"

# Usage triggers warning
obj = MyClass()
result = obj.old_method("test")  # Warning: MyClass.old_method is deprecated, use new_method instead.
```

**Functionality:**
1. **Warning Emission**: Automatically warns when deprecated method is called
2. **Method Preservation**: Maintains original method functionality
3. **Stack Tracking**: Provides accurate warning location information

## URI Parsing

### split_uri_args()
```python
def split_uri_args(query, separators="&?", need_equal=False):
```

**Purpose**: Parses query string arguments from database URIs into dictionary format.

**Parameters:**
- **query**: Query string to parse
- **separators**: Characters that separate arguments (default: "&?")
- **need_equal**: Whether equals sign is required for all arguments

**Return Value**: Dictionary with argument keys and values.

#### Parsing Modes

##### Standard Mode (need_equal=False)
```python
# Regex pattern for optional equals
regex_arg_val = "(?P<argkey>[^=%s]+)(=(?P<argvalue>[^%s]*))?[%s]?"
```

**Features:**
- Arguments can have optional values
- Supports flags without values
- Handles various separator characters

**Examples:**
```python
# Arguments with values
result = split_uri_args("host=localhost&port=3306&ssl")
# Returns: {'host': 'localhost', 'port': '3306', 'ssl': None}

# Mixed separators
result = split_uri_args("user=admin?password=secret&timeout=30")
# Returns: {'user': 'admin', 'password': 'secret', 'timeout': '30'}
```

##### Strict Mode (need_equal=True)
```python
# Regex pattern requiring equals
regex_arg_val = "(?P<argkey>[^=]+)=(?P<argvalue>[^%s]*)[%s]?"
```

**Features:**
- All arguments must have values
- Enforces key=value format
- Stricter parsing for well-formed URIs

**Examples:**
```python
# All arguments must have values
result = split_uri_args("host=localhost&port=3306", need_equal=True)
# Returns: {'host': 'localhost', 'port': '3306'}

# Invalid: flags without values are ignored
result = split_uri_args("host=localhost&ssl&port=3306", need_equal=True)
# Returns: {'host': 'localhost', 'port': '3306'}  # 'ssl' ignored
```

### Use Cases

#### Database Connection Parsing
```python
# Parse database URI arguments
uri = "mysql://user:pass@host/db?charset=utf8&ssl=true&timeout=30"
query_part = uri.split('?', 1)[1]  # "charset=utf8&ssl=true&timeout=30"
args = split_uri_args(query_part)
# Returns: {'charset': 'utf8', 'ssl': 'true', 'timeout': '30'}
```

#### Adapter Configuration
```python
# Parse adapter-specific arguments
adapter_args = split_uri_args("engine=InnoDB&charset=utf8mb4&isolation=READ_COMMITTED")
# Returns: {'engine': 'InnoDB', 'charset': 'utf8mb4', 'isolation': 'READ_COMMITTED'}
```

#### Feature Flags
```python
# Parse feature flags (with optional values)
features = split_uri_args("debug&verbose=2&trace")
# Returns: {'debug': None, 'verbose': '2', 'trace': None}
```

## Integration with PyDAL

### Deprecation Strategy
PyDAL uses the deprecation utilities to:
- **Method Evolution**: Gradually replace old APIs with new ones
- **Backward Compatibility**: Maintain old methods while warning users
- **Version Management**: Provide clear upgrade paths between versions

### URI Processing
The URI parsing functionality supports:
- **Database Adapters**: Parse connection string arguments
- **Configuration Options**: Extract adapter-specific settings
- **Connection Pooling**: Parse pool configuration parameters
- **SSL/Security Settings**: Handle security-related URI parameters

## Regular Expression Details

### Argument Parsing Patterns

#### Optional Equals Pattern
```python
"(?P<argkey>[^=%s]+)(=(?P<argvalue>[^%s]*))?[%s]?"
```

**Components:**
- `(?P<argkey>[^=%s]+)`: Captures argument key (required)
- `(=(?P<argvalue>[^%s]*))?`: Captures optional value after equals
- `[%s]?`: Optional separator at end

#### Required Equals Pattern
```python
"(?P<argkey>[^=]+)=(?P<argvalue>[^%s]*)[%s]?"
```

**Components:**
- `(?P<argkey>[^=]+)`: Captures argument key (required)
- `=(?P<argvalue>[^%s]*)`: Captures value after required equals
- `[%s]?`: Optional separator at end

## Error Handling
- **Malformed URIs**: Gracefully handles malformed query strings
- **Missing Values**: Handles arguments without values appropriately
- **Special Characters**: Properly escapes separator characters in regex

## Performance Considerations
- **Regex Compilation**: Patterns are dynamically generated for flexibility
- **Single Pass**: Parses entire query string in one regex operation
- **Memory Efficient**: Returns simple dictionary without complex objects

## Usage Examples

### Complete URI Processing
```python
def process_database_uri(uri):
    if '?' in uri:
        base_uri, query = uri.split('?', 1)
        args = split_uri_args(query)
        return base_uri, args
    return uri, {}

# Example usage
uri = "postgres://user:pass@localhost/mydb?sslmode=require&connect_timeout=10"
base, args = process_database_uri(uri)
# base: "postgres://user:pass@localhost/mydb"
# args: {'sslmode': 'require', 'connect_timeout': '10'}
```

### Adapter Configuration
```python
def configure_adapter(adapter_args_string):
    args = split_uri_args(adapter_args_string)
    config = {}
    
    for key, value in args.items():
        # Convert string values to appropriate types
        if value is None:
            config[key] = True  # Flag parameters
        elif value.isdigit():
            config[key] = int(value)  # Numeric parameters
        else:
            config[key] = value  # String parameters
    
    return config
```

## Notes
- Essential for PyDAL's backward compatibility strategy
- Provides clean deprecation warnings for API evolution
- Enables flexible URI parsing for database connections
- Supports various database adapter configuration needs
- Critical for maintaining stable public APIs while evolving internals