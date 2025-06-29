# test_utils.py

## Overview
This file contains unit tests for web2py's utility functions including UUID generation, password hashing, markdown processing, and various helper functions used throughout the framework.

## Purpose
- Tests UUID generation and validation
- Validates password hashing and security functions
- Tests markdown and text processing utilities
- Verifies cryptographic functions and security helpers
- Tests data manipulation and formatting utilities

## Key Features Tested

### UUID Functions
- **UUID Generation**: Unique identifier creation
- **Format Validation**: UUID format checking
- **Collision Testing**: Uniqueness verification
- **Performance**: Generation speed optimization

### Security Functions
- **Password Hashing**: Secure password storage
- **Encryption/Decryption**: Data encryption utilities
- **Random Generation**: Cryptographically secure random data
- **Hash Validation**: Password verification

### Text Processing
- **Markdown**: Markdown to HTML conversion
- **Text Formatting**: String manipulation utilities
- **Encoding**: Character encoding handling
- **Sanitization**: Text cleaning and validation

### Data Utilities
- **Validation**: Data format validation
- **Conversion**: Type conversion utilities
- **Formatting**: Data presentation formatting
- **Parsing**: String and data parsing

## Integration with web2py Framework

### Security Integration
- **User Authentication**: Password security
- **Session Security**: Session token generation
- **CSRF Protection**: Anti-forgery token generation
- **Data Protection**: Sensitive data handling

### Application Development
- **Unique Identifiers**: Record ID generation
- **Content Processing**: User content handling
- **Data Validation**: Input validation utilities
- **Performance**: Optimized utility functions

## Usage Example
```python
from gluon.utils import web2py_uuid, hash_password, markdown

# UUID generation
unique_id = web2py_uuid()
print(unique_id)  # 'abc123-def456-ghi789'

# Password hashing
hashed = hash_password('secret123')
print(hashed)  # 'pbkdf2(1000,20,sha512)$...'

# Markdown processing
html = markdown('# Hello\n\nThis is **bold** text.')
print(html)  # '<h1>Hello</h1>\n\n<p>This is <strong>bold</strong> text.</p>'
```

This test suite ensures web2py's utility functions provide reliable, secure, and efficient helper functionality for common development tasks and security requirements.