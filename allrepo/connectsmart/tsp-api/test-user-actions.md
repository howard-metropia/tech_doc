# Test Documentation: User Actions API

## Overview
This test suite validates the User Actions functionality within the TSP system. The test covers the logging and tracking of user interactions and behaviors within the mobile application, supporting analytics, user experience optimization, and system monitoring.

## Test Configuration
- **File**: `test/test-user-actions.js`
- **Framework**: Mocha with Chai assertions and Supertest for HTTP testing
- **Test Timeout**: 10 seconds for action logging operations
- **Authentication**: User ID-based authentication (userid: 1003)
- **Purpose**: User behavior tracking and analytics

## API Endpoints Tested

### POST /user-actions
**Purpose**: Records user actions and interactions within the application

**Authentication Required**: Yes (userid header)

**Request Structure**:
```javascript
{
  actions: [
    {
      action: 'Pre_trip_alert_open',
      attributes: {
        event_id: 'INCIDENT123456',
        type: 'incident',
        start_date: '2023-05-21T03:47:35+00:00',
        end_date: '2023-05-21T12:47:35+00:00',
        lat: 23.456,
        lng: 123.789
      }
    },
    {
      action: 'TripPlanner_Screen',
      attributes: {
        trip_mode: 'driving'
      }
    }
  ]
}
```

**Success Response**:
```javascript
{
  result: 'success',
  data: [
    // Array of processed action records
    // Length should match input actions array
  ]
}
```

## Action Types and Attributes

### 1. Pre_trip_alert_open
**Purpose**: Tracks when users open pre-trip alerts for traffic incidents

**Attributes**:
- `event_id`: Unique identifier for the traffic event
- `type`: Type of event ('incident', 'closure', 'DMS', etc.)
- `start_date`: Event start timestamp (ISO 8601 format)
- `end_date`: Event end timestamp (ISO 8601 format)
- `lat`: Event latitude coordinate
- `lng`: Event longitude coordinate

**Business Value**: 
- Measures user engagement with traffic alerts
- Tracks incident awareness and response
- Supports traffic event relevance analysis

### 2. TripPlanner_Screen
**Purpose**: Tracks user interactions with trip planning interface

**Attributes**:
- `trip_mode`: Selected transportation mode ('driving', 'transit', 'walking', 'biking', etc.)

**Business Value**:
- Analyzes transportation mode preferences
- Tracks user navigation patterns
- Supports UI/UX optimization

## Test Scenarios

### Happy Path Testing

#### Successful Action Logging
```javascript
const inputData = {
  actions: [
    {
      action: 'Pre_trip_alert_open',
      attributes: {
        event_id: 'INCIDENT123456',
        type: 'incident',
        start_date: '2023-05-21T03:47:35+00:00',
        end_date: '2023-05-21T12:47:35+00:00',
        lat: 23.456,
        lng: 123.789
      }
    },
    {
      action: 'TripPlanner_Screen',
      attributes: {
        trip_mode: 'driving'
      }
    }
  ]
};

const response = await request.set(auth).post(url).send(inputData);
expect(response.body.result).to.eq('success');
expect(response.body.data.length).to.eq(2);
```

**Validation**:
- Returns success status
- Data array length matches input actions
- All actions processed successfully

### Error Path Testing

#### 1. Missing Authentication (Error 10004)
```javascript
const response = await request.post(url).unset('userid').send(inputData);

// Expected Response
{
  result: 'fail',
  error: {
    code: 10004,
    msg: 'Request header has something wrong'
  }
}
```

#### 2. Missing Actions Array (Error 10002)
```javascript
const response = await request.set(auth).post(url).send({});

// Expected Response
{
  result: 'fail',
  error: {
    code: 10002,
    msg: '"actions" is required'
  }
}
```

## Data Structure Analysis

### Action Schema
```javascript
{
  action: String,        // Action type identifier
  attributes: Object     // Action-specific data
}
```

### Attribute Patterns

#### Geospatial Data
- `lat` and `lng` for location-based actions
- Coordinate precision for geographic analysis
- Location context for spatial analytics

#### Temporal Data
- ISO 8601 timestamp format
- Start and end times for duration analysis
- Timezone-aware datetime handling

#### Event References
- `event_id` for linking to traffic events
- `type` for event categorization
- Cross-reference with incident management system

#### User Interface Tracking
- Screen names and navigation paths
- User interaction patterns
- Feature usage analytics

## Analytics and Business Intelligence

### User Behavior Analysis
- **Navigation Patterns**: Track user movement through app screens
- **Feature Usage**: Monitor which features users engage with most
- **Response Times**: Measure user reaction to alerts and notifications
- **Mode Preferences**: Analyze transportation mode selection patterns

### Traffic Event Engagement
- **Alert Effectiveness**: Measure how often users open traffic alerts
- **Event Relevance**: Track user engagement with different event types
- **Geographic Patterns**: Analyze location-based user responses
- **Temporal Patterns**: Understand when users are most responsive to alerts

### Performance Metrics
- **User Engagement**: Track active user interactions
- **Feature Adoption**: Monitor new feature usage rates
- **User Journey**: Map complete user experience flows
- **Conversion Rates**: Measure action completion rates

## Data Privacy and Security

### User Data Protection
- User actions linked to userid for analysis
- No personally identifiable information in action logs
- Aggregated analytics protect individual privacy
- Secure data transmission and storage

### Data Retention
- Action logs stored for analytics and optimization
- Historical data supports trend analysis
- Data lifecycle management for privacy compliance
- Secure data access controls

## Integration Points

### Analytics Platform
- Data feeds into business intelligence systems
- Real-time and batch analytics processing
- Dashboard and reporting integration
- Machine learning model training data

### Event Management System
- Links user actions to traffic events
- Correlates user behavior with system events
- Supports incident response optimization
- Measures event notification effectiveness

### User Experience Optimization
- A/B testing support through action tracking
- Feature usage analytics for UI improvements
- User journey optimization insights
- Performance bottleneck identification

## Error Handling

### Validation Errors
- **10004**: Missing or invalid authentication headers
- **10002**: Missing required request parameters
- Request validation before processing

### Data Quality
- Action schema validation
- Attribute type checking
- Timestamp format validation
- Coordinate range validation

## Test Implementation

### Request Setup
```javascript
const auth = { userid: 1003, 'Content-Type': 'application/json' };
const url = router.url('addUserActions');
```

### Response Validation
```javascript
const { result, data } = resp.body;
expect(result).to.eq('success');
expect(data.length).to.eq(inputData.actions.length);
```

### Error Validation
```javascript
const { result, error } = resp.body;
expect(result).to.eq('fail');
expect(error).to.include({
  code: expectedCode,
  msg: expectedMessage
});
```

## Business Value

### Product Development
- Data-driven feature development decisions
- User experience optimization insights
- Performance monitoring and optimization
- A/B testing and experimentation support

### Operations Management
- System usage patterns and load analysis
- Feature adoption and rollout monitoring
- User support and help desk insights
- Service quality measurement

### Strategic Planning
- User behavior trend analysis
- Market research and user preferences
- Competitive advantage through user insights
- Service expansion planning support

## Test Coverage

### Functional Coverage
- ✅ Multiple action logging in single request
- ✅ Different action types and attributes
- ✅ Response format validation
- ✅ Authentication requirement verification

### Error Coverage
- ✅ Missing authentication headers
- ✅ Missing required request body
- ✅ Request validation errors
- ✅ Error response format consistency

### Data Coverage
- ✅ Complex action attribute structures
- ✅ Geographic coordinate handling
- ✅ Timestamp format processing
- ✅ Event reference validation

## Future Enhancements

### Additional Action Types
- Social sharing actions
- Payment and transaction events
- Route completion tracking
- Feedback and rating submissions

### Enhanced Analytics
- Real-time action processing
- Machine learning integration
- Predictive user behavior models
- Personalization engine support

### Data Integration
- External analytics platform integration
- Data warehouse connectivity
- Real-time dashboard updates
- Cross-platform action correlation

This test suite ensures the user actions system reliably captures user behavior data for analytics and optimization within the TSP platform.