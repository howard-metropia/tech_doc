# PyDAL CouchDB Adapter

## Overview
The CouchDB adapter provides seamless integration between PyDAL and Apache CouchDB, enabling document-oriented database operations through PyDAL's familiar ORM interface.

## Key Features

### Document Database Integration
- **Document Storage**: Store Python objects as JSON documents
- **RESTful API**: HTTP-based database operations
- **Schema Flexibility**: Dynamic document structure support
- **View Queries**: MapReduce-based data querying

### CouchDB-Specific Operations
```python
class CouchDBAdapter(BaseAdapter):
    """
    Apache CouchDB adapter for PyDAL
    
    Features:
    - Document CRUD operations
    - View-based queries
    - Attachment handling
    - Replication support
    """
```

### Connection Management
- **HTTP Connection**: RESTful API communication
- **Authentication**: Basic and cookie authentication
- **SSL Support**: Secure connections to CouchDB
- **Connection Pooling**: Efficient connection reuse

### Document Operations
- **Insert**: Create new documents with auto-generated IDs
- **Update**: Modify existing documents with revision tracking
- **Delete**: Remove documents (soft delete)
- **Bulk Operations**: Efficient batch processing

### Query Translation
- **SQL to MapReduce**: Convert PyDAL queries to CouchDB views
- **Index Optimization**: Automatic view creation for queries
- **Aggregation Support**: COUNT, SUM, AVG operations
- **Sorting and Limiting**: Result ordering and pagination

### Data Type Mapping
```python
TYPE_MAP = {
    'string': str,
    'text': str,
    'integer': int,
    'double': float,
    'boolean': bool,
    'date': datetime.date,
    'datetime': datetime.datetime,
    'json': dict
}
```

### Attachment Support
- **Binary Attachments**: File storage within documents
- **MIME Type Detection**: Automatic content type handling
- **Inline Attachments**: Base64-encoded attachments
- **Standalone Attachments**: Separate attachment endpoints

### Error Handling
- **HTTP Error Mapping**: CouchDB HTTP errors to PyDAL exceptions
- **Conflict Resolution**: Document revision conflicts
- **Network Resilience**: Connection failure recovery
- **Validation Errors**: Document validation and constraints

This adapter bridges the gap between relational ORM patterns and document database paradigms, providing CouchDB's flexibility through PyDAL's consistent interface.