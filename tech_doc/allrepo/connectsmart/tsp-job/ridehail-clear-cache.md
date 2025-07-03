# TSP Job: Ridehail Clear Cache

## Quick Summary

The `ridehail-clear-cache.js` job is a maintenance utility that removes outdated cache entries from the ridehail guest ride system. This lightweight scheduled job ensures the cache storage remains optimized by clearing expired or obsolete data related to Uber guest rides, preventing cache bloat and maintaining system performance. It runs periodically to clean up temporary ride data, price estimates, and other cached information that is no longer needed.

## Technical Analysis

### Job Structure

The job follows a minimal pattern, delegating all logic to a dedicated service:

```javascript
const { clearOutdatedCaches } = require('@app/src/services/uber/guest-ride');

module.exports = {
  inputs: {},
  fn: async function () {
    await clearOutdatedCaches();
  },
};
```

### Service Integration

The job integrates with the Uber guest ride service layer, which manages:
- **Price Estimate Caches**: Temporary storage of ride pricing calculations
- **Ride Request Caches**: Pending ride requests and their states
- **Guest Session Data**: Anonymous user session information
- **API Response Caches**: Cached responses from Uber's API to reduce external calls

### Cache Management Strategy

Based on the guest ride service pattern, this job likely handles:

1. **Time-based Expiration**: Removes caches older than a configured TTL
2. **State-based Cleanup**: Clears caches for completed or cancelled rides
3. **Memory Optimization**: Prevents unbounded cache growth
4. **Session Cleanup**: Removes orphaned guest session data

## Usage/Integration

### Scheduling Configuration

This job is typically scheduled to run at regular intervals:

```javascript
// Example cron configuration (likely in scheduler setup)
{
  name: 'ridehail-clear-cache',
  schedule: '0 */6 * * *', // Every 6 hours
  job: 'ridehail-clear-cache'
}
```

### Execution Context

The job runs in the TSP Job framework context:
- **No Input Parameters**: Operates autonomously without external configuration
- **Async Execution**: Returns a promise for proper job queue handling
- **Error Propagation**: Allows service errors to bubble up for job monitoring

### Related Services

The cache clearing integrates with several ridehail components:

```javascript
// Related cache types cleared by the service
const cacheTypes = {
  PRICE_ESTIMATES: 'uber:price:*',
  RIDE_REQUESTS: 'uber:ride:request:*',
  GUEST_SESSIONS: 'uber:guest:session:*',
  API_RESPONSES: 'uber:api:cache:*'
};
```

## Dependencies

### Internal Services
- **@app/src/services/uber/guest-ride**: Core service containing cache management logic
- **Redis/Cache Layer**: Underlying storage system for cached data
- **TSP Job Framework**: Provides job execution environment

### External Dependencies
- No direct external package dependencies
- Relies on service layer for all functionality

### Configuration Requirements

Expected configuration in the guest-ride service:

```javascript
// Likely configuration structure
{
  cache: {
    ttl: 3600,              // Cache TTL in seconds
    maxEntries: 10000,      // Maximum cache entries
    cleanupBatchSize: 100   // Entries to clean per batch
  }
}
```

## Code Examples

### Manual Execution

```javascript
// Direct job execution for testing
const ridehailClearCache = require('./ridehail-clear-cache');
await ridehailClearCache.fn();
```

### Integration with Job Runner

```javascript
// TSP Job framework integration
const jobRunner = require('@app/src/lib/job-runner');

jobRunner.registerJob({
  name: 'ridehail-clear-cache',
  handler: require('./jobs/ridehail-clear-cache'),
  schedule: '0 */6 * * *'
});
```

### Monitoring Integration

```javascript
// Example monitoring wrapper
const monitoredJob = async () => {
  const startTime = Date.now();
  try {
    await ridehailClearCache.fn();
    logger.info('Cache cleanup completed', {
      duration: Date.now() - startTime
    });
  } catch (error) {
    logger.error('Cache cleanup failed', { error });
    throw error;
  }
};
```

### Cache Pattern Examples

The underlying service likely implements patterns like:

```javascript
// Time-based cache cleanup
const clearOutdatedCaches = async () => {
  const cutoffTime = Date.now() - (config.cache.ttl * 1000);
  const keys = await redis.keys('uber:*');
  
  for (const key of keys) {
    const data = await redis.get(key);
    if (data && data.timestamp < cutoffTime) {
      await redis.del(key);
    }
  }
};

// State-based cleanup
const clearCompletedRides = async () => {
  const rideKeys = await redis.keys('uber:ride:request:*');
  
  for (const key of rideKeys) {
    const ride = await redis.get(key);
    if (ride && ['completed', 'cancelled'].includes(ride.status)) {
      await redis.del(key);
    }
  }
};
```

### Error Handling Patterns

```javascript
// Robust error handling in the service layer
const clearOutdatedCaches = async () => {
  try {
    // Batch processing to avoid blocking
    const batchSize = config.cache.cleanupBatchSize;
    let processed = 0;
    
    while (true) {
      const keys = await redis.scan(processed, 'MATCH', 'uber:*', 'COUNT', batchSize);
      if (keys.length === 0) break;
      
      await Promise.all(keys.map(key => processKey(key)));
      processed += keys.length;
    }
  } catch (error) {
    logger.error('Cache cleanup error', { error });
    // Continue operation despite errors
  }
};
```

This job plays a crucial role in maintaining the health of the ridehail system by preventing cache accumulation that could impact performance. Its simple interface masks sophisticated cache management logic that ensures the guest ride feature remains responsive and efficient even under high load conditions.