# PyRTF Renderer Module

**File**: `gluon/contrib/pyrtf/Renderer.py`  
**Type**: RTF Output Generation Engine  
**Framework**: Web2py Gluon Framework

## Overview

This module contains the rendering engine that converts PyRTF document objects into actual RTF (Rich Text Format) output. It handles the serialization of document elements, formatting properties, and structural components into the RTF specification format.

## Core Rendering Components

### Renderer Class
The main class responsible for RTF output generation:

```python
class Renderer:
    def __init__(self):
        self.output = None
        self.tab_width = DEFAULT_TAB_WIDTH
        
    def Write(self, document, output_stream):
        """Write document to RTF format"""
        self.output = output_stream
        self._write_document(document)
```

### Mapping Constants
The module defines mappings between PyRTF objects and RTF control codes:

```python
# Paragraph alignment mappings
ParagraphAlignmentMap = {
    ParagraphPropertySet.LEFT: 'ql',
    ParagraphPropertySet.RIGHT: 'qr',
    ParagraphPropertySet.CENTER: 'qc',
    ParagraphPropertySet.JUSTIFY: 'qj',
    ParagraphPropertySet.DISTRIBUTE: 'qd'
}

# Tab alignment mappings
TabAlignmentMap = {
    TabPropertySet.LEFT: '',
    TabPropertySet.RIGHT: 'tqr',
    TabPropertySet.CENTER: 'tqc',
    TabPropertySet.DECIMAL: 'tqdec'
}

# Table alignment mappings
TableAlignmentMap = {
    Table.LEFT: 'trql',
    Table.RIGHT: 'trqr',
    Table.CENTER: 'trqc'
}

# Cell alignment mappings
CellAlignmentMap = {
    Cell.ALIGN_TOP: '',
    Cell.ALIGN_CENTER: 'clvertalc',
    Cell.ALIGN_BOTTOM: 'clvertalb'
}
```

## RTF Generation Process

### Document Structure Rendering
The renderer processes documents in this hierarchy:

1. **Document Header**: RTF version, font table, color table
2. **Style Sheet**: Paragraph and character styles
3. **Document Properties**: View settings, page layout
4. **Sections**: Document content sections
5. **Headers/Footers**: Page headers and footers
6. **Content**: Paragraphs, tables, text, formatting

### Key Rendering Methods

**_write_document()**
```python
def _write_document(self, document):
    # Write RTF header
    self._write_header()
    
    # Write font table
    self._write_font_table(document.fonts)
    
    # Write color table
    self._write_color_table(document.colors)
    
    # Write style sheet
    self._write_stylesheet(document.stylesheet)
    
    # Write document properties
    self._write_document_properties(document)
    
    # Write sections
    for section in document.sections:
        self._write_section(section)
    
    # Close document
    self._write_footer()
```

## Usage Examples

### Basic Document Rendering
```python
from gluon.contrib import pyrtf

def render_document_to_file(document, filename):
    """Render PyRTF document to file"""
    with open(filename, 'wb') as f:
        renderer = pyrtf.Renderer()
        renderer.Write(document, f)
```

### In-Memory Rendering
```python
def render_document_to_string(document):
    """Render PyRTF document to string"""
    from io import BytesIO
    
    output = BytesIO()
    renderer = pyrtf.Renderer()
    renderer.Write(document, output)
    
    # Get RTF content
    rtf_content = output.getvalue()
    output.close()
    
    return rtf_content
```

### Web2py Response Integration
```python
def generate_rtf_response(document, filename="document.rtf"):
    """Generate RTF response for Web2py"""
    from gluon.contrib import pyrtf
    from io import BytesIO
    
    # Render document
    output = BytesIO()
    renderer = pyrtf.Renderer()
    renderer.Write(document, output)
    
    # Set response headers
    response.headers['Content-Type'] = 'application/rtf'
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    
    # Return content
    content = output.getvalue()
    output.close()
    
    return content
```

## Formatting Control

### Text Formatting Rendering
The renderer converts text properties to RTF control words:

```python
# Bold text: \b
# Italic text: \i
# Underline text: \ul
# Font size: \fs24 (12 point = 24 half-points)
# Font color: \cf1 (color table index)
```

### Paragraph Formatting
Paragraph properties are rendered as RTF paragraph controls:

```python
# Left alignment: \ql
# Center alignment: \qc
# Right alignment: \qr
# Justified: \qj
# Left indent: \li720 (in twips)
# First line indent: \fi360 (in twips)
# Space before: \sb240 (in twips)
# Space after: \sa240 (in twips)
```

### Table Rendering
Tables are rendered using RTF table control words:

```python
# Table row start: \trowd
# Cell definition: \cellx2880 (right edge position)
# Cell content: content\cell
# Row end: \row
```

## Advanced Rendering Features

### Custom Renderer Extension
```python
class CustomRenderer(pyrtf.Renderer):
    """Extended renderer with custom formatting"""
    
    def __init__(self, custom_options=None):
        super().__init__()
        self.custom_options = custom_options or {}
    
    def _write_custom_header(self, document):
        """Add custom header information"""
        if self.custom_options.get('add_metadata'):
            # Add custom metadata
            self.output.write(b'{\\info')
            self.output.write(b'{\\title Generated Document}')
            self.output.write(b'{\\author PyRTF Generator}')
            self.output.write(b'{\\company Web2py Application}')
            self.output.write(b'}')
    
    def _write_document(self, document):
        # Call parent method
        super()._write_document(document)
        
        # Add custom processing
        if self.custom_options.get('add_watermark'):
            self._add_watermark()
    
    def _add_watermark(self):
        """Add watermark to document"""
        # RTF watermark implementation
        pass
```

### Conditional Rendering
```python
def render_with_conditions(document, options=None):
    """Render document with conditional formatting"""
    from gluon.contrib import pyrtf
    from io import BytesIO
    
    options = options or {}
    
    # Modify document based on options
    if options.get('grayscale'):
        # Convert colors to grayscale
        for color in document.Colours:
            gray_value = int(0.299 * color.Red + 0.587 * color.Green + 0.114 * color.Blue)
            color.Red = color.Green = color.Blue = gray_value
    
    if options.get('high_contrast'):
        # Increase contrast for accessibility
        for section in document.Sections:
            for element in section.Elements:
                if hasattr(element, 'Properties') and element.Properties:
                    if element.Properties.Colour:
                        # Make text darker
                        color = element.Properties.Colour
                        if color.Red + color.Green + color.Blue > 384:  # Light color
                            color.Red = color.Green = color.Blue = 255  # White
                        else:
                            color.Red = color.Green = color.Blue = 0    # Black
    
    # Render with modifications
    output = BytesIO()
    renderer = pyrtf.Renderer()
    renderer.Write(document, output)
    
    return output.getvalue()
```

## Performance Optimization

### Efficient Rendering
```python
class OptimizedRenderer(pyrtf.Renderer):
    """Performance-optimized renderer"""
    
    def __init__(self, buffer_size=8192):
        super().__init__()
        self.buffer_size = buffer_size
        self.buffer = []
        self.buffer_length = 0
    
    def _write_buffered(self, data):
        """Buffered writing for better performance"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        self.buffer.append(data)
        self.buffer_length += len(data)
        
        if self.buffer_length >= self.buffer_size:
            self._flush_buffer()
    
    def _flush_buffer(self):
        """Flush buffer to output"""
        if self.buffer:
            self.output.write(b''.join(self.buffer))
            self.buffer = []
            self.buffer_length = 0
    
    def Write(self, document, output_stream):
        """Optimized write method"""
        self.output = output_stream
        self._write_document(document)
        self._flush_buffer()  # Ensure all data is written
```

### Large Document Handling
```python
def render_large_document(document_sections, filename):
    """Render large document in chunks"""
    from gluon.contrib import pyrtf
    
    with open(filename, 'wb') as f:
        renderer = pyrtf.Renderer()
        
        # Write document header manually
        f.write(b'{\\rtf1\\ansi\\deff0')
        
        # Write font and color tables
        # (implementation details...)
        
        # Write sections one by one
        for section in document_sections:
            # Create temporary document with single section
            temp_doc = pyrtf.Document()
            temp_doc.Sections = [section]
            
            # Render section to temporary buffer
            from io import BytesIO
            temp_buffer = BytesIO()
            renderer.Write(temp_doc, temp_buffer)
            
            # Extract section content (strip document wrapper)
            section_content = temp_buffer.getvalue()
            # Process and write section content
            f.write(extract_section_content(section_content))
            
            temp_buffer.close()
        
        # Write document footer
        f.write(b'}')
```

## Integration with Web2py

### Controller Integration
```python
def download_rtf_report():
    """Generate and download RTF report"""
    from gluon.contrib import pyrtf
    
    # Get data
    records = db(db.reports.active == True).select()
    
    # Create document
    doc = pyrtf.Document()
    section = pyrtf.Section()
    doc.Sections.append(section)
    
    # Add content
    for record in records:
        para = pyrtf.Paragraph()
        para.append(pyrtf.Text(record.title, bold=True))
        para.append(pyrtf.Text(f"\n{record.content}"))
        section.append(para)
    
    # Render and return
    return generate_rtf_response(doc, "report.rtf")
```

### Streaming Response
```python
def stream_rtf_document():
    """Stream large RTF document"""
    def generate_rtf_stream():
        from gluon.contrib import pyrtf
        from io import BytesIO
        
        # Create document sections dynamically
        for page in range(100):  # Large document
            doc = pyrtf.Document()
            section = pyrtf.Section()
            
            # Add page content
            para = pyrtf.Paragraph()
            para.append(pyrtf.Text(f"Page {page + 1} content..."))
            section.append(para)
            
            doc.Sections.append(section)
            
            # Render section
            output = BytesIO()
            renderer = pyrtf.Renderer()
            renderer.Write(doc, output)
            
            # Yield content chunk
            yield output.getvalue()
            output.close()
    
    # Set streaming response
    response.headers['Content-Type'] = 'application/rtf'
    response.headers['Content-Disposition'] = 'attachment; filename=large_document.rtf'
    
    return response.stream(generate_rtf_stream())
```

## Error Handling

### Robust Rendering
```python
def safe_rtf_render(document, fallback_content="Error generating document"):
    """Safely render RTF with error handling"""
    try:
        from gluon.contrib import pyrtf
        from io import BytesIO
        
        output = BytesIO()
        renderer = pyrtf.Renderer()
        renderer.Write(document, output)
        
        content = output.getvalue()
        output.close()
        
        # Validate RTF content
        if len(content) < 50:  # Suspiciously small
            raise ValueError("Generated RTF appears incomplete")
        
        return content
        
    except Exception as e:
        logger.error(f"RTF rendering failed: {str(e)}")
        
        # Generate fallback document
        fallback_doc = pyrtf.Document()
        section = pyrtf.Section()
        para = pyrtf.Paragraph()
        para.append(pyrtf.Text(fallback_content))
        section.append(para)
        fallback_doc.Sections.append(section)
        
        # Try to render fallback
        try:
            output = BytesIO()
            renderer = pyrtf.Renderer()
            renderer.Write(fallback_doc, output)
            content = output.getvalue()
            output.close()
            return content
        except:
            # Return minimal RTF if all else fails
            return b'{\\rtf1\\ansi Error generating document.}'
```

## Best Practices

### Rendering Guidelines
1. **Memory Management**: Use streaming for large documents
2. **Error Handling**: Always provide fallback content
3. **Performance**: Buffer output for better performance
4. **Validation**: Verify generated RTF content
5. **Encoding**: Handle character encoding properly

### Output Quality
1. **Formatting**: Ensure consistent formatting across elements
2. **Compatibility**: Test with multiple RTF readers
3. **Optimization**: Minimize unnecessary RTF control codes
4. **Structure**: Maintain proper RTF document structure

This module provides the essential rendering capabilities that transform PyRTF document objects into standard RTF format, enabling compatibility with word processors and document viewers while maintaining precise formatting control.