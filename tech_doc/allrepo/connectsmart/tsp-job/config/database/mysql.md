# TSP Job Service - MySQL Database Configuration

## Overview

The `config/database/mysql.js` file manages MySQL database configuration for the TSP Job service's relational database requirements. This configuration supports multiple MySQL database instances for different functional domains including portal operations, dataset management, GTFS transit data, and incentive systems.

## File Information

- **File Path**: `/config/database/mysql.js`
- **File Type**: JavaScript Configuration Module
- **Primary Purpose**: MySQL connection configuration for multiple database instances
- **Dependencies**: Environment variables for database credentials and connection settings

## Configuration Structure

```javascript
module.exports = {
  portal: { /* Portal database configuration */ },
  dataset: { /* Dataset database configuration */ },
  gtfs: { /* GTFS transit database configuration */ },
  incentive: { /* Incentive system database configuration */ },
};
```

## Database Instance Configurations

### 1. Portal Database Instance
```javascript
portal: {
  host: process.env.MYSQL_PORTAL_HOST,
  port: process.env.MYSQL_PORTAL_PORT || 3306,
  user: process.env.MYSQL_PORTAL_USER,
  password: process.env.MYSQL_PORTAL_PASSWORD,
  database: process.env.MYSQL_PORTAL_DB,
  charset: 'utf8mb4',
  dateStrings: true,
}
```

**Purpose**: Core portal operations and user management
- **Functional Domain**: User accounts, authentication, portal configurations
- **Character Set**: UTF-8MB4 for full Unicode support including emojis
- **Date Handling**: String format for consistent date processing

**Use Cases**:
- User registration and authentication
- Session management
- Portal configuration settings
- User preferences and profiles
- Administrative operations

**Typical Tables**:
- `users` - User account information
- `user_sessions` - Active user sessions
- `user_preferences` - User configuration settings
- `admin_users` - Administrative accounts
- `system_config` - Portal configuration

### 2. Dataset Database Instance
```javascript
dataset: {
  host: process.env.MYSQL_DATASET_HOST,
  port: process.env.MYSQL_DATASET_PORT || 3306,
  user: process.env.MYSQL_DATASET_USER,
  password: process.env.MYSQL_DATASET_PASSWORD,
  database: process.env.MYSQL_DATASET_DB,
  charset: 'utf8mb4',
  dateStrings: true,
}
```

**Purpose**: Primary transactional data and trip management
- **Functional Domain**: Trip data, reservations, payments, analytics
- **Character Set**: UTF-8MB4 for international location names
- **Date Handling**: String format for precise timestamp management

**Use Cases**:
- Trip records and reservations
- Payment transactions
- User activity tracking
- Ride-sharing coordination
- Performance analytics

**Typical Tables**:
- `trips` - Trip booking and completion data
- `reservations` - Transportation reservations
- `payments` - Financial transactions
- `user_activities` - User interaction logs
- `performance_metrics` - System performance data

### 3. GTFS Database Instance
```javascript
gtfs: {
  host: process.env.MYSQL_GTFS_HOST,
  port: process.env.MYSQL_GTFS_PORT || 3306,
  user: process.env.MYSQL_GTFS_USER,
  password: process.env.MYSQL_GTFS_PASSWORD,
  database: process.env.MYSQL_GTFS_DB,
  charset: 'utf8mb4',
  dateStrings: true,
}
```

**Purpose**: GTFS (General Transit Feed Specification) data management
- **Functional Domain**: Public transit data, routes, schedules, stops
- **Character Set**: UTF-8MB4 for international transit system names
- **Date Handling**: String format for schedule precision

**Use Cases**:
- Transit route information
- Schedule data management
- Stop location and details
- Service calendar information
- Real-time transit updates

**Typical Tables**:
- `gtfs_routes` - Transit route definitions
- `gtfs_stops` - Transit stop locations
- `gtfs_stop_times` - Schedule information
- `gtfs_trips` - Trip patterns
- `gtfs_calendar` - Service calendar data
- `gtfs_calendar_dates` - Service exceptions

### 4. Incentive Database Instance
```javascript
incentive: {
  host: process.env.MYSQL_INCENTIVE_HOST,
  port: process.env.MYSQL_INCENTIVE_PORT || 3306,
  user: process.env.MYSQL_INCENTIVE_USER,
  password: process.env.MYSQL_INCENTIVE_PASSWORD,
  database: process.env.MYSQL_INCENTIVE_DB,
  charset: 'utf8',
  dateStrings: true,
}
```

**Purpose**: Incentive program and points management system
- **Functional Domain**: Points, rewards, challenges, gamification
- **Character Set**: UTF-8 (legacy system compatibility)
- **Date Handling**: String format for reward tracking

**Use Cases**:
- Points accumulation and redemption
- Challenge management
- Reward distribution
- User engagement tracking
- Incentive program analytics

**Typical Tables**:
- `points_transactions` - Points earning and spending
- `user_challenges` - Active user challenges
- `rewards` - Available rewards catalog
- `challenge_definitions` - Challenge templates
- `user_badges` - Achievement tracking

## Database Connection Implementation

### Knex.js Integration
```javascript
const knex = require('knex');
const config = require('../config/database/mysql');

// Portal database connection
const portalDB = knex({
  client: 'mysql2',
  connection: config.portal,
  pool: {
    min: 2,
    max: 10,
    createTimeoutMillis: 3000,
    acquireTimeoutMillis: 30000,
    idleTimeoutMillis: 30000,
    reapIntervalMillis: 1000,
    createRetryIntervalMillis: 100
  },
  acquireConnectionTimeout: 60000,
  useNullAsDefault: true
});

// Dataset database connection
const datasetDB = knex({
  client: 'mysql2',
  connection: config.dataset,
  pool: {
    min: 5,
    max: 20,
    createTimeoutMillis: 3000,
    acquireTimeoutMillis: 30000,
    idleTimeoutMillis: 30000,
    reapIntervalMillis: 1000,
    createRetryIntervalMillis: 100
  },
  acquireConnectionTimeout: 60000,
  useNullAsDefault: true
});

// GTFS database connection (read-heavy)
const gtfsDB = knex({
  client: 'mysql2',
  connection: config.gtfs,
  pool: {
    min: 3,
    max: 15,
    createTimeoutMillis: 3000,
    acquireTimeoutMillis: 30000,
    idleTimeoutMillis: 60000, // Longer idle time for read operations
    reapIntervalMillis: 1000,
    createRetryIntervalMillis: 100
  },
  acquireConnectionTimeout: 60000,
  useNullAsDefault: true
});

// Incentive database connection
const incentiveDB = knex({
  client: 'mysql2',
  connection: config.incentive,
  pool: {
    min: 2,
    max: 8,
    createTimeoutMillis: 3000,
    acquireTimeoutMillis: 30000,
    idleTimeoutMillis: 30000,
    reapIntervalMillis: 1000,
    createRetryIntervalMillis: 100
  },
  acquireConnectionTimeout: 60000,
  useNullAsDefault: true
});
```

### Objection.js Model Integration
```javascript
const { Model } = require('objection');

// Portal database models
class User extends Model {
  static get tableName() { return 'users'; }
  static get knex() { return portalDB; }
  
  static get jsonSchema() {
    return {
      type: 'object',
      required: ['email', 'username'],
      properties: {
        id: { type: 'integer' },
        email: { type: 'string', format: 'email' },
        username: { type: 'string', minLength: 3, maxLength: 50 },
        created_at: { type: 'string', format: 'date-time' }
      }
    };
  }
}

// Dataset database models
class Trip extends Model {
  static get tableName() { return 'trips'; }
  static get knex() { return datasetDB; }
  
  static get relationMappings() {
    return {
      user: {
        relation: Model.BelongsToOneRelation,
        modelClass: User,
        join: {
          from: 'trips.user_id',
          to: 'users.id'
        }
      }
    };
  }
}

// GTFS database models
class GTFSRoute extends Model {
  static get tableName() { return 'gtfs_routes'; }
  static get knex() { return gtfsDB; }
  
  static get jsonSchema() {
    return {
      type: 'object',
      required: ['route_id', 'route_short_name', 'route_type'],
      properties: {
        route_id: { type: 'string' },
        route_short_name: { type: 'string' },
        route_long_name: { type: 'string' },
        route_type: { type: 'integer' }
      }
    };
  }
}

// Incentive database models
class PointsTransaction extends Model {
  static get tableName() { return 'points_transactions'; }
  static get knex() { return incentiveDB; }
  
  static get jsonSchema() {
    return {
      type: 'object',
      required: ['user_id', 'points', 'transaction_type'],
      properties: {
        id: { type: 'integer' },
        user_id: { type: 'integer' },
        points: { type: 'integer' },
        transaction_type: { type: 'string', enum: ['earn', 'redeem', 'bonus'] },
        created_at: { type: 'string', format: 'date-time' }
      }
    };
  }
}
```

## Cross-Database Operations

### Transaction Management
```javascript
class CrossDatabaseTransaction {
  static async processUserTrip(tripData, pointsData) {
    // Start transactions on multiple databases
    const datasetTrx = await datasetDB.transaction();
    const incentiveTrx = await incentiveDB.transaction();
    
    try {
      // Create trip record
      const trip = await Trip.query(datasetTrx).insert({
        user_id: tripData.userId,
        origin: tripData.origin,
        destination: tripData.destination,
        distance: tripData.distance,
        duration: tripData.duration,
        status: 'completed'
      });
      
      // Award points for the trip
      await PointsTransaction.query(incentiveTrx).insert({
        user_id: tripData.userId,
        points: pointsData.points,
        transaction_type: 'earn',
        reference_id: trip.id,
        reference_type: 'trip'
      });
      
      // Commit both transactions
      await datasetTrx.commit();
      await incentiveTrx.commit();
      
      return { trip, pointsAwarded: pointsData.points };
      
    } catch (error) {
      // Rollback both transactions
      await datasetTrx.rollback();
      await incentiveTrx.rollback();
      throw error;
    }
  }
}
```

### Data Synchronization
```javascript
class DatabaseSynchronizer {
  static async syncUserData() {
    // Sync user data between portal and dataset databases
    const portalUsers = await User.query()
      .select('id', 'email', 'username', 'updated_at')
      .where('updated_at', '>', knex.raw('DATE_SUB(NOW(), INTERVAL 1 HOUR)'));
    
    for (const user of portalUsers) {
      await datasetDB('user_profiles')
        .insert({
          user_id: user.id,
          email: user.email,
          username: user.username,
          synced_at: new Date()
        })
        .onDuplicateKeyUpdate(['email', 'username', 'synced_at']);
    }
  }
  
  static async syncGTFSData() {
    // Update GTFS data from external feed
    const routes = await GTFSRoute.query()
      .select('route_id', 'route_short_name', 'route_long_name')
      .where('route_type', 3); // Bus routes
    
    // Sync to dataset database for trip planning
    await datasetDB('transit_routes')
      .insert(routes.map(route => ({
        gtfs_route_id: route.route_id,
        name: route.route_short_name,
        description: route.route_long_name,
        type: 'bus',
        updated_at: new Date()
      })))
      .onDuplicateKeyUpdate(['name', 'description', 'updated_at']);
  }
}
```

## Performance Optimization

### Query Optimization Strategies
```javascript
// Optimized queries for each database type
class OptimizedQueries {
  // Portal database - User lookup with caching
  static async getUserById(userId) {
    return await User.query()
      .findById(userId)
      .select('id', 'email', 'username', 'status')
      .cache(300); // 5-minute cache
  }
  
  // Dataset database - Trip analytics with indexes
  static async getTripStatistics(userId, timeRange = 30) {
    return await datasetDB('trips')
      .select(
        datasetDB.raw('COUNT(*) as trip_count'),
        datasetDB.raw('SUM(distance) as total_distance'),
        datasetDB.raw('AVG(duration) as avg_duration'),
        datasetDB.raw('SUM(cost) as total_cost')
      )
      .where('user_id', userId)
      .where('created_at', '>=', datasetDB.raw('DATE_SUB(NOW(), INTERVAL ? DAY)', [timeRange]))
      .where('status', 'completed')
      .first();
  }
  
  // GTFS database - Route lookup with spatial indexing
  static async findNearbyRoutes(lat, lng, radiusKm = 1) {
    return await gtfsDB('gtfs_stops')
      .select('stop_id', 'stop_name', 'stop_lat', 'stop_lon')
      .whereRaw(
        'ST_Distance_Sphere(POINT(stop_lon, stop_lat), POINT(?, ?)) <= ?',
        [lng, lat, radiusKm * 1000]
      )
      .limit(10);
  }
  
  // Incentive database - Points balance with aggregation
  static async getUserPointsBalance(userId) {
    const result = await incentiveDB('points_transactions')
      .select(
        incentiveDB.raw('SUM(CASE WHEN transaction_type IN ("earn", "bonus") THEN points ELSE 0 END) as earned'),
        incentiveDB.raw('SUM(CASE WHEN transaction_type = "redeem" THEN points ELSE 0 END) as redeemed')
      )
      .where('user_id', userId)
      .first();
    
    return {
      balance: result.earned - result.redeemed,
      totalEarned: result.earned,
      totalRedeemed: result.redeemed
    };
  }
}
```

### Connection Pool Tuning
```javascript
// Environment-specific pool configurations
const getPoolConfig = (dbType, environment) => {
  const configs = {
    development: {
      portal: { min: 1, max: 5 },
      dataset: { min: 2, max: 8 },
      gtfs: { min: 1, max: 3 },
      incentive: { min: 1, max: 3 }
    },
    production: {
      portal: { min: 5, max: 20 },
      dataset: { min: 10, max: 50 },
      gtfs: { min: 5, max: 15 },
      incentive: { min: 3, max: 12 }
    }
  };
  
  return configs[environment][dbType] || { min: 2, max: 10 };
};
```

## Security Configuration

### Connection Security
```javascript
// SSL configuration for production
const sslConfig = {
  ssl: {
    rejectUnauthorized: true,
    ca: fs.readFileSync(process.env.MYSQL_SSL_CA),
    key: fs.readFileSync(process.env.MYSQL_SSL_KEY),
    cert: fs.readFileSync(process.env.MYSQL_SSL_CERT)
  }
};

// Apply SSL to production connections
if (process.env.NODE_ENV === 'production') {
  Object.keys(config).forEach(dbName => {
    config[dbName] = { ...config[dbName], ...sslConfig };
  });
}
```

### Query Security
```javascript
// Prepared statement examples
class SecureQueries {
  static async getUserByEmail(email) {
    // Parameterized query prevents SQL injection
    return await portalDB('users')
      .where('email', email)
      .first();
  }
  
  static async searchTrips(searchTerm) {
    // Escaped search term
    return await datasetDB('trips')
      .where('origin', 'like', `%${searchTerm}%`)
      .orWhere('destination', 'like', `%${searchTerm}%`)
      .limit(50);
  }
}
```

## Monitoring and Health Checks

### Database Health Monitoring
```javascript
async function checkDatabaseHealth() {
  const databases = { portalDB, datasetDB, gtfsDB, incentiveDB };
  const healthStatus = {};
  
  for (const [name, db] of Object.entries(databases)) {
    try {
      const start = Date.now();
      await db.raw('SELECT 1');
      healthStatus[name] = {
        status: 'healthy',
        latency: Date.now() - start,
        pool: {
          used: db.client.pool.numUsed(),
          free: db.client.pool.numFree(),
          max: db.client.pool.max
        }
      };
    } catch (error) {
      healthStatus[name] = {
        status: 'unhealthy',
        error: error.message
      };
    }
  }
  
  return healthStatus;
}
```

### Performance Monitoring
```javascript
// Query performance monitoring
const queryMetrics = new Map();

function recordQueryMetrics(database, query, duration, rowCount) {
  const key = `${database}_${query}`;
  if (!queryMetrics.has(key)) {
    queryMetrics.set(key, {
      count: 0,
      totalDuration: 0,
      totalRows: 0,
      minDuration: Infinity,
      maxDuration: 0
    });
  }
  
  const metrics = queryMetrics.get(key);
  metrics.count++;
  metrics.totalDuration += duration;
  metrics.totalRows += rowCount;
  metrics.minDuration = Math.min(metrics.minDuration, duration);
  metrics.maxDuration = Math.max(metrics.maxDuration, duration);
}
```

This MySQL configuration provides a comprehensive foundation for relational data management across multiple functional domains in the TSP Job service, supporting the diverse data requirements of the MaaS platform with optimized performance, security, and reliability.