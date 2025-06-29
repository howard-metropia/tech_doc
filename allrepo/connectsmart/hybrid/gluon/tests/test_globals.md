# test_globals.py

## Overview
This file contains unit tests for the web2py global objects (Request, Response, Session) that form the core of the web2py framework's request-response cycle. It tests RESTful API functionality, file inclusion, cookie handling, and meta tag management.

## Purpose
- Tests Request object and RESTful API decorators
- Validates Response object file inclusion and meta tag functionality
- Tests Session object and cookie management
- Verifies secure cookie handling and SameSite cookie attributes
- Tests HTTP header generation and content type handling

## Key Functions and Classes

### Helper Functions

#### `setup_clean_session()`
Creates a clean session setup for testing.

**Setup Process:**
- **Request Creation**: Creates Request object with empty environment
- **Application Context**: Sets application, controller, function values
- **Response/Session**: Initializes Response and Session objects
- **Session Connection**: Connects session to request/response
- **Global Context**: Sets up current.request, current.response, current.session

**Returns:**
- `current` object with initialized request, response, and session

### testRequest Class
Tests Request object functionality, particularly RESTful APIs.

#### Test Methods

##### `test_restful_simple(self)`
Tests basic RESTful API functionality with GET requests.

**Environment Setup:**
```python
env = {"request_method": "GET", "PATH_INFO": "/welcome/default/index/1.pdf"}
```

**RESTful Decorator Testing:**
```python
@r.restful()
def simple_rest():
    def GET(*args, **vars):
        return args[0]
    return locals()
```

**Validation:**
- Tests that GET method is called correctly
- Validates argument parsing from URL path
- Ensures proper return value handling

##### `test_restful_calls_post(self)`
Tests RESTful API with POST requests.

**Environment Setup:**
```python
env = {"request_method": "POST", "PATH_INFO": "/welcome/default/index"}
```

**POST Method Testing:**
- Tests POST method execution
- Validates return value from POST handler
- Ensures proper HTTP method routing

##### `test_restful_ignore_extension(self)`
Tests RESTful API with extension ignoring.

**Extension Handling:**
```python
@r.restful(ignore_extension=True)
def ignore_rest():
    def GET(*args, **vars):
        return args[0]
    return locals()
```

**IP Address Testing:**
- Tests handling of IP addresses in URL path
- Validates extension ignoring functionality
- Ensures proper argument extraction

### testResponse Class
Tests Response object functionality including file inclusion and cookies.

#### Helper Methods

##### `assertRegexpMatches(self, text, expected_regexp, msg=None)`
Compatibility method for regex matching across Python versions.

#### Test Methods

##### `test_include_files(self)`
Comprehensive testing of file inclusion functionality.

**File Type Testing:**
- **CSS Files**: Tests CSS file inclusion with proper link tags
- **JavaScript Files**: Tests JS file inclusion with script tags
- **CoffeeScript Files**: Tests .coffee file inclusion
- **TypeScript Files**: Tests .ts file inclusion
- **LESS Files**: Tests .less file inclusion with proper rel attribute

**Inline Content Testing:**
```python
response.files.append(("css:inline", "background-color; white;"))
response.files.append(("js:inline", 'alert("hello")'))
```

**External Resource Testing:**
- **CDN Resources**: Tests external JavaScript libraries
- **Query Parameters**: Tests URLs with query parameters
- **Duplicate Prevention**: Tests duplicate file prevention

**Selective Inclusion:**
- **Extension Filtering**: Tests filtering by file extensions
- **Mixed File Types**: Tests handling multiple file types
- **Type Specification**: Tests explicit type specification

##### `test_cookies(self)`
Tests basic cookie functionality.

**Cookie Validation:**
- **Session ID**: Tests session ID cookie generation
- **Path Setting**: Validates cookie path configuration
- **Cookie Format**: Tests proper cookie header format

##### `test_cookies_secure(self)`
Tests secure cookie functionality.

**Security Testing:**
- **Default Behavior**: Tests that cookies are not secure by default
- **Secure Flag**: Tests secure cookie flag setting
- **HTTPS Requirements**: Validates secure cookie requirements

##### `test_cookies_httponly(self)`
Tests HTTP-only cookie functionality.

**HttpOnly Testing:**
- **Default Setting**: Tests that HttpOnly is enabled by default
- **Explicit Enable**: Tests explicit HttpOnly enabling
- **Explicit Disable**: Tests HttpOnly disabling

##### `test_cookies_samesite(self)`
Tests SameSite cookie attribute functionality.

**SameSite Testing:**
- **Default Lax**: Tests that Lax is the default SameSite mode
- **Disable SameSite**: Tests disabling SameSite completely
- **Strict Mode**: Tests SameSite=Strict configuration

##### `test_include_meta(self)`
Tests meta tag inclusion functionality.

**Meta Tag Testing:**
- **Simple Meta**: Tests basic name/content meta tags
- **Complex Meta**: Tests meta tags with dictionary attributes

```python
response.meta["web2py"] = "web2py"
# Generates: <meta name="web2py" content="web2py" />

response.meta["meta_dict"] = {"tag_name": "tag_value"}
# Generates: <meta tag_name="tag_value" />
```

## Dependencies
- `unittest` - Python testing framework
- `re` - Regular expression operations
- `gluon.URL` - URL generation function
- `gluon._compat.basestring` - Cross-version string compatibility
- `gluon.globals` - Global objects (Request, Response, Session)
- `gluon.rewrite` - URL rewriting functionality

## RESTful API Features Tested

### HTTP Method Routing
- **GET Requests**: Proper GET method handling
- **POST Requests**: Proper POST method handling
- **Method Detection**: Automatic HTTP method detection
- **Method Dispatch**: Correct method function calling

### URL Processing
- **Path Parsing**: URL path argument extraction
- **Extension Handling**: File extension processing
- **Extension Ignoring**: Ability to ignore extensions
- **Query Parameters**: Query parameter handling

### Decorator Functionality
- **Function Wrapping**: Proper decorator application
- **Local Scope**: Access to local function definitions
- **Return Values**: Proper return value handling
- **Error Handling**: Graceful error handling

## File Inclusion Features

### File Types Supported
- **CSS**: Stylesheet files (.css)
- **JavaScript**: Script files (.js)
- **CoffeeScript**: CoffeeScript files (.coffee)
- **TypeScript**: TypeScript files (.ts)
- **LESS**: LESS stylesheet files (.less)

### Inclusion Methods
- **Static Files**: Application static files
- **External URLs**: CDN and external resources
- **Inline Content**: Inline CSS and JavaScript
- **Type Specification**: Explicit file type specification

### Advanced Features
- **Duplicate Prevention**: Automatic duplicate file filtering
- **Extension Filtering**: Selective file inclusion by type
- **Mixed Content**: Combining multiple file types
- **Query Parameter Support**: URLs with parameters

## Cookie Security Features

### Security Attributes
- **Secure Flag**: HTTPS-only cookie transmission
- **HttpOnly Flag**: JavaScript access prevention
- **SameSite Attribute**: Cross-site request forgery protection
- **Path Specification**: Cookie scope limitation

### Configuration Options
- **Default Settings**: Secure default configurations
- **Explicit Control**: Programmatic security control
- **Flexible Configuration**: Adaptable to different security needs

## Usage Example
```python
from gluon.globals import Request, Response, Session
from gluon import URL

# RESTful API setup
@request.restful()
def api_endpoint():
    def GET(*args, **vars):
        return {"data": args[0]}
    
    def POST(*args, **vars):
        return {"status": "created"}
    
    return locals()

# File inclusion
response.files.append(URL('a', 'static', 'css/main.css'))
response.files.append(URL('a', 'static', 'js/app.js'))
response.files.append(('css:inline', 'body { margin: 0; }'))

# Cookie security
session.secure()
session.httponly_cookies = True
session.samesite('Strict')

# Meta tags
response.meta['description'] = 'My web2py application'
response.meta['keywords'] = 'web2py, python, framework'
```

## Integration with web2py Framework

### Request-Response Cycle
- **Request Processing**: Handles incoming HTTP requests
- **Response Generation**: Creates HTTP responses
- **Session Management**: Maintains user sessions
- **Cookie Handling**: Manages HTTP cookies

### Security Integration
- **CSRF Protection**: SameSite cookie protection
- **Session Security**: Secure session handling
- **XSS Prevention**: HttpOnly cookie protection
- **HTTPS Support**: Secure cookie transmission

### Template Integration
- **File Inclusion**: Automatic asset inclusion in templates
- **Meta Tag Generation**: Automatic meta tag insertion
- **Content Type Handling**: Proper content type headers
- **Resource Management**: Efficient resource loading

## File Structure
```
gluon/tests/
├── test_globals.py       # This file
└── ... (other test files)
```

This test suite ensures web2py's global objects provide reliable, secure, and efficient request-response cycle handling with proper RESTful API support and security features.