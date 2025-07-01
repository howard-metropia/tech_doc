# test_http.py

## Overview
Unit test module for testing the HTTP exception class in Web2py, focusing on HTTP status code handling and custom status messages.

## Imports
```python
import unittest
from gluon.http import HTTP, defined_status
```

## Test Class: TestHTTP

### Description
Tests the HTTP exception class functionality, particularly status code message generation and handling.

### Helper Methods

#### gen_status_str()
Local helper function within test methods that formats status codes and messages.
```python
def gen_status_str(code, message):
    return str(code) + " " + str(message)
```

### Test Methods

#### test_status_message()
Comprehensive test of HTTP status code handling.

**Test Cases:**

1. **Custom Status Code and Message**
   - Tests creating HTTP exception with custom code (1423) and message
   - Verifies the string representation matches expected format
   - Example: `"1423 This is a custom message"`

2. **Predefined Status Codes**
   - Iterates through all codes in `defined_status` dictionary
   - Verifies each predefined code generates correct status string
   - Tests standard HTTP codes (200, 404, 500, etc.) with their default messages

3. **Custom Messages with Standard Codes**
   - Tests overriding default messages for standard HTTP codes
   - Verifies custom message takes precedence over predefined message
   - Example: `HTTP(404, "Custom not found message")`

4. **Wrong Call Detection**
   - Comment indicates test for incorrect usage detection
   - Test appears incomplete in the provided code

## Key Components

### HTTP Class
The HTTP class being tested is an exception class that:
- Accepts status codes as arguments
- Can accept custom status messages
- Has predefined messages for standard HTTP codes
- Provides string representation of the status

### defined_status Dictionary
Contains mappings of standard HTTP status codes to their messages:
- 200 → "OK"
- 404 → "Not Found"
- 500 → "Internal Server Error"
- etc.

## Testing Strategy

### Status Code Coverage
- Tests both standard and non-standard status codes
- Verifies proper formatting of status strings

### Message Handling
- Tests default message retrieval
- Tests custom message override capability
- Ensures proper string concatenation

### Edge Cases
- Non-standard status codes (like 1423)
- Message override functionality
- String representation consistency

## Expected Behaviors

1. **Standard Code**: `HTTP(404)` → `"404 Not Found"`
2. **Custom Message**: `HTTP(404, "Custom")` → `"404 Custom"`
3. **Non-standard Code**: `HTTP(1423, "Message")` → `"1423 Message"`

## Notes
- The HTTP class is typically used to raise HTTP exceptions in Web2py controllers
- These exceptions are caught by the framework and converted to proper HTTP responses
- The test ensures consistent behavior across all status codes
- The incomplete test at the end suggests additional validation tests were planned