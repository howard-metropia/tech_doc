# incentive-notify.js

## Overview
Job for processing and sending incentive notifications to users based on scheduled delivery times. Handles notification queue processing and delivery status updates for incentive-related communications.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/incentive-notify.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `@app/src/services/incentiveUtility` - Incentive utility functions
- `@maas/core/log` - Logging utility
- `@maas/core/mysql` - MySQL database connection (portal)
- `moment-timezone` - Timezone-aware date handling
- `@app/src/services/bingocard` - Bingo card challenge functions

## Core Functions

### getIncentiveNotifyUsers()
Retrieves users from the notification queue who are ready to receive incentive notifications.

**Query Conditions:**
- `deliver_time <= currentUTC` - Scheduled delivery time has passed
- `deliver = 0` - Not yet delivered
- `purpose = 'incentive'` - Incentive-related notifications only

**Returns:** Array of notification records from `incentive_notify_queue`

### executeNotify(notifyUsers)
Processes and sends notifications to queued users.

**Process Flow:**
1. Iterate through notification users
2. Extract user IDs and notification IDs
3. Format notification message (empty title, content from msg_content)
4. Send notification using utility function
5. Update delivery status for processed notifications

**Parameters:**
- `notifyUsers` - Array of notification records

### sleep(sec)
Utility function for introducing delays in processing.

**Parameters:**
- `sec` - Number of seconds to sleep

**Returns:** Promise that resolves after specified time

## Job Configuration

### Inputs
No input parameters required.

### Main Function
Processes incentive notification queue and delivers pending notifications.

## Processing Flow

### 1. Queue Retrieval
```javascript
const notifyUsers = await getIncentiveNotifyUsers();
```

### 2. Notification Processing
For each queued notification:
- Extract user_id and queue record id
- Format notification message
- Send notification to user
- Track processed IDs for status update

### 3. Status Update
- Update delivery status for all processed notifications
- Mark notifications as delivered (`deliver = 1`)

## Data Models

### incentive_notify_queue Table
```javascript
{
  id: number,
  user_id: number,
  deliver_time: datetime,
  deliver: number, // 0 = pending, 1 = delivered
  purpose: string, // 'incentive'
  msg_content: string,
  // Additional fields...
}
```

### Notification Message Format
```javascript
{
  title: string, // Empty for incentive notifications
  body: string   // From msg_content field
}
```

## Business Logic

### Delivery Timing
- Uses UTC timestamps for consistent scheduling
- Processes only notifications with past delivery times
- Prevents duplicate deliveries with status flag

### Batch Processing
- Processes all eligible notifications in single execution
- Collects user IDs and notification IDs for batch updates
- Updates delivery status after successful processing

### Message Formatting
- Uses empty title for incentive notifications
- Message body comes from database msg_content field
- Supports personalized content per user

## Error Handling
- Try-catch block around challenge addition (commented out)
- Detailed error logging with stack traces
- Graceful continuation if errors occur

## Integration Points
- Incentive utility service for notification sending
- Notification queue management system
- Challenge/bingo card system (future integration)
- Status tracking system

## Performance Considerations
- Single query to retrieve all eligible notifications
- Batch status updates to minimize database operations
- Efficient array processing for user collections

## Commented Features
Currently includes commented code for:
- Sleep delay functionality
- Challenge addition integration
- Future bingo card system integration

## Usage Scenarios
- Scheduled incentive notification delivery
- Daily/hourly notification processing
- User engagement campaigns
- Points and rewards communications

## Logging
- Error logging for challenge addition failures
- Stack trace logging for debugging
- Processing status tracking

## Notes
- Designed for scheduled execution
- Supports timezone-aware delivery scheduling
- Ready for integration with challenge systems
- Focuses on incentive-specific notifications only