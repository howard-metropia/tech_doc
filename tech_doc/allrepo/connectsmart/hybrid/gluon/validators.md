# Gluon Validators Documentation

## Overview

The `validators.py` module provides a comprehensive input validation system for the Gluon framework by leveraging PyDAL's robust validation infrastructure. It serves as a bridge between Gluon and PyDAL validators, offering a complete suite of validation tools for web applications.

## File Location
`/home/datavan/METROPIA/metro_combine/allrepo/connectsmart/hybrid/gluon/validators.py`

## Dependencies

### Core Dependencies
- **pydal.validators**: Complete validation framework from PyDAL
  - All validator classes and functions
  - Core validation infrastructure
  - Error handling mechanisms
  - Translation support

### Imported Components
```python
from pydal.validators import *
from pydal.validators import (
    ValidationError,    # Exception class for validation failures
    Validator,          # Base validator class
    __all__,           # List of all available validators
    get_digest,        # Hash digest utility function
    simple_hash,       # Simple hashing function
    translate          # Translation function for error messages
)
```

## Core Validation Classes

### Base Validator Class
The foundation class for all validators, providing the interface contract.

```python
class Validator(object):
    def __call__(self, value):
        """
        Validates a value and returns (value, error) tuple
        Args:
            value: The value to validate
        Returns:
            tuple: (processed_value, error_message_or_None)
        """
```

### ValidationError Exception
Custom exception class for validation failures.

```python
class ValidationError(Exception):
    """
    Raised when validation fails
    Contains error message and optional value information
    """
```

## Available Validators

### String Validators

#### IS_ALPHANUMERIC
```python
IS_ALPHANUMERIC(error_message='Enter only letters, numbers, and underscore')
```
- Validates alphanumeric characters plus underscore
- Useful for usernames, identifiers

#### IS_EMAIL
```python
IS_EMAIL(banned=None, forced=None, error_message='Enter a valid email address')
```
- Comprehensive email validation
- Support for banned/forced domains
- RFC-compliant email checking

#### IS_STRONG
```python
IS_STRONG(min=8, max=20, upper=1, lower=1, number=1, special=1, 
          specials='!@#$%^&*()_+-=[]{}|;:,.<>?', 
          error_message='Enter a strong password')
```
- Password strength validation
- Configurable requirements for character types
- Custom special character sets

#### IS_MATCH
```python
IS_MATCH(expression, error_message='Invalid format', extract=False, search=False)
```
- Regular expression validation
- Pattern matching with extraction options
- Search vs full match modes

### Numeric Validators

#### IS_INT_IN_RANGE
```python
IS_INT_IN_RANGE(minimum=None, maximum=None, error_message='Enter an integer between %(min)g and %(max)g')
```
- Integer range validation
- Optional minimum and maximum bounds
- Automatic type conversion

#### IS_FLOAT_IN_RANGE
```python
IS_FLOAT_IN_RANGE(minimum=None, maximum=None, error_message='Enter a number between %(min)g and %(max)g')
```
- Floating-point range validation
- Decimal number support
- Precision handling

#### IS_DECIMAL_IN_RANGE
```python
IS_DECIMAL_IN_RANGE(minimum=None, maximum=None, dot='.', error_message='Enter a number between %(min)g and %(max)g')
```
- Decimal number validation with custom separators
- High-precision numeric validation
- Currency and financial data support

### List and Choice Validators

#### IS_IN_SET
```python
IS_IN_SET(theset, labels=None, error_message='Value not allowed', multiple=False, zero='', sort=False)
```
- Validates value against allowed set
- Support for multiple selections
- Custom labels for display
- Automatic sorting options

#### IS_IN_DB
```python
IS_IN_DB(dbset, field, label=None, error_message='Value not in database', 
         orderby=None, groupby=None, distinct=None, cache=None, left=None, multiple=False, zero='', sort=False)
```
- Database-driven validation
- Foreign key constraint validation
- Custom query parameters
- Caching support for performance

#### IS_NOT_IN_DB
```python
IS_NOT_IN_DB(dbset, field, error_message='Value already in database')
```
- Uniqueness constraint validation
- Prevents duplicate entries
- Database integrity enforcement

### Date and Time Validators

#### IS_DATE
```python
IS_DATE(format='%Y-%m-%d', error_message='Enter date as %(format)s')
```
- Date format validation
- Custom date format support
- Automatic date parsing

#### IS_DATETIME
```python
IS_DATETIME(format='%Y-%m-%d %H:%M:%S', error_message='Enter date and time as %(format)s')
```
- DateTime validation with custom formats
- Timezone handling support
- Comprehensive timestamp validation

#### IS_TIME
```python
IS_TIME(error_message='Enter time as HH:MM:SS')
```
- Time format validation
- 24-hour format support
- Time range validation capabilities

### File and Upload Validators

#### IS_UPLOAD_FILENAME
```python
IS_UPLOAD_FILENAME(filename=None, extension=None, lastdot=True, case=1, error_message='Enter valid filename')
```
- File name validation
- Extension restrictions
- Case sensitivity options
- Security-focused filename checking

#### IS_IMAGE
```python
IS_IMAGE(extensions=('bmp', 'gif', 'jpeg', 'jpg', 'png'), maxsize=(10000, 10000), minsize=(0, 0))
```
- Image file validation
- Format restriction by extension
- Size validation (dimensions)
- Image integrity checking

### Length and Format Validators

#### IS_LENGTH
```python
IS_LENGTH(maxsize=255, minsize=0, error_message='Enter from %(min)g to %(max)g characters')
```
- String length validation
- Minimum and maximum length constraints
- Unicode-aware length calculation

#### IS_SLUG
```python
IS_SLUG(maxlen=80, check=False, error_message='Must be slug')
```
- URL slug validation
- SEO-friendly identifier validation
- Length and character restrictions

#### IS_URL
```python
IS_URL(error_message='Enter a valid URL', allowed_schemes=None, prepend_scheme=None)
```
- URL format validation
- Protocol scheme validation
- Automatic scheme prepending

### Logic and Conditional Validators

#### IS_EMPTY_OR
```python
IS_EMPTY_OR(other, null=None, empty_regex=None)
```
- Conditional validation
- Allow empty values or validate with another validator
- Null value handling

#### IS_NULL_OR
```python
IS_NULL_OR(other)
```
- Allow NULL values or validate with another validator
- Database NULL handling
- Optional field validation

#### IS_LIST_OF
```python
IS_LIST_OF(other=None, minimum=0, maximum=100)
```
- List validation with element validation
- Each list item validated by another validator
- List size constraints

### Security Validators

#### IS_CRYPTED
```python
IS_CRYPTED(key=None, digest_alg='md5', min_length=0, error_message='Too short')
```
- Password hashing validation
- Multiple digest algorithms
- Minimum length requirements

#### CRYPT
```python
CRYPT(key=None, digest_alg='pbkdf2(1000,20,sha512)', min_length=0, error_message='Too short')
```
- Advanced password hashing
- PBKDF2 and other secure algorithms
- Configurable iteration counts

### Utility Functions

#### get_digest
```python
get_digest(algorithm='md5')
```
- Returns hash digest function for specified algorithm
- Support for multiple hashing algorithms
- Cryptographic hash utilities

#### simple_hash
```python
simple_hash(text, key='', digest_alg='md5', salt='')
```
- Simple text hashing with optional salt
- Key-based hashing
- Multiple algorithm support

#### translate
```python
translate(text)
```
- Translation function for error messages
- Internationalization support
- Custom translation backends

## Validation Patterns

### Basic Field Validation
```python
# Single validator
field.requires = IS_NOT_EMPTY()

# Multiple validators (all must pass)
field.requires = [IS_NOT_EMPTY(), IS_EMAIL()]

# Conditional validation
field.requires = IS_EMPTY_OR(IS_EMAIL())
```

### Database Validation
```python
# Foreign key validation
db.article.author.requires = IS_IN_DB(db, 'person.id', '%(name)s')

# Unique constraint
db.person.email.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, 'person.email')]

# Complex database queries
db.order.customer.requires = IS_IN_DB(db(db.customer.active == True), 
                                      'customer.id', '%(name)s - %(company)s')
```

### Form Integration
```python
# In form processing
if form.process().accepted:
    # All validation passed
    pass
elif form.errors:
    # Handle validation errors
    for field, error in form.errors.items():
        print(f"Field {field}: {error}")
```

## Error Message Customization

### Custom Error Messages
```python
# Custom message for single validator
IS_EMAIL(error_message='Please enter a valid email address')

# Formatted error messages with parameters
IS_INT_IN_RANGE(1, 100, error_message='Age must be between %(min)d and %(max)d')

# Multi-language error messages
IS_NOT_EMPTY(error_message=T('This field cannot be empty'))
```

### Error Message Translation
```python
# Using translation function
error_message = translate('Enter a valid email address')

# Integration with web2py/gluon T() function
field.requires = IS_EMAIL(error_message=T('Invalid email'))
```

## Performance Considerations

### Validator Optimization
1. **Database Validators**: Use caching for IS_IN_DB validators
2. **Complex Validation**: Consider validator order (fail fast)
3. **Regular Expressions**: Compile patterns for repeated use
4. **File Validation**: Check size before content validation

### Caching Strategies
```python
# Cache database lookups
IS_IN_DB(db, 'category.id', '%(name)s', cache=(cache.ram, 3600))

# Cache validation results for static data
cached_validator = cache.ram('validator_key', 
                           lambda: IS_IN_SET(['a', 'b', 'c']), 
                           time_expire=3600)
```

## Security Best Practices

### Input Sanitization
1. Always validate user input
2. Use appropriate validators for data types
3. Implement length limits to prevent DoS
4. Validate file uploads thoroughly

### Password Security
```python
# Strong password requirements
password_validator = IS_STRONG(min=8, upper=1, lower=1, number=1, special=1)

# Secure password hashing
auth.settings.password_field.requires = CRYPT(key=auth.settings.hmac_key)
```

### SQL Injection Prevention
```python
# Use parameterized validators
IS_IN_DB(db(db.table.field == request.vars.param), 'table.id')

# Avoid string concatenation in validators
# WRONG: IS_IN_DB(db, "table.id", "name='" + unsafe_input + "'")
# RIGHT: IS_IN_DB(db(db.table.name == unsafe_input), 'table.id')
```

## Custom Validator Creation

### Basic Custom Validator
```python
class IS_PHONE_NUMBER:
    def __init__(self, error_message='Enter a valid phone number'):
        self.error_message = error_message
    
    def __call__(self, value):
        import re
        if not value:
            return (value, None)
        
        # Simple phone validation pattern
        pattern = r'^\+?1?-?\.?\s?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$'
        if re.match(pattern, str(value)):
            return (value, None)
        else:
            return (value, self.error_message)
```

### Advanced Custom Validator
```python
class IS_BUSINESS_HOURS:
    def __init__(self, start_time='09:00', end_time='17:00', 
                 error_message='Time must be during business hours'):
        self.start_time = start_time
        self.end_time = end_time
        self.error_message = error_message
    
    def __call__(self, value):
        from datetime import datetime
        try:
            time_obj = datetime.strptime(str(value), '%H:%M').time()
            start = datetime.strptime(self.start_time, '%H:%M').time()
            end = datetime.strptime(self.end_time, '%H:%M').time()
            
            if start <= time_obj <= end:
                return (value, None)
            else:
                return (value, self.error_message % {'start': self.start_time, 'end': self.end_time})
        except ValueError:
            return (value, 'Invalid time format')
```

## Integration Examples

### Model Integration
```python
# In models/db.py
db.define_table('user',
    Field('name', requires=IS_NOT_EMPTY()),
    Field('email', requires=[IS_NOT_EMPTY(), IS_EMAIL(), IS_NOT_IN_DB(db, 'user.email')]),
    Field('age', 'integer', requires=IS_INT_IN_RANGE(13, 120)),
    Field('website', requires=IS_EMPTY_OR(IS_URL())),
    Field('avatar', 'upload', requires=IS_EMPTY_OR(IS_IMAGE()))
)
```

### Controller Usage
```python
# In controllers
def register():
    form = SQLFORM(db.user)
    if form.process().accepted:
        response.flash = 'Registration successful'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Please correct the errors'
    return dict(form=form)
```

## Troubleshooting

### Common Issues
1. **Validation not triggering**: Check validator assignment to field.requires
2. **Error messages not displaying**: Verify error handling in views
3. **Performance issues**: Consider caching for database validators
4. **Custom validators failing**: Ensure proper tuple return format

### Debugging Techniques
```python
# Test validator directly
validator = IS_EMAIL()
result, error = validator('test@example.com')
print(f"Result: {result}, Error: {error}")

# Check validator chain
for validator in field.requires:
    result, error = validator(test_value)
    if error:
        print(f"Validator {validator.__class__.__name__} failed: {error}")
```

This validation system provides comprehensive, secure, and flexible input validation capabilities essential for robust web application development in the Gluon framework.