# PyDAL Informix Adapter

## Overview
The Informix adapter provides enterprise connectivity to IBM Informix databases, supporting advanced features for high-performance transactional and analytical applications.

## Key Features

### Enterprise Database Integration
```python
class InformixAdapter(BaseAdapter):
    """
    IBM Informix database adapter for PyDAL
    
    Features:
    - High-performance OLTP
    - Time series data support
    - Spatial data handling
    - NoSQL JSON support
    """
```

### Data Types and Extensions
```python
INFORMIX_TYPES = {
    'string': 'VARCHAR(255)',
    'text': 'TEXT',
    'integer': 'INTEGER',
    'serial': 'SERIAL',
    'bigint': 'BIGINT',
    'decimal': 'DECIMAL(16,2)',
    'money': 'MONEY(16,2)',
    'date': 'DATE',
    'datetime': 'DATETIME YEAR TO FRACTION',
    'interval': 'INTERVAL',
    'boolean': 'BOOLEAN',
    'json': 'JSON'
}
```

### Advanced SQL Support
- **Time Series**: Native time series data types
- **Spatial SQL**: Geographic information systems
- **JSON Operations**: NoSQL document capabilities
- **Hierarchical Data**: Recursive queries and CTEs

### Performance Features
- **Parallel Processing**: Multi-threading query execution
- **Fragmentation**: Horizontal and vertical partitioning
- **Compression**: Data and index compression
- **Caching**: Intelligent buffer management

### Enterprise Capabilities
- **High Availability**: Clustering and replication
- **Security**: Role-based access control
- **Auditing**: Comprehensive audit trails
- **Monitoring**: Real-time performance metrics

This adapter leverages Informix's enterprise-grade features for demanding application environments requiring high performance and reliability.