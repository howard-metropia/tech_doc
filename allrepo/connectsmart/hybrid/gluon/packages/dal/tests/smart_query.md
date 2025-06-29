# smart_query.py

## Overview
This file tests PyDAL's smart query functionality, which allows natural language-like query construction and intelligent query parsing for more intuitive database operations.

## Purpose
- Tests natural language query parsing
- Validates smart query syntax
- Verifies query optimization
- Ensures accurate SQL generation

## Key Features Tested

### Smart Query Syntax
```python
# Natural language queries
db.smart_query([db.person], 'name starts with "J" and age > 18')
db.smart_query([db.person], 'email contains "gmail"')
db.smart_query([db.person, db.pet], 'person.name = "John" and pet.owner = person.id')
```

### Query Operators
- **Comparison**: =, !=, <, >, <=, >=
- **String**: contains, starts with, ends with
- **Logic**: and, or, not
- **Special**: in, between, is null

## Advanced Parsing

### Complex Queries
- Multi-table joins
- Nested conditions
- Subquery support
- Aggregate functions

### Query Building
```python
# Dynamic query construction
conditions = []
if name:
    conditions.append(f'name = "{name}"')
if age:
    conditions.append(f'age >= {age}')
query = ' and '.join(conditions)
db.smart_query([db.person], query)
```

## Error Handling

### Parse Errors
- Invalid syntax detection
- Ambiguous field names
- Type mismatch handling
- Security validation

### Query Optimization
- Index usage hints
- Join order optimization
- Condition reordering
- Query plan analysis

This smart query testing ensures PyDAL provides an intuitive yet powerful query interface while maintaining security and performance.