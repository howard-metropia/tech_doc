# MongoDB NoSQL Adapter

🔍 **Quick Summary (TL;DR)**
- NoSQL database adapter for MongoDB providing document-oriented database operations with PyDAL's familiar interface
- Core functionality: mongodb-connectivity | document-operations | nosql-queries | collection-management | mongodb-aggregation
- Primary use cases: Document storage, content management, real-time applications, flexible schema requirements
- Compatibility: MongoDB 3.0+, PyMongo driver, supports sharding and replica sets

❓ **Common Questions Quick Index**
- Q: How does PyDAL work with MongoDB? → See Functionality Overview
- Q: What MongoDB features are supported? → See Technical Specifications
- Q: How to query MongoDB documents? → See Usage Methods
- Q: What about MongoDB aggregation? → See Detailed Code Analysis
- Q: How to handle MongoDB collections? → See Output Examples
- Q: What are the MongoDB limitations in PyDAL? → See Important Notes
- Q: How to configure MongoDB connections? → See Usage Methods
- Q: What about MongoDB indexing? → See Use Cases
- Q: How to debug MongoDB operations? → See Important Notes
- Q: What's the performance compared to SQL? → See Important Notes

📋 **Functionality Overview**
- **Non-technical explanation:** Like a smart filing system for documents that doesn't require predefined folders - MongoDB stores information as flexible documents (like JSON files) rather than rigid table rows, allowing you to store different types of data together and change the structure as your needs evolve.
- **Technical explanation:** NoSQL adapter that bridges PyDAL's relational interface with MongoDB's document-oriented storage, translating familiar SQL-like operations into MongoDB queries while preserving document flexibility and MongoDB-specific features.
- Business value: Enables rapid development with flexible data models, supports agile development practices, and provides scalability for modern web applications with evolving data requirements.
- Context: Part of PyDAL's NoSQL support, allowing developers to use familiar PyDAL syntax with MongoDB's document database capabilities.

🔧 **Technical Specifications**
- File: `pydal/adapters/mongo.py` (12KB+, Complexity: High)
- MongoDB versions: 3.0+ with full feature support
- Driver: PyMongo (official MongoDB Python driver)
- Features: Document operations, aggregation pipeline, indexing, GridFS
- Connection URI: `mongodb://user:pass@host:port/database`
- Limitations: No JOINs, limited transaction support, different query semantics
- Performance: Optimized for document retrieval and flexible schema operations

📝 **Detailed Code Analysis**
- **Mongo class**: Extends NoSQLAdapter for MongoDB-specific operations
- **Document mapping**: Translates PyDAL fields to MongoDB document structure
- **Query translation**: Converts PyDAL queries to MongoDB query language
- **Collection management**: Automatic collection creation and indexing
- **MongoDB-specific features**:
  - Document insertion and retrieval
  - Aggregation pipeline support
  - GridFS for large file storage
  - Index management and optimization
- **Data type handling**: Maps PyDAL types to MongoDB BSON types
- **Error handling**: MongoDB-specific exception handling and translation

🚀 **Usage Methods**
- Basic MongoDB connection:
```python
from pydal import DAL
db = DAL('mongodb://localhost/myapp')
db.define_table('users', 
    Field('name'),
    Field('profile', 'json'),  # Flexible document structure
    Field('tags', 'list:string'))
```
- Document operations:
```python
# Insert document
user_id = db.users.insert(
    name='John Doe',
    profile={'age': 30, 'city': 'New York'},
    tags=['developer', 'python']
)

# Query documents
users = db(db.users.profile.age > 25).select()
for user in users:
    print(user.name, user.profile['city'])
```
- MongoDB-specific operations:
```python
# Use MongoDB aggregation
result = db.users._adapter.aggregate([
    {'$match': {'tags': 'python'}},
    {'$group': {'_id': '$profile.city', 'count': {'$sum': 1}}}
])

# Create indexes
db.users._adapter.create_index([('name', 1), ('profile.age', -1)])
```

📊 **Output Examples**
- MongoDB connection:
```python
>>> db = DAL('mongodb://localhost/test')
>>> db._adapter.dbengine
'mongodb'
>>> db._adapter.driver_name
'pymongo'
```
- Document structure:
```python
>>> db.define_table('docs', Field('data', 'json'))
>>> id = db.docs.insert(data={'nested': {'value': 42}})
>>> doc = db.docs[id]
>>> doc.data
{'nested': {'value': 42}}
```
- Collection information:
```python
>>> db._adapter.db.list_collection_names()
['users', 'docs']
>>> db.users._adapter.collection.count_documents({})
150
```
- Aggregation results:
```python
>>> pipeline = [{'$group': {'_id': '$city', 'total': {'$sum': 1}}}]
>>> list(db.users._adapter.aggregate(pipeline))
[{'_id': 'New York', 'total': 45}, {'_id': 'Boston', 'total': 23}]
```

⚠️ **Important Notes**
- Schema flexibility: MongoDB allows dynamic schema changes, but PyDAL still enforces field definitions
- Query limitations: No SQL JOINs, use document embedding or manual referencing
- Transaction support: Limited compared to traditional SQL databases
- Performance: Excellent for read-heavy workloads, document retrieval
- Indexing: Critical for query performance, must be planned carefully
- Memory usage: Documents can be large, monitor memory consumption
- Data consistency: Eventual consistency in replica sets, plan accordingly
- Driver installation: Requires PyMongo (pip install pymongo)

🔗 **Related File Links**
- `pydal/adapters/base.py` - Base NoSQLAdapter class
- `pydal/helpers/mongo.py` - MongoDB utility functions
- PyMongo documentation and MongoDB driver guides
- MongoDB query language and aggregation documentation
- GridFS documentation for file storage
- MongoDB indexing and performance optimization guides

📈 **Use Cases**
- Content management systems with flexible content types
- Real-time applications requiring fast document retrieval
- IoT data collection with varying sensor data structures
- User profile management with evolving attribute sets
- Product catalogs with diverse product specifications
- Social media applications with dynamic post structures
- Analytics platforms collecting diverse event data
- API backends requiring flexible data models

🛠️ **Improvement Suggestions**
- Performance: Add query result caching for frequently accessed documents
- Features: Enhanced support for MongoDB 4.0+ transactions
- Aggregation: More PyDAL-like aggregation query interface
- Indexing: Automatic index recommendation based on query patterns
- Schema: Optional schema validation with MongoDB JSON Schema
- Monitoring: Built-in performance monitoring and slow query detection
- GridFS: Better integration with PyDAL file upload handling
- Sharding: Enhanced support for MongoDB sharded clusters

🏷️ **Document Tags**
- Keywords: mongodb, nosql, document-database, pymongo, aggregation, flexible-schema
- Technical tags: #mongodb #nosql #document-database #aggregation #flexible-schema #pydal
- Target roles: NoSQL developers (intermediate), Full-stack developers (intermediate), Data engineers (advanced)
- Difficulty level: ⭐⭐⭐⭐ - Requires understanding of NoSQL concepts and MongoDB specifics
- Maintenance level: Medium - Updated for new MongoDB versions and features
- Business criticality: High - Critical for applications using MongoDB
- Related topics: NoSQL databases, document storage, aggregation, flexible schemas, modern web development