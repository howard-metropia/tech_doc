# test_sqlhtml.py

## Overview
This file contains unit tests for web2py's SQLHTML module, which provides automatic HTML form generation from database tables. It tests SQLFORM functionality, table representation, form validation, and database-driven HTML component generation.

## Purpose
- Tests SQLFORM automatic form generation
- Validates SQLTABLE database table representation
- Tests form validation and processing
- Verifies database integration with HTML forms
- Tests custom form widgets and formatting
- Ensures proper CRUD form functionality

## Key Features Tested

### SQLFORM Generation
- **Automatic Forms**: Generate forms from database table definitions
- **Field Types**: Support for all database field types
- **Validation**: Automatic form validation based on field constraints
- **CRUD Operations**: Create, Read, Update, Delete form handling

### SQLTABLE Representation
- **Table Display**: HTML table generation from database records
- **Column Formatting**: Custom column formatting and display
- **Sorting**: Interactive column sorting
- **Pagination**: Large dataset pagination support

### Form Processing
- **Submission Handling**: Form data processing and validation
- **Error Display**: Validation error presentation
- **Success Handling**: Post-submission redirect and messaging
- **File Uploads**: File upload form handling

### Widget System
- **Custom Widgets**: Custom form input widgets
- **Field Representation**: Custom field display formatting
- **Validation Messages**: Custom validation error messages
- **Form Styling**: CSS class and styling integration

## Integration with web2py Framework

### Database Integration
- **DAL Integration**: Seamless Database Abstraction Layer integration
- **Field Types**: Support for all DAL field types and constraints
- **Relationships**: Foreign key and reference field handling
- **Validation**: Database-level validation integration

### Template System
- **Form Rendering**: Integration with web2py template system
- **Custom Templates**: Custom form template support
- **Helper Integration**: Integration with HTML helpers
- **Responsive Design**: Mobile-friendly form generation

### Security Features
- **CSRF Protection**: Cross-Site Request Forgery protection
- **Input Sanitization**: Automatic input sanitization
- **XSS Prevention**: Cross-Site Scripting attack prevention
- **Access Control**: Field-level access control

## Usage Example
```python
from gluon import *
from gluon.sqlhtml import SQLFORM, SQLTABLE

# Database setup
db = DAL('sqlite://example.db')
db.define_table('person',
    Field('name', requires=IS_NOT_EMPTY()),
    Field('email', requires=IS_EMAIL()),
    Field('age', 'integer', requires=IS_INT_IN_RANGE(0, 120))
)

# Create form
form = SQLFORM(db.person)
if form.process().accepted:
    response.flash = 'Person added successfully'
    redirect(URL('index'))
elif form.errors:
    response.flash = 'Please correct the errors'

# Display table
records = db(db.person).select()
table = SQLTABLE(records,
    headers={'person.name': 'Full Name',
             'person.email': 'Email Address'},
    truncate=50,
    _class='table table-striped'
)

# Update form
record = db.person(request.args(0))
form = SQLFORM(db.person, record)
if form.process().accepted:
    response.flash = 'Person updated successfully'
    redirect(URL('index'))
```

This test suite ensures web2py's SQLHTML module provides reliable, secure, and efficient database-driven HTML form generation with comprehensive validation and processing capabilities.