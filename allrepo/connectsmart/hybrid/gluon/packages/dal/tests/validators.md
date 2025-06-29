# validators.py

## Overview
This file contains specific tests for individual PyDAL validators, ensuring each validator class functions correctly with various input scenarios and edge cases.

## Purpose
- Tests each validator class thoroughly
- Validates error message generation
- Verifies validator parameters
- Ensures consistent behavior

## Core Validators Tested

### String Validators
- **IS_ALPHANUMERIC**: Letters and numbers only
- **IS_LENGTH**: Min/max length validation
- **IS_MATCH**: Regex pattern matching
- **IS_SLUG**: URL-friendly strings

### Numeric Validators
- **IS_INT**: Integer validation
- **IS_FLOAT**: Floating point validation
- **IS_DECIMAL**: Precision decimal validation
- **IS_INT_IN_RANGE**: Range constraints

## Specialized Validators

### Format Validators
```python
# Email validation
IS_EMAIL(error_message='Invalid email')

# URL validation  
IS_URL(mode='http', allowed_schemes=['http', 'https'])

# IP address validation
IS_IPV4(minip='10.0.0.0', maxip='10.255.255.255')
```

### Database Validators
- **IS_IN_DB**: Reference validation
- **IS_NOT_IN_DB**: Uniqueness validation
- **IS_IN_SET**: Enumeration validation
- **IS_LIST_OF**: Multiple value validation

## Complex Validation

### Conditional Validators
- Date/time range validation
- Credit card validation
- Phone number formats
- Custom business rules

### Validation Context
- Form vs API validation
- Create vs update rules
- Conditional requirements
- Cross-field validation

This validator testing ensures each PyDAL validator provides accurate, reliable data validation with clear error reporting.