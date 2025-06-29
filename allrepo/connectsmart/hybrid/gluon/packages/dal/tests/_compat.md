# _compat.py

## Overview
This file provides Python 2/3 compatibility testing for PyDAL, ensuring the database abstraction layer works seamlessly across different Python versions.

## Purpose
- Tests Python version compatibility
- Validates string/unicode handling
- Ensures import compatibility
- Verifies behavior consistency across Python versions

## Key Compatibility Areas

### String Handling
- **Unicode Support**: Python 2 unicode vs Python 3 str
- **Byte Strings**: Encoding/decoding behavior
- **String Operations**: Consistent string manipulation
- **Database Encoding**: UTF-8 compatibility

### Import Compatibility
- **Module Imports**: Python 2/3 import differences
- **Built-in Changes**: xrange/range, iteritems/items
- **Exception Handling**: except syntax variations
- **Print Function**: print statement vs function

## Version-Specific Tests

### Python 2 Compatibility
```python
# Unicode literals
u'unicode string'
# Long integers
123L
# Division behavior
1/2 == 0
```

### Python 3 Compatibility
```python
# Native unicode strings
'unicode by default'
# No long type
123
# True division
1/2 == 0.5
```

## Database Compatibility

### Encoding Tests
- UTF-8 data storage and retrieval
- Binary data handling
- Special character support
- Collation compatibility

This compatibility testing ensures PyDAL maintains consistent behavior across Python versions while properly handling database operations.