# test_template.py

## Overview
This file contains comprehensive unit tests for the YATL (Yet Another Template Language) template system. It tests template rendering, syntax parsing, control flow, variable output, template inheritance, and file system integration for web2py's template engine.

## Purpose
- Tests YATL template rendering functionality
- Validates template syntax and control flow structures
- Tests variable output and escaping mechanisms
- Verifies template inheritance and block systems
- Tests file system integration and template loading
- Ensures proper error handling and security features

## Key Classes and Methods

### TestTemplate Class
Comprehensive test suite for YATL template functionality.

#### Test Methods

##### `testRun(self)`
Tests basic template rendering and control flow structures.

**Loop Testing:**
```python
render(content='{{for i in range(n):}}{{=i}}{{pass}}', context=dict(n=3))
# Returns: '012'
```

**Conditional Testing:**
```python
render(content='{{if n>2:}}ok{{pass}}', context=dict(n=3))
# Returns: 'ok'
```

**Exception Handling:**
```python
render(content='{{try:}}{{n/0}}{{except:}}fail{{pass}}', context=dict(n=3))
# Returns: 'fail'
```

**XML Escaping:**
```python
render(content='{{="<&>"}}')
# Returns: '&lt;&amp;&gt;'
```

**String Handling:**
```python
# Various quote types and escaping
render(content='"abc"')           # Returns: '"abc"'
render(content='"a\'bc"')         # Returns: '"a\'bc"'
render(content='"a\"bc"')         # Returns: '"a\"bc"'
render(content=r'"a\"bc"')        # Returns: r'"a\"bc"'
render(content=r'"""abc\""""')    # Returns: r'"""abc\""""'
```

##### `testEqualWrite(self)`
Tests variable output generation and `response.write` functionality.

**Basic Output Testing:**
```python
render(content='{{=2+2}}')        # Returns: '4'
render(content='{{="abc"}}')      # Returns: 'abc'
```

**Whitespace Handling:**
```python
# Whitespace is stripped from output directives
render(content='{{ ="abc"}}')     # Returns: 'abc'
render(content='{{ ="abc" }}')    # Returns: 'abc'
render(content='{{pass\n="abc" }}') # Returns: 'abc'
```

**Line Recognition:**
```python
# = recognized only at beginning of physical line
render(content='{{xyz = "xyz"\n="abc"\n="def"\n=xyz }}')
# Returns: 'abcdefxyz'
```

**Control Flow Integration:**
```python
# = within conditional blocks
render(content='{{if True:\n="abc"\npass }}')
# Returns: 'abc'

render(content='{{if True:\n="abc"\npass\n="def" }}')
# Returns: 'abcdef'

render(content='{{if False:\n="abc"\npass\n="def" }}')
# Returns: 'def'

# if-else structures
render(content='{{if True:\n="abc"\nelse:\n="def"\npass }}')
# Returns: 'abc'

render(content='{{if False:\n="abc"\nelse:\n="def"\npass }}')
# Returns: 'def'
```

**Newline Handling:**
```python
# Codeblock-leading = handles internal newlines
render(content='{{=list((1,2,3))}}')        # Returns: '[1, 2, 3]'
render(content='{{=list((1,2,\\\n3))}}')    # Returns: '[1, 2, 3]'
render(content='{{=list((1,2,\n3))}}')      # Returns: '[1, 2, 3]'
```

**Syntax Error Testing:**
```python
# Multiple = operators in same codeblock cause SyntaxError
self.assertRaises(SyntaxError, render, content='{{="abc"\n="def" }}')

# Embedded = won't handle newlines
render(content='{{pass\n=list((1,2,\\\n3))}}')  # Works: '[1, 2, 3]'
self.assertRaises(SyntaxError, render, content='{{pass\n=list((1,2,\n3))}}')
```

##### `testWithDummyFileSystem(self)`
Tests template inheritance and file system integration using mock file system.

**Monkey Patching Helper:**
```python
@contextlib.contextmanager
def monkey_patch(module, fn_name, patch):
    # Temporarily replaces module functions for testing
```

**Mock File System:**
```python
def dummy_open(path):
    if path == pjoin('views', 'layout.html'):
        return ("{{block left_sidebar}}left{{end}}"
                "{{include}}" 
                "{{block right_sidebar}}right{{end}}")
    elif path == pjoin('views', 'default', 'index.html'):
        return ("{{extend 'layout.html'}}"
                "{{block left_sidebar}}{{super}} {{end}}"
                "to"
                "{{block right_sidebar}} {{super}}{{end}}")
```

**Template Inheritance Testing:**
```python
# Standard delimiter inheritance
render(filename=pjoin('views', 'default', 'index.html'),
       path='views', reader=dummy_open)
# Returns: 'left to right'

# Custom delimiter inheritance
render(filename=pjoin('views', 'default', 'indexbrackets.html'),
       path='views', delimiters='[[ ]]', reader=dummy_open)
# Returns: 'left to right'
```

**Response Object Integration:**
```python
response = DummyResponse()
response.delimiters = ('[[', ']]')
render(filename=pjoin('views', 'default', 'indexbrackets.html'),
       path='views', context={'response': response}, reader=dummy_open)
# Returns: 'left to right'
```

**NOESCAPE Testing:**
```python
render(filename=pjoin('views', 'default', 'noescape.html'),
       context={'NOESCAPE': NOESCAPE}, reader=dummy_open)
# Returns: '<script></script>' (unescaped)
```

## Dependencies
- `unittest` - Python testing framework
- `sys` - System information (Python version detection)
- `yatl` - Template rendering engine
- `yatl.template` - Template components (DummyResponse, RestrictedError, NOESCAPE)
- `contextlib` - Context management utilities
- `StringIO`/`io.StringIO` - String buffer for testing

## YATL Template Features Tested

### Template Syntax
- **Code Blocks**: `{{python code}}` syntax
- **Output Directives**: `{{=expression}}` for variable output
- **Control Flow**: `{{if}}`, `{{for}}`, `{{try}}` structures
- **Block Termination**: `{{pass}}` and `{{end}}` terminators

### Variable Output
- **Automatic Escaping**: Default XML/HTML escaping for security
- **Expression Evaluation**: Python expression evaluation
- **Context Variables**: Access to template context variables
- **Whitespace Handling**: Intelligent whitespace management

### Control Flow Structures
- **Conditionals**: if/else/elif statements
- **Loops**: for and while loops
- **Exception Handling**: try/except/finally blocks
- **Block Nesting**: Nested control structures

### Template Inheritance
- **Template Extension**: `{{extend 'parent.html'}}` syntax
- **Block Definition**: `{{block name}}...{{end}}` syntax
- **Block Override**: Child template block overrides
- **Super Calls**: `{{super}}` for parent block content

### File System Integration
- **Template Loading**: Loading templates from file system
- **Path Resolution**: Template path resolution
- **Error Handling**: Missing template error handling
- **Custom Readers**: Pluggable file reading mechanisms

### Security Features
- **Automatic Escaping**: Default escaping prevents XSS
- **NOESCAPE**: Explicit raw output when needed
- **Restricted Execution**: Safe template code execution
- **Error Isolation**: Template error isolation

## Usage Example
```python
from yatl import render
from yatl.template import NOESCAPE

# Basic template rendering
result = render(content='Hello {{=name}}!', context={'name': 'World'})
print(result)  # Hello World!

# Control flow
template = '''
{{if user.is_authenticated:}}
    Welcome back, {{=user.name}}!
{{else:}}
    Please log in.
{{pass}}
'''
result = render(content=template, context={
    'user': {'is_authenticated': True, 'name': 'John'}
})

# Template inheritance
# layout.html:
# <html><body>{{block content}}{{end}}</body></html>

# index.html:
# {{extend 'layout.html'}}
# {{block content}}Hello World!{{end}}

result = render(filename='views/index.html', path='views')

# Raw output (no escaping)
template = '{{=NOESCAPE("<b>Bold text</b>")}}'
result = render(content=template, context={'NOESCAPE': NOESCAPE})
print(result)  # <b>Bold text</b>
```

## Integration with web2py Framework

### View System
- **View Rendering**: Primary view rendering engine for web2py
- **Controller Integration**: Seamless controller-view data passing
- **Helper Integration**: Integration with HTML helpers
- **Response Management**: Integration with Response object

### Template Features
- **Layout Systems**: Master page layouts with block inheritance
- **Component System**: Reusable template components
- **Caching**: Template compilation and caching
- **Development**: Live template reloading during development

### Security Integration
- **XSS Prevention**: Automatic escaping prevents cross-site scripting
- **Code Execution**: Safe template code execution environment
- **Input Validation**: Template input validation and sanitization
- **Error Handling**: Secure error reporting and handling

### Performance Optimization
- **Template Compilation**: Pre-compilation for production performance
- **Caching**: Compiled template caching
- **Memory Management**: Efficient memory usage
- **Streaming**: Large template streaming capabilities

## Test Coverage
- **Basic Rendering**: Template compilation and rendering
- **Syntax Features**: All template syntax elements
- **Control Flow**: Conditional and loop structures
- **Variable Output**: Expression evaluation and escaping
- **Template Inheritance**: Block systems and extension
- **File System**: Template loading and path resolution
- **Error Handling**: Syntax and runtime error handling

## Expected Results
- **Correct Rendering**: Templates should render with expected output
- **Security**: Automatic escaping should prevent XSS attacks
- **Performance**: Fast template rendering for production use
- **Flexibility**: Support for complex template structures
- **Error Handling**: Clear error messages for template issues

## File Structure
```
gluon/packages/yatl/tests/
├── test_template.py      # This file
└── test_helpers.py       # HTML helpers tests

gluon/packages/yatl/
├── template.py          # Template engine implementation
├── helpers.py           # HTML helper implementation
└── ... (other YATL modules)
```

This test suite ensures YATL provides a robust, secure, and efficient template system for web2py applications with comprehensive template inheritance, control flow, and integration capabilities.