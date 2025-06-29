# test_old_doctests.py

## Overview
This file contains unit tests for legacy doctests from older web2py modules. It serves as a compatibility layer for existing doctests in modules like html.py, utf8.py, and markmin2html.py, while the framework transitions to pure unittest-based testing.

## Purpose
- Maintains backward compatibility with existing doctests
- Provides transition path from doctests to unittests
- Tests legacy functionality in core modules
- Ensures existing documentation examples continue to work
- Provides deprecation pathway for doctests

## Key Functions

### `load_tests(loader, tests, ignore)`
Discovery function that loads doctests from specified modules.

**Modules Tested:**
- **gluon.html**: HTML generation and helper functions
- **gluon.utf8**: UTF-8 encoding and Unicode handling
- **gluon.contrib.markmin.markmin2html**: Markmin markup to HTML conversion

**Implementation:**
```python
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite("gluon.html"))
    tests.addTests(doctest.DocTestSuite("gluon.utf8"))
    tests.addTests(doctest.DocTestSuite("gluon.contrib.markmin.markmin2html"))
    return tests
```

## Dependencies
- `doctest` - Python's doctest module
- `unittest` - Python's unittest framework
- `gluon.html` - HTML generation module
- `gluon.utf8` - UTF-8 handling module
- `gluon.contrib.markmin.markmin2html` - Markmin converter

## Tested Modules

### gluon.html
**Functionality Tested:**
- HTML helper functions and tag generation
- XML and HTML parsing capabilities
- URL generation and manipulation
- Form helper functions
- Template helper integration

**Example Doctests:**
- DIV, SPAN, A, and other HTML tag creation
- Attribute handling and escaping
- Nested tag structures
- URL generation with parameters

### gluon.utf8
**Functionality Tested:**
- UTF-8 encoding and decoding operations
- Unicode string handling
- Character encoding detection
- Cross-platform encoding compatibility
- String manipulation with Unicode

**Example Doctests:**
- Encoding conversion functions
- Unicode normalization
- Character set detection
- Encoding error handling

### gluon.contrib.markmin.markmin2html
**Functionality Tested:**
- Markmin markup language parsing
- HTML conversion from Markmin syntax
- Syntax highlighting support
- Link and reference handling
- Code block processing

**Example Doctests:**
- Basic markup conversion (headers, emphasis, lists)
- Code syntax highlighting
- Link generation and validation
- Table and structure conversion

## Doctest Integration

### Test Discovery
- **Automatic Discovery**: Uses doctest.DocTestSuite for module scanning
- **Integration**: Seamlessly integrates with unittest framework
- **Execution**: Runs doctests as part of regular test suite
- **Reporting**: Provides unified test reporting

### Compatibility Layer
- **Legacy Support**: Maintains existing doctest functionality
- **Transition Path**: Allows gradual migration to unittests
- **Documentation**: Keeps documentation examples functional
- **Validation**: Ensures code examples in docs remain accurate

## Usage Example
```python
# Run doctests manually
import doctest
import gluon.html
import gluon.utf8
import gluon.contrib.markmin.markmin2html

# Test individual modules
doctest.testmod(gluon.html)
doctest.testmod(gluon.utf8)
doctest.testmod(gluon.contrib.markmin.markmin2html)

# Run through unittest framework
import unittest
suite = unittest.TestLoader().loadTestsFromModule(test_old_doctests)
unittest.TextTestRunner().run(suite)
```

## Integration with web2py Framework

### Documentation Testing
- **Code Examples**: Validates code examples in documentation
- **API Consistency**: Ensures API examples remain current
- **Tutorial Validation**: Tests tutorial code snippets
- **Reference Accuracy**: Maintains reference documentation accuracy

### Quality Assurance
- **Regression Testing**: Prevents breaking changes to documented APIs
- **Example Validation**: Ensures examples produce expected output
- **API Stability**: Validates public API consistency
- **Documentation Quality**: Maintains high-quality documentation

### Development Workflow
- **Code Documentation**: Encourages well-documented code
- **Example Maintenance**: Keeps examples up-to-date
- **API Evolution**: Manages API changes with documentation impact
- **Testing Integration**: Unified testing approach

## Deprecation Notice

### Future Direction
```python
# Note from file header:
# "Don't abuse doctests, web2py > 2.4.5 will accept only unittests"
```

**Transition Strategy:**
- **Legacy Support**: Maintains existing doctests during transition
- **New Development**: Encourages unittest adoption for new code
- **Migration Path**: Provides clear path for converting doctests
- **Timeline**: Gradual phase-out of doctests in favor of unittests

### Best Practices
- **New Code**: Use unittests for all new functionality
- **Documentation**: Keep examples simple and focused
- **Testing**: Separate testing from documentation
- **Maintenance**: Regular review and update of legacy doctests

## Test Coverage
- **HTML Generation**: Core HTML functionality
- **Unicode Handling**: UTF-8 and encoding operations
- **Markup Conversion**: Markmin to HTML processing
- **Documentation Examples**: Code examples in documentation
- **API Consistency**: Public API behavior validation

## Expected Results
- **Doctest Execution**: All doctests should pass
- **Output Validation**: Generated output should match expected results
- **Error Handling**: Proper error handling in examples
- **Performance**: Reasonable execution time for doctest suite
- **Compatibility**: Cross-platform doctest execution

## File Structure
```
gluon/tests/
├── test_old_doctests.py  # This file
└── ... (other test files)

# Tested modules
gluon/
├── html.py               # HTML generation with doctests
├── utf8.py               # UTF-8 handling with doctests
└── contrib/markmin/
    └── markmin2html.py   # Markmin conversion with doctests
```

This test file ensures backward compatibility with existing doctests while providing a transition path to modern unittest-based testing practices in web2py development.