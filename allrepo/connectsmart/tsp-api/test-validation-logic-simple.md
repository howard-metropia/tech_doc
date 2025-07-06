# TSP API Test Suite - Simple Validation Logic Tests

## Overview
The `test-validation-logic-simple.js` file contains streamlined tests for basic trip validation functionality, focusing on core validation logic with simplified test scenarios and straightforward validation criteria.

## File Location
`/allrepo/connectsmart/tsp-api/test/test-validation-logic-simple.js`

## Dependencies
- **chai**: Testing assertions and expectations
- **sinon**: Test doubles, mocking, and stubbing
- **moment-timezone**: Date/time manipulation
- **validationLogic**: Core validation service

## Test Architecture

### Core Service Integration
```javascript
const validationLogic = require('../src/services/validationLogic');
const DEFINE = require('@app/src/static/defines');
const TRAVEL_MODE = DEFINE.travelMode;
```

### Travel Mode Support
```javascript
const TRAVEL_MODE = {
  WALKING: 3,
  DRIVING: 1,
  BIKING: 4,
  PUBLIC_TRANSIT: 2,
  INTERMODAL: 5,
  TRUCKING: 6,
  PARK_AND_RIDE: 7,
  DUO: 100,
  INSTANT_CARPOOL: 101
}
```

## Test Data Generation

### Simple Trip Factory
```javascript
function createTrip(overrides = {}) {
  return {
    id: 12345,
    travel_mode: TRAVEL_MODE.WALKING,
    started_on: '2023-01-01T10:00:00Z',
    estimated_arrival_on: '2023-01-01T10:30:00Z',
    ended_on: '2023-01-01T10:25:00Z',
    origin_latitude: 25.042695,
    origin_longitude: 121.534590,
    destination_latitude: 25.052695,
    destination_longitude: 121.544590,
    ...overrides
  };
}
```

### Simplified Trajectory Generator
```javascript
function createTrajectoryData(numPoints = 5, speedKmh = 5) {
  const points = [];
  const startTime = new Date('2023-01-01T10:00:00Z');
  
  // Initial coordinates (Taipei area)
  const startLat = 25.042695;
  const startLon = 121.534590;
  
  // Calculate coordinate changes based on speed
  const latChangePerMin = 0.0001 * speedKmh / 5;
  const lonChangePerMin = 0.0001 * speedKmh / 5;

  for (let i = 0; i < numPoints; i++) {
    const minutesFromStart = i * 5; // Point every 5 minutes
    const pointTime = new Date(startTime.getTime() + minutesFromStart * 60000);

    points.push({
      latitude: startLat + latChangePerMin * minutesFromStart,
      longitude: startLon + lonChangePerMin * minutesFromStart,
      timestamp: pointTime.toISOString(),
      speed: speedKmh,
      accuracy: 5
    });
  }

  return points;
}
```

### Route Data Factory
```javascript
function createRouteData(trajectory) {
  if (!trajectory) {
    trajectory = createTrajectoryData();
  }

  return {
    route: JSON.stringify(
      trajectory.map(p => ([p.longitude, p.latitude]))
    ),
    distance: calculateSimpleDistance(trajectory),
    waypoints: trajectory.length
  };
}
```

## Core Validation Tests

### 1. Basic Validation Function Tests
```javascript
describe('validateTrip函數', () => {
  it('應該根據行程類型選擇適當的驗證邏輯', async () => {
    const trip = createTrip();
    const trajectoryData = createTrajectoryData();
    const routeData = createRouteData(trajectoryData);

    const result = await validationLogic.validateTrip(trip.id, trip, trajectoryData, routeData);

    // Validate basic result structure
    expect(result).to.have.property('passed');
    expect(result).to.have.property('score');
    expect(result).to.have.property('details');
    expect(result.details).to.have.property('dimensions');
  });

  it('應該處理不支援的行程類型', async () => {
    const trip = createTrip({ travel_mode: 999 });
    const trajectoryData = createTrajectoryData();
    const routeData = createRouteData();

    const result = await validationLogic.validateTrip(trip.id, trip, trajectoryData, routeData);

    expect(result.passed).to.be.false;
    expect(result.score).to.equal(0);
    expect(result.details.message).to.include('No validation logic defined');
  });
});
```

### 2. Walking Mode Validation
```javascript
describe('步行驗證', () => {
  it('應該驗證正常步行速度', async () => {
    const trip = createTrip({
      travel_mode: TRAVEL_MODE.WALKING
    });
    const trajectoryData = createTrajectoryData(6, 4); // 6 points, 4 km/h
    const routeData = createRouteData(trajectoryData);

    const result = await validationLogic.validateTrip(trip.id, trip, trajectoryData, routeData);

    expect(result.passed).to.be.true;
    expect(result.score).to.be.greaterThan(0.5);
    expect(result.details.dimensions.speed.passed).to.be.true;
  });

  it('應該拒絕不合理的步行速度', async () => {
    const trip = createTrip({
      travel_mode: TRAVEL_MODE.WALKING
    });
    const trajectoryData = createTrajectoryData(5, 20); // Too fast for walking
    const routeData = createRouteData(trajectoryData);

    const result = await validationLogic.validateTrip(trip.id, trip, trajectoryData, routeData);

    expect(result.passed).to.be.false;
    expect(result.details.dimensions.speed.passed).to.be.false;
  });
});
```

### 3. Driving Mode Validation
```javascript
describe('駕駛驗證', () => {
  it('應該驗證正常駕駛行程', async () => {
    const trip = createTrip({
      travel_mode: TRAVEL_MODE.DRIVING
    });
    const trajectoryData = createTrajectoryData(8, 40); // 8 points, 40 km/h
    const routeData = createRouteData(trajectoryData);

    const result = await validationLogic.validateTrip(trip.id, trip, trajectoryData, routeData);

    expect(result.passed).to.be.true;
    expect(result.score).to.be.greaterThan(0.6);
    expect(result.details.dimensions.speed.averageSpeed).to.be.approximately(40, 5);
  });

  it('應該處理停車等待時間', async () => {
    const trip = createTrip({
      travel_mode: TRAVEL_MODE.DRIVING,
      estimated_arrival_on: '2023-01-01T10:45:00Z',
      ended_on: '2023-01-01T10:50:00Z' // 5 minutes late
    });
    const trajectoryData = createTrajectoryData(10, 25); // Lower speed due to traffic
    const routeData = createRouteData(trajectoryData);

    const result = await validationLogic.validateTrip(trip.id, trip, trajectoryData, routeData);

    expect(result.passed).to.be.true;
    expect(result.details.dimensions.time.delay).to.be.greaterThan(0);
  });
});
```

### 4. Biking Mode Validation
```javascript
describe('騎行驗證', () => {
  it('應該驗證標準騎行速度', async () => {
    const trip = createTrip({
      travel_mode: TRAVEL_MODE.BIKING
    });
    const trajectoryData = createTrajectoryData(7, 15); // 7 points, 15 km/h
    const routeData = createRouteData(trajectoryData);

    const result = await validationLogic.validateTrip(trip.id, trip, trajectoryData, routeData);

    expect(result.passed).to.be.true;
    expect(result.score).to.be.greaterThan(0.7);
    expect(result.details.dimensions.speed.passed).to.be.true;
  });
});
```

## Simple Validation Dimensions

### 1. Speed Validation
```javascript
const validateSimpleSpeed = (trajectory, travelMode) => {
  const speeds = trajectory.map(point => point.speed);
  const avgSpeed = speeds.reduce((a, b) => a + b, 0) / speeds.length;
  
  const speedRanges = {
    [TRAVEL_MODE.WALKING]: { min: 1, max: 8 },
    [TRAVEL_MODE.BIKING]: { min: 8, max: 30 },
    [TRAVEL_MODE.DRIVING]: { min: 15, max: 100 },
    [TRAVEL_MODE.PUBLIC_TRANSIT]: { min: 10, max: 60 }
  };
  
  const range = speedRanges[travelMode] || { min: 0, max: 200 };
  
  return {
    passed: avgSpeed >= range.min && avgSpeed <= range.max,
    averageSpeed: avgSpeed,
    expectedRange: range,
    score: calculateSimpleSpeedScore(avgSpeed, range)
  };
};
```

### 2. Distance Validation
```javascript
const validateSimpleDistance = (trajectory, trip) => {
  const trajectoryDistance = calculateTrajectoryDistance(trajectory);
  const straightLineDistance = calculateStraightLineDistance(
    trip.origin_latitude, trip.origin_longitude,
    trip.destination_latitude, trip.destination_longitude
  );
  
  const ratio = trajectoryDistance / straightLineDistance;
  
  return {
    passed: ratio >= 1.0 && ratio <= 3.0, // Reasonable detour range
    trajectoryDistance,
    straightLineDistance,
    ratio,
    score: calculateDistanceScore(ratio)
  };
};
```

### 3. Time Validation
```javascript
const validateSimpleTime = (trip, trajectory) => {
  const plannedDuration = new Date(trip.estimated_arrival_on) - new Date(trip.started_on);
  const actualDuration = new Date(trip.ended_on) - new Date(trip.started_on);
  
  const timeDifference = Math.abs(actualDuration - plannedDuration);
  const tolerance = plannedDuration * 0.3; // 30% tolerance
  
  return {
    passed: timeDifference <= tolerance,
    plannedDuration: plannedDuration / 1000, // seconds
    actualDuration: actualDuration / 1000,
    difference: timeDifference / 1000,
    tolerance: tolerance / 1000,
    score: calculateTimeScore(timeDifference, tolerance)
  };
};
```

## Utility Functions

### Distance Calculation
```javascript
const calculateSimpleDistance = (trajectory) => {
  let totalDistance = 0;
  
  for (let i = 1; i < trajectory.length; i++) {
    const prev = trajectory[i-1];
    const curr = trajectory[i];
    
    const distance = haversineDistance(
      prev.latitude, prev.longitude,
      curr.latitude, curr.longitude
    );
    
    totalDistance += distance;
  }
  
  return totalDistance;
};

const haversineDistance = (lat1, lon1, lat2, lon2) => {
  const R = 6371; // Earth's radius in kilometers
  const dLat = toRadians(lat2 - lat1);
  const dLon = toRadians(lon2 - lon1);
  
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(toRadians(lat1)) * Math.cos(toRadians(lat2)) *
    Math.sin(dLon/2) * Math.sin(dLon/2);
  
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c * 1000; // Return in meters
};
```

### Score Calculation
```javascript
const calculateSimpleSpeedScore = (avgSpeed, range) => {
  if (avgSpeed < range.min || avgSpeed > range.max) {
    return 0;
  }
  
  const optimal = (range.min + range.max) / 2;
  const deviation = Math.abs(avgSpeed - optimal);
  const maxDeviation = (range.max - range.min) / 2;
  
  return Math.max(0, 1 - (deviation / maxDeviation));
};

const calculateDistanceScore = (ratio) => {
  if (ratio < 1.0 || ratio > 3.0) {
    return 0;
  }
  
  // Optimal ratio is around 1.2 (20% detour)
  const optimal = 1.2;
  const deviation = Math.abs(ratio - optimal);
  const maxDeviation = 1.8; // 3.0 - 1.2
  
  return Math.max(0, 1 - (deviation / maxDeviation));
};
```

## Test Coverage

### Happy Path Scenarios
- Standard walking trips with normal speeds
- Typical driving trips with reasonable timing
- Regular biking trips with appropriate speeds
- Basic public transit usage

### Edge Cases
- Minimum and maximum acceptable speeds
- Very short and very long trips
- Timing variations and delays
- GPS accuracy variations

### Error Conditions
- Invalid travel modes
- Missing trajectory data
- Corrupted GPS coordinates
- Impossible speed values

## Quality Assurance

### Test Validation
```javascript
describe('測試資料品質', () => {
  it('應該生成有效的測試資料', () => {
    const trip = createTrip();
    const trajectory = createTrajectoryData();
    const routeData = createRouteData(trajectory);
    
    expect(trip.id).to.be.a('number');
    expect(trajectory).to.be.an('array');
    expect(trajectory.length).to.be.greaterThan(0);
    expect(routeData.route).to.be.a('string');
  });
});
```

### Performance Testing
```javascript
describe('性能測試', () => {
  it('應該快速處理簡單驗證', async () => {
    const trip = createTrip();
    const trajectory = createTrajectoryData(100); // Larger dataset
    const routeData = createRouteData(trajectory);
    
    const startTime = Date.now();
    const result = await validationLogic.validateTrip(trip.id, trip, trajectory, routeData);
    const endTime = Date.now();
    
    expect(endTime - startTime).to.be.lessThan(1000); // Under 1 second
    expect(result).to.have.property('passed');
  });
});
```

This simple validation test suite provides streamlined testing for basic trip validation functionality, focusing on essential validation criteria while maintaining good test coverage and performance.