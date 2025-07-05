# retention-process.js

## Overview
Job for processing user retention campaigns based on activity patterns and trip history. Sends targeted info tiles to encourage user engagement and trip generation based on user lifecycle stages.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/retention-process.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `@maas/core/mysql` - MySQL database connection (portal)
- `moment-timezone` - Timezone-aware date handling
- `geo-point-in-polygon` - Geospatial processing
- `@app/src/services/incentiveUtility` - Incentive utility functions
- `config` - Application configuration
- `@maas/core/log` - Logging utility

## Core Functions

### sendRetention(row, market, marketMsg, sendTime)
Main function for processing individual user retention campaigns.

**Parameters:**
- `row` - User market data record
- `market` - Market configuration with retention settings
- `marketMsg` - Market-specific retention messages
- `sendTime` - Configured send time for notifications

**Process Flow:**
1. Validate user eligibility (skip users < 2 days old)
2. Determine retention scenario based on trip history
3. Send appropriate retention tile based on user lifecycle stage
4. Update user retention status

## Job Configuration

### Inputs
No input parameters required.

### Main Function
Processes retention campaigns for users at 7:00 AM local time across all timezones.

## Processing Flow

### 1. Configuration Loading
```javascript
const marketGeo = await util.getMarket('assets/' + project + '/market_attribute.json');
const marketMsg = await util.getMarket('assets/' + project + '/retention_info_tile.json');
```

### 2. Timezone Processing
- Get all available timezones from market data
- Identify timezones where local time is 7:00 AM
- Process users in matching timezones

### 3. User Processing
For each eligible user:
- Check user lifecycle stage
- Determine appropriate retention intervention
- Send targeted retention message

## Retention Scenarios

### Scenario 1: No Trips Generated (Status 2)
**Condition**: User has 0 trip count after registration
**Triggers**: Days 2, 5, and 10 after registration
**Purpose**: Push the user to generate a trip

**Implementation:**
```javascript
if (row.trip_count == 0) {
  for (const k in retentionDays) {
    if (retentionDays[k].days == row.user_days) {
      // Send retention tile RT_info_tile_2, RT_info_tile_3, RT_info_tile_4
    }
  }
}
```

### Scenario 2: No Habitual Trips (Status 3)
**Condition**: User has trips but no habitual trip patterns
**Triggers**: 3 and 6 days after last trip
**Purpose**: Remind user to take the next trip

**Implementation:**
```javascript
const activityLocation = await knex('cm_activity_location').where('user_id', row.user_id);
if (activityLocation.length == 0) {
  // Send RT_info_tile_5 based on trip_to_now values
}
```

## Business Logic

### User Eligibility
- **Minimum Age**: Users must be 2+ days old to receive retention messages
- **Activity Status**: Based on trip count and habitual trip existence
- **Market Assignment**: Uses user's assigned market for messaging

### Message Selection
- **Market-Specific**: Uses tiles configured per market
- **Lifecycle-Based**: Different messages for different user stages
- **Dynamic Content**: Pulls appropriate tile based on retention configuration

### Status Updates
- **Status 2**: User pushed to generate trips
- **Status 3**: User reminded to continue trip patterns
- **Tracking**: All retention campaigns logged for analysis

## Data Models

### market_user Table (Input)
```javascript
{
  user_id: number,
  user_in_market: string,
  user_days: number,
  trip_count: number,
  trip_to_now: number,
  retention_status: number
}
```

### Retention Configuration
```javascript
{
  retention_time: [
    {
      days: number,
      title: string // RT_info_tile_2, RT_info_tile_3, etc.
    }
  ]
}
```

### Notification Data Structure
```javascript
{
  description: 'sent for retention',
  sendtime: string,
  timezone: string,
  name: string,
  title: string,
  body: string
}
```

## Retention Tile Types

### RT_info_tile_2
- **Timing**: 2 days after registration
- **Target**: Users with no trips
- **Message**: Initial trip encouragement

### RT_info_tile_3
- **Timing**: 5 days after registration
- **Target**: Users still with no trips
- **Message**: Stronger trip encouragement

### RT_info_tile_4
- **Timing**: 10 days after registration
- **Target**: Users persistently with no trips
- **Message**: Final trip encouragement

### RT_info_tile_5
- **Timing**: Dynamic based on last trip
- **Target**: Users with trips but no habitual patterns
- **Message**: Continuation encouragement

## Campaign Integration

### Info Tile Creation
```javascript
const campaignId = await util.addToInfoTile(notifyData, userId);
```

### Retention Tracking
```javascript
const rowData = {
  campaignId,
  userDays: row.user_days,
  note: 'Scenario description'
};
await util.addRetentionInfoTile(rowData, userId);
```

## Timezone Handling
- **Processing Time**: 7:00 AM local time
- **Send Time**: 8:00 AM local time
- **Market-Specific**: Uses market timezone configuration
- **Global Coverage**: Processes all timezones appropriately

## Performance Considerations
- Timezone-based batching reduces processing load
- Efficient user filtering by eligibility criteria
- Database queries optimized for user lifecycle checks

## Error Handling
- Graceful handling of missing market configurations
- Robust timezone processing
- Comprehensive logging for debugging

## Integration Points
- Market configuration system
- User activity tracking
- Campaign management system
- Retention analytics
- Notification delivery system

## Configuration Dependencies
- Market attribute files for timezone data
- Retention info tile message configurations
- Project-specific settings

## Usage Scenarios
- Daily retention campaign processing
- User lifecycle management
- Engagement optimization
- Churn prevention strategies

## Logging
- User eligibility decisions
- Campaign creation confirmations
- Processing status updates

## Notes
- Designed for daily scheduled execution
- Supports multiple markets and timezones
- Comprehensive user lifecycle tracking
- Integrates with broader retention strategy