# restapi.py

## Overview
This file tests PyDAL's REST API functionality, validating automatic REST endpoint generation, request handling, and response formatting for database operations.

## Purpose
- Tests REST API auto-generation
- Validates HTTP method handling
- Verifies response formatting
- Ensures API security and permissions

## Key Features Tested

### REST Endpoints
- **GET**: Record retrieval and queries
- **POST**: Record creation
- **PUT**: Record updates
- **DELETE**: Record deletion
- **PATCH**: Partial updates

### API Patterns
```python
# Auto-generated endpoints
@request.restful()
def api():
    def GET(tablename, id):
        return db[tablename](id)
    def POST(tablename, **vars):
        return db[tablename].insert(**vars)
    return locals()
```

## Request Handling

### Query Parameters
- Filtering: `?name=John&age=25`
- Sorting: `?orderby=name`
- Pagination: `?offset=0&limit=10`
- Field selection: `?fields=id,name,email`

### Response Formats
- JSON responses (default)
- XML format support
- CSV data export
- Custom formatters

## Security Testing

### Authentication
- API key validation
- Token-based auth
- OAuth integration
- Permission checking

### Input Validation
- SQL injection prevention
- Parameter sanitization
- Rate limiting
- CORS handling

## Advanced Features

### Batch Operations
- Multiple record creation
- Bulk updates
- Transaction support
- Partial success handling

This REST API testing ensures PyDAL can automatically provide secure, fully-featured REST endpoints for database tables.