# PyDAL Regular Expression Helpers

## Overview
Regular expression utilities for data validation, parsing, and pattern matching in PyDAL operations.

## Key Features

### Pattern Matching
```python
class RegexHelpers:
    """
    Regular expression utilities for PyDAL
    
    Features:
    - Data validation patterns
    - SQL parsing patterns
    - Field validation
    - Format checking
    """
```

### Common Patterns
```python
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
URL_PATTERN = r'^https?://[^\s/$.?#].[^\s]*$'
IP_PATTERN = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
PHONE_PATTERN = r'^\+?[1-9]\d{1,14}$'
```

### Validation Functions
```python
def validate_email(email):
    """Validate email address format"""

def validate_url(url):
    """Validate URL format"""

def validate_ip_address(ip):
    """Validate IP address format"""

def validate_phone_number(phone):
    """Validate phone number format"""
```

### SQL Pattern Matching
- **Table Name Validation**: Valid table name patterns
- **Column Name Validation**: Valid column name patterns
- **SQL Injection Prevention**: Dangerous pattern detection
- **Query Parsing**: SQL statement parsing

### Custom Validators
- **Pattern Builder**: Dynamic pattern construction
- **Validation Composer**: Multiple pattern validation
- **Error Messaging**: Descriptive validation errors
- **Localization**: Multi-language pattern support

These regex helpers provide robust data validation and pattern matching capabilities throughout PyDAL.