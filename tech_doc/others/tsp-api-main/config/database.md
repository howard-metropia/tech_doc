# Database Configuration Module Documentation

## 🔍 Quick Summary (TL;DR)
Multi-database configuration hub that provides centralized access to MySQL, Redis, MongoDB, and InfluxDB connections for the TSP API microservice. This configuration module enables the application to connect to different database systems for varied data storage and caching needs.

**Keywords:** database | config | mysql | redis | mongodb | influxdb | multi-database | connection | cache | metrics | time-series | configuration

**Primary Use Cases:**
- Database connection management for microservices
- Multi-database architecture configuration
- Cache and session storage setup
- Metrics and monitoring data storage
- Transit and transportation data persistence

**Compatibility:** Node.js 14+, Koa.js framework, @maas/core package

## ❓ Common Questions Quick Index
- **Q: How do I add a new database connection?** → See [Usage Methods](#usage-methods)
- **Q: What databases are supported?** → See [Technical Specifications](#technical-specifications)
- **Q: How to configure Redis for caching?** → See [Redis Configuration](#redis-configuration)
- **Q: Why multiple MySQL databases?** → See [Multi-tenancy](#multi-tenancy-architecture)
- **Q: How to troubleshoot connection errors?** → See [Important Notes](#important-notes)
- **Q: What environment variables are required?** → See [Environment Configuration](#environment-configuration)
- **Q: How to monitor database performance?** → See [InfluxDB Configuration](#influxdb-configuration)
- **Q: Can I use this in production?** → See [Production Considerations](#production-considerations)

## 📋 Functionality Overview

**Non-technical explanation:**
Think of this module as a master key ring that holds keys to different storage rooms in a large warehouse. Just like a warehouse manager needs access to various specialized storage areas (cold storage for food, secure vaults for valuables, quick-access areas for frequently used items), this application needs different types of databases for different purposes. It's like a phone directory that tells the application which number to call for each type of data service.

**Technical explanation:**
A configuration aggregator that exports database connection configurations for a multi-database microservice architecture. It centralizes database access patterns using the factory pattern, providing typed interfaces to MySQL (relational data), Redis (caching), MongoDB (document storage), and InfluxDB (time-series metrics).

**Business value:** Enables horizontal scaling by distributing data across specialized database systems, improves performance through caching strategies, and provides robust monitoring capabilities for transportation service operations.

**System context:** Central configuration point for the TSP API's data layer, supporting transit operations, user management, caching, and real-time monitoring across the MaaS platform.

## 🔧 Technical Specifications

**File Information:**
- Name: database.js
- Path: /config/database.js
- Language: JavaScript (Node.js module)
- Type: Configuration aggregator
- Size: ~6 lines
- Complexity: Low (⭐)

**Dependencies:**
- `@maas/core/config` (Critical) - Provides database factory methods
- `./database/mysql.js` (Critical) - MySQL connection configurations
- `./database/redis.js` (Critical) - Redis cache configuration
- `./database/mongo.js` (Critical) - MongoDB connection configurations
- `./database/influx.js` (Critical) - InfluxDB metrics configuration

**System Requirements:**
- Minimum: Node.js 14.x, 512MB RAM, network access to databases
- Recommended: Node.js 18+, 2GB RAM, dedicated database servers
- Production: Load balancer, connection pooling, database replicas

**Security Requirements:**
- Environment-based credential management
- Network encryption for database connections
- Role-based database access control
- Regular credential rotation

## 📝 Detailed Code Analysis

**Module Structure:**
```javascript
module.exports = {
  mysql: require('./database/mysql'),    // Multi-tenant MySQL configs
  redis: require('./database/redis'),    // Cache configuration
  mongo: require('./database/mongo'),    // Document storage configs
  influx: require('./database/influx')   // Metrics and monitoring
};
```

**Execution Flow:**
1. Module loads → Database sub-modules imported
2. Each sub-module provides typed configuration objects
3. Configurations merged into single exportable object
4. Application components access via destructuring

**Design Patterns:**
- **Module Pattern**: Encapsulates database configurations
- **Factory Pattern**: @maas/core provides database connection factories
- **Configuration Object Pattern**: Structured configuration access

**Error Handling:**
- Environment variable validation in sub-modules
- Connection timeout handling in factory methods
- Graceful degradation for optional services

## 🚀 Usage Methods

**Basic Integration:**
```javascript
const database = require('./config/database');

// Access specific database configuration
const mysqlConfig = database.mysql;
const redisConfig = database.redis;
```

**Service Integration:**
```javascript
const { mysql, redis, mongo, influx } = require('./config/database');

// In a service class
class UserService {
  constructor() {
    this.db = mysql.portal;  // Portal database for user data
    this.cache = redis.cache; // Redis for session caching
  }
}
```

**Environment Configuration:**
```bash
# Redis Environment Variables
REDIS_CACHE_HOST=localhost
REDIS_CACHE_PASSWORD=secure_password
REDIS_CACHE_PORT=6379

# InfluxDB Environment Variables
INFLUXDB_URL=http://localhost:8086
INFLUXDB_TOKEN=your_influx_token
INFLUXDB_ORG=your_organization
```

## 📊 Output Examples

**Configuration Object Structure:**
```javascript
{
  mysql: {
    portal: { host: 'portal-db', port: 3306, database: 'portal' },
    houston: { host: 'houston-db', port: 3306, database: 'houston' },
    gtfs: { host: 'gtfs-db', port: 3306, database: 'gtfs' },
    admin: { host: 'admin-db', port: 3306, database: 'admin' },
    carpooling: { host: 'carpool-db', port: 3306, database: 'carpooling' }
  },
  redis: {
    cache: { host: 'redis-cache', port: 6379, password: '***' }
  },
  mongo: {
    cache: { url: 'mongodb://mongo-cache:27017/cache' },
    dataset: { url: 'mongodb://mongo-dataset:27017/dataset' }
  },
  influx: {
    url: 'http://influxdb:8086',
    bucket: 'tsp-metrics',
    org: 'maas-platform'
  }
}
```

**Error Scenarios:**
```javascript
// Missing environment variable
Error: REDIS_CACHE_HOST environment variable is required

// Connection timeout
Error: Database connection timeout after 30000ms

// Invalid configuration
TypeError: Cannot read property 'mysql' of undefined
```

## ⚠️ Important Notes

**Security Considerations:**
- Never hardcode database credentials in configuration files
- Use environment variables for all sensitive data
- Implement connection encryption (SSL/TLS) for production
- Regular audit of database access permissions

**Performance Considerations:**
- Connection pooling configured in @maas/core factory methods
- Redis connection reuse for cache operations
- InfluxDB batch writing for metrics collection
- MySQL query optimization through proper indexing

**Troubleshooting:**
- **Connection refused**: Check database server status and network connectivity
- **Authentication failed**: Verify environment variables and credentials
- **Timeout errors**: Increase connection timeout or check network latency
- **Module not found**: Ensure @maas/core package is properly installed

## 🔗 Related File Links

**Configuration Dependencies:**
- `/config/database/mysql.js` - MySQL database configurations
- `/config/database/redis.js` - Redis cache configuration
- `/config/database/mongo.js` - MongoDB connection settings
- `/config/database/influx.js` - InfluxDB metrics configuration

**Consumer Services:**
- `/src/services/` - Business logic services using database connections
- `/src/controllers/` - API controllers accessing data layer
- `/src/middlewares/auth.js` - Authentication middleware using cache

**Related Documentation:**
- `/config/default.js` - Main application configuration
- `@maas/core` package documentation - Database factory methods

## 📈 Use Cases

**Development Scenarios:**
- Local development with containerized databases
- Integration testing with test database instances
- Service isolation during feature development

**Production Operations:**
- Multi-tenant database management
- Cache invalidation and warming strategies
- Metrics collection for monitoring dashboards
- Database failover and recovery procedures

**Scaling Scenarios:**
- Read replica configuration for high-traffic endpoints
- Database sharding for large datasets
- Cache clustering for improved performance
- Time-series data retention policies

## 🛠️ Improvement Suggestions

**Performance Optimizations:**
- Implement connection pooling configuration options (Medium effort, High impact)
- Add database health check endpoints (Low effort, Medium impact)
- Optimize connection timeout settings (Low effort, Low impact)

**Feature Enhancements:**
- Add database configuration validation (Medium effort, High impact)
- Implement database migration management (High effort, High impact)
- Add monitoring and alerting integration (Medium effort, Medium impact)

**Maintenance Recommendations:**
- Monthly review of connection pool settings
- Quarterly database performance analysis
- Annual security audit of database access patterns

## 🏷️ Document Tags

**Keywords:** database-config, multi-database, mysql-config, redis-cache, mongodb-document, influxdb-metrics, connection-management, microservices-data, configuration-hub, data-layer, database-factory, environment-config, cache-config, metrics-storage, maas-platform

**Technical Tags:** #database #config #mysql #redis #mongodb #influxdb #microservices #nodejs #koa #maas-core #connection-pool #cache #metrics #multi-tenant

**Target Roles:** Backend developers (intermediate), DevOps engineers (beginner), Database administrators (intermediate), System architects (advanced)

**Difficulty Level:** ⭐⭐ (Moderate - requires understanding of multi-database architecture and environment configuration)

**Maintenance Level:** Low (configuration changes are infrequent, mainly environment updates)

**Business Criticality:** High (database connectivity is essential for all application functionality)

**Related Topics:** Database administration, microservices architecture, caching strategies, time-series monitoring, multi-tenancy, connection pooling, environment configuration