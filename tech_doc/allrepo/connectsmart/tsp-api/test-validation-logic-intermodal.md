# TSP API Test Suite - Intermodal Validation Logic Tests

## Overview
The `test-validation-logic-intermodal.js` file contains comprehensive tests for intermodal transportation validation, ensuring accurate verification of multi-modal trips that combine different transportation methods within a single journey.

## File Location
`/allrepo/connectsmart/tsp-api/test/test-validation-logic-intermodal.js`

## Dependencies
- **chai**: Testing assertions and expectations
- **sinon**: Test doubles, mocking, and stubbing
- **proxyquire**: Module dependency injection for testing

## Test Architecture

### Mock Infrastructure
```javascript
// Logger Mock
const loggerMock = {
  info: sinon.stub(),
  error: sinon.stub(),
  warn: sinon.stub()
};

// Travel Mode Definitions
const DEFINE = {
  travelMode: {
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
};
```

### MongoDB Mock Models
```javascript
const routesHistoryMock = {
  findOne: sinon.stub()
};

const polyMock = {
  decode: sinon.stub()
};
```

## Intermodal Trip Characteristics

### Multi-Modal Transportation Pattern
Intermodal trips combine multiple transportation modes in sequence:
1. **Walking Phase**: Initial pedestrian movement (2-5 km/h)
2. **Biking Phase**: Cycling segment (10-20 km/h) 
3. **Public Transit Phase**: Bus/train segment (20-40 km/h)
4. **Walking Phase**: Final pedestrian movement (2-5 km/h)

### Speed Profile Analysis
```javascript
function createTrajectoryData() {
  const baseTime = new Date('2023-01-01T10:00:00Z').getTime();
  const data = [];

  for (let i = 0; i <= 60; i += 3) {
    const timestamp = new Date(baseTime + i * 60 * 1000).toISOString();
    let speed;

    // Multi-modal speed simulation
    if (i < 15) {
      speed = 2 + Math.random() * 3;      // Walking: 2-5 km/h
    } else if (i < 30) {
      speed = 10 + Math.random() * 10;    // Biking: 10-20 km/h
    } else if (i < 45) {
      speed = 20 + Math.random() * 20;    // Transit: 20-40 km/h
    } else {
      speed = 2 + Math.random() * 3;      // Walking: 2-5 km/h
    }

    data.push({
      timestamp,
      latitude: 25.0 + (i * 0.001),
      longitude: 121.5 + (i * 0.001),
      speed: speed / 1.609344  // Convert to mph for processing
    });
  }

  return data;
}
```

## Validation Logic Implementation

### Intermodal Trip Validation
```javascript
const validationLogic = proxyquire('../src/services/validationLogic', {
  '@maas/core/log': { logger: loggerMock },
  '@app/src/static/defines': DEFINE,
  '@app/src/models/RoutesHistorys': { RoutesHistorys: routesHistoryMock },
  '@app/src/services/hereMapPolylines': polyMock
});
```

### Mode Transition Analysis
```javascript
const analyzeModalTransitions = (trajectory) => {
  const speedChanges = [];
  const modes = [];
  
  for (let i = 1; i < trajectory.length; i++) {
    const prevSpeed = trajectory[i-1].speed * 1.609344; // Convert to km/h
    const currSpeed = trajectory[i].speed * 1.609344;
    const speedChange = Math.abs(currSpeed - prevSpeed);
    
    if (speedChange > SPEED_CHANGE_THRESHOLD) {
      speedChanges.push({
        timestamp: trajectory[i].timestamp,
        fromSpeed: prevSpeed,
        toSpeed: currSpeed,
        change: speedChange
      });
    }
    
    modes.push(classifyTransportMode(currSpeed));
  }
  
  return { speedChanges, modes };
};
```

## Test Data Structure

### Trip Creation Factory
```javascript
function createTrip(overrides = {}) {
  return {
    id: 12345,
    user_id: 1003,
    travel_mode: DEFINE.travelMode.INTERMODAL,
    started_on: '2023-01-01T10:00:00Z',
    estimated_arrival_on: '2023-01-01T11:00:00Z',
    ended_on: '2023-01-01T10:55:00Z',
    trip_detail_uuid: 'test-uuid-123',
    origin_latitude: 25.0,
    origin_longitude: 121.5,
    destination_latitude: 25.06,
    destination_longitude: 121.56,
    ...overrides
  };
}
```

### Trajectory Generation with Modal Phases
```javascript
const generateIntermodalTrajectory = () => {
  const phases = [
    { mode: 'walking', duration: 15, speed: 4 },      // 15 minutes walking
    { mode: 'biking', duration: 15, speed: 15 },       // 15 minutes biking  
    { mode: 'transit', duration: 20, speed: 30 },      // 20 minutes transit
    { mode: 'walking', duration: 10, speed: 4 }        // 10 minutes walking
  ];
  
  const trajectory = [];
  let currentTime = new Date('2023-01-01T10:00:00Z');
  let currentLat = 25.0;
  let currentLng = 121.5;
  
  phases.forEach(phase => {
    const points = Math.floor(phase.duration / 3); // Point every 3 minutes
    
    for (let i = 0; i < points; i++) {
      trajectory.push({
        timestamp: currentTime.toISOString(),
        latitude: currentLat,
        longitude: currentLng,
        speed: phase.speed + (Math.random() * 5 - 2.5), // ±2.5 km/h variation
        mode: phase.mode
      });
      
      currentTime = new Date(currentTime.getTime() + 3 * 60 * 1000); // +3 minutes
      currentLat += 0.001;
      currentLng += 0.001;
    }
  });
  
  return trajectory;
};
```

## Intermodal Validation Criteria

### 1. Modal Sequence Validation
```javascript
const validateModalSequence = (trajectory) => {
  const modes = trajectory.map(point => classifyTransportMode(point.speed));
  const transitions = identifyTransitions(modes);
  
  return {
    validSequence: isValidIntermodalSequence(transitions),
    transitionPoints: transitions.length,
    modesUsed: [...new Set(modes)],
    primaryMode: findPrimaryMode(modes)
  };
};
```

### 2. Speed Consistency Validation
```javascript
const validateSpeedConsistency = (trajectory) => {
  const speedsByMode = groupSpeedsByMode(trajectory);
  const consistencyScores = {};
  
  Object.entries(speedsByMode).forEach(([mode, speeds]) => {
    const avgSpeed = speeds.reduce((a, b) => a + b, 0) / speeds.length;
    const expectedRange = getExpectedSpeedRange(mode);
    
    consistencyScores[mode] = {
      average: avgSpeed,
      expected: expectedRange,
      consistent: avgSpeed >= expectedRange.min && avgSpeed <= expectedRange.max,
      variance: calculateVariance(speeds)
    };
  });
  
  return consistencyScores;
};
```

### 3. Transition Point Analysis
```javascript
const analyzeTransitionPoints = (trajectory) => {
  const transitions = [];
  let currentMode = null;
  
  trajectory.forEach((point, index) => {
    const pointMode = classifyTransportMode(point.speed);
    
    if (currentMode && pointMode !== currentMode) {
      transitions.push({
        timestamp: point.timestamp,
        location: { lat: point.latitude, lng: point.longitude },
        fromMode: currentMode,
        toMode: pointMode,
        index: index
      });
    }
    
    currentMode = pointMode;
  });
  
  return {
    transitions,
    transitionCount: transitions.length,
    validTransitions: transitions.filter(t => isValidTransition(t.fromMode, t.toMode))
  };
};
```

## Transport Mode Classification

### Speed-Based Mode Detection
```javascript
const classifyTransportMode = (speedKmh) => {
  if (speedKmh < 8) return 'walking';
  if (speedKmh < 25) return 'biking';
  if (speedKmh < 50) return 'transit';
  if (speedKmh < 80) return 'driving';
  return 'unknown';
};

const getExpectedSpeedRange = (mode) => {
  const ranges = {
    walking: { min: 2, max: 8 },
    biking: { min: 8, max: 25 },
    transit: { min: 15, max: 50 },
    driving: { min: 25, max: 120 }
  };
  
  return ranges[mode] || { min: 0, max: 200 };
};
```

## Test Scenarios

### 1. Successful Intermodal Validation
```javascript
describe('Intermodal Validation Tests', function() {
  it('should validate a complete intermodal journey', async () => {
    const trip = createTrip();
    const trajectoryData = createTrajectoryData();
    const routeData = createRouteData(trajectoryData);

    const result = await validationLogic.validateTrip(trip.id, trip, trajectoryData, routeData);

    expect(result.passed).to.be.true;
    expect(result.score).to.be.greaterThan(0.7);
    expect(result.details.intermodalAnalysis).to.exist;
    expect(result.details.intermodalAnalysis.modesDetected).to.have.length.greaterThan(1);
  });
});
```

### 2. Modal Transition Validation
```javascript
it('should detect valid modal transitions', async () => {
  const trip = createTrip();
  const trajectoryData = generateIntermodalTrajectory();
  const routeData = createRouteData(trajectoryData);

  const result = await validationLogic.validateTrip(trip.id, trip, trajectoryData, routeData);

  expect(result.details.transitions).to.have.length.greaterThan(0);
  expect(result.details.transitions.every(t => t.valid)).to.be.true;
});
```

### 3. Speed Profile Validation
```javascript
it('should validate speed profiles for each transport mode', async () => {
  const trip = createTrip();
  const trajectoryData = createTrajectoryData();
  const routeData = createRouteData(trajectoryData);

  const result = await validationLogic.validateTrip(trip.id, trip, trajectoryData, routeData);

  const speedAnalysis = result.details.speedAnalysis;
  expect(speedAnalysis.walking.consistent).to.be.true;
  expect(speedAnalysis.biking.consistent).to.be.true;
  expect(speedAnalysis.transit.consistent).to.be.true;
});
```

## Route Data Integration

### HERE Maps Polyline Integration
```javascript
const routeData = {
  polyline: 'encoded_polyline_string',
  distance: 15000, // meters
  duration: 3300,  // seconds
  segments: [
    { mode: 'walking', distance: 800, duration: 600 },
    { mode: 'biking', distance: 3000, duration: 720 },
    { mode: 'transit', distance: 10000, duration: 1200 },
    { mode: 'walking', distance: 1200, duration: 900 }
  ]
};
```

### Polyline Decoding Mock
```javascript
polyMock.decode.returns([
  [121.5, 25.0],    // Walking start
  [121.51, 25.01],  // Bike pickup
  [121.53, 25.03],  // Transit station
  [121.55, 25.05],  // Transit destination
  [121.56, 25.06]   // Walking end
]);
```

## Quality Assurance

### Validation Metrics
- **Mode Detection Accuracy**: Correct classification of transport modes
- **Transition Validation**: Valid modal transition points
- **Speed Consistency**: Appropriate speeds for each mode
- **Route Compliance**: Adherence to planned intermodal route
- **Temporal Accuracy**: Realistic timing for mode transitions

### Edge Case Handling
- **Incomplete Trajectories**: Missing GPS data during transitions
- **Mode Ambiguity**: Speed ranges that overlap between modes
- **Rapid Transitions**: Quick changes between transportation modes
- **GPS Noise**: Inaccurate location data affecting speed calculations

### Performance Considerations
- **Processing Time**: Efficient analysis of complex multi-modal data
- **Memory Usage**: Optimal handling of large trajectory datasets
- **Accuracy vs Speed**: Balance between validation accuracy and processing speed

## Integration Points

### Trip Management System
- Real-time validation during intermodal trips
- Mode transition notifications
- Progress tracking across transportation modes

### Incentive System  
- Multi-modal trip bonuses
- Environmental impact calculations
- Mode-specific reward calculations

### Route Planning
- Intermodal route optimization
- Real-time mode availability
- Dynamic route adjustments

This comprehensive test suite ensures the intermodal validation system accurately processes complex multi-modal journeys, correctly identifies transportation mode transitions, and provides reliable validation for incentive programs while maintaining high performance standards.