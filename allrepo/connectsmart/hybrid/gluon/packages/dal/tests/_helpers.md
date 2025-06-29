# _helpers.py

## Overview
This file contains helper functions and utilities specifically designed for PyDAL testing, providing reusable components for test data generation, assertion helpers, and testing utilities.

## Purpose
- Provides test data generators
- Implements custom assertion methods
- Offers database setup utilities
- Supplies mock objects for testing

## Key Helper Functions

### Data Generation
- **make_person()**: Creates test person records
- **make_purchase()**: Generates purchase transactions
- **random_string()**: Produces random test strings
- **bulk_data()**: Creates large datasets for performance testing

### Assertion Helpers
- **assert_sql_equals()**: Compares generated SQL
- **assert_count()**: Validates record counts
- **assert_fields()**: Checks field definitions
- **assert_no_errors()**: Ensures clean execution

## Test Utilities

### Database Helpers
```python
def setup_test_db(adapter='sqlite:memory'):
    """Create test database with common tables"""
    
def populate_test_data(db, count=100):
    """Fill database with test records"""
    
def cleanup_test_db(db):
    """Remove all test data"""
```

### Mock Objects
- **MockRequest**: Simulates web requests
- **MockResponse**: Fake response objects
- **MockAuth**: Authentication simulation
- **MockCache**: Cache behavior testing

## Performance Utilities

### Benchmarking Tools
- Execution timer decorators
- Memory usage tracking
- Query count monitoring
- Connection pool statistics

This helpers module provides essential testing infrastructure to ensure comprehensive and efficient PyDAL test coverage.