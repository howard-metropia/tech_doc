# gluon/contrib/fpdf/py3k.py

## Overview

The py3k.py module provides a compatibility layer between Python 2 and Python 3 for the FPDF library. It handles differences in imports, string types, and various standard library changes, ensuring the FPDF library works seamlessly across Python versions.

## Key Components

### Version Detection
```python
PY3K = sys.version_info >= (3, 0)
```
- Global flag indicating Python 3.x environment
- Used throughout FPDF for conditional logic

### Import Compatibility
The module provides unified imports for modules that changed between Python versions:
- **pickle/cPickle**: Serialization support
- **urllib/urllib.request**: URL operations
- **StringIO/BytesIO**: In-memory file operations
- **md5/hashlib**: Hashing functions
- **HTMLParser**: HTML parsing
- **Image/PIL**: Image processing

## Compatibility Imports

### Serialization
```python
try:
    import cPickle as pickle  # Python 2 - faster C implementation
except ImportError:
    import pickle  # Python 3 - unified module
```
- Prefers cPickle for performance in Python 2
- Falls back to standard pickle in Python 3

### URL Operations
```python
try:
    from urllib import urlopen  # Python 2
except ImportError:
    from urllib.request import urlopen  # Python 3
```
- Handles urllib module reorganization
- Maintains consistent API

### I/O Operations
```python
try:
    from io import BytesIO  # Python 3
except ImportError:
    try:
        from cStringIO import StringIO as BytesIO  # Python 2 - C version
    except ImportError:
        from StringIO import StringIO as BytesIO  # Python 2 - pure Python
```
- Provides BytesIO for binary data handling
- Performance optimization with cStringIO when available

### Hashing
```python
try:
    from hashlib import md5  # Modern approach
except ImportError:
    try:
        from md5 import md5  # Legacy Python
    except ImportError:
        md5 = None  # No MD5 support
```

### Image Processing
```python
try:
    from PIL import Image  # Pillow (preferred)
except ImportError:
    try:
        import Image  # PIL (legacy)
    except ImportError:
        Image = None  # No image support
```

## String Type Handling

### Type Definitions
```python
if PY3K:
    basestring = str
    unicode = str
    ord = lambda x: x if isinstance(x, int) else ord(x)
else:
    basestring = basestring
    unicode = unicode
    ord = ord
```
- Unifies string type checking
- Handles unicode/str differences
- Adapts ord() for byte handling

### String Helpers
```python
def b(s):
    """Convert string to bytes"""
    if isinstance(s, basestring):
        return s.encode("latin1")
    return s
```
- Ensures byte representation
- Uses latin1 encoding for PDF compatibility

### Exception Handling
```python
def exception():
    """Get current exception for re-raising"""
    return sys.exc_info()[1]
```
- Provides consistent exception access
- Works across Python versions

## Utility Functions

### Path Hashing
```python
def hashpath(fn):
    """Generate MD5 hash of filename"""
    h = md5()
    if PY3K:
        h.update(fn.encode("UTF-8"))
    else:
        h.update(fn)
    return h.hexdigest()
```
- Creates deterministic hash from filepath
- Handles string encoding for Python 3
- Used for cache file naming

## HTML Parser Compatibility

### Parser Import
```python
if PY3K:
    from html.parser import HTMLParser
else:
    from HTMLParser import HTMLParser
```
- Module relocated in Python 3
- Maintains same class name

## Usage Patterns

### Version-Specific Code
```python
if PY3K:
    # Python 3 specific code
    text = str(data, 'utf-8')
else:
    # Python 2 specific code
    text = unicode(data, 'utf-8')
```

### String Type Checking
```python
if isinstance(value, basestring):
    # Works for both str (Py3) and str/unicode (Py2)
    process_string(value)
```

### Binary Data Handling
```python
# Create in-memory binary file
buffer = BytesIO()
buffer.write(b('binary data'))
buffer.seek(0)
```

## Integration with FPDF

### Font Cache Management
- hashpath() used for cache file generation
- Ensures consistent naming across platforms

### Image Processing
- Conditional Image support
- Graceful degradation without PIL/Pillow

### Serialization
- Font metric caching using pickle
- Cross-version compatibility

## Best Practices

### Import Usage
1. Always import from py3k module
2. Use provided aliases consistently
3. Avoid direct version checks when possible

### String Handling
1. Use basestring for type checking
2. Explicitly encode/decode at boundaries
3. Prefer bytes for binary data

### Exception Management
1. Use exception() helper for re-raising
2. Maintain exception context
3. Handle version differences gracefully

## Performance Considerations

### Import Optimization
- Attempts faster C implementations first
- Falls back to pure Python versions
- One-time import cost

### String Operations
- Encoding/decoding overhead in Python 3
- Type checking simplified with basestring
- Consistent performance across versions

## Limitations and Constraints

### Missing Dependencies
- Image processing requires PIL/Pillow
- MD5 might not be available in restricted environments
- Some imports may fail in embedded Python

### API Differences
- Not all API differences are abstracted
- Some manual version checking still required
- Complex compatibility issues need custom solutions

### Maintenance Burden
- Must track Python version changes
- New Python versions may require updates
- Deprecation warnings need monitoring

## Error Handling

### Import Failures
```python
try:
    from module import feature
except ImportError:
    feature = None  # Graceful degradation
```

### Function Availability
```python
if Image is None:
    raise RuntimeError("PIL/Pillow required for image support")
```

### Version Detection
```python
if not PY3K and sys.version_info < (2, 6):
    raise RuntimeError("Python 2.6+ required")
```

## Future Compatibility

### Python 3 Transition
- Module designed for Python 2 to 3 migration
- Can be simplified when Python 2 support dropped
- Provides clear migration path

### Deprecation Handling
- Handles deprecated modules gracefully
- Provides fallback options
- Maintains backward compatibility