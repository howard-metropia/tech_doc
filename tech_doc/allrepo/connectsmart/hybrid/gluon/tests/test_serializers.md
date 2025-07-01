# test_serializers.py

## Overview
Unit tests for Web2py's serialization functionality, focusing on JSON serialization with special handling for various Python types and Web2py-specific objects.

## Imports
```python
import datetime
import decimal
import unittest
from gluon.html import SPAN
from gluon.languages import TranslatorFactory
from gluon.serializers import *
from gluon.storage import Storage
from .fix_path import fix_sys_path
```

## Test Class: TestSerializers

### Description
Tests the JSON serialization functionality with Web2py-specific enhancements and edge cases.

### Test Methods

#### testJSON()
Comprehensive test of the `json()` function and its various features.

**Test Cases:**

1. **Unicode Line/Paragraph Separators**
   ```python
   weird = {"JSON": "ro" + "\u2028" + "ck" + "\u2029" + "s!"}
   ```
   - Tests handling of Unicode line separator (U+2028)
   - Tests handling of Unicode paragraph separator (U+2029)
   - These are escaped to prevent JavaScript injection vulnerabilities
   - Expected output: `'{"JSON": "ro\\u2028ck\\u2029s!"}'`

2. **Date/Time Object Serialization**
   ```python
   objs = [
       datetime.datetime(2014, 1, 1, 12, 15, 35),
       datetime.date(2014, 1, 1),
       datetime.time(12, 15, 35),
   ]
   ```
   - Datetime objects converted to ISO format
   - 'T' separator replaced with space
   - Truncated to 19 characters (removing microseconds)
   - Ensures consistent format across all date/time types

3. **Decimal Number Handling**
   ```python
   obj = {"a": decimal.Decimal("4.312312312312")}
   ```
   - Decimal objects converted to numeric JSON values
   - Preserves precision without quotes
   - Output: `'{"a": 4.312312312312}'`

4. **Lazy Translation Objects**
   ```python
   T = TranslatorFactory("", "en")
   lazy_translation = T("abc")
   ```
   - TranslatorFactory creates lazy translation objects
   - These are evaluated and serialized as strings
   - Output: `'"abc"'`

5. **HTML Helper Serialization**
   ```python
   SPAN("abc")
   ```
   - With `cls=None`: Raw XML output `"<span>abc</span>"`
   - Default: HTML entities escaped for JavaScript safety
   - Output: `'"\\u003cspan\\u003eabc\\u003c/span\\u003e"'`

6. **Unicode Keys in JSON Loading**
   ```python
   base = {"è": 1, "b": 2}
   ```
   - Tests round-trip serialization with Unicode keys
   - `loads_json()` with `unicode_keys=True` (default) preserves Unicode
   - `unicode_keys=False` may convert keys to bytes (Python 2 behavior)

## Key Functions Tested

### json()
Web2py's enhanced JSON serializer that handles:
- Python datetime objects
- Decimal numbers
- Translation objects
- HTML helpers
- Unicode edge cases

### loads_json()
Web2py's JSON deserializer with options for:
- Unicode key handling
- Compatibility with different Python versions

## Serialization Features

### Security Enhancements
- Escapes Unicode separators to prevent injection
- HTML entities escaped by default
- Safe for embedding in JavaScript contexts

### Type Conversions
- **datetime/date/time**: ISO format without 'T'
- **Decimal**: Numeric value (not string)
- **LazyT**: Evaluated translation
- **HTML helpers**: XML representation

### Compatibility
- Handles Python 2/3 Unicode differences
- Configurable key encoding behavior
- Standards-compliant with extensions

## Testing Patterns

### Round-trip Testing
```python
base_enc = json(base)
base_load = loads_json(base_enc)
self.assertTrue(base == base_load)
```
Ensures data integrity through serialization cycle.

### Edge Case Coverage
- Unicode control characters
- Special object types
- Configuration options

### Type-specific Handling
Different serialization strategies for different types:
- Native JSON types: Direct conversion
- Date/time: String formatting
- Custom objects: Special handlers

## Web2py Serialization Philosophy

### Safe by Default
- Escapes potentially dangerous characters
- HTML-safe output
- JavaScript injection prevention

### Practical Defaults
- Human-readable date formats
- Decimal precision preservation
- Translation integration

### Extensibility
- Custom handlers for Web2py types
- Configurable behavior
- Backward compatibility

## Notes
- The `json()` function differs from standard `json.dumps()` to handle Web2py-specific types
- Security considerations drive many design decisions
- Unicode handling is critical for internationalization
- The serializer is designed for web contexts where data often moves between Python and JavaScript