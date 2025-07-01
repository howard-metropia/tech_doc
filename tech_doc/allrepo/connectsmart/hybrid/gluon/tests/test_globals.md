# test_globals.py

## Overview
Unit test module for testing the core global objects in Web2py: Request, Response, and Session. These objects are fundamental to the framework's request/response cycle.

## Imports
```python
import re
import unittest
from gluon import URL
from gluon._compat import basestring
from gluon.globals import Request, Response, Session
from gluon.rewrite import regex_url_in
```

## Helper Functions

### setup_clean_session()
Creates and configures a clean session environment for testing.

**Setup Process:**
1. Creates a Request object with empty environment
2. Sets default application/controller/function values
3. Creates Response and Session objects
4. Connects session to request and response
5. Sets up current context with all three objects

**Returns:** The current context object containing request, response, and session

## Test Classes

### testRequest

Tests the Request object functionality, particularly RESTful routing.

#### setUp()
Initializes a clean Response object in the current context.

#### test_restful_simple()
Tests basic RESTful routing with GET method and arguments.

**Test Flow:**
1. Creates request environment for GET to `/welcome/default/index/1.pdf`
2. Uses `@r.restful()` decorator to create RESTful handler
3. Defines GET method that returns first argument
4. Verifies that "1" is extracted and returned

#### test_restful_calls_post()
Tests RESTful routing for POST requests.

**Test Flow:**
1. Creates request environment for POST to `/welcome/default/index`
2. Defines POST handler that returns "I posted"
3. Verifies correct method dispatch

#### test_restful_ignore_extension()
Tests RESTful routing with extension ignore flag.

**Test Flow:**
1. Creates request for path with IP address (`127.0.0.1`)
2. Uses `ignore_extension=True` to prevent treating `.1` as extension
3. Verifies full IP address is preserved as argument

### testResponse

Tests the Response object functionality, particularly file inclusion and cookie handling.

#### Helper Methods

##### assertRegexpMatches()
Port of Python 2.7 method for regex matching (needed for Python 2.5/2.6 compatibility).

#### test_include_files()
Comprehensive test of the `include_files()` method for various file types.

**Test Cases:**

1. **CSS Files**
   - Input: `URL("a", "static", "css/file.css")`
   - Output: `<link href="/a/static/css/file.css" rel="stylesheet" type="text/css" />`

2. **JavaScript Files**
   - Input: `URL("a", "static", "css/file.js")`
   - Output: `<script src="/a/static/css/file.js" type="text/javascript"></script>`

3. **CoffeeScript Files**
   - Input: `URL("a", "static", "css/file.coffee")`
   - Output: `<script src="/a/static/css/file.coffee" type="text/coffee"></script>`

4. **TypeScript Files**
   - Input: `URL("a", "static", "css/file.ts")`
   - Output: `<script src="/a/static/css/file.ts" type="text/typescript"></script>`

5. **LESS Files**
   - Input: `URL("a", "static", "css/file.less")`
   - Output: `<link href="/a/static/css/file.less" rel="stylesheet/less" type="text/css" />`

6. **Inline CSS**
   - Input: `("css:inline", "background-color; white;")`
   - Output: `<style type="text/css">\nbackground-color; white;\n</style>`

7. **Inline JavaScript**
   - Input: `("js:inline", 'alert("hello")')`
   - Output: `<script type="text/javascript">\nalert("hello")\n</script>`

8. **External URLs**
   - Tests jQuery CDN inclusion
   - Tests URL with query parameters
   - Tests duplicate file prevention

9. **Mixed File Types**
   - Tests proper ordering and inclusion of multiple file types

10. **Extension Filtering**
    - Tests filtering by specific extensions

11. **Regression Tests**
    - Tests for issue #628 with proper handling of external URLs

#### test_cookies()
Tests basic cookie generation for sessions.

**Validates:**
- Cookie starts with "Set-Cookie: "
- Contains session ID
- Includes "Path=/" directive

#### test_cookies_secure()
Tests secure cookie flag functionality.

**Test Cases:**
1. Default: secure flag not set
2. With `session.secure()`: secure flag is set

#### test_cookies_httponly()
Tests HttpOnly cookie flag functionality.

**Test Cases:**
1. Default: HttpOnly is set (security default)
2. `httponly_cookies = True`: HttpOnly is set
3. `httponly_cookies = False`: HttpOnly is not set

#### test_cookies_samesite()
Tests SameSite cookie attribute functionality.

**Test Cases:**
1. Default: SameSite=Lax
2. `samesite(False)`: SameSite attribute removed
3. `samesite("Strict")`: SameSite=Strict

#### test_include_meta()
Tests HTML meta tag generation.

**Test Cases:**
1. Simple meta tag: `response.meta["web2py"] = "web2py"`
   - Output: `<meta name="web2py" content="web2py" />`

2. Dictionary meta tag: `response.meta["meta_dict"] = {"tag_name": "tag_value"}`
   - Output: `<meta tag_name="tag_value" />`

## Key Features Tested

### Request Object
- RESTful method routing
- URL argument parsing
- Extension handling

### Response Object
- Static file inclusion with proper HTML tags
- Support for various file types (CSS, JS, CoffeeScript, TypeScript, LESS)
- Inline CSS/JS inclusion
- External URL handling
- Duplicate file prevention
- Cookie security attributes (Secure, HttpOnly, SameSite)
- Meta tag generation

### Session Object
- Cookie generation
- Security flag management
- Cross-site request protection

## Notes
- Tests cover both modern and legacy Python versions
- Comprehensive coverage of file inclusion scenarios
- Security-focused cookie testing
- RESTful routing validation