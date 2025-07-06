# exceptions.py

## Overview
Custom exception classes for PyDAL that provide specific error handling for database operations, authorization, and NoSQL compatibility issues.

## Exception Classes

### NotFoundException
```python
class NotFoundException(Exception):
    pass
```

**Purpose**: Raised when requested database records or resources are not found.

**Use Cases:**
- Record not found in queries
- Table or field doesn't exist
- Missing database objects
- Failed lookups by ID or criteria

**Example Usage:**
```python
# Typical usage in PyDAL
user = db.auth_user(id=123)
if not user:
    raise NotFoundException("User with ID 123 not found")
```

### NotAuthorizedException
```python
class NotAuthorizedException(Exception):
    pass
```

**Purpose**: Raised when database operations are attempted without proper authorization.

**Use Cases:**
- Insufficient permissions for database operations
- Authentication failures
- Access control violations
- Security policy enforcement

**Example Usage:**
```python
# Access control in database operations
if not user.has_permission('write', table):
    raise NotAuthorizedException("Write access denied to table")
```

### NotOnNOSQLError
```python
class NotOnNOSQLError(NotImplementedError):
    def __init__(self, message=None):
        if message is None:
            message = "Not Supported on NoSQL databases"
        super(NotOnNOSQLError, self).__init__(message)
```

**Purpose**: Raised when SQL-specific operations are attempted on NoSQL databases.

**Inheritance**: Inherits from `NotImplementedError` to indicate feature limitation.

**Default Message**: "Not Supported on NoSQL databases"

**Use Cases:**
- SQL JOIN operations on MongoDB
- Complex SQL queries on document databases
- Relational constraints on NoSQL systems
- SQL-specific functions on non-relational backends

**Features:**
- **Default Message**: Provides informative default error message
- **Custom Messages**: Allows override for specific operation details
- **Inheritance**: Uses NotImplementedError to indicate intentional limitation

## Exception Hierarchy

### Standard Python Exceptions
- **Exception** (base for NotFoundException, NotAuthorizedException)
- **NotImplementedError** (base for NotOnNOSQLError)

### PyDAL Exception Tree
```
Exception
├── NotFoundException
├── NotAuthorizedException
└── NotImplementedError
    └── NotOnNOSQLError
```

## Usage Patterns

### Record Operations
```python
try:
    record = table.select().first()
    if not record:
        raise NotFoundException("No records found")
except NotFoundException as e:
    # Handle missing record
    return None
```

### Authorization Checks
```python
try:
    if not authorized:
        raise NotAuthorizedException("Access denied")
    # Perform database operation
except NotAuthorizedException as e:
    # Handle authorization failure
    log_security_violation(e)
```

### NoSQL Compatibility
```python
def join_operation(self):
    if self.adapter.dbengine in ['mongodb', 'couchdb']:
        raise NotOnNOSQLError("JOIN operations not supported")
    # Perform SQL JOIN
```

## Integration with PyDAL

### Adapter Level
Database adapters use these exceptions to provide consistent error handling:
- **SQL Adapters**: May raise NotOnNOSQLError for NoSQL compatibility
- **NoSQL Adapters**: Raise NotOnNOSQLError for unsupported operations
- **All Adapters**: Use NotFoundException for missing records

### ORM Level
- **Table Operations**: NotFoundException for missing tables/fields
- **Record Operations**: NotFoundException for missing records
- **Security Layer**: NotAuthorizedException for access control

### Query Engine
- **Complex Queries**: NotOnNOSQLError for SQL-specific operations
- **Result Processing**: NotFoundException for empty results
- **Validation**: Various exceptions for constraint violations

## Error Handling Best Practices

### Catching Specific Exceptions
```python
try:
    record = db.table(id=123)
except NotFoundException:
    # Handle missing record specifically
    pass
except NotAuthorizedException:
    # Handle authorization failure
    pass
```

### Generic Exception Handling
```python
try:
    db.operation()
except (NotFoundException, NotAuthorizedException) as e:
    # Handle both types
    logger.error(f"Database operation failed: {e}")
```

### NoSQL Compatibility Checks
```python
def sql_specific_operation(db):
    try:
        return db.complex_join()
    except NotOnNOSQLError:
        # Fallback for NoSQL databases
        return db.simple_query()
```

## Design Philosophy

### Explicit Error Types
- Clear distinction between different failure modes
- Specific exceptions for specific problems
- Easier debugging and error handling

### Compatibility Awareness
- NotOnNOSQLError acknowledges SQL/NoSQL differences
- Enables graceful degradation for cross-database code
- Promotes database-agnostic application design

### Standard Inheritance
- Follows Python exception hierarchy conventions
- Compatible with standard exception handling patterns
- Integrates well with existing error handling code

## Extension Points

### Custom Exceptions
Developers can extend these base exceptions:
```python
class RecordValidationError(NotFoundException):
    """Raised when record fails validation checks"""
    pass

class DatabaseConnectionError(NotAuthorizedException):
    """Raised when database connection fails due to auth"""
    pass
```

### Adapter-Specific Exceptions
Database adapters can define specific exceptions while inheriting from these base classes for consistency.

## Notes
- Minimal but essential exception hierarchy for PyDAL
- Focuses on most common database operation failure modes
- Provides foundation for robust error handling in database applications
- Enables clean separation between different types of database errors
- Critical for building reliable database-driven applications