# IncentiveEngine Service

## Quick Summary

The IncentiveEngine service is a comprehensive trip incentive processing system that validates, calculates, and distributes reward points to users based on their travel behavior. This service handles the core business logic for ConnectSmart's gamification system, processing trip data to determine eligible rewards while enforcing various validation rules and limits.

**Key Features:**
- Automated trip validation and reward calculation
- Geographic service area verification using geospatial analysis
- Weekly point limits and anti-fraud protection
- Multi-mode transportation support
- Real-time notification delivery
- Comprehensive logging and error handling

## Technical Analysis

### Architecture Overview

The service is built around a main processing function `makeTripProcess` that orchestrates a complex validation and reward pipeline. The system integrates with multiple data sources including MySQL databases, MongoDB collections, and external notification services.

### Core Components

#### 1. Trip Validation Engine
```javascript
async function makeTripProcess({ userId, tripId, travelMode, mti, distance }) {
  // Multi-layer validation:
  // - Internal user filtering
  // - Market user validation  
  // - Trip data integrity checks
  // - Geographic boundary verification
  // - Distance requirements
  // - Duplicate reward prevention
}
```

#### 2. Geospatial Service Area Verification
```javascript
async function checkTripInServiceArea(serviceProfile, userId, tripId, mti) {
  const geoJson = parse(serviceProfile.polygon);
  let polygon = turf.polygon(geoJson.coordinates);
  return await checkServiceArea(tripId, mti, polygon);
}
```

#### 3. Weekly Bonus Tracking
```javascript
async function userTripsWeekBonus(userId) {
  const today = moment();
  const startDate = today.startOf('week');
  const endDate = startDate.clone().endOf('week');
  // Calculates user's accumulated points for current week
}
```

### Data Flow Architecture

1. **Input Processing**: Receives trip completion events with user ID, trip ID, travel mode, and location data
2. **Validation Pipeline**: Multi-stage validation including user eligibility, trip authenticity, and geographic constraints
3. **Reward Calculation**: Dynamic point calculation based on travel mode, trip characteristics, and user history
4. **Notification System**: Automated push notification delivery with personalized messaging
5. **Database Operations**: Transactional updates to multiple tables ensuring data consistency

### Validation Rules Implementation

The service implements comprehensive validation rules:

```javascript
// Distance validation
if (distance < Number(modeRule.distance ?? 1) * 1609) {
  await sendZeroPointsNotification(
    userId,
    incentiveEventType.INCENTIVE_TRIP_LESS_THAN_1_MILE,
    now,
    Number(modeRule.distance ?? 1)
  );
  return;
}

// Weekly limit enforcement
const weeklyLimit = rule.L ?? INCENTIVE_POINTS_LIMIT_PER_WEEK;
if (utils.pointSum(point, pointsCurrentWeek) > weeklyLimit) {
  await sendZeroPointsNotification(
    userId,
    incentiveEventType.INCENTIVE_REACH_THE_WEEKLY_CAP,
    now
  );
  return;
}
```

### Geographic Analysis Engine

The service uses Turf.js for sophisticated geospatial operations:

```javascript
// Point-in-polygon checks for trip endpoints
let startPointInServiceArea = turf.booleanPointInPolygon(startPoint, polygon);
let endPointInServiceArea = turf.booleanPointInPolygon(endPoint, polygon);

// Trajectory sampling for route verification
let traceInServiceArea = select(trace, 20).some((point) => {
  const result = turf.booleanPointInPolygon(turf.point(point), polygon);
  return result;
});
```

## Usage/Integration

### Primary Integration Points

#### 1. Trip Completion Events
```javascript
// Called when a trip is completed and validated
await makeTripProcess({
  userId: 12345,
  tripId: 67890,
  travelMode: 'transit',
  mti: {
    origin_latitude: 29.7604,
    origin_longitude: -95.3698,
    destination_latitude: 29.7749,
    destination_longitude: -95.4194,
    started_on: '2023-12-01T08:00:00Z'
  },
  distance: 5000 // meters
});
```

#### 2. Service Area Validation
```javascript
// Verify trip falls within service boundaries
const serviceProfile = getServiceProfile('connectsmart');
const isInArea = await checkTripInServiceArea(
  serviceProfile, 
  userId, 
  tripId, 
  mti
);
```

#### 3. Weekly Bonus Queries
```javascript
// Get user's current week accumulated points
const weeklyPoints = await userTripsWeekBonus(userId);
```

### Configuration Requirements

The service requires several configuration parameters:

- **Incentive Rules**: Database-stored rules per market defining point values and limits
- **Service Profiles**: Geographic polygons defining service areas
- **Distance Thresholds**: Minimum trip distances per transportation mode
- **Weekly Limits**: Maximum points earnable per week per user
- **Notification Templates**: Customizable message templates for different event types

### Error Handling Strategy

The service implements comprehensive error handling with graceful degradation:

```javascript
try {
  // Core processing logic
} catch (e) {
  logger.warn(`[${userId}:${tripId}] Error description`, e);
  await sendZeroPointsNotification(
    userId,
    incentiveEventType.INCENTIVE_TRIP_INVALID_TRIP,
    now
  );
  return;
}
```

## Dependencies

### Core Framework Dependencies
- **@maas/core/log**: Centralized logging system for debugging and monitoring
- **@maas/core/mysql**: Database connection pooling and query management
- **@app/src/services/queue**: Asynchronous task queue for notifications
- **@app/src/services/wallet**: Points transaction and balance management

### Geospatial Libraries
- **@turf/turf**: Advanced geospatial analysis and geometric operations
- **wkt**: Well-Known Text format parsing for geographic data

### Utility Dependencies
- **moment-timezone**: Date/time manipulation with timezone support
- **@app/src/services/utils**: Common utility functions and formatters

### Data Models
- **TripIncentiveRules**: MongoDB model for dynamic incentive rule management
- **InternalUserTag**: User filtering and administrative controls
- **TripTrajectory**: MongoDB collection storing GPS trajectory data

### External Services
- **SQS/Queue System**: Asynchronous notification delivery
- **MySQL Portal Database**: Primary data storage for trips and users
- **MongoDB**: High-performance storage for trajectory and rule data

## Code Examples

### Complete Trip Processing Workflow

```javascript
// Main incentive processing workflow
async function processCompletedTrip(tripData) {
  const { userId, tripId, travelMode } = tripData;
  
  // 1. Prepare trip incentive data
  const mti = await incentiveTripData(
    tripData, 
    tripData.destination_latitude,
    tripData.destination_longitude
  );
  
  // 2. Process incentive with full validation
  await makeTripProcess({
    userId,
    tripId, 
    travelMode,
    mti,
    distance: tripData.distance
  });
  
  console.log(`Incentive processing completed for trip ${tripId}`);
}
```

### Custom Notification System

```javascript
// Zero-points notification with dynamic messaging
async function sendZeroPointsNotification(userId, eventType, now, distance = 1) {
  const title = incentiveNotificationTitle[eventType];
  let body = '';
  
  if (eventType === incentiveEventType.INCENTIVE_TRIP_LESS_THAN_1_MILE) {
    const distWording = distance === 1 ? 
      `${distance} mile` : `${distance} miles`;
    body = incentiveNotificationBody[eventType].format(distWording);
  } else {
    body = incentiveNotificationBody[eventType];
  }
  
  const meta = { event_type: eventType };
  const endedOn = new Date(new Date().getTime() + 7 * 24 * 60 * 60 * 1000);
  
  await sendTask('cloud_message', {
    silent: false,
    user_list: [userId],
    notification_type: INCENTIVE_NOTIFICATION_TYPE,
    ended_on: utils.d2dbs(endedOn),
    title,
    body,
    meta
  });
}
```

### Geographic Validation Implementation

```javascript
// Advanced trajectory analysis for service area verification
async function analyzeUserTrajectory(tripId, servicePolygon) {
  // Retrieve full trajectory from MongoDB
  const trajectories = await TripTrajectory.find({ trip_id: tripId });
  
  // Process and sort trajectory points
  const trace = trajectories
    .reduce((prev, curr) => prev.concat(curr.trajectory), [])
    .sort((a, b) => a.timestamp - b.timestamp)
    .map((point) => [point.longitude, point.latitude]);
  
  // Sample trajectory points for efficiency
  const sampledPoints = selectSamplePoints(trace, 20);
  
  // Check if any sampled point falls within service area
  return sampledPoints.some((point) => {
    return turf.booleanPointInPolygon(turf.point(point), servicePolygon);
  });
}

function selectSamplePoints(trajectory, sampleSize) {
  const factor = Math.ceil(trajectory.length / sampleSize);
  const result = [];
  for (let i = 0; i < trajectory.length; i++) {
    if ((i % factor) === 0) {
      result.push(trajectory[i]);
    }
  }
  return result;
}
```

### Reward Point Calculation System

```javascript
// Dynamic point calculation with first-time user bonuses
async function calculateIncentiveReward(userId, rule, modeRule) {
  const isFirstTime = (await knex('incentive_notify_queue')
    .where({
      user_id: userId,
      msg_key: 'Incentive1_2_make_trip'
    })
    .select('id')).length === 0;
  
  const basePoints = await incentiveHelper.getIncentiveRewardPoint(
    isFirstTime,
    rule,
    modeRule
  );
  
  return {
    points: basePoints,
    isFirstTime,
    eventType: isFirstTime ? 
      incentiveEventType.INCENTIVE_FIRST_TRIP : 
      incentiveEventType.INCENTIVE_NON_FIRST_TRIP
  };
}
```

This incentive engine represents a sophisticated gamification system that balances user engagement with fraud prevention, geographic constraints, and business rules, making it a critical component of the ConnectSmart mobility platform.