# __init__.py

## Overview
This file serves as the package initialization file for the gluon tests module. It imports all test modules and makes them available for the testing framework, with conditional import support for Python version compatibility.

## Purpose
- Centralizes test module imports for easy access
- Provides a single entry point for all gluon test modules
- Handles Python version-specific test imports
- Enables package-level test discovery and execution

## Module Imports
The file imports all test modules using relative imports:

### Core Test Modules
- `test_appadmin` - Application administration interface tests
- `test_authapi` - Authentication API tests
- `test_cache` - Caching system tests
- `test_compileapp` - Application compilation tests
- `test_contenttype` - Content type detection tests
- `test_contribs` - Contributed modules tests
- `test_cron` - Cron scheduler tests
- `test_dal` - Database Abstraction Layer tests
- `test_fileutils` - File utility tests
- `test_globals` - Global objects tests
- `test_html` - HTML generation tests
- `test_http` - HTTP handling tests
- `test_languages` - Internationalization tests
- `test_recfile` - Record file tests
- `test_redis` - Redis cache tests
- `test_router` - URL routing tests
- `test_routes` - URL routes tests
- `test_scheduler` - Task scheduler tests
- `test_serializers` - Data serialization tests
- `test_sqlhtml` - SQL HTML form tests
- `test_storage` - Storage utilities tests
- `test_tools` - Framework tools tests
- `test_utils` - Utility functions tests
- `test_web` - Web framework tests

### Version-Specific Imports
```python
if sys.version[:3] == "2.7":
    from .test_old_doctests import *
```
- Conditionally imports legacy doctest module for Python 2.7 compatibility

## Dependencies
- `sys` module for Python version detection (implicit import)

## Usage Example
```python
# Import all tests
from gluon.tests import *

# Or import specific test modules
from gluon.tests.test_cache import TestCache
from gluon.tests.test_dal import TestDAL
```

## Integration with web2py Framework
- Provides comprehensive test coverage for all major web2py components
- Enables automated testing of framework functionality
- Supports continuous integration and quality assurance
- Facilitates regression testing during development

## Test Organization
The test module follows a structured approach:
- Each major gluon component has its own test module
- Tests are organized by functionality and component
- Supports both unit testing and integration testing
- Provides version compatibility for different Python versions

## Package Structure
```
gluon/tests/
├── __init__.py           # This file - package initialization
├── test_appadmin.py      # Admin interface tests
├── test_authapi.py       # Authentication tests
├── test_cache.py         # Caching tests
└── ... (other test modules)
```

This initialization file ensures that all gluon test modules are properly packaged and accessible for comprehensive framework testing.