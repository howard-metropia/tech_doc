# migrator.py

## Overview
Database migration engine for PyDAL that handles automatic schema creation, table alterations, and migration management across different database backends with support for both real and fake migrations.

## Core Class: Migrator

### Initialization
```python
class Migrator(object):
    def __init__(self, adapter):
        self.adapter = adapter
```

### Key Properties
```python
@property
def db(self):
    return self.adapter.db

@property
def dialect(self):
    return self.adapter.dialect

@property
def dbengine(self):
    return self.adapter.dbengine
```

## Main Migration Methods

### create_table()
Primary method for table creation and migration management.

#### Parameters
- **table**: PyDAL Table object to create/migrate
- **migrate** (bool): Enable migration tracking (default: True)
- **fake_migrate** (bool): Perform fake migration (metadata only)
- **polymodel**: Inheritance model specification

#### Process Flow

##### 1. Field Analysis
```python
fields = []
postcreation_fields = []  # PostGIS geometry fields
sql_fields = {}          # Migration metadata
sql_fields_aux = {}      # Creation SQL
TFK = {}                 # Table-level foreign keys
```

##### 2. Field Type Processing
For each field in the table:
- **Custom Types**: Handle SQLCustomType fields
- **References**: Process foreign key relationships
  - `reference` and `big-reference` field types
  - Self-references (referenced = ".")
  - Cross-table references with table.field syntax
  - Multi-column primary key references

##### 3. Foreign Key Resolution
```python
# Reference field processing
if field_type.startswith(("reference", "big-reference")):
    referenced = field_type[10:].strip()  # or [14:] for big-reference
    
    # Resolve referenced table and field
    rtable = db[referenced]
    rfield = rtable._id
    
    # Handle multi-column foreign keys
    if len(rtable._primarykey) > 1:
        TFK[rtablename][rfieldname] = field_name
```

##### 4. SQL Generation
- **Field Definitions**: Generate SQL field definitions
- **Constraints**: Add primary key and foreign key constraints
- **Database-Specific**: Handle engine-specific requirements

```python
# MySQL-specific handling
if self.dbengine == "mysql":
    if not hasattr(table, "_primarykey"):
        fields.append("PRIMARY KEY (%s)" % (table._id._rname))
    engine = self.adapter.adapter_args.get("engine", "InnoDB")
    other = " ENGINE=%s CHARACTER SET utf8;" % engine
```

##### 5. Migration File Management
- **SQLite Memory**: No migration files for in-memory databases
- **Custom Migration**: Support for custom migration file paths
- **Default Location**: Use database hash and table name

```python
if isinstance(migrate, string_types):
    table._dbt = pjoin(dbpath, migrate)
else:
    table._dbt = pjoin(dbpath, "%s_%s.table" % (db._uri_hash, tablename))
```

## Migration Detection and Execution

### Field Comparison
The migrator compares current field definitions with stored metadata:

#### Metadata Structure
```python
sql_fields[field_name] = dict(
    length=field.length,
    unique=field.unique,
    notnull=field.notnull,
    sortable=sortable,
    type=str(field_type),
    sql=ftype,
    rname=field._rname,
    raw_rname=field._raw_rname,
)
```

### Migration Scenarios

#### 1. New Fields
When fields are added to existing tables:
```python
# Standard databases
query = [
    "ALTER TABLE %s ADD %s %s;" % (
        table._rname,
        sql_fields[key]["rname"],
        sql_fields_aux[key]["sql"]
    )
]

# SQLite special handling (no ALTER COLUMN support)
if self.dbengine in ("sqlite", "spatialite"):
    # Use ADD column approach with data copying
```

#### 2. Field Renaming
When field names change:
```python
# Add new column
"ALTER TABLE %s ADD %s %s;" % (table._rname, new_rname, field_sql)
# Copy data from old to new
"UPDATE %s SET %s=%s;" % (table._rname, new_rname, old_rname)
# Drop old column
drop_expr % (table._rname, old_rname)
```

#### 3. Field Type Changes
For fields with changed types (excluding certain types):
```python
# SQLite approach: use temporary column
key_tmp = self.dialect.quote(key + "__tmp")
query = [
    "ALTER TABLE %s ADD %s %s;" % (table._rname, key_tmp, new_sql),
    "UPDATE %s SET %s=%s;" % (table._rname, key_tmp, old_rname),
    drop_expr % (table._rname, old_rname),
    "ALTER TABLE %s ADD %s %s;" % (table._rname, new_rname, new_sql),
    "UPDATE %s SET %s=%s;" % (table._rname, new_rname, key_tmp),
    drop_expr % (table._rname, key_tmp),
]
```

#### 4. Field Removal
When fields are deleted:
```python
# Standard removal
query = [drop_expr % (table._rname, old_field_rname)]

# PostGIS geometry fields
if ftype.startswith("geometry"):
    query = [
        "SELECT DropGeometryColumn ('%s', '%s', '%s');" % (
            schema, table._raw_rname, field_raw_rname
        )
    ]
```

## File Operations

### Migration File Format
Migration files store pickled metadata:
```python
# Save migration metadata
with portalocker.LockedFile(table._dbt, "wb", timeout=60) as f:
    pickle.dump(sql_fields_current, f)
```

### File Locking
Uses portalocker for thread-safe file operations:
- Prevents concurrent migration conflicts
- Ensures atomic metadata updates
- Handles file system race conditions

### Logging
Comprehensive logging of migration operations:
```python
def log(self, message, table):
    if table._dbt:
        with portalocker.LockedFile(table._dbt + ".sql", "ab", timeout=60) as f:
            f.write(to_bytes(message))
```

## Database-Specific Handling

### SQLite Limitations
- No ALTER COLUMN support
- Use ADD column + UPDATE + DROP column pattern
- Special handling for field type changes

### PostgreSQL Features
- PostGIS geometry fields added after table creation
- Specialized geometry column removal
- Advanced constraint support

### MySQL Features
- Engine specification (InnoDB, MyISAM)
- Character set specification
- Custom primary key handling

## Migration Types

### Real Migration (migrate=True)
- Creates actual database tables
- Executes DDL statements
- Modifies database schema
- Tracks changes in migration files

### Fake Migration (fake_migrate=True)
- Updates migration metadata only
- No actual database changes
- Useful for production deployments
- Synchronizes metadata with existing schema

### No Migration (migrate=False)
- Returns SQL statements without execution
- Useful for manual schema management
- SQL generation without database impact

## Error Handling

### Reference Resolution
- Validates referenced tables exist
- Handles table.field syntax
- Provides detailed error messages for invalid references

### Constraint Validation
- Checks foreign key compatibility
- Validates multi-column foreign key consistency
- Ensures proper ON DELETE action consistency

### File System Operations
- Graceful handling of file locking failures
- Automatic retry mechanisms
- Path encoding handling for cross-platform compatibility

## Integration Points

### Adapter Integration
- Works with all PyDAL database adapters
- Uses adapter-specific SQL dialects
- Leverages adapter type mappings

### Field System Integration
- Processes all PyDAL field types
- Handles custom field types
- Supports field validation and constraints

### Transaction Support
- Migration operations are transactional where supported
- Rollback capabilities for failed migrations
- Atomic schema changes

## Usage Examples

### Basic Migration
```python
# Create table with migration
table = db.define_table('users',
    Field('name', 'string'),
    migrate=True
)
```

### Fake Migration
```python
# Update metadata without schema changes
table = db.define_table('users',
    Field('name', 'string'),
    fake_migrate=True
)
```

### Custom Migration File
```python
# Use specific migration file
table = db.define_table('users',
    Field('name', 'string'),
    migrate='custom_users_migration.table'
)
```

## Notes
- Central component of PyDAL's automatic schema management
- Enables zero-downtime deployments with fake migrations
- Provides cross-database compatibility for schema operations
- Essential for development-to-production workflows
- Handles complex scenarios like field renaming and type changes
- Critical for maintaining database schema evolution over time