# test_contribs.py

## Overview
This file contains unit tests for the web2py contrib package, which includes third-party libraries and utilities integrated into the framework. It specifically tests PDF generation functionality and application configuration management.

## Purpose
- Tests PDF generation using fpdf and pyfpdf libraries
- Validates application configuration management with AppConfig
- Tests contrib module integration and compatibility
- Ensures proper functionality of third-party components

## Key Classes and Methods

### Module Setup/Teardown Functions

#### `setUpModule()`
Module-level setup for contrib tests (currently empty).

#### `tearDownModule()`
Module-level cleanup that removes temporary config files:
- Removes `appconfig.json` test file if it exists

### TestContribs Class
Test suite for contrib package functionality.

#### Test Methods

##### `test_fpdf(self)`
Tests PDF generation functionality using fpdf library.

**Version Compatibility Testing:**
- **Version Match**: Ensures fpdf and pyfpdf have matching versions
- **Class Match**: Validates fpdf.FPDF and pyfpdf.FPDF are the same class
- **Import Consistency**: Tests that both imports reference the same implementation

**PDF Generation Testing:**
```python
pdf = fpdf.FPDF()
pdf.add_page()
pdf.compress = False
pdf.set_font("Arial", "", 14)
pdf.ln(10)
pdf.write(5, "hello world")
pdf_out = pdf.output("", "S")
```

**Content Validation:**
- **Version String**: Verifies FPDF version is embedded in PDF output
- **Content Integrity**: Ensures written text appears in PDF output
- **Binary Output**: Tests PDF generation returns proper binary data

##### `test_appconfig(self)`
Tests application configuration management using AppConfig.

**Configuration Setup:**
- **JSON Config**: Creates test configuration file with nested structure
- **Request Context**: Sets up mock request context for testing
- **File Management**: Creates and manages temporary config files

**Test Configuration Structure:**
```json
{
    "config1": "abc",
    "config2": "bcd", 
    "config3": {
        "key1": 1,
        "key2": 2
    }
}
```

**Configuration Access Testing:**
- **Direct Access**: Tests `myappconfig["config1"]` dictionary-style access
- **Take Method**: Tests `myappconfig.take("config1")` method access
- **Nested Access**: Tests `myappconfig.take("config3.key1")` dot notation
- **Type Casting**: Tests `cast=str` parameter for type conversion
- **Cast Persistence**: Validates that once cast, values maintain their type

## Dependencies
- `unittest` - Python testing framework
- `os` - Operating system interface
- `gluon._compat.to_bytes` - Compatibility utility for byte conversion
- `gluon.contrib.fpdf` - PDF generation library
- `gluon.contrib.pyfpdf` - Alternative PDF library import
- `gluon.contrib.appconfig.AppConfig` - Application configuration management
- `gluon.storage.Storage` - web2py storage utility

## Contrib Modules Tested

### PDF Generation (fpdf/pyfpdf)
- **Cross-compatibility**: Both fpdf and pyfpdf should work identically
- **PDF Creation**: Basic PDF document creation and formatting
- **Content Addition**: Text writing and formatting capabilities
- **Output Generation**: Binary PDF output generation

### Application Configuration (AppConfig)
- **JSON Parsing**: Configuration file parsing and loading
- **Nested Configuration**: Support for hierarchical configuration structures
- **Type Management**: Configuration value type casting and persistence
- **Context Integration**: Integration with web2py request context

## Usage Example
```python
# PDF Generation
from gluon.contrib import fpdf

pdf = fpdf.FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(40, 10, "Hello World", 0, 1)
pdf_output = pdf.output("document.pdf", "F")

# Application Configuration
from gluon.contrib.appconfig import AppConfig

config = AppConfig("private/appconfig.json")
database_uri = config.take("database.uri")
debug_mode = config.take("debug", cast=bool)
port = config.take("server.port", cast=int)
```

## Integration with web2py Framework

### PDF Generation Integration
- **Response Headers**: Automatic Content-Type setting for PDF responses  
- **File Serving**: Integration with web2py's file serving capabilities
- **Template Integration**: Can be used within controllers and views
- **Memory Management**: Efficient handling of PDF binary data

### Configuration Management Integration
- **Application Context**: Integrates with web2py's application structure
- **Private Files**: Uses application's private directory for config files
- **Request Context**: Accesses current request information
- **Environment Variables**: Can integrate with deployment configurations

### Third-party Library Management
- **Package Isolation**: Contrib packages are isolated from core framework
- **Version Management**: Maintains compatibility across different versions
- **Import Consistency**: Provides consistent import paths
- **Documentation**: Centralized documentation for contrib modules

## Test Coverage
- **PDF Functionality**: Basic PDF creation and content validation
- **Configuration Access**: Various methods of accessing config data
- **Type Handling**: Configuration value type casting and conversion
- **File Management**: Temporary file creation and cleanup
- **Import Validation**: Library import and compatibility checking
- **Context Integration**: web2py context and request handling

## Expected Results
- **PDF Generation**: Should create valid PDF documents with embedded content
- **Configuration Loading**: Should parse JSON configuration correctly
- **Type Casting**: Should handle type conversion and persistence properly
- **Import Compatibility**: fpdf and pyfpdf should be interchangeable
- **Context Access**: Should properly access web2py request context

## File Structure
```
gluon/tests/
├── test_contribs.py      # This file
└── ... (other test files)

gluon/contrib/
├── fpdf.py              # PDF generation library
├── pyfpdf.py            # Alternative PDF library
├── appconfig.py         # Application configuration management
└── ... (other contrib modules)
```

This test suite ensures that web2py's contrib package provides reliable functionality for PDF generation and application configuration management, maintaining compatibility and proper integration with the framework.