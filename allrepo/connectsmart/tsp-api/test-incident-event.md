# Test Documentation: Incident Event API

## Overview
This test suite validates the Incident Event functionality, which provides real-time traffic incident and event information along user routes within the TSP system. The test covers retrieval of various event types including DMS (Dynamic Message Signs), traffic incidents, flood warnings, and road closures that affect user transportation planning.

## Test Configuration
- **File**: `test/test-incident-event.js`
- **Framework**: Mocha with Chai assertions, Sinon for mocking, Axios for HTTP testing
- **Test Timeout**: 10 seconds
- **Models Used**: `EventAggregator`, `IncidentsEvent` (MongoDB)
- **External Services**: HERE Routing API (mocked)
- **Authentication**: User ID-based (userid: 1003)

## API Endpoints Tested

### POST /user_informatic_events
**Purpose**: Retrieves traffic events and incidents along specified routes

**Request Structure**:
```javascript
{
  routes: [
    {
      id: 'R1',
      polyline: 'encoded_polyline_string'
    }
  ],
  type: 0, // Event type filter
  departure_time: 1705262400
}
```

**Event Types**:
- **0**: All event types
- **1**: Incidents only
- **2**: DMS (Dynamic Message Signs) only
- **3**: Flood warnings only
- **4**: Land closures only

## Event Types and Data Structures

### 1. DMS (Dynamic Message Signs) Events
**Source**: `EventAggregator` collection
**Purpose**: Real-time traffic signs and messages

**Test Data**:
```javascript
{
  _id: 'TESTDMS12345',
  event_id: 'TESTDMS12345',
  description: 'ROAD[nl]WORK[nl]AHEAD[np]REDUCED[nl]SPEED[nl]AHEAD',
  lat: -29.7725,
  lon: -96.07,
  location: 'IH-10 West Eastbound at Mlcak Rd',
  polygon: [/* geofence coordinates */],
  reroute: 0,
  type: 'DMS'
}
```

**Response Format**:
```javascript
{
  event_id: 'TESTDMS12345',
  polygon: [/* coordinates */],
  location: 'IH-10 West Eastbound at Mlcak Rd',
  type: 'DMS',
  expires_undecided: 0,
  incident_type: 'DMS',
  lat: -29.7725,
  lon: -96.07,
  description: 'ROAD\\nWORK\\nAHEAD\\fREDUCED\\nSPEED\\nAHEAD\\f',
  sound_description: [
    {
      delay: 0.25,
      message: 'The traffic sign 2 miles down the route says'
    },
    {
      message: 'ROAD',
      delay: 0.25
    }
    // ... additional audio segments
  ],
  reroute: 0,
  start: 'timestamp',
  expires: 'timestamp'
}
```

### 2. Traffic Incidents
**Source**: `IncidentsEvent` collection
**Purpose**: Real-time traffic incidents and disruptions

**Test Data**:
```javascript
{
  _id: 'TESTINCIDENT123456',
  event_id: 'TESTINCIDENT123456',
  description: 'Stalled vehicle',
  incident_type: 'Stalled vehicle',
  lat: -29.7776,
  lon: -95.3811,
  location: 'IH-10 Katy Westbound Before Taylor St',
  expires: '2023-03-26T16:12:00Z',
  start: '2023-03-25T15:12:00',
  type: 'incident',
  reroute: 0,
  record_formatted: {
    ROADWAY_NAME: 'IH-10 Katy'
  }
}
```

**Audio Description**:
```javascript
sound_description: [
  {
    message: 'A stalled vehicle on INTERSTATE 10 Katy might cause delays, you are still on the fastest route',
    delay: 0.5
  }
]
```

### 3. Flood Warning Events
**Purpose**: Weather-related flooding alerts

**Test Data**:
```javascript
{
  _id: 'TESTFLOOD98765',
  event_id: 'TESTFLOOD98765',
  incident_type: 'Incident',
  lat: 29.916112,
  lon: -95.141641,
  type: 'Flood',
  polygon: [/* large flood area polygon */]
}
```

**Response Format**:
```javascript
{
  event_id: 'TESTFLOOD98765',
  location: 'High risk of roadway flooding in this area. Avoid unnecessary travel.',
  incident_type: 'Roadway Flooding Danger',
  sound_description: [
    {
      message: 'Caution: Flooding Possible, follow posted signs and drive with care',
      delay: 0.5
    }
  ]
}
```

### 4. Land Closure Events
**Purpose**: Construction and road closure information

**Test Data**:
```javascript
{
  _id: 'TESTConst1234567',
  event_id: 'TESTConst1234567',
  description: 'Closed continuously until 5:00 PM, Friday, April 7',
  location: 'SH-146 Northbound At 9Th St (Closed continuously until 5:00 PM, Friday, April 7)',
  type: 'Closure',
  reroute: 1
}
```

**Response Format**:
```javascript
{
  incident_type: 'Construction zone',
  sound_description: [/* empty sound description */],
  reroute: 1
}
```

## Test Scenarios

### Happy Path Testing

#### 1. All Event Types (type: 0)
- Returns both DMS and incident events
- Validates complete event data structure
- Excludes time-sensitive fields from validation (start/expires)

#### 2. Incidents Only (type: 1)
- Filters to incident events only
- Validates incident-specific response format
- Includes audio description for navigation

#### 3. DMS Only (type: 2)
- Filters to DMS events only
- Validates DMS message formatting
- Excludes time-sensitive fields (start/expires)

#### 4. Flood Warnings (type: 3)
- Uses specific polyline for flood area intersection
- Validates flood-specific messaging
- Includes safety-focused audio descriptions

#### 5. Land Closures (type: 4)
- Uses specific polyline for closure area intersection
- Validates construction zone information
- Includes reroute recommendations

### Unhappy Path Testing

#### 1. Empty Route Validation
```javascript
{
  routes: [{ id: 'R1', polyline: '' }], // Empty polyline
  type: 0
}
```
**Expected Error**: `10002 - Request body not correct`

#### 2. Invalid Event Type
```javascript
{
  routes: [{ id: 'R1', polyline: 'valid_polyline' }],
  type: -1 // Invalid type
}
```
**Expected Error**: `10002 - Request body not correct`

#### 3. Missing Route ID
```javascript
{
  routes: [{ polyline: 'valid_polyline' }], // Missing id
  type: 0
}
```
**Expected Error**: `10002 - Request body not correct`

## External Service Integration

### HERE Routing API Mock
**Purpose**: Provides route calculation for event intersection detection

**Mock Response**:
```javascript
{
  routes: [
    {
      sections: [
        {
          summary: {
            baseDuration: 1
          }
        }
      ]
    }
  ]
}
```

**Usage**: Determines if events intersect with user's planned route

## Audio Description Processing

### DMS Message Formatting
- Converts special markers: `[nl]` → `\\n`, `[np]` → `\\f`
- Generates audio segments with timing delays
- Provides contextual introduction for traffic signs

### Incident Audio Generation
- Creates natural language descriptions
- Includes roadway information from `record_formatted`
- Provides reassurance about route optimality

### Safety Audio Messages
- Flood warnings emphasize caution and safety
- Construction zones use empty descriptions (visual-only)
- Consistent delay timing for audio playback

## Geospatial Processing

### Polyline Intersection
- Uses encoded polylines for route representation
- Calculates intersections with event polygons
- Supports complex polygon geometries for flood/closure areas

### Event Filtering
- Geographic filtering based on route intersection
- Type-based filtering for specific event categories
- Time-based filtering for active events only

## Data Management

### Test Data Setup
```javascript
before(async () => {
  // Insert mock data into MongoDB collections
  await EventAggregator.findOneAndUpdate(/* DMS data */);
  await IncidentsEvent.findOneAndUpdate(/* Incident data */);
  await IncidentsEvent.findOneAndUpdate(/* Flood data */);
  await IncidentsEvent.findOneAndUpdate(/* Closure data */);
});
```

### Test Data Cleanup
```javascript
after(async () => {
  // Remove test data
  await EventAggregator.deleteOne({ _id: mockDmsData._id });
  await IncidentsEvent.deleteMany({
    _id: { $in: [/* test event IDs */] }
  });
});
```

## Error Handling and Logging

### Validation Logging
- Logs validation errors with specific details
- Tracks request body validation failures
- Monitors logger warning call counts

### Service Integration Monitoring
- Monitors external service call success/failure
- Logs geospatial processing errors
- Tracks event retrieval performance

## Business Value

### Real-Time Navigation
- Provides current traffic conditions for route planning
- Enables proactive route adjustments based on incidents
- Supports multi-modal transportation decisions

### Safety Enhancement
- Warns users of hazardous conditions (flooding)
- Provides construction zone awareness
- Delivers audio alerts for hands-free operation

### Traffic Management
- Integrates with city traffic management systems
- Supports DMS message distribution
- Enables coordinated incident response

## Test Coverage

### Functional Coverage
- ✅ All event type filtering (0-4)
- ✅ Geospatial intersection processing
- ✅ Audio description generation
- ✅ External service integration
- ✅ Data format validation

### Error Coverage
- ✅ Request validation errors
- ✅ Invalid route data handling
- ✅ Service integration failures
- ✅ Geospatial processing edge cases

### Integration Coverage
- ✅ MongoDB event retrieval
- ✅ HERE Routing API interaction
- ✅ Audio description service integration
- ✅ Polyline encoding/decoding

This test suite ensures the incident event system provides reliable, real-time traffic information to enhance user transportation decisions and safety within the TSP platform.