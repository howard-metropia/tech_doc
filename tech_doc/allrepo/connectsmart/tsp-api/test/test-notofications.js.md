# test-notofications.js

## Overview
Comprehensive test suite for the notification system in the TSP API. Tests notification retrieval, status updates, categorization, and the notification sending helper functionality.

## File Location
`/test/test-notofications.js`

## Dependencies
- **@maas/core**: Core MaaS framework components
- **supertest**: HTTP assertions for API testing
- **chai**: BDD/TDD assertion library
- **Models**: NotificationUsers, NotificationMsgs, Notifications, NotificationTypes
- **Helpers**: authToken, send-notification

## Test Structure

### Main Test Suite: Notification

#### Test Data Setup
```javascript
const userid = 1003;
const notificationType = 1;
const originalNotificationId = 1001;
```

#### Authentication Configuration
- User ID: 1003
- JWT Bearer token authentication
- Content-Type: application/json
- Timezone: America/Chicago

### Test Categories

#### 1. Get Notifications
**Endpoint**: `getNotification`

**Test Cases**:
- **Basic Retrieval**: Get notifications with pagination
  - Verifies response structure (total_count, next_offset, notifications)
  - Tests offset and perpage parameters
- **Pagination Edge Cases**: Test with offset at total count
- **Authentication Errors**: 
  - Missing token (error 10003)
  - Invalid parameters (error 10001)

#### 2. Update Notification Status
**Endpoint**: `updateNotification`

**Test Cases**:
- **Status Update**: Mark notification as read
- **Authentication Validation**: Token required checks
- **Parameter Validation**: ID must be numeric
- **Non-existent ID Handling**: Graceful handling of invalid IDs

#### 3. Status and Filtering Tests
**Status Values**:
- 1, 2: Unread states
- 3: Default/delivered state
- 5: Read state

**Filter Tests**:
- Status filtering (status: '3,5')
- Type filtering (type: '1')
- Combined status and type filtering

### Special Test Suite: MET-15555

#### Category-Based Notification Testing
**Categories**:
- **General**: Default notification type (type 1)
- **Incentive**: Bingo/badge/tier notifications (type 101)

**Test Cases**:
- Default behavior (returns general notifications)
- Explicit general category filtering
- Null category handling
- Incentive category filtering

### Notification Helper Testing

#### Send Notification Function
**Test Cases**:
- **Complete Parameters**: userIds, titleParams, bodyParams, type, meta, silent, image
- **Optional Image**: Test without image parameter
- **Return Value Validation**: Returns object with user IDs as keys

## Database Models Integration

### Model Relationships
```
Notifications (1) -> (N) NotificationMsgs
NotificationMsgs (1) -> (N) NotificationUsers
NotificationTypes (1) -> (N) Notifications
```

### Test Data Management
- **Before Hook**: Creates test notifications, messages, and user associations
- **After Hook**: Cleans up all test data to prevent interference
- **Proper Cleanup**: Deletes in correct order to maintain referential integrity

## API Response Format

### Success Response
```json
{
  "result": "success",
  "data": {
    "total_count": 10,
    "next_offset": 10,
    "notifications": [...]
  }
}
```

### Error Response
```json
{
  "result": "fail",
  "error": {
    "code": 10001,
    "msg": "Validation error message"
  }
}
```

## Error Codes Tested
- **10001**: Validation error (invalid parameter types)
- **10003**: Authentication error (token required)

## Key Features Tested

### 1. Pagination System
- Offset-based pagination
- Per-page limits
- Total count tracking
- Next offset calculation

### 2. Status Management
- Read/unread status tracking
- Status filtering capabilities
- Status update functionality

### 3. Categorization
- General vs. incentive notifications
- Type-based filtering
- Category parameter handling

### 4. Authentication & Authorization
- JWT token validation
- User-specific notification retrieval
- Proper error handling for unauthorized access

## Business Logic Validation

### Notification Lifecycle
1. **Creation**: Notifications created with default status
2. **Delivery**: Status updated to delivered (3)
3. **Reading**: Status updated to read (5)
4. **Filtering**: Retrieved based on status and type

### User Experience Features
- **Unread Counts**: Total count includes status filtering
- **Category Separation**: General notifications vs. incentive notifications
- **Real-time Updates**: Status changes reflected immediately

## Testing Best Practices

### Data Isolation
- Unique test user ID (1003)
- Proper setup and teardown
- No interference between test cases

### Comprehensive Coverage
- Happy path scenarios
- Error conditions
- Edge cases (empty results, invalid parameters)
- Authentication and authorization

### Helper Function Testing
- Direct testing of send-notification utility
- Parameter validation
- Return value verification

## Integration Points

### External Dependencies
- **Database**: MySQL for notification data
- **Authentication**: JWT token system
- **Routing**: Named route handling

### Model Operations
- **Create**: Insert test data
- **Read**: Query with filtering and pagination
- **Update**: Status modifications
- **Delete**: Cleanup operations

This test suite ensures the notification system works correctly across all user interactions, maintains data integrity, and provides proper error handling for the TSP API's communication features.