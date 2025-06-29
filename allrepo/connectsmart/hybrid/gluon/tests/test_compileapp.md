# test_compileapp.py

## Overview
This file contains unit tests for the web2py application compilation and packaging system. It tests the functionality of compiling applications to bytecode, creating and managing application packages (w2p files), and administrative operations like app creation and cleanup.

## Purpose
- Tests application compilation to bytecode for performance
- Validates w2p package creation and extraction
- Tests administrative functions for app lifecycle management
- Verifies version checking and update mechanisms
- Tests file packaging and deployment workflows

## Key Classes and Methods

### Global Configuration
- `test_app_name` - Name for test application ("_test_compileapp")
- `test_app2_name` - Name for admin test application ("_test_compileapp_admin")
- `test_unpack_dir` - Directory for package extraction testing
- `WEB2PY_VERSION_URL` - URL for version checking tests

### TestPack Class
Comprehensive test suite for application compilation and packaging.

#### Class Setup/Teardown Methods

##### `setUpClass(cls)`
Class-level setup executed once before all tests:
- **Test App Creation**: Creates test application directory
- **App Structure**: Initializes basic application structure using `create_app()`
- **Directory Validation**: Ensures test application exists

##### `tearDownClass(cls)`
Class-level cleanup executed after all tests:
- **Directory Cleanup**: Removes test application directory
- **Package Cleanup**: Removes created w2p package files
- **Temp Directory Cleanup**: Removes temporary extraction directories

#### Test Methods

##### `test_compile(self)`
Tests application compilation and packaging workflow.

**Compilation Testing:**
- **Bytecode Compilation**: Tests `compile_application()` for performance optimization
- **Compilation Cleanup**: Tests `remove_compiled_application()` for cleanup
- **Return Validation**: Ensures compilation returns None on success

**Packaging Testing:**
- **Compiled Packaging**: Creates w2p package with compiled bytecode
- **Source Packaging**: Creates w2p package with source code
- **Package Extraction**: Tests `w2p_unpack()` functionality

**File Operations:**
```python
# Compilation
compile_application(app_path)
remove_compiled_application(app_path)

# Packaging
w2p_pack(test_pack, app_path, compiled=True, filenames=None)
w2p_pack(test_pack, app_path, compiled=False, filenames=None)

# Extraction
w2p_unpack(test_pack, test_unpack_dir)
```

##### `test_admin_compile(self)`
Tests administrative compilation functions.

**Admin Operations Tested:**
- **App Creation**: `app_create()` - Creates new application
- **App Compilation**: `app_compile()` - Compiles existing application
- **App Cleanup**: `app_cleanup()` - Removes compiled files
- **App Uninstall**: `app_uninstall()` - Completely removes application

**Test Workflow:**
1. **Setup**: Creates request context for admin operations
2. **Creation**: Creates new test application
3. **Validation**: Verifies application files exist
4. **Compilation**: Compiles the application
5. **Cleanup**: Tests cleanup and uninstall operations

**Request Context Setup:**
```python
request = Request(env={})
request.application = "a"
request.controller = "c"
request.function = "f"
request.folder = "applications/admin"
```

##### `test_check_new_version(self)`
Tests version checking functionality.

**Version Checking:**
- **Remote Version Check**: Tests `check_new_version()` against web2py.com
- **Version Comparison**: Validates version comparison logic
- **Network Handling**: Tests handling of network requests
- **Return Value Validation**: Ensures proper return value format

**Test Process:**
```python
vert = check_new_version(global_settings.web2py_version, WEB2PY_VERSION_URL)
self.assertNotEqual(vert[0], -1)  # Valid version response
```

## Dependencies
- `unittest` - Python testing framework
- `os` - Operating system interface
- `shutil` - High-level file operations
- `tempfile` - Temporary file and directory creation
- `gluon.admin` - Administrative functions
- `gluon.compileapp` - Application compilation utilities
- `gluon.fileutils` - File utility functions
- `gluon.globals` - Global context objects
- `gluon.main` - Main application settings

## Functions Tested

### Compilation Functions
- `compile_application(app_path)` - Compiles app to bytecode
- `remove_compiled_application(app_path)` - Removes compiled files

### Packaging Functions
- `w2p_pack(filename, path, compiled, filenames)` - Creates w2p package
- `w2p_unpack(filename, path)` - Extracts w2p package
- `create_app(path)` - Creates basic app structure

### Administrative Functions
- `app_create(name, request)` - Creates new application
- `app_compile(name, request)` - Compiles application
- `app_cleanup(name, request)` - Cleans up application
- `app_uninstall(name, request)` - Uninstalls application

### Version Functions
- `check_new_version(current, url)` - Checks for updates

## Usage Example
```python
# Compile application
from gluon.compileapp import compile_application, remove_compiled_application

app_path = "applications/myapp"
compile_application(app_path)  # Compile to bytecode
remove_compiled_application(app_path)  # Remove compiled files

# Package application
from gluon.fileutils import w2p_pack, w2p_unpack

w2p_pack("myapp.w2p", app_path, compiled=True)  # Create package
w2p_unpack("myapp.w2p", "/tmp/extract")  # Extract package

# Administrative operations
from gluon.admin import app_create, app_compile

request = Request(env={})
request.folder = "applications/admin"

app_create("newapp", request)  # Create application
app_compile("newapp", request)  # Compile application
```

## Integration with web2py Framework

### Application Lifecycle
- **Development**: Source code management and editing
- **Compilation**: Bytecode compilation for production
- **Packaging**: Application distribution and deployment
- **Installation**: Application deployment and setup

### Performance Optimization
- **Bytecode Compilation**: Improves runtime performance
- **Package Compression**: Reduces distribution file size
- **Selective Compilation**: Compiles only necessary files

### Administrative Interface
- **Web-based Management**: Admin interface integration
- **Batch Operations**: Multiple application management
- **Version Control**: Application versioning and updates

### Security and Deployment
- **Package Integrity**: Validates package contents
- **Controlled Deployment**: Secure application installation
- **Cleanup Operations**: Proper resource management

## Test Coverage
- **Compilation Process**: Bytecode generation and cleanup
- **Packaging Operations**: Package creation and extraction
- **Administrative Functions**: Complete app lifecycle
- **Version Management**: Update checking and validation
- **File Operations**: Directory and file management
- **Error Handling**: Proper error responses and cleanup

## Expected Results
- **Compilation**: Should complete without errors
- **Packaging**: Should create valid w2p files
- **Extraction**: Should restore complete application structure
- **Admin Operations**: Should manage applications properly
- **Version Checking**: Should return valid version information

## File Structure
```
gluon/tests/
├── test_compileapp.py    # This file
├── ... (other test files)
└── test applications/
    ├── _test_compileapp/     # Test application
    └── _test_compileapp_admin/  # Admin test application
```

This test suite ensures the web2py application compilation and packaging system works reliably for development, deployment, and administrative operations.