# Gluon Highlight Module Technical Documentation

## Module: `highlight.py`

### Overview
The `highlight` module provides syntax highlighting functionality for the Gluon web framework. It supports multiple programming languages including Python, C/C++, and HTML, with special support for web2py-specific syntax. The module generates HTML output with inline CSS styling for code display.

### Table of Contents
1. [Dependencies](#dependencies)
2. [Core Classes](#core-classes)
3. [Language Support](#language-support)
4. [Highlighting Functions](#highlighting-functions)
5. [Style Customization](#style-customization)
6. [Usage Examples](#usage-examples)
7. [Advanced Features](#advanced-features)

### Dependencies
```python
import re
from pydal._compat import xrange
from yatl.sanitizer import xmlescape
```

### Core Classes

#### `all_styles`
A custom non-data descriptor for lazy initialization of syntax highlighting styles.

```python
class all_styles(object):
    """
    Custom non-data descriptor for lazy initialization of
    Highlighter.all_styles class attribute.
    """
    def __get__(self, instance, owner):
        val = _get_all_styles(owner)
        setattr(owner, "all_styles", val)
        return val
```

#### `Highlighter`
Main class that performs syntax highlighting for various languages.

**Constructor:**
```python
def __init__(self, mode, link=None, styles=None):
    """
    Initialize highlighter:
        mode = language (PYTHON, WEB2PY, C, CPP, HTML, HTML_PLAIN)
        link = base URL for linking web2py keywords
        styles = custom style dictionary
    """
```

**Parameters:**
- `mode` (str): Language mode (case-insensitive)
- `link` (str): Base URL for creating links (optional)
- `styles` (dict): Custom style overrides (optional)

**Supported Modes:**
- `PYTHON`: Standard Python syntax
- `WEB2PY`: Python with web2py framework keywords
- `C`: C language syntax
- `CPP`: C++ language (uses C mode with C++ keywords)
- `HTML`: HTML with embedded Python support
- `HTML_PLAIN`: HTML without embedded Python

### Language Support

#### Python Language Patterns
```python
# Python tokens and their styles
GOTOHTML: "{{" -> "color: red"
PUNC: "[-+*!|&^~/%\=<>\[\]{}(),.:]]" -> "font-weight: bold"
NUMBER: "0x[0-9a-fA-F]+|[+-]?\d+(\.\d+)?([eE][+-]\d+)?|\d+" -> "color: red"
KEYWORD: Python keywords -> "color:#185369; font-weight: bold"
WEB2PY: web2py specific keywords -> "link:%(link)s;text-decoration:None;color:#FF5C1F;"
MAGIC: "self|None" -> "color:#185369; font-weight: bold"
MULTILINESTRING: "'''|\"\"\"" -> "color: #FF9966"
STRING: Single/double quoted strings -> "color: #FF9966"
COMMENT: "# comments" -> "color: green; font-style: italic"
```

#### C/C++ Language Patterns
```python
# C/C++ tokens and their styles
COMMENT: "//..." -> "color: green; font-style: italic"
MULTILINECOMMENT: "/* ... */" -> "color: green; font-style: italic"
PREPROCESSOR: "#include etc." -> "color: magenta; font-style: italic"
PUNC: Operators and punctuation -> "font-weight: bold"
NUMBER: Numeric literals -> "color: red"
KEYWORD: C keywords -> "color:#185369; font-weight: bold"
CPPKEYWORD: C++ specific keywords -> "color: blue; font-weight: bold"
STRING: String literals -> "color: #FF9966"
```

#### HTML Language Patterns
```python
# HTML tokens and their styles
GOTOPYTHON: "{{" -> "color: red"
COMMENT: "<!-- ... -->" -> "color: green; font-style: italic"
XMLCRAP: "<!...>" -> "color: blue; font-style: italic"
SCRIPT: "<script>...</script>" -> "color: black"
TAG: HTML tags -> "color: darkred; font-weight: bold"
ENDTAG: "/>" -> "color: darkred; font-weight: bold"
```

### Highlighting Functions

#### `highlight(code, language, link="/examples/globals/vars/", counter=1, styles=None, highlight_line=None, context_lines=None, attributes=None)`
Main highlighting function that generates HTML with syntax highlighting.

**Parameters:**
- `code` (str): Source code to highlight
- `language` (str): Language mode
- `link` (str): Base URL for links (default: "/examples/globals/vars/")
- `counter` (int/str/None): Line numbering options
- `styles` (dict): Custom styles
- `highlight_line` (int): Line number to highlight
- `context_lines` (int): Number of context lines around highlighted line
- `attributes` (dict): HTML attributes for the table element

**Returns:**
- `str`: HTML table with highlighted code

**Example:**
```python
# Basic Python highlighting
html_output = highlight(
    "def hello():\n    print('Hello, World!')",
    "PYTHON"
)

# With line numbers and custom styles
html_output = highlight(
    code,
    "PYTHON",
    counter=1,
    styles={'CODE': 'font-size: 14px;'},
    highlight_line=5
)
```

### Style Customization

#### Default Styles
```python
# Code block style
code_style = """
font-size: 11px;
font-family: Bitstream Vera Sans Mono,monospace;
background-color: transparent;
margin: 0;
padding: 5px;
border: none;
overflow: auto;
white-space: pre !important;
"""

# Line numbers style
linenumbers_style = """
font-size: 11px;
font-family: Bitstream Vera Sans Mono,monospace;
background-color: transparent;
margin: 0;
padding: 5px;
border: none;
color: #A0A0A0;
"""

# Line highlight style
linehighlight_style = "background-color: #EBDDE2;"
```

#### Custom Style Dictionary
```python
custom_styles = {
    'CODE': 'custom code style CSS',
    'LINENUMBERS': 'custom line number style CSS',
    'LINEHIGHLIGHT': 'custom highlight style CSS',
    'KEYWORD': 'color: blue;',
    'STRING': 'color: green;',
    'COMMENT': 'color: gray; font-style: italic;'
}
```

### Usage Examples

#### Basic Syntax Highlighting
```python
# Python code highlighting
python_code = '''
def factorial(n):
    """Calculate factorial recursively"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)
'''

html = highlight(python_code, "PYTHON")
```

#### Web2py Code with Links
```python
# Web2py code with framework keywords linked
web2py_code = '''
def index():
    form = SQLFORM(db.person)
    if form.process().accepted:
        redirect(URL('list'))
    return dict(form=form)
'''

html = highlight(
    web2py_code, 
    "WEB2PY",
    link="/admin/default/docs/"
)
```

#### C++ Code Highlighting
```python
# C++ code highlighting
cpp_code = '''
#include <iostream>
using namespace std;

class Rectangle {
private:
    int width, height;
public:
    Rectangle(int w, int h) : width(w), height(h) {}
    int area() { return width * height; }
};
'''

html = highlight(cpp_code, "CPP")
```

#### HTML with Embedded Python
```python
# HTML template with Python code
template = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{=title}}</title>
</head>
<body>
    {{for item in items:}}
        <li>{{=item}}</li>
    {{pass}}
</body>
</html>
'''

html = highlight(template, "HTML")
```

### Advanced Features

#### Line Highlighting with Context
```python
# Highlight specific line with context
code = open('script.py').read()
html = highlight(
    code,
    "PYTHON",
    highlight_line=42,      # Highlight line 42
    context_lines=3,        # Show 3 lines before/after
    counter=35              # Start line numbers at 35
)
```

#### Custom Line Numbering
```python
# No line numbers
html = highlight(code, "PYTHON", counter=None)

# Fixed prefix for all lines
html = highlight(code, "PYTHON", counter=">>>")

# Start from specific number
html = highlight(code, "PYTHON", counter=100)
```

#### HTML Attributes
```python
# Add custom HTML attributes
html = highlight(
    code,
    "PYTHON",
    attributes={
        '_id': 'code-block',
        '_class': 'syntax-highlight',
        '_data-language': 'python'
    }
)
# Generates: <table id="code-block" class="syntax-highlight" data-language="python">
```

### Tokenizer Methods

#### `python_tokenizer(token, match, style)`
Handles Python-specific token processing including:
- Multiline string detection
- Link generation for web2py keywords
- Special token transformations

#### `c_tokenizer(token, match, style)`
Processes C/C++ tokens with XML escaping.

#### `html_tokenizer(token, match, style)`
Handles HTML tokens and transitions to Python mode for embedded code.

### Integration Examples

#### Web Application Integration
```python
from gluon.highlight import highlight

def show_source():
    """Controller to display source code"""
    filename = request.args(0)
    if not filename:
        raise HTTP(404)
    
    # Read source file
    filepath = os.path.join(request.folder, 'controllers', filename)
    if not os.path.exists(filepath):
        raise HTTP(404)
    
    code = open(filepath).read()
    
    # Determine language from extension
    if filename.endswith('.py'):
        language = 'WEB2PY'
    elif filename.endswith('.html'):
        language = 'HTML'
    else:
        language = None
    
    # Generate highlighted HTML
    highlighted = highlight(
        code,
        language,
        link=URL('admin', 'default', 'docs'),
        counter=1
    )
    
    return dict(filename=filename, code=XML(highlighted))
```

#### Code Review Tool
```python
def review_changes(old_code, new_code, changed_lines):
    """Highlight code changes for review"""
    
    # Custom styles for changes
    review_styles = {
        'LINEHIGHLIGHT': 'background-color: #ffcccc;'
    }
    
    html_parts = []
    
    for line_num in changed_lines:
        # Show old version
        old_html = highlight(
            old_code,
            'PYTHON',
            highlight_line=line_num,
            context_lines=2,
            styles=review_styles
        )
        
        # Show new version
        new_html = highlight(
            new_code,
            'PYTHON',
            highlight_line=line_num,
            context_lines=2,
            styles={'LINEHIGHLIGHT': 'background-color: #ccffcc;'}
        )
        
        html_parts.append((old_html, new_html))
    
    return html_parts
```

### Command Line Usage
```python
if __name__ == "__main__":
    import sys
    
    # Read file and highlight
    with open(sys.argv[1]) as f:
        data = f.read()
    
    # Output highlighted HTML
    print("<html><body>")
    print(highlight(data, sys.argv[2]))
    print("</body></html>")
```

Usage:
```bash
python highlight.py script.py PYTHON > highlighted.html
```

### Performance Considerations

1. **Regex Compilation**: Patterns are compiled once and reused
2. **Lazy Style Loading**: Styles loaded only when needed
3. **Efficient Tokenization**: Single pass through source code
4. **Memory Usage**: Processes code incrementally

### Security Notes

1. **XSS Protection**: All code is XML-escaped
2. **Safe HTML Generation**: No raw user input in HTML
3. **Link Validation**: Ensure link parameter is trusted
4. **Style Injection**: Validate custom styles

### Module Metadata

- **License**: LGPLv3
- **Part of**: web2py Web Framework
- **Dependencies**: regex, YATL sanitizer
- **Thread Safety**: Yes (no shared mutable state)
- **Python**: 2.7+, 3.x compatible