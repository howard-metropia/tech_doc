# Gluon Decoder Module Technical Documentation

## Module: `decoder.py`

### Overview
The `decoder` module provides XML encoding auto-detection functionality for the Gluon web framework. It automatically detects the character encoding of XML documents and provides decoding utilities to convert byte streams to properly encoded Unicode text.

### Table of Contents
1. [Dependencies](#dependencies)
2. [Constants](#constants)
3. [Functions](#functions)
4. [Usage Examples](#usage-examples)
5. [Technical Details](#technical-details)
6. [Error Handling](#error-handling)

### Dependencies
```python
import codecs
from gluon._compat import to_unicode
```

### Constants

#### `autodetect_dict`
Dictionary mapping byte patterns to encoding names:
```python
autodetect_dict = {
    (0x00, 0x00, 0xFE, 0xFF): ("ucs4_be"),     # UTF-32 Big Endian
    (0xFF, 0xFE, 0x00, 0x00): ("ucs4_le"),     # UTF-32 Little Endian
    (0xFE, 0xFF, None, None): ("utf_16_be"),   # UTF-16 Big Endian
    (0xFF, 0xFE, None, None): ("utf_16_le"),   # UTF-16 Little Endian
    (0x00, 0x3C, 0x00, 0x3F): ("utf_16_be"),   # UTF-16 BE with XML
    (0x3C, 0x00, 0x3F, 0x00): ("utf_16_le"),   # UTF-16 LE with XML
    (0x3C, 0x3F, 0x78, 0x6D): ("utf_8"),       # UTF-8 with XML declaration
    (0x4C, 0x6F, 0xA7, 0x94): ("EBCDIC"),      # EBCDIC encoding
}
```

### Functions

#### `autoDetectXMLEncoding(buffer)`
Automatically detects XML encoding from a byte buffer using BOM (Byte Order Mark) detection and XML declaration parsing.

**Parameters:**
- `buffer` (bytes): Buffer containing at least 4 bytes of XML data

**Returns:**
- `str`: Encoding name (e.g., "utf_8", "utf_16_be", etc.)
- `None`: If encoding cannot be detected

**Algorithm:**
1. Examines first 4 bytes for BOM patterns
2. Falls back to UTF-8 as default encoding
3. If XML declaration found, extracts encoding attribute
4. Refines encoding based on XML declaration

**Example:**
```python
# Detect encoding from XML buffer
with open('document.xml', 'rb') as f:
    buffer = f.read(1024)
    encoding = autoDetectXMLEncoding(buffer)
    print(f"Detected encoding: {encoding}")
```

#### `decoder(buffer)`
Main decoder function that automatically detects and decodes XML content.

**Parameters:**
- `buffer` (bytes): Raw byte buffer containing XML data

**Returns:**
- `unicode/str`: Decoded Unicode string

**Example:**
```python
# Decode XML content automatically
with open('document.xml', 'rb') as f:
    raw_data = f.read()
    decoded_text = decoder(raw_data)
    print(decoded_text)
```

### Technical Details

#### Encoding Detection Process

1. **BOM Detection**: The module first checks for Byte Order Marks:
   - UTF-32 BE: `00 00 FE FF`
   - UTF-32 LE: `FF FE 00 00`
   - UTF-16 BE: `FE FF`
   - UTF-16 LE: `FF FE`
   - UTF-8 with XML: `3C 3F 78 6D` ("<?xm")

2. **Variable Byte Handling**: Uses `None` to represent variable bytes in patterns, allowing flexible matching.

3. **XML Declaration Parsing**: If initial detection succeeds, the module decodes enough of the document to read the XML declaration:
   ```xml
   <?xml version="1.0" encoding="ISO-8859-1"?>
   ```

4. **Quote Handling**: Supports both single and double quotes in encoding declarations:
   - `encoding="UTF-8"`
   - `encoding='UTF-8'`

#### Implementation Notes

**Performance Optimization:**
- Only decodes first line for XML declaration parsing
- Uses efficient byte pattern matching
- Caches codec lookups

**Compatibility:**
- Based on ActiveState Recipe 52257
- Licensed under PSF License
- Compatible with Python 2/3 via _compat module

### Error Handling

The module implements graceful fallback mechanisms:

1. **Default Encoding**: Falls back to UTF-8 if detection fails
2. **Partial Buffer**: Handles buffers shorter than 4 bytes
3. **Missing Codecs**: Returns encoding name even if decoder not installed
4. **Malformed XML**: Continues with best-guess encoding

### Usage Examples

#### Basic XML Decoding
```python
# Simple XML file decoding
def read_xml_file(filename):
    with open(filename, 'rb') as f:
        raw_data = f.read()
    return decoder(raw_data)

# Usage
xml_content = read_xml_file('data.xml')
```

#### Advanced Encoding Detection
```python
# Detect encoding without decoding
def get_xml_encoding(filename):
    with open(filename, 'rb') as f:
        # Read enough for detection
        buffer = f.read(1024)
    return autoDetectXMLEncoding(buffer)

# Check multiple files
files = ['utf8.xml', 'utf16.xml', 'latin1.xml']
for filename in files:
    encoding = get_xml_encoding(filename)
    print(f"{filename}: {encoding}")
```

#### Streaming XML Processing
```python
# Process large XML files with detected encoding
def process_large_xml(filename):
    # Detect encoding from beginning
    with open(filename, 'rb') as f:
        initial_buffer = f.read(1024)
        encoding = autoDetectXMLEncoding(initial_buffer)
    
    # Reopen with detected encoding
    with open(filename, 'r', encoding=encoding) as f:
        for line in f:
            process_line(line)
```

#### Error Handling Example
```python
# Robust XML reading with fallback
def safe_read_xml(data):
    try:
        # Try automatic detection
        return decoder(data)
    except Exception as e:
        # Fallback to UTF-8
        try:
            return data.decode('utf-8')
        except:
            # Last resort: Latin-1
            return data.decode('latin-1', errors='replace')
```

### Best Practices

1. **Buffer Size**: Provide at least 4 bytes for reliable detection
2. **XML Declaration**: Include encoding in XML declaration when possible
3. **BOM Usage**: Consider adding BOM for UTF-16/32 documents
4. **Error Handling**: Always implement fallback for unknown encodings
5. **Performance**: For large files, detect encoding once and reuse

### Security Considerations

1. **Input Validation**: Validate buffer contains actual XML data
2. **Encoding Injection**: Be cautious with user-provided encoding names
3. **Memory Usage**: Limit buffer size for untrusted sources
4. **EBCDIC Support**: Note that EBCDIC may not have installed decoder

### Integration with Gluon

The decoder module integrates with Gluon's Unicode handling:

```python
# Gluon template rendering
from gluon.decoder import decoder

def render_xml_template(xml_bytes):
    # Decode XML content
    xml_text = decoder(xml_bytes)
    
    # Process with Gluon template engine
    from gluon.template import render
    return render(xml_text)
```

### Module Metadata

- **License**: PSF License
- **Based On**: ActiveState Recipe 52257
- **Compatibility**: Python 2.7+, Python 3.x
- **Thread Safety**: Yes (no shared state)
- **Dependencies**: Standard library only