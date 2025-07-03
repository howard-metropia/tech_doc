# info-tile-first.js

## Overview
Job for creating and scheduling WTA (Washington Transit Agency) experiment info tiles based on user habitual trip patterns and travel mode preferences. Generates personalized campaign messages for transit behavior change experiments.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/info-tile-first.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `@maas/core/mysql` - MySQL database connection (portal)
- `@app/src/services/incentiveUtility` - Incentive utility functions
- `moment` / `moment-timezone` - Date/time manipulation
- `geo-tz` - Geographic timezone detection
- `@maas/core/log` - Logging utility
- `fs` - File system for JSON configuration

## Core Functions

### Main Query Logic
Complex SQL query to identify eligible users for WTA experiments based on:
- WTA agreement status (`wta_agree = 1`)
- Habitual trip patterns (7am-7pm)
- Second highest travel mode probability
- Market assignment and microsurvey completion

### Campaign Creation Process
For each eligible user, creates two info tile campaigns:
1. **First Info Tile**: Scheduled for next Sunday 8:00 PM
2. **Second Info Tile**: Scheduled for next Tuesday 8:00 PM

## Processing Flow

### 1. User Eligibility Query
```sql
SELECT Table3.user_id, departure_time, second_MOD_probability, 
       second_MOD_value, change_type, market, activity_id
FROM (complex nested query)
WHERE change_type = 'ChangeMode' 
  AND second_MOD_probability >= 5
  AND microsurvey IN (1, 2)
```

### 2. Timezone Calculation
- Uses geographic coordinates to determine user's timezone
- Calculates UTC offset for proper scheduling
- Adjusts campaign timing based on local time zones

### 3. Travel Mode Content Selection
Based on `second_travel_mode`, selects appropriate tile content:
- **Transit**: Tiles 0 and 1 from configuration
- **Walking**: Tiles 2 and 3 from configuration  
- **Bicycling**: Tiles 4 and 5 from configuration

### 4. Campaign Database Insertion
Creates comprehensive campaign structure:
- `cm_campaign` - Main campaign record
- `cm_step` - Campaign content and messaging
- `cm_campaign_user` - User-campaign associations
- `wta_info_tile` - Experiment tracking record

## Data Models

### WTA Info Tile Configuration
```javascript
{
  [market]: [
    {
      tile_name: string,
      body: string
    }
  ]
}
```

### Campaign Tables Structure

#### cm_campaign
```javascript
{
  is_active: 1,
  name: 'WTA_Experiment_info_tile',
  type_id: 1,
  creater: 'black.tseng@metropia.com',
  utc_setting: 'America/Los_Angeles',
  start_time: datetime,
  end_time: datetime, // +240 minutes
  status: 1
}
```

#### cm_step
```javascript
{
  campaign_id: number,
  title: string,
  body: string,
  action_type: 1,
  step_no: 1,
  choice_type: 1,
  sys_question_id: 0
}
```

#### wta_info_tile
```javascript
{
  user_id: number,
  activity_id: number,
  campaign_id: string, // Comma-separated IDs
  departure_time: time,
  travel_mode: string,
  change_type: 'ChangeMode',
  sent_process: 0,
  info_tile1: datetime,
  info_tile2: datetime,
  results: datetime // Results collection time
}
```

## Business Logic

### Experiment Selection Criteria
- **Most Frequent Habitual Trip**: Between 7am-7pm
- **Second Mode Probability**: >= 5% threshold
- **Change Type**: 'ChangeMode' (vs 'ChangeTime')
- **Market Assignment**: Valid market with tile configuration
- **Consent Status**: Microsurvey completed (1 or 2)

### Scheduling Algorithm
```javascript
// First tile: Next Sunday 8:00 PM local time
const info_tile1 = tz.utc()
  .add(7 - current_day, 'days')
  .format('YYYY-MM-DD 20:00:00')
  .add(timezone_diff, 'hours');

// Second tile: Next Tuesday 8:00 PM local time  
const info_tile2 = tz.utc()
  .add(9 - current_day, 'days')
  .format('YYYY-MM-DD 20:00:00')
  .add(timezone_diff, 'hours');
```

### Travel Mode Mapping
- **Transit**: Public transportation options
- **Walking**: Pedestrian-focused messaging
- **Bicycling**: Cycling-specific content
- **Driving**: Default mode (excluded from second mode)

## Geographic Processing

### Timezone Detection
```javascript
const timeZone = find(latitude, longitude);
const offset = moment.tz(timeZone[0]).format('ZZ') - 
               moment.tz('Europe/London').format('ZZ');
```

### Market-Based Content
- Loads market-specific tile configurations
- Matches user market to appropriate messaging
- Supports localized content per geographic region

## Campaign Duration
- **Active Period**: 4 hours (240 minutes)
- **Start Time**: Calculated based on user timezone
- **End Time**: Start time + 240 minutes
- **Results Collection**: Following Saturday at 8:00 PM

## Error Handling
- Checks for existing info tiles to prevent duplicates
- Validates market configuration availability
- Graceful handling of missing geographic data
- Comprehensive logging of all operations

## Integration Points
- WTA agreement tracking system
- Habitual trip analysis engine
- Campaign management system
- Geographic market definitions
- Microsurvey completion tracking

## Configuration Dependencies
- `./assets/goezy/wta_tile.json` - Tile content configuration
- Market-specific messaging templates
- Geographic timezone data
- Travel mode classifications

## Performance Considerations
- Complex nested SQL queries
- Multiple database insertions per user
- Geographic calculations for timezone conversion
- File system access for configuration loading

## Experiment Framework
This job is part of a larger WTA experiment framework:
1. **Week 1**: Info tile delivery and behavior monitoring
2. **Evaluation**: Behavior change assessment
3. **Phase 2**: Additional experiments if no change detected

## Usage Scenarios
- Transit behavior change experiments
- Personalized mobility recommendations
- Geographic market testing
- Travel mode shift analysis

## Notes
- Designed for WTA-specific experiment requirements
- Supports multiple markets and timezones
- Creates comprehensive audit trail for research
- Integrates with broader campaign management system