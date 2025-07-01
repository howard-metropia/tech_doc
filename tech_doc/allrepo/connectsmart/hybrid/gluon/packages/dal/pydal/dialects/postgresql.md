# PyDAL PostgreSQL Dialect

## Overview
The PostgreSQL dialect provides advanced SQL generation optimized for PostgreSQL's rich feature set, including arrays, JSON, full-text search, and window functions.

## Key Features

### PostgreSQL-Specific SQL
```python
class PostgreSQLDialect(BaseDialect):
    """
    PostgreSQL database dialect
    
    Features:
    - Array data types
    - JSON/JSONB operations
    - Full-text search
    - Window functions
    - Common table expressions
    """
```

### Advanced Data Types
- **Arrays**: Native array support with operators
- **JSON/JSONB**: Document operations and indexing
- **UUID**: Native UUID data type
- **Geometric Types**: Point, line, polygon support
- **Network Types**: INET, CIDR address types

### PostgreSQL Functions
```python
POSTGRESQL_FUNCTIONS = {
    'EXTRACT': 'EXTRACT({0} FROM {1})',
    'SUBSTRING': 'SUBSTRING({0} FROM {1} FOR {2})',
    'REGEXP_REPLACE': 'REGEXP_REPLACE({0}, {1}, {2})',
    'ARRAY_AGG': 'ARRAY_AGG({0})',
    'JSON_EXTRACT': '{0}->{1}',
    'JSONB_EXTRACT': '{0}->>{1}'
}
```

### Query Optimization
- **Partial Indexes**: Conditional index support
- **Expression Indexes**: Function-based indexes
- **GIN/GiST Indexes**: Advanced indexing strategies
- **Query Planner**: EXPLAIN plan optimization

### Advanced Features
- **CTEs**: Common table expressions with recursion
- **Window Functions**: OVER clause analytics
- **Full-Text Search**: tsvector and tsquery
- **Lateral Joins**: Correlated subqueries in FROM

This dialect leverages PostgreSQL's advanced capabilities for high-performance applications requiring sophisticated data operations.