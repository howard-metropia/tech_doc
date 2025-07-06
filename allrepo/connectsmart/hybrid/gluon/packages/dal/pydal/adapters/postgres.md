# PostgreSQL Database Adapter

🔍 **Quick Summary (TL;DR)**
- Advanced PyDAL adapter for PostgreSQL with support for modern PostgreSQL features including JSON, arrays, and advanced data types
- Core functionality: postgresql-connectivity | advanced-sql-features | json-support | array-operations | full-text-search
- Primary use cases: Modern web applications, data analytics, GIS applications, high-performance database operations
- Compatibility: PostgreSQL 9.0+, supports psycopg2 and psycopg2cffi drivers, advanced PostgreSQL features

❓ **Common Questions Quick Index**
- Q: What PostgreSQL features are supported? → See Technical Specifications
- Q: How to use PostgreSQL JSON operations? → See Usage Methods
- Q: What about PostgreSQL arrays? → See Output Examples
- Q: How to configure PostgreSQL connections? → See Usage Methods
- Q: What's the performance compared to other adapters? → See Important Notes
- Q: How to use PostgreSQL-specific data types? → See Detailed Code Analysis
- Q: What about full-text search? → See Use Cases
- Q: How to debug PostgreSQL connection issues? → See Important Notes
- Q: What about PostgreSQL extensions? → See Improvement Suggestions
- Q: How to handle large PostgreSQL datasets? → See Important Notes

📋 **Functionality Overview**
- **Non-technical explanation:** Like a sophisticated interpreter fluent in PostgreSQL's advanced capabilities - while it handles basic database tasks like any adapter, it also understands PostgreSQL's powerful features like JSON documents, arrays, and complex queries, making it ideal for modern applications requiring advanced data handling.
- **Technical explanation:** Advanced database adapter extending SQLAdapter with comprehensive PostgreSQL feature support including JSON/JSONB operations, array handling, advanced indexing, full-text search, and PostgreSQL-specific optimizations.
- Business value: Enables leveraging PostgreSQL's advanced features for complex applications, improving performance and reducing application complexity through database-native operations.
- Context: Production-grade PostgreSQL adapter widely used in enterprise applications requiring advanced database capabilities and high performance.

🔧 **Technical Specifications**
- File: `pydal/adapters/postgres.py` (20KB+, Complexity: Very High)
- PostgreSQL versions: 9.0+ with full feature support for modern versions
- Drivers: psycopg2 (primary), psycopg2cffi (PyPy compatibility)
- Advanced features: JSON/JSONB, arrays, hstore, full-text search, window functions
- Connection URI: `postgresql://user:pass@host:port/db?options`
- Performance: Optimized for high-concurrency and large dataset operations

📝 **Detailed Code Analysis**
- **Postgre class**: Main PostgreSQL adapter with advanced feature support
- **PostgrePsyco class**: Alternative implementation for specific use cases
- **JSON/JSONB support**: Native PostgreSQL JSON operations and indexing
- **Array operations**: PostgreSQL array data type handling and queries
- **Advanced SQL generation**: PostgreSQL-specific syntax and optimizations
- **Connection features**:
  - Connection pooling with psycopg2
  - SSL support and security options
  - Custom connection parameters
  - Transaction isolation levels
- **PostgreSQL-specific methods**:
  - RETURNING clause support
  - UPSERT operations (INSERT ... ON CONFLICT)
  - Common table expressions (CTEs)
  - Window functions and advanced aggregates

🚀 **Usage Methods**
- Basic PostgreSQL connection:
```python
from pydal import DAL
db = DAL('postgresql://user:password@localhost/mydb')
db.define_table('users', Field('name'), Field('data', 'json'))
```
- JSON operations:
```python
# Define table with JSON field
db.define_table('documents', 
    Field('title'),
    Field('metadata', 'json'),
    Field('content', 'jsonb'))

# JSON queries
query = db.documents.metadata['author'] == 'John'
results = db(query).select()
```
- Array operations:
```python
# Array field definition
db.define_table('tags_table',
    Field('name'),
    Field('tags', 'list:string'))

# Array queries  
db.tags_table.insert(name='Post1', tags=['python', 'web2py'])
query = db.tags_table.tags.contains('python')
```
- Advanced PostgreSQL features:
```python
# Full-text search
db.define_table('articles',
    Field('title'),
    Field('content', 'text'),
    Field('search_vector', 'tsvector'))

# Window functions
db.executesql('''
    SELECT name, salary, 
           RANK() OVER (ORDER BY salary DESC) as rank
    FROM employees
''')
```

📊 **Output Examples**
- PostgreSQL-specific SQL generation:
```python
>>> db.define_table('test', Field('data', 'json'))
>>> str(db.test.insert(data={'key': 'value'}))
'INSERT INTO test(data) VALUES (\'{"key": "value"}\') RETURNING id;'
```
- JSON query examples:
```python
>>> query = db.test.data['user']['name'] == 'John'
>>> str(query)
"(test.data->'user'->>'name' = 'John')"
```
- Array operations:
```python
>>> db.define_table('arrays', Field('numbers', 'list:integer'))
>>> str(db.arrays.numbers.contains(5))
'(5 = ANY(arrays.numbers))'
```
- Connection information:
```python
>>> db._adapter.dbengine
'postgresql'
>>> db._adapter.driver_name
'psycopg2'
```

⚠️ **Important Notes**
- Driver installation: Requires psycopg2 (pip install psycopg2-binary)
- Performance: PostgreSQL adapter is highly optimized for complex queries
- JSON vs JSONB: Use JSONB for better performance with indexing
- Array indexing: PostgreSQL arrays are 1-indexed, not 0-indexed
- Connection pooling: psycopg2 provides excellent connection pooling
- Memory management: Use server-side cursors for large result sets
- Security: Supports all PostgreSQL security features including row-level security
- Extensions: Many PostgreSQL extensions work seamlessly with this adapter

🔗 **Related File Links**
- `pydal/adapters/base.py` - Base SQLAdapter class
- `pydal/dialects/postgres.py` - PostgreSQL-specific SQL dialect
- `pydal/helpers/postgres.py` - PostgreSQL utility functions
- psycopg2 documentation and configuration guides
- PostgreSQL JSON and array operation documentation
- PyDAL field type mapping for PostgreSQL

📈 **Use Cases**
- Modern web applications with complex data structures
- Data analytics platforms requiring advanced SQL features
- GIS applications using PostGIS extension
- Document storage with PostgreSQL JSON capabilities
- High-performance APIs with complex query requirements
- Real-time applications with PostgreSQL LISTEN/NOTIFY
- Multi-tenant applications with advanced security
- Data warehousing with PostgreSQL analytical functions

🛠️ **Improvement Suggestions**
- Features: Add support for PostgreSQL 14+ features (multirange types)
- Performance: Implement prepared statement caching
- Extensions: Add built-in support for popular extensions (PostGIS, pgcrypto)
- Async support: Implement asyncio-compatible operations
- Monitoring: Add PostgreSQL-specific performance monitoring
- Security: Enhanced support for PostgreSQL security features
- JSON: Improved JSON schema validation and operations
- Streaming: Better support for large dataset streaming

🏷️ **Document Tags**
- Keywords: postgresql, postgres, json, jsonb, arrays, advanced-sql, psycopg2, database-adapter
- Technical tags: #postgresql #json #arrays #advanced-sql #psycopg2 #database #pydal
- Target roles: Backend developers (advanced), Data engineers (intermediate), Database architects (expert)
- Difficulty level: ⭐⭐⭐⭐ - Requires understanding of PostgreSQL advanced features
- Maintenance level: Medium - Updated for new PostgreSQL versions and features
- Business criticality: High - Critical for PostgreSQL-based enterprise applications  
- Related topics: PostgreSQL administration, JSON operations, array handling, advanced SQL, database optimization