# PyDAL SQLite Parser

## Overview
SQLite-specific parser that handles SQLite's unique SQL dialect and lightweight database features.

## Key Features

### SQLite SQL Parsing
```python
class SQLiteParser(BaseParser):
    """
    SQLite database parser
    
    Features:
    - SQLite dialect parsing
    - PRAGMA statement parsing
    - FTS query parsing
    - JSON1 extension parsing
    """
```

### SQLite Features
- **Dynamic Typing**: Flexible type system parsing
- **PRAGMA Commands**: Database configuration parsing
- **FTS Queries**: Full-text search parsing
- **JSON1**: JSON extension parsing
- **Virtual Tables**: Virtual table parsing

### Optimization
- **Query Planning**: EXPLAIN query plan analysis
- **Index Usage**: Index optimization analysis
- **Performance**: Efficient query generation
- **Memory Usage**: Memory-conscious parsing

This parser optimizes SQL parsing for SQLite's lightweight architecture and unique features.