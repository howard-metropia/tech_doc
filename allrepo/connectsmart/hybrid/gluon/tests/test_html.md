# test_html.py

## Overview
This file contains comprehensive unit tests for the web2py HTML generation system. It tests HTML helper functions, tag creation, URL generation, string manipulation utilities, and various HTML components that form the foundation of web2py's template and view system.

## Purpose
- Tests HTML helper functions and tag generation
- Validates URL generation and routing functionality
- Tests string manipulation utilities like truncation
- Verifies static file versioning and URL handling
- Tests various HTML components and their attributes
- Validates XML/HTML parsing and serialization

## Key Classes and Methods

### TestBareHelpers Class
Tests basic HTML helper utilities and functions.

#### Test Methods

##### `test_truncate_string(self)`
Tests string truncation functionality for different text types.

**ASCII Text Testing:**
```python
truncate_string(
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
    "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    length=30
)
# Returns: "Lorem ipsum dolor sit amet,..."
```

**Short Text Handling:**
- Tests that short text remains unchanged when below length limit
- Validates that text shorter than limit is returned as-is

**Unicode Text Testing:**
```python
truncate_string(
    "Un texte en français avec des accents et des caractères bizarre.",
    length=30
)
# Returns: "Un texte en français avec d..."
```

**Features Tested:**
- **Length Limiting**: Respects specified character length
- **Ellipsis Addition**: Adds "..." when text is truncated
- **Unicode Support**: Properly handles international characters
- **Word Boundaries**: Intelligent truncation at appropriate points

##### `test_StaticURL(self)`
Tests static file URL generation with versioning support.

**Basic URL Generation:**
```python
URL("a", "c", "f")                    # Returns: "/a/c/f"
URL("a", "static", "design.css")      # Returns: "/a/static/design.css"
```

**Version URL Testing:**
```python
response.static_version = "1.2.3"
response.static_version_urls = True
URL("a", "static", "design.css")      # Returns: "/a/static/_1.2.3/design.css"
```

**Features Tested:**
- **Basic Static URLs**: Standard static file URL generation
- **Version Integration**: Static file versioning for cache busting
- **Configuration Control**: Enable/disable versioned URLs
- **Path Insertion**: Proper version path insertion

##### `test_URL(self)`
Comprehensive testing of URL generation functionality.

**Argument Handling:**
```python
URL("a", "c", "f", args="1")          # Returns: "/a/c/f/1"
URL("a", "c", "f", args=("1", "2"))   # Returns: "/a/c/f/1/2"
URL("a", "c", "f", args=["1", "2"])   # Returns: "/a/c/f/1/2"
```

**Path Processing:**
```python
URL("a", "c", "/f")                   # Returns: "/a/c/f" (leading slash removed)
URL("a", "c", "f.json")               # Returns: "/a/c/f.json" (extension preserved)
```

**Context-Dependent URLs:**
- **Current Request**: Uses current request context when parameters omitted
- **Default Values**: Fills in missing application/controller/function from context
- **Extension Support**: Handles file extensions in URLs

**Error Handling:**
- **Invalid Context**: Raises SyntaxError when request context missing
- **Parameter Validation**: Validates URL parameter combinations

## Dependencies
- `unittest` - Python testing framework
- `re` - Regular expression operations
- `gluon._compat` - Cross-version compatibility utilities
- `gluon.decoder` - Content decoding utilities
- `gluon.html` - HTML generation components
- `gluon.storage` - Storage utilities

## HTML Components Tested
The file imports and tests numerous HTML components:

### Basic HTML Tags
- **Structure**: HTML, HEAD, BODY, DIV, SPAN
- **Text Formatting**: H1-H6, P, B, I, EM, STRONG, TT
- **Lists**: UL, OL, LI
- **Tables**: TABLE, THEAD, TBODY, TFOOT, TR, TD, TH

### Form Elements
- **Forms**: FORM, FIELDSET, LEGEND
- **Inputs**: INPUT, TEXTAREA, SELECT, OPTION, OPTGROUP
- **Controls**: BUTTON, LABEL

### Media and Objects
- **Images**: IMG
- **Links**: A, LINK
- **Scripts**: SCRIPT, STYLE
- **Embedded**: IFRAME, EMBED, OBJECT

### Specialized Components
- **Layout**: CENTER, HR, BR
- **Code**: CODE, PRE
- **Meta**: META, TITLE
- **Custom**: CAT, XML, TAG

## URL Generation Features

### Basic URL Construction
- **Application/Controller/Function**: Standard web2py URL pattern
- **Arguments**: Single arguments, tuples, and lists
- **Extensions**: File extension support (.json, .xml, etc.)
- **Path Normalization**: Handles leading slashes and path cleanup

### Static File Handling
- **Static Directory**: Special handling for static file URLs
- **Version Control**: Cache-busting version insertion
- **Configuration**: Runtime configuration of versioning behavior
- **Path Manipulation**: Intelligent path modification for versions

### Context Integration
- **Request Context**: Uses current request for default values
- **Global Context**: Integrates with web2py's global context system
- **Error Handling**: Proper error reporting for invalid contexts
- **Default Behavior**: Sensible defaults for missing parameters

## String Utilities

### Text Truncation
- **Length Control**: Precise character length limiting
- **Unicode Support**: Proper handling of international characters
- **Ellipsis Addition**: Visual indication of truncated content
- **Smart Truncation**: Attempts to break at word boundaries
- **Preserve Short Text**: No modification of text below limit

### Character Encoding
- **Unicode Handling**: Proper Unicode string processing
- **Cross-platform**: Consistent behavior across operating systems
- **Character Counting**: Accurate character counting for truncation
- **Encoding Preservation**: Maintains original text encoding

## Usage Example
```python
from gluon.html import DIV, A, IMG, URL, truncate_string
from gluon.storage import Storage

# HTML generation
content = DIV(
    H1("Welcome"),
    P("This is a paragraph with ", A("a link", _href=URL('default', 'index'))),
    IMG(_src=URL('static', 'images/logo.png'), _alt="Logo")
)

# URL generation
home_url = URL('default', 'index')
static_css = URL('static', 'css/main.css')
api_url = URL('api', 'users', args=[123], extension='json')

# String truncation
short_desc = truncate_string(long_description, length=150)

# Static versioning
response.static_version = "2.1.0"
response.static_version_urls = True
versioned_css = URL('static', 'css/app.css')  # /app/static/_2.1.0/css/app.css
```

## Integration with web2py Framework

### Template System
- **Helper Functions**: Provides HTML helpers for templates
- **Tag Generation**: Automatic HTML tag generation with proper attributes
- **Content Safety**: Automatic escaping and safety handling
- **Nested Structures**: Support for complex nested HTML structures

### URL Routing
- **Request Integration**: Uses current request context for URL generation
- **Route Resolution**: Integrates with web2py's routing system
- **Parameter Handling**: Manages URL parameters and arguments
- **Extension Support**: Handles different response formats

### Static Asset Management
- **Cache Busting**: Version-based cache invalidation
- **Asset Organization**: Structured static file organization
- **Performance**: Optimized static file serving
- **Development**: Easy asset management during development

### Form Processing
- **Form Generation**: Automatic form HTML generation
- **Input Handling**: Various input type support
- **Validation Integration**: Integrates with form validation
- **CSRF Protection**: Security features for form processing

## Test Coverage
- **URL Generation**: Complete URL construction testing
- **HTML Components**: Basic HTML tag functionality
- **String Utilities**: Text manipulation and formatting
- **Static Assets**: Versioned static file handling
- **Context Integration**: web2py context system integration
- **Error Handling**: Proper error detection and reporting

## Expected Results
- **Valid HTML**: Generated HTML should be well-formed and valid
- **Correct URLs**: URLs should follow web2py conventions
- **Proper Escaping**: Content should be properly escaped for security
- **Performance**: Efficient HTML generation and URL construction
- **Compatibility**: Cross-browser and cross-platform compatibility

## File Structure
```
gluon/tests/
├── test_html.py          # This file
└── ... (other test files)
```

This test suite ensures web2py's HTML generation system provides reliable, secure, and efficient HTML creation capabilities with proper URL handling and content management.