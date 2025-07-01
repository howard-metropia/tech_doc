# Gluon Template Engine Documentation

## Overview

The `template.py` module provides a minimalist template engine interface for the Gluon framework. It serves as a bridge to the YATL (Yet Another Template Language) template system, offering template parsing and rendering capabilities for web applications.

## File Location
`/home/datavan/METROPIA/metro_combine/allrepo/connectsmart/hybrid/gluon/template.py`

## Dependencies

### External Dependencies
- **yatl.template**: Core template parsing and rendering engine
  - `parse_template`: Function for parsing template syntax
  - `render`: Function for rendering templates with context data

## Core Functionality

### Template System Integration

The module provides a clean interface to YATL template functionality through imported functions:

```python
from yatl.template import parse_template, render
```

### Key Features

1. **Template Parsing**: Direct access to YATL's template parsing capabilities
2. **Template Rendering**: Clean interface for rendering templates with data
3. **Minimal Overhead**: Lightweight wrapper around YATL functionality
4. **Framework Integration**: Seamless integration with Gluon web framework

## Architecture Pattern

### Delegation Pattern
The module follows a delegation pattern, providing a simplified interface to the underlying YATL template engine while maintaining full compatibility with its feature set.

### Template Engine Interface
```python
# Template parsing capability
parse_template(template_string, context=None, path=None, writer=None, lexers=None, delimiters=None, reader=None)

# Template rendering capability  
render(template, context=None, delimiters=None, filename=None)
```

## Integration Points

### Web2py/Gluon Framework
- Integrates with Gluon's MVC architecture
- Supports template inheritance and includes
- Compatible with Gluon's response and request objects
- Works with Gluon's internationalization system

### YATL Template Features
- Template inheritance with `{{extend}}`
- Template includes with `{{include}}`
- Python code blocks with `{{pass}}`
- Variable interpolation with `{{=variable}}`
- Control structures (if, for, while)
- Custom delimiters support

## Usage Patterns

### Basic Template Rendering
```python
from gluon.template import render, parse_template

# Parse template from string
template = parse_template(template_string)

# Render with context data
output = render(template, context={'name': 'John', 'items': [1, 2, 3]})
```

### Template File Processing
```python
# Template files typically use .html extension
# Content example:
# <h1>Hello {{=name}}</h1>
# {{for item in items:}}
#   <p>Item: {{=item}}</p>
# {{pass}}
```

## Template Syntax Support

### Variable Output
```html
{{=variable}}          <!-- Escaped output -->
{{=XML(variable)}}     <!-- Unescaped output -->
```

### Control Structures
```html
{{if condition:}}
  Content when true
{{else:}}
  Content when false
{{pass}}

{{for item in items:}}
  <p>{{=item}}</p>
{{pass}}
```

### Template Inheritance
```html
{{extend 'layout.html'}}
{{block content}}
  Page-specific content
{{end}}
```

## Performance Considerations

### Template Caching
- Templates are automatically cached after first parse
- Compiled templates provide fast rendering
- Memory-efficient template reuse

### Optimization Features
- Pre-compiled template support
- Efficient variable interpolation
- Minimal parsing overhead for cached templates

## Error Handling

### Template Syntax Errors
- Clear error messages for syntax issues
- Line number reporting for debugging
- Graceful handling of missing variables

### Runtime Error Management
- Safe variable access patterns
- Exception handling in template code
- Debugging information preservation

## Security Features

### XSS Protection
- Automatic HTML escaping by default
- XML() function for trusted content
- Safe template variable handling

### Code Injection Prevention
- Controlled Python code execution
- Template sandbox environment
- Restricted function access

## Best Practices

### Template Organization
1. Use template inheritance for consistent layouts
2. Separate logic from presentation
3. Keep templates focused and modular
4. Use meaningful variable names

### Performance Optimization
1. Cache frequently used templates
2. Minimize complex logic in templates
3. Use template includes judiciously
4. Optimize template hierarchy depth

### Security Guidelines
1. Always escape user-provided content
2. Validate template input data
3. Use XML() only for trusted content
4. Implement proper access controls

## Integration Examples

### Controller Integration
```python
# In controller
def index():
    context = {
        'title': 'Welcome',
        'users': db().select(db.users.ALL)
    }
    return dict(**context)
```

### View Template
```html
{{extend 'layout.html'}}
<h1>{{=title}}</h1>
{{for user in users:}}
  <div class="user">{{=user.name}}</div>
{{pass}}
```

## Debugging Support

### Template Debugging
- Source line mapping for errors
- Variable inspection capabilities
- Template compilation status
- Performance profiling hooks

### Development Tools
- Template syntax validation
- Variable usage analysis
- Performance monitoring
- Debug output formatting

## Compatibility Notes

### Python Version Support
- Compatible with Python 2.7+ and Python 3.x
- Unicode string handling
- Cross-platform file path support

### Framework Compatibility
- Full Web2py compatibility
- Gluon framework integration
- WSGI application support
- GAE (Google App Engine) compatibility

## Related Components

### Gluon Framework Modules
- `gluon.html`: HTML helper integration
- `gluon.globals`: Global context access
- `gluon.languages`: Internationalization support
- `gluon.cache`: Template caching integration

### YATL Features
- Template inheritance system
- Custom tag definitions
- Plugin architecture
- Extension mechanisms

## Future Considerations

### Enhancement Opportunities
1. Template preprocessing optimizations
2. Advanced caching strategies
3. Template compilation improvements
4. Performance monitoring tools

### Migration Path
- Seamless YATL version updates
- Template syntax extensions
- Framework integration improvements
- Backward compatibility maintenance

This template engine module provides a clean, efficient interface to powerful template functionality while maintaining the simplicity and elegance expected in the Gluon framework architecture.