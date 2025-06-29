# base.py

## Overview
This file provides the base test class and fundamental testing infrastructure for PyDAL test suite, establishing common patterns and utilities used across all database tests.

## Purpose
- Defines base test class for all PyDAL tests
- Provides common test setup and teardown methods
- Implements shared testing utilities
- Manages test database lifecycle

## Key Components

### BaseTest Class
- **setUp()**: Initializes test database and tables
- **tearDown()**: Cleans up test data and connections
- **db**: Test database instance
- **define_tables()**: Creates common test table schemas

### Test Utilities
- **assert_query()**: Validates generated SQL queries
- **execute_test()**: Runs database operations with error handling
- **compare_results()**: Cross-database result comparison
- **measure_performance()**: Execution time tracking

## Test Database Management

### Database Lifecycle
- Automatic database creation for tests
- Transaction rollback after each test
- Connection pooling management
- Temporary table handling

### Schema Definitions
```python
# Common test tables
- person: id, name, age, email
- pet: id, name, owner (reference person)
- purchase: id, buyer, product, quantity, price
- tag: id, name, articles (list:reference)
```

## Testing Patterns

### Isolation Strategies
- Independent test execution
- No shared state between tests
- Predictable test data
- Repeatable test results

This base testing module provides the foundation for comprehensive PyDAL testing across all supported databases.