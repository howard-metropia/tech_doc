# nosql.py

## Overview
This file contains tests for PyDAL's NoSQL database support, validating functionality for document-oriented databases like MongoDB and CouchDB.

## Purpose
- Tests NoSQL adapter implementations
- Validates document CRUD operations
- Verifies query translation to NoSQL
- Ensures NoSQL-specific features work correctly

## Key Features Tested

### NoSQL Adapters
- **MongoDB Adapter**: Document operations and queries
- **CouchDB Adapter**: RESTful document handling
- **Google Datastore**: Entity management
- **DynamoDB Support**: Key-value operations

### Document Operations
- **Insert**: Document creation with nested data
- **Find**: Query documents with conditions
- **Update**: Partial and full document updates
- **Delete**: Document removal and bulk deletion

## NoSQL-Specific Tests

### MongoDB Features
```python
# Nested documents
db.posts.insert(
    title='Test',
    author={'name': 'John', 'email': 'john@example.com'},
    tags=['python', 'nosql']
)

# Array operations
db(db.posts.tags.contains('python')).select()
```

### Query Translation
- SQL to MongoDB query conversion
- Aggregation pipeline generation
- Index creation for NoSQL
- Geospatial query support

## Data Type Handling

### Complex Types
- Nested documents/objects
- Arrays and lists
- Binary data (GridFS)
- Geospatial data types

### Schema Flexibility
- Dynamic field addition
- Schema-less operations
- Field type changes
- Document validation rules

This NoSQL testing suite ensures PyDAL provides consistent API across both SQL and NoSQL databases.