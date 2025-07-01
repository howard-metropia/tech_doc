# objects.py

## Overview
Core PyDAL objects module containing the fundamental database abstraction classes: Field, Table, Row, Rows, Query, Set, and Expression. These classes form the backbone of PyDAL's ORM functionality and provide the primary interface for database operations.

## Constants and Utilities

### Default Field Lengths
```python
DEFAULTLENGTH = {
    "string": 512,
    "password": 512,
    "upload": 512,
    "text": 2 ** 15,    # 32,768 characters
    "blob": 2 ** 31,   # 2GB
}
```

### Default Validation Patterns
```python
DEFAULT_REGEX = {
    "id": "[1-9]\d*",
    "decimal": "\d{1,10}\.\d{2}",
    "integer": "[+-]?\d*",
    "float": "[+-]?\d*(\.\d*)?",
    "double": "[+-]?\d*(\.\d*)?",
    "date": "\d{4}\-\d{2}\-\d{2}",
    "time": "\d{2}\:\d{2}(\:\d{2}(\.\d*)?)?",
    "datetime": "\d{4}\-\d{2}\-\d{2} \d{2}\:\d{2}(\:\d{2}(\.\d*)?)?",
}
```

## Core Classes

### Row
```python
class Row(BasicStorage):
```
Represents a single database record with enhanced dictionary-like access.

**Key Features:**
- **Attribute Access**: Access fields via `row.fieldname`
- **Dictionary Access**: Access fields via `row['fieldname']`
- **Update Operations**: `row.update_record()` method
- **Delete Operations**: `row.delete_record()` method
- **Validation**: Automatic field validation on updates
- **Serialization**: Support for JSON/XML export

**Usage Examples:**
```python
# Access field values
user = db.auth_user(1)
print(user.name)           # Attribute access
print(user['email'])       # Dictionary access

# Update record
user.update_record(name='New Name')

# Delete record
user.delete_record()
```

### Table
```python
class Table(Serializable, BasicStorage):
```
Represents a database table with its schema and provides query interface.

**Key Features:**
- **Field Definitions**: Container for Field objects
- **Query Interface**: Generate Query objects via `table.field == value`
- **Insert Operations**: `table.insert()` method
- **Schema Management**: Migration and validation support
- **Relationships**: Foreign key and reference handling
- **Indexes**: Database index management

**Table Properties:**
- `_tablename`: Logical table name
- `_rname`: Real/quoted table name for SQL
- `_fields`: Ordered list of field names
- `_id`: Primary key field
- `_primarykey`: Composite primary key support
- `_common_filter`: Default query filter

**Usage Examples:**
```python
# Define table
users = db.define_table('users',
    Field('name', 'string'),
    Field('email', 'string', unique=True)
)

# Insert record
user_id = users.insert(name='John', email='john@example.com')

# Query table
query = users.name == 'John'
user = db(query).select().first()
```

### Field
```python
class Field(Expression, Serializable):
```
Represents a database table column with type information, constraints, and validation.

**Field Types:**
- **Basic Types**: string, text, integer, bigint, float, double, decimal
- **Date/Time**: date, time, datetime
- **Binary**: blob, upload
- **Boolean**: boolean
- **JSON**: json
- **References**: reference, big-reference
- **Special**: id, password

**Field Properties:**
- **type**: Field data type
- **length**: Maximum field length
- **default**: Default value
- **required**: NOT NULL constraint
- **unique**: Unique constraint
- **notnull**: Explicit NOT NULL
- **ondelete**: Foreign key cascade behavior

**Validation and Representation:**
- **requires**: List of validators
- **represent**: Display formatting function
- **widget**: Form widget for input
- **label**: Human-readable field label
- **comment**: Help text or documentation

**Usage Examples:**
```python
# Basic field
Field('name', 'string', length=100, required=True)

# Field with validation
Field('email', 'string', requires=IS_EMAIL())

# Reference field
Field('user_id', 'reference auth_user', ondelete='CASCADE')

# Field with custom representation
Field('price', 'decimal(10,2)', represent=lambda v: f"${v:.2f}")
```

### Query
```python
class Query(Serializable):
```
Represents database query conditions that can be combined and optimized.

**Query Operators:**
- **Comparison**: `==`, `!=`, `<`, `<=`, `>`, `>=`
- **Text Matching**: `like()`, `ilike()`, `regexp()`
- **List Operations**: `belongs()`, `contains()`
- **Logical**: `&` (AND), `|` (OR), `~` (NOT)
- **Null Checks**: Special handling for None values

**Query Combination:**
```python
# Basic queries
query1 = db.users.name == 'John'
query2 = db.users.age > 18

# Combined queries
combined = query1 & query2  # AND
alternative = query1 | query2  # OR
negated = ~query1  # NOT
```

### Set
```python
class Set(Serializable):
```
Represents a set of database records matching a query, providing CRUD operations.

**Key Methods:**
- **select()**: Retrieve records with options
- **update()**: Mass update operations
- **delete()**: Mass delete operations
- **count()**: Count matching records
- **isempty()**: Check if set is empty

**Select Options:**
- **orderby**: Sort order specification
- **groupby**: Grouping fields
- **having**: Post-aggregation filtering
- **limitby**: Pagination support
- **left**: LEFT JOIN operations
- **distinct**: Remove duplicates

**Usage Examples:**
```python
# Create set
users_set = db(db.users.age > 18)

# Select with options
adults = users_set.select(
    orderby=db.users.name,
    limitby=(0, 10)
)

# Mass operations
users_set.update(status='active')
count = users_set.count()
```

### Expression
```python
class Expression(object):
```
Base class for all SQL expressions (fields, functions, operations).

**Expression Types:**
- **Field References**: `table.field`
- **Functions**: `field.sum()`, `field.count()`, `field.max()`
- **Operations**: `field + 1`, `field.like('%pattern%')`
- **Case Statements**: Conditional expressions

### Rows
```python
class Rows(BasicRows):
```
Collection of Row objects with additional functionality for result set manipulation.

**Key Features:**
- **Iteration**: Iterate over individual Row objects
- **Indexing**: Access rows by index
- **Slicing**: Extract subsets of results
- **Filtering**: `find()` method for client-side filtering
- **Sorting**: `sort()` method for client-side sorting
- **Export**: JSON, XML, CSV export capabilities
- **Rendering**: HTML table generation

**Methods:**
- **find()**: Client-side record filtering
- **exclude()**: Client-side record exclusion
- **sort()**: Client-side sorting
- **group_by_value()**: Group records by field value
- **render()**: Generate HTML representation
- **export_to_csv_file()**: CSV export

### LazyReferenceGetter
```python
class LazyReferenceGetter(object):
```
Provides lazy loading for reference fields to avoid N+1 query problems.

**Features:**
- **Deferred Loading**: References loaded only when accessed
- **Caching**: Avoid duplicate queries for same reference
- **Batch Loading**: Optimize multiple reference access

### FieldVirtual and FieldMethod
```python
class FieldVirtual(object):
class FieldMethod(object):
```
Support for computed fields and virtual methods on records.

**Virtual Fields:**
- Computed from other fields
- Not stored in database
- Calculated on access

**Field Methods:**
- Instance methods on Row objects
- Access to full record context
- Can perform additional queries

## Advanced Features

### Upload Field Handling
Specialized support for file upload fields:
- **File Storage**: Automatic file system management
- **Naming**: Unique filename generation
- **Validation**: File type and size validation
- **Cleanup**: Automatic orphaned file removal

### JSON Support
Native JSON field type with:
- **Validation**: JSON syntax validation
- **Indexing**: Database-specific JSON indexing
- **Querying**: JSON path queries where supported

### Polymorphic Models
Support for table inheritance:
- **Single Table**: Multiple entity types in one table
- **Joined Tables**: Related tables for inheritance
- **Abstract Models**: Base model definitions

### Migration Support
Automatic schema migration:
- **Field Addition**: Add new fields to existing tables
- **Field Modification**: Change field properties
- **Field Removal**: Remove obsolete fields
- **Index Management**: Automatic index creation/removal

## Database Adapter Integration

### SQL Generation
Objects work with database adapters to generate appropriate SQL:
- **Dialect Support**: Database-specific SQL variations
- **Type Mapping**: Python types to database types
- **Constraint Generation**: Primary keys, foreign keys, indexes

### Transaction Support
Integration with database transactions:
- **Atomic Operations**: Ensure data consistency
- **Rollback Support**: Error recovery
- **Savepoints**: Nested transaction support

### Performance Optimization
- **Query Optimization**: Automatic query plan optimization
- **Connection Pooling**: Efficient connection reuse
- **Lazy Loading**: Deferred data loading
- **Caching**: Result set caching where appropriate

## Usage Patterns

### Basic CRUD Operations
```python
# Create
user_id = db.users.insert(name='John', email='john@example.com')

# Read
user = db.users(user_id)
users = db(db.users.age > 18).select()

# Update
db.users(user_id).update_record(name='John Doe')
db(db.users.age > 65).update(status='senior')

# Delete
db.users(user_id).delete_record()
db(db.users.status == 'inactive').delete()
```

### Complex Queries
```python
# Joins
query = db.orders.user_id == db.users.id
results = db(query).select(db.users.name, db.orders.total)

# Aggregation
total_sales = db.orders.total.sum()
result = db().select(total_sales).first()[total_sales]

# Subqueries
subquery = db(db.users.age > 18).select(db.users.id)
orders = db(db.orders.user_id.belongs(subquery)).select()
```

## Notes
- Central component of PyDAL's ORM functionality
- Provides Pythonic interface to database operations
- Supports wide range of database backends
- Handles complex relationships and constraints
- Essential for building database-driven applications
- Extensive validation and security features built-in