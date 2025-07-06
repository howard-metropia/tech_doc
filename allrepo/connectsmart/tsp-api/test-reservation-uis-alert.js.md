# test-reservation-uis-alert.js Technical Documentation

## Purpose

Integration test suite for UIS (Urban Information System) alert functionality within the reservation system, testing how transit alerts affect reservations and trip details.

## Core Features

### Alert Management Integration

#### 1. Transit Alert Processing
- **Model**: `TransitAlert`
- **Alert Types**: Delays, detours, service disruptions
- **Properties**:
  - `event_id`: Unique alert identifier
  - `type`: Alert category
  - `effect_name`: Impact type (Delay, Detour, etc.)
  - `header_text`: Alert title
  - `description_text`: Detailed alert information
  - `severity`: Alert priority level
  - `start`/`expires`: Alert timeframe

#### 2. Route-Alert Association
- **Model**: `TransitAlertRoute`
- **Purpose**: Links alerts to specific transit routes
- **Structure**: `event_id` + `route_id` mapping

#### 3. UIS Alert Tagging
- **Feature**: `is_uis_alert` flag on reservations and trip sections
- **Logic**: Determines if reservation/trip is affected by active alerts
- **Application**: Both reservation lists and trip detail views

## Test Data Structure

### Mock Alert Events
```javascript
const mockAlerts = [
  {
    event_id: 12344,
    type: 'TEST',
    effect_name: 'Delay',
    header_text: 'Minor delays on the Red Line...',
    severity: 'Information',
    start: moment.utc().unix(),        // Ongoing
    expires: 0,                       // No expiration
  },
  {
    event_id: 12345,
    effect_name: 'Delay',
    start: moment.utc().unix(),
    expires: moment.utc().add(1, 'month').unix(), // Future expiration
  },
  {
    event_id: 12346,
    start: moment.utc().unix(),
    expires: moment.utc().add(-9, 'minute').unix(), // Expired
  }
];
```

### Route Associations
```javascript
const mockAlertRoutes = [
  { event_id: 12344, route_id: 'ME555' },
  { event_id: 12344, route_id: 'ME666' },
  { event_id: 12345, route_id: 'ME384' },
  { event_id: 12346, route_id: 'ME532' },
];
```

### Test Reservations
- **Travel Modes**: Public Transit, Park & Ride, Intermodal, Biking, Driving
- **Status Types**: Reserved, Canceled
- **Time Ranges**: Future trips, past trips

## Alert Logic Testing

### Affected vs Unaffected Reservations

#### Affected Cases (is_uis_alert: true)
1. **Public Transit + Active Alert**: Route ME384 with ongoing alert
2. **Intermodal + Multiple Alerts**: Multiple transit segments with alerts

#### Unaffected Cases (is_uis_alert: false)  
1. **Expired Alerts**: Route ME532 with expired alert
2. **Non-Transit Modes**: Biking, driving modes
3. **No Route Match**: Transit routes without alerts

### Trip Detail Alert Tagging

#### Multi-Section Trips
```javascript
// Intermodal trip with multiple transit sections
const sections = [
  { type: 'pedestrian', transport: { mode: 'pedestrian' } },
  { 
    type: 'transit', 
    transport: { 
      route_id: 'ME384',  // Has alert
      is_uis_alert: true 
    } 
  },
  { type: 'waiting' },
  { 
    type: 'transit', 
    transport: { 
      route_id: 'ME555',  // Has alert
      is_uis_alert: true 
    } 
  },
  { type: 'pedestrian' }
];
```

## API Endpoints Tested

### 1. Get Reservations with Alert Tags
- **Route**: `getReservations`
- **Method**: GET
- **Response Enhancement**: Adds `is_uis_alert` boolean to each reservation
- **Logic**: Checks if reservation's routes have active alerts

### 2. Get Trip Detail with Alert Tags  
- **Route**: `getTripDetail/:id`
- **Method**: GET
- **Response Enhancement**: Adds `is_uis_alert` to transport objects
- **Granularity**: Per-section alert tagging

## Test Scenarios

### Reservation List Tests
```javascript
it('should return the reservation having the tag of is_uis_alert', async () => {
  const resp = await httpClient.get(url, config);
  const { reservations } = resp.data.data;
  
  expect(reservations[0].is_uis_alert).to.be.eq(true);   // ME384 route
  expect(reservations[1].is_uis_alert).to.be.eq(false);  // ME532 (expired)
  expect(reservations[2].is_uis_alert).to.be.eq(true);   // Intermodal
  expect(reservations[3].is_uis_alert).to.be.eq(false);  // Biking
  expect(reservations[4].is_uis_alert).to.be.eq(false);  // Driving
});
```

### Trip Detail Tests
```javascript
it('should return multiple UIS alert tags for intermodal trip', async () => {
  const sections = await expectedTransportSections(123458);
  
  const transport1 = sections[2].transport;  // ME384
  expect(transport1.is_uis_alert).to.eq(true);
  
  const transport2 = sections[5].transport;  // ME555  
  expect(transport2.is_uis_alert).to.eq(true);
});
```

## Alert State Management

### Active Alert Criteria
1. **Time Validation**: `start <= now < expires` (or expires = 0)
2. **Route Matching**: Route ID exists in alert associations
3. **Status Check**: Alert is not marked as resolved

### Alert Types Supported
- **Service Delays**: Minor/major delays
- **Route Detours**: Temporary route changes
- **Service Disruptions**: Partial/complete service interruptions
- **Maintenance Alerts**: Planned service changes

## Data Relationships

### Alert-Route-Reservation Chain
```
TransitAlert (event_id) 
    ↓
TransitAlertRoute (event_id + route_id)
    ↓  
TripDetail.steps[].transport.route_id
    ↓
Reservation (affected via trip_detail_uuid)
```

### Trip Section Structure
```javascript
const tripStep = {
  type: 'transit',
  transport: {
    route_id: 'ME384',
    mode: 'bus',
    name: '384',
    category: 'Bus',
    is_uis_alert: true  // Added by alert logic
  }
};
```

## Performance Considerations

### Alert Processing
- **Real-time Evaluation**: Alerts checked against current time
- **Route Lookup**: Efficient route-alert association queries
- **Caching Strategy**: Alert data cached for performance

### Data Volume
- **Multiple Alerts**: Handles concurrent alerts on same route
- **Multi-Modal Trips**: Processes multiple transit sections
- **Historical Data**: Manages expired alerts appropriately

## Error Handling

### Alert System Failures
- **Graceful Degradation**: System continues without alert tags
- **Default Values**: `is_uis_alert: false` when uncertain
- **Logging**: Alert processing errors logged for monitoring

## Integration Points

### External Systems
- **Transit Agencies**: Alert data feeds
- **UIS Platform**: Urban information system integration
- **Route Planning**: Trip planning with alert awareness

### Internal Dependencies
- **Reservation System**: Core reservation functionality
- **Trip Planning**: Intermodal route calculation
- **User Notifications**: Alert-based user messaging

## Usage in Production

### User Experience
- **Visual Indicators**: UI shows alert status on trips
- **Detailed Information**: Users can access full alert details
- **Alternative Options**: System can suggest alert-free routes

### Operations Management
- **Service Monitoring**: Track alert impact on reservations
- **Performance Metrics**: Measure alert processing efficiency
- **Data Quality**: Validate alert data accuracy

This test suite ensures that the UIS alert integration correctly identifies affected reservations and trip sections, providing users with real-time service disruption information.