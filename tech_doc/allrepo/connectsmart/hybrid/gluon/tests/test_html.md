# test_html.py

## Overview
Comprehensive unit test suite for the Gluon HTML helper module, testing all HTML generation helpers, XML handling, and web2py-specific features like MARKMIN and BEAUTIFY.

## Imports
```python
import re
import unittest
from gluon._compat import PY2, to_native, xrange
from gluon.decoder import decoder
from gluon.html import (ASSIGNJS, BEAUTIFY, BODY, BR, BUTTON, CAT, CENTER,
                        CODE, COL, COLGROUP, DIV, EM, EMBED, FIELDSET, FORM,
                        H1, H2, H3, H4, H5, H6, HEAD, HR, HTML, IFRAME, IMG,
                        INPUT, LABEL, LEGEND, LI, LINK, MARKMIN, MENU, META,
                        OBJECT, OL, OPTGROUP, OPTION, PRE, SCRIPT, SELECT,
                        SPAN, STRONG, STYLE, TABLE, TAG, TBODY, TD, TEXTAREA,
                        TFOOT, TH, THEAD, TITLE, TR, TT, UL, URL, XHTML, XML,
                        A, B, I, P, TAG_pickler, TAG_unpickler, XML_pickle,
                        XML_unpickle, truncate_string, verifyURL,
                        web2pyHTMLParser)
from gluon.storage import Storage
```

## Test Classes

### TestBareHelpers
Tests basic helper functions like URL generation, string truncation, and XML handling.

#### String Manipulation Tests

##### test_truncate_string()
Tests string truncation with ellipsis:
- ASCII text truncation at 30 characters
- Text shorter than limit (no truncation)
- French text with accented characters

##### test_decoder()
Tests HTML decoding functionality with nested tags and attributes.

#### URL Generation Tests

##### test_StaticURL()
Tests static file URL versioning:
- Basic URL generation
- Static version with `response.static_version`
- Versioned URLs with `response.static_version_urls`

##### test_URL()
Comprehensive URL generation testing:
- Basic path construction with args
- List and tuple arguments
- Extension handling (.json)
- Function objects as endpoints
- HMAC signature generation
- User signature support
- Hash variables functionality
- CRLF injection prevention
- URL encoding for international characters

##### test_URL_encode()
Python 2-specific test for URL encoding without percent-encoding.

##### test_verifyURL()
Tests URL signature verification:
- Missing signature detection
- Various hash_vars configurations
- User signature validation
- Session-based HMAC keys

#### XML Handling Tests

##### test_XML()
Tests XML object creation and sanitization:
- HTML sanitization (removes data attributes)
- Unicode handling
- Length calculation
- Tag comparison
- Self-closing tag handling
- Flatten functionality with custom renderers

##### test_XML_pickle_unpickle()
Tests XML serialization and deserialization.

### HTML Helper Tests

#### Container Elements

##### test_DIV()
Tests DIV element functionality:
- Empty DIV creation
- Attribute handling (dict-like updates)
- Component length calculation
- Boolean evaluation (always True)
- Parent/sibling navigation
- Unicode content handling
- Element finding with `.element()`
- Attribute retrieval with `.get()`

##### test_CAT()
Tests concatenation helper for combining elements without wrapper.

##### test_TAG()
Tests generic tag creation:
- Custom tag names
- Self-closing tags (ending with underscore)
- Unicode content support

#### Document Structure

##### test_HTML()
Tests HTML document generation with various doctypes:
- Default (transitional)
- Strict, frameset, html5
- Custom doctype strings
- Empty doctype (no declaration)

##### test_XHTML()
Tests XHTML document generation:
- Proper namespace declarations
- XML language attributes
- Various XHTML doctypes

#### Head Elements

##### test_HEAD(), test_TITLE(), test_META(), test_LINK()
Tests document head elements with proper self-closing tags where appropriate.

##### test_SCRIPT()
Tests JavaScript inclusion:
- CDATA wrapping for inline scripts
- Empty script handling
- Script concatenation

##### test_STYLE()
Tests CSS inclusion with CDATA sections for XHTML compatibility.

#### Text Elements

##### test_H1() through test_H6()
Tests all heading levels with proper escaping.

##### test_P()
Tests paragraph element with CR to BR conversion option.

##### test_SPAN(), test_STRONG(), test_B(), test_EM(), test_I(), test_TT()
Tests inline text formatting elements.

##### test_PRE(), test_CODE()
Tests preformatted text and syntax-highlighted code blocks.

#### Interactive Elements

##### test_A()
Tests anchor tags with Web2py AJAX features:
- Basic links
- AJAX callbacks with `cid` and `callback`
- Delete confirmations
- Component loading
- Disable-with functionality
- Target specifications

##### test_BUTTON()
Tests button element with type attribute.

##### test_INPUT()
Tests input fields:
- Default type="text"
- List value handling

##### test_TEXTAREA()
Tests textarea with customizable rows/cols.

#### List Elements

##### test_UL(), test_OL(), test_LI()
Tests list creation with automatic LI wrapping.

#### Table Elements

##### test_TABLE(), test_TR(), test_TD(), test_TH()
Tests table structure with automatic wrapping:
- TABLE wraps content in TR/TD
- TR wraps content in TD
- Proper nesting behavior

##### test_THEAD(), test_TBODY(), test_TFOOT()
Tests table sections with automatic row wrapping.

##### test_COL(), test_COLGROUP()
Tests column definitions:
- COL as self-closing tag
- COLGROUP as container
- Error handling for invalid COL content

#### Form Elements

##### test_FORM()
Tests form creation:
- Default multipart encoding
- Default POST method
- Action attribute defaulting to "#"

##### test_SELECT(), test_OPTION(), test_OPTGROUP()
Tests dropdown functionality:
- Option creation from various data types
- Multiple selection support
- Option groups
- List/tuple value handling

##### test_FIELDSET(), test_LEGEND()
Tests form grouping elements.

#### Media Elements

##### test_IMG(), test_EMBED()
Tests self-closing media tags.

##### test_IFRAME(), test_OBJECT()
Tests embedded content containers.

### Web2py-Specific Features

#### test_BEAUTIFY()
Tests pretty-printing of Python objects as HTML tables:
- List and dictionary rendering
- Unicode content support

#### test_MENU()
Tests menu generation:
- Desktop mode (UL/LI structure)
- Mobile mode (SELECT element)
- CSS class application
- Active item handling

#### test_MARKMIN()
Tests Markmin wiki syntax rendering:
- Basic text to paragraph conversion
- Code block syntax highlighting
- Escaping of HTML entities

#### test_ASSIGNJS()
Tests JavaScript variable assignment generation:
- String values (quoted)
- Numeric values (unquoted)
- Multiple assignments

#### test_web2pyHTMLParser()
Tests HTML parsing and manipulation:
- Tree structure creation
- Element finding and modification
- Self-closing tag handling
- HTML entity decoding (decimal and hexadecimal)

### TestData Class

#### test_Adata()
Tests data attribute handling with proper escaping of special characters.

## Key Testing Patterns

### Escaping Verification
All tests verify proper HTML escaping of special characters (`<>` becomes `&lt;&gt;`).

### Attribute Handling
Tests verify underscore-prefixed attributes become HTML attributes (`_class` → `class`).

### Unicode Support
Multiple tests ensure proper UTF-8 encoding of international characters.

### Web2py Integration
Tests cover Web2py-specific features like:
- AJAX helpers (callback, cid, delete)
- Component loading
- User signatures
- Static versioning

### Serialization
Tests cover various serialization formats:
- XML output (`.xml()`)
- YAML output (`.as_yaml()`) - commented due to dependency
- Custom flattening (`.flatten()`)

## Notes
- Tests include Python 2/3 compatibility checks
- Comprehensive coverage of all HTML helpers
- Special attention to security (XSS prevention, CRLF injection)
- Tests for both common use cases and edge cases