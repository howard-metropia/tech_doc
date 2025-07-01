# Gluon Contrib MemDB Module

## Overview
In-memory database abstraction layer for web2py applications using memcache as the storage backend. Provides a DAL-compatible interface for applications that need database-like functionality with memcache storage, particularly useful for Google App Engine environments.

## Module Information
- **Module**: `gluon.contrib.memdb`
- **Authors**: Massimo Di Pierro, Robin B
- **License**: LGPLv3
- **Purpose**: Memcache-based database abstraction
- **Platform**: Google App Engine, general memcache environments

## Key Features
- **DAL Compatible**: Provides web2py DAL-like interface
- **Memcache Storage**: Uses memcache as storage backend
- **Field Validation**: Built-in field validation and formatting
- **Relationship Support**: Basic table relationships and references
- **Query Interface**: Simplified query syntax for memcache operations
- **Record Management**: Full CRUD operations on records

## Core Classes

### MEMDB
Main database class that manages tables and provides DAL interface.

**Constructor:**
```python
def __init__(self, client)
```

**Parameters:**
- `client`: Memcache client instance

**Attributes:**
- `_dbname`: Database name ('memdb')
- `tables`: List of defined table names
- `_translator`: SQL dialect translator for memcache
- `client`: Memcache client for storage operations

**Usage:**
```python
from google.appengine.api.memcache import Client
db = MEMDB(Client())
```

### Table
Represents a database table with fields and operations.

**Constructor:**
```python
def __init__(self, db, tablename, *fields)
```

**Attributes:**
- `_db`: Parent database instance
- `_tablename`: Table name
- `fields`: List of field names
- `_referenced_by`: List of referencing tables
- `_tableobj`: Memcache client reference

### Field
Represents a table field with type, validation, and constraints.

**Constructor:**
```python
def __init__(self, fieldname, type='string', length=None, default=None,
             required=False, requires=sqlhtml_validators, ondelete='CASCADE',
             notnull=False, unique=False, uploadfield=True)
```

**Field Types:**
- `string`: Text with specified length
- `text`: Long text content
- `integer`: Numeric integer values
- `double`: Floating-point numbers
- `boolean`: True/False values
- `date`: Date values
- `time`: Time values
- `datetime`: Date and time values
- `blob`: Binary data
- `upload`: File upload references
- `password`: Password fields
- `reference`: Foreign key references

## Database Operations

### Table Definition
```python
# Define table with fields
db.define_table('users',
    Field('name', 'string', length=100),
    Field('email', 'string', length=255),
    Field('age', 'integer'),
    Field('active', 'boolean', default=True),
    Field('created', 'datetime')
)

# Reference field
db.define_table('posts',
    Field('title', 'string'),
    Field('content', 'text'),
    Field('user', 'reference users')
)
```

### Record Operations

#### Insert Records
```python
# Insert single record
user_id = db.users.insert(
    name='John Doe',
    email='john@example.com',
    age=30,
    active=True
)

# Insert with default values
post_id = db.posts.insert(
    title='My Post',
    content='Post content',
    user=user_id
)
```

#### Retrieve Records
```python
# Get by ID
user = db.users.get(user_id)
if user:
    print(user.name)

# Table call syntax
user = db.users(user_id)
if user:
    print(user.email)

# With conditions
user = db.users(user_id, active=True)
```

#### Update Records
```python
# Update by ID
db.users.update(user_id, name='Jane Doe', age=31)

# Update via record
user = db.users.get(user_id)
if user:
    user.name = 'Updated Name'
    db.users.update(user_id, **user)
```

#### Delete Records
```python
# Delete by ID
db.users.delete(user_id)

# Delete via set
db(db.users.id == user_id).delete()
```

### Query Operations

#### Basic Queries
```python
# Query by ID (only supported query type)
query = db.users.id == user_id
set = db(query)
records = set.select()

# Count records
count = set.count()

# Update set
set.update(active=False)

# Delete set
set.delete()
```

#### Query Limitations
The module only supports queries by ID field:
```python
# Supported
query = db.users.id == 123

# Not supported
query = db.users.name == 'John'  # Raises SyntaxError
query = db.users.age > 25        # Raises SyntaxError
```

## Field Validation

### Built-in Validators
```python
# Automatic validators based on field type
Field('email', 'string', length=255)  # IS_LENGTH(255)
Field('age', 'integer')               # IS_INT_IN_RANGE(-1e100, 1e100)
Field('price', 'double')              # IS_FLOAT_IN_RANGE(-1e100, 1e100)
Field('birthdate', 'date')            # IS_DATE()
Field('created_at', 'datetime')       # IS_DATETIME()

# Custom validators
Field('email', 'string', requires=[IS_EMAIL(), IS_NOT_EMPTY()])
Field('age', 'integer', requires=IS_INT_IN_RANGE(1, 120))
```

### Field Constraints
```python
Field('name', 'string', required=True, notnull=True)
Field('email', 'string', unique=True)
Field('status', 'string', default='active')
```

## Data Storage Format

### Key Generation
Records are stored in memcache with structured keys:
```python
# Key format: __memdb__/t/{tablename}/k/{id}
key = '__memdb__/t/users/k/12345'
```

### ID Generation
```python
# Uses web2py UUID converted to long integer
id = long(web2py_uuid().replace('-',''), 16)
```

### Value Storage
Records stored as dictionaries with field values:
```python
{
    'name': 'John Doe',
    'email': 'john@example.com',
    'age': 30,
    'active': True,
    'created': datetime.datetime(2023, 1, 1, 12, 0, 0)
}
```

## Advanced Features

### Relationships
```python
# Define relationships
db.define_table('categories',
    Field('name', 'string')
)

db.define_table('products',
    Field('name', 'string'),
    Field('category', 'reference categories')
)

# Access relationships
product = db.products.get(product_id)
category_id = product.category
category = db.categories.get(category_id)
```

### Record Formatting
```python
# Field formatters
class CustomField(Field):
    def formatter(self, value):
        if self.type == 'string':
            return value.upper()
        return value

# Apply formatting
Field('name', 'string').formatter('john')  # Returns formatted value
```

### Data Type Conversion
```python
# Automatic type conversion
def obj_represent(object, fieldtype, db):
    if fieldtype == 'date':
        # Convert string to date
        return datetime.date(*[int(x) for x in str(object).split('-')])
    elif fieldtype == 'integer':
        return long(object)
    return object
```

## Error Handling

### Common Exceptions
```python
# Invalid table/field names
SyntaxError: "Can't cleanup 'invalid-name': only [0-9a-zA-Z_] allowed"

# Unsupported queries
SyntaxError: "only equality by id is supported"

# Table redefinition
SyntaxError: "table already defined: users"

# Missing references
SyntaxError: "Table: table referenced_table does not exist"
```

### Safe Operations
```python
# Check if record exists
user = db.users.get(user_id)
if user is not None:
    # Record exists, safe to use
    print(user.name)

# Handle insertion conflicts
try:
    user_id = db.users.insert(name='John', email='john@example.com')
except RuntimeError as e:
    if "Too many ID conflicts" in str(e):
        # Retry or handle conflict
        pass
```

## Performance Considerations

### Memory Usage
- All data stored in memcache memory
- No persistent storage
- Data lost when memcache flushes

### Scalability
- Limited by memcache size limits
- No complex query support
- Simple key-value operations only

### Optimization
```python
# Minimize memcache operations
# Batch operations when possible
users = []
for i in range(100):
    users.append(db.users.get(i))

# Consider caching frequently accessed data
cache = {}
def get_user_cached(user_id):
    if user_id not in cache:
        cache[user_id] = db.users.get(user_id)
    return cache[user_id]
```

## Integration Examples

### Web2py Application
```python
# In models/db.py
from gluon.contrib.memdb import MEMDB, Field
from google.appengine.api.memcache import Client

# Initialize database
db = MEMDB(Client())

# Define tables
db.define_table('users',
    Field('name', 'string'),
    Field('email', 'string'),
    Field('active', 'boolean', default=True)
)

# In controllers/default.py
def add_user():
    if request.vars.name and request.vars.email:
        user_id = db.users.insert(
            name=request.vars.name,
            email=request.vars.email
        )
        return dict(message='User created', id=user_id)
    return dict()

def get_user():
    user_id = request.args(0)
    user = db.users.get(long(user_id))
    if user:
        return dict(user=user)
    else:
        raise HTTP(404, 'User not found')
```

### Testing
```python
# Unit tests
def test_memdb():
    from google.appengine.api.memcache import Client
    from gluon.contrib.memdb import MEMDB, Field
    
    db = MEMDB(Client())
    db.define_table('test', Field('name', 'string'))
    
    # Test insert
    test_id = db.test.insert(name='test')
    assert test_id is not None
    
    # Test get
    record = db.test.get(test_id)
    assert record.name == 'test'
    
    # Test update
    db.test.update(test_id, name='updated')
    record = db.test.get(test_id)
    assert record.name == 'updated'
    
    # Test delete
    db.test.delete(test_id)
    record = db.test.get(test_id)
    assert record is None
```

## Limitations

### Query Limitations
- Only ID-based queries supported
- No complex WHERE clauses
- No JOINs between tables
- No aggregation functions

### Storage Limitations
- Memcache size restrictions
- No persistence across restarts
- Potential data loss under memory pressure

### Feature Limitations
- No transactions
- No complex relationships
- Limited data types
- No indexing support

This module provides a specialized solution for simple database needs in memcache-based environments, offering basic CRUD operations with a familiar DAL-like interface while working within the constraints of key-value storage.