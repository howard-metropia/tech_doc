# TSP Job Service - MongoDB Configuration

## Overview

The `config/database/mongo.js` file manages MongoDB configuration for the TSP Job service's document-oriented database requirements. MongoDB is used for flexible data storage, job queue management, geospatial data processing, and analytics across the MaaS platform.

## File Information

- **File Path**: `/config/database/mongo.js`
- **File Type**: JavaScript Configuration Module
- **Primary Purpose**: MongoDB connection configuration management
- **Dependencies**: Environment variables for database credentials and connection settings

## Configuration Structure

```javascript
module.exports = {
  cache: {
    username: process.env.MONGO_CACHE_USER,
    password: process.env.MONGO_CACHE_PASSWORD,
    database: process.env.MONGO_CACHE_DB,
    host: process.env.MONGO_CACHE_HOST,
    port: process.env.MONGO_CACHE_PORT || 27017,
  },
  dataset: {
    username: process.env.MONGO_DATASET_USER,
    password: process.env.MONGO_DATASET_PASSWORD,
    database: process.env.MONGO_DATASET_DB,
    host: process.env.MONGO_DATASET_HOST,
    port: process.env.MONGO_DATASET_PORT || 27017,
  },
};
```

## Database Instance Configurations

### 1. Cache Database Instance
```javascript
cache: {
  username: process.env.MONGO_CACHE_USER,
  password: process.env.MONGO_CACHE_PASSWORD,
  database: process.env.MONGO_CACHE_DB,
  host: process.env.MONGO_CACHE_HOST,
  port: process.env.MONGO_CACHE_PORT || 27017,
}
```

**Purpose**: High-performance caching layer for temporary and frequently accessed data

**Use Cases**:
- Job queue data and metadata
- Session information and user tokens
- API response caching
- Temporary computation results
- Real-time data buffering

**Configuration Details**:
- **username/password**: Authentication credentials for cache database
- **database**: Dedicated database name for cache operations
- **host**: MongoDB server hostname or IP address
- **port**: MongoDB server port (default: 27017)

**Performance Characteristics**:
- Optimized for high read/write throughput
- TTL (Time-To-Live) indexes for automatic data expiration
- Memory-mapped storage for faster access
- Minimal data persistence requirements

### 2. Dataset Database Instance
```javascript
dataset: {
  username: process.env.MONGO_DATASET_USER,
  password: process.env.MONGO_DATASET_PASSWORD,
  database: process.env.MONGO_DATASET_DB,
  host: process.env.MONGO_DATASET_HOST,
  port: process.env.MONGO_DATASET_PORT || 27017,
}
```

**Purpose**: Persistent data storage for complex documents and analytical datasets

**Use Cases**:
- Trip trajectory and geospatial data
- User behavior analytics
- Complex reporting datasets
- Configuration and metadata storage
- Machine learning training data

**Configuration Details**:
- **username/password**: Authentication credentials for dataset database
- **database**: Dedicated database name for persistent datasets
- **host**: MongoDB server hostname (may be different from cache instance)
- **port**: MongoDB server port (default: 27017)

**Performance Characteristics**:
- Optimized for complex queries and aggregations
- Comprehensive indexing for analytical workloads
- Durable storage with replication
- Support for large document sizes

## Connection Implementation

### Cache Database Connection
```javascript
const mongoose = require('mongoose');
const config = require('../config/database/mongo');

// Cache database connection
const cacheConnection = mongoose.createConnection(
  `mongodb://${config.cache.username}:${config.cache.password}@${config.cache.host}:${config.cache.port}/${config.cache.database}`,
  {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    maxPoolSize: 10,
    serverSelectionTimeoutMS: 5000,
    socketTimeoutMS: 45000,
    bufferCommands: false,
    bufferMaxEntries: 0
  }
);

// Cache-specific schemas and models
const jobQueueSchema = new mongoose.Schema({
  jobId: { type: String, required: true, unique: true },
  jobType: { type: String, required: true },
  payload: { type: mongoose.Schema.Types.Mixed },
  status: { type: String, enum: ['pending', 'processing', 'completed', 'failed'] },
  priority: { type: Number, default: 0 },
  createdAt: { type: Date, default: Date.now, expires: 86400 }, // 24 hours TTL
  processedAt: Date,
  error: String
});

const JobQueue = cacheConnection.model('JobQueue', jobQueueSchema);
```

### Dataset Database Connection
```javascript
// Dataset database connection
const datasetConnection = mongoose.createConnection(
  `mongodb://${config.dataset.username}:${config.dataset.password}@${config.dataset.host}:${config.dataset.port}/${config.dataset.database}`,
  {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    maxPoolSize: 20,
    serverSelectionTimeoutMS: 5000,
    socketTimeoutMS: 60000,
    bufferCommands: true
  }
);

// Dataset-specific schemas and models
const tripTrajectorySchema = new mongoose.Schema({
  tripId: { type: String, required: true },
  userId: { type: String, required: true },
  trajectory: [{
    lat: Number,
    lng: Number,
    timestamp: Date,
    accuracy: Number,
    speed: Number
  }],
  startLocation: {
    type: { type: String, default: 'Point' },
    coordinates: [Number] // [longitude, latitude]
  },
  endLocation: {
    type: { type: String, default: 'Point' },
    coordinates: [Number]
  },
  distance: Number,
  duration: Number,
  mode: String,
  createdAt: { type: Date, default: Date.now }
});

// Geospatial index for location queries
tripTrajectorySchema.index({ startLocation: '2dsphere' });
tripTrajectorySchema.index({ endLocation: '2dsphere' });
tripTrajectorySchema.index({ userId: 1, createdAt: -1 });

const TripTrajectory = datasetConnection.model('TripTrajectory', tripTrajectorySchema);
```

## Data Access Patterns

### 1. Job Queue Management (Cache Database)
```javascript
class JobQueueManager {
  static async enqueueJob(jobType, payload, priority = 0) {
    const jobId = `${jobType}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    return await JobQueue.create({
      jobId,
      jobType,
      payload,
      priority,
      status: 'pending'
    });
  }
  
  static async dequeueJob() {
    return await JobQueue.findOneAndUpdate(
      { status: 'pending' },
      { status: 'processing', processedAt: new Date() },
      { 
        sort: { priority: -1, createdAt: 1 },
        new: true 
      }
    );
  }
  
  static async completeJob(jobId, result = null) {
    return await JobQueue.findOneAndUpdate(
      { jobId, status: 'processing' },
      { 
        status: 'completed',
        result: result,
        completedAt: new Date()
      }
    );
  }
  
  static async failJob(jobId, error) {
    return await JobQueue.findOneAndUpdate(
      { jobId, status: 'processing' },
      { 
        status: 'failed',
        error: error.message,
        failedAt: new Date()
      }
    );
  }
}
```

### 2. Geospatial Data Operations (Dataset Database)
```javascript
class GeospatialDataManager {
  static async storeTripTrajectory(tripData) {
    return await TripTrajectory.create({
      tripId: tripData.tripId,
      userId: tripData.userId,
      trajectory: tripData.trajectory,
      startLocation: {
        type: 'Point',
        coordinates: [tripData.startLng, tripData.startLat]
      },
      endLocation: {
        type: 'Point',
        coordinates: [tripData.endLng, tripData.endLat]
      },
      distance: tripData.distance,
      duration: tripData.duration,
      mode: tripData.mode
    });
  }
  
  static async findTripsNearLocation(lat, lng, radiusKm = 1) {
    return await TripTrajectory.find({
      startLocation: {
        $near: {
          $geometry: {
            type: 'Point',
            coordinates: [lng, lat]
          },
          $maxDistance: radiusKm * 1000 // Convert km to meters
        }
      }
    });
  }
  
  static async getUserTripHistory(userId, limit = 100) {
    return await TripTrajectory.find({ userId })
      .sort({ createdAt: -1 })
      .limit(limit);
  }
  
  static async analyzeHabitualTrips(userId) {
    return await TripTrajectory.aggregate([
      { $match: { userId } },
      {
        $group: {
          _id: {
            startArea: {
              $geoNear: {
                $geometry: '$startLocation',
                distanceField: 'distance'
              }
            }
          },
          count: { $sum: 1 },
          avgDistance: { $avg: '$distance' },
          avgDuration: { $avg: '$duration' }
        }
      },
      { $sort: { count: -1 } },
      { $limit: 10 }
    ]);
  }
}
```

## Performance Optimization

### Index Strategies
```javascript
// Cache database indexes
db.jobQueue.createIndex({ status: 1, priority: -1, createdAt: 1 });
db.jobQueue.createIndex({ jobType: 1, status: 1 });
db.jobQueue.createIndex({ createdAt: 1 }, { expireAfterSeconds: 86400 });

// Dataset database indexes
db.tripTrajectory.createIndex({ userId: 1, createdAt: -1 });
db.tripTrajectory.createIndex({ startLocation: '2dsphere' });
db.tripTrajectory.createIndex({ endLocation: '2dsphere' });
db.tripTrajectory.createIndex({ mode: 1, createdAt: -1 });
```

### Connection Pooling
```javascript
const cacheConnectionOptions = {
  maxPoolSize: 10,        // Small pool for cache operations
  minPoolSize: 2,         // Minimum connections
  maxIdleTimeMS: 30000,   // Close connections after 30 seconds of inactivity
  serverSelectionTimeoutMS: 5000,
  socketTimeoutMS: 45000,
  connectTimeoutMS: 10000
};

const datasetConnectionOptions = {
  maxPoolSize: 20,        // Larger pool for complex queries
  minPoolSize: 5,         // Higher minimum for analytics workload
  maxIdleTimeMS: 60000,   // Longer idle time for persistent connections
  serverSelectionTimeoutMS: 5000,
  socketTimeoutMS: 60000,
  connectTimeoutMS: 10000
};
```

### Aggregation Pipeline Optimization
```javascript
// Optimized analytics queries
class AnalyticsManager {
  static async getUserEngagementMetrics(timeRange) {
    return await TripTrajectory.aggregate([
      {
        $match: {
          createdAt: {
            $gte: new Date(Date.now() - timeRange)
          }
        }
      },
      {
        $group: {
          _id: '$userId',
          tripCount: { $sum: 1 },
          totalDistance: { $sum: '$distance' },
          totalDuration: { $sum: '$duration' },
          modes: { $addToSet: '$mode' }
        }
      },
      {
        $project: {
          userId: '$_id',
          tripCount: 1,
          totalDistance: 1,
          totalDuration: 1,
          avgDistance: { $divide: ['$totalDistance', '$tripCount'] },
          avgDuration: { $divide: ['$totalDuration', '$tripCount'] },
          modeVariety: { $size: '$modes' }
        }
      },
      { $sort: { tripCount: -1 } }
    ]);
  }
}
```

## Security Configuration

### Authentication and Authorization
```javascript
// Secure connection string with authentication
const buildConnectionString = (config) => {
  const auth = config.username && config.password 
    ? `${encodeURIComponent(config.username)}:${encodeURIComponent(config.password)}@`
    : '';
    
  return `mongodb://${auth}${config.host}:${config.port}/${config.database}`;
};

// SSL/TLS configuration for production
const secureConnectionOptions = {
  ssl: true,
  sslValidate: true,
  sslCA: [fs.readFileSync('path/to/ca-certificate.crt')],
  sslCert: fs.readFileSync('path/to/client-certificate.crt'),
  sslKey: fs.readFileSync('path/to/client-key.key'),
  sslPass: process.env.MONGO_SSL_PASSPHRASE
};
```

### Data Encryption
```javascript
// Field-level encryption for sensitive data
const encryptedSchema = new mongoose.Schema({
  userId: String,
  encryptedData: {
    type: String,
    set: function(value) {
      return encrypt(JSON.stringify(value));
    },
    get: function(value) {
      return JSON.parse(decrypt(value));
    }
  }
});
```

## Monitoring and Health Checks

### Connection Health Monitoring
```javascript
async function checkMongoHealth() {
  const healthStatus = {
    cache: { status: 'unknown', latency: null },
    dataset: { status: 'unknown', latency: null }
  };
  
  // Check cache database
  try {
    const start = Date.now();
    await cacheConnection.db.admin().ping();
    healthStatus.cache = {
      status: 'healthy',
      latency: Date.now() - start,
      readyState: cacheConnection.readyState
    };
  } catch (error) {
    healthStatus.cache = {
      status: 'unhealthy',
      error: error.message
    };
  }
  
  // Check dataset database
  try {
    const start = Date.now();
    await datasetConnection.db.admin().ping();
    healthStatus.dataset = {
      status: 'healthy',
      latency: Date.now() - start,
      readyState: datasetConnection.readyState
    };
  } catch (error) {
    healthStatus.dataset = {
      status: 'unhealthy',
      error: error.message
    };
  }
  
  return healthStatus;
}
```

### Performance Metrics Collection
```javascript
// Database operation metrics
const mongoMetrics = {
  operations: new Map(),
  
  recordOperation(database, operation, duration, success) {
    const key = `${database}_${operation}`;
    if (!this.operations.has(key)) {
      this.operations.set(key, {
        count: 0,
        totalDuration: 0,
        errors: 0
      });
    }
    
    const stats = this.operations.get(key);
    stats.count++;
    stats.totalDuration += duration;
    if (!success) stats.errors++;
  },
  
  getMetrics() {
    const metrics = {};
    for (const [key, stats] of this.operations) {
      metrics[key] = {
        count: stats.count,
        avgDuration: stats.totalDuration / stats.count,
        errorRate: stats.errors / stats.count
      };
    }
    return metrics;
  }
};
```

## Backup and Recovery

### Automated Backup Strategy
```javascript
// Backup configuration for different databases
const backupConfig = {
  cache: {
    frequency: 'daily',
    retention: 7, // days
    compress: true,
    incremental: false
  },
  dataset: {
    frequency: 'hourly',
    retention: 30, // days
    compress: true,
    incremental: true
  }
};

async function performBackup(database) {
  const config = backupConfig[database];
  const timestamp = new Date().toISOString().replace(/:/g, '-');
  const backupName = `${database}_backup_${timestamp}`;
  
  // MongoDB dump command would be executed here
  // This is a conceptual example
  const command = `mongodump --host ${config.host}:${config.port} --db ${config.database} --out /backups/${backupName}`;
  
  // Execute backup and handle result
}
```

This MongoDB configuration provides a robust foundation for document-oriented data storage in the TSP Job service, supporting both high-performance caching operations and complex analytical workloads across the MaaS platform.