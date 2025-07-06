# Purge ParkMobile Cache Job

## Quick Summary
**Purpose**: Maintains database hygiene by removing outdated ParkMobile pricing and event data from MongoDB cache collections.

**Key Features**:
- Removes price objects older than 30 days
- Purges parking events older than 90 days
- Prevents unbounded database growth
- Maintains optimal query performance

**Functionality**: Executes periodic cleanup of MongoDB collections to remove stale ParkMobile data while preserving recent records needed for active operations and historical reporting.

## Technical Analysis

### Code Structure
The job uses a minimal wrapper around the service function:

```javascript
module.exports = {
  inputs: {},
  fn: purgeOutdatedCache
};
```

### Implementation Details

1. **Retention Policies**:
   - **Price Objects**: 30-day retention period
   - **Parking Events**: 90-day retention period
   - Different retention periods based on data importance and usage patterns

2. **Database Operations**:
   ```javascript
   const purgeOutdatedCache = async () => {
     const daysAgo = (days) => {
       return moment().subtract(days, 'days').toDate();
     };
     
     // Remove old price objects
     const thirtyDaysAgo = daysAgo(30);
     let result = await PmPriceObjects.deleteMany({
       createdAt: { $lt: thirtyDaysAgo },
     });
     
     // Remove old parking events
     const ninetyDaysAgo = daysAgo(90);
     result = await PmParkingEvents.deleteMany({
       createdAt: { $lt: ninetyDaysAgo },
     });
   };
   ```

3. **MongoDB Collections**:
   - `PmPriceObjects`: Caches parking rate information
   - `PmParkingEvents`: Stores historical parking session data

### Performance Optimization

1. **Bulk Deletion Strategy**:
   - Uses `deleteMany()` for efficient bulk operations
   - Single database round-trip per collection
   - Leverages MongoDB indexes on `createdAt` field

2. **Resource Management**:
   - Non-blocking asynchronous operations
   - Minimal memory footprint
   - No data loading into application memory

## Usage/Integration

### Scheduling Configuration
- **Frequency**: Daily (recommended at off-peak hours)
- **Timing**: 2:00 AM local time or during low-traffic periods
- **Priority**: Low - maintenance task

### Cron Expression
```
0 2 * * * // Daily at 2:00 AM
```

### Integration Points
1. **MongoDB Cache Database**: Primary data store
2. **ParkMobile Service**: Provides data models
3. **Logging System**: Tracks deletion metrics

## Dependencies

### Required Modules
```javascript
const { purgeOutdatedCache } = require('@app/src/services/parkMobile');
```

### Service Dependencies
```javascript
// From parkMobile service:
const axios = require('axios');
const moment = require('moment');
const PmParkingEvents = require('@app/src/models/pmParkingEvents');
const PmPriceObjects = require('@app/src/models/pmPriceObjects');
const { logger } = require('@maas/core/log');
```

### External Services
1. **MongoDB**: Cache database for ParkMobile data
2. **Logging Infrastructure**: For operation tracking

### Configuration Requirements
- MongoDB connection string
- Database name and collection configurations
- Logging level settings

## Code Examples

### Manual Execution
```javascript
// Run the cache purge manually
const job = require('./purge-parkmobile-cache');
await job.fn();
```

### Custom Retention Periods
```javascript
// Modify retention periods if needed
const customPurge = async (priceDays, eventDays) => {
  const priceDate = moment().subtract(priceDays, 'days').toDate();
  const eventDate = moment().subtract(eventDays, 'days').toDate();
  
  await PmPriceObjects.deleteMany({ createdAt: { $lt: priceDate } });
  await PmParkingEvents.deleteMany({ createdAt: { $lt: eventDate } });
};
```

### Monitoring Deletion Counts
```javascript
// Enhanced logging for monitoring
const result = await PmPriceObjects.deleteMany({
  createdAt: { $lt: thirtyDaysAgo },
});
logger.info(`[park-mobile.purgeCache] ${result.deletedCount} price objects deleted`);
```

### Error Handling
The service includes comprehensive error handling:

```javascript
try {
  // Deletion operations
} catch (err) {
  logger.error(`[park-mobile.purgeCache] ${err.message}`);
  logger.error(`[park-mobile.purgeCache] ${err.stack}`);
  throw err;
}
```

### Database Index Requirements
For optimal performance, ensure indexes exist:

```javascript
// MongoDB index recommendations
db.pmPriceObjects.createIndex({ createdAt: 1 });
db.pmParkingEvents.createIndex({ createdAt: 1 });
```

### Impact Analysis
1. **Storage Benefits**:
   - Reduces database size
   - Improves backup/restore times
   - Lowers storage costs

2. **Performance Benefits**:
   - Faster query execution
   - Reduced index size
   - Better cache utilization

3. **Data Lifecycle**:
   - Price data remains fresh and relevant
   - Historical events preserved for reporting
   - Compliance with data retention policies

### Monitoring Recommendations
- Track deletion counts over time
- Monitor database size trends
- Alert on failed purge operations
- Review retention policies quarterly