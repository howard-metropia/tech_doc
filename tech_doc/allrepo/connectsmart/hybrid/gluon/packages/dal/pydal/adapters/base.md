# PyDAL Base Adapter Classes

🔍 **Quick Summary (TL;DR)**
- Core base classes for PyDAL database adapters providing common functionality for SQL and NoSQL database implementations
- Core functionality: adapter-base-classes | sql-adapter | nosql-adapter | query-generation | connection-management | database-abstraction
- Primary use cases: adapter development, database abstraction, query compilation, connection pooling, transaction management
- Compatibility: Python 2/3, supports all PyDAL database backends, provides foundation for custom adapters

❓ **Common Questions Quick Index**
- Q: What base adapter classes are available? → See Detailed Code Analysis
- Q: How to create custom database adapters? → See Usage Methods
- Q: What's the difference between SQL and NoSQL adapters? → See Technical Specifications
- Q: How does query compilation work? → See Functionality Overview
- Q: What about connection management? → See Important Notes
- Q: How to debug adapter issues? → See Output Examples
- Q: What methods must be implemented? → See Improvement Suggestions
- Q: How does transaction handling work? → See Detailed Code Analysis
- Q: What about adapter configuration? → See Usage Methods
- Q: How to extend existing adapters? → See Use Cases

📋 **Functionality Overview**
- **Non-technical explanation:** Like a master blueprint for building database translators - provides the common foundation and tools that all specific database adapters need, similar to how all car manufacturers follow basic engineering principles but customize for their specific engines and features.
- **Technical explanation:** Abstract base classes implementing the Template Method pattern to provide common database adapter functionality including connection management, query compilation, result processing, and transaction handling while allowing database-specific customization.
- Business value: Reduces development effort for new database support, ensures consistent behavior across adapters, and provides robust foundation for database abstraction layer.
- Context: Foundation component of PyDAL's adapter ecosystem, enabling support for 15+ database backends through standardized interfaces and shared functionality.

🔧 **Technical Specifications**
- File: `pydal/adapters/base.py` (45KB+, Complexity: Very High)
- Dependencies: PyDAL core objects, connection pooling, migration system, regex helpers
- Base classes: SQLAdapter for relational databases, NoSQLAdapter for document stores
- Features: Query compilation, result processing, connection pooling, transaction management, migration support
- Design patterns: Template Method, Strategy, Factory, Adapter patterns
- Extension points: Database-specific query generation, type mapping, connection handling

📝 **Detailed Code Analysis**
- **SQLAdapter class**: Base class for relational database adapters
  - Connection management with pooling support
  - SQL query generation and compilation
  - Result set processing and caching
  - Transaction management (commit, rollback)
  - Schema migration support
  - Type mapping and validation
- **NoSQLAdapter class**: Base class for document/NoSQL databases
  - Document-oriented query interface
  - Schema-less operation support
  - Specialized indexing strategies
- **Key methods**: `_initialize_()`, `_select()`, `_insert()`, `_update()`, `_delete()`
- **Abstract methods**: Database-specific implementations required
- **Helper methods**: Common utilities for all adapters

🚀 **Usage Methods**
- Creating custom SQL adapter:
```python
from pydal.adapters.base import SQLAdapter
from pydal.adapters import adapters

@adapters.register_for('mydb')
class MyDBAdapter(SQLAdapter):
    dbengine = 'mydb'
    drivers = ('mydb_driver',)
    
    def _initialize_(self):
        # Custom initialization
        super()._initialize_()
        
    def _select(self, query, fields, attributes):
        # Custom SELECT implementation
        pass
```
- Extending existing adapter:
```python
from pydal.adapters.mysql import MySQL

class CustomMySQL(MySQL):
    def _insert(self, table, fields):
        # Custom insert logic
        result = super()._insert(table, fields)
        # Additional processing
        return result
```
- Connection configuration:
```python
class MyAdapter(SQLAdapter):
    def _initialize_(self):
        super()._initialize_()
        self.connection_parameters = {
            'pool_size': 10,
            'timeout': 30
        }
```

📊 **Output Examples**
- Adapter hierarchy:
```python
>>> from pydal.adapters.mysql import MySQL
>>> MySQL.__bases__
(<class 'pydal.adapters.base.SQLAdapter'>,)
>>> MySQL.dbengine
'mysql'
>>> MySQL.drivers
('MySQLdb', 'pymysql', 'mysqlconnector')
```
- Query compilation:
```python
>>> adapter = SQLAdapter(db, 'sqlite://memory')
>>> query = db.users.name == 'John'
>>> adapter._select(query, [db.users.ALL], {})
'SELECT users.id, users.name FROM users WHERE (users.name = \'John\');'
```
- Connection status:
```python
>>> adapter.connection
<sqlite3.Connection object at 0x...>
>>> adapter.connection_status
'connected'
```

⚠️ **Important Notes**
- Abstract methods: Custom adapters must implement all required abstract methods
- Connection management: Proper connection pooling and cleanup is critical
- Thread safety: Base classes provide thread-safe connection handling patterns
- Error handling: Exceptions should be properly caught and transformed
- Performance: Query compilation caching is essential for performance
- Transaction isolation: Different databases have different isolation levels
- Memory management: Result sets can be large, proper iteration is important
- SQL injection: Base classes provide parameterized query protection

🔗 **Related File Links**
- `pydal/adapters/mysql.py` - MySQL adapter implementation example
- `pydal/adapters/postgres.py` - PostgreSQL adapter with advanced features
- `pydal/adapters/sqlite.py` - SQLite adapter for embedded databases
- `pydal/connection.py` - Connection pooling implementation
- `pydal/migrator.py` - Schema migration system
- `pydal/objects.py` - Database objects (Table, Field, Query)

📈 **Use Cases**
- Adding support for new database engines
- Customizing existing database adapters for specific requirements
- Implementing database-specific optimizations
- Creating specialized adapters for cloud databases
- Building test doubles for database operations
- Implementing custom caching strategies
- Adding database-specific monitoring and logging
- Supporting legacy or proprietary database systems

🛠️ **Improvement Suggestions**
- Documentation: Add comprehensive adapter development guide
- Testing: Provide adapter testing framework and test cases
- Performance: Implement query plan caching and optimization hints
- Monitoring: Add built-in performance monitoring and profiling
- Security: Enhance parameterized query validation
- Features: Add support for database-specific advanced features
- Async support: Implement asynchronous query execution patterns
- Cloud integration: Add cloud database-specific optimizations

🏷️ **Document Tags**
- Keywords: base-adapter, sql-adapter, nosql-adapter, database-abstraction, query-compilation, adapter-development
- Technical tags: #adapter-base #sql #nosql #database #abstraction #template-method #pydal
- Target roles: Database adapter developers (expert), Framework architects (advanced), Backend developers (advanced)
- Difficulty level: ⭐⭐⭐⭐⭐ - Requires deep understanding of database systems and design patterns
- Maintenance level: High - Core component requiring careful updates
- Business criticality: Critical - Foundation for all database operations
- Related topics: Database abstraction, adapter patterns, query compilation, connection pooling, database drivers