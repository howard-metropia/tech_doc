# mtc-experiment-tile.js

## Overview
Job for creating MTC (Metropolitan Transportation Commission) experiment tiles that encourage users to change travel modes through personalized incentives. Generates info and action tiles based on habitual trip patterns with randomized rewards.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/mtc-experiment-tile.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `@maas/core/mysql` - MySQL database connection (portal)
- `@maas/core/log` - Logging utility
- `@app/src/services/incentiveUtility` - Incentive utility functions
- `moment` / `moment-timezone` - Date/time manipulation
- `random-choice` - Weighted random selection
- `crypto` - Group ID generation
- `geo-tz` - Geographic timezone detection
- `config` - Application configuration

## Core Functions

### convertDeliverTime(departureTime, qty)
Converts departure time to delivery time in 15-minute timeslots.

**Parameters:**
- `departureTime` - User's habitual departure time
- `qty` - Number of 15-minute slots to subtract

**Returns:** Formatted time string (HH:mm:ss)

### convertTravelMode(msg)
Maps travel mode strings to numeric codes for database storage.

**Mapping:**
- 'public transit' → 5
- 'walking' → 3  
- 'cycling' → 4

### infoTileInsert(userODT, mtcConfig, ranChoice, currentDate)
Main function for creating experiment tiles for a user's habitual trip.

**Parameters:**
- `userODT` - User's origin-destination-time record
- `mtcConfig` - MTC experiment configuration
- `ranChoice` - Randomly selected experiment type
- `currentDate` - Current processing date

## Job Configuration

### Inputs
No input parameters required.

### Main Function
Processes MTC experiment tile creation for eligible users with driving habitual trips.

## Processing Flow

### 1. Configuration Loading
```javascript
const mtcJSON = await util.getMarket('assets/' + project + '/mtc_tiles_new.json');
const mtcConfig = mtcJSON.MTC;
```

### 2. Event Period Validation
- Checks if current date is before event end date (2023-03-31)
- Terminates processing if event has ended

### 3. User and Trip Processing
For each MTC user:
- Retrieve habitual driving trips (>=2 for GoEzy, >3 for HCS)
- Generate random experiment choice based on probabilities
- Create experiment tiles if eligible

### 4. Tile Creation Process
- Generate unique group ID for experiment tracking
- Calculate delivery times based on timezone offsets
- Create info tile and action tile campaigns
- Insert compensation records for validation

## Experiment Types

### Random Choice Options
Based on configured probabilities:
- **'no message'** - Control group, no intervention
- **'public transit'** - Encourage transit use
- **'walking'** - Encourage walking
- **'cycling'** - Encourage cycling  
- **'do not drive'** - General driving discouragement
- **'second best'** - Promote user's second-best mode

### Mode-Specific Processing
For 'do not drive' and 'second best':
- Queries user's travel mode probabilities
- Selects second-highest probability mode
- Maps to specific encouragement message

## Tile Types

### Info Tile (Type 1)
- **Timing**: 1 hour before departure (5 timeslots)
- **Purpose**: Inform user about experiment and potential rewards
- **Content**: Personalized message with reward amount
- **Delivery**: Next day if weekday matches habitual pattern

### Action Tile (Type 4)  
- **Timing**: 15 minutes before departure (1 timeslot)
- **Purpose**: Provide actionable mode change suggestion
- **Content**: Specific travel mode recommendation
- **Integration**: Links to campaign management system

## Reward System

### Points Calculation
```javascript
const points = util.random_decimal_generator(
  param.maximum_value,
  param.minimum_value, 
  param.mean,
  param.beta
);
```

### Mode-Specific Parameters
- Each travel mode has distinct reward parameters
- Uses beta distribution for natural variation
- Zero rewards possible based on configuration

### Message Personalization
- Replaces `[$XX.XX]` placeholder with calculated points
- Removes reward text if points are zero
- Maintains consistent messaging structure

## Timezone Handling

### Seasonal Adjustment
```javascript
if (currentTZOffset < habitualTZOffset) {
  newDepartureTime = tz(departureTime).add(minutes, 'minutes');
} else if (currentTZOffset > habitualTZOffset) {
  newDepartureTime = tz(departureTime).add(-minutes, 'minutes');
}
```

### Delivery Scheduling
- Accounts for daylight saving time changes
- Uses origin coordinates for timezone detection
- Adjusts delivery times to maintain local consistency

## Data Models

### mtc_experiment_tile Table
```javascript
{
  user_id: number,
  activity_location_id: number,
  group_id: string, // Hex string for experiment grouping
  weekday: number, // 1-7 (Monday-Sunday)
  notification_type: number, // 1=info, 4=action
  points: number,
  random_mode: string,
  send_mode: string,
  msg_title: string,
  msg_content: string,
  deliver_time: datetime,
  campaign_id: number
}
```

### mtc_compensation Table
```javascript
{
  experiment_id: number,
  user_id: number,
  campaign_id: number,
  specified_mode: number,
  points: number,
  deliver_time: datetime,
  validate_time: datetime // 2 hours after info tile
}
```

## Business Logic

### Eligibility Criteria
- User must be in MTC user signup list
- Must have driving habitual trips meeting trip count threshold
- Weekday of delivery must match habitual trip weekday
- No existing experiment tile for the day

### Experiment Grouping
- Each user-trip combination gets unique group ID
- Enables tracking of related info and action tiles
- Supports experiment result analysis

### Validation Window
- 2-hour window after info tile delivery
- Used for measuring behavior change success
- Integrated with compensation tracking

## Campaign Integration

### Info Tile Campaigns
```javascript
const mtcInfoTileId = await util.addToInfoTile(notifyData, userId, 'MTC');
```

### Action Tile Campaigns
```javascript
const mtcActionTileId = await util.addToActionTile(notifyData, userId, 'MTC');
```

## Performance Considerations
- Processes only users with qualifying habitual trips
- Efficient duplicate prevention queries
- Batch processing for multiple user trips
- Timezone calculations optimized per user

## Error Handling
- Validates configuration availability
- Checks for missing location data
- Graceful handling of timezone conversion errors
- Comprehensive logging for debugging

## Integration Points
- Campaign management system
- User signup tracking
- Habitual trip analysis
- Compensation validation system
- Event tracking and analytics

## Usage Scenarios
- Daily experiment tile generation
- A/B testing for travel behavior change
- Transit mode shift research
- Personalized mobility incentives

## Notes
- Event concluded on 2023-03-31
- Supports multiple projects (GoEzy, HCS) with different thresholds
- Comprehensive experiment tracking for research analysis
- Integrates with broader MTC research framework