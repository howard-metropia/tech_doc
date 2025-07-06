# action-tile-first.js

## Overview
Job module for WTA (Washington Transportation Authority) experiment that processes info tiles and creates action tiles for behavioral change experiments. This job handles first-week experimental data processing and prepares users for second-week experiments based on travel behavior analysis.

## Purpose
- Process completed first-week info tiles without behavior changes
- Create second-week action tiles with incentive campaigns
- Generate travel mode change recommendations with monetary rewards
- Manage experimental campaign lifecycle for behavioral studies

## Key Features
- **Experiment Progression**: Transitions users from info tiles to action tiles
- **Travel Mode Mapping**: Converts travel modes to standardized IDs
- **Dynamic Incentive Generation**: Creates random reward points based on market configuration
- **Campaign Management**: Automated creation of info and action tile campaigns
- **Habitual Trip Analysis**: Identifies recurring travel patterns for targeting

## Dependencies
```javascript
const knex = require('@maas/core/mysql')('portal');
const queueService = require('@app/src/services/queue');
const util = require('@app/src/services/incentiveUtility');
const Moment = require('moment');
const tz = require('moment-timezone');
```

## Configuration Files
- `./assets/goezy/market_attribute.json` - Market-specific configuration and incentive parameters
- `./assets/goezy/wta_tile.json` - Tile content templates for different markets

## Travel Mode Mappings
```javascript
// Standard Travel Modes
// 1: driving, 2: public_transit, 3: walking
// 4: biking, 5: intermodal, 6: trucking
// 7: park & ride, 100: duo

// Tile Travel Modes
const modeMapping = {
  transit: { travel_mode: 6, suggested_mode: 5 },
  walking: { travel_mode: 8, suggested_mode: 3 },
  bicycling: { travel_mode: 10, suggested_mode: 4 }
};
```

## Core Functions

### Main Processing Logic
```javascript
module.exports = {
  inputs: {},
  fn: async function () {
    // Process WTA info tiles ready for action tile creation
    // Generate campaign schedules and incentive amounts
    // Create database entries for experimental campaigns
  }
};
```

### Experiment Selection Query
```sql
SELECT *,
(CASE
 WHEN hybrid.wta_info_tile.travel_mode = 'transit' THEN 6
 WHEN hybrid.wta_info_tile.travel_mode = 'walking' THEN 8
 WHEN hybrid.wta_info_tile.travel_mode = 'bicycling' THEN 10
 ELSE 0
 END) AS travel_mode,
CONCAT(DATE_FORMAT(DATE_ADD(hybrid.wta_info_tile.results, INTERVAL 1 DAY), "%Y-%m-%d"), ' ', departure_time) AS results_date
FROM hybrid.wta_info_tile
WHERE (sent_process = 1 AND ISNULL(change_behavior)) 
   OR (sent_process <= 1 AND results <= now());
```

### Habitual Trip Identification
```sql
SELECT user_id, o_id, d_id,
SUBSTRING(departure_time, 12, 8) AS departure_time,
CONVERT_TZ(departure_time, 'UTC', 'Europe/London') AS utc
FROM hybrid.cm_activity_location
WHERE user_id = ? AND trip_count > 3;
```

## Campaign Creation Process

### 1. Info Tile Campaign
- **Type**: Information tile (type_id: 1)
- **Timing**: 60 minutes before departure time
- **Duration**: 10-minute window
- **Purpose**: Pre-trip behavioral nudge

### 2. Action Tile Campaign
- **Type**: Change mode campaign (type_id: 4)
- **Timing**: At departure time
- **Duration**: 12-hour window
- **Incentive**: Dynamic reward points based on market configuration

## Incentive Generation
```javascript
// Market-specific random incentive calculation
randomPoints = util.random_decimal_generator(
  market_config.maximum_value,
  market_config.minimum_value,
  market_config.mean,
  market_config.beta
);
```

## Database Operations

### Campaign Tables
- `hybrid.cm_campaign` - Main campaign configuration
- `hybrid.cm_step` - Campaign content and actions
- `hybrid.cm_campaign_user` - User-campaign associations

### Experimental Tables
- `hybrid.wta_info_tile` - First-week experiment data
- `hybrid.wta_action_tile` - Second-week experiment tracking

## Scheduling Logic
```javascript
const day = 5; // 5-day campaign duration
const infoTileTime = -60; // 60 minutes before departure

// Calculate next Monday as start date
const startDay = tz.utc(tz.utc()
  .add(8 - now_2, 'days')
  .format('YYYY-MM-DD 20:00:00'))
  .format('YYYY-MM-DD HH:mm:ss');
```

## Content Personalization
- Market-specific tile text from configuration files
- Dynamic reward amount insertion using `[$x.xx]` placeholder
- Travel mode specific messaging based on suggested alternatives

## Error Handling
- Database transaction safety with proper error logging
- Market configuration validation
- User eligibility verification

## Performance Considerations
- Sequential processing of users to avoid database conflicts
- Efficient query structure for large datasets
- Proper timezone handling for global deployments

## Integration Points
- Queue service for asynchronous processing
- Incentive utility service for reward calculations
- MySQL portal database for campaign management
- Asset file system for configuration data

## Usage Notes
- Runs as scheduled job for WTA behavioral experiments
- Processes users who completed first week without behavior change
- Creates comprehensive second-week intervention campaigns
- Maintains experiment integrity through proper state management

## Monitoring
- Process timing logged with `DBstartTime`
- Console logging for debugging and monitoring
- Database operation result tracking
- Campaign creation success verification