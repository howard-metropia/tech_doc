# drivers.py

## Overview
Database driver discovery and registration module for PyDAL that dynamically detects available database drivers and maintains a registry for adapter selection.

## Global Registry
```python
DRIVERS = {}
```
Central dictionary containing all successfully imported database drivers, keyed by driver name.

## Driver Categories

### Google App Engine (GAE)
Special handling for Google App Engine environment:

```python
from ._gae import gae

if gae is not None:
    DRIVERS["google"] = gae
    # Set other drivers to None in GAE environment
    psycopg2_adapt = None
    cx_Oracle = None
    pyodbc = None
    couchdb = None
    is_jdbc = False
```

**GAE Behavior:**
- When GAE is available, other drivers are disabled
- Prevents conflicts in GAE sandbox environment
- Uses GAE-specific datastore and SQL interfaces

### SQLite Drivers

#### SQLite2 (Legacy)
```python
try:
    from pysqlite2 import dbapi2 as sqlite2
    DRIVERS["sqlite2"] = sqlite2
except ImportError:
    pass
```

#### SQLite3 (Standard)
```python
try:
    from sqlite3 import dbapi2 as sqlite3
    DRIVERS["sqlite3"] = sqlite3
except ImportError:
    pass
```

**SQLite Features:**
- File-based and in-memory databases
- No server setup required
- ACID transactions
- Cross-platform compatibility

### MySQL Drivers

#### PyMySQL (Pure Python)
```python
try:
    import pymysql
    DRIVERS["pymysql"] = pymysql
except ImportError:
    pass
```

#### MySQLdb (C Extension)
```python
try:
    import MySQLdb
    DRIVERS["MySQLdb"] = MySQLdb
except ImportError:
    pass
```

#### MySQL Connector (Official)
```python
try:
    import mysql.connector as mysqlconnector
    DRIVERS["mysqlconnector"] = mysqlconnector
except ImportError:
    pass
```

**MySQL Driver Selection:**
- **PyMySQL**: Pure Python, easier installation
- **MySQLdb**: C extension, better performance
- **mysql.connector**: Official Oracle driver

### PostgreSQL Drivers

#### psycopg2 (Primary)
```python
try:
    import psycopg2
    from psycopg2.extensions import adapt as psycopg2_adapt
    DRIVERS["psycopg2"] = psycopg2
except ImportError:
    psycopg2_adapt = None
```

**Features:**
- Most popular PostgreSQL driver
- Advanced features support
- Connection pooling
- Custom type adapters

### Oracle Drivers

#### cx_Oracle
```python
try:
    import cx_Oracle
    DRIVERS["cx_Oracle"] = cx_Oracle
except ImportError:
    cx_Oracle = None
```

**Oracle Support:**
- Enterprise database connectivity
- Advanced Oracle features
- PL/SQL support
- Large object handling

### ODBC Drivers

#### PyODBC (Primary)
```python
try:
    import pyodbc
    DRIVERS["pyodbc"] = pyodbc
except ImportError:
    try:
        import pypyodbc as pyodbc
        DRIVERS["pyodbc"] = pyodbc
    except ImportError:
        pyodbc = None
```

**ODBC Support:**
- Universal database connectivity
- Windows-centric but cross-platform
- Supports multiple databases:
  - DB2
  - Teradata
  - Ingres
  - SQL Server
  - And many others

### IBM Databases

#### DB2 Support
```python
try:
    import ibm_db_dbi
    DRIVERS["ibm_db_dbi"] = ibm_db_dbi
except ImportError:
    pass
```

#### Sybase Support
```python
try:
    import Sybase
    DRIVERS["Sybase"] = Sybase
except ImportError:
    pass
```

### Firebird Drivers

#### kinterbasdb (Legacy)
```python
try:
    import kinterbasdb
    DRIVERS["kinterbasdb"] = kinterbasdb
except ImportError:
    pass
```

#### fdb (Modern)
```python
try:
    import fdb
    DRIVERS["fdb"] = fdb
except ImportError:
    pass
```

#### firebirdsql (Alternative)
```python
try:
    import firebirdsql
    DRIVERS["firebirdsql"] = firebirdsql
except ImportError:
    pass
```

**Firebird Evolution:**
- **kinterbasdb**: Original driver
- **fdb**: Modern replacement
- **firebirdsql**: Pure Python alternative

### Experimental/Specialized Drivers

#### Informix
```python
try:
    import informixdb
    DRIVERS["informixdb"] = informixdb
except ImportError:
    pass
```

#### SAP DB
```python
try:
    import sapdb
    DRIVERS["sapdb"] = sapdb
except ImportError:
    pass
```

#### Cubrid
```python
try:
    import cubriddb
    DRIVERS["cubriddb"] = cubriddb
except ImportError:
    pass
```

### JDBC Support (Jython)
```python
try:
    from com.ziclix.python.sql import zxJDBC
    import java.sql
    from org.sqlite import JDBC
    
    zxJDBC_sqlite = java.sql.DriverManager
    DRIVERS["zxJDBC"] = zxJDBC
    is_jdbc = True
except ImportError:
    is_jdbc = False
```

**Jython/JDBC Features:**
- Java database connectivity in Jython
- Access to all JDBC drivers
- Enterprise Java integration
- SQLite JDBC driver included

### NoSQL/Document Databases

#### CouchDB
```python
try:
    import couchdb
    DRIVERS["couchdb"] = couchdb
except ImportError:
    couchdb = None
```

#### MongoDB
```python
try:
    import pymongo
    DRIVERS["pymongo"] = pymongo
except:
    pass
```

### Protocol-Based Drivers

#### IMAP
```python
try:
    import imaplib
    DRIVERS["imaplib"] = imaplib
except:
    pass
```

#### TDS (SQL Server)
```python
try:
    import pytds
    DRIVERS["pytds"] = pytds
except:
    pass
```

## Driver Selection Strategy

### Import Pattern
All drivers use the same pattern:
```python
try:
    import driver_module
    DRIVERS["driver_name"] = driver_module
except ImportError:
    pass  # or set to None
```

**Benefits:**
- Graceful handling of missing drivers
- No hard dependencies
- Runtime driver availability detection
- Optional driver installation

### Fallback Mechanisms
Some drivers have fallback options:
- **pyodbc → pypyodbc**: Pure Python ODBC fallback
- **sqlite3 → pysqlite2**: SQLite version fallback
- Multiple Firebird drivers available

## Usage in PyDAL

### Adapter Selection
PyDAL adapters use the DRIVERS registry to check availability:
```python
if "psycopg2" in DRIVERS:
    # Use PostgreSQL adapter
    pass
elif "pyodbc" in DRIVERS:
    # Use ODBC adapter for PostgreSQL
    pass
```

### Runtime Detection
Applications can check driver availability:
```python
from pydal.drivers import DRIVERS

if "pymysql" in DRIVERS:
    print("MySQL support available")
```

### Error Handling
Missing drivers result in informative error messages when connection is attempted.

## Driver Categories by Use Case

### Production Databases
- **PostgreSQL**: psycopg2
- **MySQL**: MySQLdb, pymysql, mysqlconnector
- **Oracle**: cx_Oracle
- **SQL Server**: pyodbc, pytds

### Development/Testing
- **SQLite**: sqlite3, pysqlite2
- **In-Memory**: SQLite memory databases

### Enterprise Integration
- **ODBC**: pyodbc (universal connectivity)
- **JDBC**: zxJDBC (Jython environments)
- **IBM**: ibm_db_dbi (DB2)

### Cloud Platforms
- **Google App Engine**: gae
- **CouchDB**: couchdb (document storage)
- **MongoDB**: pymongo (document storage)

### Specialized Use Cases
- **Email**: imaplib (email as database)
- **Legacy**: Various specialized drivers

## Notes
- Provides foundation for PyDAL's multi-database support
- Enables "soft dependencies" - PyDAL works with whatever drivers are available
- Supports development with SQLite and production with enterprise databases
- Graceful degradation when drivers are unavailable
- Essential for PyDAL's "write once, run anywhere" philosophy