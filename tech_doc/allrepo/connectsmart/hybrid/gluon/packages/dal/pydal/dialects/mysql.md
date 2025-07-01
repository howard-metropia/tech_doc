# PyDAL MySQL Dialect

## Overview
The MySQL dialect optimizes SQL generation for MySQL and MariaDB databases, supporting MySQL-specific syntax, storage engines, and performance features.

## Key Features

### MySQL-Specific Optimizations
```python
class MySQLDialect(BaseDialect):
    """
    MySQL/MariaDB database dialect
    
    Features:
    - Storage engine optimization
    - MySQL-specific functions
    - Index hints and optimization
    - Partitioning support
    """
```

### MySQL Functions
```python
MYSQL_FUNCTIONS = {
    'CONCAT': 'CONCAT({0})',
    'SUBSTRING': 'SUBSTRING({0}, {1}, {2})',
    'DATE_FORMAT': 'DATE_FORMAT({0}, {1})',
    'IFNULL': 'IFNULL({0}, {1})',
    'LIMIT': 'LIMIT {0}, {1}'
}
```

### Storage Engine Support
- **InnoDB**: Transaction support and foreign keys
- **MyISAM**: High-performance read operations
- **Memory**: In-memory table storage
- **Archive**: Compressed archival storage

### Performance Features
- **Index Hints**: USE/FORCE/IGNORE INDEX
- **Query Cache**: Result caching optimization
- **Partitioning**: Table partitioning strategies
- **Replication**: Master-slave optimization

This dialect provides optimal MySQL performance through database-specific SQL generation and optimization strategies.