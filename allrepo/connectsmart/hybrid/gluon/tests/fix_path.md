# fix_path.py

## Overview
This file provides path fixing utilities for web2py tests, ensuring tests can properly locate and import web2py modules regardless of the test execution location.

## Purpose
- Fixes Python import paths for testing
- Ensures web2py modules are discoverable
- Handles relative path resolution
- Supports various test execution contexts

## Key Functions

### Path Manipulation
```python
def fix_sys_path():
    """Add web2py root to Python path"""
    import os
    import sys
    path = os.path.dirname(os.path.abspath(__file__))
    parent = os.path.dirname(os.path.dirname(path))
    if parent not in sys.path:
        sys.path.insert(0, parent)
```

### Import Helpers
- **add_path()**: Adds directory to sys.path
- **remove_path()**: Cleans up test paths
- **get_root()**: Finds web2py root directory
- **setup_environment()**: Configures test environment

## Test Environment Setup

### Path Configuration
- Gluon module discovery
- Application path setup
- Static file locations
- Temporary directory handling

### Cross-Platform Support
- Windows path handling
- Unix/Linux compatibility
- MacOS considerations
- Virtual environment support

## Usage Patterns

### Test Initialization
```python
# At the top of test files
import fix_path
fix_path.fix_sys_path()

# Now can import gluon modules
from gluon import *
```

This path fixing utility ensures web2py tests run reliably across different environments and execution contexts.