# PyDAL Microsoft SQL Server Dialect

## Overview
The MSSQL dialect provides T-SQL generation optimized for Microsoft SQL Server, supporting SQL Server-specific features and performance optimizations.

## Key Features

### T-SQL Support
```python
class MSSQLDialect(BaseDialect):
    """
    Microsoft SQL Server dialect
    
    Features:
    - T-SQL syntax support
    - Common table expressions
    - Window functions
    - MERGE statements
    """
```

### SQL Server Functions
```python
MSSQL_FUNCTIONS = {
    'SUBSTRING': 'SUBSTRING({0}, {1}, {2})',
    'LEN': 'LEN({0})',
    'ISNULL': 'ISNULL({0}, {1})',
    'GETDATE': 'GETDATE()',
    'DATEADD': 'DATEADD({0}, {1}, {2})',
    'DATEDIFF': 'DATEDIFF({0}, {1}, {2})'
}
```

### Advanced Features
- **CTEs**: Common table expressions
- **MERGE**: Upsert operations
- **TOP**: Result limiting
- **OUTPUT**: Returning data from modifications

### Performance Optimization
- **Index Hints**: WITH (INDEX=...) hints
- **Query Store**: Performance insights
- **Execution Plans**: Query optimization
- **Columnstore**: In-memory analytics

This dialect maximizes SQL Server performance through T-SQL optimization and enterprise features.