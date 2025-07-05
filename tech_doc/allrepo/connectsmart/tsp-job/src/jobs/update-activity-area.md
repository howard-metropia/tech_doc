# Update Activity Area Job

## Overview
Job that generates and maintains user activity areas by clustering location data from various sources (trip trajectories, app data, and home locations) using DBSCAN clustering algorithm and convex hull geometry. This creates spatial polygons representing areas where users frequently travel or spend time, supporting location-based analytics and services.

## File Location
`/src/jobs/update-activity-area.js`

## Dependencies
- `@maas/core/log` - Logging framework for operational monitoring
- `moment-timezone` - Date/time manipulation and timezone handling
- `@maas/core/mysql` - MySQL database connection for portal database
- `@app/src/static/defines` - Static configuration definitions
- `@turf/turf` - Geospatial analysis and geometry processing library
- `@app/src/models/ActivityArea` - MongoDB model for user activity areas
- `@app/src/models/TripTrajectoryIndex` - MongoDB model for indexed trajectory data

## Job Configuration

### Inputs
```javascript
inputs: {
  userID: String  // Optional user ID for processing specific user (0 or null for all users)
}
```

### Processing Mode
- **Single User Mode**: Process specific user when userID provided
- **Batch Mode**: Process all users when userID is 0 or not provided

## Data Source Integration

### H-Trip Data (Currently Disabled)
```javascript
const getHTrip = async () => {
  // Currently returns empty array - functionality disabled
  // Previously processed habitual trip origin-destination pairs
  return [];
};
```

**Historical Logic** (commented out):
- Processed cm_activity_location records with trip_count > 2
- Required top_lt1_ceff_prob > 0.5 for confidence threshold
- Grouped by unique origin-destination-user combinations

### Trip Trajectory Data
```javascript
const getTripTrajectory = async (userID) => {
  const sampleFrequence = DEFINES.activityArea.TripTrajectorySampleFrequence;
  const pipeline = [
    {
      $match: userID === 0 ? {} : { user_id: userID }
    },
    {
      $project: {
        user_id: 1,
        coordinates: {
          $filter: {
            input: "$trajectory.coordinates",
            as: "coords",
            cond: {
              $eq: [
                { $mod: [{ $indexOfArray: ["$trajectory.coordinates", "$$coords"] }, sampleFrequence] },
                0
              ]
            }
          }
        }
      }
    }
  ];
  const result = await TripTrajectoryIndex.aggregate(pipeline);
  return result;
};
```

**Sampling Strategy**:
- Uses configurable sample frequency to reduce data density
- Applies modulo operation to select evenly spaced trajectory points
- Optimizes processing performance while maintaining spatial accuracy

### App Data Collection
```javascript
const getAppDataList = async (currentDatetime, userID) => {
  const lastWeekDatetime = moment(currentDatetime)
    .subtract(DEFINES.activityArea.availableAppDateDurationDays, 'days')
    .format('YYYY-MM-DD HH:mm:ss');
  
  const userFilter = userID === 0 ? `` : `and m.user_id = ${userID}`;
  const SQL = `
    SELECT l.user_id, l.lat, l.lon from (
      SELECT m.*, concat(TRUNCATE(m.lat,6),',', TRUNCATE(m.lon,6), ',', m.user_id) as identity 
      FROM hybrid.app_data as m 
      left join auth_user as u on m.user_id = u.id 
      where m.created_on > '${lastWeekDatetime}' and m.lon < 0 ${userFilter}
    ) as l group by l.identity order by l.user_id desc;`;
};
```

**Features**:
- Configurable time window for recent app activity
- Deduplication using truncated coordinates and user ID
- Geographic filtering (longitude < 0 for Western Hemisphere)
- User validation through auth_user join

### Home Location Data
```javascript
const getHomeList = async (userID) => {
  const userFilter = userID === 0 ? `` : `and s.user_id = ${userID}`;
  const SQL = `
    WITH selected_group AS (
      SELECT m.*, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_on DESC) AS rn 
      FROM hybrid.user_favorites AS m where m.category = 1 
    )
    SELECT s.user_id, s.latitude as lat, s.longitude as lon 
    FROM selected_group as s 
    left join auth_user as u on s.user_id = u.id 
    WHERE s.rn = 1 and s.longitude < 0 ${userFilter};`;
};
```

**Home Detection Logic**:
- Category 1 in user_favorites represents home locations
- Uses window function to get most recent home per user
- Geographic validation and user authentication

## Geographic Filtering

### Area Boundary Filter
```javascript
const areaFilter = (point) => {
  if(point[0] > -94.81 || point[0] < -95.81 || point[1] > 30.21 || point[1] < 29.31) {
    return false;
  }
  return true;
};
```

**Geographic Bounds**:
- **Longitude**: -95.81 to -94.81 (Houston metro area)
- **Latitude**: 29.31 to 30.21 (Houston metro area)
- Filters out points outside the target geographic region

## Data Aggregation and Processing

### User Data Consolidation
```javascript
const userSet = new Set();
let userList = {};

// Process each data source and aggregate by user
htripList.forEach(trip => {
  if(userSet.has(Number(trip.user_id))) {
    userList[trip.user_id].locList.push([trip.o_lon, trip.o_lat], [trip.d_lon, trip.d_lat]);
  } else {
    let locList = [[trip.o_lon, trip.o_lat], [trip.d_lon, trip.d_lat]];
    userList[trip.user_id] = { locList };
    userSet.add(Number(trip.user_id));
  }
});
```

### Batch Processing System
```javascript
const splitIntoChunks = (userList, chunkSize) => {
  const result = [];
  let tempSubArray = [];
  let count = 0;
  const keys = Object.keys(userList);
  const lastKey = keys[keys.length - 1];
  
  for(let userID in userList) {
    if(count < chunkSize) {
      tempSubArray.push({
        user_id: userID,
        locList: userList[userID].locList
      });
      // Handle last key logic
      count = count + 1;
    } else {
      result.push(Array.from(tempSubArray));
      tempSubArray = [];
      count = 0;
      // Continue processing
    }
  }
  return result;
};
```

## Clustering Algorithm Implementation

### DBSCAN Clustering
```javascript
const clusteredResult = turf.clustersDbscan(
  turf.points(user.locList), 
  DEFINES.activityArea.clusterDistance, 
  {minPoints: DEFINES.activityArea.clusterMinPoints}
);
```

**Configuration Parameters**:
- `clusterDistance`: Maximum distance between points in same cluster
- `clusterMinPoints`: Minimum points required to form a cluster
- Uses Turf.js implementation of DBSCAN algorithm

### Cluster Processing
```javascript
const features = {};
const cSet = new Set();

clusteredResult.features.forEach((f, index) => {
  if(f.properties.dbscan !== 'noise') {
    if(cSet.has(f.properties.cluster)) {
      let tempArray = Array.from(features[f.properties.cluster].coordinates);
      tempArray.push(f.geometry.coordinates);
      features[f.properties.cluster].coordinates = tempArray;
    } else {
      features[f.properties.cluster] = {
        type: 'Points',
        coordinates: [f.geometry.coordinates]
      };
      cSet.add(f.properties.cluster);
    }
  } else {
    features[`n${index}`] = {
      type: 'Point',
      coordinates: f.geometry.coordinates
    };
  }
});
```

## Geometry Generation

### Convex Hull Creation
```javascript
const resultMultiPolygon = [];
for (let key in features) {
  if(features[key].type === 'Points') {
    const points = turf.points(features[key].coordinates);
    const hullPolygon = turf.convex(points, {concavity: DEFINES.activityArea.convexConcavity});
    if(hullPolygon?.geometry?.coordinates) {
      resultMultiPolygon.push(hullPolygon.geometry.coordinates);
    }
  }
}
```

**Geometry Processing**:
- Creates convex hull polygons around clustered points
- Uses configurable concavity parameter for hull generation
- Handles clusters with sufficient points for polygon creation
- Filters noise points (excluded from polygon generation)

### MultiPolygon Structure
```javascript
if(resultMultiPolygon.length > 0) {
  await ActivityArea.updateOne(
    { user_id: user.user_id },
    {
      user_id: user.user_id,
      geometry: {
        type: 'MultiPolygon',
        coordinates: resultMultiPolygon
      },
      updated_at: nowDate
    },
    { upsert: true }
  );
}
```

## Configuration Management

### Activity Area Defines
Referenced from `DEFINES.activityArea`:
- `TripTrajectorySampleFrequence`: Trajectory point sampling rate
- `availableAppDateDurationDays`: Time window for app data
- `clusterDistance`: DBSCAN clustering distance parameter
- `clusterMinPoints`: DBSCAN minimum points parameter
- `convexConcavity`: Convex hull concavity setting

## Performance Optimization

### Chunked Processing
```javascript
const userChunkedArray = splitIntoChunks(userList, 50);
logger.info(`[update-activity-area] user chunk count: ${userChunkedArray.length}`);

for (let index in userChunkedArray) {
  await Promise.all(
    userChunkedArray[index].map(async (user) => {
      // Process each user in parallel within chunk
    })
  );
  logger.info(`[update-activity-area] chunk No.${index} Done`);
}
```

**Benefits**:
- Parallel processing within chunks
- Memory management through batching
- Progress tracking per chunk
- Prevents database connection exhaustion

### Memory Management
- Processes users in batches of 50
- Uses lean queries where possible
- Cleans up intermediate data structures
- Manages large datasets efficiently

## Data Quality and Validation

### Geographic Validation
- Filters coordinates outside target region
- Validates longitude < 0 for Western Hemisphere
- Ensures proper coordinate format and numeric types

### Cluster Validation
- Requires minimum points for cluster formation
- Excludes noise points from polygon generation
- Validates polygon geometry before storage

## Error Handling and Logging

### Comprehensive Logging
```javascript
logger.error(`[update-activity-area] htrip loc count: ${htripList.length}`);
logger.error(`[update-activity-area] trip trajectory count: ${tripTrajectoryList.length}`);
logger.error(`[update-activity-area] appData loc count: ${appDataList.length}`);
logger.error(`[update-activity-area] home loc count: ${homeList.length}`);
```

### Error Management
```javascript
try {
  // Main processing logic
} catch (e) {
  logger.error(`[update-activity-area] error: ${e.message}`);
  logger.info(`[update-activity-area] stack: ${e.stack}`);
}
```

## Integration Points

### Data Sources
- **Trip Trajectories**: Movement patterns and routes
- **App Data**: Location pings and user activity
- **Home Locations**: User-defined residence information
- **H-Trip Data**: Historical habitual trip patterns (disabled)

### Output Storage
- **MongoDB ActivityArea Collection**: Stores user activity polygons
- **GeoJSON Format**: Standard spatial data format
- **Upsert Operations**: Updates existing or creates new records

## Schedule Context
Typically scheduled to run periodically (daily or weekly) to:
- Update user activity areas based on recent location data
- Support location-based services and analytics
- Maintain current activity patterns for user profiling
- Enable geographic analysis and personalization features

## Business Impact
- Enables personalized location-based services
- Supports user behavior analysis and insights
- Provides foundation for geographic targeting
- Enhances user experience through location awareness
- Supports transportation planning and analytics
- Enables efficient spatial queries for user activity patterns