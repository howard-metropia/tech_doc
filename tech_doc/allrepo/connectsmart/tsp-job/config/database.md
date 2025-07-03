# TSP Job Service - Database Configuration Hub

## Overview

The `config/database.js` file serves as the central database configuration hub for the TSP Job service, orchestrating connections to multiple database systems used across the MaaS platform. This module consolidates database configurations for MySQL, Redis, MongoDB, and InfluxDB, providing a unified interface for database connectivity management.

## File Information

- **File Path**: `/config/database.js`
- **File Type**: JavaScript Configuration Module
- **Primary Purpose**: Database connection configuration aggregation
- **Dependencies**: Individual database configuration modules

## Configuration Structure

```javascript
module.exports = {
  mysql: require('./database/mysql'),
  redis: require('./database/redis'),
  mongo: require('./database/mongo'),
  influx: require('./database/influx'),
};
```

## Database Architecture Overview

The TSP Job service utilizes a polyglot persistence architecture, leveraging different database technologies for their specific strengths:

### 1. MySQL Database
**Purpose**: Primary relational database for transactional data
- **Configuration Module**: `./database/mysql`
- **Use Cases**: 
  - User accounts and authentication
  - Trip records and reservations
  - Financial transactions and points
  - System configurations and metadata

**Key Features**:
- ACID compliance for critical transactions
- Complex relational queries for analytics
- Mature ecosystem with extensive tooling
- High availability and replication support

### 2. Redis Database
**Purpose**: In-memory data structure store for caching and sessions
- **Configuration Module**: `./database/redis`
- **Use Cases**:
  - Session management and user tokens
  - Distributed caching layer
  - Job queue management
  - Real-time data buffering

**Key Features**:
- Sub-millisecond response times
- Built-in data expiration
- Pub/Sub messaging capabilities
- Atomic operations and transactions

### 3. MongoDB Database
**Purpose**: Document-oriented database for flexible data structures
- **Configuration Module**: `./database/mongo`
- **Use Cases**:
  - Job queue data and metadata
  - Geospatial data and trajectory analysis
  - Analytics and reporting data
  - Schema-flexible configuration storage

**Key Features**:
- Flexible document schemas
- Built-in geospatial indexing
- Horizontal scaling capabilities
- Rich query language for complex data

### 4. InfluxDB Database
**Purpose**: Time-series database for metrics and monitoring
- **Configuration Module**: `./database/influx`
- **Use Cases**:
  - Application performance metrics
  - Job execution statistics
  - System health monitoring
  - Time-based analytics and reporting

**Key Features**:
- Optimized for time-series data
- Built-in downsampling and retention
- High write throughput
- Efficient storage compression

## Database Integration Patterns

### Connection Management
Each database configuration module handles:
- Connection string construction
- Connection pool management
- Authentication and security
- Error handling and reconnection logic

### Transaction Coordination
For operations spanning multiple databases:
```javascript
async function processJobWithTransaction(jobData) {
  const mysqlTrx = await knex.transaction();
  const mongoSession = await mongoose.startSession();
  
  try {
    mongoSession.startTransaction();
    
    // MySQL operations
    await MySQLModel.query(mysqlTrx).insert(jobData.relationalData);
    
    // MongoDB operations
    await MongoModel.create([jobData.documentData], { session: mongoSession });
    
    // Redis operations (no transactions, but atomic operations)
    await redis.multi()
      .set(jobData.cacheKey, jobData.cacheValue)
      .expire(jobData.cacheKey, 3600)
      .exec();
    
    // Commit all transactions
    await mysqlTrx.commit();
    await mongoSession.commitTransaction();
    
  } catch (error) {
    // Rollback all transactions
    await mysqlTrx.rollback();
    await mongoSession.abortTransaction();
    throw error;
  } finally {
    await mongoSession.endSession();
  }
}
```

## Configuration Usage in Application

### Database Initialization
```javascript
const config = require('config');
const databaseConfig = config.get('database');

// Initialize MySQL with Knex and Objection
const knex = require('knex')(databaseConfig.mysql);
const { Model } = require('objection');
Model.knex(knex);

// Initialize MongoDB with Mongoose
const mongoose = require('mongoose');
await mongoose.connect(databaseConfig.mongo.uri, databaseConfig.mongo.options);

// Initialize Redis
const redis = require('redis');
const redisClient = redis.createClient(databaseConfig.redis);

// Initialize InfluxDB
const { InfluxDB } = require('@influxdata/influxdb-client');
const influxClient = new InfluxDB(databaseConfig.influx);
```

### Health Check Implementation
```javascript
async function performDatabaseHealthChecks() {
  const healthStatus = {
    mysql: { status: 'unknown', latency: null },
    redis: { status: 'unknown', latency: null },
    mongo: { status: 'unknown', latency: null },
    influx: { status: 'unknown', latency: null }
  };
  
  // MySQL health check
  try {
    const start = Date.now();
    await knex.raw('SELECT 1');
    healthStatus.mysql = {
      status: 'healthy',
      latency: Date.now() - start
    };
  } catch (error) {
    healthStatus.mysql = {
      status: 'unhealthy',
      error: error.message
    };
  }
  
  // Redis health check
  try {
    const start = Date.now();
    await redisClient.ping();
    healthStatus.redis = {
      status: 'healthy',
      latency: Date.now() - start
    };
  } catch (error) {
    healthStatus.redis = {
      status: 'unhealthy',
      error: error.message
    };
  }
  
  // MongoDB health check
  try {
    const start = Date.now();
    await mongoose.connection.db.admin().ping();
    healthStatus.mongo = {
      status: 'healthy',
      latency: Date.now() - start
    };
  } catch (error) {
    healthStatus.mongo = {
      status: 'unhealthy',
      error: error.message
    };
  }
  
  // InfluxDB health check
  try {
    const start = Date.now();
    await influxClient.ping();
    healthStatus.influx = {
      status: 'healthy',
      latency: Date.now() - start
    };
  } catch (error) {
    healthStatus.influx = {
      status: 'unhealthy',
      error: error.message
    };
  }
  
  return healthStatus;
}
```

## Data Flow Patterns

### 1. Job Processing Data Flow
```
1. Job Request → Redis Queue
2. Job Processing → MySQL (transactional data)
3. Job Results → MongoDB (flexible documents)
4. Job Metrics → InfluxDB (time-series data)
5. Caching → Redis (performance optimization)
```

### 2. User Interaction Data Flow
```
1. User Request → MySQL (user data validation)
2. Session Check → Redis (authentication cache)
3. Activity Log → MongoDB (flexible event data)
4. Performance Metrics → InfluxDB (monitoring)
```

### 3. Analytics Data Flow
```
1. Raw Data → MySQL (source of truth)
2. Aggregation → MongoDB (flexible aggregation)
3. Caching → Redis (query result cache)
4. Metrics → InfluxDB (time-based analysis)
```

## Performance Optimization

### Connection Pooling
Each database uses optimized connection pooling:
- **MySQL**: Knex.js connection pool with configurable min/max connections
- **MongoDB**: Mongoose connection pool with automatic management
- **Redis**: Redis client with connection reuse
- **InfluxDB**: HTTP client with keep-alive connections

### Query Optimization
- **MySQL**: Proper indexing, query optimization, and prepared statements
- **MongoDB**: Compound indexes, aggregation pipeline optimization
- **Redis**: Pipeline operations, key expiration strategies
- **InfluxDB**: Batch writes, optimized retention policies

### Caching Strategies
```javascript
// Multi-level caching implementation
async function getCachedData(key, mysqlQuery, options = {}) {
  // Level 1: Redis cache
  const cached = await redis.get(key);
  if (cached) {
    return JSON.parse(cached);
  }
  
  // Level 2: Database query
  const data = await knex.raw(mysqlQuery);
  
  // Cache the result
  await redis.setex(key, options.ttl || 3600, JSON.stringify(data));
  
  return data;
}
```

## Security Configuration

### Connection Security
- **MySQL**: SSL/TLS encryption, credential rotation
- **MongoDB**: Authentication, role-based access control
- **Redis**: AUTH authentication, SSL support
- **InfluxDB**: Token-based authentication, HTTPS

### Data Security
- Encryption at rest for sensitive data
- Connection encryption in transit
- Database user privilege separation
- Regular security audits and updates

## Monitoring and Observability

### Database Metrics Collection
```javascript
// Metrics collection for all databases
function collectDatabaseMetrics() {
  return {
    mysql: {
      connections: knex.client.pool.numUsed(),
      maxConnections: knex.client.pool.max,
      queryCount: mysqlQueryCounter.get(),
      avgLatency: mysqlLatencyHistogram.mean()
    },
    redis: {
      connections: redisClient.status,
      memoryUsage: redisInfo.used_memory,
      hitRate: (redisInfo.keyspace_hits / (redisInfo.keyspace_hits + redisInfo.keyspace_misses)) * 100
    },
    mongo: {
      connections: mongoose.connection.readyState,
      collections: mongoose.connection.collections.length,
      documents: mongoDocumentCounter.get()
    },
    influx: {
      writePoints: influxWriteCounter.get(),
      queries: influxQueryCounter.get(),
      retention: influxRetentionInfo
    }
  };
}
```

## Backup and Recovery

### Backup Strategies
- **MySQL**: Automated daily backups with point-in-time recovery
- **MongoDB**: Replica set with automated backup
- **Redis**: RDB snapshots and AOF logging
- **InfluxDB**: Backup with retention policy management

### Disaster Recovery
- Cross-region replication for critical databases
- Automated failover mechanisms
- Recovery time objective (RTO) and recovery point objective (RPO) targets
- Regular disaster recovery testing

## Migration Management

### Schema Migrations
```javascript
// MySQL migrations with Knex
await knex.migrate.latest();

// MongoDB migrations with custom scripts
await runMongoMigrations();

// Redis key migrations
await migrateRedisKeyStructure();
```

### Data Migration
- Cross-database data synchronization
- ETL processes for data transformation
- Validation and rollback procedures
- Performance impact monitoring

This database configuration hub provides a robust foundation for the TSP Job service's multi-database architecture, ensuring optimal performance, security, and reliability across all data persistence layers.