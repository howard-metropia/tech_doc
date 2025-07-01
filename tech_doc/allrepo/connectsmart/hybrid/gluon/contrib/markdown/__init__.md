# gluon/contrib/markdown/__init__.py

## Overview

The markdown __init__ module provides Markdown text processing integration for Web2py applications. This module exposes markdown2 functionality through Web2py's XML helper system, enabling safe conversion of Markdown text to HTML within the Web2py framework.

## Key Components

### Main Function: WIKI()
```python
def WIKI(text, encoding="utf8", safe_mode='escape', html4tags=False, **attributes):
    """
    Convert Markdown text to Web2py XML object
    
    Args:
        text: Markdown source text
        encoding: Text encoding (default: utf8)
        safe_mode: HTML escaping mode ('escape', 'remove', 'replace')
        html4tags: Use HTML4 tags instead of XHTML
        **attributes: Additional XML attributes
        
    Returns:
        XML: Web2py XML object with converted HTML
    """
```

### Dependencies
```python
from .markdown2 import *              # Markdown processing engine
from gluon.html import XML            # Web2py XML helper
from gluon._compat import to_unicode  # Unicode handling
```

## Functionality

### Markdown to XML Conversion
The WIKI function provides a bridge between Markdown text and Web2py's XML system:

```python
# Convert Markdown to XML
wiki_content = WIKI("""
# Header
This is **bold** and *italic* text.
""")

# Use in Web2py views
return dict(content=wiki_content)
```

### Safe HTML Processing
```python
# Safe mode options:
# 'escape' - Escape HTML tags (default)
# 'remove' - Remove HTML tags
# 'replace' - Replace with placeholders

safe_content = WIKI(user_input, safe_mode='escape')
```

### Extended Markdown Features
```python
# Support for markdown2 extras
enhanced_content = WIKI(text, extras=['fenced-code-blocks', 'tables'])
```

## Implementation Details

### Text Processing Pipeline
1. **Input Validation**: Check for empty or None input
2. **Unicode Conversion**: Ensure proper text encoding
3. **Markdown Processing**: Convert Markdown to HTML using markdown2
4. **XML Wrapping**: Wrap result in Web2py XML object
5. **Encoding**: Apply proper character encoding

### Unicode Handling
```python
text = to_unicode(text, encoding, 'replace')
```
- Converts input to Unicode string
- Handles encoding errors gracefully
- Maintains text integrity

### Error Handling
```python
if not text:
    text = ''  # Handle None/empty input
```

## Integration with Web2py

### XML Object Creation
```python
return XML(markdown(text, extras=extras,
                   safe_mode=safe_mode, html4tags=html4tags)
          .encode(encoding, 'xmlcharrefreplace'), **attributes)
```

### Template Integration
```python
# In Web2py controller
def page():
    content = db.page[request.args(0)].content
    return dict(wiki_content=WIKI(content))

# In view
{{=wiki_content}}
```

### Form Integration
```python
# In model for wiki-style forms
db.define_table('page',
    Field('title'),
    Field('content', 'text', widget=SQLFORM.widgets.text.widget),
    Field('content_html', compute=lambda r: WIKI(r['content']))
)
```

## Security Features

### Safe Mode Implementation
- **escape**: Converts HTML tags to safe entities
- **remove**: Strips HTML tags completely  
- **replace**: Replaces tags with placeholders

### XSS Prevention
```python
# Automatic escaping of user content
user_markdown = WIKI(user_input, safe_mode='escape')
```

### Character Encoding
- Uses `xmlcharrefreplace` for safe XML encoding
- Handles non-ASCII characters properly
- Prevents encoding-related security issues

## Configuration Options

### Markdown Extras
Support for extended Markdown features:
- **fenced-code-blocks**: GitHub-style code blocks
- **tables**: Table syntax support
- **footnotes**: Footnote references
- **toc**: Table of contents generation
- **code-friendly**: Disable underscore emphasis
- **cuddled-lists**: Relaxed list formatting

### HTML Output Options
```python
# XHTML output (default)
WIKI(text, html4tags=False)

# HTML4 output
WIKI(text, html4tags=True)
```

## Usage Examples

### Basic Markdown
```python
# Simple text conversion
text = """
# My Document
This is a **markdown** document with *emphasis*.

- List item 1
- List item 2
"""

content = WIKI(text)
```

### Advanced Features
```python
# With extras and custom attributes
content = WIKI(
    text, 
    extras=['fenced-code-blocks', 'tables'],
    _class='markdown-content',
    _id='wiki-text'
)
```

### Form Processing
```python
# Process form input safely
def process_wiki():
    if form.process().accepted:
        # Convert and store
        html_content = WIKI(form.vars.markdown_text, safe_mode='escape')
        db.documents.insert(
            title=form.vars.title,
            markdown_source=form.vars.markdown_text,
            html_content=str(html_content)
        )
```

## Performance Considerations

### Caching Strategy
```python
# Cache converted content
@cache.action()
def get_wiki_content(page_id):
    page = db.page[page_id]
    return WIKI(page.content)
```

### Large Document Handling
- Convert large documents in background tasks
- Store HTML output in database
- Use lazy loading for large wikis

## Best Practices

### Input Validation
1. Always validate user input before processing
2. Use appropriate safe_mode settings
3. Consider input size limits
4. Implement rate limiting for conversions

### Output Handling
1. Cache converted HTML when possible
2. Validate HTML output in templates
3. Use proper encoding in all contexts
4. Test with international characters

### Security Guidelines
1. Never trust user input without safe_mode
2. Validate extras list from user input
3. Sanitize file includes and links
4. Monitor for potential XSS vectors

## Error Recovery

### Input Error Handling
```python
try:
    content = WIKI(user_input)
except Exception as e:
    # Log error and provide fallback
    content = XML(f"<p>Error processing content: {str(e)}</p>")
```

### Encoding Error Management
```python
# Robust encoding handling
def safe_wiki(text, encoding='utf-8'):
    try:
        return WIKI(text, encoding=encoding)
    except UnicodeError:
        # Try alternative encoding
        return WIKI(text, encoding='latin-1')
```

This module provides a robust foundation for integrating Markdown processing into Web2py applications while maintaining security and performance standards.