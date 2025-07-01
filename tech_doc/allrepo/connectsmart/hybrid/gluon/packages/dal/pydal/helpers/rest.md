# PyDAL REST API Helpers

## Overview
Helper functions and utilities for creating RESTful APIs with PyDAL, providing standardized REST endpoints and operations.

## Key Features

### REST API Support
```python
class RESTHelpers:
    """
    REST API utilities for PyDAL
    
    Features:
    - Automatic endpoint generation
    - HTTP method mapping
    - JSON serialization
    - Error handling
    """
```

### HTTP Method Mapping
```python
REST_METHODS = {
    'GET': 'select',      # Read operations
    'POST': 'insert',     # Create operations
    'PUT': 'update',      # Update operations
    'DELETE': 'delete'    # Delete operations
}
```

### Endpoint Generation
- **Resource URLs**: Automatic URL generation
- **Collection Endpoints**: List and filter operations
- **Item Endpoints**: Individual record operations
- **Nested Resources**: Related data access

### Serialization
```python
def serialize_rows(rows):
    """Convert PyDAL rows to JSON"""

def serialize_row(row):
    """Convert PyDAL row to JSON"""

def deserialize_data(json_data):
    """Convert JSON to PyDAL format"""
```

### Authentication & Authorization
- **Token-based Auth**: JWT token support
- **Role-based Access**: Permission checking
- **API Key Management**: Key-based authentication
- **Rate Limiting**: Request throttling

### Error Handling
- **HTTP Status Codes**: Appropriate error responses
- **Error Messages**: Descriptive error information
- **Validation Errors**: Field-level error reporting
- **Exception Mapping**: Python exceptions to HTTP errors

These helpers simplify the creation of RESTful APIs backed by PyDAL databases.