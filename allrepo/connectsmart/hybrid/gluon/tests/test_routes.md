# test_routes.py

## Overview
This file contains unit tests for the web2py regex-based routing system. It tests the traditional routes.py configuration approach using regular expressions for URL mapping, providing comprehensive validation of incoming and outgoing URL transformations.

## Purpose
- Tests regex-based URL routing functionality
- Validates routes.py configuration processing
- Tests incoming and outgoing URL mappings
- Verifies static file routing and security
- Tests application-specific routing configurations
- Ensures proper URL transformation and validation

## Key Functions and Classes

### Module Setup Functions

#### `setUpModule()`
Creates temporary application structure for routing tests.

**Application Structure:**
```
applications/
├── admin/controllers/
├── examples/
│   ├── controllers/
│   └── routes.py  # App-specific routes
└── welcome/controllers/
```

**App-specific Routes:**
```python
# applications/examples/routes.py
default_function='exdef'
```

#### `tearDownModule()`
Cleans up temporary application structure.

#### `norm_root(root)`
Normalizes file paths for cross-platform compatibility.

### TestRoutes Class
Test suite for regex routing functionality.

#### Test Methods

##### `test_routes_null(self)`
Tests behavior with empty routes configuration.

**Null Routes Setup:**
```python
load(data="")  # Empty routes configuration
```

**Incoming URL Testing:**
```python
# Root and application mapping
filter_url("http://domain.com")           # → "/init/default/index"
filter_url("http://domain.com/")          # → "/init/default/index"
filter_url("http://domain.com/abc")       # → "/abc/default/index"
filter_url("http://domain.com/abc/def")   # → "/abc/def/index"
filter_url("http://domain.com/abc/def/ghi") # → "/abc/def/ghi"

# Arguments handling
filter_url("http://domain.com/abc/def/ghi/jkl") 
# → "/abc/def/ghi ['jkl']"

# URL encoding
filter_url("http://domain.com/abc/def/ghi/j%20kl")
# → "/abc/def/ghi ['j_kl']"
```

**Static File Testing:**
```python
# Static file resolution
filter_url("http://domain.com/welcome/static/path/to/static")
# → "/path/to/applications/welcome/static/path/to/static"
```

**Outgoing URL Testing:**
```python
# Reverse URL mapping
filter_url("http://domain.com/init/default/index", out=True)  # → "/"
filter_url("http://domain.com/init/default/abc", out=True)    # → "/abc"
```

## Dependencies
- `unittest` - Python testing framework
- `os` - Operating system interface
- `shutil` - High-level file operations
- `tempfile` - Temporary directory management
- `gluon._compat` - Cross-version compatibility
- `gluon.html` - URL generation functions
- `gluon.http` - HTTP exception handling
- `gluon.rewrite` - URL rewriting and routing
- `gluon.settings` - Global settings management
- `gluon.storage` - Storage utilities

## Routing Features Tested

### URL Mapping
- **Application Detection**: Automatic application detection from URLs
- **Controller Resolution**: Controller identification and mapping
- **Function Mapping**: Function resolution within controllers
- **Argument Extraction**: URL argument parsing and handling

### Static File Handling
- **Path Resolution**: Static file path construction
- **Security Validation**: Path traversal attack prevention
- **Application Scoping**: App-specific static file serving
- **Performance**: Efficient static file routing

### Bidirectional Routing
- **Incoming URLs**: External URL to internal path mapping
- **Outgoing URLs**: Internal path to external URL mapping
- **Consistency**: Bidirectional mapping consistency
- **Optimization**: URL generation optimization

### Default Behaviors
- **Default Application**: "init" application for unspecified apps
- **Default Controller**: "default" controller for unspecified controllers
- **Default Function**: "index" function for unspecified functions
- **Argument Handling**: URL arguments beyond function name

## Usage Example
```python
from gluon.rewrite import load, filter_url

# Load empty routes (default behavior)
load(data="")

# Test incoming URL mapping
internal_path = filter_url("http://example.com/blog/posts/view/123")
# Returns: "/blog/posts/view ['123']"

# Test outgoing URL mapping  
public_url = filter_url("http://example.com/blog/default/index", out=True)
# Returns: "/blog"

# Static file handling
static_path = filter_url("http://example.com/app/static/css/main.css")
# Returns: "/path/to/applications/app/static/css/main.css"
```

## Integration with web2py Framework

### Request Processing
- **URL Parsing**: Incoming request URL parsing
- **Route Matching**: URL pattern matching against routes
- **Parameter Extraction**: URL parameter and argument extraction
- **Application Routing**: Multi-application request routing

### Response Generation
- **URL Generation**: Template URL generation
- **Link Creation**: Automatic link generation for forms and menus
- **Static Assets**: Static file URL generation
- **Redirect Handling**: Proper redirect URL construction

### Security Features
- **Path Validation**: Static file path security validation
- **Input Sanitization**: URL parameter sanitization
- **Access Control**: Application-level access control
- **Error Handling**: Secure error response generation

### Performance Optimization
- **Caching**: Route matching result caching
- **Compilation**: Route pattern compilation for speed
- **Static Serving**: Efficient static file serving
- **Memory Usage**: Optimized memory usage for large route sets

## Routing Patterns

### Default Routing
```python
# Default routing without routes.py
/{application}/{controller}/{function}/{arg1}/{arg2}/...
```

### Application-specific Routing
```python
# applications/myapp/routes.py
default_function = 'home'  # Changes default function
```

### Static File Routing
```python
# Static files
/{application}/static/{path}
# Maps to: applications/{application}/static/{path}
```

## Test Coverage
- **Empty Configuration**: Default routing behavior
- **URL Mapping**: Bidirectional URL transformation
- **Static Files**: Static file routing and security
- **Application Resolution**: Multi-application routing
- **Error Conditions**: Invalid URL handling
- **Cross-platform**: Path separator handling

## Expected Results
- **Correct Mapping**: URLs should map correctly between external and internal forms
- **Security**: Invalid paths should be blocked with appropriate errors
- **Performance**: Routing should be fast for high-traffic applications
- **Consistency**: Bidirectional mapping should be consistent
- **Compatibility**: Cross-platform path handling should work correctly

## Comparison with Router System
This regex-based routing system differs from the advanced router system:

- **Configuration**: Uses routes.py files vs. router dictionaries
- **Syntax**: Regular expressions vs. structured configuration
- **Flexibility**: More flexible but more complex configuration
- **Performance**: Generally faster for simple routing patterns
- **Maintenance**: Requires more careful maintenance of regex patterns

## File Structure
```
gluon/tests/
├── test_routes.py        # This file
└── ... (other test files)

# Test application structure (temporary)
/tmp/test_apps/
└── applications/
    ├── admin/
    ├── examples/
    │   └── routes.py     # App-specific routes
    └── welcome/
```

This test suite ensures web2py's traditional regex-based routing system provides reliable, secure, and efficient URL routing capabilities for web applications using the classic routes.py configuration approach.