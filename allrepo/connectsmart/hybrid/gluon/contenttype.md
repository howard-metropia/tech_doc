# Gluon Content Type Module Documentation

## Overview
The `contenttype.py` module provides comprehensive MIME type detection and content type determination for the Gluon web framework. It implements a file extension-based mapping system to identify appropriate Content-Type headers for HTTP responses, supporting over 800 different file formats.

## Module Information
- **File**: `allrepo/connectsmart/hybrid/gluon/contenttype.py`
- **Component**: Web2py Framework Content Type Handler
- **Purpose**: MIME type detection and Content-Type header generation
- **Dependencies**: gluon._compat
- **Standard**: Based on freedesktop.org shared MIME info database v1.1

## Key Components

### Main Function
```python
def contenttype(filename, default="text/plain"):
    """
    Returns the Content-Type string matching extension of the given filename.
    """
```

**Parameters:**
- `filename`: File name or path to analyze
- `default`: Default content type (default: "text/plain")

**Returns:**
- Content-Type string with charset for text files
- Raw content type for binary files

### CONTENT_TYPE Dictionary
Comprehensive mapping of file extensions to MIME types:

#### Document Formats
```python
".pdf": "application/pdf",
".doc": "application/msword",
".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
".xls": "application/vnd.ms-excel",
".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
".ppt": "application/vnd.ms-powerpoint",
".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
```

#### Image Formats
```python
".jpg": "image/jpeg",
".jpeg": "image/jpeg",
".png": "image/png",
".gif": "image/gif",
".bmp": "image/bmp",
".svg": "image/svg+xml",
".ico": "image/vnd.microsoft.icon",
".tiff": "image/tiff",
".webp": "image/webp",
```

#### Audio Formats
```python
".mp3": "audio/mpeg",
".wav": "audio/x-wav",
".ogg": "application/ogg",
".flac": "audio/flac",
".aac": "audio/aac",
".wma": "audio/x-ms-wma",
".m4a": "audio/mp4",
```

#### Video Formats
```python
".mp4": "video/mp4",
".avi": "video/x-msvideo",
".mov": "video/quicktime",
".wmv": "video/x-ms-wmv",
".flv": "video/x-flv",
".webm": "video/webm",
".mkv": "video/x-matroska",
```

#### Web Formats
```python
".html": "text/html",
".htm": "text/html",
".css": "text/css",
".js": "application/javascript",
".json": "application/json",
".xml": "application/xml",
".rss": "application/rss+xml",
".atom": "application/atom+xml",
```

#### Programming Languages
```python
".py": "text/x-python",
".java": "text/x-java",
".c": "text/x-csrc",
".cpp": "text/x-c++src",
".h": "text/x-chdr",
".php": "application/x-php",
".rb": "application/x-ruby",
".pl": "application/x-perl",
```

#### Archive Formats
```python
".zip": "application/zip",
".rar": "application/x-rar",
".7z": "application/x-7z-compressed",
".tar": "application/x-tar",
".gz": "application/gzip",
".bz2": "application/x-bzip",
".xz": "application/x-xz",
```

### Special Handling

#### Multiple Extensions
The function handles files with multiple extensions by checking both:
1. Complete extension (e.g., `.tar.gz`)
2. Final extension (e.g., `.gz`)

```python
def contenttype(filename, default="text/plain"):
    filename = to_native(filename)
    i = filename.rfind(".")
    if i >= 0:
        default = CONTENT_TYPE.get(filename[i:].lower(), default)
        j = filename.rfind(".", 0, i)
        if j >= 0:
            default = CONTENT_TYPE.get(filename[j:].lower(), default)
```

#### Text File Charset
Automatic UTF-8 charset addition for text files:
```python
if default.startswith("text/"):
    default += "; charset=utf-8"
```

### Deviations from Standards

#### Custom Mappings
```python
# Deviations from official standards:
# - .md: application/x-genesis-rom --> text/x-markdown
# - .png: image/x-apple-ios-png --> image/png
```

#### Web2py Additions
```python
# Additions specific to web2py:
".load": "text/html",        # Web2py LOAD components
".json": "application/json",  # JSON data
".jsonp": "application/jsonp", # JSONP callbacks
".pickle": "application/python-pickle", # Python pickle files
".w2p": "application/w2p",    # Web2py package files
```

### Supported File Categories

#### Document Types
- **Office**: Microsoft Office (doc, xls, ppt) and OpenDocument formats
- **PDF**: Portable Document Format and variants
- **Text**: Plain text, markup languages, configuration files
- **eBooks**: EPUB, MOBI, and other e-reader formats

#### Media Types
- **Images**: Raster (JPEG, PNG, GIF) and vector (SVG, EPS) formats
- **Audio**: Compressed (MP3, AAC) and uncompressed (WAV, FLAC) formats
- **Video**: Modern (MP4, WebM) and legacy (AVI, MOV) formats

#### Development Files
- **Source Code**: Multiple programming languages
- **Configuration**: Various config file formats
- **Data**: JSON, XML, CSV, and database formats

#### System Files
- **Archives**: Various compression formats
- **Executables**: Platform-specific binary formats
- **Fonts**: TrueType, OpenType, and bitmap fonts

### Usage Examples

#### Basic Usage
```python
from gluon.contenttype import contenttype

# Simple file extension
content_type = contenttype("document.pdf")
# Returns: "application/pdf"

# Text file with charset
content_type = contenttype("script.py")
# Returns: "text/x-python; charset=utf-8"

# Unknown extension
content_type = contenttype("unknown.xyz")
# Returns: "text/plain; charset=utf-8"
```

#### Multiple Extensions
```python
# Compressed archive
content_type = contenttype("backup.tar.gz")
# Returns: "application/x-compressed-tar"

# Compressed PDF
content_type = contenttype("document.pdf.gz")
# Returns: "application/x-gzpdf"
```

#### Custom Default
```python
# Custom default for unknown files
content_type = contenttype("binary.unknown", "application/octet-stream")
# Returns: "application/octet-stream"
```

### Integration with Web2py

#### HTTP Response Headers
```python
# In controllers/views
response.headers['Content-Type'] = contenttype(filename)
```

#### File Downloads
```python
# Force download with correct content type
def download():
    filename = request.args(0)
    response.headers['Content-Type'] = contenttype(filename)
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response.stream(open(filename, 'rb'))
```

### Performance Characteristics

#### Lookup Speed
- **O(1)** dictionary lookup for known extensions
- **O(n)** string operations for extension extraction
- Minimal memory overhead

#### Memory Usage
- Static dictionary loaded once
- No dynamic allocations during lookup
- Efficient string handling

### Security Considerations

#### File Type Validation
```python
# Validate file type before processing
def is_safe_file(filename):
    content_type = contenttype(filename)
    return content_type.startswith(('text/', 'image/', 'application/json'))
```

#### Content Sniffing Prevention
- Explicit Content-Type headers prevent browser content sniffing
- Reduces XSS vulnerabilities from misinterpreted files
- Ensures proper file handling

### Extension Coverage

#### Comprehensive Support
- **800+** file extensions supported
- **Modern formats**: WebP, WebM, AVIF
- **Legacy formats**: BMP, AVI, older Office formats
- **Specialized formats**: CAD, scientific, gaming

#### Regular Updates
- Based on freedesktop.org MIME database
- Periodic updates for new formats
- Backward compatibility maintained

### Error Handling

#### Graceful Degradation
- Unknown extensions return configurable default
- No exceptions for invalid filenames
- Handles edge cases (empty strings, no extensions)

#### Robust Processing
```python
# Handles various filename formats
contenttype("/path/to/file.txt")      # Works
contenttype("file.txt")               # Works
contenttype("file")                   # Returns default
contenttype("")                       # Returns default
```

This content type module provides essential MIME type detection functionality for the Gluon framework, ensuring proper HTTP Content-Type headers for all file types while maintaining excellent performance and comprehensive format support.