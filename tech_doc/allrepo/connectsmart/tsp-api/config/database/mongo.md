# MongoDB Database Configuration

## 🔍 Quick Summary (TL;DR)

MongoDB database configuration module that exports cache and dataset connection instances for the TSP API, enabling distributed caching and dataset storage across the mobility platform.

**Keywords:** mongodb | mongo | database | config | cache | dataset | connection | tsp-api | maas | database-configuration | nosql | document-database

**Primary Use Cases:**
- Database connection management for MongoDB instances
- Separation of cache and dataset storage concerns  
- Centralized MongoDB configuration for microservices
- Real-time data caching and persistent dataset storage

**Compatibility:** Node.js 16+, MongoDB 4.4+, @maas/core package

## ❓ Common Questions Quick Index

**Q: How do I connect to MongoDB cache database?**
A: Use `require('./config/database/mongo').cache` - see [Usage Methods](#usage-methods)

**Q: What's the difference between cache and dataset connections?**
A: Cache for temporary data, dataset for persistent storage - see [Functionality Overview](#functionality-overview)

**Q: How to troubleshoot MongoDB connection issues?**
A: Check environment variables and connection strings - see [Important Notes](#important-notes)

**Q: Can I add more MongoDB connections?**
A: Yes, extend the module with additional database calls - see [Improvement Suggestions](#improvement-suggestions)

**Q: What if MongoDB is unavailable?**
A: Connections will retry automatically via @maas/core - see [Error Handling](#error-handling)

**Q: How to configure MongoDB for different environments?**
A: Environment-specific configs via @maas/core - see [Technical Specifications](#technical-specifications)

**Q: What MongoDB operations are supported?**
A: Full MongoDB driver functionality through connections - see [Usage Methods](#usage-methods)

**Q: How to monitor MongoDB performance?**
A: Use built-in MongoDB monitoring and @maas/core metrics - see [Output Examples](#output-examples)

## 📋 Functionality Overview

**Non-technical Explanation:**
Think of this file as a phone directory for databases - it knows exactly how to reach two different MongoDB databases (cache and dataset). Like having separate filing cabinets for temporary notes versus permanent records, this ensures the right data goes to the right place without confusion.

**Technical Explanation:**
Configuration module that exports MongoDB connection instances using the @maas/core database factory pattern. Implements separation of concerns with dedicated connections for caching and dataset operations.

**Business Value:**
Enables scalable data architecture by separating ephemeral cache data from persistent datasets, supporting real-time mobility services while maintaining data integrity and performance optimization.

**System Context:**
Central database configuration for TSP API within the ConnectSmart microservices ecosystem, providing MongoDB connectivity for transit operations, user tracking, and real-time mobility data.

## 🔧 Technical Specifications

**File Information:**
- **Name:** mongo.js
- **Path:** /config/database/mongo.js  
- **Language:** JavaScript (Node.js)
- **Type:** Configuration module
- **Size:** ~120 bytes
- **Complexity:** ⭐ (Simple configuration export)

**Dependencies:**
- `@maas/core/config`: Core database configuration factory (Critical)
  - Purpose: Provides standardized MongoDB connection management
  - Version: Latest (managed by workspace)

**Compatibility Matrix:**
- Node.js: 16.0+ (Required)
- MongoDB: 4.4+ (Recommended 5.0+)
- @maas/core: Latest version
- Mongoose: 6.0+ (if used with connections)

**Configuration Parameters:**
- Cache database: Configured via @maas/core database.mongo("cache")
- Dataset database: Configured via @maas/core database.mongo("dataset")
- Connection strings: Environment-specific via @maas/core

**System Requirements:**
- Memory: Minimal (<1MB)
- Network: MongoDB cluster access
- Security: MongoDB authentication credentials

## 📝 Detailed Code Analysis

**Module Structure:**
```javascript
const { database } = require('@maas/core/config');
module.exports = {
  cache: database.mongo("cache"),
  dataset: database.mongo("dataset"),
};
```

**Execution Flow:**
1. Import database factory from @maas/core
2. Create cache MongoDB connection instance
3. Create dataset MongoDB connection instance  
4. Export both connections as named properties

**Design Patterns:**
- **Factory Pattern:** @maas/core provides database connection factory
- **Configuration Object:** Exports structured connection instances
- **Separation of Concerns:** Distinct connections for different data types

**Memory Usage:**
- Static configuration with minimal memory footprint
- Connection pooling handled by @maas/core
- No memory leaks as connections are managed externally

## 🚀 Usage Methods

**Basic Import:**
```javascript
const mongo = require('./config/database/mongo');
const { cache, dataset } = require('./config/database/mongo');
```

**Cache Database Operations:**
```javascript
const { cache } = require('./config/database/mongo');

// Store temporary data
await cache.collection('sessions').insertOne({
  userId: '12345',
  token: 'jwt-token',
  expires: new Date(Date.now() + 3600000)
});

// Retrieve cached data
const session = await cache.collection('sessions')
  .findOne({ userId: '12345' });
```

**Dataset Database Operations:**
```javascript
const { dataset } = require('./config/database/mongo');

// Store persistent mobility data
await dataset.collection('trips').insertOne({
  userId: '12345',
  startLocation: { lat: 37.7749, lng: -122.4194 },
  endLocation: { lat: 37.7849, lng: -122.4094 },
  timestamp: new Date(),
  mode: 'transit'
});

// Query historical data
const userTrips = await dataset.collection('trips')
  .find({ userId: '12345' })
  .sort({ timestamp: -1 })
  .limit(10)
  .toArray();
```

**Service Integration:**
```javascript
const mongo = require('./config/database/mongo');

class CacheService {
  constructor() {
    this.db = mongo.cache;
  }
  
  async set(key, value, ttl = 3600) {
    return this.db.collection('cache').insertOne({
      key, value, expires: new Date(Date.now() + ttl * 1000)
    });
  }
}
```

## 📊 Output Examples

**Successful Connection:**
```javascript
// Connection objects returned
{
  cache: MongoClient { 
    topology: Topology { ... },
    options: { useUnifiedTopology: true },
    readPreference: ReadPreference { mode: 'primary' }
  },
  dataset: MongoClient { 
    topology: Topology { ... },
    options: { useUnifiedTopology: true },
    readPreference: ReadPreference { mode: 'primary' }
  }
}
```

**Database Operation Results:**
```javascript
// Insert operation
{ acknowledged: true, insertedId: ObjectId('...') }

// Find operation  
[
  { _id: ObjectId('...'), userId: '12345', timestamp: 2024-01-15T10:30:00.000Z },
  { _id: ObjectId('...'), userId: '12345', timestamp: 2024-01-15T09:15:00.000Z }
]

// Count operation
{ totalTrips: 247, cacheEntries: 1503 }
```

**Error Scenarios:**
```javascript
// Connection error
MongoServerError: Authentication failed
// Resolution: Check MongoDB credentials in environment

// Database not found  
MongoError: Database 'cache' not found
// Resolution: Ensure database exists or auto-creation is enabled
```

## ⚠️ Important Notes

**Security Considerations:**
- MongoDB credentials managed via @maas/core environment configuration
- Use connection string authentication, never hardcode credentials
- Enable MongoDB authentication and SSL/TLS in production
- Implement proper access controls and role-based permissions

**Common Troubleshooting:**

*Symptom:* Connection timeout errors
*Diagnosis:* Network connectivity or MongoDB server availability
*Solution:* Verify MongoDB cluster status and network firewall rules

*Symptom:* Authentication failures  
*Diagnosis:* Invalid credentials or expired certificates
*Solution:* Update environment variables and rotate certificates

*Symptom:* Database not found errors
*Diagnosis:* Missing database creation or incorrect naming
*Solution:* Create databases or verify naming conventions

**Performance Considerations:**
- Connection pooling automatically managed by @maas/core
- Use appropriate indexes on frequently queried collections
- Monitor connection pool metrics and adjust pool size if needed
- Cache connection has shorter TTL, dataset optimized for persistence

**Environment Configuration:**
- Development: Local MongoDB or Docker containers
- Staging: Shared MongoDB cluster with staging databases  
- Production: Dedicated MongoDB clusters with replication

## 🔗 Related File Links

**Direct Dependencies:**
- `@maas/core/config`: Core configuration package (external BitBucket repo)
- `config/default.js`: Environment-specific database configuration
- `src/services/`: Services consuming MongoDB connections

**Related Database Files:**
- `config/database.js`: MySQL database configuration
- `config/vendor.js`: Third-party service configurations  
- `src/middlewares/auth.js`: Authentication using cache database

**Service Consumers:**
- `src/services/notification.js`: Uses cache for temporary notifications
- `src/services/trip.js`: Uses dataset for persistent trip storage
- `src/controllers/*`: Various controllers accessing both databases

**Testing:**
- `test/integration/mongo.test.js`: MongoDB integration tests
- `test/helpers/database.js`: Test database setup utilities

## 📈 Use Cases

**Cache Database Scenarios:**
- Session management and JWT token storage
- Temporary notification queues and real-time updates
- API response caching and rate limiting data
- User preference caching and temporary calculations

**Dataset Database Scenarios:**  
- Historical trip data and mobility analytics
- User profile persistence and activity logging
- Transit schedule data and route information
- Payment transaction records and audit trails

**Development Workflow:**
- Local development with Docker MongoDB containers
- Integration testing with dedicated test databases
- Performance testing with production-like data volumes
- Database migration and schema evolution management

**Anti-patterns to Avoid:**
- Don't store large files directly in MongoDB (use GridFS or external storage)
- Avoid cross-database transactions (use application-level coordination)
- Don't bypass connection pooling by creating direct connections
- Avoid storing sensitive data without proper encryption

## 🛠️ Improvement Suggestions

**Performance Optimization:**
- Add read preference configuration for query optimization
- Implement connection monitoring and health checks
- Add database-specific connection pool tuning parameters
- Consider MongoDB sharding for high-volume datasets

**Feature Enhancements:**
- Add support for additional specialized databases (e.g., analytics, logs)
- Implement automatic database creation and index management
- Add connection retry logic with exponential backoff
- Create database migration utilities for schema changes

**Monitoring Improvements:**
- Add MongoDB performance metrics collection
- Implement connection pool monitoring and alerting
- Create database health check endpoints
- Add query performance logging and slow query detection

**Code Quality:**
- Add JSDoc documentation for exported connections
- Implement TypeScript definitions for better IDE support
- Add unit tests for configuration validation
- Create configuration schema validation

## 🏷️ Document Tags

**Keywords:** mongodb, mongo, database, config, connection, cache, dataset, nosql, document-database, tsp-api, maas, microservices, configuration, connectivity, data-storage, real-time, persistence

**Technical Tags:** #mongodb #database-config #connection-management #cache #dataset #nosql #maas #tsp-api #microservices #data-architecture

**Target Roles:**
- Backend developers (intermediate)
- DevOps engineers (beginner) 
- Database administrators (beginner)
- System architects (intermediate)

**Difficulty Level:** ⭐⭐ (Simple with external dependencies)
**Maintenance Level:** Low (stable configuration)
**Business Criticality:** High (essential for data operations)
**Related Topics:** database-administration, mongodb-operations, microservices-architecture, data-storage, caching-strategies