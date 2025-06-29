# sql.py

## Overview
This file contains comprehensive tests for PyDAL's SQL generation and execution functionality, validating correct SQL syntax across different database dialects.

## Purpose
- Tests SQL query generation
- Validates SQL syntax for each database
- Verifies query execution results
- Ensures SQL injection prevention

## Key SQL Operations Tested

### Basic CRUD SQL
- **SELECT**: Query generation and execution
- **INSERT**: Single and bulk inserts
- **UPDATE**: Conditional updates
- **DELETE**: Safe deletion with conditions

### Complex SQL Features
- **JOINs**: Inner, left, right, full outer
- **GROUP BY**: Aggregation queries
- **ORDER BY**: Sorting with multiple columns
- **HAVING**: Post-aggregation filtering

## SQL Generation Tests

### Query Building
```python
# Simple select
sql = db(db.person.age > 18)._select()
# Complex join
sql = db(db.person.id == db.pet.owner)._select(
    db.person.name, db.pet.name
)
# Aggregation
sql = db()._select(
    db.person.age, 
    db.person.id.count(),
    groupby=db.person.age
)
```

### Dialect Differences
- MySQL backtick quoting
- PostgreSQL double quotes
- SQLite pragma commands
- MSSQL square brackets

## SQL Safety

### Injection Prevention
- Parameter binding tests
- Quote escaping validation
- Prepared statement usage
- Dangerous pattern detection

### Transaction Testing
- BEGIN/COMMIT/ROLLBACK
- Savepoint support
- Isolation levels
- Deadlock handling

This SQL testing suite ensures PyDAL generates correct, safe, and optimized SQL across all supported databases.