# PyRTF Package

**File**: `gluon/contrib/pyrtf/__init__.py`  
**Type**: Rich Text Format (RTF) Generation Library  
**Framework**: Web2py Gluon Framework  
**Purpose**: RTF Document Creation and Manipulation

## Overview

PyRTF is a Python library for creating Rich Text Format (RTF) documents programmatically. This package provides a comprehensive set of tools for generating formatted documents that can be opened by Microsoft Word, LibreOffice, and other RTF-compatible applications.

## Package Architecture

### Core Modules
- **Elements**: Document structure and content elements
- **PropertySets**: Formatting properties for text, paragraphs, and pages
- **Styles**: Style definitions and management
- **Renderer**: RTF output generation and serialization
- **Constants**: RTF constants, enumerations, and utility values

### Module Imports
```python
from .PropertySets import *  # Formatting properties
from .Elements import *      # Document elements
from .Styles import *        # Style definitions
from .Renderer import *      # RTF rendering
from .Constants import PY2   # Python 2/3 compatibility
```

## Key Features

### Document Generation
- **Complete RTF Support**: Full RTF specification implementation
- **Rich Formatting**: Text styles, paragraphs, tables, headers, footers
- **Cross-Platform**: Works with any RTF-compatible application
- **Python 2/3 Compatible**: Supports both Python versions

### Content Elements
- **Text Formatting**: Font, size, color, bold, italic, underline
- **Paragraph Formatting**: Alignment, indentation, spacing, bullets
- **Tables**: Multi-column layouts with cell formatting
- **Headers/Footers**: Page headers and footers with content
- **Images**: Embedded image support

## Main Functions

### dumps()
Primary function for RTF document serialization:

```python
def dumps(doc):
    """Convert Document object to RTF string"""
    s = BytesIO()
    r = Renderer()
    r.Write(doc, s)
    return s.getvalue()
```

**Usage**:
```python
import pyrtf

# Create document
doc = pyrtf.Document()
section = pyrtf.Section()
doc.Sections.append(section)

# Add content
p = pyrtf.Paragraph()
p.append(pyrtf.Text("Hello, RTF World!"))
section.append(p)

# Generate RTF
rtf_content = pyrtf.dumps(doc)
```

## Python 2/3 Compatibility

### BytesIO Handling
```python
if PY2:
    from cStringIO import StringIO as BytesIO
else:
    from io import BytesIO
```

The package automatically handles the differences between Python 2 and 3 for:
- String/bytes handling
- IO operations
- Unicode processing

## Usage Examples

### Basic Document Creation
```python
from gluon.contrib import pyrtf

# Create new document
doc = pyrtf.Document()
section = pyrtf.Section()
doc.Sections.append(section)

# Add paragraph with formatted text
paragraph = pyrtf.Paragraph()
paragraph.append(pyrtf.Text("Bold text", bold=True))
paragraph.append(pyrtf.Text(" and "))
paragraph.append(pyrtf.Text("italic text", italic=True))
section.append(paragraph)

# Generate RTF output
rtf_string = pyrtf.dumps(doc)
```

### Web2py Controller Integration
```python
def generate_report():
    from gluon.contrib import pyrtf
    
    # Create document
    doc = pyrtf.Document()
    section = pyrtf.Section()
    doc.Sections.append(section)
    
    # Add title
    title = pyrtf.Paragraph()
    title.append(pyrtf.Text("Monthly Report", 
                           font_size=24, 
                           bold=True))
    section.append(title)
    
    # Add content from database
    for record in db(db.reports.id > 0).select():
        p = pyrtf.Paragraph()
        p.append(pyrtf.Text(record.content))
        section.append(p)
    
    # Generate and return RTF
    rtf_content = pyrtf.dumps(doc)
    
    response.headers['Content-Type'] = 'application/rtf'
    response.headers['Content-Disposition'] = 'attachment; filename=report.rtf'
    
    return rtf_content
```

### Table Creation
```python
def create_data_table():
    from gluon.contrib import pyrtf
    
    doc = pyrtf.Document()
    section = pyrtf.Section()
    doc.Sections.append(section)
    
    # Create table
    table = pyrtf.Table()
    
    # Add header row
    header_row = pyrtf.TableRow()
    header_row.append(pyrtf.Cell(pyrtf.Paragraph(pyrtf.Text("Name", bold=True))))
    header_row.append(pyrtf.Cell(pyrtf.Paragraph(pyrtf.Text("Age", bold=True))))
    header_row.append(pyrtf.Cell(pyrtf.Paragraph(pyrtf.Text("City", bold=True))))
    table.append(header_row)
    
    # Add data rows
    for person in db(db.persons).select():
        row = pyrtf.TableRow()
        row.append(pyrtf.Cell(pyrtf.Paragraph(pyrtf.Text(person.name))))
        row.append(pyrtf.Cell(pyrtf.Paragraph(pyrtf.Text(str(person.age)))))
        row.append(pyrtf.Cell(pyrtf.Paragraph(pyrtf.Text(person.city))))
        table.append(row)
    
    section.append(table)
    return pyrtf.dumps(doc)
```

## Advanced Features

### Custom Styles
```python
def create_styled_document():
    from gluon.contrib import pyrtf
    
    # Create document
    doc = pyrtf.Document()
    
    # Define custom styles
    heading_style = pyrtf.ParagraphStyle('Heading1',
                                        font_size=18,
                                        bold=True,
                                        space_after=240)
    
    body_style = pyrtf.ParagraphStyle('Body',
                                     font_size=12,
                                     space_after=120)
    
    # Add styles to document
    doc.StyleSheet.append(heading_style)
    doc.StyleSheet.append(body_style)
    
    # Use styles in content
    section = pyrtf.Section()
    
    # Heading with style
    heading = pyrtf.Paragraph(heading_style)
    heading.append(pyrtf.Text("Chapter 1"))
    section.append(heading)
    
    # Body text with style
    body = pyrtf.Paragraph(body_style)
    body.append(pyrtf.Text("This is the chapter content..."))
    section.append(body)
    
    doc.Sections.append(section)
    return pyrtf.dumps(doc)
```

### Header and Footer
```python
def document_with_header_footer():
    from gluon.contrib import pyrtf
    
    doc = pyrtf.Document()
    section = pyrtf.Section()
    
    # Add header
    header = pyrtf.HeaderFooter()
    header_p = pyrtf.Paragraph()
    header_p.append(pyrtf.Text("Company Name - Confidential"))
    header.append(header_p)
    section.Header = header
    
    # Add footer with page numbers
    footer = pyrtf.HeaderFooter()
    footer_p = pyrtf.Paragraph()
    footer_p.append(pyrtf.Text("Page "))
    footer_p.append(pyrtf.PageNumber())
    footer.append(footer_p)
    section.Footer = footer
    
    # Add content
    content = pyrtf.Paragraph()
    content.append(pyrtf.Text("Document content goes here..."))
    section.append(content)
    
    doc.Sections.append(section)
    return pyrtf.dumps(doc)
```

## Integration Patterns

### Database Report Generation
```python
def generate_database_report(table_name, query_conditions=None):
    from gluon.contrib import pyrtf
    
    # Query database
    query = db[table_name].id > 0
    if query_conditions:
        query &= query_conditions
    
    records = db(query).select()
    
    # Create document
    doc = pyrtf.Document()
    section = pyrtf.Section()
    doc.Sections.append(section)
    
    # Title
    title = pyrtf.Paragraph()
    title.append(pyrtf.Text(f"{table_name.title()} Report", 
                           font_size=20, bold=True))
    section.append(title)
    
    # Records table
    if records:
        table = pyrtf.Table()
        
        # Header row with field names
        header_row = pyrtf.TableRow()
        for field in records[0]:
            cell = pyrtf.Cell(pyrtf.Paragraph(pyrtf.Text(field, bold=True)))
            header_row.append(cell)
        table.append(header_row)
        
        # Data rows
        for record in records:
            row = pyrtf.TableRow()
            for field in record:
                cell_text = str(record[field]) if record[field] is not None else ""
                cell = pyrtf.Cell(pyrtf.Paragraph(pyrtf.Text(cell_text)))
                row.append(cell)
            table.append(row)
        
        section.append(table)
    
    return pyrtf.dumps(doc)
```

### Form-Based Document Generation
```python
def generate_form_document():
    form = FORM(
        TABLE(
            TR("Document Title:", INPUT(_name="title", requires=IS_NOT_EMPTY())),
            TR("Content:", TEXTAREA(_name="content", requires=IS_NOT_EMPTY())),
            TR("Include Header:", INPUT(_type="checkbox", _name="include_header")),
            TR("", INPUT(_type="submit", _value="Generate RTF"))
        )
    )
    
    if form.process().accepted:
        from gluon.contrib import pyrtf
        
        doc = pyrtf.Document()
        section = pyrtf.Section()
        doc.Sections.append(section)
        
        # Add header if requested
        if form.vars.include_header:
            header = pyrtf.HeaderFooter()
            header_p = pyrtf.Paragraph()
            header_p.append(pyrtf.Text("Generated Document"))
            header.append(header_p)
            section.Header = header
        
        # Add title
        title = pyrtf.Paragraph()
        title.append(pyrtf.Text(form.vars.title, font_size=18, bold=True))
        section.append(title)
        
        # Add content
        content = pyrtf.Paragraph()
        content.append(pyrtf.Text(form.vars.content))
        section.append(content)
        
        # Generate and download
        rtf_content = pyrtf.dumps(doc)
        
        response.headers['Content-Type'] = 'application/rtf'
        response.headers['Content-Disposition'] = 'attachment; filename=document.rtf'
        
        return rtf_content
    
    return dict(form=form)
```

## Output and Compatibility

### RTF Output
The generated RTF is compatible with:
- **Microsoft Word** (all versions)
- **LibreOffice Writer**
- **Apache OpenOffice Writer**
- **WordPad**
- **Other RTF-compatible applications**

### File Handling
```python
def save_rtf_file(doc, filename):
    rtf_content = pyrtf.dumps(doc)
    
    # Save to file
    with open(filename, 'wb') as f:
        if isinstance(rtf_content, str):
            f.write(rtf_content.encode('utf-8'))
        else:
            f.write(rtf_content)
```

## Best Practices

### Performance
1. **Reuse objects**: Create style objects once and reuse them
2. **Batch operations**: Add multiple elements before rendering
3. **Memory management**: Process large documents in sections

### Formatting
1. **Consistent styles**: Use style sheets for consistent formatting
2. **Proper structure**: Use proper document hierarchy
3. **Valid content**: Ensure all text content is properly encoded

### Error Handling
```python
def safe_rtf_generation(content_generator):
    try:
        doc = content_generator()
        return pyrtf.dumps(doc)
    except Exception as e:
        logger.error(f"RTF generation failed: {str(e)}")
        # Return simple fallback document
        doc = pyrtf.Document()
        section = pyrtf.Section()
        error_p = pyrtf.Paragraph()
        error_p.append(pyrtf.Text("Error generating document"))
        section.append(error_p)
        doc.Sections.append(section)
        return pyrtf.dumps(doc)
```

This package provides comprehensive RTF document generation capabilities for Web2py applications, enabling the creation of professional formatted documents for reports, letters, forms, and other business documentation needs.