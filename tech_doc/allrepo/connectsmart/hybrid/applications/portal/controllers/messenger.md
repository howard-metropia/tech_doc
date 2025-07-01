# Messenger Controller API Documentation

## Overview
The Messenger Controller manages notification delivery and messaging functionality in the MaaS platform. It provides comprehensive notification management including delivery status tracking, administrative controls, and user notification preferences.

**File Path:** `/allrepo/connectsmart/hybrid/applications/portal/controllers/messenger.py`

**Controller Type:** Mixed Authentication Portal Controller

**Authentication:** JWT for user endpoints, Login for admin endpoints

## Features
- User notification retrieval with pagination
- Administrative notification management and bulk operations
- Notification status tracking and delivery confirmation
- Message filtering and categorization
- Real-time notification updates
- Comprehensive notification lifecycle management

## API Endpoints

### User Notifications
**Endpoint:** `/messenger/notification`
**Methods:** GET, PUT
**Authentication:** Mixed (JWT for GET, Login for PUT)

#### GET - Retrieve User Notifications
Retrieves notifications for the authenticated user with filtering and pagination.

**Parameters:**
- `offset` (optional): Starting offset for pagination (default: 0)
- `perpage` (optional): Items per page (default: 10)

**Response Format:**
```json
{
  "success": true,
  "data": {
    "notifications": [
      {
        "id": 12345,
        "type": 10,
        "title": "Carpool Match Found",
        "body": "A new carpool match is available for your trip",
        "data": {
          "group_id": 456,
          "reservation_id": 789,
          "match_user_id": 123
        },
        "started_on": "2024-01-15T08:00:00Z",
        "send_status": 3,
        "silent": false
      }
    ],
    "total_count": 25,
    "next_offset": 10
  }
}
```

**Notification Types Excluded:**
- Microsurvey first time notes
- Multiple choice question surveys

**Send Status Values:**
- `0`: Queued
- `1`: Send failed
- `2`: Sent
- `3`: Received

**Status Codes:**
- `200`: Success
- `400`: Invalid parameters

#### PUT - Update Notification End Time (Admin)
Updates the end time for a specific notification (administrative function).

**Authentication:** Login required, Metropia role

**URL Parameter:**
- `notification_id`: Notification ID to update

**Required Fields:**
- `ended_on`: ISO 8601 datetime string for notification end time

**Request Example:**
```json
{
  "ended_on": "2024-01-15T18:00:00Z"
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "updated": 1
  }
}
```

**Status Codes:**
- `200`: Successfully updated
- `400`: Invalid parameters
- `404`: Notification not found

### Bulk Notification Management
**Endpoint:** `/messenger/notifications`
**Methods:** PUT
**Authentication:** Login required, Metropia role

#### PUT - Bulk Update Notifications
Updates end time for multiple notifications simultaneously.

**Required Fields:**
- `notification_ids`: Array of notification IDs
- `ended_on`: ISO 8601 datetime string for end time

**Request Example:**
```json
{
  "notification_ids": [12345, 12346, 12347],
  "ended_on": "2024-01-15T18:00:00Z"
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "updated": 3
  }
}
```

**Status Codes:**
- `200`: Successfully updated
- `400`: Invalid parameters

### Notification Receipt Confirmation
**Endpoint:** `/messenger/receive`
**Methods:** PUT
**Authentication:** JWT token required

#### PUT - Confirm Notification Receipt
Marks a notification as received by the user.

**URL Parameter:**
- `notification_id`: Notification ID to mark as received

**Response Format:**
```json
{
  "success": true
}
```

**Special Handling:**
- **DUO Broadcasting (Type 70)**: Marked as "replied" instead of "received"
- **Standard Notifications**: Marked as "received"

**Status Codes:**
- `200`: Successfully updated
- `400`: Invalid parameters
- `404`: Notification not found

## Data Models

### Notification Structure
```python
{
    "id": int,                          # Notification identifier
    "type": int,                        # Notification type code
    "title": str,                       # Notification title
    "body": str,                        # Notification message body
    "data": dict,                       # Additional notification data
    "started_on": datetime,             # Notification start time
    "ended_on": datetime,               # Notification end time
    "send_status": int,                 # Delivery status
    "silent": bool                      # Silent notification flag
}
```

### Notification Types
Common notification types in the system:
- **Carpool Matching**: Match found, ride requests, confirmations
- **Group Management**: Join requests, invitations, updates
- **Payment**: Transaction confirmations, payment failures
- **System**: App updates, maintenance notifications
- **DUO Broadcasting (70)**: Special broadcast messages

### Send Status Codes
```python
NOTIFY_STATUS_QUEUE = 0         # Queued for delivery
NOTIFY_STATUS_SEND_FAIL = 1     # Delivery failed
NOTIFY_STATUS_SENT = 2          # Successfully sent
NOTIFY_STATUS_RECEIVED = 3      # Received by user
NOTIFY_STATUS_REPLIED = 4       # User replied/interacted
```

## Database Schema

### Core Tables
- **notification**: Main notification metadata
- **notification_msg**: Notification message content
- **notification_user**: User-specific notification delivery data

### Query Structure
```sql
SELECT * FROM notification_user nu
JOIN notification_msg nm ON nu.notification_msg_id = nm.id
JOIN notification n ON nm.notification_id = n.id
WHERE nu.user_id = ? 
  AND n.ended_on >= NOW()
  AND nu.send_status IN (0, 1, 2, 3)
ORDER BY n.id DESC
```

## Message Data Handling

### JSON Data Processing
```python
try:
    data = json.loads(row.notification.msg_data)
except TypeError:
    data = row.notification.msg_data  # Fallback for non-JSON data
```

### Data Structure Examples
```json
{
  "carpool_data": {
    "group_id": 456,
    "reservation_id": 789,
    "match_user_id": 123,
    "pickup_location": "Downtown Station",
    "departure_time": "2024-01-15T08:00:00Z"
  },
  "group_data": {
    "group_id": 456,
    "group_name": "Downtown Commuters",
    "action": "join_request",
    "requester_name": "John Doe"
  }
}
```

## Administrative Functions

### Notification Lifecycle Management
Administrators can control notification visibility and lifecycle:
- **End Time Updates**: Set when notifications expire
- **Bulk Operations**: Manage multiple notifications simultaneously
- **Status Tracking**: Monitor delivery and engagement metrics

### Hide Notification API
```python
hide_notification_api(db, notification_ids, ended_on=ended_on)
```

This function:
- Updates notification end times
- Prevents further delivery attempts
- Maintains audit trail of changes

## Authentication and Authorization

### User Endpoints (JWT)
- `@auth.allows_jwt()`: JWT token validation
- `@jwt_helper.check_token()`: Token integrity verification
- User-scoped data access (users see only their notifications)

### Administrative Endpoints (Login)
- `@auth.requires_login()`: Session-based authentication
- `@auth.requires_membership('Metropia')`: Role-based access control
- System-wide notification management capabilities

## Error Handling

### Parameter Validation
```python
try:
    notification_id = int(notification_id)
    ended_on = string_to_datetime(fields['ended_on'])
except (ValueError, TypeError, KeyError):
    response.status = 400
    return json_response.fail(ERROR_BAD_REQUEST_PARAMS, T('Invalid parameters'))
```

### Error Codes
- `ERROR_BAD_REQUEST_PARAMS`: Invalid URL parameters
- `ERROR_BAD_REQUEST_BODY`: Invalid request body
- `ERROR_NOTIFICATION_NOT_FOUND`: Notification does not exist

### Error Response Format
```json
{
  "success": false,
  "error_code": "ERROR_NOTIFICATION_NOT_FOUND",
  "message": "Notification not found"
}
```

## Special Notification Handling

### DUO Broadcasting (Type 70)
Special handling for broadcast notifications:
```python
if row.notification.notification_type == 70:
    row.notification_user.update_record(send_status=notif.NOTIFY_STATUS_REPLIED)
    logger.debug('[DUO] Broadcasting notification id: %d is replied' % notification_id)
```

### Microsurvey Filtering
Excludes survey notifications from user notification lists:
```python
~db.notification.notification_type.belongs([
    notif.MICROSURVEY_FIRST_TIME_NOTE,
    notif.MICROSURVEY_MULTIPLE_CHOICE_QUESTION
])
```

## Usage Examples

### Retrieve User Notifications
```bash
curl -X GET "/messenger/notification?offset=0&perpage=20" \
  -H "Authorization: Bearer <jwt_token>"
```

### Mark Notification as Received
```bash
curl -X PUT "/messenger/receive/12345" \
  -H "Authorization: Bearer <jwt_token>"
```

### Admin: Update Notification End Time
```bash
curl -X PUT "/messenger/notification/12345" \
  -H "Cookie: session_token=<session>" \
  -H "Content-Type: application/json" \
  -d '{"ended_on": "2024-01-15T18:00:00Z"}'
```

### Admin: Bulk Update Notifications
```bash
curl -X PUT "/messenger/notifications" \
  -H "Cookie: session_token=<session>" \
  -H "Content-Type: application/json" \
  -d '{
    "notification_ids": [12345, 12346, 12347],
    "ended_on": "2024-01-15T18:00:00Z"
  }'
```

## Integration Points

### Push Notification Systems
- Firebase Cloud Messaging (FCM) for mobile apps
- Apple Push Notification Service (APNS) for iOS
- Web push notifications for browser clients
- SMS and email fallback channels

### Carpool System Integration
- Match found notifications
- Ride request confirmations
- Trip status updates
- Payment confirmations

### Group Management Integration
- Join request notifications
- Group updates and announcements
- Administrative actions
- Member activity alerts

## Performance Optimization

### Query Optimization
- Indexed notification lookups by user and date
- Pagination to limit result set size
- Filtered queries to exclude expired notifications
- Efficient join operations across notification tables

### Caching Strategy
- User notification count caching
- Frequently accessed notification templates
- Status lookup optimizations

## Monitoring and Analytics

### Key Metrics
- Notification delivery success rates
- User engagement with notifications
- Administrative action frequency
- System performance metrics

### Delivery Tracking
```python
logger.debug('Update the notification: %s, ended_on=%s' % (notification_id, ended_on))
logger.debug('[DUO] Broadcasting notification id: %d is replied' % notification_id)
```

## Security Considerations

### Data Privacy
- User-scoped notification access
- Secure handling of notification content
- Audit trails for administrative actions
- Minimal data exposure in responses

### Input Validation
- Comprehensive parameter validation
- SQL injection prevention through ORM
- XSS protection in notification content
- Authorization checks for all operations

## Future Enhancements

### Planned Features
- **Real-time Delivery**: WebSocket-based instant notifications
- **Rich Media**: Support for images and interactive content
- **Personalization**: AI-driven notification preferences
- **Analytics Dashboard**: Comprehensive delivery and engagement metrics

### Scalability Improvements
- **Message Queuing**: Asynchronous notification processing
- **Service Decomposition**: Dedicated notification microservice
- **Global Distribution**: Multi-region notification delivery
- **Performance Optimization**: Advanced caching and database optimization