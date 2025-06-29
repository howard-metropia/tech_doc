# _adapt.py

## Overview
This file contains adapter testing utilities for PyDAL, focusing on database-specific adapter implementations and their compatibility across different database systems.

## Purpose
- Tests database adapter implementations
- Validates adapter-specific SQL generation
- Ensures cross-database compatibility
- Verifies adapter initialization and configuration

## Key Features

### Adapter Testing Framework
- **Adapter Factory**: Creates test adapters for different databases
- **SQL Generation**: Tests adapter-specific SQL syntax
- **Connection Testing**: Validates database connections
- **Feature Detection**: Tests database-specific capabilities

### Database Adapter Tests
- **SQLite Adapter**: Memory and file-based testing
- **MySQL Adapter**: Connection pooling and charset handling
- **PostgreSQL Adapter**: Array types and JSON support
- **MSSQL Adapter**: Windows authentication and schemas

## Test Scenarios

### Connection Management
- Connection establishment and teardown
- Connection pooling behavior
- Timeout and retry logic
- Error handling and recovery

### SQL Dialect Testing
- CREATE TABLE variations
- Data type mappings
- Index creation syntax
- Constraint definitions

## Integration Testing

### Cross-Adapter Compatibility
- Unified API testing across adapters
- Migration compatibility tests
- Query portability validation
- Performance comparison benchmarks

This adapter testing module ensures PyDAL maintains consistent behavior across all supported database platforms while leveraging platform-specific optimizations.