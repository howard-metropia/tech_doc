# Gluon Contrib PDF Invoice Module

## Overview
PDF invoice generation module for web2py applications using ReportLab. Provides a complete solution for creating professional invoices with customizable layouts, company branding, and itemized billing.

## Module Information
- **Module**: `gluon.contrib.pdfinvoice`
- **Author**: Massimo Di Pierro
- **License**: BSD
- **Dependencies**: ReportLab, cStringIO, datetime, decimal
- **Purpose**: Professional invoice PDF generation

## Key Features
- **Professional Layout**: Pre-designed invoice template
- **Company Branding**: Logo and business details support
- **Multi-page Support**: Automatic pagination for large invoices
- **Currency Formatting**: Automatic currency formatting with thousands separators
- **Itemized Billing**: Support for detailed line items with calculations
- **Customizable**: Configurable fonts, sizes, and layouts

## Main Class

### PDF
Primary class for generating invoice PDFs.

**Constructor:**
```python
def __init__(self, page_size=A4, font_face='Helvetica')
```

**Parameters:**
- `page_size`: Page size (default: A4)
- `font_face`: Font family (default: 'Helvetica')

## Core Methods

### draw()
Generate PDF invoice from invoice data structure.

**Signature:**
```python
def draw(self, invoice, items_page=10)
```

**Parameters:**
- `invoice`: Invoice data dictionary
- `items_page`: Items per page (default: 10)

**Returns:**
- PDF content as string

## Invoice Data Structure

### Required Fields
```python
invoice = {
    'title': 'INVOICE',
    'id': 'INV-001',
    'date': datetime.date.today(),
    'from': 'Company Name\nAddress Line 1\nCity, State ZIP',
    'to': 'Customer Name\nCustomer Address\nCity, State ZIP',
    'items': [
        {
            'description': 'Product/Service Description',
            'quantity': 2,
            'unit_price': 100.00,
            'total': 200.00
        }
    ],
    'subtotal': 200.00,
    'tax_rate': 0.08,
    'tax_amount': 16.00,
    'total': 216.00,
    'notes': 'Payment terms and conditions'
}
```

## Usage Examples

### Basic Invoice Generation
```python
from gluon.contrib.pdfinvoice import PDF
import datetime

# Create PDF generator
pdf_generator = PDF()

# Define invoice data
invoice_data = {
    'title': 'INVOICE',
    'id': 'INV-2023-001',
    'date': datetime.date.today(),
    'from': 'Your Company\n123 Business St\nCity, ST 12345\nPhone: (555) 123-4567',
    'to': 'Customer Corp\n456 Client Ave\nTown, ST 67890',
    'items': [
        {
            'description': 'Web Development Services',
            'quantity': 40,
            'unit_price': 75.00,
            'total': 3000.00
        },
        {
            'description': 'Hosting Setup',
            'quantity': 1,
            'unit_price': 200.00,
            'total': 200.00
        }
    ],
    'subtotal': 3200.00,
    'tax_rate': 0.08,
    'tax_amount': 256.00,
    'total': 3456.00,
    'notes': 'Payment due within 30 days\nThank you for your business!'
}

# Generate PDF
pdf_content = pdf_generator.draw(invoice_data)

# Save to file
with open('invoice.pdf', 'wb') as f:
    f.write(pdf_content)
```

### Web2py Controller Integration
```python
def generate_invoice():
    """Generate PDF invoice for order"""
    order_id = request.args(0) or redirect(URL('orders'))
    
    # Get order data
    order = db.orders[order_id] or redirect(URL('orders'))
    order_items = db(db.order_items.order_id == order_id).select()
    
    # Calculate totals
    subtotal = sum(item.quantity * item.unit_price for item in order_items)
    tax_amount = subtotal * 0.08  # 8% tax
    total = subtotal + tax_amount
    
    # Build invoice data
    invoice_data = {
        'title': 'INVOICE',
        'id': f'INV-{order.id:06d}',
        'date': order.created_on.date(),
        'from': '\n'.join([
            current.app_config.company_name,
            current.app_config.company_address,
            current.app_config.company_phone
        ]),
        'to': '\n'.join([
            f"{order.customer_name}",
            order.billing_address,
            f"{order.billing_city}, {order.billing_state} {order.billing_zip}"
        ]),
        'items': [
            {
                'description': item.product_name,
                'quantity': item.quantity,
                'unit_price': float(item.unit_price),
                'total': float(item.quantity * item.unit_price)
            } for item in order_items
        ],
        'subtotal': float(subtotal),
        'tax_rate': 0.08,
        'tax_amount': float(tax_amount),
        'total': float(total),
        'notes': 'Payment due within 30 days\nThank you for your business!'
    }
    
    # Generate PDF
    pdf_generator = PDF()
    pdf_content = pdf_generator.draw(invoice_data)
    
    # Set response headers
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'
    
    return pdf_content
```

### Custom Branding
```python
def create_branded_invoice():
    """Create invoice with company logo"""
    
    # Initialize PDF with custom settings
    pdf_generator = PDF(font_face='Times-Roman')
    
    # Add company logo
    pdf_generator.logo = 'path/to/company_logo.png'
    
    # Invoice data with enhanced branding
    invoice_data = {
        'title': 'PROFESSIONAL INVOICE',
        'id': 'INV-PRO-001',
        'from': 'Premium Services Inc.\nSuite 100\n123 Executive Blvd\nBusiness City, BC 12345\nTel: (555) 123-4567\nEmail: billing@premiumservices.com',
        'to': 'Valued Customer\nCustomer Address',
        'items': [
            {
                'description': 'Premium Consultation Services',
                'quantity': 1,
                'unit_price': 500.00,
                'total': 500.00
            }
        ],
        'subtotal': 500.00,
        'tax_amount': 40.00,
        'total': 540.00,
        'notes': 'Terms: Net 15 days\nLate payment fee: 1.5% per month\nThank you for choosing Premium Services!'
    }
    
    return pdf_generator.draw(invoice_data)
```

### Bulk Invoice Generation
```python
def generate_monthly_invoices():
    """Generate invoices for all customers with pending orders"""
    
    # Get customers with pending invoices
    customers = db(db.orders.invoice_generated == False).select(
        db.orders.customer_id,
        groupby=db.orders.customer_id
    )
    
    pdf_generator = PDF()
    generated_invoices = []
    
    for customer_record in customers:
        customer_id = customer_record.customer_id
        customer = db.customers[customer_id]
        
        # Get customer orders
        orders = db((db.orders.customer_id == customer_id) & 
                   (db.orders.invoice_generated == False)).select()
        
        for order in orders:
            # Get order items
            items = db(db.order_items.order_id == order.id).select()
            
            # Build invoice data
            invoice_data = build_invoice_data(order, customer, items)
            
            # Generate PDF
            pdf_content = pdf_generator.draw(invoice_data)
            
            # Save PDF file
            filename = f'invoices/invoice_{order.id}.pdf'
            with open(filename, 'wb') as f:
                f.write(pdf_content)
            
            # Mark as generated
            order.update_record(
                invoice_generated=True,
                invoice_file=filename,
                invoice_date=datetime.date.today()
            )
            
            generated_invoices.append(filename)
    
    return generated_invoices
```

## Advanced Features

### Custom Currency Formatting
```python
class CustomPDF(PDF):
    def format_currency(self, value, currency_symbol='$'):
        """Enhanced currency formatting with symbol"""
        formatted = super(CustomPDF, self).format_currency(value)
        return f"{currency_symbol}{formatted}"

# Usage with different currencies
pdf_euro = CustomPDF()
pdf_euro.format_currency = lambda v: CustomPDF.format_currency(pdf_euro, v, '€')
```

### Multi-language Support
```python
def create_multilingual_invoice(language='en'):
    """Create invoice in specified language"""
    
    translations = {
        'en': {
            'title': 'INVOICE',
            'subtotal': 'Subtotal:',
            'tax': 'Tax:',
            'total': 'Total:',
            'notes_header': 'Terms and Conditions:'
        },
        'es': {
            'title': 'FACTURA',
            'subtotal': 'Subtotal:',
            'tax': 'Impuesto:',
            'total': 'Total:',
            'notes_header': 'Términos y Condiciones:'
        }
    }
    
    t = translations.get(language, translations['en'])
    
    invoice_data = {
        'title': t['title'],
        # ... other fields with translations
    }
    
    return PDF().draw(invoice_data)
```

### Integration with Payment Systems
```python
def create_invoice_with_payment_link(order_id):
    """Create invoice with payment integration"""
    
    # Generate invoice
    invoice_data = get_invoice_data(order_id)
    
    # Add payment information
    payment_url = URL('payment', 'process', args=[order_id], scheme=True)
    qr_code_url = generate_qr_code(payment_url)
    
    invoice_data['notes'] += f'\n\nPay online: {payment_url}\nOr scan QR code for quick payment'
    
    # Generate PDF with payment info
    pdf_generator = PDF()
    return pdf_generator.draw(invoice_data)
```

## Error Handling

### Validation and Error Handling
```python
def safe_invoice_generation(invoice_data):
    """Generate invoice with error handling"""
    
    try:
        # Validate required fields
        required_fields = ['title', 'id', 'from', 'to', 'items']
        for field in required_fields:
            if field not in invoice_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate items
        if not invoice_data['items']:
            raise ValueError("Invoice must contain at least one item")
        
        for item in invoice_data['items']:
            if 'description' not in item or 'total' not in item:
                raise ValueError("Invalid item structure")
        
        # Generate PDF
        pdf_generator = PDF()
        return True, pdf_generator.draw(invoice_data)
    
    except Exception as e:
        logger.error(f"Invoice generation failed: {str(e)}")
        return False, str(e)

# Usage
success, result = safe_invoice_generation(invoice_data)
if success:
    # Save PDF
    with open('invoice.pdf', 'wb') as f:
        f.write(result)
else:
    # Handle error
    print(f"Error: {result}")
```

This module provides comprehensive PDF invoice generation capabilities for web2py applications, supporting professional layouts, customization, and integration with business workflows.