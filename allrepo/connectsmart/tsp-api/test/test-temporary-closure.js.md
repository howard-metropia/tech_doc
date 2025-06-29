# test-temporary-closure.js

## Overview
Test suite for the road temporary closure system in the TSP API. Tests the filtering of parking lots based on active road closure events using polygon-based geographic filtering.

## File Location
`/test/test-temporary-closure.js`

## Dependencies
- **chai**: BDD/TDD assertion library
- **sinon**: Test spies, stubs, and mocks
- **moment**: Date/time manipulation
- **@maas/core**: Core MaaS framework components
- **Models**: RoadTemporaryClosure
- **Services**: parking/roadTemporaryClosure

## Core Functionality

### Main Function Under Test
```javascript
const { filterParkingLots } = require('@app/src/services/parking/roadTemporaryClosure');
```

### Input Format
```javascript
{
  offStreet: [{ lng: -77, lat: 44 }, ...],
  onStreet: [{ lng: -81, lat: 44 }, ...]
}
```

### Output Format
```javascript
{
  off: [...],  // Filtered off-street parking
  on: [...]    // Filtered on-street parking
}
```

## Database Model

### RoadTemporaryClosure Schema
```javascript
{
  id: number,
  event_name: string,
  start_time: ISO_DATE_STRING,
  end_time: ISO_DATE_STRING,
  polygon: JSON_STRING  // Array of coordinate arrays
}
```

### Polygon Format
```javascript
// Single polygon
[[-81, 41], [-81, 47], [-72, 47], [-72, 41], [-81, 41]]

// Multiple polygons
[
  [[-81, 41], [-81, 47], [-72, 47], [-72, 41], [-81, 41]],
  [[81, 41], [81, 47], [72, 47], [72, 41], [81, 41]]
]
```

## Test Structure

### Test Data Management
```javascript
const eventIds = [];
const addNewEvents = async (events) => {
  for (const event of events) {
    const res = await RoadTemporaryClosure.query().insert(event);
    eventIds.push(res.id);
  }
};
```

### Cleanup Process
```javascript
afterEach(async () => {
  await RoadTemporaryClosure.query().delete().whereIn('id', eventIds);
});
```

## Happy Path Test Cases

### 1. Empty Input Handling
**Test**: Empty parking lot arrays
**Expected**: Empty results
```javascript
const result = await filterParkingLots({
  offStreet: [],
  onStreet: []
});
// Expects: off.length = 0, on.length = 0
```

### 2. No Active Events
**Test**: Parking lots with no ongoing closure events
**Expected**: Original results returned unchanged
```javascript
const result = await filterParkingLots({
  offStreet: [{}, {}],
  onStreet: [{}, {}, {}, {}, {}]
});
// Expects: off.length = 2, on.length = 5
```

### 3. Expired Event Handling
**Test**: Past closure events should not affect results
**Event Time**: 2 days ago to 1 day ago
**Expected**: Original results returned
```javascript
start_time: moment.utc().add(-2, 'days').toISOString(),
end_time: moment.utc().add(-1, 'days').toISOString()
```

### 4. Points Inside Polygon
**Test**: Parking lots within closure polygon are filtered out
**Polygon**: Rectangular area from [-81,41] to [-72,47]
**Points**: 
- Inside: lng: -77, lat: 44
- Inside: lng: -81, lat: 44
**Expected**: Empty results (all points filtered)

### 5. Points Outside Polygon
**Test**: Parking lots outside closure polygon are preserved
**Points**:
- Outside: lng: -73, lat: 40
- Outside: lng: 81, lat: 44
**Expected**: Original results returned

### 6. Mixed Scenarios
**Test**: Combination of inside and outside points
**Expected**: Only outside points returned
```javascript
// Input: 2 off-street, 2 on-street
// One inside, one outside each
// Expected: 1 off-street, 1 on-street
```

### 7. Multiple Events
**Test**: Multiple active closure events
**Events**: Two separate polygon areas
**Expected**: Points filtered if inside ANY active polygon

### 8. Multiple Polygons per Event
**Test**: Single event with multiple polygon areas
**Polygon**: Two separate rectangular areas
**Expected**: Points filtered if inside ANY polygon of the event

### 9. Complex Multi-Event Multi-Polygon
**Test**: Multiple events, each with multiple polygons
**Events**: 
- Event 1: 2 polygons (west and east areas)
- Event 2: 2 polygons (central areas)
**Expected**: Comprehensive filtering across all polygons

## Unhappy Path Test Cases

### Exception Handling
**Test**: Database query failure
**Setup**: 
```javascript
const myOrmStub = sinon.stub(RTC, 'query');
myOrmStub.throws(new Error('Something happened'));
```
**Expected**: Original input returned unchanged
**Purpose**: Graceful degradation when closure data unavailable

## Geographic Logic

### Polygon Intersection
- **Point-in-Polygon Algorithm**: Determines if parking coordinates fall within closure boundaries
- **Multi-Polygon Support**: Events can have multiple non-contiguous areas
- **Coordinate System**: Standard longitude/latitude (WGS84)

### Time-Based Filtering
```javascript
// Event time validation
start_time: moment.utc().add(-1, 'days').toISOString(),  // Started yesterday
end_time: moment.utc().add(1, 'days').toISOString()      // Ends tomorrow
// Current time must be between start_time and end_time
```

## Test Scenarios Coverage

### Single Event Scenarios
1. **Empty inputs**: No parking lots to filter
2. **No events**: No active closures
3. **Expired events**: Past closures don't affect current results
4. **All inside**: All parking lots within closure area
5. **All outside**: No parking lots affected by closure
6. **Mixed locations**: Some affected, some not

### Multiple Event Scenarios
1. **Multiple single-polygon events**: Each event affects different areas
2. **Single multi-polygon event**: One event covers multiple areas
3. **Multiple multi-polygon events**: Complex closure patterns

### Error Scenarios
1. **Database failure**: System gracefully handles query errors
2. **Invalid polygon data**: System handles malformed geographic data

## Business Logic

### Parking Availability Impact
- **Road Closures**: Affect nearby parking availability
- **Event-Based**: Temporary closures for events, construction, etc.
- **Real-Time Filtering**: Dynamic parking recommendations based on current closures

### User Experience
- **Accurate Directions**: Prevents routing to inaccessible parking
- **Real-Time Updates**: Reflects current road conditions
- **Safety**: Avoids directing users to blocked areas

## Integration Points

### Geographic Services
- **Coordinate Processing**: Handles longitude/latitude calculations
- **Polygon Operations**: Point-in-polygon geometric calculations
- **Time Zone Handling**: UTC time for consistent closure timing

### Parking Services
- **Off-Street Parking**: Private lots and garages
- **On-Street Parking**: Public street parking spaces
- **Availability Updates**: Real-time parking space filtering

## Testing Best Practices

### Data Isolation
- **Unique Test Events**: Each test creates isolated closure events
- **Cleanup**: Automatic removal of test data after each test
- **No Interference**: Tests don't affect each other or production data

### Geographic Accuracy
- **Real Coordinates**: Uses realistic longitude/latitude values
- **Boundary Testing**: Tests edge cases at polygon boundaries
- **Multiple Scenarios**: Covers various geographic configurations

### Error Resilience
- **Exception Handling**: Tests system behavior during failures
- **Graceful Degradation**: Ensures service continues when closure data unavailable
- **Stub Testing**: Uses sinon to simulate database failures

This test suite ensures the road temporary closure system accurately filters parking options based on active closure events, maintaining service reliability and user safety in the TSP API's parking recommendation system.