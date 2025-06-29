# test_helpers.py

## Overview
This file contains unit tests for the YATL (Yet Another Template Language) HTML helpers. It tests tag generation, XML output, attribute handling, sanitization features, and security validation for HTML content generation.

## Purpose
- Tests YATL HTML tag generation functionality
- Validates XML output formatting and escaping
- Tests HTML attribute handling and validation
- Verifies HTML sanitization and security features
- Tests permitted tags and allowed attributes filtering
- Ensures proper HTML content escaping and safety

## Key Classes and Methods

### TestHelpers Class
Comprehensive test suite for YATL HTML helpers.

#### Test Methods

##### `test_all_tags(self)`
Tests automatic tag generation for all supported HTML tags.

**Tag Generation Testing:**
```python
for x in TAG.__all_tags__:
    # Regular tags: <tag></tag>
    # Self-closing tags: <tag/>
    self.assertEqual(TAG[x]().xml(), "<%s></%s>" % (x, x) 
                    if not x[-1] == "/" else "<%s>" % x)
```

**Features Tested:**
- **All HTML Tags**: Tests every tag in `TAG.__all_tags__`
- **Regular Tags**: Paired opening and closing tags
- **Self-closing Tags**: Tags ending with "/" (e.g., img/, br/)
- **XML Output**: Proper XML formatting for all tags

##### `test_tags(self)`
Tests specific tag functionality and attribute handling.

**Basic Tag Creation:**
```python
DIV = TAG.div
IMG = TAG['img/']

# Basic tag generation
DIV().xml()          # Returns: "<div></div>"
IMG().xml()          # Returns: "<img/>"
```

**Attribute Handling:**
```python
# ID attribute
DIV(_id="my_id").xml()  # Returns: "<div id=\"my_id\"></div>"

# Source attribute
IMG(_src="crazy").xml() # Returns: "<img src=\"crazy\"/>"

# Multiple attributes
DIV(_class="my_class", _mytrueattr=True).xml()
# Returns: "<div class=\"my_class\" mytrueattr=\"mytrueattr\"></div>"
```

**Special Attribute Values:**
- **None Values**: `_none=None` - Attributes with None values are omitted
- **False Values**: `_false=False` - False attributes are omitted
- **True Values**: `_mytrueattr=True` - True values become attribute name
- **Underscore Handling**: `without_underline="serius?"` - Non-underscore attributes

**Content Escaping:**
```python
# Automatic XML escaping
DIV("<b>xmlscapedthis</b>").xml()
# Returns: "<div>&lt;b&gt;xmlscapedthis&lt;/b&gt;</div>"

# No escaping with XML wrapper
DIV(XML("<b>don'txmlscapedthis</b>")).xml()
# Returns: "<div><b>don'txmlscapedthis</b></div>"
```

##### `test_invalid_atribute_name(self)`
Tests validation of invalid HTML attribute names.

**Invalid Characters Testing:**
```python
invalid_chars = [" ", "=", "'", '"', ">", "<", "/"]
for x in invalid_chars:
    attr_name = "_any%sthings" % x
    attr = {attr_name: "invalid_atribute_name"}
    self.assertRaises(ValueError, DIV("any content", **attr).xml)
```

**Security Features:**
- **Character Validation**: Prevents dangerous characters in attribute names
- **HTML Injection Prevention**: Protects against attribute-based XSS
- **Standards Compliance**: Ensures HTML/XML standards compliance
- **Error Handling**: Proper ValueError raising for invalid attributes

##### `test_sanitize(self)`
Comprehensive testing of HTML sanitization functionality.

**Permitted Tags Configuration:**
```python
permitted_tags = [
    'div', 'td', 'b', 'br/', 'strong', 'span', 'img/', 'a'
]

allowed_attributes = {
    'a': ['href', 'title'],
    'img': ['src', 'alt'],
    'blockquote': ['type'],
    'td': ['colspan'],
}
```

**Permitted Tag Testing:**
- **Allowed Tags**: Tags in permitted list are preserved
- **Required Attributes**: Special handling for img/ and a tags
- **Attribute Validation**: Only allowed attributes are preserved
- **Content Preservation**: Tag content is maintained during sanitization

**Special Tag Requirements:**
```python
# IMG tags require alt or src attribute
IMG(_alt="empty").xml()  # Valid
IMG(_src="/image.png").xml()  # Valid

# A tags with href or title
A("this is a link", _href="http://web2py.com/").xml()  # Valid
A("without href", _title="this is a link?").xml()  # Valid
```

**Forbidden Tag Testing:**
```python
out_of_list = [
    'blockquote', 'i', 'li', 'ol', 'ul', 'p', 'cite', 'code', 'pre',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'table', 'tbody', 'thead', 'tfoot', 'tr', 'strong'
]

# Tags not in permitted list are escaped
for x in out_of_list:
    T = TAG[x]
    # Returns: "&lt;tag&gt;&lt;/tag&gt;" (escaped)
```

**Malicious Tag Testing:**
```python
# Unusual/evil tags are escaped
for x in ["evil", "n0c1v3"]:
    T = TAG[x]
    # Returns: "&lt;evil&gt;&lt;/evil&gt;" (escaped)
```

**Attribute Filtering:**
```python
# Only allowed attributes are preserved
s_tag = TAG['td']("content_td", _colspan="2", _extra_attr="invalid").xml()
XML(s_tag, sanitize=True, permitted_tags=['td'], 
    allowed_attributes={'td': ['colspan']}).xml()
# Returns: '<td colspan="2">content_td</td>' (extra_attr removed)
```

## Dependencies
- `unittest` - Python testing framework
- `yatl.helpers` - YATL HTML helpers (TAG, XML)

## YATL Features Tested

### Tag Generation
- **Dynamic Tags**: `TAG[tagname]` and `TAG.tagname` syntax
- **All HTML Tags**: Comprehensive HTML tag support
- **Self-closing Tags**: Proper handling of void elements
- **XML Compliance**: Valid XML output generation

### Attribute Management
- **Underscore Convention**: `_attribute` becomes `attribute`
- **Special Values**: None, False, True value handling
- **Validation**: Invalid attribute name detection
- **Security**: XSS prevention through validation

### Content Handling
- **Automatic Escaping**: Default XML escaping for safety
- **Raw Content**: XML wrapper for unescaped content
- **Mixed Content**: Tags and text content combination
- **Nested Structures**: Complex nested tag structures

### Sanitization System
- **Whitelist Approach**: Only permitted tags allowed
- **Attribute Filtering**: Only allowed attributes preserved
- **Content Preservation**: Safe content is maintained
- **Security**: Malicious content is neutralized

## Usage Example
```python
from yatl.helpers import TAG, XML

# Basic tag creation
DIV = TAG.div
IMG = TAG['img/']
A = TAG.a

# Simple tags
div_tag = DIV("Hello World")
print(div_tag.xml())  # <div>Hello World</div>

# Tags with attributes
img_tag = IMG(_src="/logo.png", _alt="Logo")
print(img_tag.xml())  # <img src="/logo.png" alt="Logo"/>

# Complex nested structure
form = TAG.form(
    DIV(
        TAG.label("Name:", _for="name"),
        TAG.input(_type="text", _name="name", _id="name")
    ),
    DIV(
        TAG.input(_type="submit", _value="Submit")
    ),
    _method="post", _action="/submit"
)

# Raw HTML content
raw_content = XML("<b>Bold text</b>")
div_with_raw = DIV("Regular text ", raw_content)

# Sanitization
untrusted_html = "<script>alert('xss')</script><div>Safe content</div>"
safe_html = XML(untrusted_html, sanitize=True, 
                permitted_tags=['div'], allowed_attributes={})
print(safe_html.xml())  # &lt;script&gt;alert('xss')&lt;/script&gt;<div>Safe content</div>
```

## Integration with web2py Framework

### Template System
- **View Generation**: HTML generation in web2py views
- **Helper Functions**: Template helper functions
- **Form Generation**: Automatic form HTML generation
- **Component System**: Reusable component creation

### Security Features
- **XSS Prevention**: Automatic escaping prevents XSS attacks
- **Input Sanitization**: Safe handling of user-generated content
- **Content Filtering**: Whitelist-based content filtering
- **Attribute Validation**: Secure attribute handling

### Performance Optimization
- **Efficient Generation**: Fast HTML generation
- **Memory Management**: Efficient memory usage
- **Caching**: Generated content caching capabilities
- **Streaming**: Large content streaming support

## Test Coverage
- **Tag Generation**: All HTML tag types and variations
- **Attribute Handling**: Various attribute scenarios
- **Content Escaping**: Automatic and manual escaping
- **Security Features**: XSS prevention and sanitization
- **Error Handling**: Invalid input handling
- **Edge Cases**: Special attribute values and characters

## Expected Results
- **Valid HTML**: Generated HTML should be well-formed
- **Security**: Malicious content should be neutralized
- **Performance**: Fast HTML generation
- **Compliance**: HTML/XML standards compliance
- **Flexibility**: Support for complex HTML structures

## File Structure
```
gluon/packages/yatl/tests/
├── test_helpers.py       # This file
└── test_template.py      # Template system tests

gluon/packages/yatl/
├── helpers.py           # HTML helper implementation
└── ... (other YATL modules)
```

This test suite ensures YATL's HTML helper system provides secure, efficient, and standards-compliant HTML generation capabilities for web2py applications.