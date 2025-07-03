# ParkMobile Cache Purge Test Suite

## Overview
Comprehensive test suite for the ParkMobile cache purging functionality that validates the automated cleanup of outdated cached data from MongoDB collections. The test ensures proper data retention policies and database maintenance for ParkMobile parking events and price objects, preventing unnecessary storage accumulation.

## File Location
`/test/testPmPurgeCache.js`

## Technical Analysis

### Core Service Under Test
```javascript
const { purgeOutdatedCache } = require('@app/src/services/parkMobile');
```

This service function implements intelligent cache purging based on configurable age thresholds, removing outdated parking event data and price information that no longer serves active user sessions.

### Dependencies
- `@maas/core/bootstrap` - Application bootstrap and environment configuration
- `chai` - Assertion library with expect interface for validation
- `@app/src/models/pmParkingEvents` - MongoDB model for parking event cache
- `@app/src/models/pmPriceObjects` - MongoDB model for parking price cache
- `moment` - Date/time manipulation for age calculation
- `@maas/core/log` - Centralized logging for cache operations

### MongoDB Collection Models

#### ParkMobile Parking Events Cache
```javascript
const PmParkingEvents = require('@app/src/models/pmParkingEvents');
```
Stores cached parking session data with HTTP status tracking and creation timestamps for automated cleanup.

#### ParkMobile Price Objects Cache  
```javascript
const PmPriceObjects = require('@app/src/models/pmPriceObjects');
```
Maintains cached pricing information for parking zones with zone identifiers and temporal data for retention management.

### Test Data Architecture

#### Mock Parking Events
```javascript
const mockParkingEvents = [
  {
    _id: 'fakeEvent01',
    http_status: 0,
    createdAt: moment.utc().add(-95, 'days'),    // Should be purged
  },
  {
    _id: 'fakeEvent02', 
    http_status: 0,
    createdAt: moment.utc().add(-89, 'days'),    // Should be purged
  },
  {
    _id: 'fakeEvent03',
    http_status: 0,                               // Recent, should remain
  },
];
```

#### Mock Price Objects
```javascript
const mockPriceObjects = [
  {
    _id: 'fakePrice01',
    zone: '953471198',
    createdAt: moment.utc().add(-50, 'days'),    // Should be purged
  },
  {
    _id: 'fakePrice02',
    zone: '953471198', 
    createdAt: moment.utc().add(-29, 'days'),    // Should be purged
  },
  {
    _id: 'fakePrice03',
    zone: '953471198',                           // Recent, should remain
  },
];
```

### Cache Retention Policy Testing

#### Age-Based Purging Logic
The test validates the service's ability to:
- **Identify Outdated Records**: Detect records exceeding configured age thresholds
- **Preserve Recent Data**: Maintain recently created cache entries
- **Selective Deletion**: Remove only expired data while preserving active cache

#### Expected Retention Behavior
Based on the test data configuration:
- Records older than approximately 90 days are purged
- Records newer than 30 days are retained
- The exact thresholds are managed by the service configuration

## Usage/Integration

### Test Execution Flow
1. **Setup Phase**: Inserts mock data with various creation timestamps
2. **Execution Phase**: Runs the cache purging service function
3. **Validation Phase**: Verifies correct retention of recent data and removal of outdated entries
4. **Cleanup Phase**: Removes remaining test data to maintain database cleanliness

### Purge Operation Validation
```javascript
it('should purge the outdated data', async function () {
  await purgeOutdatedCache();
  
  const outDatedPriceObjs = await PmPriceObjects.find({
    _id: { $regex: 'fake' },
  });
  expect(outDatedPriceObjs.length).to.eq(2);
  
  const outDatedEvents = await PmParkingEvents.find({
    _id: { $regex: 'fake' },
  });
  expect(outDatedEvents.length).to.eq(2);
});
```

The test expects exactly 2 records to remain in each collection after purging, indicating that 1 record per collection was successfully removed based on age criteria.

### Database Setup and Teardown
```javascript
before(async () => {
  const res = await PmParkingEvents.insertMany(mockParkingEvents);
  logger.info(res);
  const res2 = await PmPriceObjects.insertMany(mockPriceObjects);
  logger.info(res2);
});

after(async () => {
  const res = await PmParkingEvents.deleteMany({ _id: { $regex: 'fake' } });
  logger.info(res);
  const res2 = await PmPriceObjects.deleteMany({ _id: { $regex: 'fake' } });
  logger.info(res2);
});
```

## Code Examples

### Cache Age Analysis
```javascript
const oldEventExample = {
  _id: 'event_to_purge',
  http_status: 0,
  createdAt: moment.utc().add(-95, 'days'),  // 95 days old
  user_session_data: { ... },
  parking_details: { ... }
};
```

### MongoDB Query Pattern for Cleanup
```javascript
// Service implementation pattern (inferred from test behavior)
const purgeThreshold = moment.utc().subtract(90, 'days').toDate();

// Remove outdated parking events
await PmParkingEvents.deleteMany({
  createdAt: { $lt: purgeThreshold }
});

// Remove outdated price objects  
await PmPriceObjects.deleteMany({
  createdAt: { $lt: purgeThreshold }
});
```

### Logging Integration
```javascript
before(async () => {
  const res = await PmParkingEvents.insertMany(mockParkingEvents);
  logger.info(res);  // Log insertion results for debugging
});
```

### Regex-Based Test Data Management
```javascript
// Clean up all test records using regex pattern
await PmParkingEvents.deleteMany({ _id: { $regex: 'fake' } });
await PmPriceObjects.deleteMany({ _id: { $regex: 'fake' } });
```

## Integration Points

### MongoDB Integration
- **Connection Management**: Uses established MongoDB connections through model layer
- **Collection Operations**: Bulk insert and delete operations for efficient data management
- **Index Utilization**: Leverages database indexes for efficient age-based queries

### Cache Management Strategy
- **Automated Cleanup**: Scheduled purging prevents database bloat
- **Performance Optimization**: Removes stale data that could impact query performance
- **Storage Efficiency**: Maintains optimal storage utilization for active data

### System Maintenance
- **Background Jobs**: Typically executed as scheduled maintenance tasks
- **Monitoring Integration**: Logging provides visibility into purge operations
- **Data Retention Compliance**: Implements configurable data lifecycle policies

### ParkMobile Service Dependencies
- **API Response Caching**: Cached data from ParkMobile API calls
- **Session Data Management**: Temporary storage for active parking sessions
- **Price Information Cache**: Cached pricing data for quick user responses

### Configuration Management
The purging service likely supports:
- **Configurable Thresholds**: Adjustable age limits for different data types
- **Selective Purging**: Different retention policies for events vs. prices
- **Performance Tuning**: Batch size and execution frequency controls

This test suite ensures the ParkMobile cache purging system maintains optimal database performance by automatically removing outdated cached data while preserving recently accessed information needed for active user sessions and current parking operations.