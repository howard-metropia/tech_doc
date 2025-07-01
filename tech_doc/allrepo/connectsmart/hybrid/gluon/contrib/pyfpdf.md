# Gluon Contrib PyFPDF Module

## Overview
PyFPDF library integration for web2py applications. Provides pure Python PDF generation capabilities without external dependencies, offering an alternative to ReportLab for creating PDFs with text, images, and basic graphics.

## Module Information
- **Module**: `gluon.contrib.pyfpdf`
- **License**: LGPL
- **Dependencies**: None (pure Python)
- **Purpose**: Lightweight PDF generation
- **Use Case**: Simple PDF documents, reports, certificates

## Key Features
- **Pure Python**: No external dependencies required
- **Lightweight**: Minimal footprint compared to ReportLab
- **Cross-platform**: Works on all Python-supported platforms
- **Multi-format Support**: PNG, JPEG image embedding
- **Font Support**: TrueType font integration
- **Page Management**: Multi-page documents with headers/footers

## Basic Usage

### Simple PDF Creation
```python
from gluon.contrib.pyfpdf import FPDF

# Create PDF instance
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(40, 10, 'Hello World!')

# Output PDF
pdf_content = pdf.output(dest='S')  # Return as string
```

### Web2py Controller Integration
```python
def generate_report():
    """Generate PDF report using PyFPDF"""
    from gluon.contrib.pyfpdf import FPDF
    
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Monthly Report', 0, 1, 'C')
    pdf.ln(10)
    
    # Content
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Report Date: {datetime.date.today()}', 0, 1)
    
    # Data from database
    records = db(db.sales.created_on >= last_month).select()
    total_sales = sum(record.amount for record in records)
    
    pdf.cell(0, 10, f'Total Sales: ${total_sales:,.2f}', 0, 1)
    pdf.cell(0, 10, f'Number of Transactions: {len(records)}', 0, 1)
    
    # Set response headers
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename="report.pdf"'
    
    return pdf.output(dest='S')
```

## Advanced Features

### Tables and Formatting
```python
def create_invoice_pdf():
    """Create invoice using PyFPDF"""
    from gluon.contrib.pyfpdf import FPDF
    
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(0, 20, 'INVOICE', 0, 1, 'C')
    
    # Invoice details
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Invoice #: INV-001', 0, 1)
    pdf.cell(0, 10, f'Date: {datetime.date.today()}', 0, 1)
    pdf.ln(10)
    
    # Table header
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(80, 10, 'Description', 1, 0, 'C')
    pdf.cell(30, 10, 'Quantity', 1, 0, 'C')
    pdf.cell(30, 10, 'Price', 1, 0, 'C')
    pdf.cell(30, 10, 'Total', 1, 1, 'C')
    
    # Table data
    pdf.set_font('Arial', '', 10)
    items = [
        ('Web Development', 40, 75.00, 3000.00),
        ('Domain Setup', 1, 50.00, 50.00),
        ('Hosting (1 year)', 1, 200.00, 200.00)
    ]
    
    for item in items:
        pdf.cell(80, 10, item[0], 1)
        pdf.cell(30, 10, str(item[1]), 1, 0, 'C')
        pdf.cell(30, 10, f'${item[2]:.2f}', 1, 0, 'R')
        pdf.cell(30, 10, f'${item[3]:.2f}', 1, 1, 'R')
    
    # Total
    pdf.set_font('Arial', 'B', 12)
    total = sum(item[3] for item in items)
    pdf.cell(140, 10, 'Total:', 1, 0, 'R')
    pdf.cell(30, 10, f'${total:.2f}', 1, 1, 'R')
    
    return pdf.output(dest='S')
```

### Images and Graphics
```python
def create_certificate():
    """Create certificate with images"""
    from gluon.contrib.pyfpdf import FPDF
    
    pdf = FPDF('L', 'mm', 'A4')  # Landscape orientation
    pdf.add_page()
    
    # Background or logo
    if os.path.exists('static/images/certificate_bg.jpg'):
        pdf.image('static/images/certificate_bg.jpg', 0, 0, 297, 210)
    
    # Certificate title
    pdf.set_font('Arial', 'B', 24)
    pdf.set_text_color(0, 0, 100)
    pdf.cell(0, 50, 'CERTIFICATE OF COMPLETION', 0, 1, 'C')
    
    # Recipient name
    pdf.set_font('Arial', 'B', 18)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 20, 'This certifies that', 0, 1, 'C')
    
    pdf.set_font('Arial', 'B', 20)
    pdf.set_text_color(100, 0, 0)
    pdf.cell(0, 20, 'John Doe', 0, 1, 'C')
    
    # Course details
    pdf.set_font('Arial', '', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 20, 'has successfully completed the course', 0, 1, 'C')
    pdf.cell(0, 20, 'Web Development Fundamentals', 0, 1, 'C')
    
    # Date
    pdf.cell(0, 30, f'Date: {datetime.date.today().strftime("%B %d, %Y")}', 0, 1, 'C')
    
    return pdf.output(dest='S')
```

## Font Management

### Custom Fonts
```python
def use_custom_fonts():
    """Use custom TrueType fonts"""
    from gluon.contrib.pyfpdf import FPDF
    
    pdf = FPDF()
    
    # Add custom font
    pdf.add_font('CustomFont', '', 'path/to/custom_font.ttf', uni=True)
    pdf.add_page()
    
    # Use custom font
    pdf.set_font('CustomFont', '', 14)
    pdf.cell(0, 10, 'Text in custom font', 0, 1)
    
    return pdf.output(dest='S')
```

## Batch Processing

### Multiple PDF Generation
```python
def generate_student_reports():
    """Generate individual reports for all students"""
    from gluon.contrib.pyfpdf import FPDF
    
    students = db(db.students).select()
    generated_files = []
    
    for student in students:
        # Create PDF for each student
        pdf = FPDF()
        pdf.add_page()
        
        # Student header
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, f'Student Report: {student.name}', 0, 1, 'C')
        pdf.ln(10)
        
        # Student details
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'Student ID: {student.id}', 0, 1)
        pdf.cell(0, 10, f'Grade: {student.grade}', 0, 1)
        pdf.cell(0, 10, f'Class: {student.class_name}', 0, 1)
        
        # Grades
        grades = db(db.grades.student_id == student.id).select()
        if grades:
            pdf.ln(10)
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Grades:', 0, 1)
            
            pdf.set_font('Arial', '', 10)
            for grade in grades:
                pdf.cell(0, 8, f'{grade.subject}: {grade.score}', 0, 1)
        
        # Save file
        filename = f'reports/student_{student.id}_report.pdf'
        pdf.output(filename, 'F')
        generated_files.append(filename)
    
    return generated_files
```

## Performance Optimization

### Memory Management
```python
def large_document_generation():
    """Handle large documents efficiently"""
    from gluon.contrib.pyfpdf import FPDF
    
    pdf = FPDF()
    
    # Process data in chunks
    page_size = 50
    total_records = db(db.large_table).count()
    
    for offset in range(0, total_records, page_size):
        records = db(db.large_table).select(
            limitby=(offset, offset + page_size)
        )
        
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f'Page {offset//page_size + 1}', 0, 1, 'C')
        
        pdf.set_font('Arial', '', 10)
        for record in records:
            pdf.cell(0, 8, f'{record.name}: {record.value}', 0, 1)
    
    return pdf.output(dest='S')
```

This module provides lightweight PDF generation capabilities for web2py applications when full-featured libraries like ReportLab are not required or available.