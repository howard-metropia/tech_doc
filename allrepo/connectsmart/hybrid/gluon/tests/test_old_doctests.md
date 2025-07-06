# test_old_doctests.py

## Overview
Unit test module that runs legacy doctests from various Gluon modules. This serves as a bridge to maintain backward compatibility while transitioning from doctests to proper unit tests.

## Imports
```python
import doctest
import unittest
```

## Purpose
This module exists to preserve and run existing doctests that were embedded in source code documentation. Web2py versions after 2.4.5 moved toward standard unit tests, but this ensures old doctests continue to be validated.

## Function: load_tests()

### Description
A test loader hook that integrates doctests into the unittest framework.

### Parameters
- `loader`: The test loader instance
- `tests`: The test suite to add tests to
- `ignore`: Ignored parameter (part of the load_tests protocol)

### Functionality
Adds doctest suites from three modules:

1. **gluon.html**
   - Contains doctests for HTML helper functions
   - Tests embedded in docstrings of HTML generation functions

2. **gluon.utf8**
   - Contains doctests for UTF-8 handling functions
   - Tests Unicode string operations and encoding

3. **gluon.contrib.markmin.markmin2html**
   - Contains doctests for Markmin to HTML conversion
   - Tests wiki-style markup transformation

### Returns
The augmented test suite containing both regular unit tests and doctests.

## Execution
When run as main module, executes all collected tests using `unittest.main()`.

## Historical Context

### Doctests vs Unit Tests
- **Doctests**: Tests embedded in docstrings, serve as both documentation and tests
- **Unit Tests**: Separate test files with dedicated test cases
- Web2py transitioned away from doctests for better test organization

### Example Doctest Format
```python
def function_with_doctest(param):
    """
    This function does something.
    
    >>> function_with_doctest("test")
    'result'
    >>> function_with_doctest(123)
    '123'
    """
    return str(param)
```

## Modules Being Tested

### gluon.html
Likely contains doctests for:
- HTML element generation
- Attribute handling
- Escaping functions
- Helper methods

### gluon.utf8
Likely contains doctests for:
- UTF-8 encoding/decoding
- String manipulation
- Character handling
- Byte/string conversions

### gluon.contrib.markmin.markmin2html
Likely contains doctests for:
- Markmin syntax parsing
- HTML generation from markup
- Special formatting rules
- Link and image handling

## Testing Strategy
This approach allows:
- Preservation of existing documentation-based tests
- Integration with modern test runners
- Gradual migration to dedicated unit tests
- Backward compatibility maintenance

## Notes
- The comment warns against abusing doctests in newer versions
- This file acts as a compatibility layer
- Doctests are useful for simple examples but can become unwieldy for complex testing
- The transition to unit tests provides better test organization and debugging capabilities