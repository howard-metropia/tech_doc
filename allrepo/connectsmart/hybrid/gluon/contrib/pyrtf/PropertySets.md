# PyRTF PropertySets Module

**File**: `gluon/contrib/pyrtf/PropertySets.py`  
**Type**: RTF Formatting Properties  
**Framework**: Web2py Gluon Framework

## Overview

This module defines property sets that control the formatting and appearance of RTF document elements. It provides classes for managing text properties, paragraph formatting, page layout, table formatting, and other style attributes.

## Core Property Classes

### TextPropertySet Class
Controls text-level formatting properties:

```python
class TextPropertySet:
    def __init__(self, font=None, font_size=None, bold=None, 
                 italic=None, underline=None, colour=None, 
                 language=None, background_colour=None):
        self.Font = font
        self.FontSize = font_size
        self.Bold = bold
        self.Italic = italic
        self.Underline = underline
        self.Colour = colour
        self.Language = language
        self.BackgroundColour = background_colour
```

### ParagraphPropertySet Class
Controls paragraph-level formatting:

```python
class ParagraphPropertySet:
    LEFT = 'left'
    RIGHT = 'right'
    CENTER = 'center'
    JUSTIFY = 'justify'
    DISTRIBUTE = 'distribute'
    
    def __init__(self, alignment=None, first_line_indent=None,
                 left_indent=None, right_indent=None,
                 space_before=None, space_after=None,
                 line_spacing=None):
        self.Alignment = alignment
        self.FirstLineIndent = first_line_indent
        self.LeftIndent = left_indent
        self.RightIndent = right_indent
        self.SpaceBefore = space_before
        self.SpaceAfter = space_after
        self.LineSpacing = line_spacing
```

### PagePropertySet Class
Controls page layout and margins:

```python
class PagePropertySet:
    def __init__(self, width=None, height=None,
                 top_margin=None, bottom_margin=None,
                 left_margin=None, right_margin=None,
                 header_distance=None, footer_distance=None):
        self.Width = width
        self.Height = height
        self.TopMargin = top_margin
        self.BottomMargin = bottom_margin
        self.LeftMargin = left_margin
        self.RightMargin = right_margin
        self.HeaderDistance = header_distance
        self.FooterDistance = footer_distance
```

## Color and Font Management

### Colour Class
Defines colors for text and backgrounds:

```python
class Colour:
    def __init__(self, name, red, green, blue):
        self.Name = name
        self.Red = red      # 0-255
        self.Green = green  # 0-255
        self.Blue = blue    # 0-255
```

### Font Class
Defines font properties:

```python
class Font:
    def __init__(self, name, family=None, character_set=None):
        self.Name = name
        self.Family = family
        self.CharacterSet = character_set
```

## Usage Examples

### Text Formatting
```python
from gluon.contrib import pyrtf

def create_formatted_text():
    doc = pyrtf.Document()
    section = pyrtf.Section()
    doc.Sections.append(section)
    
    # Define text properties
    bold_props = pyrtf.TextPropertySet(bold=True, font_size=14)
    italic_props = pyrtf.TextPropertySet(italic=True, 
                                        colour=pyrtf.Colour('Blue', 0, 0, 255))
    
    # Create paragraph with mixed formatting
    paragraph = pyrtf.Paragraph()
    
    # Add formatted text
    paragraph.append(pyrtf.Text("Bold Title", properties=bold_props))
    paragraph.append(pyrtf.Text(" and "))
    paragraph.append(pyrtf.Text("italic subtitle", properties=italic_props))
    
    section.append(paragraph)
    return pyrtf.dumps(doc)
```

### Paragraph Formatting
```python
def create_formatted_paragraphs():
    from gluon.contrib import pyrtf
    
    doc = pyrtf.Document()
    section = pyrtf.Section()
    doc.Sections.append(section)
    
    # Center-aligned paragraph
    center_props = pyrtf.ParagraphPropertySet(
        alignment=pyrtf.ParagraphPropertySet.CENTER,
        space_after=240  # 240 twips = 12 points
    )
    
    title_paragraph = pyrtf.Paragraph(properties=center_props)
    title_paragraph.append(pyrtf.Text("Centered Title", bold=True, font_size=18))
    section.append(title_paragraph)
    
    # Justified paragraph with indentation
    body_props = pyrtf.ParagraphPropertySet(
        alignment=pyrtf.ParagraphPropertySet.JUSTIFY,
        first_line_indent=360,  # 360 twips = 0.25 inch
        left_indent=720,        # 720 twips = 0.5 inch
        right_indent=720,
        space_before=120,
        space_after=120,
        line_spacing=1.5
    )
    
    body_paragraph = pyrtf.Paragraph(properties=body_props)
    body_paragraph.append(pyrtf.Text(
        "This is a justified paragraph with custom indentation and spacing. "
        "The first line is indented, and there's space before and after the paragraph."
    ))
    section.append(body_paragraph)
    
    return pyrtf.dumps(doc)
```

### Page Layout Configuration
```python
def create_custom_page_layout():
    from gluon.contrib import pyrtf
    
    doc = pyrtf.Document()
    
    # Custom page properties (letter size with custom margins)
    page_props = pyrtf.PagePropertySet(
        width=12240,      # 8.5 inches * 1440 twips/inch
        height=15840,     # 11 inches * 1440 twips/inch
        top_margin=1440,  # 1 inch
        bottom_margin=1440,
        left_margin=1080, # 0.75 inch
        right_margin=1080,
        header_distance=720,  # 0.5 inch
        footer_distance=720
    )
    
    section = pyrtf.Section(properties=page_props)
    
    # Add content
    paragraph = pyrtf.Paragraph()
    paragraph.append(pyrtf.Text("Content with custom page layout"))
    section.append(paragraph)
    
    doc.Sections.append(section)
    return pyrtf.dumps(doc)
```

## Table and Cell Properties

### TablePropertySet Class
```python
class TablePropertySet:
    def __init__(self, alignment=None, width=None):
        self.Alignment = alignment
        self.Width = width
```

### CellPropertySet Class
```python
class CellPropertySet:
    def __init__(self, width=None, background_colour=None,
                 vertical_alignment=None, padding=None):
        self.Width = width
        self.BackgroundColour = background_colour
        self.VerticalAlignment = vertical_alignment
        self.Padding = padding
```

### Table Formatting Example
```python
def create_formatted_table():
    from gluon.contrib import pyrtf
    
    doc = pyrtf.Document()
    section = pyrtf.Section()
    doc.Sections.append(section)
    
    # Define table properties
    table_props = pyrtf.TablePropertySet(
        alignment=pyrtf.Table.CENTER,
        width=8000  # Total table width in twips
    )
    
    table = pyrtf.Table(properties=table_props)
    
    # Header row with special formatting
    header_row = pyrtf.TableRow()
    
    # Define cell properties for headers
    header_cell_props = pyrtf.CellPropertySet(
        background_colour=pyrtf.Colour('HeaderGray', 200, 200, 200),
        vertical_alignment=pyrtf.Cell.ALIGN_CENTER,
        padding=120  # 6 points padding
    )
    
    headers = ["Product", "Price", "Quantity", "Total"]
    for header_text in headers:
        cell = pyrtf.Cell(properties=header_cell_props)
        header_para = pyrtf.Paragraph()
        header_para.append(pyrtf.Text(header_text, bold=True))
        cell.append(header_para)
        header_row.append(cell)
    
    table.append(header_row)
    
    # Data rows
    products = [
        ("Widget A", "$10.00", "5", "$50.00"),
        ("Widget B", "$15.00", "3", "$45.00"),
        ("Widget C", "$8.00", "10", "$80.00")
    ]
    
    for product, price, qty, total in products:
        row = pyrtf.TableRow()
        
        # Product name cell
        product_cell = pyrtf.Cell()
        product_para = pyrtf.Paragraph()
        product_para.append(pyrtf.Text(product))
        product_cell.append(product_para)
        row.append(product_cell)
        
        # Price cell (right-aligned)
        price_props = pyrtf.ParagraphPropertySet(
            alignment=pyrtf.ParagraphPropertySet.RIGHT
        )
        price_cell = pyrtf.Cell()
        price_para = pyrtf.Paragraph(properties=price_props)
        price_para.append(pyrtf.Text(price))
        price_cell.append(price_para)
        row.append(price_cell)
        
        # Quantity cell (center-aligned)
        qty_props = pyrtf.ParagraphPropertySet(
            alignment=pyrtf.ParagraphPropertySet.CENTER
        )
        qty_cell = pyrtf.Cell()
        qty_para = pyrtf.Paragraph(properties=qty_props)
        qty_para.append(pyrtf.Text(qty))
        qty_cell.append(qty_para)
        row.append(qty_cell)
        
        # Total cell (right-aligned, bold)
        total_cell = pyrtf.Cell()
        total_para = pyrtf.Paragraph(properties=price_props)
        total_para.append(pyrtf.Text(total, bold=True))
        total_cell.append(total_para)
        row.append(total_cell)
        
        table.append(row)
    
    section.append(table)
    return pyrtf.dumps(doc)
```

## Integration with Web2py

### Dynamic Style Generation
```python
def create_styled_report(data, style_config=None):
    from gluon.contrib import pyrtf
    
    # Default style configuration
    if not style_config:
        style_config = {
            'title_size': 20,
            'title_color': (0, 0, 128),
            'body_size': 12,
            'body_color': (0, 0, 0),
            'table_header_color': (240, 240, 240)
        }
    
    doc = pyrtf.Document()
    section = pyrtf.Section()
    doc.Sections.append(section)
    
    # Create title style
    title_props = pyrtf.TextPropertySet(
        font_size=style_config['title_size'],
        bold=True,
        colour=pyrtf.Colour('TitleBlue', *style_config['title_color'])
    )
    
    # Create body style
    body_props = pyrtf.TextPropertySet(
        font_size=style_config['body_size'],
        colour=pyrtf.Colour('BodyBlack', *style_config['body_color'])
    )
    
    # Add title
    title_para = pyrtf.Paragraph()
    title_para.append(pyrtf.Text("Data Report", properties=title_props))
    section.append(title_para)
    
    # Add data table
    if data:
        table = pyrtf.Table()
        
        # Create header row
        if data:
            header_row = pyrtf.TableRow()
            for field_name in data[0].keys():
                cell = pyrtf.Cell()
                header_para = pyrtf.Paragraph()
                header_para.append(pyrtf.Text(field_name.title(), bold=True))
                cell.append(header_para)
                header_row.append(cell)
            table.append(header_row)
            
            # Add data rows
            for record in data:
                row = pyrtf.TableRow()
                for value in record.values():
                    cell = pyrtf.Cell()
                    data_para = pyrtf.Paragraph()
                    data_para.append(pyrtf.Text(str(value), properties=body_props))
                    cell.append(data_para)
                    row.append(cell)
                table.append(row)
        
        section.append(table)
    
    doc.Sections.append(section)
    return pyrtf.dumps(doc)
```

### Form-Based Style Configuration
```python
def configurable_document_generator():
    form = FORM(
        TABLE(
            TR("Title Font Size:", INPUT(_name="title_size", _type="number", _value=18)),
            TR("Body Font Size:", INPUT(_name="body_size", _type="number", _value=12)),
            TR("Title Color:", SELECT(
                OPTION("Black", _value="0,0,0"),
                OPTION("Blue", _value="0,0,255"),
                OPTION("Red", _value="255,0,0"),
                OPTION("Green", _value="0,128,0"),
                _name="title_color"
            )),
            TR("Table Style:", SELECT(
                OPTION("Plain", _value="plain"),
                OPTION("Striped", _value="striped"),
                OPTION("Bordered", _value="bordered"),
                _name="table_style"
            )),
            TR("", INPUT(_type="submit", _value="Generate Document"))
        )
    )
    
    if form.process().accepted:
        from gluon.contrib import pyrtf
        
        # Parse form values
        title_size = int(form.vars.title_size or 18)
        body_size = int(form.vars.body_size or 12)
        title_color = tuple(map(int, form.vars.title_color.split(',')))
        
        # Create document with custom styles
        doc = pyrtf.Document()
        section = pyrtf.Section()
        doc.Sections.append(section)
        
        # Apply custom styling
        title_props = pyrtf.TextPropertySet(
            font_size=title_size,
            bold=True,
            colour=pyrtf.Colour('CustomTitle', *title_color)
        )
        
        # Add styled content
        title_para = pyrtf.Paragraph()
        title_para.append(pyrtf.Text("Custom Styled Document", properties=title_props))
        section.append(title_para)
        
        # Generate and return
        rtf_content = pyrtf.dumps(doc)
        response.headers['Content-Type'] = 'application/rtf'
        response.headers['Content-Disposition'] = 'attachment; filename=styled_document.rtf'
        return rtf_content
    
    return dict(form=form)
```

## Measurement Units

### Twips (Twentieths of a Point)
RTF uses "twips" as the basic unit of measurement:
- **1 inch = 1440 twips**
- **1 point = 20 twips**
- **1 cm ≈ 567 twips**

### Common Measurements
```python
# Measurement constants
INCH = 1440
POINT = 20
CM = 567

# Common margins
MARGIN_NARROW = INCH * 0.5      # 0.5 inch
MARGIN_NORMAL = INCH            # 1 inch  
MARGIN_WIDE = INCH * 1.25       # 1.25 inches

# Common font sizes
FONT_SMALL = 10 * POINT         # 10 point
FONT_NORMAL = 12 * POINT        # 12 point
FONT_LARGE = 14 * POINT         # 14 point
FONT_TITLE = 18 * POINT         # 18 point
```

## Best Practices

### Property Management
1. **Consistent Styling**: Define standard property sets and reuse them
2. **Measurement Units**: Use constants for common measurements
3. **Color Management**: Define colors once and reference them
4. **Performance**: Create property objects once and reuse them

### Formatting Guidelines
1. **Readability**: Use appropriate font sizes and line spacing
2. **Consistency**: Maintain consistent margins and indentation
3. **Hierarchy**: Use different font sizes to create visual hierarchy
4. **Accessibility**: Ensure sufficient color contrast

This module provides comprehensive formatting control for RTF documents, enabling precise styling and professional document appearance in Web2py applications.