# Gluon Contrib PyPyODBC Module

## Overview
Pure Python ODBC database connectivity module for web2py applications. Provides database access to ODBC-compatible databases without requiring compiled extensions, making it ideal for environments where traditional ODBC drivers are difficult to install.

## Module Information
- **Module**: `gluon.contrib.pypyodbc`
- **Purpose**: ODBC database connectivity
- **Dependencies**: None (pure Python)
- **Compatibility**: Cross-platform ODBC access

## Key Features
- **Pure Python**: No compiled extensions required
- **ODBC Compatibility**: Works with any ODBC-compliant database
- **Cross-platform**: Windows, Linux, macOS support
- **Multiple Databases**: SQL Server, Oracle, MySQL, PostgreSQL support
- **Connection Pooling**: Efficient connection management

## Basic Usage

### Database Connection
```python
import pypyodbc

# SQL Server connection
conn = pypyodbc.connect(
    'Driver=SQL Server;'
    'Server=localhost;'
    'Database=mydb;'
    'UID=username;'
    'PWD=password;'
)

# Execute queries
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
results = cursor.fetchall()
```

### Web2py Integration
```python
# In models/db.py
db = DAL('mssql4://username:password@server/database', 
         adapter_args={'driver': 'pypyodbc'})
```

This module enables ODBC database connectivity for web2py applications using pure Python implementation.