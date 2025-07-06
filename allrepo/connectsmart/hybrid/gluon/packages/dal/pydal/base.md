# base.py

## Overview
Core module of PyDAL containing the main DAL (Database Abstraction Layer) class and associated metaclass, providing the primary interface for database operations across multiple database backends.

## Supported Database Systems
PyDAL supports a comprehensive range of database systems:

### Relational Databases
- **SQLite & SpatiaLite**: File-based and in-memory databases
- **MySQL**: Popular open-source database
- **PostgreSQL**: Advanced open-source database with full SQL compliance
- **Oracle**: Enterprise database system
- **Microsoft SQL Server**: Enterprise database with multiple versions (mssql, mssql2, mssql3, mssql4)
- **Firebird**: Open-source SQL relational database
- **DB2**: IBM enterprise database
- **Informix**: IBM database system (versions 9+ and SE)
- **Ingres**: Open-source database
- **Teradata**: Data warehouse platform

### Experimental/NoSQL Databases
- **MongoDB**: Document-oriented NoSQL database
- **CouchDB**: Document-oriented database
- **Google App Engine**: Both datastore (NoSQL) and SQL variants
- **IMAP**: Email server protocol support

### Connection URI Examples
```python
# SQLite variants
'sqlite://test.db'
'spatialite://test.db'
'sqlite:memory'

# MySQL
'mysql://root:password@localhost/database'

# PostgreSQL with different drivers
'postgres://user:password@localhost/database'
'postgres:psycopg2://user:password@localhost/database'
'postgres:pg8000://user:password@localhost/database'

# SQL Server variants
'mssql://user:password@server/database'
'mssql2://user:password@server/database'  # alternate mappings
'mssql3://user:password@server/database'  # better pagination (>=2005)
'mssql4://user:password@server/database'  # best pagination (>=2012)

# NoSQL and Cloud
'google:datastore'  # Google App Engine datastore
'mongodb://user:password@server:port/database'
```

## Core Classes

### MetaDAL
Metaclass for the DAL class that provides customization capabilities:

#### Intercepted Parameters
```python
intercepts = [
    "logger",        # Custom logging instance
    "representers",  # Data representation handlers
    "serializers",   # Data serialization handlers
    "uuid",          # UUID generation function
    "validators",    # Field validation functions
    "validators_method",  # Validation method selector
    "Table",         # Custom Table class
    "Row",          # Custom Row class
]
```

**Functionality:**
- Intercepts constructor arguments for class-level customization
- Sets intercepted values as class attributes
- Enables runtime customization of DAL behavior

### DAL Class
Main database abstraction layer class providing unified database interface.

#### Inheritance
```python
class DAL(with_metaclass(MetaDAL, Serializable, BasicStorage)):
```
- **MetaDAL**: Custom metaclass for parameter interception
- **Serializable**: Provides serialization capabilities
- **BasicStorage**: Enhanced dictionary-like storage

#### Key Attributes
```python
serializers = None           # Data serialization handlers
validators = None            # Custom validation functions
representers = {}           # Data representation handlers
validators_method = default_validators  # Default validation method
uuid = lambda x: str(uuid4())  # UUID generation function
logger = logging.getLogger("pyDAL")  # Logger instance

# Core classes
Field = Field               # Field definition class
Table = Table              # Table definition class
Rows = Rows               # Query result set class
Row = Row                 # Single record class

# Record operations
record_operators = {
    "update_record": RecordUpdater,
    "delete_record": RecordDeleter
}

# Execution handlers
execution_handlers = [TimingHandler]
```

#### Constructor Parameters

**Basic Connection:**
- **uri** (str): Database connection string (default: `'sqlite://dummy.db'`)
- **pool_size**: Number of concurrent database connections
- **folder**: Directory for .table files (auto-set in web2py)

**Encoding and Hashing:**
- **db_codec**: Database string encoding (default: 'UTF-8')
- **table_hash**: Database identifier for .tables files

**Validation:**
- **check_reserved**: SQL keyword validation
  - `'common'`: Common SQL keywords across all databases
  - `'all'`: All known SQL keywords
  - `'<adaptername>'`: Adapter-specific keywords
  - `'<adaptername>_nonreserved'`: Non-reserved keywords

**Migration Control:**
- **migrate**: Default migration behavior for all tables
- **fake_migrate**: Default fake migration behavior
- **migrate_enabled**: Global migration enable/disable
- **fake_migrate_all**: Force fake migration for all tables

**Advanced Options:**
- **attempts**: Connection retry attempts
- **auto_import**: Automatic table definition import
- **bigint_id**: Use bigint instead of int for ID fields
- **lazy_tables**: Delay table definition until access
- **after_connection**: Callback executed after connection

#### Instance Management
Uses thread-local storage for instance management:

```python
THREAD_LOCAL._pydal_db_instances_        # Active instances
THREAD_LOCAL._pydal_db_instances_zombie_ # Zombie instances
```

**Instance Lifecycle:**
1. **Creation**: Instances stored in thread-local storage
2. **Zombie Mode**: Special `<zombie>` URI for instance recovery
3. **UID Management**: Unique identifier based on URI hash
4. **Cleanup**: Automatic cleanup on close()

## Key Methods

### Database Operations

#### executesql()
Executes arbitrary SQL queries with advanced result handling:

**Parameters:**
- **query** (str): SQL query to execute
- **placeholders**: Parameter substitution (sequence or dict)
- **as_dict** (bool): Return results as dictionaries
- **fields**: DAL Field objects for result parsing
- **colnames**: Column names in tablename.fieldname format
- **as_ordered_dict** (bool): Ordered dictionary results

**Features:**
- **Raw SQL Support**: Execute any SQL statement
- **Parameter Binding**: Safe parameter substitution
- **Result Conversion**: Convert to DAL Rows objects
- **Dictionary Results**: Key-value result format
- **Field Mapping**: Map results to DAL fields

#### Connection Management

##### close()
Closes database connection and cleans up resources:
- Calls adapter close() method
- Removes instance from thread-local storage
- Cleans adapter thread-local data

## Table Arguments
Supported arguments for `define_table()`:

```python
TABLE_ARGS = {
    "migrate",        # Enable/disable migration
    "primarykey",     # Custom primary key definition
    "fake_migrate",   # Fake migration flag
    "format",         # Record representation format
    "redefine",       # Allow table redefinition
    "singular",       # Singular form name
    "plural",         # Plural form name
    "trigger_name",   # Custom trigger name
    "sequence_name",  # Custom sequence name
    "fields",         # Field list override
    "common_filter",  # Default query filter
    "polymodel",      # Inheritance support
    "table_class",    # Custom table class
    "on_define",      # Definition callback
    "rname",          # Real table name
}
```

## Usage Examples

### Basic Usage
```python
# Create database connection
db = DAL('sqlite://test.db')

# Define table
person = db.define_table('person', Field('name', 'string'))

# Insert record
id = person.insert(name='James')

# Query records
james = person(id)                    # By ID
james = person(name='James')          # By field
query = (person.name == 'James')      # Complex query
people = db(query).select()           # Execute query

# Update records
james.update_record(name='Jim')       # Single record
db(person.name.like('J%')).update(name='James')  # Multiple records

# Delete records
james.delete_record()                 # Single record
db(person.name == 'Jim').delete()     # Multiple records
```

### Advanced Features
```python
# Custom validation
db = DAL('sqlite://test.db', 
         check_reserved=['common'],
         migrate=False)

# Raw SQL execution
results = db.executesql('SELECT * FROM person', as_dict=True)

# Connection pooling
db = DAL('mysql://user:pass@host/db', pool_size=10)

# Custom UUID generation
db = DAL('postgres://user:pass@host/db', 
         uuid=lambda: str(uuid4()).replace('-', ''))
```

## Integration Points

### Adapter Architecture
- **BaseAdapter**: Common database adapter interface
- **Dialect System**: SQL dialect handling per database
- **Connection Pooling**: Multi-connection management
- **Transaction Support**: ACID transaction handling

### Field and Table System
- **Field Types**: Comprehensive type system
- **Validation**: Built-in and custom validators
- **Representation**: Data display formatting
- **Relationships**: Foreign keys and references

### Query Engine
- **Expression Building**: Pythonic query construction
- **SQL Generation**: Automatic SQL generation
- **Result Processing**: Unified result handling
- **Optimization**: Query optimization and caching

## Thread Safety
- Thread-local instance storage
- Global locking for critical operations
- Per-thread connection management
- Safe concurrent access patterns

## Notes
- Central component of PyDAL architecture
- Provides unified interface across all database types
- Handles connection lifecycle and resource management
- Supports both ORM-style and raw SQL operations
- Thread-safe design for web application deployment
- Extensive customization through metaclass and parameters