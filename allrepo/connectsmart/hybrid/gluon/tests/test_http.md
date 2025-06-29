# test_http.py

## Overview
This file contains unit tests for the web2py HTTP module, which handles HTTP status codes, exceptions, and response management. It tests the HTTP exception class functionality and status code message handling.

## Purpose
- Tests HTTP exception class and status code handling
- Validates predefined HTTP status codes and messages
- Tests custom status code and message functionality
- Ensures proper HTTP response formatting
- Tests error detection and validation

## Key Classes and Methods

### TestHTTP Class
Test suite for HTTP status code and exception functionality.

#### Test Methods

##### `test_status_message(self)`
Tests HTTP status code message functionality.

**Custom Status Code Testing:**
```python
message = "1423 This is a custom message"
code = 1423
self.assertEqual(str(h(gen_status_str(code, message))), gen_status_str(code, message))
```

**Predefined Status Code Testing:**
- Tests all predefined HTTP status codes in `defined_status`
- Validates that predefined codes return correct messages
- Ensures proper format: "code message"

**Status Message Override Testing:**
- Tests ability to override predefined status messages
- Validates custom message handling for known codes
- Tests format consistency across different message types

**Error Detection:**
- Tests wrong call detection and error handling
- Validates parameter validation

## Dependencies
- `unittest` - Python testing framework
- `gluon.http` - HTTP handling module (HTTP class, defined_status)

## HTTP Module Features Tested

### HTTP Status Codes
- **Predefined Codes**: Standard HTTP status codes (200, 404, 500, etc.)
- **Custom Codes**: Non-standard status codes with custom messages
- **Code Validation**: Proper status code format validation
- **Message Association**: Correct message mapping to status codes

### HTTP Exception Class
- **Status String Generation**: Proper "code message" format
- **Custom Messages**: Override capability for status messages
- **String Representation**: Correct string output for HTTP objects
- **Error Handling**: Detection of invalid parameters

## Usage Example
```python
from gluon.http import HTTP, defined_status

# Standard HTTP status
raise HTTP(404)  # "404 Not Found"
raise HTTP(200)  # "200 OK"

# Custom status message
raise HTTP("404 Custom Not Found Message")
raise HTTP("500 Custom Server Error")

# Check predefined status
if 404 in defined_status:
    print(defined_status[404])  # "Not Found"
```

## Integration with web2py Framework

### Error Handling
- **HTTP Exceptions**: Structured HTTP error responses
- **Status Code Management**: Centralized status code handling
- **Response Generation**: Automatic HTTP response creation
- **Error Pages**: Integration with error page system

### Controller Integration
- **Exception Raising**: Easy HTTP exception raising in controllers
- **Status Control**: Fine-grained HTTP status control
- **Response Customization**: Custom error messages and responses
- **API Development**: Proper HTTP status for API endpoints

### Middleware Integration
- **Error Processing**: HTTP exception processing in middleware
- **Status Code Routing**: Different handling based on status codes
- **Logging Integration**: HTTP status logging and monitoring
- **Debug Information**: Development-mode error details

## Test Coverage
- **Predefined Status Codes**: All standard HTTP status codes
- **Custom Status Codes**: Non-standard code handling
- **Message Formatting**: Proper message format validation
- **String Representation**: HTTP object string conversion
- **Error Detection**: Invalid parameter handling

## Expected Results
- **Correct Format**: Status codes should follow "code message" format
- **Predefined Accuracy**: Standard codes should return correct messages
- **Custom Support**: Custom codes should work with custom messages
- **Error Detection**: Invalid calls should be properly detected
- **Consistency**: Consistent behavior across different status types

## File Structure
```
gluon/tests/
├── test_http.py          # This file
└── ... (other test files)
```

This test suite ensures web2py's HTTP module provides reliable and standard-compliant HTTP status code handling for web applications and API development.