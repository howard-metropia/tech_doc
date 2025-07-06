# incentive-process.js

## Overview
Comprehensive job for processing user incentives based on app usage and trip activities. Handles timezone-based reward calculations, points distribution, and notification scheduling for open app and trip completion rewards.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/incentive-process.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `@maas/core/mysql` - MySQL database connection (portal)
- `moment` / `moment-timezone` - Date/time manipulation
- `@app/src/services/incentiveUtility` - Incentive utility functions
- `@app/src/services/wallet` - Wallet and transaction services
- `@maas/core/log` - Logging utility
- `config` - Application configuration

## Core Functions

### openAppProcess(userId, userInMarket, openAppConf, marketInfo, sendTime)
Processes open app incentives for eligible users.

**Parameters:**
- `userId` - Target user ID
- `userInMarket` - User's market assignment
- `openAppConf` - Open app incentive configuration
- `marketInfo` - Market information including timezone
- `sendTime` - Notification send time

**Process Flow:**
1. Generate random points using beta distribution
2. Check for duplicate incentives within 2 hours
3. Update user wallet with app rewards
4. Schedule notification delivery
5. Update market user status

### makeTripProcess(userId, resultTrip, userInMarket, makeTripConf, marketInfo, sendTime)
Processes trip completion incentives with weekly limits.

**Parameters:**
- `userId` - Target user ID
- `resultTrip` - Array of completed trips
- `userInMarket` - User's market assignment
- `makeTripConf` - Trip incentive configuration
- `marketInfo` - Market information
- `sendTime` - Notification send time

**Process Flow:**
1. Generate random points for each trip
2. Check weekly bonus limits (5 points maximum)
3. Process each eligible trip reward
4. Aggregate points and transaction IDs
5. Schedule consolidated notification

## Helper Functions

### checkAppLoginRecords(userId, startDate, endDate)
Verifies user app login activity within specified timeframe.

**Returns:** Array of app_data records

### checkActualTripRecords(userId, startDate, endDate)
Validates completed trips over 1 mile distance.

**Query Conditions:**
- Trip distance > 1609 meters (1 mile)
- Active and auto-logged trips only
- Within specified date range

### checkExistIncentive(userId, type)
Prevents duplicate incentive awards within 2-hour window.

**Parameters:**
- `userId` - Target user ID
- `type` - Incentive type ('incentive open app' or 'incentive make trip')

### userTripsWeekBonus(userId)
Calculates user's current week trip bonus points.

**Returns:** Total points earned from trip incentives this week

## Job Configuration

### Inputs
No input parameters required.

### Main Function
Processes incentives for users at 6:00 AM local time across all timezones.

## Processing Flow

### 1. Configuration Loading
```javascript
const marketGeo = await util.getMarket('assets/' + project + '/market_attribute.json');
const incentiveEngine = await util.getMarket('assets/' + project + '/incentive_engine_message.json');
```

### 2. Timezone Processing
- Get all available timezones from market data
- Identify timezones where local time is 6:00 AM
- Process users in matching timezones

### 3. User Processing
For each eligible user:
- Check if within open app reward period
- Process app login incentives if applicable
- Handle trip completion rewards (currently disabled)

### 4. Date Range Calculation
- Calculate previous day: 6 hours ago to 30 hours ago
- Ensures consistent daily processing regardless of timezone

## Incentive Types

### Open App Rewards
- **Trigger**: User opens app within reward period
- **Points**: Random generation using beta distribution
- **Frequency**: Once per day per user
- **Message Key**: 'Incentive1_1_open_app'

### Trip Completion Rewards (Disabled)
- **Trigger**: Complete trips over 1 mile
- **Points**: Random generation per trip
- **Weekly Limit**: 5 points maximum
- **Message Key**: 'Incentive1_2_make_trip'
- **Status**: Currently commented out (MET-13992)

## Points Distribution Algorithm

### Random Point Generation
Uses `util.random_decimal_generator()` with parameters:
- `maximum_value` - Upper bound
- `minimum_value` - Lower bound  
- `mean` - Distribution mean
- `beta` - Beta distribution parameter

### Wallet Integration
```javascript
const transactionId = await util.userWalletSync(userId, {
  activity_type: 6,
  points: calculatedPoints,
  balance: updatedBalance,
  note: 'Sign-in reward' | 'Make trip reward'
});
```

## Data Models

### Incentive Configuration
```javascript
{
  incentive_parm: {
    maximum_value: number,
    minimum_value: number,
    mean: number,
    beta: number
  },
  push_notification: string // Template with [$x] placeholder
}
```

### Notification Queue Record
```javascript
{
  user_id: number,
  points_transaction_id: string, // Comma-separated IDs
  trip_ids: string, // Comma-separated trip IDs
  market: string,
  purpose: 'incentive',
  incentive_type: string,
  notification_type: 1,
  msg_key: string,
  msg_content: string,
  timezone: string
}
```

## Business Logic

### Daily Processing Window
- Processes at 6:00 AM local time for each timezone
- Uses previous day data (6-30 hours ago)
- Prevents duplicate processing with time-based checks

### Reward Eligibility
- Open app rewards: Within configured day limit
- Trip rewards: Within trip day limit and weekly bonus cap
- Duplicate prevention: 2-hour cooldown period

### Points Calculation
- Random generation ensures variety
- Balance tracking prevents overpayment
- Transaction logging for audit trails

## Performance Optimizations
- Timezone-based batching reduces processing load
- Single-day data windows limit query scope
- Batch notification scheduling
- Reuse of database connections

## Error Handling
- Graceful handling of missing configurations
- Database transaction rollback capabilities
- Detailed logging for debugging

## Integration Points
- Market configuration system
- User wallet service
- Notification delivery system
- Trip tracking system
- App usage analytics

## Configuration Dependencies
- Market attribute files for timezone data
- Incentive engine configuration for rewards
- Project-specific settings

## Notes
- Trip incentives temporarily disabled per MET-13992
- Designed for daily scheduled execution
- Supports multiple markets and timezones
- Comprehensive audit logging for compliance