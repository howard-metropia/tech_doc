# indexes.py

## Overview
This file contains comprehensive tests for PyDAL's index management functionality, validating index creation, modification, and performance impact across different database systems.

## Purpose
- Tests database index creation and management
- Validates index types and options
- Verifies index performance improvements
- Ensures cross-database index compatibility

## Key Features Tested

### Index Types
- **Primary Key**: Automatic primary key indexes
- **Unique Index**: Uniqueness constraint indexes
- **Composite Index**: Multi-column indexes
- **Full-text Index**: Text search indexes

### Index Operations
- **CREATE INDEX**: Index creation syntax
- **DROP INDEX**: Index removal testing
- **INDEX HINTS**: Query optimizer hints
- **INDEX STATS**: Performance statistics

## Test Scenarios

### Basic Indexing
```python
# Single column index
db.define_table('person',
    Field('name', index=True),
    Field('email', unique=True))

# Composite index
db.executesql('CREATE INDEX idx_name_age ON person(name, age)')
```

### Advanced Indexing
- Partial indexes (WHERE clause)
- Functional indexes (expressions)
- Covering indexes (INCLUDE columns)
- Clustered vs non-clustered

## Performance Testing

### Index Effectiveness
- Query execution plan analysis
- Index usage verification
- Performance benchmarking
- Index maintenance overhead

### Cross-Database Support
- MySQL index syntax
- PostgreSQL index types
- SQLite index limitations
- MSSQL index options

This index testing suite ensures PyDAL properly manages database indexes for optimal query performance.