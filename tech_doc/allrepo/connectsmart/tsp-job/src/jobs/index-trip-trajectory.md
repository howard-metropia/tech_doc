# Index Trip Trajectory Job

## Overview
Job that processes and indexes trip trajectory data from MongoDB, converting raw trajectory points into GeoJSON LineString format for efficient spatial queries and analysis. This job maintains an indexed collection for faster geographic analysis while managing data retention and synchronization with MySQL trip activity mappings.

## File Location
`/src/jobs/index-trip-trajectory.js`

## Dependencies
- `@maas/core/log` - Logging framework for operational monitoring
- `config` - Configuration management system
- `@maas/services` - Service collection including SlackManager
- `@maas/core/mysql` - MySQL database connection for portal database
- `@app/src/models/TripTrajectoryIndex` - MongoDB model for indexed trajectory data
- `@app/src/models/TripTrajectory` - MongoDB model for raw trajectory data
- `moment-timezone` - Date/time manipulation and timezone handling

## Job Configuration

### Inputs
```javascript
inputs: {}  // No input parameters - runs automatically based on internal logic
```

### Slack Integration Configuration
```javascript
const slackConfig = config.get('vendor.slack');
const { SlackManager } = require('@maas/services');
```

## Data Processing Workflow

### Phase 1: Activity ID Synchronization
**Get Last Indexed Activity ID**:
```javascript
const getActivityIDOfLastIndexedTripTrajectory = async () => {
  const result = await TripTrajectoryIndex.find()
    .sort({ last_activity_id_stamp: -1 })
    .limit(1)
    .lean();
  return result;
};
```

**Find Unprocessed Trip Activities**:
```javascript
const getNotIndexList = async (lastActivityID) => {
  const rawSql = 
    `SELECT m.trip_id, m.activity_id FROM trip_activity_mapping as m where activity_id > ${lastActivityID};`;
  const result = await knex.raw(rawSql);
  return result;
};
```

### Phase 2: Trajectory Data Processing
**Count Trajectory Records**:
```javascript
const getNumberOfTripTrajectory = async (tripList, dateTime) => {
  const result = await TripTrajectory.count({
    timestamp: { $gt: dateTime },
    trip_id: { $in: tripList }
  }).lean();
  return result;
};
```

**Paginated Trajectory Retrieval**:
```javascript
const getTripTrajectory = async (tripList, page, dateTime) => {
  const result = await TripTrajectory.find({ 
    timestamp: { $gt: dateTime }, 
    trip_id: { $in: tripList } 
  })
  .sort({ _id: 1 })
  .skip(page * 50)
  .limit(50)
  .lean();
  return result;
};
```

## GeoJSON Transformation

### LineString Conversion
```javascript
const transToGeoJson = (array) => {
  const result = array.map((t) => {
    let lineString = [];
    t.trajectory.forEach((trj) => {
      lineString.push([Number(trj.longitude), Number(trj.latitude)]);
    });
    return {
      trip_id: t.trip_id,
      timestamp: Number(t.timestamp),
      user_id: Number(t.user_id),
      trajectory: {
        type: 'LineString',
        coordinates: lineString
      }
    };
  });
  return result;
};
```

**GeoJSON Structure**:
- **Type**: LineString geometry for spatial indexing
- **Coordinates**: Array of [longitude, latitude] pairs
- **Properties**: Trip ID, timestamp, and user ID for referencing

## Index Management

### Upsert Operation
```javascript
const insertIndexedTripTrajectory = async (document, lastActivityID) => {
  const result = await TripTrajectoryIndex.updateOne(
    {
      trip_id: document.trip_id,
      timestamp: document.timestamp
    }, // filter
    {
      trip_id: document.trip_id,
      timestamp: document.timestamp,
      trajectory: document.trajectory,
      user_id: document.user_id,
      last_activity_id_stamp: lastActivityID
    }, // update
    {
      upsert: true
    }
  );
  return result;
};
```

### Data Retention Management
```javascript
const deleteIndexedTripTrajectory = async (outDate) => {
  const result = await TripTrajectoryIndex.deleteMany({
    timestamp: { $lt: outDate }
  });
  return result;
};
```

**Retention Logic**:
```javascript
const getOutdate = (nowTime) => {
  const formattedDatetime = moment(nowTime, 'YYYY-MM-DD HH:mm:ss');
  const previousMonth = formattedDatetime.subtract(1, 'months');
  const outDate = previousMonth.unix();
  return outDate;
};
```

## Batch Processing System

### Main Processing Loop
```javascript
const updateMainProcess = async (tripList, page, outDate, lastActivityID) => {
  const updateData = await getTripTrajectory(tripList, page, outDate);
  const geoJsonDocus = transToGeoJson(updateData);
  const allResult = await Promise.all(
    geoJsonDocus.map(async (d) => {
      const result = await insertIndexedTripTrajectory(d, lastActivityID);
      return result;
    })
  );
  return `OK on page ${page}`;
};
```

### Pagination Logic
```javascript
let i = 0;
while (i * 50 < numberOfIndexTrajectory + 50) {
  const finalResult = await updateMainProcess(updateList, i, outDate, findLastActivityID(tripArray));
  logger.info(finalResult);
  i++;
}
```

## Activity ID Tracking

### Last Activity ID Detection
```javascript
const findLastActivityID = (tripArray) => {
  let lastActivityID = 0;
  tripArray[0].forEach(t => {
    if(t.activity_id > lastActivityID) {
      lastActivityID = t.activity_id;
    }
  });
  return lastActivityID;
};
```

**Purpose**:
- Tracks processing progress across job executions
- Ensures incremental processing without duplication
- Maintains synchronization with MySQL activity mappings

## Error Handling and Monitoring

### Comprehensive Error Tracking
```javascript
try {
  // Main processing logic
} catch (e) {
  const slack = new SlackManager(slackConfig.token, slackConfig.channelId);
  const slackMessage = {
    project: 'tsp-job',
    stage: process.env.PROJECT_STAGE,
    status: 'ERROR',
    vendor: 'index-trip-trajectory',
    vendorApi: `index-trip-trajectory`,
    originApi: 'tsp-job job : index-trip-trajectory',
    errorMsg: `index-trip-trajectory failed ${nowTime}: ${JSON.stringify(e.message)}`,
    meta: `index-trip-trajectory failed ${nowTime}`
  };
  slack.sendVendorFailedMsg(slackMessage);
  logger.error(`[job.index-trip-trajectory] ${nowTime}: ${e}`);
}
```

### Slack Integration Features
- **Real-time Error Alerting**: Immediate notification of job failures
- **Contextual Information**: Project stage, timestamp, and error details
- **Vendor API Tracking**: Specific service identification for monitoring
- **Error Message Preservation**: Full error context for debugging

## Performance Optimization

### Batch Processing Strategy
- **Page Size**: 50 records per batch to balance memory and performance
- **Sequential Processing**: Prevents MongoDB connection pool exhaustion
- **Progress Tracking**: Page-by-page completion monitoring

### Database Query Optimization
```javascript
.sort({ _id: 1 })
.skip(page * 50)
.limit(50)
.lean();
```
- **Lean Queries**: Reduces memory overhead by skipping Mongoose hydration
- **Sorted Results**: Consistent pagination order
- **Limited Results**: Controlled memory usage

## Data Synchronization

### MySQL-MongoDB Coordination
1. **MySQL Source**: Trip activity mappings provide authoritative activity IDs
2. **MongoDB Processing**: Raw trajectory data transformation
3. **Index Creation**: Optimized GeoJSON format for spatial queries
4. **Progress Tracking**: Activity ID stamps ensure synchronization

### Incremental Processing
- Only processes new activities since last run
- Maintains processing state across job executions
- Prevents duplicate processing and ensures data consistency

## Spatial Data Features

### GeoJSON Standards Compliance
- **LineString Geometry**: Standard format for route visualization
- **Coordinate Order**: [longitude, latitude] per GeoJSON specification
- **Numeric Conversion**: Ensures proper data types for spatial operations

### Indexing Benefits
- **Faster Spatial Queries**: Pre-processed GeoJSON for geographic analysis
- **Reduced Processing Load**: Eliminates real-time trajectory conversion
- **Enhanced Performance**: Optimized format for mapping and analytics

## Schedule Context
Typically scheduled to run regularly (hourly or daily) to:
- Process new trip trajectory data incrementally
- Maintain up-to-date spatial index for analytics
- Support real-time geographic analysis and reporting
- Clean up old data to manage storage requirements

## Integration Points
- **Trip Activity Mapping**: MySQL synchronization for processing state
- **Raw Trajectory Data**: MongoDB source data transformation
- **Spatial Analytics**: Provides optimized data for geographic analysis
- **Monitoring Systems**: Slack integration for operational awareness

## Business Impact
- Enables efficient spatial analysis of transportation patterns
- Supports real-time geographic queries and mapping features
- Optimizes database performance for trajectory-based analytics
- Maintains data retention policies for storage management
- Provides foundation for location-based transportation insights