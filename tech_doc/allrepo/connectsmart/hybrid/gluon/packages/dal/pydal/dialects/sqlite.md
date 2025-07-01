# PyDAL SQLite Dialect

## Overview
The SQLite dialect provides optimized SQL generation for SQLite databases, handling SQLite's unique characteristics and lightweight architecture.

## Key Features

### SQLite-Specific Adaptations
```python
class SQLiteDialect(BaseDialect):
    """
    SQLite database dialect
    
    Features:
    - Dynamic typing adaptation
    - PRAGMA optimization
    - FTS (Full-Text Search)
    - JSON1 extension support
    """
```

### SQLite Functions
```python
SQLITE_FUNCTIONS = {
    'SUBSTR': 'SUBSTR({0}, {1}, {2})',
    'REPLACE': 'REPLACE({0}, {1}, {2})',
    'DATETIME': 'DATETIME({0})',
    'STRFTIME': 'STRFTIME({0}, {1})',
    'JSON_EXTRACT': 'JSON_EXTRACT({0}, {1})'
}
```

### Unique Features
- **Dynamic Types**: Flexible column typing
- **WITHOUT ROWID**: Optimized table structure
- **FTS**: Full-text search capabilities
- **JSON1**: JSON processing extension

### Optimization Strategies
- **PRAGMA Settings**: Database optimization
- **Index Optimization**: Efficient indexing
- **Query Planning**: EXPLAIN query plan
- **WAL Mode**: Write-ahead logging

This dialect maximizes SQLite's performance while accommodating its lightweight, embedded nature.