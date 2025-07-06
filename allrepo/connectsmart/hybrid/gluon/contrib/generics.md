# Gluon Contrib Generics Module

## Overview
Generic response format converters for web2py applications. This module provides utilities to convert HTML content to various output formats including LaTeX, PDF (via pdflatex or PyFPDF), and other serialization formats with comprehensive error handling.

## Module Information
- **Module**: `gluon.contrib.generics`
- **Dependencies**: `gluon.contrib.fpdf`, `gluon.contrib.markmin`, `gluon.sanitizer`
- **Purpose**: HTML-to-format conversion utilities
- **Use Case**: Generic views, export functionality, document generation

## Key Features
- **Multi-format Export**: HTML to LaTeX, PDF conversion
- **Dual PDF Engines**: pdflatex (preferred) and PyFPDF (fallback)
- **Error Handling**: Comprehensive exception handling with HTTP responses
- **Image Processing**: Automatic image path resolution and mapping
- **Content Sanitization**: HTML sanitization for safe PDF generation

## Core Functions

### wrapper()
Generic function wrapper that provides standardized error handling for serializers.

**Signature:**
```python
def wrapper(f)
```

**Parameters:**
- `f`: Function to wrap (serializer function)

**Returns:**
- Wrapped function with error handling

.**Error Handling:**
- `TypeError/ValueError`: 405 HTTP error with serialization error message
- `ImportError`: 405 HTTP error indicating missing dependencies
- `Exception`: 405 HTTP error with generic error message

**Note:**
- Contains typo: `ouput` should be `output` on line 16
- Returns XML-wrapped output

## HTML-to-LaTeX Conversion

### latex_from_html()
Convert HTML content to LaTeX format via Markmin intermediate representation.

**Signature:**
```python
def latex_from_html(html)
```

**Parameters:**
- `html`: HTML content string

**Returns:**
- LaTeX formatted string

**Process:**
1. Parse HTML using TAG parser
2. Extract body content
3. Flatten to Markmin format using `markmin_serializer`
4. Convert Markmin to LaTeX using `markmin2latex()`

**Usage:**
```python
html_content = "<body><h1>Title</h1><p>Content</p></body>"
latex_output = latex_from_html(html_content)
```

## PDF Generation

### pdflatex_from_html()
Generate PDF using pdflatex system command (preferred method).

**Signature:**
```python
def pdflatex_from_html(html)
```

**Parameters:**
- `html`: HTML content string

**Returns:**
- PDF binary data

**Requirements:**
- pdflatex system command must be available
- Checks availability with `which pdflatex`

**Process:**
1. Check pdflatex availability
2. Convert HTML to Markmin format
3. Generate PDF using `markmin2pdf()`
4. Handle errors and warnings
5. Return PDF binary or error HTML

**Error Handling:**
- If errors occur, returns HTML error page with:
  - Error list
  - Warning list
  - Sets Content-Type to text/html
  - Raises HTTP 405 error

### pyfpdf_from_html()
Generate PDF using PyFPDF library (fallback method).

**Signature:**
```python
def pyfpdf_from_html(html)
```

**Parameters:**
- `html`: HTML content string

**Returns:**
- XML-wrapped PDF binary data

**Features:**
- **Image Mapping**: Resolves image paths for PDF inclusion
- **HTML Sanitization**: Filters HTML for safe PDF rendering
- **Table Support**: Preserves table formatting attributes

**Image Path Resolution:**
```python
def image_map(path):
    if path.startswith('/%s/static/' % request.application):
        return os.path.join(request.folder, path.split('/', 2)[2])
    return 'http%s://%s%s' % (request.is_https and 's' or '', 
                             request.env.http_host, path)
```

**Allowed HTML Attributes:**
- `a`: href, title
- `img`: src, alt  
- `blockquote`: type
- `td`: align, bgcolor, colspan, height, width
- `tr`: bgcolor, height, width
- `table`: border, bgcolor, height, width

### pdf_from_html()
Smart PDF generation that chooses the best available method.

**Signature:**
```python
def pdf_from_html(html)
```

**Parameters:**
- `html`: HTML content string

**Returns:**
- PDF binary data

**Logic:**
1. Check if pdflatex is available
2. If available: use `pdflatex_from_html()`
3. If not available: use `pyfpdf_from_html()`

**Preference Order:**
1. **pdflatex** (higher quality, better LaTeX support)
2. **PyFPDF** (pure Python, always available)

## Integration Examples

### Generic View Usage
```python
# In controller
def export():
    if request.extension == 'pdf':
        # HTML content will be converted to PDF
        return dict(content=html_content)
    return dict(content=html_content)

# In generic.pdf view
{{=pdf_from_html(response.render('path/to/template.html'))}}
```

### Custom Export Function
```python
def generate_report():
    # Generate HTML content
    html = response.render('reports/template.html', data)
    
    if request.vars.format == 'latex':
        response.headers['Content-Type'] = 'application/x-latex'
        return latex_from_html(html)
    elif request.vars.format == 'pdf':
        response.headers['Content-Type'] = 'application/pdf'
        return pdf_from_html(html)
    else:
        return html
```

### Wrapper Usage
```python
@wrapper
def custom_serializer(data):
    # Custom serialization logic
    return serialize_data(data)

# Usage in view
{{=custom_serializer(data)}}
```

## Error Handling Patterns

### PDF Generation Errors
```python
try:
    pdf_content = pdf_from_html(html)
    response.headers['Content-Type'] = 'application/pdf'
    return pdf_content
except HTTP as e:
    # Handle conversion errors
    if e.status == 405:
        # Fallback to HTML
        return html
    raise
```

### LaTeX Conversion Errors
```python
try:
    latex_content = latex_from_html(html)
except Exception as e:
    # Handle conversion errors
    logger.error("LaTeX conversion failed: %s" % e)
    return "Conversion failed"
```

## Dependencies and Requirements

### System Requirements
- **pdflatex**: For high-quality PDF generation (optional)
- **Operating System**: Unix-like system for `which` command

### Python Dependencies
- **PyFPDF**: For alternative PDF generation
- **Markmin**: For HTML-to-LaTeX conversion
- **Sanitizer**: For HTML content cleaning

### Web2py Integration
- Uses `current.request` for context
- Uses `current.response` for headers
- Integrates with web2py's generic views system

## Performance Considerations

### PDF Generation Speed
- **pdflatex**: Slower but higher quality
- **PyFPDF**: Faster but limited LaTeX features

### Memory Usage
- Large HTML documents may consume significant memory
- PDF generation is memory-intensive

### Caching Strategies
```python
@cache.action()
def cached_pdf():
    html = generate_content()
    return pdf_from_html(html)
```

## Security Considerations

### HTML Sanitization
- Input HTML is sanitized before PDF generation
- Prevents XSS and injection attacks
- Filters dangerous HTML elements and attributes

### Image Path Validation
- Image paths are validated and resolved safely
- Prevents directory traversal attacks
- Maps application static files correctly

### Error Information Disclosure
- Error messages may reveal system information
- Consider generic error messages in production

This module provides essential format conversion capabilities for web2py applications, enabling flexible content export with robust error handling and security considerations.