# MySQL Database Adapter

🔍 **Quick Summary (TL;DR)**
- PyDAL adapter for MySQL database providing optimized connectivity and query generation for MySQL-specific features and dialects
- Core functionality: mysql-connectivity | mysql-sql-generation | connection-pooling | transaction-support | mysql-optimization
- Primary use cases: MySQL database integration, web application backends, high-performance MySQL operations
- Compatibility: MySQL 5.0+, MariaDB, supports MySQLdb, PyMySQL, and mysql-connector drivers

❓ **Common Questions Quick Index**
- Q: What MySQL drivers are supported? → See Technical Specifications
- Q: How to configure MySQL connections? → See Usage Methods
- Q: What MySQL-specific features are supported? → See Detailed Code Analysis
- Q: How to handle MySQL charset issues? → See Important Notes
- Q: What about MySQL performance optimization? → See Output Examples
- Q: How to debug MySQL connection issues? → See Important Notes
- Q: What's the connection string format? → See Usage Methods
- Q: How to use MySQL stored procedures? → See Use Cases
- Q: What about MySQL replication support? → See Improvement Suggestions
- Q: How to handle large MySQL datasets? → See Important Notes

📋 **Functionality Overview**
- **Non-technical explanation:** Like a specialized translator specifically trained in MySQL's unique dialect - while it can handle standard database operations like any other translator, it also knows MySQL's special features, performance tricks, and quirks, ensuring optimal communication between your application and MySQL servers.
- **Technical explanation:** Specialized database adapter that extends SQLAdapter to provide MySQL-specific optimizations including custom SQL generation, MySQL dialect support, multiple driver compatibility, and MySQL-specific features like distributed transactions.
- Business value: Enables high-performance MySQL integration with automatic optimization for MySQL-specific features, reducing development time and maximizing database performance.
- Context: Production-ready MySQL adapter within PyDAL ecosystem, widely used in web applications requiring robust MySQL connectivity.

🔧 **Technical Specifications**
- File: `pydal/adapters/mysql.py` (15KB+, Complexity: High)
- MySQL versions: 5.0+ and MariaDB support
- Drivers supported: MySQLdb (fastest), PyMySQL (pure Python), mysql-connector (official)
- Features: Distributed transactions, AUTO_INCREMENT support, charset handling
- Connection URI: `mysql://user:password@host:port/database?charset=utf8&unix_socket=/path`
- Performance: Optimized for high-concurrency web applications

📝 **Detailed Code Analysis**
- **MySQL class**: Inherits from SQLAdapter with MySQL-specific implementations
- **Driver detection**: Automatic selection from MySQLdb > PyMySQL > mysql-connector
- **URI parsing**: Regular expression for MySQL connection string validation
- **Connection parameters**:
  - Host, port, database, user, password
  - Charset configuration (default UTF-8)
  - Unix socket support for local connections
  - SSL and connection timeout options
- **MySQL-specific features**:
  - `commit_on_alter_table = True` for schema changes
  - `support_distributed_transaction = True` for XA transactions
  - AUTO_INCREMENT handling for primary keys
  - MySQL-specific SQL dialect generation

🚀 **Usage Methods**
- Basic MySQL connection:
```python
from pydal import DAL
db = DAL('mysql://user:password@localhost/mydb')
db.define_table('users', Field('name'), Field('email'))
```
- Advanced connection with options:
```python
db = DAL('mysql://user:pass@host:3306/db?charset=utf8mb4&unix_socket=/tmp/mysql.sock')
# With connection pooling
db = DAL('mysql://user:pass@host/db', pool_size=20)
```
- Using specific MySQL driver:
```python
# Force PyMySQL driver
db = DAL('mysql://user:pass@host/db', driver_args={'driver': 'pymysql'})
```
- MySQL-specific operations:
```python
# Use distributed transactions
db.begin()
try:
    db.users.insert(name='John')
    db.commit()
except:
    db.rollback()
```

📊 **Output Examples**
- Connection establishment:
```python
>>> db = DAL('mysql://root:pass@localhost/test')
>>> db._adapter.dbengine
'mysql'
>>> db._adapter.drivers
('MySQLdb', 'pymysql', 'mysqlconnector')
```
- MySQL-specific SQL generation:
```python
>>> db.define_table('test', Field('id', 'id'), Field('name'))
>>> str(db.test.insert(name='John'))
'INSERT INTO test(name) VALUES (\'John\');'
>>> str(db(db.test.id > 0).select())
'SELECT test.id, test.name FROM test WHERE (test.id > 0);'
```
- Driver information:
```python
>>> db._adapter.driver_name
'MySQLdb'  # or 'pymysql' or 'mysql.connector'
>>> db._adapter.connection
<MySQLdb.connections.Connection at 0x...>
```
- Performance metrics:
```python
>>> db.executesql('SHOW STATUS LIKE "Connections"')
[('Connections', '1234')]
```

⚠️ **Important Notes**
- Driver installation: MySQL drivers must be installed separately (pip install MySQLdb or PyMySQL)
- Charset configuration: Always specify charset to avoid encoding issues
- Connection limits: MySQL has connection limits, use connection pooling appropriately
- Performance: MySQLdb is fastest but requires compilation, PyMySQL is pure Python
- Thread safety: All supported drivers are thread-safe when used correctly
- Memory management: Large result sets should use iterators to avoid memory issues
- Security: Always use parameterized queries, never string interpolation
- Time zones: Be aware of MySQL time zone settings and UTC handling

🔗 **Related File Links**
- `pydal/adapters/base.py` - Base SQLAdapter class inherited by MySQL adapter
- `pydal/connection.py` - Connection pooling implementation
- `pydal/dialects/mysql.py` - MySQL-specific SQL dialect definitions
- MySQL driver documentation: MySQLdb, PyMySQL, mysql-connector
- MySQL configuration files and optimization guides
- PyDAL field type mapping documentation

📈 **Use Cases**
- High-traffic web applications with MySQL backend
- E-commerce platforms requiring reliable database operations
- Content management systems with complex data relationships
- API backends serving millions of requests
- Data analytics applications with large MySQL datasets
- Multi-tenant applications with shared MySQL infrastructure
- Real-time applications requiring fast database access
- Legacy system integration with existing MySQL databases

🛠️ **Improvement Suggestions**
- Performance: Add query result caching for frequently accessed data
- Monitoring: Implement connection health checking and failover
- Security: Add support for MySQL 8.0 authentication methods
- Features: Support for MySQL JSON data type and operations
- Replication: Add read/write splitting for MySQL replication setups
- Optimization: Implement MySQL-specific query optimization hints
- Async support: Add asynchronous query execution capabilities
- Cloud integration: Optimize for cloud MySQL services (RDS, CloudSQL)

🏷️ **Document Tags**
- Keywords: mysql, database-adapter, sql, mysql-connector, pymysql, mysqldb, database-connectivity
- Technical tags: #mysql #database #sql #adapter #connectivity #web2py #pydal
- Target roles: Backend developers (intermediate), Database administrators (intermediate), Full-stack developers (basic)
- Difficulty level: ⭐⭐⭐ - Requires understanding of MySQL and database concepts
- Maintenance level: Medium - Updated for new MySQL versions and driver changes
- Business criticality: High - Critical for MySQL-based applications
- Related topics: MySQL administration, database connectivity, SQL optimization, web application backends