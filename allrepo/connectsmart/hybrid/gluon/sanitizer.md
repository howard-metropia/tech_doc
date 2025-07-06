# Sanitizer Module

## Overview
The sanitizer module provides a simple wrapper around the YATL (Yet Another Template Language) sanitizer functionality. It serves as a compatibility bridge for HTML sanitization within the Gluon framework.

## Dependencies
- **yatl.sanitizer**: External YATL library sanitization module

## Exported Functions

### sanitize
Direct import from `yatl.sanitizer.sanitize`.

**Purpose:**
Sanitizes HTML content to prevent XSS attacks and ensure safe rendering of user-generated content.

**Usage:**
```python
from gluon.sanitizer import sanitize

# Basic sanitization
clean_html = sanitize(user_input)

# With custom allowed tags
clean_html = sanitize(
    user_input,
    allowed_tags=['p', 'br', 'strong', 'em'],
    allowed_attributes={'a': ['href', 'title']}
)
```

## Integration with Gluon

### Web2py Templates
The sanitizer is commonly used in web2py views to clean user content:

```python
# In controller
def show_comment():
    comment = db.comments(request.args(0))
    comment.body = sanitize(comment.body)
    return dict(comment=comment)
```

### Form Processing
Used with SQLFORM and form validators:

```python
# Sanitize form input
if form.process().accepted:
    form.vars.content = sanitize(form.vars.content)
    db.posts.insert(**form.vars)
```

## Security Considerations

### Default Behavior
- Removes potentially dangerous tags (script, iframe, etc.)
- Strips event handlers (onclick, onload, etc.)
- Validates URL schemes in links
- Preserves safe formatting tags

### Customization Options
The underlying YATL sanitizer supports:
- Custom tag whitelists
- Attribute filtering
- URL scheme validation
- Style attribute handling

## Common Use Cases

### User Comments
```python
def post_comment():
    form = SQLFORM(db.comments)
    if form.process().accepted:
        # Sanitize before storage
        db.comments[form.vars.id].update_record(
            body=sanitize(form.vars.body)
        )
    return dict(form=form)
```

### Rich Text Editors
```python
# Clean output from WYSIWYG editors
def save_article():
    content = request.vars.content
    clean_content = sanitize(
        content,
        allowed_tags=['p', 'br', 'strong', 'em', 'u', 
                     'h1', 'h2', 'h3', 'ul', 'ol', 'li']
    )
```

### API Responses
```python
# Sanitize data from external APIs
def show_external_content():
    data = fetch_from_api()
    data['description'] = sanitize(data['description'])
    return dict(data=data)
```

## Best Practices

### Input Validation
1. Always sanitize user input before storage
2. Re-sanitize when displaying if source is untrusted
3. Use appropriate sanitization levels for context

### Performance
- Cache sanitized content when possible
- Sanitize during write, not read operations
- Use bulk sanitization for multiple items

### Configuration
- Define sanitization policies per content type
- Document allowed tags and attributes
- Test sanitization rules thoroughly

## Migration Notes

### From Old Sanitizer
If migrating from older Gluon versions:

```python
# Old way
from gluon.html import sanitize_html
clean = sanitize_html(content)

# New way  
from gluon.sanitizer import sanitize
clean = sanitize(content)
```

### YATL Integration
The module now uses YATL's sanitizer, providing:
- Better performance
- More configuration options
- Active maintenance
- Consistent behavior with YATL templates

## Limitations

### Current Implementation
- Module is a thin wrapper
- No Gluon-specific customizations
- Relies entirely on YATL functionality

### Considerations
- Check YATL documentation for full options
- Test thoroughly when upgrading YATL
- Monitor for security updates

## See Also
- [YATL Documentation](https://github.com/web2py/yatl)
- Gluon HTML helpers
- Web2py security guidelines
- XSS prevention best practices