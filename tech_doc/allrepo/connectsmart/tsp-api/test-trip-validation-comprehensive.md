# TSP API Test Suite - Comprehensive Trip Validation Tests

## Overview
The `test-validation-logic-comprehensive.js` file contains extensive tests for the complete trip validation system, covering all transportation modes with sophisticated validation algorithms and comprehensive edge case handling.

## File Location
`/allrepo/connectsmart/tsp-api/test/test-validation-logic-comprehensive.js`

## Dependencies
- **chai**: Testing assertions and expectations
- **sinon**: Test doubles, mocking, and stubbing
- **moment-timezone**: Date/time manipulation and timezone handling

## Test Architecture

### Core Service Integration
```javascript
const validationLogic = require('../src/services/validationLogic');
const DEFINE = require('../src/static/defines');
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

## Test Data Generation Framework

### Trip Creation Factory
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

### Trajectory Data Factory
```javascript
function createTrajectoryData(options = {}) {
  const {
    numPoints = 6,
    speedKmh = 5,
    speedVariation = 0,
    startTime = '2023-01-01T10:00:00Z',
    endTime = '2023-01-01T10:25:00Z',
    routeDeviation = 0,
    irregularTimeGaps = false
  } = options;

  // Generate realistic trajectory points
  const points = [];
  const startTimeObj = new Date(startTime);
  const endTimeObj = new Date(endTime);
  const totalDurationMs = endTimeObj - startTimeObj;

  for (let i = 0; i < numPoints; i++) {
    const progress = i / (numPoints - 1);
    const pointTimeObj = new Date(startTimeObj.getTime() + progress * totalDurationMs);
    
    points.push({
      latitude: 25.042695 + progress * 0.01 + generateDeviation(routeDeviation),
      longitude: 121.534590 + progress * 0.01 + generateDeviation(routeDeviation),
      timestamp: pointTimeObj.toISOString(),
      speed: speedKmh + (Math.random() * 2 - 1) * speedVariation
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
    distance: calculateRouteDistance(trajectory),
    duration: calculateRouteDuration(trajectory)
  };
}
```

## Comprehensive Validation Test Suite

### 1. Core Validation Function Tests
```javascript
describe('validateTrip函數', () => {
  it('應該根據行程類型選擇適當的驗證邏輯', async () => {
    const trip = createTrip();
    const trajectoryData = createTrajectoryData();
    const routeData = createRouteData(trajectoryData);

    const result = await validationLogic.validateTrip(trip.id, trip, trajectoryData, routeData);

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
describe('步行模式驗證', () => {
  it('應該驗證正常的步行行程', async () => {
    const trip = createTrip({
      travel_mode: TRAVEL_MODE.WALKING
    });
    const trajectoryData = createTrajectoryData({
      speedKmh: 4,
      numPoints: 8
    });
    const routeData = createRouteData(trajectoryData);

    const result = await validationLogic.validateTrip(trip.id, trip, trajectoryData, routeData);

    expect(result.passed).to.be.true;
    expect(result.score).to.be.greaterThan(0.7);
    expect(result.details.dimensions).to.include.keys(['speed', 'route', 'time']);
  });

  it('應該拒絕速度過快的步行行程', async () => {
    const trip = createTrip({
      travel_mode: TRAVEL_MODE.WALKING
    });
    const trajectoryData = createTrajectoryData({
      speedKmh: 25, // Too fast for walking
      numPoints: 6
    });
    const routeData = createRouteData(trajectoryData);

    const result = await validationLogic.validateTrip(trip.id, trip, trajectoryData, routeData);

    expect(result.passed).to.be.false;
    expect(result.details.dimensions.speed.passed).to.be.false;
  });
});
```

### 3. Driving Mode Validation
```javascript
describe('駕駛模式驗證', () => {
  it('應該驗證正常的駕駛行程', async () => {
    const trip = createTrip({
      travel_mode: TRAVEL_MODE.DRIVING
    });
    const trajectoryData = createTrajectoryData({
      speedKmh: 45,
      numPoints: 12,
      speedVariation: 10
    });
    const routeData = createRouteData(trajectoryData);

    const result = await validationLogic.validateTrip(trip.id, trip, trajectoryData, routeData);

    expect(result.passed).to.be.true;
    expect(result.score).to.be.greaterThan(0.6);
    expect(result.details.dimensions.speed.passed).to.be.true;
  });

  it('應該處理交通擁塞情況', async () => {
    const trip = createTrip({
      travel_mode: TRAVEL_MODE.DRIVING,
      estimated_arrival_on: '2023-01-01T11:00:00Z',
      ended_on: '2023-01-01T11:30:00Z' // 30 minutes delay
    });
    const trajectoryData = createTrajectoryData({
      speedKmh: 15, // Slow due to traffic
      numPoints: 20,
      irregularTimeGaps: true
    });
    const routeData = createRouteData(trajectoryData);

    const result = await validationLogic.validateTrip(trip.id, trip, trajectoryData, routeData);

    expect(result.passed).to.be.true;
    expect(result.details.dimensions.time.notes).to.include('traffic');
  });
});
```

### 4. Biking Mode Validation
```javascript
describe('騎行模式驗證', () => {
  it('應該驗證正常的騎行行程', async () => {
    const trip = createTrip({
      travel_mode: TRAVEL_MODE.BIKING
    });
    const trajectoryData = createTrajectoryData({
      speedKmh: 18,
      numPoints: 10,
      speedVariation: 5
    });
    const routeData = createRouteData(trajectoryData);

    const result = await validationLogic.validateTrip(trip.id, trip, trajectoryData, routeData);

    expect(result.passed).to.be.true;
    expect(result.score).to.be.greaterThan(0.7);
  });

  it('應該處理坡度變化的騎行', async () => {
    const trip = createTrip({
      travel_mode: TRAVEL_MODE.BIKING
    });
    const trajectoryData = createTrajectoryData({
      speedKmh: 12,
      numPoints: 15,
      speedVariation: 8 // High variation due to hills
    });
    const routeData = createRouteData(trajectoryData);

    const result = await validationLogic.validateTrip(trip.id, trip, trajectoryData, routeData);

    expect(result.passed).to.be.true;
    expect(result.details.dimensions.speed.variationScore).to.be.greaterThan(0.5);
  });
});
```

### 5. Public Transit Validation
```javascript
describe('大眾運輸驗證', () => {
  it('應該驗證公車行程', async () => {
    const trip = createTrip({
      travel_mode: TRAVEL_MODE.PUBLIC_TRANSIT
    });
    const trajectoryData = createTrajectoryData({
      speedKmh: 25,
      numPoints: 18,
      irregularTimeGaps: true // Bus stops
    });
    const routeData = createRouteData(trajectoryData);

    const result = await validationLogic.validateTrip(trip.id, trip, trajectoryData, routeData);

    expect(result.passed).to.be.true;
    expect(result.details.dimensions.route.transitStops).to.be.greaterThan(0);
  });

  it('應該驗證地鐵行程', async () => {
    const trip = createTrip({
      travel_mode: TRAVEL_MODE.PUBLIC_TRANSIT
    });
    const trajectoryData = createTrajectoryData({
      speedKmh: 35,
      numPoints: 8,
      routeDeviation: 50 // Underground GPS variations
    });
    const routeData = createRouteData(trajectoryData);

    const result = await validationLogic.validateTrip(trip.id, trip, trajectoryData, routeData);

    expect(result.passed).to.be.true;
    expect(result.details.dimensions.route.undergroundTolerance).to.be.true;
  });
});
```

## Advanced Validation Dimensions

### 1. Speed Validation
```javascript
const validateSpeed = (trajectory, travelMode) => {
  const speeds = trajectory.map(point => point.speed);
  const avgSpeed = speeds.reduce((a, b) => a + b, 0) / speeds.length;
  const maxSpeed = Math.max(...speeds);
  const speedVariation = calculateStandardDeviation(speeds);

  const thresholds = getSpeedThresholds(travelMode);
  
  return {
    passed: avgSpeed >= thresholds.min && avgSpeed <= thresholds.max,
    averageSpeed: avgSpeed,
    maxSpeed: maxSpeed,
    variation: speedVariation,
    score: calculateSpeedScore(avgSpeed, thresholds)
  };
};
```

### 2. Route Validation
```javascript
const validateRoute = (trajectory, routeData, travelMode) => {
  const plannedRoute = JSON.parse(routeData.route);
  const actualRoute = trajectory.map(p => [p.longitude, p.latitude]);
  
  const routeDeviation = calculateRouteDeviation(plannedRoute, actualRoute);
  const routeCompletion = calculateRouteCompletion(plannedRoute, actualRoute);
  
  const thresholds = getRouteThresholds(travelMode);
  
  return {
    passed: routeDeviation <= thresholds.maxDeviation && routeCompletion >= thresholds.minCompletion,
    deviation: routeDeviation,
    completion: routeCompletion,
    score: calculateRouteScore(routeDeviation, routeCompletion, thresholds)
  };
};
```

### 3. Time Validation
```javascript
const validateTime = (trip, trajectory) => {
  const plannedDuration = new Date(trip.estimated_arrival_on) - new Date(trip.started_on);
  const actualDuration = new Date(trip.ended_on) - new Date(trip.started_on);
  const trajectoryDuration = new Date(trajectory[trajectory.length - 1].timestamp) - new Date(trajectory[0].timestamp);
  
  const timeDeviation = Math.abs(actualDuration - plannedDuration) / plannedDuration;
  const trajectoryConsistency = Math.abs(actualDuration - trajectoryDuration) / actualDuration;
  
  return {
    passed: timeDeviation <= 0.5 && trajectoryConsistency <= 0.1,
    plannedDuration: plannedDuration,
    actualDuration: actualDuration,
    deviation: timeDeviation,
    consistency: trajectoryConsistency,
    score: calculateTimeScore(timeDeviation, trajectoryConsistency)
  };
};
```

## Quality Assurance Framework

### Test Coverage Matrix
- **Travel Modes**: All 9 supported transportation modes
- **Validation Dimensions**: Speed, Route, Time, Distance
- **Edge Cases**: Extreme values, missing data, corrupted trajectories
- **Performance**: Large datasets, real-time processing
- **Integration**: Cross-system validation consistency

### Data Quality Validation
```javascript
const validateDataQuality = (trajectory) => {
  const qualityChecks = {
    completeness: trajectory.length >= MIN_TRAJECTORY_POINTS,
    consistency: validateTimestampSequence(trajectory),
    accuracy: validateCoordinateAccuracy(trajectory),
    plausibility: validateSpeedPlausibility(trajectory)
  };
  
  return {
    passed: Object.values(qualityChecks).every(check => check),
    checks: qualityChecks,
    score: calculateQualityScore(qualityChecks)
  };
};
```

### Performance Benchmarks
```javascript
describe('性能測試', () => {
  it('應該在合理時間內完成驗證', async () => {
    const trip = createTrip();
    const trajectoryData = createTrajectoryData({ numPoints: 1000 });
    const routeData = createRouteData(trajectoryData);

    const startTime = Date.now();
    const result = await validationLogic.validateTrip(trip.id, trip, trajectoryData, routeData);
    const endTime = Date.now();

    expect(endTime - startTime).to.be.lessThan(5000); // 5 seconds max
    expect(result.passed).to.be.a('boolean');
  });
});
```

## Integration Testing

### Cross-Mode Validation
```javascript
describe('跨模式整合測試', () => {
  it('應該一致地處理所有交通模式', async () => {
    const modes = Object.values(TRAVEL_MODE);
    const results = [];

    for (const mode of modes) {
      const trip = createTrip({ travel_mode: mode });
      const trajectoryData = createTrajectoryData(getModeSpecificOptions(mode));
      const routeData = createRouteData(trajectoryData);

      const result = await validationLogic.validateTrip(trip.id, trip, trajectoryData, routeData);
      results.push({ mode, result });
    }

    // Validate consistency across modes
    results.forEach(({ mode, result }) => {
      expect(result).to.have.property('passed');
      expect(result).to.have.property('score');
      expect(result.score).to.be.within(0, 1);
    });
  });
});
```

This comprehensive test suite ensures the validation system accurately processes all transportation modes with consistent quality standards, robust error handling, and reliable performance across diverse real-world scenarios.