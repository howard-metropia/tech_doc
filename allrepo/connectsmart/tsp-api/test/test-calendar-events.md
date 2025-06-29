# Calendar Events API Test Suite

## Overview
Comprehensive test suite for the Calendar Events API, validating CRUD operations for user calendar event management. Tests calendar event creation, updates, deletion, and data synchronization with MongoDB storage.

## File Purpose
- **Primary Function**: Test calendar event management operations
- **Type**: Integration test suite
- **Role**: Validates calendar event CRUD operations and data integrity

## Test Configuration

### Test Setup
- **Framework**: Mocha with Chai assertions
- **HTTP Testing**: Supertest for API endpoint testing
- **Database**: MongoDB for calendar event storage
- **Test User**: User ID 1003
- **Timeout**: 10-second timeout for complex operations

### Dependencies
- `@maas/core/bootstrap`: Application bootstrapping
- `@maas/core/api`: API application factory
- `@maas/core`: Router and core utilities
- `CalendarEvents`: MongoDB model for calendar events
- `supertest`: HTTP assertion library
- `chai`: Assertion library

## Test Data Structure

### Sample Destination
```javascript
const destination = {
  name: 'The Museum of Fine Arts, Houston',
  address: '1001 Bissonnet St, Houston, TX 77005 US',
  latitude: 29.6704173,
  longitude: -95.4768428
};
```

### Sample Calendar Events
```javascript
const calendarEvents = {
  events: [
    {
      uuid: '-1',
      title: 'TEST from Android',
      arrival_time: '2022-07-01T15:00:00Z',
      destination: destination,
      reminder_time: 1656662400,
      platform: 'Android',
      is_removed: false
    },
    {
      uuid: '5c6c3ea59dd6b62e79661180',
      title: 'TEST from iOS',
      arrival_time: '2022-07-01T15:00:00Z',
      destination: destination,
      reminder_time: 1656662400,
      platform: 'iOS',
      is_removed: false
    }
  ]
};
```

## Test Scenarios

### POST /calendars - Calendar Event Creation

#### Test Case 1: Create Multiple Calendar Events
**Purpose**: Test bulk calendar event creation
**Input**: Array of 2 calendar events (Android and iOS)
**Expected Response**:
```javascript
{
  "result": "success",
  "data": {
    "upsertedCount": 2,
    "modifiedCount": 0,
    "removedCount": 0
  }
}
```

**Validation Steps**:
1. Submit calendar events array
2. Verify success response
3. Confirm 2 events created, 0 modified, 0 removed
4. Validate response includes operation counts

#### Test Case 2: Update Existing and Create New Events
**Purpose**: Test mixed upsert operations
**Input**: Modified existing events + 1 new event
**Expected Response**:
```javascript
{
  "upsertedCount": 1,
  "modifiedCount": 2,
  "removedCount": 0
}
```

**Process**:
1. Modify reminder_time for existing events
2. Add new event to events array
3. Submit updated events collection
4. Verify correct upsert counts

#### Test Case 3: Remove All Calendar Events
**Purpose**: Test bulk event removal
**Input**: Empty events array
**Expected Response**:
```javascript
{
  "upsertedCount": 0,
  "modifiedCount": 0,
  "removedCount": 3
}
```

**Validation**:
- All existing events marked as removed
- No new events created or modified
- Proper cleanup of user calendar data

### PUT /calendars/{id} - Calendar Event Updates

#### Test Case 1: Update Calendar Event by ID
**Purpose**: Test individual event modification
**Input**: Modified event title
**Expected Behavior**:
- Event updated successfully
- Response contains updated event data
- All event properties preserved except modified fields

**Response Properties**:
```javascript
[
  'destination',
  'arrival_time',
  'is_removed',
  'platform',
  'reminder_time',
  'title'
]
```

### DELETE /calendars/{id} - Calendar Event Deletion

#### Test Case 1: Delete Calendar Event by ID
**Purpose**: Test individual event removal
**Expected Response**:
- Success result with empty data
- Event marked as removed in database
- No impact on other user events

## Error Handling Test Cases

### Authentication Errors (Code 10004)

#### Missing User ID Header
**Trigger**: Request without userid header
**Response**:
```javascript
{
  "result": "fail",
  "error": {
    "code": 10004,
    "msg": "Request header has something wrong"
  }
}
```

**Affected Endpoints**:
- POST /calendars
- PUT /calendars/{id}
- DELETE /calendars/{id}

### Validation Errors (Code 10002)

#### Missing Required Fields
**POST /calendars without events**:
```javascript
{
  "error": {
    "code": 10002,
    "msg": "\"events\" is required"
  }
}
```

**PUT /calendars/{id} with invalid fields**:
```javascript
{
  "error": {
    "code": 10002,
    "msg": "\"fakeKey\" is not allowed"
  }
}
```

### Data Not Found Errors (Code 20001)

#### Invalid Event ID
**Trigger**: Operations on non-existent event IDs
**Response**:
```javascript
{
  "result": "fail",
  "error": {
    "code": 20001,
    "msg": "Data not found"
  }
}
```

**Affected Operations**:
- PUT /calendars/{fakeId}
- DELETE /calendars/{nonExistentId}

## Database Operations

### MongoDB Integration
- **Model**: CalendarEvents MongoDB model
- **Operations**: Upsert, update, delete operations
- **Filtering**: User-specific event management

### Data Lifecycle
```javascript
// Test setup
before('Connect MongoDB', async () => {});

// Test cleanup
after('Delete testing data', async () => {
  await CalendarEvents.deleteMany({
    userId: userid
  });
});
```

### Upsert Logic
- **Create**: New events with unique UUIDs
- **Update**: Existing events identified by UUID
- **Remove**: Events not in submitted array

## API Endpoint Details

### Authentication Requirements
- **Header**: `userid` required for all operations
- **Content-Type**: `application/json`
- **User Context**: Operations scoped to authenticated user

### URL Patterns
- **Create Events**: `POST /calendars`
- **Update Event**: `PUT /calendars/{uuid}`
- **Delete Event**: `DELETE /calendars/{uuid}`

### Request/Response Format

#### Event Data Structure
```javascript
{
  "uuid": "string",
  "title": "string",
  "arrival_time": "ISO 8601 datetime",
  "destination": {
    "name": "string",
    "address": "string",
    "latitude": number,
    "longitude": number
  },
  "reminder_time": number,
  "platform": "Android|iOS",
  "is_removed": boolean
}
```

## Platform Support

### Cross-Platform Compatibility
- **Android**: Native Android calendar integration
- **iOS**: Native iOS calendar integration
- **Platform Field**: Tracks event source platform

### UUID Management
- **Android**: Negative integer UUIDs (-1, -2, etc.)
- **iOS**: MongoDB ObjectId format
- **Uniqueness**: Platform-specific UUID generation

## Time Zone Handling

### Timestamp Formats
- **arrival_time**: ISO 8601 UTC format
- **reminder_time**: Unix timestamp
- **Time Zone**: Server-side conversion handling

### Reminder Logic
- **Scheduling**: Based on reminder_time timestamp
- **Notifications**: Platform-specific notification delivery
- **Time Accuracy**: Precise timing for user alerts

## Performance Considerations

### Bulk Operations
- **Batch Processing**: Multiple events in single request
- **Upsert Efficiency**: Minimize database round trips
- **Index Usage**: UUID-based event lookup

### MongoDB Optimization
- **User Indexing**: userId field indexing
- **UUID Indexing**: Fast event identification
- **Query Optimization**: Efficient upsert operations

## Integration Points

### Calendar Services
- **Native Calendars**: Platform calendar synchronization
- **Event Reminders**: System notification integration
- **Location Services**: Destination coordinate validation

### User Experience
- **Cross-Device Sync**: Event synchronization across devices
- **Offline Support**: Local storage and sync capabilities
- **Conflict Resolution**: Handling concurrent modifications

## Test Environment Setup

### MongoDB Configuration
- **Test Database**: Isolated test environment
- **Data Cleanup**: Automatic test data removal
- **Connection Management**: Proper connection handling

### Mock Data Strategy
- **Realistic Data**: Houston museum destination
- **Varied Scenarios**: Different platforms and times
- **Edge Cases**: Boundary condition testing

## Security Considerations

### Data Privacy
- **User Isolation**: Events scoped to authenticated user
- **Data Validation**: Input sanitization and validation
- **Access Control**: User-specific data access

### Location Data
- **Coordinate Validation**: Latitude/longitude bounds
- **Address Privacy**: Secure address handling
- **Destination Security**: Safe location data storage

## Maintenance Notes

### Test Data Maintenance
- **Realistic Destinations**: Keep test locations current
- **Time Stamps**: Update test dates as needed
- **UUID Formats**: Maintain platform-specific formats

### API Evolution
- **Field Additions**: Test new event properties
- **Platform Support**: Add new platform testing
- **Performance Monitoring**: Track operation efficiency

### Future Enhancements
- **Recurring Events**: Test repeating calendar events
- **Event Categories**: Test event classification
- **Shared Events**: Test multi-user event sharing
- **Calendar Integration**: Test external calendar sync