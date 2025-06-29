# validation.py

## Overview
This file tests PyDAL's data validation framework, ensuring field validators work correctly, validation chains function properly, and custom validators integrate seamlessly.

## Purpose
- Tests built-in validator functionality
- Validates custom validator implementation
- Verifies validation error handling
- Ensures validation chain processing

## Key Validators Tested

### Basic Validators
- **IS_NOT_EMPTY**: Required field validation
- **IS_LENGTH**: String length constraints
- **IS_INT_IN_RANGE**: Numeric range validation
- **IS_EMAIL**: Email format validation

### Advanced Validators
- **IS_MATCH**: Regular expression matching
- **IS_IN_DB**: Foreign key validation
- **IS_NOT_IN_DB**: Uniqueness checking
- **IS_DATE**: Date format validation

## Validation Chains

### Multiple Validators
```python
db.define_table('user',
    Field('email', 
          requires=[IS_EMAIL(),
                    IS_NOT_IN_DB(db, 'user.email')]),
    Field('age',
          requires=IS_INT_IN_RANGE(0, 120)),
    Field('password',
          requires=[IS_LENGTH(minsize=8),
                    IS_STRONG()])
)
```

### Custom Validators
- Class-based validators
- Function validators
- Async validation
- Complex business rules

## Error Handling

### Validation Errors
- Error message customization
- Internationalization support
- Field-specific errors
- Form-level validation

### Edge Cases
- Null value handling
- Empty string validation
- Type conversion errors
- Cascading validation

This validation testing ensures PyDAL provides robust data validation to maintain data integrity across all operations.