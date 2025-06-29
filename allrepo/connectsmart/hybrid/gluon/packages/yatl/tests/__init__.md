# __init__.py

## Overview
This file initializes the YATL (Yet Another Template Language) test suite, providing testing infrastructure for web2py's template engine functionality.

## Purpose
- Initializes YATL test module namespace
- Configures template testing environment
- Imports test utilities for template testing
- Provides common template test fixtures

## Key Components

### Test Organization
- **Template Tests**: Basic template rendering
- **Helper Tests**: HTML helper functionality
- **Security Tests**: XSS prevention and escaping
- **Performance Tests**: Template compilation speed

### Test Categories
- **Syntax Tests**: Template language features
- **Expression Tests**: Python expression evaluation
- **Block Tests**: Template inheritance testing
- **Include Tests**: Template inclusion mechanics

## Test Infrastructure

### Template Testing Setup
```python
# Test template environment
from yatl import render, Template
from yatl.helpers import *

# Mock context
context = {'name': 'Test', 'items': [1, 2, 3]}
```

### Test Utilities
- Template compilation helpers
- Rendering assertion methods
- HTML comparison functions
- Performance benchmarking

## Testing Patterns

### Template Rendering
- Basic variable substitution
- Control structures (if/for)
- Template inheritance
- Custom helpers

This YATL test initialization ensures comprehensive testing of web2py's template engine capabilities.