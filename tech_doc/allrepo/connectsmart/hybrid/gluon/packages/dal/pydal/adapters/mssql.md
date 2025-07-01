# PyDAL Microsoft SQL Server Adapter

## Overview
The MSSQL adapter provides comprehensive support for Microsoft SQL Server databases, enabling PyDAL applications to leverage SQL Server's enterprise features and capabilities.

## Key Features

### SQL Server Integration
```python
class MSSQLAdapter(BaseAdapter):
    """
    Microsoft SQL Server adapter for PyDAL
    
    Features:
    - T-SQL support
    - Stored procedures and functions
    - Common table expressions
    - Window functions
    """
```

### Advanced SQL Features
- **T-SQL Extensions**: SQL Server specific syntax
- **CTEs**: Common table expressions and recursion
- **Window Functions**: OVER clause and analytics
- **MERGE Statements**: Upsert operations
- **XML Data Type**: Native XML support

### Data Types
```python
MSSQL_TYPES = {
    'string': 'NVARCHAR(255)',
    'text': 'NTEXT',
    'integer': 'INT',
    'bigint': 'BIGINT',
    'double': 'FLOAT',
    'decimal': 'DECIMAL(18,2)',
    'date': 'DATE',
    'datetime': 'DATETIME2',
    'time': 'TIME',
    'boolean': 'BIT',
    'uuid': 'UNIQUEIDENTIFIER',
    'xml': 'XML',
    'json': 'NVARCHAR(MAX)'
}
```

### Enterprise Features
- **Always On**: High availability and disaster recovery
- **Columnstore**: In-memory analytics
- **Row-Level Security**: Fine-grained access control
- **Temporal Tables**: System-versioned tables
- **In-Memory OLTP**: Memory-optimized tables

### Performance Optimization
- **Query Store**: Query performance insights
- **Automatic Tuning**: AI-powered optimization
- **Index Recommendations**: Intelligent indexing
- **Execution Plans**: Query optimization analysis

### Integration Capabilities
- **Active Directory**: Windows authentication
- **Azure Integration**: Cloud database services
- **Business Intelligence**: SSRS, SSIS, SSAS integration
- **JSON Support**: Native JSON functions

### Security Features
- **Transparent Data Encryption**: TDE support
- **Always Encrypted**: Column-level encryption
- **Dynamic Data Masking**: Sensitive data protection
- **Audit**: Comprehensive auditing capabilities

This adapter provides full enterprise database capabilities for applications requiring SQL Server's advanced features and Microsoft ecosystem integration.