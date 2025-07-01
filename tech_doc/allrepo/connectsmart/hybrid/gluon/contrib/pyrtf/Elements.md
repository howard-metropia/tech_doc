# PyRTF Elements Module

**File**: `gluon/contrib/pyrtf/Elements.py`  
**Type**: RTF Document Structure Elements  
**Framework**: Web2py Gluon Framework

## Overview

This module defines the core structural elements that make up RTF documents, including documents, sections, paragraphs, text, tables, and other content elements. It provides the building blocks for creating rich formatted documents.

## Core Element Classes

### Document Class
The root container for an RTF document:

```python
class Document:
    def __init__(self):
        self.Sections = []        # Document sections
        self.StyleSheet = []      # Style definitions
        self.Colours = []         # Color table
        self.Fonts = []          # Font table
        self.ViewKind = None     # View mode
        self.ViewScale = None    # Zoom level
        self.DefaultLanguage = None
```

### Section Class
Represents a document section with its own formatting:

```python
class Section:
    def __init__(self):
        self.Elements = []       # Section content
        self.Header = None       # Section header
        self.Footer = None       # Section footer
        self.FirstHeader = None  # First page header
        self.FirstFooter = None  # First page footer
```

### Paragraph Class
Container for text and inline elements:

```python
class Paragraph:
    def __init__(self, style=None):
        self.Elements = []       # Paragraph content
        self.Style = style       # Paragraph style
        
    def append(self, element):
        self.Elements.append(element)
```

### Text Class
Basic text element with formatting properties:

```python
class Text:
    def __init__(self, text, font=None, font_size=None, 
                 bold=None, italic=None, underline=None, 
                 colour=None, language=None):
        self.Data = text
        self.Properties = TextPropertySet(
            font=font, font_size=font_size,
            bold=bold, italic=italic, underline=underline,
            colour=colour, language=language
        )
```

## Table Elements

### Table Class
Container for table rows:

```python
class Table:
    LEFT = 'left'
    RIGHT = 'right'
    CENTER = 'center'
    
    def __init__(self, alignment=LEFT):
        self.Rows = []
        self.Alignment = alignment
        
    def append(self, row):
        self.Rows.append(row)
```

### TableRow Class
Container for table cells:

```python
class TableRow:
    def __init__(self):
        self.Cells = []
        
    def append(self, cell):
        self.Cells.append(cell)
```

### Cell Class
Individual table cell:

```python
class Cell:
    ALIGN_TOP = 'top'
    ALIGN_CENTER = 'center'
    ALIGN_BOTTOM = 'bottom'
    
    def __init__(self, *elements, **kwargs):
        self.Elements = list(elements)
        self.Properties = CellPropertySet(**kwargs)
```

## Usage Examples

### Basic Document Structure
```python
from gluon.contrib import pyrtf

# Create document
doc = pyrtf.Document()

# Create section
section = pyrtf.Section()
doc.Sections.append(section)

# Create paragraph with text
paragraph = pyrtf.Paragraph()
text = pyrtf.Text("Hello, World!")
paragraph.append(text)
section.append(paragraph)

# Generate RTF
rtf_output = pyrtf.dumps(doc)
```

### Formatted Text Examples
```python
def create_formatted_text():
    from gluon.contrib import pyrtf
    
    doc = pyrtf.Document()
    section = pyrtf.Section()
    doc.Sections.append(section)
    
    # Different text formatting
    paragraph = pyrtf.Paragraph()
    
    # Bold text
    paragraph.append(pyrtf.Text("Bold text", bold=True))
    paragraph.append(pyrtf.Text(" | "))
    
    # Italic text
    paragraph.append(pyrtf.Text("Italic text", italic=True))
    paragraph.append(pyrtf.Text(" | "))
    
    # Underlined text
    paragraph.append(pyrtf.Text("Underlined text", underline=True))
    paragraph.append(pyrtf.Text(" | "))
    
    # Colored text
    paragraph.append(pyrtf.Text("Red text", colour=pyrtf.Colour('Red', 255, 0, 0)))
    paragraph.append(pyrtf.Text(" | "))
    
    # Different font size
    paragraph.append(pyrtf.Text("Large text", font_size=18))
    
    section.append(paragraph)
    return pyrtf.dumps(doc)
```

### Table Creation
```python
def create_data_table():
    from gluon.contrib import pyrtf
    
    doc = pyrtf.Document()
    section = pyrtf.Section()
    doc.Sections.append(section)
    
    # Create table
    table = pyrtf.Table(alignment=pyrtf.Table.CENTER)
    
    # Header row
    header_row = pyrtf.TableRow()
    header_row.append(pyrtf.Cell(
        pyrtf.Paragraph(pyrtf.Text("Name", bold=True))
    ))
    header_row.append(pyrtf.Cell(
        pyrtf.Paragraph(pyrtf.Text("Age", bold=True))
    ))
    header_row.append(pyrtf.Cell(
        pyrtf.Paragraph(pyrtf.Text("Department", bold=True))
    ))
    table.append(header_row)
    
    # Data rows
    employees = [
        ("John Doe", "30", "Engineering"),
        ("Jane Smith", "28", "Marketing"),
        ("Bob Johnson", "35", "Sales")
    ]
    
    for name, age, dept in employees:
        row = pyrtf.TableRow()
        row.append(pyrtf.Cell(pyrtf.Paragraph(pyrtf.Text(name))))
        row.append(pyrtf.Cell(pyrtf.Paragraph(pyrtf.Text(age))))
        row.append(pyrtf.Cell(pyrtf.Paragraph(pyrtf.Text(dept))))
        table.append(row)
    
    section.append(table)
    return pyrtf.dumps(doc)
```

## Advanced Elements

### Headers and Footers
```python
def document_with_headers():
    from gluon.contrib import pyrtf
    
    doc = pyrtf.Document()
    section = pyrtf.Section()
    
    # Create header
    header = pyrtf.HeaderFooter()
    header_paragraph = pyrtf.Paragraph()
    header_paragraph.append(pyrtf.Text("Document Header", bold=True))
    header.append(header_paragraph)
    section.Header = header
    
    # Create footer
    footer = pyrtf.HeaderFooter()
    footer_paragraph = pyrtf.Paragraph()
    footer_paragraph.append(pyrtf.Text("Page "))
    footer_paragraph.append(pyrtf.PageNumber())
    footer_paragraph.append(pyrtf.Text(" - Company Name"))
    footer.append(footer_paragraph)
    section.Footer = footer
    
    # Add content
    content_paragraph = pyrtf.Paragraph()
    content_paragraph.append(pyrtf.Text("This is the main document content."))
    section.append(content_paragraph)
    
    doc.Sections.append(section)
    return pyrtf.dumps(doc)
```

### Complex Table with Cell Formatting
```python
def create_formatted_table():
    from gluon.contrib import pyrtf
    
    doc = pyrtf.Document()
    section = pyrtf.Section()
    doc.Sections.append(section)
    
    # Financial report table
    table = pyrtf.Table()
    
    # Header row with background color
    header_row = pyrtf.TableRow()
    
    # Create cells with background shading
    header_cells = ["Quarter", "Revenue", "Expenses", "Profit"]
    for header_text in header_cells:
        cell = pyrtf.Cell(
            pyrtf.Paragraph(pyrtf.Text(header_text, bold=True)),
            background_colour=pyrtf.Colour('LightGray', 211, 211, 211)
        )
        header_row.append(cell)
    
    table.append(header_row)
    
    # Data rows
    financial_data = [
        ("Q1 2023", "$150,000", "$120,000", "$30,000"),
        ("Q2 2023", "$175,000", "$130,000", "$45,000"),
        ("Q3 2023", "$200,000", "$140,000", "$60,000"),
        ("Q4 2023", "$225,000", "$160,000", "$65,000")
    ]
    
    for quarter, revenue, expenses, profit in financial_data:
        row = pyrtf.TableRow()
        
        # Quarter cell
        row.append(pyrtf.Cell(
            pyrtf.Paragraph(pyrtf.Text(quarter))
        ))
        
        # Revenue cell (green for positive)
        row.append(pyrtf.Cell(
            pyrtf.Paragraph(pyrtf.Text(revenue, 
                          colour=pyrtf.Colour('Green', 0, 128, 0)))
        ))
        
        # Expenses cell (red)
        row.append(pyrtf.Cell(
            pyrtf.Paragraph(pyrtf.Text(expenses,
                          colour=pyrtf.Colour('Red', 128, 0, 0)))
        ))
        
        # Profit cell (bold green)
        row.append(pyrtf.Cell(
            pyrtf.Paragraph(pyrtf.Text(profit, bold=True,
                          colour=pyrtf.Colour('DarkGreen', 0, 100, 0)))
        ))
        
        table.append(row)
    
    section.append(table)
    return pyrtf.dumps(doc)
```

## Integration with Web2py

### Database-Driven Document Generation
```python
def generate_employee_report():
    from gluon.contrib import pyrtf
    
    # Query database
    employees = db(db.employees.active == True).select(
        orderby=db.employees.department|db.employees.last_name
    )
    
    # Create document
    doc = pyrtf.Document()
    section = pyrtf.Section()
    doc.Sections.append(section)
    
    # Title
    title = pyrtf.Paragraph()
    title.append(pyrtf.Text("Employee Directory", font_size=20, bold=True))
    section.append(title)
    
    # Group by department
    current_dept = None
    for employee in employees:
        # Department header
        if employee.department != current_dept:
            current_dept = employee.department
            
            dept_header = pyrtf.Paragraph()
            dept_header.append(pyrtf.Text(f"\n{current_dept}", 
                             font_size=16, bold=True,
                             colour=pyrtf.Colour('Blue', 0, 0, 128)))
            section.append(dept_header)
        
        # Employee info
        emp_para = pyrtf.Paragraph()
        emp_para.append(pyrtf.Text(f"{employee.first_name} {employee.last_name}", 
                      bold=True))
        emp_para.append(pyrtf.Text(f" - {employee.position}"))
        emp_para.append(pyrtf.Text(f" | Email: {employee.email}"))
        emp_para.append(pyrtf.Text(f" | Phone: {employee.phone}"))
        section.append(emp_para)
    
    doc.Sections.append(section)
    return pyrtf.dumps(doc)
```

### Form-Based Document Creation
```python
def create_custom_document():
    form = FORM(
        TABLE(
            TR("Title:", INPUT(_name="title", requires=IS_NOT_EMPTY())),
            TR("Author:", INPUT(_name="author", requires=IS_NOT_EMPTY())),
            TR("Content:", TEXTAREA(_name="content", _rows=10, requires=IS_NOT_EMPTY())),
            TR("Include Table:", INPUT(_type="checkbox", _name="include_table")),
            TR("", INPUT(_type="submit", _value="Generate Document"))
        )
    )
    
    if form.process().accepted:
        from gluon.contrib import pyrtf
        
        doc = pyrtf.Document()
        section = pyrtf.Section()
        doc.Sections.append(section)
        
        # Document header
        header = pyrtf.HeaderFooter()
        header_p = pyrtf.Paragraph()
        header_p.append(pyrtf.Text(f"Author: {form.vars.author}"))
        header.append(header_p)
        section.Header = header
        
        # Title
        title = pyrtf.Paragraph()
        title.append(pyrtf.Text(form.vars.title, font_size=18, bold=True))
        section.append(title)
        
        # Content
        content_lines = form.vars.content.split('\n')
        for line in content_lines:
            if line.strip():
                para = pyrtf.Paragraph()
                para.append(pyrtf.Text(line))
                section.append(para)
        
        # Optional table
        if form.vars.include_table:
            table = pyrtf.Table()
            
            # Sample table
            header_row = pyrtf.TableRow()
            header_row.append(pyrtf.Cell(pyrtf.Paragraph(pyrtf.Text("Item", bold=True))))
            header_row.append(pyrtf.Cell(pyrtf.Paragraph(pyrtf.Text("Description", bold=True))))
            table.append(header_row)
            
            # Add a few sample rows
            for i in range(3):
                row = pyrtf.TableRow()
                row.append(pyrtf.Cell(pyrtf.Paragraph(pyrtf.Text(f"Item {i+1}"))))
                row.append(pyrtf.Cell(pyrtf.Paragraph(pyrtf.Text(f"Description for item {i+1}"))))
                table.append(row)
            
            section.append(table)
        
        doc.Sections.append(section)
        
        # Return RTF content
        rtf_content = pyrtf.dumps(doc)
        response.headers['Content-Type'] = 'application/rtf'
        response.headers['Content-Disposition'] = 'attachment; filename=document.rtf'
        return rtf_content
    
    return dict(form=form)
```

## Element Hierarchy

### Document Structure
```
Document
├── StyleSheet[]
├── Colours[]
├── Fonts[]
└── Sections[]
    ├── Header (HeaderFooter)
    ├── Footer (HeaderFooter)
    └── Elements[]
        ├── Paragraph
        │   └── Elements[] (Text, PageNumber, etc.)
        └── Table
            └── Rows[]
                └── Cells[]
                    └── Elements[] (Paragraphs)
```

### Best Practices

1. **Document Structure**: Always create proper document hierarchy
2. **Resource Management**: Define colors and fonts in document tables
3. **Content Organization**: Use sections to organize content logically
4. **Table Design**: Plan table structure before implementation
5. **Text Formatting**: Apply consistent formatting through styles

This module provides the essential building blocks for creating structured, formatted RTF documents that can be used for reports, letters, forms, and other business documentation in Web2py applications.