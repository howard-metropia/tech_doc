# TSP Job Service - Redis Configuration

## Overview

The `config/database/redis.js` file manages Redis configuration for the TSP Job service's in-memory data structure store requirements. Redis serves as a high-performance caching layer, session manager, and real-time data buffer for the MaaS platform's distributed architecture.

## File Information

- **File Path**: `/config/database/redis.js`
- **File Type**: JavaScript Configuration Module
- **Primary Purpose**: Redis connection configuration and cache management
- **Dependencies**: Environment variables for Redis server credentials and connection settings

## Configuration Structure

```javascript
module.exports = {
  cache: {
    host: process.env.REDIS_CACHE_HOST,
    password: process.env.REDIS_CACHE_PASSWORD,
    port: process.env.REDIS_CACHE_PORT,
    maxRetriesPerRequest: null,
    enableReadyCheck: false,
  },
};
```

## Configuration Components

### Cache Instance Configuration
```javascript
cache: {
  host: process.env.REDIS_CACHE_HOST,
  password: process.env.REDIS_CACHE_PASSWORD,
  port: process.env.REDIS_CACHE_PORT,
  maxRetriesPerRequest: null,
  enableReadyCheck: false,
}
```

**Configuration Parameters**:
- **host**: Redis server hostname or IP address
- **password**: Authentication password for Redis server
- **port**: Redis server port (typically 6379)
- **maxRetriesPerRequest**: Disables retry mechanism for failed requests
- **enableReadyCheck**: Disables connection ready state checking for performance

**Purpose**: Primary Redis instance for high-performance caching operations

**Performance Optimizations**:
- `maxRetriesPerRequest: null` - Prevents infinite retry loops in high-load scenarios
- `enableReadyCheck: false` - Reduces connection overhead for established connections

## Redis Implementation Patterns

### Connection Management
```javascript
const Redis = require('ioredis');
const config = require('../config/database/redis');

// Primary cache connection
const redisCache = new Redis({
  host: config.cache.host,
  port: config.cache.port,
  password: config.cache.password,
  maxRetriesPerRequest: config.cache.maxRetriesPerRequest,
  enableReadyCheck: config.cache.enableReadyCheck,
  retryDelayOnFailover: 100,
  maxRetriesPerRequest: 3,
  lazyConnect: true,
  keepAlive: 30000,
  connectTimeout: 10000,
  commandTimeout: 5000,
  family: 4 // IPv4
});

// Connection event handlers
redisCache.on('connect', () => {
  console.log('Redis connected successfully');
});

redisCache.on('error', (error) => {
  console.error('Redis connection error:', error);
});

redisCache.on('close', () => {
  console.log('Redis connection closed');
});

redisCache.on('reconnecting', () => {
  console.log('Redis reconnecting...');
});
```

### Session Management
```javascript
class SessionManager {
  static async createSession(userId, sessionData, ttl = 3600) {
    const sessionId = `session:${userId}:${Date.now()}`;
    const sessionKey = `user_session:${sessionId}`;
    
    await redisCache.hmset(sessionKey, {
      user_id: userId,
      created_at: new Date().toISOString(),
      last_activity: new Date().toISOString(),
      ...sessionData
    });
    
    await redisCache.expire(sessionKey, ttl);
    return sessionId;
  }
  
  static async getSession(sessionId) {
    const sessionKey = `user_session:${sessionId}`;
    const session = await redisCache.hgetall(sessionKey);
    
    if (Object.keys(session).length === 0) {
      return null;
    }
    
    // Update last activity
    await redisCache.hset(sessionKey, 'last_activity', new Date().toISOString());
    
    return session;
  }
  
  static async extendSession(sessionId, ttl = 3600) {
    const sessionKey = `user_session:${sessionId}`;
    return await redisCache.expire(sessionKey, ttl);
  }
  
  static async destroySession(sessionId) {
    const sessionKey = `user_session:${sessionId}`;
    return await redisCache.del(sessionKey);
  }
  
  static async getUserSessions(userId) {
    const pattern = `user_session:session:${userId}:*`;
    const keys = await redisCache.keys(pattern);
    
    const sessions = [];
    for (const key of keys) {
      const session = await redisCache.hgetall(key);
      if (Object.keys(session).length > 0) {
        sessions.push({ sessionId: key.split(':')[2], ...session });
      }
    }
    
    return sessions;
  }
}
```

### Caching Layer Implementation
```javascript
class CacheManager {
  static async set(key, value, ttl = 3600) {
    const serializedValue = JSON.stringify(value);
    if (ttl) {
      return await redisCache.setex(key, ttl, serializedValue);
    } else {
      return await redisCache.set(key, serializedValue);
    }
  }
  
  static async get(key) {
    const value = await redisCache.get(key);
    if (value === null) return null;
    
    try {
      return JSON.parse(value);
    } catch (error) {
      console.error('Cache parse error:', error);
      return null;
    }
  }
  
  static async del(key) {
    return await redisCache.del(key);
  }
  
  static async mget(keys) {
    const values = await redisCache.mget(keys);
    return values.map(value => {
      if (value === null) return null;
      try {
        return JSON.parse(value);
      } catch (error) {
        return null;
      }
    });
  }
  
  static async mset(keyValuePairs, ttl = null) {
    const pipeline = redisCache.pipeline();
    
    for (const [key, value] of Object.entries(keyValuePairs)) {
      const serializedValue = JSON.stringify(value);
      if (ttl) {
        pipeline.setex(key, ttl, serializedValue);
      } else {
        pipeline.set(key, serializedValue);
      }
    }
    
    return await pipeline.exec();
  }
  
  static async exists(key) {
    return await redisCache.exists(key);
  }
  
  static async expire(key, ttl) {
    return await redisCache.expire(key, ttl);
  }
  
  static async ttl(key) {
    return await redisCache.ttl(key);
  }
  
  static async keys(pattern) {
    return await redisCache.keys(pattern);
  }
  
  static async flushPattern(pattern) {
    const keys = await redisCache.keys(pattern);
    if (keys.length > 0) {
      return await redisCache.del(...keys);
    }
    return 0;
  }
}
```

### Job Queue Implementation
```javascript
class JobQueue {
  static async enqueue(queueName, jobData, priority = 0) {
    const jobId = `job:${Date.now()}:${Math.random().toString(36).substr(2, 9)}`;
    const job = {
      id: jobId,
      data: jobData,
      priority: priority,
      created_at: new Date().toISOString(),
      status: 'pending'
    };
    
    // Add job to priority queue (sorted set)
    await redisCache.zadd(`queue:${queueName}`, priority, JSON.stringify(job));
    
    // Add job details to hash
    await redisCache.hset(`job:${jobId}`, job);
    
    // Set job expiration (24 hours)
    await redisCache.expire(`job:${jobId}`, 86400);
    
    return jobId;
  }
  
  static async dequeue(queueName) {
    // Get highest priority job
    const jobs = await redisCache.zrevrange(`queue:${queueName}`, 0, 0);
    
    if (jobs.length === 0) return null;
    
    const job = JSON.parse(jobs[0]);
    
    // Remove from queue
    await redisCache.zrem(`queue:${queueName}`, jobs[0]);
    
    // Update job status
    await redisCache.hset(`job:${job.id}`, 'status', 'processing');
    
    return job;
  }
  
  static async completeJob(jobId, result = null) {
    await redisCache.hmset(`job:${jobId}`, {
      status: 'completed',
      completed_at: new Date().toISOString(),
      result: result ? JSON.stringify(result) : null
    });
    
    // Set shorter expiration for completed jobs
    await redisCache.expire(`job:${jobId}`, 3600);
  }
  
  static async failJob(jobId, error) {
    await redisCache.hmset(`job:${jobId}`, {
      status: 'failed',
      failed_at: new Date().toISOString(),
      error: error.message || error.toString()
    });
    
    // Keep failed jobs longer for debugging
    await redisCache.expire(`job:${jobId}`, 7200);
  }
  
  static async getJobStatus(jobId) {
    return await redisCache.hgetall(`job:${jobId}`);
  }
  
  static async getQueueStats(queueName) {
    const queueLength = await redisCache.zcard(`queue:${queueName}`);
    const processingJobs = await redisCache.keys('job:*');
    
    let pendingCount = 0;
    let processingCount = 0;
    let completedCount = 0;
    let failedCount = 0;
    
    for (const jobKey of processingJobs) {
      const status = await redisCache.hget(jobKey, 'status');
      switch (status) {
        case 'pending': pendingCount++; break;
        case 'processing': processingCount++; break;
        case 'completed': completedCount++; break;
        case 'failed': failedCount++; break;
      }
    }
    
    return {
      queueLength,
      pending: pendingCount,
      processing: processingCount,
      completed: completedCount,
      failed: failedCount
    };
  }
}
```

### Real-time Data Management
```javascript
class RealtimeDataManager {
  static async publishEvent(channel, eventData) {
    const event = {
      timestamp: new Date().toISOString(),
      data: eventData
    };
    
    return await redisCache.publish(channel, JSON.stringify(event));
  }
  
  static async subscribe(channel, callback) {
    const subscriber = redisCache.duplicate();
    
    subscriber.subscribe(channel);
    subscriber.on('message', (receivedChannel, message) => {
      if (receivedChannel === channel) {
        try {
          const event = JSON.parse(message);
          callback(event);
        } catch (error) {
          console.error('Error parsing event:', error);
        }
      }
    });
    
    return subscriber;
  }
  
  static async setRealtimeData(key, data, ttl = 60) {
    const realtimeKey = `realtime:${key}`;
    await redisCache.setex(realtimeKey, ttl, JSON.stringify({
      timestamp: new Date().toISOString(),
      data: data
    }));
  }
  
  static async getRealtimeData(key) {
    const realtimeKey = `realtime:${key}`;
    const value = await redisCache.get(realtimeKey);
    
    if (!value) return null;
    
    try {
      return JSON.parse(value);
    } catch (error) {
      return null;
    }
  }
  
  static async updateUserLocation(userId, lat, lng, accuracy = null) {
    const locationKey = `location:${userId}`;
    const locationData = {
      latitude: lat,
      longitude: lng,
      accuracy: accuracy,
      timestamp: new Date().toISOString()
    };
    
    // Store current location
    await redisCache.setex(locationKey, 300, JSON.stringify(locationData)); // 5 minutes TTL
    
    // Add to geospatial index
    await redisCache.geoadd('user_locations', lng, lat, userId);
    
    // Publish location update
    await this.publishEvent('location_updates', {
      userId: userId,
      location: locationData
    });
  }
  
  static async findNearbyUsers(lat, lng, radiusKm = 1, unit = 'km') {
    return await redisCache.georadius('user_locations', lng, lat, radiusKm, unit, 'WITHDIST', 'WITHCOORD');
  }
}
```

## Performance Optimization

### Connection Pooling and Clustering
```javascript
// Redis Cluster configuration for high availability
const cluster = new Redis.Cluster([
  { host: process.env.REDIS_CLUSTER_HOST_1, port: 6379 },
  { host: process.env.REDIS_CLUSTER_HOST_2, port: 6379 },
  { host: process.env.REDIS_CLUSTER_HOST_3, port: 6379 }
], {
  redisOptions: {
    password: process.env.REDIS_CLUSTER_PASSWORD,
    maxRetriesPerRequest: 3
  },
  enableOfflineQueue: false,
  maxRetriesPerRequest: 3,
  retryDelayOnFailover: 100
});

// Pipeline operations for batch processing
class OptimizedCacheOperations {
  static async batchSet(items, ttl = 3600) {
    const pipeline = redisCache.pipeline();
    
    for (const [key, value] of Object.entries(items)) {
      pipeline.setex(key, ttl, JSON.stringify(value));
    }
    
    return await pipeline.exec();
  }
  
  static async batchGet(keys) {
    const pipeline = redisCache.pipeline();
    
    keys.forEach(key => pipeline.get(key));
    
    const results = await pipeline.exec();
    return results.map(([error, result]) => {
      if (error || result === null) return null;
      try {
        return JSON.parse(result);
      } catch (e) {
        return null;
      }
    });
  }
  
  static async atomicIncrement(key, increment = 1, ttl = null) {
    const pipeline = redisCache.pipeline();
    pipeline.incrby(key, increment);
    if (ttl) {
      pipeline.expire(key, ttl);
    }
    const results = await pipeline.exec();
    return results[0][1]; // Return the incremented value
  }
}
```

### Memory Management
```javascript
class MemoryManager {
  static async getMemoryInfo() {
    const info = await redisCache.info('memory');
    const lines = info.split('\r\n');
    const memoryInfo = {};
    
    lines.forEach(line => {
      if (line.includes(':')) {
        const [key, value] = line.split(':');
        memoryInfo[key] = value;
      }
    });
    
    return {
      usedMemory: parseInt(memoryInfo.used_memory),
      usedMemoryHuman: memoryInfo.used_memory_human,
      maxMemory: parseInt(memoryInfo.maxmemory),
      maxMemoryHuman: memoryInfo.maxmemory_human,
      memoryUsagePercentage: memoryInfo.maxmemory > 0 
        ? (parseInt(memoryInfo.used_memory) / parseInt(memoryInfo.maxmemory)) * 100 
        : 0
    };
  }
  
  static async cleanupExpiredKeys() {
    // Force cleanup of expired keys
    await redisCache.eval(`
      local cursor = "0"
      repeat
        local result = redis.call("SCAN", cursor, "COUNT", 100)
        cursor = result[1]
        local keys = result[2]
        for i=1, #keys do
          if redis.call("TTL", keys[i]) == -1 then
            -- Key has no expiration, check if it should
            local keyType = redis.call("TYPE", keys[i])["ok"]
            if keyType == "string" and string.match(keys[i], "^(session|cache|temp):") then
              redis.call("EXPIRE", keys[i], 3600)
            end
          end
        end
      until cursor == "0"
      return "OK"
    `, 0);
  }
  
  static async clearNamespace(namespace) {
    const pattern = `${namespace}:*`;
    const keys = await redisCache.keys(pattern);
    
    if (keys.length > 0) {
      // Delete in batches to avoid blocking
      const batchSize = 100;
      for (let i = 0; i < keys.length; i += batchSize) {
        const batch = keys.slice(i, i + batchSize);
        await redisCache.del(...batch);
      }
    }
    
    return keys.length;
  }
}
```

## Monitoring and Health Checks

### Health Check Implementation
```javascript
async function checkRedisHealth() {
  try {
    const start = Date.now();
    const pingResult = await redisCache.ping();
    const latency = Date.now() - start;
    
    const info = await redisCache.info('server');
    const memoryInfo = await MemoryManager.getMemoryInfo();
    
    return {
      status: 'healthy',
      latency: latency,
      ping: pingResult,
      uptime: info.match(/uptime_in_seconds:(\d+)/)[1],
      memory: memoryInfo,
      connections: {
        connected: await redisCache.client('list'),
        total: info.match(/connected_clients:(\d+)/)[1]
      }
    };
  } catch (error) {
    return {
      status: 'unhealthy',
      error: error.message,
      timestamp: new Date().toISOString()
    };
  }
}
```

### Performance Monitoring
```javascript
class RedisMetrics {
  static async getOperationStats() {
    const info = await redisCache.info('stats');
    const lines = info.split('\r\n');
    const stats = {};
    
    lines.forEach(line => {
      if (line.includes(':')) {
        const [key, value] = line.split(':');
        if (key.includes('commands_processed') || 
            key.includes('instantaneous_ops') ||
            key.includes('keyspace_hits') ||
            key.includes('keyspace_misses')) {
          stats[key] = parseInt(value) || value;
        }
      }
    });
    
    // Calculate hit rate
    const hits = stats.keyspace_hits || 0;
    const misses = stats.keyspace_misses || 0;
    stats.hit_rate = hits + misses > 0 ? (hits / (hits + misses)) * 100 : 0;
    
    return stats;
  }
  
  static async getSlowLogs(count = 10) {
    return await redisCache.slowlog('get', count);
  }
}
```

## Security Configuration

### Authentication and Access Control
```javascript
// Enhanced Redis configuration with authentication
const secureRedisConfig = {
  host: config.cache.host,
  port: config.cache.port,
  password: config.cache.password,
  
  // TLS configuration for production
  ...(process.env.NODE_ENV === 'production' && {
    tls: {
      rejectUnauthorized: true,
      cert: fs.readFileSync(process.env.REDIS_TLS_CERT),
      key: fs.readFileSync(process.env.REDIS_TLS_KEY),
      ca: fs.readFileSync(process.env.REDIS_TLS_CA)
    }
  }),
  
  // Connection security
  connectTimeout: 10000,
  lazyConnect: true,
  keepAlive: 30000,
  
  // Prevent command abuse
  maxRetriesPerRequest: 3,
  retryDelayOnFailover: 100
};
```

This Redis configuration provides a robust, high-performance caching and session management foundation for the TSP Job service, supporting the real-time and scalability requirements of the MaaS platform with optimized memory usage, comprehensive monitoring, and security best practices.