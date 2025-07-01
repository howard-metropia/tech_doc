# Gluon SQL Module

## Overview

The `sql.py` module provides backward compatibility support for web2py's database abstraction layer. This module serves as a compatibility shim between the legacy web2py SQL interface and the modern PyDAL (Python Database Abstraction Layer) implementation. It maintains API compatibility while leveraging the enhanced functionality of PyDAL.

## Key Features

- **Backward Compatibility**: Maintains legacy web2py SQL API
- **PyDAL Integration**: Leverages modern PyDAL functionality
- **Alias Support**: Provides legacy class and function aliases
- **Driver Abstraction**: Database driver management and selection
- **Seamless Migration**: Enables gradual migration to PyDAL

## Core Components

### Database Abstraction Layer

#### `DAL` (Database Abstraction Layer)
The primary database interface imported from PyDAL, providing:

**Features:**
- Multi-database support (MySQL, PostgreSQL, SQLite, etc.)
- Connection pooling and management
- Transaction handling
- Migration support
- Query optimization

**Usage:**
```python
from gluon.sql import DAL, Field

# Create database connection
db = DAL('sqlite://storage.db')

# Define table
db.define_table('person',
    Field('name', 'string'),
    Field('age', 'integer'),
    Field('email', 'string')
)
```

#### `Field` Class
Database field definition class for table schemas.

**Features:**
- Type specification and validation
- Constraint definition
- Default value assignment
- Relationship management

**Field Types:**
- `'string'`: Text data
- `'text'`: Large text blocks
- `'integer'`: Numeric integers
- `'double'`: Floating-point numbers
- `'boolean'`: True/False values
- `'date'`: Date values
- `'datetime'`: Date and time values
- `'time'`: Time values
- `'password'`: Encrypted password storage
- `'upload'`: File upload handling
- `'reference table'`: Foreign key relationships

### PyDAL Core Objects

#### Database Query Components

##### `Expression`
Base class for database expressions and operations.

**Features:**
- Operator overloading
- Expression composition
- SQL generation
- Type safety

##### `Query`
Represents database query conditions.

**Usage:**
```python
# Simple query
query = db.person.age > 18

# Complex query
query = (db.person.age > 18) & (db.person.name.startswith('John'))

# Query execution
records = db(query).select()
```

##### `Set`
Represents a set of database records for operations.

**Methods:**
- `select()`: Retrieve records
- `update()`: Modify records
- `delete()`: Remove records
- `count()`: Count matching records

**Usage:**
```python
# Create set
record_set = db(db.person.age > 18)

# Operations
records = record_set.select()
record_set.update(status='adult')
count = record_set.count()
```

##### `Table`
Represents database table structure and operations.

**Features:**
- Field access and validation
- Table-level operations
- Relationship management
- Index creation

##### `Row` / `Rows`
Represent individual records and record collections.

**Row Features:**
- Attribute-style field access
- Dictionary-like interface
- Type conversion
- Validation

**Rows Features:**
- Iteration support
- List-like interface
- Serialization methods
- Aggregation functions

### Legacy Compatibility Aliases

#### Database Classes
```python
SQLDB = DAL          # Legacy database class
GQLDB = DAL          # Google App Engine compatibility
SQLField = Field     # Legacy field class
SQLTable = Table     # Legacy table class
```

#### Query Components
```python
SQLXorable = Expression  # Legacy expression class
SQLQuery = Query         # Legacy query class
SQLSet = Set            # Legacy set class
SQLRows = Rows          # Legacy rows class
SQLStorage = Row        # Legacy row class
```

### Driver Management

#### `DRIVERS`
Dictionary of available database drivers imported from PyDAL.

**Supported Drivers:**
- MySQL: `pymysql`, `mysqldb`
- PostgreSQL: `psycopg2`, `pg8000`
- SQLite: `sqlite3`
- Oracle: `cx_oracle`
- MSSQL: `pyodbc`
- MongoDB: `pymongo`
- And many others

**Usage:**
```python
from gluon.sql import DRIVERS

# Check available drivers
print(DRIVERS.keys())

# Check specific driver
if 'pymysql' in DRIVERS:
    db = DAL('mysql://user:pass@host/db')
```

### Advanced Components

#### `BaseAdapter`
Base class for database adapters providing common functionality.

**Features:**
- Connection management
- Query execution
- Result processing
- Error handling

#### `SQLALL`
Helper class for advanced SQL operations.

**Features:**
- Complex query construction
- Advanced SQL generation
- Custom SQL injection
- Raw query execution

#### `SQLCustomType`
Support for custom field types and validation.

**Features:**
- Custom type definition
- Validation logic
- Representation methods
- Database mapping

## Migration Support

### Legacy Code Compatibility
The module ensures existing web2py applications continue to work:

```python
# Old web2py code continues to work
from gluon.sql import SQLDB, SQLField

db = SQLDB('sqlite://app.db')
db.define_table('users',
    SQLField('name', 'string'),
    SQLField('email', 'string')
)
```

### Modern PyDAL Usage
New code can use modern PyDAL features:

```python
# Modern PyDAL approach
from gluon.sql import DAL, Field

db = DAL('sqlite://app.db')
db.define_table('users',
    Field('name', 'string', requires=IS_NOT_EMPTY()),
    Field('email', 'string', requires=IS_EMAIL()),
    Field('created_on', 'datetime', default=request.now)
)
```

## Usage Patterns

### Basic Database Operations

#### Table Definition
```python
from gluon.sql import DAL, Field

db = DAL('sqlite://example.db')

# Define table with various field types
db.define_table('product',
    Field('name', 'string', length=100, required=True),
    Field('description', 'text'),
    Field('price', 'double', default=0.0),
    Field('in_stock', 'boolean', default=True),
    Field('created_at', 'datetime', default=request.now)
)
```

#### CRUD Operations
```python
# Create
product_id = db.product.insert(
    name='Widget',
    description='A useful widget',
    price=19.99
)

# Read
product = db.product(product_id)
products = db(db.product.price < 50).select()

# Update
db(db.product.id == product_id).update(price=24.99)

# Delete
db(db.product.id == product_id).delete()
```

### Advanced Queries

#### Complex Conditions
```python
# Multiple conditions
expensive_in_stock = db(
    (db.product.price > 100) & 
    (db.product.in_stock == True)
).select()

# OR conditions
search_results = db(
    (db.product.name.contains('widget')) |
    (db.product.description.contains('widget'))
).select()
```

#### Joins and Relationships
```python
# Define related tables
db.define_table('category',
    Field('name', 'string')
)

db.define_table('product',
    Field('name', 'string'),
    Field('category_id', 'reference category')
)

# Join query
products_with_categories = db(
    db.product.category_id == db.category.id
).select(
    db.product.ALL,
    db.category.name
)
```

## Integration Points

### Web2py Framework Integration
```python
# Controllers can use either legacy or modern syntax
def list_products():
    products = db(db.product).select()
    return dict(products=products)

def legacy_list():
    # Legacy syntax still works
    products = db().select(db.product.ALL)
    return dict(products=products)
```

### Template Integration
```python
# Views/templates.html
{{for product in products:}}
    <div>{{=product.name}} - ${{=product.price}}</div>
{{pass}}
```

## Performance Considerations

### Connection Management
- PyDAL handles connection pooling automatically
- Legacy aliases maintain same performance characteristics
- Proper connection cleanup and management

### Query Optimization
- Modern PyDAL optimizations available through aliases
- Lazy loading and efficient result handling
- Query caching and optimization

## Migration Strategy

### Gradual Migration
1. **Assessment**: Identify legacy SQL usage
2. **Alias Usage**: Leverage compatibility aliases
3. **Modern Features**: Gradually adopt PyDAL features
4. **Testing**: Ensure functionality preservation
5. **Optimization**: Take advantage of PyDAL improvements

### Legacy Support Timeline
- Full backward compatibility maintained
- Gradual deprecation warnings
- Modern alternatives provided
- Migration documentation available

## Error Handling

### Database Errors
```python
try:
    db.product.insert(name='Test Product')
    db.commit()
except Exception as e:
    db.rollback()
    logger.error(f"Database error: {e}")
```

### Connection Issues
```python
try:
    db = DAL('mysql://user:pass@host/db')
except Exception as e:
    # Fallback to SQLite
    db = DAL('sqlite://fallback.db')
```

## Best Practices

### Modern Development
- Use `DAL` instead of `SQLDB` for new code
- Leverage PyDAL's advanced features
- Implement proper error handling
- Use connection pooling effectively

### Legacy Maintenance
- Maintain existing alias usage for stability
- Test thoroughly when migrating
- Document compatibility requirements
- Plan gradual modernization

## Usage Examples

### Complete Application Example
```python
from gluon.sql import DAL, Field

# Database setup
db = DAL('sqlite://blog.db')

# Table definitions
db.define_table('author',
    Field('name', 'string', required=True),
    Field('email', 'string', unique=True)
)

db.define_table('post',
    Field('title', 'string', required=True),
    Field('content', 'text'),
    Field('author_id', 'reference author'),
    Field('published', 'boolean', default=False),
    Field('created_at', 'datetime', default=request.now)
)

# Application logic
def create_post(title, content, author_id):
    return db.post.insert(
        title=title,
        content=content,
        author_id=author_id
    )

def get_published_posts():
    return db(db.post.published == True).select(
        db.post.ALL,
        db.author.name,
        join=db.author.on(db.post.author_id == db.author.id),
        orderby=~db.post.created_at
    )
```

This module ensures seamless compatibility between legacy web2py SQL code and modern PyDAL functionality, enabling applications to benefit from PyDAL improvements while maintaining existing code investments.