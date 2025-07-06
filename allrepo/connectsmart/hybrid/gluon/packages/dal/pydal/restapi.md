# restapi.py

## Overview
RESTful API module for PyDAL that provides automatic REST API generation for database tables with comprehensive security policies, validation, and query capabilities.

## Module Constants
```python
__version__ = "0.1"
MAX_LIMIT = 1000
```

## Exception Classes

### PolicyViolation
```python
class PolicyViolation(ValueError):
    pass
```
Raised when REST API access violates security policies.

### InvalidFormat
```python
class InvalidFormat(ValueError):
    pass
```
Raised when API request format is invalid.

### NotFound
```python
class NotFound(ValueError):
    pass
```
Raised when requested resource is not found.

## Utility Functions

### maybe_call(value)
```python
def maybe_call(value):
    return value() if callable(value) else value
```
Executes callable values or returns value unchanged - enables dynamic policy evaluation.

### error_wrapper(func)
Decorator that standardizes REST API error responses:

**Response Format:**
```python
{
    "status": "success|error",
    "code": 200|400|401|404|422,
    "message": "Error description",
    "timestamp": "ISO datetime",
    "api_version": "0.1",
    "errors": {...}  # Validation errors
}
```

**HTTP Status Codes:**
- **200**: Success
- **400**: Bad Request (InvalidFormat, KeyError, ValueError)
- **401**: Unauthorized (PolicyViolation)
- **404**: Not Found (NotFound)
- **422**: Validation Errors

## Policy System

### Policy Class
```python
class Policy(object):
```
Configurable security policy system for REST API access control.

#### Default Policy Model
```python
model = {
    "POST": {
        "authorize": False,
        "fields": None
    },
    "PUT": {
        "authorize": False, 
        "fields": None
    },
    "DELETE": {
        "authorize": False
    },
    "GET": {
        "authorize": False,
        "fields": None,
        "query": None,
        "allowed_patterns": [],
        "denied_patterns": [],
        "limit": MAX_LIMIT,
        "allow_lookup": False,
    },
}
```

#### Policy Configuration

##### set(tablename, method, **attributes)
Configure policy for specific table and HTTP method:
```python
policy = Policy()
policy.set('users', 'GET', 
    authorize=True,
    fields=['id', 'name', 'email'],
    allowed_patterns=['name*', 'email*'],
    limit=100
)
```

##### get(tablename, method, name)
Retrieve policy attribute with fallback to wildcard (*) policies:
```python
# Get authorization requirement
auth_required = policy.get('users', 'GET', 'authorize')
```

#### Authorization Methods

##### check_if_allowed()
Comprehensive authorization check:
```python
def check_if_allowed(self, method, tablename, id=None, 
                    get_vars=None, post_vars=None, exceptions=True):
```

**Validation Steps:**
1. **Policy Existence**: Check if policy exists for table/method
2. **Authorization**: Evaluate authorize function/value
3. **Pattern Matching**: Validate query parameters against allowed/denied patterns
4. **Field Access**: Ensure requested fields are permitted

##### check_if_lookup_allowed()
Check if table lookup operations are permitted:
```python
allowed = policy.check_if_lookup_allowed('users')
```

#### Field Access Control

##### allowed_fieldnames(table, method="GET")
Get list of fields accessible for specific HTTP method:
```python
# Returns readable fields for GET, writable fields for POST/PUT
fields = policy.allowed_fieldnames(db.users, 'GET')
```

##### check_fieldnames(table, fieldnames, method="GET")
Validate that requested fieldnames are allowed:
```python
policy.check_fieldnames(db.users, ['name', 'email'], 'POST')
```

### Predefined Policies

#### DENY_ALL_POLICY
```python
DENY_ALL_POLICY = Policy()
```
Default restrictive policy - denies all access.

#### ALLOW_ALL_POLICY
```python
ALLOW_ALL_POLICY = Policy()
ALLOW_ALL_POLICY.set(
    tablename="*",
    method="GET",
    authorize=True,
    allowed_patterns=["**"],
    allow_lookup=True,
)
```
Permissive policy allowing all operations (for development/testing).

## RestAPI Class

### Initialization
```python
class RestAPI(object):
    def __init__(self, db, policy):
        self.db = db
        self.policy = policy
```

### Request Processing

#### __call__(method, tablename, id=None, get_vars=None, post_vars=None)
Main REST API entry point handling all HTTP methods:

**URL Patterns:**
```
GET    /api/users           # List users
GET    /api/users/123       # Get user by ID
POST   /api/users           # Create user
PUT    /api/users/123       # Update user
DELETE /api/users/123       # Delete user
```

**Processing Flow:**
1. **Validation**: Parse table name and validate existence
2. **Authorization**: Check policy permissions
3. **Field Validation**: Ensure requested fields are allowed
4. **Method Dispatch**: Route to appropriate handler

#### HTTP Method Handlers

##### GET - Search/Retrieve
```python
if method == "GET":
    if id:
        get_vars["id.eq"] = id
    return self.search(tablename, get_vars)
```

**Query Parameters:**
- **field.eq=value**: Equality filter
- **field.ne=value**: Not equal filter
- **field.lt=value**: Less than filter
- **field.le=value**: Less than or equal filter
- **field.gt=value**: Greater than filter
- **field.ge=value**: Greater than or equal filter
- **field.in=val1,val2**: IN filter
- **field.like=pattern**: LIKE filter
- **order=field**: Order by field
- **limit=N**: Limit results
- **offset=N**: Skip results

##### POST - Create
```python
elif method == "POST":
    table = self.db[tablename]
    return table.validate_and_insert(**post_vars).as_dict()
```
Creates new record with validation.

##### PUT - Update
```python
elif method == "PUT":
    id = id or post_vars["id"]
    table = self.db[tablename]
    data = table.validate_and_update(id, **post_vars).as_dict()
    if not data.get("errors") and not data.get("updated"):
        raise NotFound("Item not found")
    return data
```
Updates existing record with validation.

##### DELETE - Remove
```python
elif method == "DELETE":
    id = id or post_vars["id"]
    table = self.db[tablename]
    deleted = self.db(table._id == id).delete()
    if not deleted:
        raise NotFound("Item not found")
    return {"deleted": deleted}
```
Deletes record by ID.

### Query Processing

#### Regular Expressions
```python
re_table_and_fields = re.compile(r"\w+([\w+(,\w+)+])?")
re_lookups = re.compile(r"((\w*\!?\:)?(\w+(\[\w+(,\w+)*\])?)(\.\w+(\[\w+(,\w+)*\])?)*)")
re_no_brackets = re.compile(r"\[.*?\]")
```

Used for parsing complex query syntax and field specifications.

#### table_model(table, fieldnames)
Generates table schema information for API documentation:
```python
def table_model(self, table, fieldnames):
```

Returns field definitions including:
- Field types and constraints
- Validation requirements
- Permitted operations per field
- Readable/writable access levels

## Usage Examples

### Basic Setup
```python
from pydal import DAL
from pydal.restapi import RestAPI, Policy

# Database setup
db = DAL('sqlite://test.db')
db.define_table('users',
    Field('name', 'string'),
    Field('email', 'string'),
    Field('age', 'integer')
)

# Policy configuration
policy = Policy()
policy.set('users', 'GET', authorize=True, 
          allowed_patterns=['**'], limit=50)
policy.set('users', 'POST', authorize=True,
          fields=['name', 'email', 'age'])

# API initialization
api = RestAPI(db, policy)
```

### Request Handling
```python
# GET request
result = api('GET', 'users', get_vars={'name.like': 'John%'})

# POST request
result = api('POST', 'users', post_vars={
    'name': 'John Doe',
    'email': 'john@example.com',
    'age': 30
})

# PUT request
result = api('PUT', 'users', id=1, post_vars={'age': 31})

# DELETE request
result = api('DELETE', 'users', id=1)
```

### Advanced Policies
```python
# Dynamic authorization
def authorize_user(tablename, id, get_vars, post_vars):
    # Custom authorization logic
    return current_user.has_permission(tablename)

policy.set('sensitive_table', 'GET', authorize=authorize_user)

# Field-level access control
policy.set('users', 'GET', fields=['id', 'name'])  # Hide email
policy.set('users', 'PUT', fields=['name'])        # Only name updatable
```

## Security Features

### Pattern Matching
- **Allowed Patterns**: Whitelist query parameters
- **Denied Patterns**: Blacklist dangerous patterns
- **Wildcard Support**: `**` allows all, `*` for prefix matching

### Field Access Control
- **Method-Specific**: Different fields for GET/POST/PUT
- **Readable/Writable**: Respects PyDAL field permissions
- **Dynamic Control**: Callable authorization functions

### Validation Integration
- Uses PyDAL's built-in validation
- Returns structured error responses
- Maintains data integrity

## Notes
- Provides complete REST API layer for PyDAL applications
- Comprehensive security policy system
- Supports complex query operations
- Integrates with PyDAL validation and constraints
- Suitable for production API deployment
- Enables rapid API development from database schemas