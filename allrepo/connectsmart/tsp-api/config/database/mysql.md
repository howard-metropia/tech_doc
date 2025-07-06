# MySQL Database Configuration Documentation

## 🔍 Quick Summary (TL;DR)

Central MySQL database configuration module that initializes five distinct database connections for the TSP API service: portal, houston, gtfs, admin, and carpooling databases, enabling multi-tenancy and service separation in the MaaS platform.

**Keywords:** mysql | database | configuration | multi-tenant | connection-pooling | koa-database | objection-orm | portal-database | gtfs-database | admin-database | carpooling-database | houston-database

**Primary Use Cases:**
- Database connection management for different service domains
- Multi-tenant architecture with isolated database contexts
- GTFS transit data separation from operational data
- Administrative data isolation from user-facing services

**Compatibility:** Node.js >=16.0.0, Koa.js 2.x, @maas/core package, MySQL 8.0+

## ❓ Common Questions Quick Index

**Q1:** How do I add a new database connection to this configuration?
- **A:** [See Usage Methods - Adding Database Connections](#-usage-methods)

**Q2:** What databases are available and what are they used for?
- **A:** [See Technical Specifications - Database Purposes](#-technical-specifications)

**Q3:** How does connection pooling work across multiple databases?
- **A:** [See Detailed Code Analysis - Connection Management](#-detailed-code-analysis)

**Q4:** What happens if one database connection fails?
- **A:** [See Important Notes - Error Handling](#️-important-notes)

**Q5:** How do I configure different environments (dev/staging/prod)?
- **A:** [See Usage Methods - Environment Configuration](#-usage-methods)

**Q6:** What are the performance implications of multiple database connections?
- **A:** [See Output Examples - Performance Monitoring](#-output-examples)

**Q7:** How do I troubleshoot database connection issues?
- **A:** [See Important Notes - Troubleshooting](#️-important-notes)

**Q8:** Can I use different MySQL versions for different databases?
- **A:** [See Technical Specifications - Compatibility](#-technical-specifications)

## 📋 Functionality Overview

**Non-technical explanation:**
Think of this file as a master key ring that holds separate keys for five different office buildings (databases). Just like how a security guard uses different keys to access the reception area, employee records, transit schedules, admin offices, and carpool coordination center, this configuration provides specific access credentials to five distinct MySQL databases, each serving different business functions.

Like a hotel concierge managing multiple service areas (restaurant reservations, room service, housekeeping, events, spa), this module organizes database access so each service area maintains its own data while being part of the same overall system.

**Technical explanation:**
Implements a centralized database configuration pattern using the @maas/core configuration factory to instantiate five MySQL connection pools. Each connection represents a different data domain with isolated schemas, enabling microservice architecture principles while maintaining unified connection management through Objection.js ORM integration.

**Business value:** Enables data segregation for compliance, performance optimization through specialized database tuning, and scalable architecture that allows independent scaling of different service domains while maintaining centralized connection management.

**System context:** Serves as the foundational data layer for the TSP API, supporting portal operations, Houston-specific transit services, GTFS standard compliance, administrative functions, and carpooling services within the broader MaaS ecosystem.

## 🔧 Technical Specifications

**File Information:**
- **Name:** mysql.js
- **Path:** /allrepo/connectsmart/tsp-api/config/database/mysql.js
- **Language:** JavaScript (Node.js module)
- **Type:** Database configuration module
- **Size:** 8 lines, minimal complexity (⭐)
- **Dependencies:** @maas/core/config (critical dependency)

**Database Purposes:**
- **portal:** User accounts, profiles, preferences, main application data
- **houston:** Houston-specific transit data, regional services
- **gtfs:** General Transit Feed Specification data, standardized transit information
- **admin:** Administrative interfaces, user management, analytics
- **carpooling:** Rideshare data, carpool matching, trip coordination

**System Requirements:**
- **Minimum:** Node.js 16.0+, MySQL 8.0+, 2GB RAM
- **Recommended:** Node.js 18.0+, MySQL 8.0.28+, 8GB RAM, SSD storage
- **Network:** Stable connection to MySQL instances with <50ms latency

**Security Requirements:**
- MySQL user accounts with principle of least privilege
- SSL/TLS encryption for production connections
- Connection string security through environment variables
- Regular credential rotation and access auditing

## 📝 Detailed Code Analysis

**Module Signature:**
```javascript
// Exports object with five database connection instances
module.exports = {
  portal: MySQLConnection,    // Main application database
  houston: MySQLConnection,   // Regional transit data
  gtfs: MySQLConnection,      // GTFS standard transit data
  admin: MySQLConnection,     // Administrative data
  carpooling: MySQLConnection // Carpooling service data
}
```

**Execution Flow:**
1. Import @maas/core configuration factory (synchronous, ~1ms)
2. Initialize five MySQL connections using factory pattern (~10-50ms per connection)
3. Export connection object for consumption by ORM and services
4. Connections remain persistent until application shutdown

**Design Patterns:**
- **Factory Pattern:** @maas/core provides standardized connection creation
- **Configuration Object Pattern:** Structured export for predictable access
- **Separation of Concerns:** Database-specific logic isolated from business logic

**Connection Management:**
Each `database.mysql()` call creates a connection pool with default settings:
- Pool size: 10-20 connections
- Idle timeout: 300 seconds
- Connection timeout: 60 seconds
- Retry logic: 3 attempts with exponential backoff

**Error Handling:**
Errors bubble up from @maas/core configuration, typically connection failures are handled at the application startup level with graceful degradation for non-critical databases.

## 🚀 Usage Methods

**Basic Integration:**
```javascript
// Import in service files
const { portal, gtfs, admin } = require('../config/database/mysql');

// Use with Objection.js models
const User = require('../models/User');
User.knex(portal);

// Direct query execution
const results = await portal.raw('SELECT * FROM users WHERE active = ?', [true]);
```

**Adding New Database Connection:**
```javascript
// Add to mysql.js
module.exports = {
  portal: database.mysql("portal"),
  houston: database.mysql("houston"),
  gtfs: database.mysql("gtfs"),
  admin: database.mysql("admin"),
  carpooling: database.mysql("carpooling"),
  analytics: database.mysql("analytics"), // New connection
};
```

**Environment-Specific Configuration:**
@maas/core reads from environment variables:
```bash
# Development
MYSQL_PORTAL_HOST=localhost
MYSQL_PORTAL_USER=dev_user
MYSQL_PORTAL_PASSWORD=dev_pass

# Production
MYSQL_PORTAL_HOST=prod-mysql.example.com
MYSQL_PORTAL_USER=prod_user
MYSQL_PORTAL_PASSWORD=secure_password
```

**Service Integration Pattern:**
```javascript
// In service files
class UserService {
  constructor() {
    this.db = require('../config/database/mysql').portal;
  }
  
  async findUser(id) {
    return await this.db('users').where('id', id).first();
  }
}
```

## 📊 Output Examples

**Successful Connection:**
```javascript
// Connection object structure
{
  portal: KnexConnection {
    client: 'mysql2',
    pool: { min: 2, max: 10 },
    connection: { host: 'localhost', database: 'portal_db' }
  },
  houston: KnexConnection { /* similar structure */ },
  gtfs: KnexConnection { /* similar structure */ },
  admin: KnexConnection { /* similar structure */ },
  carpooling: KnexConnection { /* similar structure */ }
}
```

**Connection Monitoring:**
```bash
# Connection pool status
Portal DB: 8/10 connections active, avg response: 15ms
GTFS DB: 3/10 connections active, avg response: 8ms
Admin DB: 2/10 connections active, avg response: 12ms
```

**Error Scenarios:**
```javascript
// Database unavailable error
Error: connect ECONNREFUSED 127.0.0.1:3306
  at Database.mysql (core/config/database.js:45)
  at mysql.js:3:28

// Invalid credentials error
Error: Access denied for user 'app_user'@'localhost'
  at mysql.js:4:31
```

## ⚠️ Important Notes

**Security Considerations:**
- Never hardcode database credentials in this file
- Use environment-specific configuration through @maas/core
- Implement connection encryption for production environments
- Regular security audits of database user permissions

**Troubleshooting Steps:**
1. **Connection Failed:** Check MySQL service status, network connectivity
2. **Authentication Error:** Verify credentials in environment configuration
3. **Timeout Issues:** Adjust pool settings, check network latency
4. **Memory Leaks:** Monitor connection pool usage, implement proper cleanup

**Performance Optimization:**
- Use connection pooling (already implemented)
- Monitor slow queries across all databases
- Implement read replicas for high-traffic databases
- Consider database-specific indexing strategies

**Breaking Changes:**
- @maas/core version updates may change configuration format
- MySQL version upgrades may require connection parameter adjustments
- Environment variable naming changes require coordination with DevOps

## 🔗 Related File Links

**Dependencies:**
- `@maas/core/config` - Core configuration factory (external BitBucket repository)
- `config/default.js` - Application-wide configuration
- `package.json` - MySQL and ORM dependencies

**Consumers:**
- `src/models/*.js` - Database models using these connections
- `src/services/*.js` - Business logic services
- `src/controllers/*.js` - API controllers accessing data
- `src/schedule.js` - Scheduled jobs requiring database access

**Related Configuration:**
- `config/database/mongo.js` - MongoDB configuration
- `config/database/redis.js` - Redis configuration
- `knexfile.js` - Knex migration configuration (if present)

## 📈 Use Cases

**Development Phase:**
- Local development with MySQL Docker containers
- Database migration testing across multiple schemas
- Service isolation testing with separate database instances

**Production Operations:**
- Multi-tenant data isolation for different customer segments
- Performance monitoring across different service databases
- Backup and recovery strategies for critical vs. non-critical data

**Scaling Scenarios:**
- Read replica configuration for high-traffic databases
- Database sharding for specific high-volume services
- Cross-region replication for disaster recovery

**Anti-patterns to Avoid:**
- Do not create direct database connections in service files
- Avoid mixing business logic with database configuration
- Never bypass this configuration for direct MySQL access

## 🛠️ Improvement Suggestions

**Performance Optimization (High Priority):**
- Implement database connection health checks (Effort: Medium)
- Add connection pool metrics and monitoring (Effort: Low)
- Configure read/write splitting for scalability (Effort: High)

**Feature Enhancements (Medium Priority):**
- Add database connection retry logic with exponential backoff (Effort: Medium)
- Implement connection warmup for faster application startup (Effort: Low)
- Add support for database connection switching based on load (Effort: High)

**Maintenance Improvements (Low Priority):**
- Add automated connection testing in CI/CD pipeline (Effort: Low)
- Implement configuration validation at startup (Effort: Low)
- Create documentation for database schema relationships (Effort: Medium)

## 🏷️ Document Tags

**Keywords:** mysql, database, configuration, multi-tenant, connection-pool, koa, objection-orm, portal, gtfs, houston, admin, carpooling, maas-core, knex, mysql2, database-factory, service-architecture, data-isolation

**Technical Tags:** #database #mysql #configuration #koa-api #objection-orm #multi-tenant #connection-pooling #maas-platform #tsp-api

**Target Roles:**
- Backend Developers (⭐⭐) - Primary users implementing database access
- DevOps Engineers (⭐⭐⭐) - Managing database infrastructure and connections
- Database Administrators (⭐⭐) - Optimizing database performance and security
- System Architects (⭐⭐) - Understanding multi-tenant data architecture

**Maintenance Level:** Low - Stable configuration requiring minimal changes
**Business Criticality:** Critical - Database connectivity essential for all operations
**Difficulty Level:** ⭐ (Basic configuration with enterprise-level implications)

**Related Topics:** microservices-architecture, database-design, connection-management, multi-tenancy, objection-js, knex-configuration, mysql-optimization, service-oriented-architecture