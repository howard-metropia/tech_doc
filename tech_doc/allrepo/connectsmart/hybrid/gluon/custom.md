# Gluon Custom Exception Handling Module Documentation

## Overview
The `custom.py` module provides specialized exception handling and response formatting for the Gluon web framework. It implements custom error processing, output parsing, and JSON-formatted error responses with comprehensive logging capabilities.

## Module Information
- **File**: `allrepo/connectsmart/hybrid/gluon/custom.py`
- **Component**: Web2py Framework Custom Exception Handler  
- **Purpose**: Exception processing and error response generation
- **Dependencies**: sys, re, json, traceback, logging, gluon.http
- **Integration**: ConnectSmart platform error handling

## Key Components

### Core Functions

#### extract_output()
```python
def extract_output(output):
    """Extract error information from RestrictedError output strings"""
    pattern = re.compile(r'<.+ \'.+\.(?P<type>[^.]+)\'> (?P<msg>.*)')
    match = pattern.match(output)
    return match.groupdict()
```

**Purpose:**
- Parses structured error output from web2py RestrictedError
- Extracts error type and message using regex pattern matching
- Returns dictionary with parsed components

**Pattern Analysis:**
- Matches format: `<... 'filename.ext'> error_message`
- Captures file extension as `type`
- Captures remaining text as `msg`

#### extract_exception()
```python
def extract_exception(e):
    """Extract comprehensive exception details for logging and response"""
    detail = {}
    if e.__class__.__name__ == "RestrictedError":
        detail = extract_output(e.output)
        detail['file'] = e.layer
    else:
        cl, exc, tb = sys.exc_info()
        lastCallStack = traceback.extract_tb(tb)[-1]
        detail['type'] = e.__class__.__name__
        detail['msg'] = "error"
        detail['file'] = lastCallStack[0]
    return "%(type)s: %(msg)s in File: %(file)s" % detail
```

**Exception Types Handled:**
1. **RestrictedError**: Web2py-specific restricted execution errors
2. **General Exceptions**: Standard Python exceptions with traceback analysis

**Information Extracted:**
- **type**: Exception class name or extracted type
- **msg**: Error message or "error" default
- **file**: Source file where error occurred

#### exception_handler_response()
```python
def exception_handler_response(e, request, response):
    """Generate standardized JSON error response"""
    response.headers['Content-Type'] = "application/json"
    logger.error("[%s] %s" % (request.env.web2py_original_uri, e.output))
    logger.error(e.traceback)
    content = {
        'result': 'fail',
        'error': {
            'code': 99999,
            'msg': e.output,
        }
    }
    return HTTP(500, json.dumps(content), **response.headers)
```

**Response Structure:**
- **HTTP Status**: 500 Internal Server Error
- **Content-Type**: application/json
- **Body Format**: Standardized JSON error structure

### Error Response Format

#### JSON Structure
```json
{
    "result": "fail",
    "error": {
        "code": 99999,
        "msg": "Detailed error message"
    }
}
```

**Fields:**
- **result**: Always "fail" for error responses
- **error.code**: Standard error code (99999 for general errors)
- **error.msg**: Detailed error message from exception

### Logging Integration

#### Error Logging
```python
logger = logging.getLogger("web2py")

# Log request URI and error output
logger.error("[%s] %s" % (request.env.web2py_original_uri, e.output))

# Log full traceback
logger.error(e.traceback)
```

**Logging Features:**
- **Request Context**: Includes original URI in log messages
- **Error Output**: Logs exception output for debugging
- **Traceback**: Full stack trace for troubleshooting
- **Logger Name**: Uses "web2py" logger for integration

### Usage Examples

#### Basic Exception Handling
```python
try:
    # Some operation that might fail
    result = risky_operation()
except Exception as e:
    # Extract exception details
    error_details = extract_exception(e)
    logger.error("Operation failed: %s" % error_details)
```

#### RestrictedError Processing
```python
# For web2py RestrictedError instances
try:
    exec(code_string)
except RestrictedError as e:
    # Extract structured error information
    error_info = extract_output(e.output)
    print("Error type:", error_info.get('type'))
    print("Error message:", error_info.get('msg'))
```

#### HTTP Error Response
```python
# In controller or error handler
def handle_api_error(e, request, response):
    return exception_handler_response(e, request, response)
    # Returns HTTP 500 with JSON error body
```

### Integration Points

#### Web2py Framework
- **RestrictedError**: Handles web2py's code execution restrictions
- **Request Context**: Accesses web2py request environment
- **Response Headers**: Manipulates web2py response object
- **HTTP Class**: Uses gluon.http.HTTP for response generation

#### ConnectSmart Platform
- **API Responses**: Standardized JSON error format
- **Error Codes**: Consistent error code system
- **Logging**: Integrated with platform logging infrastructure

### Error Pattern Matching

#### Regex Pattern
```python
pattern = re.compile(r'<.+ \'.+\.(?P<type>[^.]+)\'> (?P<msg>.*)')
```

**Pattern Components:**
- `<.+ `: Matches opening bracket and any characters
- `'.+\.`: Matches filename in quotes with extension
- `(?P<type>[^.]+)`: Captures file extension as 'type'
- `\'> `: Matches closing quote and bracket
- `(?P<msg>.*)`: Captures remaining message

#### Example Matches
```
Input: "<class 'controller.py'> NameError: name 'undefined_var' is not defined"
Output: {'type': 'py', 'msg': "NameError: name 'undefined_var' is not defined"}

Input: "<view 'template.html'> SyntaxError: invalid syntax"  
Output: {'type': 'html', 'msg': 'SyntaxError: invalid syntax'}
```

### Traceback Analysis

#### Stack Frame Extraction
```python
cl, exc, tb = sys.exc_info()
lastCallStack = traceback.extract_tb(tb)[-1]
detail['file'] = lastCallStack[0]
```

**Information Extracted:**
- **Exception Class**: Type of exception raised
- **Exception Instance**: The actual exception object
- **Traceback**: Complete stack trace
- **Last Frame**: Final call in the stack (error location)

### Security Considerations

#### Information Disclosure
- **Error Messages**: Careful balance between helpful and secure
- **File Paths**: May expose internal application structure
- **Stack Traces**: Logged but not exposed in API responses

#### Error Code Standardization
- **Generic Code**: Uses 99999 to avoid exposing internal error classification
- **Consistent Format**: Prevents information leakage through error variations

### Performance Characteristics

#### Processing Speed
- **Regex Compilation**: Compiled once at module load
- **Minimal Overhead**: Lightweight exception processing
- **String Operations**: Efficient pattern matching and formatting

#### Memory Usage
- **Pattern Caching**: Compiled regex stored in memory
- **Temporary Objects**: Minimal allocation during error handling
- **JSON Generation**: Efficient serialization

### Error Recovery

#### Graceful Degradation
```python
# Fallback for pattern matching failures
if not match:
    return {}  # Empty dict for safe access
    
# Safe dictionary formatting
return "%(type)s: %(msg)s in File: %(file)s" % detail
```

#### Robust Processing
- **Null Checks**: Handles missing exception attributes
- **Default Values**: Provides fallbacks for missing information
- **Exception Safety**: No additional exceptions during error handling

### Customization Options

#### Error Code Mapping
```python
# Could be extended to support different error codes
ERROR_CODES = {
    'NameError': 1001,
    'SyntaxError': 1002,
    'TypeError': 1003,
    # ... more specific mappings
}
```

#### Response Format Extension
```python
# Enhanced error response with additional context
content = {
    'result': 'fail',
    'error': {
        'code': 99999,
        'msg': e.output,
        'timestamp': datetime.now().isoformat(),
        'request_id': request.env.get('REQUEST_ID'),
    }
}
```

This custom exception handling module provides essential error processing capabilities for the Gluon framework, ensuring consistent error responses, comprehensive logging, and proper integration with the ConnectSmart platform's error handling infrastructure.