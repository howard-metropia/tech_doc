# Test Documentation: Incident Event Service Functions

## Overview
This test suite validates the core service functions used for processing incident events and user informatics within the TSP system. The test covers geospatial operations, polygon intersections, event retrieval, and trip ID extraction utilities that support the incident event API functionality.

## Test Configuration
- **File**: `test/test-incident-event-service.js`
- **Framework**: Mocha with Chai assertions, Sinon for stubbing/spying
- **Models Used**: `EventAggregator`, `IncidentsEvent` (MongoDB)
- **Service**: `@app/src/services/uis/userInformaticEvent`
- **Dependencies**: GeoJSON processing, angle calculations, database operations

## Functions Tested

### 1. transToGEOJson(coordinates)
**Purpose**: Converts coordinate arrays to GeoJSON format by swapping lat/lng order

**Happy Path**:
```javascript
// Input: [[longitude, latitude]]
const coordinates = [[123, 45]];
const result = transToGEOJson(coordinates);
// Output: [[latitude, longitude]]
expect(result).to.deep.eq([[45, 123]]);
```

**Edge Cases**:
- **Empty Input**: Returns empty array `[]`
- **Invalid Coordinates**: Returns empty array and logs error
- **Incomplete Coordinates**: `[[123]]` returns `[]` with error logging

**Error Handling**: Logs errors for malformed coordinate data

### 2. intersectPolygon(eventPolygon, tripPolygon)
**Purpose**: Calculates geometric intersection between event and trip polygons

**Happy Path**:
```javascript
const intersection = intersectPolygon(testEvent.polygon, testTripPolygon);
expect(intersection).not.to.be.empty;
expect(intersection).not.to.deep.eq({});
```

**Error Cases**:
- **Empty Event Polygon**: Returns `{}` and logs error
- **Empty Trip Polygon**: Returns `{}` and logs error
- **Invalid Polygon Data**: Handles gracefully with error logging

**Geospatial Processing**: Uses GeoJSON geometry intersection algorithms

### 3. hasIntersect(intersectionResult)
**Purpose**: Determines if polygon intersection contains any features

**Test Cases**:
```javascript
// Valid intersection
const validInput = { features: [1, 2, 4] };
expect(hasIntersect(validInput)).to.be.true;

// Empty intersection
const emptyInput = { features: [] };
expect(hasIntersect(emptyInput)).to.be.false;

// Null input
expect(hasIntersect(null)).to.be.false;
```

**Logic**: Returns `true` if features array exists and has length > 0

### 4. getTripAngle(event, tripCoordinates)
**Purpose**: Calculates angle between event location and trip coordinates

**Happy Path**:
```javascript
const angle = getTripAngle(testEvent, testTripPolygon);
const expectedAngle = 287.13596612103277;
expect(angle).to.deep.eq(expectedAngle);
```

**Error Cases**:
- **Null Event**: Returns `-1` and logs error
- **Null Coordinates**: Returns `-1` and logs error
- **Invalid Data**: Handles gracefully with error logging

**Mathematical Calculation**: Uses geometric formulas to determine bearing/angle

### 5. checkAngleAndDirection(description, angle)
**Purpose**: Validates if event direction matches trip angle

**Happy Path**:
```javascript
const testAngle = 280;
const result = checkAngleAndDirection(testEvent.location, testAngle);
expect(result).to.be.true;
```

**Error Cases**:
- **Null Description**: Returns `false` and logs error
- **Null Angle**: Returns `false`
- **Invalid Data**: Returns `false`

**Direction Matching**: Parses location descriptions for directional keywords (Northbound, Southbound, etc.)

### 6. getOngoingEvents(type)
**Purpose**: Retrieves active events from database by type

**Happy Path**:
```javascript
// Setup test data in MongoDB
await IncidentsEvent.findOneAndUpdate(
  { _id: testEvent._id, event_id: testEvent.event_id },
  testEvent,
  { upsert: true }
);

const events = await getOngoingEvents(testEvent.type);
expect(events).not.to.be.empty;
```

**Error Handling**:
```javascript
// Mock database error
stubCollection = sinon.stub(IncidentsEvent, 'find');
stubCollection.throws(new Error('Something happened'));

const result = await getOngoingEvents(testEvent.type);
expect(result).to.be.null;
expect(spyLoggerError.callCount).to.be.eq(1);
```

**Database Integration**: Queries `IncidentsEvent` collection with error handling

### 7. getDmsEvents(type)
**Purpose**: Retrieves DMS (Dynamic Message Sign) events from EventAggregator

**Happy Path**:
```javascript
// Setup DMS test data
await EventAggregator.findOneAndUpdate(
  { _id: mockDmsData._id, event_id: mockDmsData.event_id },
  mockDmsData,
  { upsert: true }
);

const dmsEvents = await getDmsEvents(mockDmsData.type);
expect(dmsEvents).not.to.be.empty;
```

**Error Handling**:
```javascript
// Mock database error
stubCollection = sinon.stub(EventAggregator, 'find');
stubCollection.throws(new Error('Something happened'));

const result = await getDmsEvents(mockDmsData.type);
expect(result).to.be.null;
expect(spyLoggerError.callCount).to.be.eq(1);
```

**Collection Difference**: Uses `EventAggregator` instead of `IncidentsEvent`

### 8. extractTripIDFromActivityID(activityId)
**Purpose**: Extracts trip information from encoded activity IDs

**Trip Type Patterns**:

#### Habitual Trip (Type 1)
```javascript
const activityId = 11609620240306; // Format: 1[trip_id][date]
const result = extractTripIDFromActivityID(activityId);
expect(result).to.deep.eq({ type: 1, trip_id: 16096 });
```

#### Reservation Trip (Type 2)
```javascript
const activityId = 28534; // Format: 2[trip_id]
const result = extractTripIDFromActivityID(activityId);
expect(result).to.deep.eq({ type: 2, trip_id: 8534 });
```

#### Calendar Event Trip (Type 3)
```javascript
const activityId = 3169231708954200; // Format: 3[trip_id]
const result = extractTripIDFromActivityID(activityId);
expect(result).to.deep.eq({ type: 3, trip_id: 169231708954200 });
```

**Error Cases**:
```javascript
// Invalid format
const invalidId = 54657;
expect(extractTripIDFromActivityID(invalidId)).to.be.null;

// Empty input
expect(extractTripIDFromActivityID('')).to.be.null;
```

**ID Parsing Logic**:
- Type determined by first digit
- Trip ID extracted by removing type prefix and date suffix
- Complex parsing for different activity types

## Test Data Structures

### Mock Event Data
```javascript
const testEvent = {
  _id: 'TESTConst1234567',
  event_id: 'TESTConst1234567',
  close: false,
  description: 'Closed continuously until 5:00 PM, Friday, April 7',
  expires: '2024-01-23T03:24:26.143Z',
  lat: -29.540446,
  lon: -95.019508,
  location: 'SH-146 Northbound At 9Th St (Closed continuously until 5:00 PM, Friday, April 7)',
  polygon: [/* complex polygon coordinates */],
  reroute: 1,
  start: '2023-03-06T13:00:00',
  type: 'Closure'
};
```

### Mock DMS Data
```javascript
const mockDmsData = {
  _id: 'TESTDMS12345',
  description: 'ROAD[nl]WORK[nl]AHEAD[np]REDUCED[nl]SPEED[nl]AHEAD',
  event_id: 'TESTDMS12345',
  lat: -29.7725,
  lon: -96.07,
  location: 'IH-10 West Eastbound at Mlcak Rd',
  polygon: [/* polygon coordinates */],
  reroute: 0,
  type: 'DMS'
};
```

### Test Trip Polygon
```javascript
const testTripPolygon = [
  [-95.133318, -29.915773],
  [-95.133396, -29.915064],
  // ... additional coordinate pairs
  [-95.14834599999996, -29.920422000000013]
];
```

## Error Handling Patterns

### Database Error Simulation
```javascript
let stubCollection;
before(() => {
  stubCollection = sinon.stub(IncidentsEvent, 'find');
  stubCollection.throws(new Error('Something happened'));
});
after(() => {
  stubCollection.restore();
});
```

### Error Logging Verification
```javascript
let spyLoggerError;
beforeEach(() => {
  spyLoggerError = sandbox.spy(logger, 'error');
});
afterEach(() => {
  spyLoggerError.restore();
});

// Test verification
expect(spyLoggerError.callCount).to.be.eq(1);
```

## Geospatial Processing

### Coordinate Transformation
- Handles longitude/latitude order conversion for GeoJSON
- Validates coordinate array completeness
- Provides error handling for malformed data

### Polygon Intersection
- Calculates geometric intersections between polygons
- Returns intersection results as GeoJSON features
- Handles edge cases with empty or invalid polygons

### Angle Calculation
- Computes bearing angles between geographical points
- Uses mathematical formulas for precise angle determination
- Provides directional analysis for route relevance

## Database Integration

### MongoDB Collections
- **IncidentsEvent**: Traffic incidents, closures, flood warnings
- **EventAggregator**: DMS signs and aggregated event data

### Query Patterns
- Type-based event filtering
- Active event retrieval (non-closed events)
- Upsert operations for test data management

### Error Recovery
- Graceful handling of database connection issues
- Null return values for failed operations
- Comprehensive error logging for debugging

## Activity ID Encoding

### ID Structure Analysis
The `extractTripIDFromActivityID` function reveals a complex encoding scheme:

**Pattern Recognition**:
- **Habitual Trips**: `1` + `trip_id` + `date_suffix`
- **Reservation Trips**: `2` + `trip_id`
- **Calendar Events**: `3` + `trip_id`

**Parsing Logic**:
- First digit determines trip type
- Remaining digits parsed based on type pattern
- Date information extracted for habitual trips

## Test Coverage

### Unit Test Coverage
- ✅ Coordinate transformation functions
- ✅ Geospatial intersection calculations
- ✅ Angular computation and direction matching
- ✅ Database query operations
- ✅ ID parsing and extraction

### Error Scenario Coverage
- ✅ Database connection failures
- ✅ Invalid input data handling
- ✅ Malformed coordinate arrays
- ✅ Null and undefined inputs
- ✅ Error logging verification

### Integration Points
- ✅ MongoDB collection interactions
- ✅ GeoJSON processing workflows
- ✅ Mathematical calculation accuracy
- ✅ Activity ID parsing logic

## Business Logic Insights

### Trip Route Analysis
- Functions support real-time route analysis against traffic events
- Angle calculations enable directional relevance filtering
- Polygon intersections provide precise geographical matching

### Event Relevance
- Geometric calculations determine if events affect user routes
- Direction matching ensures relevant event notifications
- Distance and angle thresholds filter irrelevant events

### Data Architecture
- Separation between incident events and DMS data
- Activity ID encoding supports multiple trip management systems
- Flexible polygon geometry handling for various event types

This test suite ensures the reliability of core geospatial and data processing functions that power the incident event notification system within the TSP platform.