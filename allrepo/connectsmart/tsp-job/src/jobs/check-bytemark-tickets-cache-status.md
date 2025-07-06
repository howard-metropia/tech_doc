# check-bytemark-tickets-cache-status.js

## Overview
Job for checking and updating Bytemark ticket cache status based on expiration times and usage patterns. Monitors cached ticket passes and updates their status from USABLE to USING to EXPIRED based on timestamps.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/check-bytemark-tickets-cache-status.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with inputs and async function

## Key Dependencies
- `@app/src/models/BytemarkTickets` - Bytemark tickets cache model
- `@app/src/models/BytemarkCacheStatusCheckLog` - Status check logging model
- `@maas/core/log` - Logging utility
- `moment` - Date/time manipulation

## Core Functions

### checkPassesStatus(pass, nowTime)
Validates and updates individual pass status based on expiration and usage.

**Parameters:**
- `pass` - Pass object with status and payload
- `nowTime` - Current Unix timestamp

**Status Logic:**
- `USABLE` → `USING` (when first_use exists and not expired)
- `USABLE` → `EXPIRED` (when first_use exists and expired)
- `USING` → `EXPIRED` (when past expiration time)

**Returns:**
```javascript
{
  pass: updatedPass,
  status_valid: boolean,
  status_log: string
}
```

### mainProcess(cache, nowTime, editMode)
Main processing logic for cache status checking and updating.

**Parameters:**
- `cache` - BytemarkTicketsCache instance
- `nowTime` - Current Unix timestamp
- `editMode` - Boolean flag for saving changes

**Process Flow:**
1. Check each pass in cache.passes array
2. Update pass statuses using checkPassesStatus
3. Save changes if editMode is enabled and invalid passes found
4. Generate status change logs

### createLog(passesStatusChecked, cache)
Creates log object for passes with invalid status.

**Returns:**
```javascript
{
  user_id: number,
  invalid_list: [
    {
      pass_uuid: string,
      status_log: string
    }
  ]
}
```

## Job Configuration

### Inputs
- `userID` (Number) - Target user ID (0 for all users)
- `statusChange` (Number) - Edit mode flag (1 = save changes)

### Main Function
Processes Bytemark ticket cache status for specified user or all users.

**Process Steps:**
1. Set current timestamp and edit mode
2. Query cache(s) based on userID parameter
3. Process each cache through mainProcess function
4. Collect status change logs
5. Save comprehensive log to BytemarkCacheStatusCheckLog

## Data Models

### BytemarkTicketsCache
```javascript
{
  user_id: number,
  passes: [
    {
      pass_uuid: string,
      status: string, // 'USABLE', 'USING', 'EXPIRED'
      payload: {
        expiration: string,
        first_use: string | null
      }
    }
  ]
}
```

### BytemarkCacheStatusCheckLog
```javascript
{
  _id: number, // Unix timestamp
  check_userID: number | 'all users',
  editMode: boolean,
  check_time: string, // ISO timestamp
  log: array // Array of status change logs
}
```

## Business Logic

### Status Transitions
1. **USABLE → USING**: When pass is first used and not expired
2. **USABLE → EXPIRED**: When pass expires without use
3. **USING → EXPIRED**: When active pass expires

### Edit Mode Behavior
- **Edit Mode ON**: Updates cache and saves changes
- **Edit Mode OFF**: Only generates logs without saving

### Batch Processing
- Single user: Process specific user's cache
- All users: Process all user caches in parallel

## Error Handling
- Try-catch blocks around main process and individual operations
- Detailed logging of errors and stack traces
- Graceful handling of missing cache data

## Logging
- Entry and completion status
- User ID and edit mode settings
- Status change summaries
- Error details with stack traces

## Performance Considerations
- Parallel processing for multiple users
- Lean queries for user ID lists
- Conditional cache saving based on edit mode

## Usage Examples

### Check Single User (Read-only)
```javascript
inputs: { userID: 12345, statusChange: 0 }
```

### Update All Users
```javascript
inputs: { userID: 0, statusChange: 1 }
```

## Integration Points
- Bytemark ticket management system
- Cache status monitoring
- Audit logging system
- Scheduled job processing

## Notes
- Designed for scheduled execution
- Supports both read-only checks and update operations
- Comprehensive logging for audit trails
- Handles both individual user and bulk operations