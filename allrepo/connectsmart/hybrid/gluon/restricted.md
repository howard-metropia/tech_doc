# Gluon Restricted Module

## Overview

The `restricted.py` module provides a secure execution environment for running application code in the web2py Gluon framework. It implements sandboxed code execution, comprehensive error handling, exception tracking, and debugging capabilities. This module is critical for safely executing user applications while maintaining system security and providing detailed error reporting.

## Key Features

- **Secure Code Execution**: Sandboxed environment for running untrusted code
- **Exception Management**: Comprehensive error tracking and logging
- **Ticket System**: Persistent error storage and retrieval
- **Debug Information**: Detailed stack traces and variable snapshots
- **Database Integration**: Optional database storage for error tickets
- **Development Support**: Enhanced debugging for development environments

## Core Components

### Execution Environment

#### `restricted(ccode, environment=None, layer="Unknown", scode=None)`
Executes code in a controlled environment with comprehensive error handling.

**Parameters:**
- `ccode`: Compiled code object to execute
- `environment`: Execution namespace (globals dictionary)
- `layer`: Descriptive name for error identification
- `scode`: Source code for error reporting

**Features:**
- Safe execution with exception capture
- Preserves HTTP exceptions for framework handling
- Prevents RestrictedError obfuscation
- Environment variable injection (`__file__`, `__name__`)

**Security Measures:**
- Sandboxed execution environment
- Exception type filtering
- Memory and resource management
- Debug hook integration

**Usage Example:**
```python
# Compile and execute user code safely
code = compile2(source_code, "controller.py")
environment = {'request': request, 'response': response}
restricted(code, environment, "controller.py", source_code)
```

#### `compile2(code, layer)`
Compiles source code for secure execution.

**Features:**
- Standard Python compilation with exec mode
- Layer identification for debugging
- Exception propagation

### Error Management

#### `RestrictedError` Class
Specialized exception class for wrapping execution errors.

**Attributes:**
- `layer`: Description of error location
- `code`: Source code causing the error
- `output`: Error message for user display
- `environment`: Execution context at time of error
- `traceback`: Formatted exception traceback
- `snapshot`: Detailed debugging information

**Initialization:**
```python
error = RestrictedError(
    layer="controller.py",
    code=source_code,
    output="Error message",
    environment=execution_env
)
```

**Error Processing:**
- Automatic traceback generation
- Context snapshot creation
- Safe error message formatting
- Exception chaining prevention

#### Error Logging and Retrieval

##### `log(request)`
Logs the error and generates a unique ticket ID.

**Features:**
- Unique ticket generation using request UUID
- Database or file-based storage
- Console output for development
- Secure error data serialization

**Returns:** Ticket ID for error retrieval

##### `load(request, app, ticket_id)`
Loads previously logged error information.

**Features:**
- Ticket-based error retrieval
- Cross-application error access
- Secure deserialization
- Missing ticket handling

### Ticket Storage System

#### `TicketStorage` Class
Manages persistent storage of error tickets.

**Storage Options:**
- **File-based**: Local filesystem storage in `errors/` directory
- **Database**: Centralized storage with structured tables
- **Hybrid**: Automatic selection based on configuration

**Initialization:**
```python
# File-based storage
storage = TicketStorage()

# Database storage
storage = TicketStorage(db=database, tablename="error_tickets")
```

#### Storage Methods

##### `store(request, ticket_id, ticket_data)`
Stores error information persistently.

**Features:**
- Automatic storage type selection
- Atomic write operations
- Serialization handling
- Error recovery mechanisms

##### `_store_in_db(request, ticket_id, ticket_data)`
Database-specific storage implementation.

**Features:**
- Dynamic table creation
- Application-specific table naming
- Transaction management
- Connection handling

**Table Structure:**
```python
table = db.define_table(
    tablename + "_" + app,
    db.Field("ticket_id", length=100),
    db.Field("ticket_data", "text"),
    db.Field("created_datetime", "datetime")
)
```

##### `_store_on_disk(request, ticket_id, ticket_data)`
File-based storage implementation.

**Features:**
- Application-specific error directories
- Pickle serialization
- File locking for concurrent access
- Path resolution and validation

##### `load(request, app, ticket_id)`
Retrieves stored error information.

**Features:**
- Multi-storage support
- Error handling for missing tickets
- Automatic deserialization
- Cross-application access

## Debug Information System

### `snapshot(info=None, context=5, code=None, environment=None)`
Creates detailed debugging information for exceptions.

**Features:**
- Stack frame analysis
- Variable inspection
- Source code context
- Exception details
- Environment variable capture

**Information Captured:**
- Python version and executable path
- Exception type and value
- Stack frames with local variables
- Source code context around error
- Web2py-specific objects (request, response, session)

**Frame Information:**
```python
frame_info = {
    'file': '/path/to/file.py',
    'func': 'function_name',
    'call': 'function(arg1=value1, arg2=value2)',
    'lines': {line_num: 'source code'},
    'lnum': current_line_number,
    'dump': {'var_name': 'repr(value)'}
}
```

### Enhanced Debugging

#### Development Environment Integration
- Wing IDE debugger support
- Console error output
- Detailed stack traces
- Variable inspection

#### Template Error Handling
- HTML template error detection
- Generated code mapping
- Template-specific error formatting
- Context preservation

## Security Considerations

### Sandboxing
- Controlled execution environment
- Limited global namespace
- Import restrictions
- Resource limitations

### Error Information Security
- Sensitive data filtering
- Safe error message generation
- Environment variable sanitization
- Debug information access control

### File System Security
- Path validation and sanitization
- Directory traversal prevention
- Permission checking
- Atomic operations

## Configuration Options

### Error Storage Configuration
```python
# Database storage
ticket_storage = TicketStorage(
    db=database,
    tablename="application_errors"
)

# File storage (default)
ticket_storage = TicketStorage()
```

### Development Settings
```python
# Enable console output
global_settings.cmd_options.errors_to_console = True

# Debug environment detection
if __debug__ and "WINGDB_ACTIVE" in os.environ:
    # Enhanced debugging enabled
    pass
```

## Usage Patterns

### Controller Execution
```python
def execute_controller(code, environment):
    try:
        compiled_code = compile2(code, "controller")
        restricted(compiled_code, environment, "controller", code)
    except RestrictedError as e:
        ticket_id = e.log(current.request)
        return dict(error=True, ticket=ticket_id)
```

### Error Display
```python
def error():
    """Display error ticket information"""
    ticket_id = request.args(0)
    if ticket_id:
        error = RestrictedError()
        error.load(request, request.application, ticket_id)
        return dict(error=error)
    else:
        raise HTTP(404)
```

### Custom Error Handling
```python
def custom_error_handler(e):
    """Custom error processing"""
    if isinstance(e, RestrictedError):
        # Log to external service
        external_logger.error({
            'layer': e.layer,
            'traceback': e.traceback,
            'snapshot': e.snapshot
        })
        
        # Generate user-friendly message
        user_message = "An error occurred. Please try again."
        return dict(message=user_message)
```

## Performance Considerations

### Memory Management
- Exception object cleanup
- Stack frame reference management
- Snapshot data optimization
- Garbage collection considerations

### Storage Optimization
- Efficient serialization
- Database query optimization
- File I/O minimization
- Concurrent access handling

## Integration Points

### Web2py Framework Integration
- Request/response object access
- Session data preservation
- Template system integration
- Database connection sharing

### External System Integration
- Logging framework compatibility
- Monitoring system hooks
- Error tracking services
- Debug tool integration

## Error Recovery

### Graceful Degradation
- Fallback error storage
- Minimal error information
- Service continuation
- User experience preservation

### Error Analysis
- Pattern recognition
- Frequency analysis
- Performance impact assessment
- Root cause identification

## Usage Examples

### Basic Error Handling
```python
try:
    # Execute potentially problematic code
    code = compile("print('Hello World')", "test", "exec")
    restricted(code, {}, "test_layer")
except RestrictedError as e:
    # Handle the error
    ticket = e.log(request)
    logger.error(f"Error ticket: {ticket}")
```

### Advanced Debugging Setup
```python
def debug_controller(controller_code):
    """Enhanced controller execution with debugging"""
    environment = {
        'request': current.request,
        'response': current.response,
        'session': current.session,
        'db': current.db
    }
    
    try:
        compiled = compile2(controller_code, f"{request.controller}.py")
        restricted(compiled, environment, request.controller, controller_code)
    except RestrictedError as e:
        # Create detailed debug information
        debug_info = {
            'controller': request.controller,
            'function': request.function,
            'ticket': e.log(request),
            'snapshot': e.snapshot,
            'environment_keys': list(environment.keys())
        }
        
        # Store debug session
        session.last_error = debug_info
        raise HTTP(500, "Internal Server Error")
```

This module ensures that web2py applications can execute user code safely while providing comprehensive error tracking and debugging capabilities essential for application development and maintenance.