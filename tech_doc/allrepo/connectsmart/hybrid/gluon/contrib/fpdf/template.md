# gluon/contrib/fpdf/template.py

## Overview

The template.py module provides a template-based PDF generation system for FPDF. It allows creation of PDF documents using predefined templates with placeholders for dynamic content, making it ideal for generating forms, reports, and standardized documents with variable data.

## Key Components

### Main Class: Template
```python
class Template:
    def __init__(self, infile=None, elements=None, format='A4', 
                 orientation='portrait', title='', author='', 
                 subject='', creator='', keywords=''):
```
- Manages template elements and rendering
- Supports CSV-based template definitions
- Handles multiple element types
- Integrates with FPDF for output

### Element Handlers
```python
self.handlers = {
    'T': self.text,      # Text element
    'L': self.line,      # Line element
    'I': self.image,     # Image element
    'B': self.rect,      # Box/Rectangle element
    'BC': self.barcode,  # Barcode element
    'W': self.write,     # Write/flowing text element
}
```

### Helper Functions
```python
def rgb(col):
    """Convert integer color to RGB tuple"""
    return (col // 65536), (col // 256 % 256), (col % 256)
```

## Template Structure

### Element Definition
Each template element contains:
- **name**: Unique identifier
- **type**: Element type (T, L, I, B, BC, W)
- **x1, y1**: Starting coordinates
- **x2, y2**: Ending coordinates (for lines/boxes)
- **font**: Font family
- **size**: Font size
- **bold, italic, underline**: Text styling
- **foreground, background**: Colors
- **align**: Text alignment
- **text**: Default text content
- **priority**: Rendering order
- **multiline**: Multi-line text support

### CSV Template Format
```csv
name,type,x1,y1,x2,y2,font,size,bold,italic,underline,foreground,background,align,text,priority,multiline
title,T,10,10,200,20,Arial,16,1,0,0,0,16777215,C,Document Title,1,0
line1,L,10,25,200,25,,,,,,,,,,,2,
logo,I,10,30,50,70,,,,,,,,,logo.png,3,
```

## Core Functionality

### Template Loading

#### CSV Parser
```python
def parse_csv(self, infile, delimiter=",", decimal_sep="."):
    """Parse template format csv file and create elements dict"""
    keys = ('name','type','x1','y1','x2','y2','font','size',
        'bold','italic','underline','foreground','background',
        'align','text','priority', 'multiline')
    
    with open(infile) as f:
        for row in csv.DictReader(f, keys, delimiter=delimiter):
            # Process each row into element
            self.elements.append(self.parse_element(row))
```

#### Element Structure
```python
def load_elements(self, elements):
    """Initialize the internal element structures"""
    self.pg_no = 0
    self.elements = elements
    self.keys = [v['name'].lower() for v in self.elements]
```

### Rendering Process

#### Main Render Method
```python
def render(self, outfile=None, dest="F"):
    """Render the template to PDF"""
    self.pdf.add_page()
    
    # Sort elements by priority
    sorted_elements = sorted(self.elements, key=lambda x: x['priority'])
    
    # Render each element
    for element in sorted_elements:
        handler = self.handlers.get(element['type'])
        if handler:
            handler(element)
    
    return self.pdf.output(outfile, dest)
```

### Element Handlers

#### Text Element Handler
```python
def text(self, element):
    """Render text element"""
    # Set font properties
    self.pdf.set_font(element['font'], 
                     self.get_style(element), 
                     element['size'])
    
    # Set colors
    if element['foreground']:
        self.pdf.set_text_color(*rgb(element['foreground']))
    
    # Position and render text
    if element['multiline']:
        self.pdf.set_xy(element['x1'], element['y1'])
        self.pdf.multi_cell(element['x2']-element['x1'], 
                           element['size'], 
                           element['text'], 
                           align=element['align'])
    else:
        self.pdf.text(element['x1'], element['y1'], element['text'])
```

#### Line Element Handler
```python
def line(self, element):
    """Render line element"""
    self.pdf.line(element['x1'], element['y1'], 
                  element['x2'], element['y2'])
```

#### Image Element Handler
```python
def image(self, element):
    """Render image element"""
    self.pdf.image(element['text'],  # Image path in text field
                   element['x1'], element['y1'],
                   element['x2']-element['x1'],  # Width
                   element['y2']-element['y1'])  # Height
```

#### Rectangle Element Handler
```python
def rect(self, element):
    """Render rectangle/box element"""
    style = 'D'  # Draw only by default
    if element['background']:
        self.pdf.set_fill_color(*rgb(element['background']))
        style = 'DF'  # Draw and fill
    
    self.pdf.rect(element['x1'], element['y1'],
                  element['x2']-element['x1'],
                  element['y2']-element['y1'],
                  style)
```

## Data Binding

### Text Substitution
```python
self.texts = {}  # Dictionary for text replacements

def set_text(self, name, value):
    """Set text value for named element"""
    self.texts[name.lower()] = value

def apply_texts(self):
    """Apply text substitutions to elements"""
    for element in self.elements:
        if element['name'].lower() in self.texts:
            element['text'] = self.texts[element['name'].lower()]
```

### Dynamic Content
```python
# Usage example
template = Template('invoice.csv')
template.set_text('customer_name', 'John Doe')
template.set_text('invoice_no', 'INV-2024-001')
template.set_text('total', '$1,234.56')
template.render('invoice.pdf')
```

## Advanced Features

### Multi-Page Support
```python
def add_page(self):
    """Add new page and render page elements"""
    self.pdf.add_page()
    self.pg_no += 1
    # Render elements marked for all pages
    self.render_page_elements()
```

### Barcode Support
```python
def barcode(self, element):
    """Render barcode element"""
    # Integration point for barcode libraries
    # Element contains barcode type and data
    barcode_type = element.get('barcode_type', 'code39')
    self.render_barcode(element['text'], 
                       element['x1'], element['y1'],
                       barcode_type)
```

### Style Management
```python
def get_style(self, element):
    """Build font style string from element properties"""
    style = ''
    if element.get('bold'):
        style += 'B'
    if element.get('italic'):
        style += 'I'
    if element.get('underline'):
        style += 'U'
    return style
```

## Usage Patterns

### Basic Template Usage
```python
# Create template from CSV
template = Template('form_template.csv')

# Set dynamic values
template.set_text('name', 'Jane Smith')
template.set_text('date', '2024-01-15')

# Render to PDF
template.render('output.pdf')
```

### Programmatic Template
```python
# Define elements programmatically
elements = [
    {
        'name': 'header',
        'type': 'T',
        'x1': 10, 'y1': 10,
        'x2': 200, 'y2': 20,
        'text': 'Report Title',
        'size': 18,
        'bold': 1,
        'align': 'C',
        'priority': 1
    }
]

template = Template(elements=elements)
template.render('report.pdf')
```

### Batch Processing
```python
# Process multiple records
template = Template('certificate.csv')

for student in students:
    template.set_text('student_name', student['name'])
    template.set_text('course', student['course'])
    template.set_text('date', student['completion_date'])
    
    filename = f"certificate_{student['id']}.pdf"
    template.render(filename)
    template.reset()  # Clear for next iteration
```

## Error Handling

### Validation
```python
def validate_element(self, element):
    """Validate element properties"""
    required = ['name', 'type', 'x1', 'y1']
    for field in required:
        if field not in element:
            raise ValueError(f"Missing required field: {field}")
    
    if element['type'] not in self.handlers:
        raise ValueError(f"Unknown element type: {element['type']}")
```

### Coordinate Validation
```python
def validate_coordinates(self, element):
    """Ensure coordinates are within page bounds"""
    page_width = self.pdf.w
    page_height = self.pdf.h
    
    if element['x1'] < 0 or element['x1'] > page_width:
        raise ValueError("X coordinate out of bounds")
    if element['y1'] < 0 or element['y1'] > page_height:
        raise ValueError("Y coordinate out of bounds")
```

## Performance Optimization

### Element Caching
- Pre-process elements on load
- Cache calculated positions
- Minimize repeated calculations

### Batch Rendering
- Group similar operations
- Reuse font settings
- Optimize color changes

## Best Practices

### Template Design
1. Use meaningful element names
2. Set appropriate priorities
3. Design with reusability in mind
4. Document template structure

### Data Management
1. Validate input data
2. Handle missing values gracefully
3. Escape special characters
4. Use consistent data formats

### Error Recovery
1. Provide default values
2. Log rendering errors
3. Continue with valid elements
4. Generate partial output when possible