# gluon/contrib/fpdf/php.py

## Overview

The php.py module provides PHP-compatible helper functions for the FPDF library. Since FPDF was originally written in PHP, this module implements Python equivalents of common PHP functions to maintain compatibility with the original implementation and ease the porting process.

## Key Components

### String Manipulation Functions
Functions that mimic PHP's string handling behavior:
- **substr()**: PHP-style substring extraction
- **sprintf()**: PHP-style string formatting
- **str_repeat()**: Repeat string n times
- **str_pad()**: Pad string to certain length
- **strlen()**: String length (PHP compatible)

### Encoding Functions
UTF-8 and UTF-16 conversion utilities:
- **UTF8ToUTF16BE()**: Convert UTF-8 to UTF-16 Big Endian
- **UTF8StringToArray()**: Convert UTF-8 string to codepoint array

### Utility Functions
General purpose PHP-style utilities:
- **print_r()**: PHP-style array/dict printing
- **die()**: PHP-style fatal error
- **count()**: Array/list counting

## Function Implementations

### String Manipulation

#### substr()
```python
def substr(s, start, length=-1):
    """PHP-style substring function"""
    if length < 0:
        length = len(s) - start
    return s[start:start+length]
```
- Negative length means "to end of string"
- Maintains PHP substr() behavior

#### sprintf()
```python
def sprintf(fmt, *args):
    """PHP sprintf emulation"""
    return fmt % args
```
- Simple wrapper around Python's % formatting
- Maintains PHP sprintf() syntax

#### str_repeat()
```python
def str_repeat(s, count):
    """Repeat string count times"""
    return s * count
```
- Direct multiplication in Python
- Equivalent to PHP str_repeat()

#### str_pad()
```python
def str_pad(s, pad_length=0, pad_char=" ", pad_type=+1):
    """Pad string to specified length"""
    if pad_type < 0:  # pad left
        return s.rjust(pad_length, pad_char)
    elif pad_type > 0:  # pad right
        return s.ljust(pad_length, pad_char)
```
- pad_type: -1 for left, +1 for right
- Uses Python's built-in padding methods

### Encoding Functions

#### UTF8ToUTF16BE()
```python
def UTF8ToUTF16BE(instr, setbom=True):
    """Converts UTF-8 strings to UTF16-BE."""
    outstr = "".encode()
    if setbom:
        outstr += "\xFE\xFF".encode("latin1")
    if not isinstance(instr, unicode):
        instr = instr.decode('UTF-8')
    outstr += instr.encode('UTF-16BE')
    # Convert bytes back to fake unicode string for compatibility
    if PY3K:
        outstr = outstr.decode("latin1")
    return outstr
```

Key features:
- Optional BOM (Byte Order Mark) insertion
- Handles both Unicode and byte strings
- Python 2/3 compatibility handling
- Returns latin1-decoded string for PDF compatibility

#### UTF8StringToArray()
```python
def UTF8StringToArray(instr):
    """Converts UTF-8 strings to codepoints array"""
    return [ord(c) for c in instr]
```
- Converts each character to its Unicode codepoint
- Returns list of integers
- Used for font subsetting and character mapping

### Utility Functions

#### print_r()
```python
def print_r(array):
    """PHP-style array printing"""
    if not isinstance(array, dict):
        array = dict([(k, k) for k in array])
    for k, v in array.items():
        print("[%s] => %s " % (k, v))
```
- Mimics PHP's print_r() output format
- Converts non-dict inputs to dict representation
- Useful for debugging

#### die()
```python
def die(msg):
    """PHP-style fatal error"""
    raise RuntimeError(msg)
```
- Raises RuntimeError instead of exiting
- More Pythonic than sys.exit()
- Allows proper exception handling

## Python 2/3 Compatibility

### Import Handling
```python
from .py3k import PY3K, basestring, unicode
```
- Uses py3k module for compatibility layer
- Handles string type differences
- Ensures cross-version support

### String Type Management
- Checks for unicode type existence
- Handles encoding/decoding appropriately
- Maintains backward compatibility

## Integration with FPDF

### Font Processing
These functions are crucial for:
- Character width calculations
- UTF-16 encoding for PDF text
- Font subsetting operations

### Text Output
Used extensively in:
- PDF string formatting
- Text positioning calculations
- Multi-byte character handling

### Error Handling
- die() function for fatal errors
- Consistent error reporting
- PHP-style error messages

## Usage Examples

### String Operations
```python
# PHP-style substring
text = "Hello World"
sub = substr(text, 6, 5)  # "World"
sub2 = substr(text, 6)    # "World" (to end)

# String padding
padded = str_pad("test", 10, "*", -1)  # "******test"
padded2 = str_pad("test", 10, "-", +1)  # "test------"

# String repeat
repeated = str_repeat("ab", 3)  # "ababab"
```

### Encoding Operations
```python
# UTF-8 to UTF-16BE conversion
utf8_text = "Hello 世界"
utf16_text = UTF8ToUTF16BE(utf8_text)  # With BOM
utf16_no_bom = UTF8ToUTF16BE(utf8_text, setbom=False)

# String to codepoints
codepoints = UTF8StringToArray("ABC")  # [65, 66, 67]
```

### Debugging
```python
# Print array/dict PHP-style
data = {'name': 'John', 'age': 30}
print_r(data)
# Output:
# [name] => John
# [age] => 30

# Fatal error
if error_condition:
    die("Critical error occurred")
```

## Performance Considerations

### String Operations
- Python string operations are generally efficient
- Avoid repeated concatenation in loops
- Use join() for multiple concatenations

### Encoding Performance
- UTF-16 conversion can be memory intensive
- Cache converted strings when possible
- Consider batch processing for multiple conversions

## Best Practices

### Function Usage
1. Use these functions only for PHP compatibility
2. Prefer native Python methods when not interfacing with PHP code
3. Be aware of encoding implications

### Error Handling
1. Wrap die() calls in try-except when needed
2. Provide meaningful error messages
3. Consider logging before raising errors

### Character Encoding
1. Always specify encoding explicitly
2. Handle BOM requirements carefully
3. Test with multi-byte characters

## Limitations

### PHP Compatibility
- Not all PHP functions are implemented
- Some behavior differences may exist
- No PHP superglobal support

### Performance
- Additional function call overhead
- Some operations less efficient than native Python
- Memory usage for encoding conversions

### Type Handling
- PHP's loose typing not fully replicated
- Some implicit conversions missing
- Array/dict differences from PHP