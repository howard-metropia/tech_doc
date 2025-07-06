# TSP Job: Recalculate Instant Carpool

## Quick Summary

The `recalculate-instant-carpool.js` job is a sophisticated trajectory verification system for instant carpool trips that ensures driver and passenger ride-sharing compliance. It recalculates and validates carpool trips from the past 72 hours (or a specified date) by analyzing GPS trajectory data to verify that drivers and passengers actually traveled together. The job processes trips where initial trajectory scores fell below the threshold, updates trip records, awards incentives for verified trips, and manages enterprise telework logging for commute tracking.

## Technical Analysis

### Core Algorithm

The job implements a complex trajectory matching algorithm that:

1. **Time-based Grouping**: Divides GPS trajectories into 5-second intervals
2. **Distance Calculation**: Uses Haversine formula to calculate distances between coordinates
3. **Proximity Validation**: Checks if driver and rider coordinates are within 100 meters
4. **Speed Verification**: Ensures both parties have speed > 0 (indicating movement)
5. **Score Calculation**: Requires minimum 36 matching trajectory points (configurable threshold)

### Key Components

```javascript
// Distance calculation using Haversine formula
const calcDistance = (lat1, lng1, lat2, lng2) => {
  const EARTH_RADIUS = 6378.137;
  const radLat1 = (lat1 * Math.PI) / 180.0;
  const radLat2 = (lat2 * Math.PI) / 180.0;
  const radLng1 = (lng1 * Math.PI) / 180.0;
  const radLng2 = (lng2 * Math.PI) / 180.0;
  const a = radLat1 - radLat2;
  const b = radLng1 - radLng2;
  let s = 2 * Math.asin(
    Math.sqrt(
      Math.pow(Math.sin(a / 2), 2) +
      Math.cos(radLat1) * Math.cos(radLat2) * Math.pow(Math.sin(b / 2), 2)
    )
  );
  s = s * EARTH_RADIUS * 1000; // Convert to meters
  return s;
};
```

### Trajectory Matching Logic

```javascript
const verifyTrajectoryMatch = async ({ driver, riders, startTimestamp, endTimestamp }) => {
  // Fetch driver trajectories grouped by 5-second intervals
  const driverTrajectories = await fetchTrajectories(
    driver.userId, driver.tripId, startTimestamp, endTimestamp
  );
  
  let isDriverPassed = false;
  
  await Promise.all(riders.map(async (rider) => {
    const riderTrajectories = await fetchTrajectories(
      rider.userId, rider.tripId, startTimestamp, endTimestamp
    );
    
    // Compare each time group
    const matchResult = driverTrajectories.map((driverTrajectory, index) => {
      return driverTrajectory && driverTrajectory.some((driver) => {
        return riderTrajectories[index] && riderTrajectories[index].some((rider) => {
          const distance = calcDistance(
            driver.latitude, driver.longitude,
            rider.latitude, rider.longitude
          );
          const haveSpeed = rider.speed > 0 && driver.speed > 0;
          return distance < 100 && haveSpeed;
        });
      });
    });
    
    const score = matchResult.filter(el => el).length;
    rider.trajectoryScore = score;
    
    if (score >= TRAJECTORY_PASSED_SCORE) {
      isDriverPassed = true;
    }
  }));
  
  return isDriverPassed;
};
```

## Usage/Integration

### Job Configuration

The job accepts an optional `assignDate` parameter:

```javascript
module.exports = {
  inputs: {
    assignDate: String, // Optional: specific date to start recalculation
  },
  fn: async (assignDate) => {
    // If no date provided, processes last 72 hours
    const startDate = isValidDate
      ? moment.utc(assignDate).toISOString()
      : moment.utc().subtract(config.reCalculateRange, 'h').toISOString();
  }
};
```

### Processing Flow

1. **Trip Selection**: Queries MongoDB for trips with driver status 'finished' and trajectory scores below threshold
2. **End Trip Data Sync**: Updates MySQL trip records and MongoDB trip_records with destination and distance data
3. **Trajectory Verification**: Performs detailed GPS trajectory matching between driver and riders
4. **Telework Logging**: Creates telework records for verified enterprise commutes
5. **Incentive Processing**: Triggers incentive engine for validated trips
6. **Event Publishing**: Sends carpooling completion events for analytics

### Enterprise Integration

The job includes sophisticated workplace detection:

```javascript
const verifyODIsWorkPlace = async (userId, origin, destination) => {
  const workPosition = await UserFavorites.query()
    .where({ user_id: userId, category: 2 }) // category 2 = work
    .first();
    
  if (workPosition) {
    const distanceWithOrig = calcDistance(
      workPosition.longitude, workPosition.latitude,
      origin.longitude, origin.latitude
    );
    const distanceWithDest = calcDistance(
      workPosition.longitude, workPosition.latitude,
      destination.longitude, destination.latitude
    );
    // Within 100m of work location
    if (distanceWithOrig < 100 || distanceWithDest < 100) 
      return true;
  }
  return false;
};
```

## Dependencies

### External Services
- **MongoDB**: TripTrajectory, InstantCarpoolings, TripRecords collections
- **MySQL**: Portal database for trips, telework, enterprises, user_favorites
- **Incentive Engine**: makeTripProcess for reward calculations
- **Event System**: sendEvent for carpooling analytics

### NPM Packages
- `moment-timezone`: Time zone aware date handling
- `geo-tz`: Geographic timezone detection
- `@maas/core/mysql`: Database connection management
- `@maas/core/log`: Centralized logging

### Configuration
```javascript
const config = require('config').instantCarpool;
// Expected config structure:
{
  trajectoryThreshold: 36,        // Minimum matching points
  reCalculateRange: 72            // Hours to look back
}
```

## Code Examples

### Manual Recalculation Trigger

```javascript
// Recalculate trips from specific date
await recalculateInstantCarpool.fn('2023-05-01');

// Recalculate last 72 hours
await recalculateInstantCarpool.fn('false');
```

### Telework Record Creation

```javascript
const insertPassedTrip = async ({ origin, destination, userInfo, role, timeZone }) => {
  const travelMode = role === ROLE.DRIVER 
    ? 'instant_carpool_driver' 
    : 'instant_carpool_rider';
    
  const teleworkData = {
    user_id: userInfo.userId,
    enterprise_id: enterpriseId,
    trip_date: tripDate,
    trip_id: userInfo.tripId,
    is_autolog: 1,
    is_active: 1,
    started_on: startOn,
    ended_on: endedOn
  };
  
  const telework = await Teleworks.query().insert(teleworkData);
  
  const teleworkLogData = {
    telework_id: telework.id,
    travel_mode: travelMode,
    origin_name: origin.name,
    destination_name: destination.name,
    mile: userInfo.distance,
    distance: userInfo.distance
  };
  
  await TeleworkLogs.query().insert(teleworkLogData);
};
```

### Event Publishing Example

```javascript
carpoolingEvent.push({
  userIds: [trip.driver.userId],
  eventName: 'carpooling',
  eventMeta: {
    action: 'finish_instant_carpool',
    trip_id: trip.driver.tripId,
    role: 'driver'
  }
});

await sendEvent(carpoolingEvent);
```

This job is critical for maintaining the integrity of the instant carpool system, ensuring that only legitimate shared rides receive incentives and enterprise commute credits. The sophisticated trajectory matching algorithm provides robust verification while accounting for GPS inaccuracies and temporary signal loss.