# Content Type Detection Tests

🔍 **Quick Summary (TL;DR)**
- Unit tests for web2py's MIME type detection system that maps file extensions to proper HTTP Content-Type headers
- Core functionality: mime-type-detection | content-type-mapping | file-extension-handling | http-headers | media-type-validation
- Primary use cases: file serving validation, HTTP response header testing, media type recognition, web asset delivery
- Compatibility: Python 2/3, unittest framework, supports standard and custom MIME types

❓ **Common Questions Quick Index**
- Q: What file types are tested? → See Detailed Code Analysis
- Q: How are custom MIME types handled? → See Technical Specifications
- Q: What about unknown file extensions? → See Output Examples
- Q: How to add new content types? → See Usage Methods
- Q: What if extension has no dot prefix? → See Important Notes
- Q: How are override mappings tested? → See Detailed Code Analysis
- Q: What about charset specifications? → See Technical Specifications
- Q: How to debug content type issues? → See Important Notes
- Q: What's the fallback behavior? → See Output Examples
- Q: How to test custom mappings? → See Use Cases

📋 **Functionality Overview**
- **Non-technical explanation:** Like a smart filing system that automatically knows what type of document each file is based on its extension - just as a librarian can tell if something is a book, magazine, or DVD by looking at it, this system identifies web files as images, text, videos, or other types so browsers know how to handle them properly.
- **Technical explanation:** Test suite validating web2py's content type detection system that maps file extensions to MIME types for proper HTTP Content-Type header generation, including custom overrides for web-specific formats.
- Business value: Ensures proper file serving and browser compatibility, preventing download issues and enabling correct rendering of web assets.
- Context: Essential component of web2py's HTTP response handling, critical for proper file delivery and browser compatibility.

🔧 **Technical Specifications**
- File: `gluon/tests/test_contenttype.py` (1.3KB, Complexity: Low)
- Dependencies: gluon.contenttype.contenttype, gluon._compat, unittest
- Test coverage: Standard MIME types (png, gif, tar.bz2) and web2py custom types
- Custom mappings: .load, .json, .jsonp, .pickle, .w2p, .md extensions
- Charset handling: UTF-8 charset specifications for text-based formats
- Extension handling: Tests with and without leading dot prefix

📝 **Detailed Code Analysis**
- **TestContentType class**: Main test class inheriting from unittest.TestCase
- **testTypeRecognition method**: Validates standard and custom MIME type mappings
- **Standard types tested**:
  - `.png` → `image/png`
  - `.gif` → `image/gif`
  - `.tar.bz2` → `application/x-bzip-compressed-tar`
- **Web2py custom mappings**:
  - `.load` → `text/html; charset=utf-8` (AJAX components)
  - `.json` → `application/json` (JSON data)
  - `.jsonp` → `application/jsonp` (JSONP callbacks)
  - `.pickle` → `application/python-pickle` (Python objects)
  - `.w2p` → `application/w2p` (web2py packages)
  - `.md` → `text/x-markdown; charset=utf-8` (Markdown)
- **Edge case testing**: Extensions without dot prefix return default text/plain

🚀 **Usage Methods**
- Run content type tests:
```python
import unittest
from gluon.tests.test_contenttype import TestContentType
suite = unittest.TestLoader().loadTestsFromTestCase(TestContentType)
unittest.TextTestRunner(verbosity=2).run(suite)
```
- Manual content type testing:
```python
from gluon.contenttype import contenttype
# Test standard types
print(contenttype('.jpg'))  # image/jpeg
print(contenttype('.pdf'))  # application/pdf
# Test web2py custom types
print(contenttype('.load'))  # text/html; charset=utf-8
```
- Custom mapping validation:
```python
# Verify custom extensions work correctly
for ext in ['.json', '.md', '.w2p']:
    mime_type = contenttype(ext)
    print(f"{ext} -> {mime_type}")
```

📊 **Output Examples**
- Standard MIME type detection:
```python
>>> contenttype('.png')
'image/png'
>>> contenttype('.gif')
'image/gif'
>>> contenttype('.tar.bz2')
'application/x-bzip-compressed-tar'
```
- Web2py custom types:
```python
>>> contenttype('.load')
'text/html; charset=utf-8'
>>> contenttype('.json')
'application/json'
>>> contenttype('.md')
'text/x-markdown; charset=utf-8'
```
- Fallback behavior:
```python
>>> contenttype('png')  # No leading dot
'text/plain; charset=utf-8'
>>> contenttype('.unknown')
'application/octet-stream'  # Binary fallback
```
- Test execution results:
```
testTypeRecognition (gluon.tests.test_contenttype.TestContentType) ... ok
----------------------------------------------------------------------
Ran 1 test in 0.001s
OK
```

⚠️ **Important Notes**
- Extension format: Leading dot is required for proper MIME type detection
- Charset specifications: Text-based formats include UTF-8 charset by default
- Fallback behavior: Unknown extensions return appropriate fallback MIME types
- Case sensitivity: File extensions are typically case-insensitive
- HTTP compliance: Generated MIME types follow HTTP/1.1 specification
- Browser compatibility: Custom types may not be recognized by all browsers
- Performance: MIME type detection should be fast for file serving operations

🔗 **Related File Links**
- `gluon/contenttype.py` - Core content type detection implementation
- `gluon/http.py` - HTTP response handling that uses content types
- `gluon/tools.py` - File serving utilities that depend on MIME types
- Static file serving configuration in web2py applications
- Browser compatibility documentation for custom MIME types
- HTTP specification documents for MIME type standards

📈 **Use Cases**
- Static file serving validation in web applications
- API response content type verification
- File upload processing and validation
- Browser compatibility testing for custom file types
- Content delivery network (CDN) configuration validation
- Security testing for file type restrictions
- Performance optimization for file serving
- Cross-browser compatibility testing

🛠️ **Improvement Suggestions**
- Coverage: Add tests for more file extensions (video, audio, fonts)
- Security: Test MIME type validation for security-sensitive extensions
- Performance: Add benchmarks for MIME type detection speed
- Configuration: Test custom MIME type mapping configuration
- Internationalization: Test Unicode filenames and extensions
- Validation: Add tests for malformed or suspicious extensions
- Caching: Test MIME type detection caching for performance
- Documentation: Add examples for common web development scenarios

🏷️ **Document Tags**
- Keywords: mime-type, content-type, file-extension, http-headers, media-type, web2py, file-serving
- Technical tags: #mime-type #content-type #http #file-serving #web2py
- Target roles: Web developers (basic), Backend developers (intermediate), DevOps engineers (basic)
- Difficulty level: ⭐⭐ - Requires understanding of HTTP headers and MIME types
- Maintenance level: Low - Stable system, updates mainly for new file type support
- Business criticality: Medium - Important for proper file serving, but fallbacks exist
- Related topics: HTTP protocol, file serving, web standards, browser compatibility, content delivery