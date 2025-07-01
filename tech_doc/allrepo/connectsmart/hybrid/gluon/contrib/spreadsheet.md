# Gluon Contrib Spreadsheet Module

## Overview
Spreadsheet generation and manipulation utilities for web2py applications. Provides functionality to create Excel-compatible spreadsheets, read existing files, and export data in various spreadsheet formats.

## Module Information
- **Module**: `gluon.contrib.spreadsheet`
- **Purpose**: Spreadsheet file operations
- **Formats**: Excel, CSV, OpenDocument
- **Integration**: Web2py data export/import

## Key Features
- **Multiple Formats**: Excel (.xlsx), CSV, OpenDocument support
- **Data Export**: Database to spreadsheet export
- **Data Import**: Spreadsheet to database import
- **Formatting**: Cell styling and formatting
- **Large Data**: Efficient handling of large datasets

## Basic Usage

### Excel Export
```python
from gluon.contrib.spreadsheet import ExcelWriter

def export_users():
    """Export users to Excel file"""
    
    # Get user data
    users = db(db.users).select()
    
    # Create Excel writer
    writer = ExcelWriter()
    
    # Add headers
    headers = ['ID', 'Name', 'Email', 'Created']
    writer.write_row(headers)
    
    # Add data rows
    for user in users:
        writer.write_row([
            user.id,
            user.name,
            user.email,
            user.created_on.strftime('%Y-%m-%d')
        ])
    
    # Generate file
    excel_content = writer.get_content()
    
    # Set response headers
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = 'attachment; filename="users.xlsx"'
    
    return excel_content
```

### CSV Export
```python
def export_to_csv(table_name, query=None):
    """Generic CSV export function"""
    import csv
    import io
    
    table = db[table_name]
    if query is None:
        query = table
    
    # Get records
    records = db(query).select()
    
    # Create CSV content
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write headers
    headers = [field.name for field in table.fields]
    writer.writerow(headers)
    
    # Write data
    for record in records:
        row = [str(record[field]) for field in headers]
        writer.writerow(row)
    
    csv_content = output.getvalue()
    output.close()
    
    # Set response headers
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename="{table_name}.csv"'
    
    return csv_content
```

### Data Import
```python
def import_from_excel(file_path, table_name):
    """Import data from Excel file"""
    from openpyxl import load_workbook
    
    table = db[table_name]
    workbook = load_workbook(file_path)
    worksheet = workbook.active
    
    # Get headers from first row
    headers = [cell.value for cell in worksheet[1]]
    
    # Import data rows
    imported_count = 0
    errors = []
    
    for row_num, row in enumerate(worksheet.iter_rows(min_row=2), start=2):
        try:
            row_data = {}
            for col_num, cell in enumerate(row):
                if col_num < len(headers):
                    field_name = headers[col_num]
                    if field_name in table.fields:
                        row_data[field_name] = cell.value
            
            # Insert record
            table.insert(**row_data)
            imported_count += 1
            
        except Exception as e:
            errors.append(f"Row {row_num}: {str(e)}")
    
    db.commit()
    
    return {
        'imported': imported_count,
        'errors': errors
    }
```

This module provides comprehensive spreadsheet functionality for web2py applications, enabling data export and import in various formats.