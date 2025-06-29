# test_router.py

## Overview
This file contains comprehensive unit tests for the web2py URL routing system (routers). It tests the advanced router functionality from gluon.rewrite, including URL mapping, application resolution, static file handling, and various routing configurations.

## Purpose
- Tests router-based URL routing (advanced routing option)
- Validates application resolution and mapping
- Tests static file routing and security
- Verifies router configuration syntax and validation
- Tests incoming and outgoing URL transformations
- Validates app-specific routing configurations

## Key Functions and Classes

### Module Setup Functions

#### `setUpModule()`
Creates temporary application tree for testing routing functionality.

**Application Structure Created:**
```
applications/
├── admin/
│   └── controllers/
│       ├── appadmin.py
│       ├── default.py
│       ├── gae.py
│       ├── mercurial.py
│       ├── shell.py
│       └── wizard.py
├── examples/
│   ├── controllers/
│   │   ├── ajax_examples.py
│   │   ├── appadmin.py
│   │   ├── default.py
│   │   ├── global.py
│   │   └── spreadsheet.py
│   ├── routes.py  # App-specific routes
│   └── static/
│       ├── en/file
│       └── it/file
└── welcome/
    └── controllers/
        ├── appadmin.py
        ├── default.py
        ├── other.py
        └── admin.py
```

**App-specific Routes Configuration:**
```python
# applications/examples/routes.py
routers=dict(examples=dict(default_function='exdef'))
```

#### `tearDownModule()`
Cleans up temporary application structure and restores original settings.

#### `norm_root(root)`
Normalizes path separators for cross-platform compatibility.

### TestRouter Class
Comprehensive test suite for router functionality.

#### Helper Methods

##### `myassertRaisesRegex(self, *args, **kwargs)`
Cross-version compatibility method for regex assertion in exceptions.

#### Test Methods

##### `test_router_syntax(self)`
Tests router configuration syntax validation and error handling.

**Syntax Error Testing:**
```python
# Invalid syntax
self.assertRaises(SyntaxError, load, data="x::y")

# Unknown configuration keys
self.assertRaises(SyntaxError, load, rdict=dict(BASE=dict(badkey="value")))

# Invalid key placement
self.assertRaises(SyntaxError, load, 
    rdict=dict(BASE=dict(), app=dict(default_application="name")))
```

**Error Message Validation:**
- Tests specific error messages for different syntax errors
- Validates regex patterns in error messages
- Ensures proper error reporting for configuration issues

##### `test_router_null(self)`
Tests null (empty) router configuration behavior.

**Application Resolution:**
```python
load(rdict=dict())  # Empty router configuration

# App resolution testing
filter_url("http://domain.com/welcome", app=True)  # Returns: "welcome"
filter_url("http://domain.com/", app=True)         # Returns: "init"
```

**Incoming URL Processing:**
- **Favicon**: Special handling for `/favicon.ico`
- **Default Routing**: `/abc` → `/init/default/abc`
- **Function Arguments**: `/index/abc` → `/init/default/index ['abc']`
- **Static Files**: Proper static file path resolution
- **Security**: Invalid static file path rejection

**Outgoing URL Processing:**
- **Index Removal**: `/init/default/index` → `/`
- **Function Arguments**: `/init/default/index/arg1` → `/index/arg1`
- **Controller Mapping**: Various controller URL mappings
- **Application Prefixes**: Proper application prefix handling

##### `test_router_specific(self)`
Tests application-specific routing configurations.

**App-specific Routes:**
```python
# Default behavior
filter_url("http://domain.com/welcome")  # Returns: "/welcome/default/index"

# Custom default function from routes.py
filter_url("http://domain.com/examples") # Returns: "/examples/default/exdef"
```

##### `test_router_defapp(self)`
Tests default application configuration.

**Default Application Setup:**
```python
routers = dict(BASE=dict(default_application="welcome"))
load(rdict=routers)
```

**Behavior Testing:**
- **Root Access**: `/` maps to default application
- **Application Resolution**: Proper default app resolution
- **Controller Mapping**: Controllers mapped within default app
- **URL Generation**: Proper URL generation for default app

## Dependencies
- `unittest` - Python testing framework
- `logging` - Logging for router operations
- `os` - Operating system interface
- `shutil` - High-level file operations
- `tempfile` - Temporary directory creation
- `gluon._compat` - Cross-version compatibility
- `gluon.html` - URL generation functions
- `gluon.http` - HTTP exception handling
- `gluon.rewrite` - URL rewriting and routing
- `gluon.settings` - Global settings management
- `gluon.storage` - Storage utilities

## Router Features Tested

### URL Mapping
- **Incoming URLs**: Request URL to internal path mapping
- **Outgoing URLs**: Internal path to public URL mapping
- **Static Files**: Static file path resolution and security
- **Arguments**: Function argument extraction and handling

### Application Resolution
- **Default Application**: Configurable default application
- **Application Detection**: Automatic application detection from URLs
- **Multi-application**: Multiple application support
- **App-specific Configuration**: Per-application routing rules

### Security Features
- **Path Validation**: Static file path security validation
- **Directory Traversal**: Protection against directory traversal attacks
- **Invalid Characters**: Rejection of invalid characters in paths
- **Error Handling**: Proper HTTP error responses for security violations

### Configuration Management
- **Syntax Validation**: Router configuration syntax checking
- **Error Reporting**: Detailed error messages for configuration issues
- **Key Validation**: Valid configuration key enforcement
- **Hierarchical Config**: BASE and application-specific configurations

## Usage Example
```python
from gluon.rewrite import load, filter_url, get_effective_router

# Basic router configuration
routers = dict(
    BASE=dict(
        default_application="welcome",
        default_controller="default",
        default_function="index"
    ),
    welcome=dict(
        controllers=["default", "user", "admin"],
        default_function="home"
    )
)

# Load router configuration
load(rdict=routers)

# Test incoming URL mapping
internal_path = filter_url("http://example.com/user/profile")
# Returns: "/welcome/user/profile"

# Test outgoing URL mapping
public_url = filter_url("http://example.com/welcome/default/index", out=True)
# Returns: "/"

# Get effective router for application
router = get_effective_router("welcome")
```

## Integration with web2py Framework

### URL Routing System
- **Request Processing**: Incoming request URL processing
- **Response Generation**: Outgoing URL generation for templates
- **Static File Serving**: Static file path resolution
- **Error Handling**: HTTP error responses for routing issues

### Application Management
- **Multi-tenancy**: Multiple application support
- **Application Discovery**: Automatic application detection
- **Controller Resolution**: Controller and function resolution
- **Default Configurations**: Sensible default behaviors

### Security Integration
- **Path Security**: Static file path security validation
- **Access Control**: Application-level access control
- **Error Responses**: Secure error response handling
- **Attack Prevention**: Directory traversal attack prevention

### Development Support
- **Configuration Validation**: Development-time configuration checking
- **Error Reporting**: Detailed error messages for debugging
- **Testing Support**: Comprehensive testing framework
- **Documentation**: Well-documented configuration options

## Test Coverage
- **Configuration Syntax**: Router configuration validation
- **URL Mapping**: Bidirectional URL mapping testing
- **Application Resolution**: Multi-application routing
- **Static File Handling**: Static file security and resolution
- **Error Conditions**: Invalid configuration and URL handling
- **Cross-platform**: Path separator normalization

## Expected Results
- **Correct Mapping**: URLs should map correctly in both directions
- **Security**: Invalid paths should be rejected with proper errors
- **Configuration**: Invalid configurations should raise syntax errors
- **Performance**: Routing should be efficient for high-traffic sites
- **Flexibility**: Support for complex routing requirements

## File Structure
```
gluon/tests/
├── test_router.py        # This file
└── ... (other test files)

# Test application structure (temporary)
/tmp/test_apps/
└── applications/
    ├── admin/
    ├── examples/
    └── welcome/
```

This test suite ensures web2py's advanced router system provides reliable, secure, and flexible URL routing capabilities for complex multi-application deployments.