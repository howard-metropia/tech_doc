# gluon/contrib/markdown/markdown2.py

## Overview

The markdown2.py module is a complete Python implementation of Markdown text-to-HTML conversion. Originally developed by Trent Mick, this module provides fast and comprehensive Markdown processing with numerous extensions, making it a powerful text processing engine for Web2py applications.

## Key Components

### Main Class: Markdown
```python
class Markdown(object):
    """
    A Markdown processor with support for extras and safe mode.
    Converts Markdown text to HTML with customizable options.
    """
```

### Core Functions
```python
def markdown(text, html4tags=False, tab_width=4, safe_mode=None, extras=None, 
             link_patterns=None, use_file_vars=False):
    """
    Convert a markdown string to HTML
    
    Args:
        text: Markdown source text
        html4tags: Use HTML4 instead of XHTML tags
        tab_width: Tab expansion width
        safe_mode: HTML safety mode ('escape', 'remove', 'replace')
        extras: List of extra features to enable
        link_patterns: Custom link pattern matching
        
    Returns:
        str: HTML output
    """
```

## Markdown Syntax Support

### Core Syntax
- **Headers**: # ## ### etc.
- **Emphasis**: *italic* **bold** ***bold-italic***
- **Lists**: Unordered (-,*,+) and ordered (1.)
- **Links**: [text](url) and [text][ref]
- **Images**: ![alt](src)
- **Code**: `inline` and ```blocks```
- **Blockquotes**: > quoted text
- **Horizontal rules**: --- or ***

### Advanced Features
- **Tables**: GitHub-style table syntax
- **Footnotes**: Reference-style footnotes
- **Definition lists**: Term : definition syntax
- **Abbreviations**: Automatic abbreviation expansion

## Extra Features

### Code Processing
```python
# Fenced code blocks
extras = ['fenced-code-blocks']
markdown_text = """
```python
def hello():
    print("Hello, World!")
```
"""
```

### Table Support
```python
# GitHub-style tables
extras = ['tables']
markdown_text = """
| Name | Age | City |
|------|-----|------|
| John | 30  | NYC  |
| Jane | 25  | LA   |
"""
```

### Syntax Highlighting
```python
# Code syntax highlighting
extras = ['fenced-code-blocks', 'code-friendly']
# Requires Pygments for syntax highlighting
```

## Available Extras

### Text Processing
- **code-friendly**: Disable _ and __ for em/strong
- **cuddled-lists**: Allow lists cuddled to paragraphs
- **fenced-code-blocks**: GitHub-style ``` code blocks
- **footnotes**: Reference-style footnotes
- **header-ids**: Automatic header ID generation
- **markdown-in-html**: Process markdown inside HTML blocks
- **nofollow**: Add rel="nofollow" to external links
- **pyshell**: Python shell code block processing
- **smarty-pants**: Smart quotes and typography
- **spoiler**: Spoiler tag support
- **strike**: ~~strikethrough~~ text
- **tables**: GitHub-style table syntax
- **tag-friendly**: Disable < and > encoding in text
- **toc**: Table of contents generation
- **wiki-tables**: MediaWiki-style table syntax
- **xml**: XML/XHTML compatible output

### Link Processing
- **link-patterns**: Custom link pattern recognition
- **auto-link**: Automatic URL linking
- **break-on-newline**: Convert newlines to <br>

## Safe Mode Options

### HTML Sanitization
```python
# Escape HTML tags
html = markdown(text, safe_mode='escape')

# Remove HTML tags
html = markdown(text, safe_mode='remove') 

# Replace HTML with placeholders
html = markdown(text, safe_mode='replace')
```

### Security Implementation
- **escape**: Converts `<script>` to `&lt;script&gt;`
- **remove**: Strips HTML tags completely
- **replace**: Replaces with `[HTML_REMOVED]` placeholders

## Performance Features

### Optimization Techniques
- **Compiled regex patterns**: Pre-compiled for speed
- **Lazy processing**: Process sections as needed
- **Memory efficiency**: Minimal memory overhead
- **Incremental parsing**: Stream-friendly processing

### Caching Support
```python
# Cache compiled patterns
class CachedMarkdown(Markdown):
    _pattern_cache = {}
    
    def __init__(self, *args, **kwargs):
        if self.__class__ not in self._pattern_cache:
            super().__init__(*args, **kwargs)
            self._pattern_cache[self.__class__] = self._patterns
        else:
            self._patterns = self._pattern_cache[self.__class__]
```

## Advanced Usage

### Custom Extensions
```python
class CustomMarkdown(Markdown):
    """Custom Markdown processor with additional features"""
    
    def __init__(self):
        super().__init__(extras=['tables', 'code-friendly'])
        
    def _do_custom_processing(self, text):
        """Add custom text processing"""
        # Custom processing logic
        return text
```

### Link Pattern Matching
```python
# Custom link patterns
link_patterns = [
    (re.compile(r'bug (\d+)', re.IGNORECASE),
     r'http://bugs.example.com/\1'),
    (re.compile(r'issue #(\d+)', re.IGNORECASE),
     r'http://github.com/user/repo/issues/\1')
]

html = markdown(text, link_patterns=link_patterns)
```

### Table of Contents Generation
```python
# Generate TOC
md = Markdown(extras=['toc'])
html = md.convert(text)
toc_html = md.toc_html  # Access generated TOC
```

## Error Handling

### Input Validation
```python
def safe_markdown(text):
    """Safely process markdown with error handling"""
    if not text:
        return ''
    
    try:
        return markdown(text, safe_mode='escape')
    except Exception as e:
        # Log error and return escaped text
        import logging
        logging.error(f"Markdown processing error: {e}")
        return escape(str(text))
```

### Unicode Handling
```python
# Proper Unicode processing
def unicode_markdown(text, encoding='utf-8'):
    """Process markdown with Unicode support"""
    if isinstance(text, bytes):
        text = text.decode(encoding, 'replace')
    
    return markdown(text)
```

## Integration Examples

### Web2py Integration
```python
# In Web2py model
def markdown_field(text):
    """Convert markdown field to HTML"""
    return XML(markdown(text, 
                       safe_mode='escape',
                       extras=['fenced-code-blocks', 'tables']))

# In database definition
db.define_table('post',
    Field('title'),
    Field('content', 'text'),
    Field('content_html', 'text', 
          compute=lambda r: str(markdown_field(r['content'])))
)
```

### File Processing
```python
def markdown_file(filepath):
    """Process markdown file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return markdown(content, extras=['toc', 'tables'])
```

### Batch Processing
```python
def batch_markdown(texts, **kwargs):
    """Process multiple markdown texts efficiently"""
    md = Markdown(**kwargs)
    return [md.convert(text) for text in texts]
```

## Configuration Examples

### Documentation Processing
```python
# Configure for documentation
doc_markdown = Markdown(
    extras=[
        'fenced-code-blocks',
        'tables', 
        'toc',
        'header-ids',
        'footnotes'
    ],
    safe_mode='escape'
)
```

### Blog Processing
```python
# Configure for blog posts
blog_markdown = Markdown(
    extras=[
        'fenced-code-blocks',
        'smarty-pants',
        'break-on-newline',
        'nofollow'
    ],
    safe_mode='escape'
)
```

### Comment Processing
```python
# Configure for user comments
comment_markdown = Markdown(
    extras=['code-friendly'],
    safe_mode='remove'  # Remove HTML completely
)
```

## Best Practices

### Security Guidelines
1. **Always use safe_mode** for user input
2. **Validate extras list** from user configuration
3. **Sanitize file paths** in include operations
4. **Monitor output size** to prevent DoS attacks

### Performance Guidelines
1. **Reuse Markdown instances** for multiple conversions
2. **Cache converted HTML** when possible
3. **Use appropriate extras** - only enable what's needed
4. **Profile large document processing**

### Content Guidelines
1. **Standardize on extras** across application
2. **Document supported syntax** for users
3. **Provide preview functionality** for editors
4. **Test with international content**

This comprehensive Markdown implementation provides robust text processing capabilities while maintaining security and performance standards for production web applications.