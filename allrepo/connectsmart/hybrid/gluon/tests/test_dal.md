# test_dal.py

## Overview
This file contains unit tests for the web2py Database Abstraction Layer (DAL). It tests DAL functionality, serialization capabilities, and integration with PyDAL (the standalone DAL package). The tests ensure proper database operations and compatibility across different database backends.

## Purpose
- Tests DAL subclass functionality and integration
- Validates serialization and deserialization of database objects
- Tests PyDAL integration and compatibility
- Verifies database adapter functionality across different backends
- Tests database operations and result set handling

## Key Classes and Methods

### Module Functions

#### `tearDownModule()`
Module-level cleanup that removes temporary database files:
- Removes `dummy.db` test database file

#### `_prepare_exec_for_file(filename)`
Utility function for preparing module execution from file paths.

**Parameters:**
- `filename` (str) - Path to Python file or module

**Functionality:**
- **Module Path Resolution**: Converts file paths to module import paths
- **Package Detection**: Identifies package structure using `__init__.py` files
- **Path Manipulation**: Handles both file and directory paths
- **Import Preparation**: Prepares proper module names for dynamic import

#### `load_pydal_tests_module()`
Loads the PyDAL test module for integration testing.

**Process:**
- **Path Discovery**: Locates web2py root directory
- **PyDAL Location**: Finds PyDAL tests in packages directory
- **Module Import**: Dynamically imports PyDAL test module
- **Integration**: Provides access to PyDAL test suite

#### `pydal_suite()`
Creates a test suite from PyDAL test modules.

**Suite Creation:**
- **Test Discovery**: Finds all test classes in PyDAL module
- **Suite Assembly**: Creates unified test suite
- **Class Filtering**: Filters classes that start with "Test"
- **Suite Integration**: Adds all test cases to unified suite

### TestDALSubclass Class
Tests core DAL functionality and integration.

#### Test Methods

##### `testRun(self)`
Tests basic DAL functionality and default configurations.

**Serializer Testing:**
- **JSON Serializer**: Validates `db.serializers["json"]` uses `custom_json`
- **XML Serializer**: Validates `db.serializers["xml"]` uses `xml`
- **Default Assignment**: Ensures proper default serializer assignment

**Representer Testing:**
- **Rows Render**: Validates `db.representers["rows_render"]` uses `sqlhtml.represent`
- **Rows XML**: Validates `db.representers["rows_xml"]` uses `sqlhtml.SQLTABLE`
- **Integration**: Tests integration with HTML generation components

**Database Operations:**
```python
db = DAL(check_reserved=["all"])
# Tests default configurations
db.close()
```

##### `testSerialization(self)`
Tests serialization and deserialization of database objects.

**Database Setup:**
```python
db = DAL("sqlite:memory", check_reserved=["all"])
db.define_table("t_a", Field("f_a"))
db.t_a.insert(f_a="test")
```

**Serialization Process:**
- **Cacheable Select**: Creates cacheable result set using `cacheable=True`
- **Pickle Serialization**: Serializes result set using `pickle.dumps()`
- **Deserialization**: Deserializes using `pickle.loads()`
- **Integrity Check**: Validates deserialized object maintains database reference

**Validation:**
- **Database Reference**: Ensures `a.db == b.db` after serialization
- **Data Integrity**: Validates data consistency across serialization
- **Object State**: Ensures object state is preserved

### TestDALAdapters Class
Tests database adapter functionality across different backends.

#### Test Methods

##### `_run_tests(self)`
Runs the complete PyDAL test suite.

**Test Execution:**
- **Suite Creation**: Creates PyDAL test suite
- **Test Runner**: Executes tests with verbose output
- **Result Collection**: Collects and returns test results

##### `test_mysql(self)`
Tests MySQL database adapter functionality.

**Environment Checks:**
- **AppVeyor Skip**: Skips test on AppVeyor CI environment
- **Travis Configuration**: Sets up MySQL connection for Travis CI

**MySQL Testing:**
```python
if os.environ.get("TRAVIS"):
    os.environ["DB"] = "mysql://root:@localhost/pydal"
    result = self._run_tests()
    self.assertTrue(result)
```

**Test Coverage:**
- **Connection Testing**: Tests MySQL database connection
- **CRUD Operations**: Tests Create, Read, Update, Delete operations
- **Data Types**: Tests various MySQL data types
- **Performance**: Tests query performance and optimization

## Dependencies
- `unittest` - Python testing framework
- `os` - Operating system interface
- `sys` - System-specific parameters
- `gluon.dal` - Database Abstraction Layer
- `gluon._compat.pickle` - Compatibility pickle module
- `gluon.serializers` - Data serialization utilities
- `gluon.sqlhtml` - SQL HTML integration

## DAL Components Tested

### Core DAL Functionality
- **Database Connection**: Connection management and configuration
- **Table Definition**: Table creation and field specification
- **CRUD Operations**: Basic database operations
- **Result Sets**: Query result handling and manipulation

### Serialization System
- **JSON Serialization**: Custom JSON serialization for database objects
- **XML Serialization**: XML representation of database data
- **Pickle Support**: Python object serialization for caching
- **Result Set Serialization**: Cacheable result set handling

### Integration Components
- **HTML Integration**: Integration with HTML generation (sqlhtml)
- **Template Integration**: Integration with template system
- **Form Integration**: Integration with form generation
- **Validation Integration**: Integration with validation system

### Database Adapters
- **SQLite**: Default adapter for development and testing
- **MySQL**: Production database adapter
- **PostgreSQL**: Advanced database features (via PyDAL)
- **Other Adapters**: Various database backend support

## Usage Example
```python
from gluon.dal import DAL, Field

# Basic database setup
db = DAL("sqlite://storage.sqlite", check_reserved=["all"])

# Table definition
db.define_table("users",
    Field("name", "string", length=50),
    Field("email", "string"),
    Field("created_on", "datetime", default=request.now)
)

# CRUD operations
user_id = db.users.insert(name="John Doe", email="john@example.com")
user = db.users[user_id]
db(db.users.id == user_id).update(email="newemail@example.com")

# Cacheable queries
users = db(db.users.id > 0).select(cacheable=True)

# Serialization
import pickle
serialized = pickle.dumps(users)
deserialized = pickle.loads(serialized)

db.close()
```

## Integration with web2py Framework

### Model Integration
- **Model Loading**: Automatic model loading and table definition
- **Relationship Management**: Foreign key and relationship handling
- **Validation Integration**: Field validation and constraint checking
- **Migration Support**: Automatic schema migration and updates

### Controller Integration
- **Query Building**: Intuitive query construction
- **Result Processing**: Easy result set manipulation
- **Transaction Management**: Automatic transaction handling
- **Error Handling**: Comprehensive error reporting

### View Integration
- **Template Variables**: Easy access to database objects in templates
- **Form Generation**: Automatic form generation from database tables
- **HTML Representation**: Automatic HTML representation of data
- **AJAX Support**: Seamless AJAX integration for database operations

### Caching Integration
- **Query Caching**: Automatic query result caching
- **Object Serialization**: Cacheable database objects
- **Performance Optimization**: Reduced database load through caching
- **Cache Invalidation**: Automatic cache management

## Test Coverage
- **Core DAL**: Basic database operations and functionality
- **Serialization**: Object serialization and deserialization
- **Adapter Testing**: Database adapter functionality
- **Integration**: Integration with web2py components
- **PyDAL Compatibility**: Compatibility with standalone PyDAL
- **Error Handling**: Proper error handling and recovery

## Expected Results
- **Database Operations**: Should execute without errors
- **Serialization**: Objects should serialize and deserialize correctly
- **Adapter Tests**: Database adapters should pass all tests
- **Integration**: Should integrate properly with web2py components
- **Performance**: Should provide efficient database operations

## File Structure
```
gluon/tests/
├── test_dal.py           # This file
└── ... (other test files)

gluon/packages/dal/
├── tests/               # PyDAL test suite
│   └── __init__.py      # PyDAL test initialization
└── ... (PyDAL modules)
```

This test suite ensures the web2py DAL provides reliable, efficient, and compatible database abstraction functionality across different database backends and integration scenarios.