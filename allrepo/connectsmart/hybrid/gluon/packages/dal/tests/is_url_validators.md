# is_url_validators.py

## Overview
This file tests PyDAL's URL validation functionality, ensuring proper validation of database connection URLs and web URLs used in validators and field types.

## Purpose
- Tests URL format validation
- Validates connection string parsing
- Verifies web URL validation rules
- Ensures proper error handling for invalid URLs

## Key Validation Tests

### Database URL Validation
- **SQLite URLs**: `sqlite://storage.db`, `sqlite:memory`
- **MySQL URLs**: `mysql://user:pass@localhost/db`
- **PostgreSQL URLs**: `postgres://user:pass@host:5432/db`
- **Connection Parameters**: Query string options

### Web URL Validation
- **HTTP/HTTPS**: Protocol validation
- **Domain Names**: Valid domain formats
- **IP Addresses**: IPv4 and IPv6 support
- **Port Numbers**: Optional port validation

## Test Cases

### Valid URL Patterns
```python
# Database URLs
'sqlite://test.db'
'mysql://root:password@localhost:3306/mydb?charset=utf8'
'postgresql://user@host/database?sslmode=require'

# Web URLs
'http://example.com'
'https://sub.domain.com:8080/path'
'http://192.168.1.1:3000'
```

### Invalid URL Detection
- Missing protocol schemes
- Invalid characters in URLs
- Malformed connection strings
- Security validation (SQL injection attempts)

## Validator Integration

### IS_URL Validator
- Mode options (http, https, any)
- Prepend scheme behavior
- Error message customization
- Unicode URL support

This URL validator testing ensures reliable validation of both database connection strings and web URLs throughout PyDAL applications.