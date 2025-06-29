# test_contenttype.py

## Overview
This file contains unit tests for the web2py content type detection system. It tests the functionality of the `contenttype` module which determines MIME types based on file extensions, ensuring proper HTTP Content-Type headers are set for different file types.

## Purpose
- Tests MIME type detection based on file extensions
- Validates web2py-specific content type mappings
- Tests standard and custom file type recognition
- Ensures proper Content-Type header generation
- Tests edge cases and error handling for unknown types

## Key Classes and Methods

### TestContentType Class
Test suite for content type detection functionality.

#### Test Methods

##### `testTypeRecognition(self)`
Comprehensive test for file type recognition and MIME type mapping.

**Standard Image Types:**
```python
contenttype(".png")  # Returns "image/png"
contenttype(".gif")  # Returns "image/gif"
```

**Compressed Archive Types:**
```python
contenttype(".tar.bz2")  # Returns "application/x-bzip-compressed-tar"
```

**web2py-Specific Mappings:**
The test validates custom content type mappings specific to web2py:

```python
mapping = {
    ".load": "text/html; charset=utf-8",      # LOAD components
    ".json": "application/json",              # JSON data
    ".jsonp": "application/jsonp",            # JSONP callbacks
    ".pickle": "application/python-pickle",   # Python pickle files
    ".w2p": "application/w2p",                # web2py application packages
    ".md": "text/x-markdown; charset=utf-8",  # Markdown files
}
```

**Extension Validation:**
- **With Dot**: Tests extensions with leading dot (standard format)
- **Without Dot**: Tests handling of extensions without dot prefix
- **Unknown Types**: Tests fallback to default content type

**Edge Case Testing:**
```python
contenttype("png")  # Without dot - returns "text/plain; charset=utf-8"
```

## Dependencies
- `unittest` - Python testing framework
- `gluon._compat.iteritems` - Cross-version dictionary iteration
- `gluon.contenttype.contenttype` - Content type detection function

## Content Type Function

### `contenttype(extension)`
Main function for determining MIME type from file extension.

**Parameters:**
- `extension` (str) - File extension with or without leading dot

**Returns:**
- `str` - MIME type string with optional charset specification

**Behavior:**
- **Standard Types**: Uses Python's mimetypes module for common extensions
- **Custom Mappings**: Applies web2py-specific overrides and additions
- **Charset Handling**: Adds UTF-8 charset for text-based content
- **Fallback**: Returns "text/plain; charset=utf-8" for unknown types

## Usage Example
```python
from gluon.contenttype import contenttype

# Standard image types
mime_type = contenttype(".jpg")     # Returns "image/jpeg"
mime_type = contenttype(".png")     # Returns "image/png"

# web2py specific types
mime_type = contenttype(".load")    # Returns "text/html; charset=utf-8"
mime_type = contenttype(".json")    # Returns "application/json"
mime_type = contenttype(".w2p")     # Returns "application/w2p"

# Markdown files
mime_type = contenttype(".md")      # Returns "text/x-markdown; charset=utf-8"

# Unknown extensions
mime_type = contenttype(".xyz")     # Returns "text/plain; charset=utf-8"
mime_type = contenttype("txt")      # Without dot - returns default
```

## Integration with web2py Framework

### HTTP Response Headers
- **Content-Type Setting**: Automatically sets proper HTTP headers
- **Character Encoding**: Ensures UTF-8 encoding for text content
- **Browser Compatibility**: Provides standard MIME types browsers recognize

### File Serving
- **Static Files**: Determines content type for static file serving
- **Dynamic Content**: Sets appropriate headers for generated content
- **Download Handling**: Proper headers for file downloads

### Component Integration
- **LOAD Components**: Special handling for .load files as HTML
- **AJAX Responses**: Proper content types for JSON/JSONP responses
- **Application Packages**: Recognition of .w2p application files

### Development Tools
- **Documentation**: Markdown file support for documentation
- **Debugging**: Proper content types for development files
- **Serialization**: Recognition of pickle and other serialization formats

## MIME Type Categories

### Text Content
- **HTML**: `text/html; charset=utf-8` for .load files
- **Markdown**: `text/x-markdown; charset=utf-8` for .md files
- **Plain Text**: `text/plain; charset=utf-8` for unknown types

### Application Data
- **JSON**: `application/json` for structured data
- **JSONP**: `application/jsonp` for cross-domain requests
- **Pickle**: `application/python-pickle` for Python serialization
- **web2py Packages**: `application/w2p` for application archives

### Standard Types
- **Images**: Standard image MIME types (image/png, image/gif, etc.)
- **Archives**: Compressed file types with proper application types
- **Documents**: Standard document MIME types

## Test Coverage
- **Standard Extensions**: Common file types (images, documents)
- **Custom Extensions**: web2py-specific file types
- **Edge Cases**: Extensions without dots, unknown types
- **Character Encoding**: UTF-8 charset for text content
- **Fallback Behavior**: Default handling for unrecognized types

## Expected Behavior
- **Accurate Detection**: Returns correct MIME type for known extensions
- **Consistent Formatting**: Proper MIME type string format
- **Charset Inclusion**: UTF-8 charset for text-based content
- **Graceful Fallback**: Safe default for unknown extensions
- **Case Handling**: Proper handling of extension format variations

## File Structure
```
gluon/tests/
├── test_contenttype.py   # This file
└── ... (other test files)
```

This test suite ensures the web2py content type detection system accurately identifies file types and provides proper MIME type information for HTTP responses and file handling operations.