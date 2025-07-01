# validators.py

## Overview
Comprehensive validation framework for PyDAL providing data validation, transformation, and constraint enforcement for database fields and form inputs. Contains 40+ validator classes covering common validation scenarios.

## Core Framework

### ValidationError
```python
class ValidationError(Exception):
    pass
```
Base exception for all validation failures.

### Validator Base Class
```python
class Validator(object):
```
Abstract base class for all validators providing common functionality:

**Key Features:**
- **Translator Support**: Internationalization of error messages
- **Default Error Messages**: Standardized error text
- **Validation Interface**: Common `__call__` method
- **Transformation**: Input value modification capabilities

## String and Pattern Validators

### IS_MATCH
```python
class IS_MATCH(Validator):
    def __init__(self, expression, error_message='Invalid expression', 
                 extract=False, search=False, strict=False, is_unicode=None):
```

**Purpose**: Validates input against regular expression patterns.

**Parameters:**
- **expression**: Regex pattern (string or compiled regex)
- **extract**: Return matched groups instead of boolean
- **search**: Use `re.search()` instead of `re.match()`
- **strict**: Require exact pattern match
- **is_unicode**: Unicode handling mode

**Examples:**
```python
# Phone number validation
IS_MATCH(r'^\d{3}-\d{3}-\d{4}$', error_message='Invalid phone format')

# Extract area code
IS_MATCH(r'^(\d{3})-\d{3}-\d{4}$', extract=True)  # Returns ('555',)
```

### IS_ALPHANUMERIC
```python
class IS_ALPHANUMERIC(IS_MATCH):
```
Validates alphanumeric characters only (inherits from IS_MATCH).

### IS_LENGTH
```python
class IS_LENGTH(Validator):
    def __init__(self, maxsize=255, minsize=0, error_message='Too long'):
```

**Purpose**: Validates string length constraints.

**Features:**
- Minimum and maximum length validation
- Handles Unicode character counting
- Supports None values (bypasses validation)

### IS_NOT_EMPTY
```python
class IS_NOT_EMPTY(Validator):
```
Ensures field has non-empty value (not None, '', [], {}).

## Numeric Validators

### IS_INT_IN_RANGE
```python
class IS_INT_IN_RANGE(Validator):
    def __init__(self, minimum=None, maximum=None, error_message='Too small/large'):
```

**Purpose**: Validates integers within specified range.

**Features:**
- Optional minimum/maximum bounds
- Automatic type conversion to int
- Handles string representations of integers

### IS_FLOAT_IN_RANGE
```python
class IS_FLOAT_IN_RANGE(Validator):
    def __init__(self, minimum=None, maximum=None, error_message='Out of range'):
```

**Purpose**: Validates floating-point numbers within range.

**Features:**
- Decimal precision handling
- Scientific notation support
- Type conversion from strings

### IS_DECIMAL_IN_RANGE
```python
class IS_DECIMAL_IN_RANGE(Validator):
    def __init__(self, minimum=None, maximum=None, precision=(10,2)):
```

**Purpose**: Validates decimal numbers with precision control.

**Features:**
- Fixed-point decimal validation
- Precision specification (digits, decimal places)
- Financial calculation support

## Date and Time Validators

### IS_DATE
```python
class IS_DATE(Validator):
    def __init__(self, format='%Y-%m-%d', error_message='Invalid date'):
```

**Purpose**: Validates and converts date strings.

**Features:**
- Custom date format specification
- Automatic datetime.date conversion
- Locale-aware formatting

### IS_DATETIME
```python
class IS_DATETIME(Validator):
    def __init__(self, format='%Y-%m-%d %H:%M:%S', error_message='Invalid datetime'):
```

**Purpose**: Validates datetime strings with time components.

### IS_TIME
```python
class IS_TIME(Validator):
    def __init__(self, error_message='Invalid time'):
```

**Purpose**: Validates time-only strings (HH:MM:SS format).

### IS_DATE_IN_RANGE / IS_DATETIME_IN_RANGE
Range validators for dates with minimum/maximum constraints.

## Email and URL Validators

### IS_EMAIL
```python
class IS_EMAIL(Validator):
    def __init__(self, banned=None, forced=None, error_message='Invalid email'):
```

**Purpose**: Comprehensive email address validation.

**Features:**
- RFC-compliant email validation
- Domain blacklist/whitelist support
- International domain support (IDN)
- Local email detection

**Advanced Options:**
```python
# Banned domains
IS_EMAIL(banned='^.*\\.edu$')

# Force specific domains
IS_EMAIL(forced='^.*@company\\.com$')
```

### IS_LIST_OF_EMAILS
```python
class IS_LIST_OF_EMAILS(Validator):
```
Validates comma-separated list of email addresses.

### IS_URL
```python
class IS_URL(Validator):
    def __init__(self, allowed_schemes=None, prepend_scheme=None):
```

**Purpose**: Validates URL format and scheme.

**Features:**
- Multiple URL scheme support (http, https, ftp, etc.)
- Automatic scheme prepending
- International domain support

## Database Validators

### IS_IN_DB
```python
class IS_IN_DB(Validator):
    def __init__(self, dbset, field, label=None, error_message='Value not found',
                 orderby=None, cache=None, multiple=False, zero=''):
```

**Purpose**: Validates that value exists in database table.

**Key Features:**
- **Foreign Key Validation**: Ensures referential integrity
- **Multiple Selection**: Support for multiple values
- **Custom Labels**: Display different text than stored value
- **Caching**: Performance optimization for repeated queries
- **Ordering**: Control option display order

**Examples:**
```python
# Basic foreign key validation
IS_IN_DB(db, 'user.id')

# With custom labels
IS_IN_DB(db, 'user.id', '%(first_name)s %(last_name)s')

# Multiple selection
IS_IN_DB(db, 'category.id', multiple=True)
```

### IS_NOT_IN_DB
```python
class IS_NOT_IN_DB(Validator):
    def __init__(self, dbset, field, error_message='Value already exists'):
```

**Purpose**: Ensures value doesn't exist in database (uniqueness).

**Use Cases:**
- Username uniqueness validation
- Email address uniqueness
- Prevent duplicate entries

## List and Set Validators

### IS_IN_SET
```python
class IS_IN_SET(Validator):
    def __init__(self, theset, labels=None, error_message='Value not allowed',
                 multiple=False, zero='', sort=True):
```

**Purpose**: Validates value against predefined set of options.

**Features:**
- Static option lists
- Custom labels for display
- Multiple selection support
- Automatic sorting

**Examples:**
```python
# Simple choices
IS_IN_SET(['red', 'green', 'blue'])

# With labels
IS_IN_SET(['S', 'M', 'L'], labels={'S': 'Small', 'M': 'Medium', 'L': 'Large'})

# Multiple selection
IS_IN_SET(['tag1', 'tag2', 'tag3'], multiple=True)
```

### IS_LIST_OF
```python
class IS_LIST_OF(Validator):
    def __init__(self, other_validator, minimum=0, maximum=100):
```

**Purpose**: Validates each item in a list using another validator.

**Example:**
```python
# List of email addresses
IS_LIST_OF(IS_EMAIL())

# List of integers in range
IS_LIST_OF(IS_INT_IN_RANGE(1, 100))
```

## Network Validators

### IS_IPV4
```python
class IS_IPV4(Validator):
```
Validates IPv4 addresses (e.g., 192.168.1.1).

### IS_IPV6
```python
class IS_IPV6(Validator):
```
Validates IPv6 addresses.

### IS_IPADDRESS
```python
class IS_IPADDRESS(Validator):
    def __init__(self, is_localhost=None, is_private=None, is_automatic=None):
```

**Purpose**: Comprehensive IP address validation with network type checking.

**Features:**
- IPv4 and IPv6 support
- Localhost detection
- Private network detection
- Automatic IP detection

## File Validators

### IS_UPLOAD_FILENAME
```python
class IS_UPLOAD_FILENAME(Validator):
    def __init__(self, filename=None, extension=None, lastdot=True,
                 case=1, error_message='Invalid file'):
```

**Purpose**: Validates uploaded file names and extensions.

**Features:**
- Extension whitelist/blacklist
- Case sensitivity control
- Filename pattern validation

### IS_FILE
```python
class IS_FILE(Validator):
    def __init__(self, extension=None, maxsize=None, minsize=None):
```

**Purpose**: Validates uploaded files by content and size.

### IS_IMAGE
```python
class IS_IMAGE(Validator):
    def __init__(self, extensions=('bmp','gif','jpeg','png'), maxsize=(10000,10000)):
```

**Purpose**: Specialized validator for image files.

## Advanced Validators

### IS_JSON
```python
class IS_JSON(Validator):
    def __init__(self, error_message='Invalid JSON', native_json=False):
```

**Purpose**: Validates JSON format and optionally parses content.

**Features:**
- JSON syntax validation
- Optional parsing to Python objects
- Error location reporting

### IS_STRONG
```python
class IS_STRONG(Validator):
    def __init__(self, min=8, max=20, upper=1, lower=1, number=1, special=0,
                 specials=r'!@#$%^&*()_+-={}[]|;:,.<>?'):
```

**Purpose**: Password strength validation.

**Features:**
- Length requirements
- Character type requirements (upper, lower, numeric, special)
- Custom special character sets

### CRYPT
```python
class CRYPT(object):
    def __init__(self, key=None, digest_alg='pbkdf2(1000,20,sha512)', salt=True):
```

**Purpose**: Password hashing and verification.

**Features:**
- Multiple hashing algorithms (PBKDF2, bcrypt, SHA, MD5)
- Automatic salt generation
- Secure password storage

## Utility Validators

### IS_EMPTY_OR / IS_NULL_OR
```python
class IS_EMPTY_OR(Validator):
    def __init__(self, other, null=None, empty_regex=None):

class IS_NULL_OR(IS_EMPTY_OR):  # Alias
```

**Purpose**: Allows empty/null values or validates using another validator.

### ANY_OF
```python
class ANY_OF(Validator):
    def __init__(self, *validators, **kwargs):
```

**Purpose**: Validates if input passes any of multiple validators (OR logic).

### CLEANUP
```python
class CLEANUP(Validator):
    def __init__(self, regex, replace='', error_message=None):
```

**Purpose**: Removes/replaces patterns in input (transformation validator).

## Specialized Validators

### IS_SLUG
```python
class IS_SLUG(IS_MATCH):
```
Validates URL-friendly strings (alphanumeric plus hyphens/underscores).

### IS_UPPER / IS_LOWER
Validates and converts text case.

### IS_EQUAL_TO
```python
class IS_EQUAL_TO(Validator):
    def __init__(self, expression, error_message='No match'):
```
Validates equality to another value (useful for password confirmation).

### IS_EXPR
```python
class IS_EXPR(Validator):
    def __init__(self, expression, error_message='Invalid expression'):
```
Validates using arbitrary Python expression.

## Usage Patterns

### Field Validation
```python
# Single validator
Field('email', 'string', requires=IS_EMAIL())

# Multiple validators
Field('username', 'string', requires=[
    IS_NOT_EMPTY(),
    IS_LENGTH(minsize=3, maxsize=20),
    IS_ALPHANUMERIC(),
    IS_NOT_IN_DB(db, 'user.username')
])
```

### Form Processing
```python
# Validate and transform input
validator = IS_EMAIL()
value, error = validator('user@example.com')
if error:
    print(f"Validation failed: {error}")
else:
    print(f"Valid email: {value}")
```

### Custom Validators
```python
class IS_EVEN(Validator):
    def __init__(self, error_message='Must be even'):
        self.error_message = error_message
    
    def __call__(self, value):
        try:
            if int(value) % 2 == 0:
                return (int(value), None)
            else:
                return (value, self.error_message)
        except (ValueError, TypeError):
            return (value, 'Invalid number')
```

## Internationalization

### Translation Support
```python
def translate(text):
    return Validator.translator(text)

# Custom translator function
Validator.translator = lambda text: my_translation_func(text)
```

All error messages support internationalization through the translator function.

## Notes
- Comprehensive validation coverage for web applications
- Supports both client-side and server-side validation
- Integrates with PyDAL field definitions
- Extensible framework for custom validators
- Thread-safe and performant
- Essential for data integrity and security