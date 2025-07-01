# gluon/contrib/fpdf/html.py

## Overview

The html.py module provides HTML to PDF conversion capabilities for the FPDF library. It implements an HTML parser that can render basic HTML markup into PDF format, enabling the conversion of web content into printable documents while preserving formatting and structure.

## Key Components

### Main Class: HTML2FPDF
An HTMLParser subclass that processes HTML tags and converts them to PDF elements:
- Parses HTML structure
- Handles text formatting
- Processes tables and lists
- Manages hyperlinks
- Embeds images

### Helper Functions
```python
def px2mm(px):
    """Convert pixels to millimeters"""
    return int(px)*25.4/72.0

def hex2dec(color="#000000"):
    """Convert hex color to RGB decimal values"""
    if color:
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        return r, g, b
```

## HTML Parser Implementation

### Initialization
```python
def __init__(self, pdf, image_map=None):
    HTMLParser.__init__(self)
    self.pdf = pdf                    # FPDF instance
    self.style = {}                   # Current style state
    self.href = ''                    # Current hyperlink
    self.align = ''                   # Text alignment
    self.font_stack = []              # Font state stack
    self.image_map = image_map        # Image URL mapper
    self.table = None                 # Table attributes
    self.td = None                    # Cell attributes
```

### State Management
The parser maintains various states:
- **style**: Current text styling (bold, italic, etc.)
- **pre**: Preformatted text mode
- **font_stack**: Stack for nested font changes
- **table context**: Table, row, and cell tracking

## Supported HTML Elements

### Text Formatting
- **Bold**: `<b>`, `<strong>`
- **Italic**: `<i>`, `<em>`
- **Underline**: `<u>`
- **Font**: `<font>` with face, size, color attributes
- **Preformatted**: `<pre>`

### Structure Elements
- **Paragraphs**: `<p>` with alignment
- **Line Breaks**: `<br>`, `<br/>`
- **Horizontal Rule**: `<hr>`
- **Blockquote**: `<blockquote>`

### Lists
- **Unordered Lists**: `<ul>`, `<li>`
- **Ordered Lists**: `<ol>`, `<li>`
- Nested list support
- Custom bullet styles

### Tables
- **Table**: `<table>` with border, width
- **Row**: `<tr>`
- **Cell**: `<td>` with width, align, bgcolor
- **Header**: `<th>` with special formatting

### Links and Images
- **Hyperlinks**: `<a href="">`
- **Images**: `<img src="">` with width, height
- Image mapping for URL transformation

## HTML Processing Flow

### Tag Handling
```python
def handle_starttag(self, tag, attrs):
    """Process opening HTML tags"""
    if tag == 'b' or tag == 'strong':
        self.set_style('B', True)
    elif tag == 'i' or tag == 'em':
        self.set_style('I', True)
    elif tag == 'u':
        self.set_style('U', True)
    elif tag == 'p':
        self.handle_paragraph(attrs)
    elif tag == 'table':
        self.handle_table_start(attrs)
    # ... more tag handlers
```

### Text Processing
```python
def handle_data(self, data):
    """Process text content"""
    if self.pre:
        # Preserve whitespace in pre mode
        self.pdf.write(self.h, data)
    else:
        # Normal text processing
        data = data.strip()
        if data:
            self.write_text(data)
```

### Style Management
```python
def set_style(self, style, enable):
    """Toggle text style"""
    if enable:
        self.style[style] = True
    else:
        self.style.pop(style, None)
    self.update_font()

def update_font(self):
    """Apply current font styles"""
    style = ''
    if 'B' in self.style:
        style += 'B'
    if 'I' in self.style:
        style += 'I'
    if 'U' in self.style:
        style += 'U'
    self.pdf.set_font(self.font_face, style, self.font_size)
```

## Table Support

### Table Structure
```python
def handle_table_start(self, attrs):
    """Initialize table processing"""
    self.table = {
        'border': 0,
        'cells': [],
        'rows': [],
        'col_widths': []
    }
    # Parse table attributes
```

### Cell Management
```python
def handle_td(self, attrs):
    """Process table cell"""
    self.td = {
        'width': None,
        'align': 'L',
        'bgcolor': None,
        'content': ''
    }
    # Parse cell attributes
```

### Table Rendering
- Automatic column width calculation
- Cell border and background support
- Text alignment within cells
- Multi-line cell content

## Image Handling

### Image Processing
```python
def handle_img(self, attrs):
    """Embed image in PDF"""
    src = attrs.get('src', '')
    if self.image_map:
        src = self.image_map(src)
    
    width = attrs.get('width', 0)
    height = attrs.get('height', 0)
    
    self.pdf.image(src, self.pdf.get_x(), self.pdf.get_y(), width, height)
```

### Image Mapping
- URL transformation support
- Local file path resolution
- Dimension preservation

## Font and Color Management

### Font Handling
```python
def handle_font(self, attrs):
    """Process font tag"""
    if 'face' in attrs:
        self.font_face = attrs['face']
    if 'size' in attrs:
        self.font_size = int(attrs['size'])
    if 'color' in attrs:
        self.set_text_color(attrs['color'])
```

### Color Processing
- Hex color parsing (#RRGGBB)
- RGB color application
- Text and background colors

## List Processing

### List State
```python
self.bullet = []  # Stack of list markers
self.indent = 0   # Current indentation level
```

### List Item Rendering
- Automatic numbering for ordered lists
- Bullet symbols for unordered lists
- Proper indentation handling
- Nested list support

## Integration Features

### FPDF Integration
```python
class HTMLMixin(FPDF, HTML2FPDF):
    """Mixin class for FPDF with HTML support"""
    def write_html(self, html):
        parser = HTML2FPDF(self)
        parser.feed(html)
```

### Usage Pattern
```python
pdf = FPDF()
pdf.add_page()
pdf.write_html('<h1>Title</h1><p>Content</p>')
```

## Limitations and Constraints

### HTML Support
- Basic HTML 4 subset only
- No CSS support beyond inline styles
- Limited attribute handling
- No JavaScript execution

### Layout Limitations
- Simple table layouts only
- No floating elements
- Basic text flow
- Limited positioning options

### Performance Considerations
- Linear parsing
- Memory usage scales with HTML size
- No streaming support

## Error Handling

### Malformed HTML
- Graceful handling of unclosed tags
- Missing attribute defaults
- Invalid color fallbacks

### Resource Loading
- Missing image handling
- Invalid URL recovery
- File access validation

## Usage Examples

### Basic HTML Conversion
```python
pdf = FPDF()
pdf.add_page()
html2pdf = HTML2FPDF(pdf)
html2pdf.feed('<p>Hello <b>World</b>!</p>')
pdf.output('output.pdf')
```

### Table Generation
```python
html = '''
<table border="1">
    <tr>
        <th>Header 1</th>
        <th>Header 2</th>
    </tr>
    <tr>
        <td>Cell 1</td>
        <td>Cell 2</td>
    </tr>
</table>
'''
html2pdf.feed(html)
```

### Image Embedding
```python
def image_mapper(src):
    # Transform URLs to local paths
    return f'/images/{src.split("/")[-1]}'

html2pdf = HTML2FPDF(pdf, image_map=image_mapper)
html2pdf.feed('<img src="http://example.com/image.jpg" width="100">')
```