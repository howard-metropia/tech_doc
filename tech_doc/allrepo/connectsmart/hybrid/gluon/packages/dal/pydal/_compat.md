# _compat.py

## Overview
Compatibility layer for PyDAL that provides unified interfaces across Python 2 and Python 3 versions, handling differences in standard library modules, string/bytes handling, and language features.

## Python Version Detection
```python
PY2 = sys.version_info[0] == 2
```

## Identity Function
```python
_identity = lambda x: x
```
Used as a no-op decorator for Python 3 where certain compatibility decorators aren't needed.

## Python 2 Compatibility (PY2 = True)

### Import Mappings
Maps Python 2 modules to their standard library locations:

**Core Modules:**
- `cPickle` → `pickle` (optimized pickle implementation)
- `cStringIO` → `StringIO` (optimized string I/O)
- `copy_reg` → `copyreg` (pickle registration)
- `__builtin__` → `builtin` (built-in functions)

**HTTP/URL Modules:**
- `urllib` → URL encoding/decoding functions
- `urllib2` → `urlopen` and HTTP handlers
- `HTMLParser` → HTML parsing
- `Cookie` → HTTP cookie handling
- `cookielib` → Cookie jar management

**Network/Protocol:**
- `xmlrpclib.ProtocolError` → XML-RPC errors
- `Queue` → Thread-safe queues
- `ConfigParser` → Configuration file parsing

**Email Support:**
- Complete email.MIME* module mappings
- `email.Encoders` and `email.Charset` support
- Header encoding and multipart message support

### String and Unicode Types
```python
string_types = (str, unicode)
text_type = unicode
basestring = basestring
unicodeT = unicode
```

### Integer Types
```python
integer_types = (int, long)
long = long
```

### Iterator Methods
```python
iterkeys = lambda d: d.iterkeys()
itervalues = lambda d: d.itervalues()
iteritems = lambda d: d.iteritems()
```

### Compatibility Functions

#### implements_bool(cls)
Decorator for Python 2 boolean compatibility:
- Maps `__bool__` to `__nonzero__`
- Removes `__bool__` method

#### implements_iterator(cls)
Decorator for Python 2 iterator compatibility:
- Maps `__next__` to `next`
- Removes `__next__` method

#### to_bytes(obj, charset="utf-8", errors="strict")
Converts objects to bytes in Python 2:
- **None**: Returns `None`
- **bytes/bytearray/buffer**: Returns `bytes(obj)`
- **unicode**: Encodes to bytes using specified charset
- **Other types**: Raises `TypeError`

#### to_native(obj, charset="utf8", errors="strict")
Converts to native string type (str in Python 2):
- **None/str**: Returns unchanged
- **Other**: Encodes to str using charset

## Python 3 Compatibility (PY2 = False)

### Import Mappings
Maps to Python 3 standard library locations:

**Core Modules:**
- `io.StringIO`, `io.BytesIO` → String/bytes I/O
- `importlib.reload` → Module reloading
- `functools.reduce` → Reduction operations
- `builtins` → Built-in functions

**HTTP/URL Modules:**
- `urllib.parse` → URL parsing and encoding
- `urllib.request` → HTTP requests
- `html.parser.HTMLParser` → HTML parsing
- `http.cookies` → Cookie handling

**Email Support:**
- `email.mime.*` → MIME type handling
- `email.encoders` → Email encoding
- Updated import paths for all email modules

### Type Redefinitions
```python
string_types = (str,)
text_type = str
basestring = str
integer_types = (int,)
long = int
unichr = chr
unicodeT = str
xrange = range
ClassType = type
```

### Iterator Methods
```python
iterkeys = lambda d: iter(d.keys())
itervalues = lambda d: iter(d.values())
iteritems = lambda d: iter(d.items())
```

### Hash Function
```python
hashlib_md5 = lambda s: hashlib.md5(bytes(s, "utf8"))
```

### Compatibility Decorators
```python
implements_iterator = _identity
implements_bool = _identity
```
No-op decorators since Python 3 uses the new methods directly.

#### to_bytes(obj, charset="utf-8", errors="strict")
Converts objects to bytes in Python 3:
- **None**: Returns `None`
- **bytes/bytearray/memoryview**: Returns `bytes(obj)`
- **str**: Encodes to bytes using specified charset
- **Other types**: Raises `TypeError`

#### to_native(obj, charset="utf8", errors="strict")
Converts to native string type (str in Python 3):
- **None/str**: Returns unchanged
- **Other**: Decodes to str using charset

## Cross-Version Functions

### with_metaclass(meta, *bases)
Creates a base class with a metaclass, compatible with both Python versions.

**Implementation Pattern:**
1. Creates temporary metaclass that inherits from target metaclass
2. Overrides `__new__` to return actual metaclass when instantiated
3. Returns temporary class for inheritance

**Usage:**
```python
class MyClass(with_metaclass(MyMeta, BaseClass)):
    pass
```

### to_unicode(obj, charset="utf-8", errors="strict")
Universal Unicode conversion:
- **None**: Returns `None`
- **No decode method**: Converts using `text_type(obj)`
- **Has decode method**: Calls `obj.decode(charset, errors)`

## File System Shortcuts
```python
pjoin = os.path.join
exists = os.path.exists
```

## Key Features

### Unified String Handling
- Abstracts differences between Python 2 unicode/str and Python 3 str/bytes
- Provides consistent encoding/decoding interfaces
- Handles None values gracefully

### Import Abstraction
- Single import point for modules that moved between Python versions
- Maintains same API regardless of Python version
- Covers all major standard library changes

### Type Compatibility
- Normalizes type checking across versions
- Provides consistent integer and string type tuples
- Handles iterator protocol differences

### Metaclass Support
- Cross-version metaclass creation
- Enables advanced ORM functionality
- Maintains Python 2/3 compatibility

## Usage in PyDAL
This module is imported throughout PyDAL to ensure:
- Database drivers work on both Python versions
- String/bytes handling is consistent
- Email functionality works across versions
- HTTP and URL handling is unified

## Notes
- Essential for maintaining Python 2/3 compatibility in PyDAL
- Provides foundation for all other PyDAL modules
- Handles most common compatibility issues in single location
- Enables gradual migration between Python versions