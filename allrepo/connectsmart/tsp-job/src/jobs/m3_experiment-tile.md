# m3_experiment-tile.js

## Overview
Job for creating and scheduling M3 (Mobility Mode Modification) experiment tiles based on user habitual trip patterns and travel mode probabilities. This sophisticated job generates personalized mobility interventions using machine learning insights to encourage sustainable travel behavior changes through targeted incentives and messaging.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/m3_experiment-tile.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `@maas/core/mysql` - MySQL database connection (portal)
- `@maas/core/log` - Structured logging utility
- `@app/src/services/incentiveUtility` - Incentive calculation and campaign management
- `@app/src/models/ClusterTrips` - MongoDB model for clustered trip data
- `@app/src/models/ModResults` - MongoDB model for mode prediction results
- `@app/src/models/CmClusterId` - MongoDB model for cluster ID mapping
- `moment` / `moment-timezone` - Advanced date/time manipulation
- `crypto` - Cryptographic functions for group ID generation
- `geo-tz` - Geographic timezone detection
- `config` - Application configuration management

## Core Functions

### Advanced Trip Clustering Analysis
Analyzes user habitual trips using machine learning clustering:
- **Cluster-Based Patterns**: Uses MongoDB clustered trip data for pattern recognition
- **Mode Probability Analysis**: Leverages ML models to predict travel mode preferences
- **Temporal Pattern Recognition**: Identifies weekday/weekend travel patterns
- **Geographic Clustering**: Groups trips by origin-destination patterns

### Intelligent Incentive Generation
Creates personalized incentives using statistical models:
- **Beta Distribution**: Uses random_decimal_generator with configurable parameters
- **Mode-Specific Incentives**: Different incentive structures per travel mode
- **Dynamic Point Calculation**: Real-time point value generation based on user behavior

### Timezone-Aware Scheduling
Implements sophisticated timezone handling:
- **Geographic Timezone Detection**: Uses coordinates to determine local timezone
- **Seasonal Offset Adjustment**: Handles daylight saving time transitions
- **Multi-Region Support**: Supports experiments across different timezones

## Processing Flow

### 1. User Eligibility Analysis
```javascript
const userIds = (
  await knex('market_user')
    .select('market_user.user_id')
    .leftJoin('user_config', 'user_config.user_id', 'market_user.user_id')
    .where('market_user.user_in_market', 'HCS')
    .whereNull('user_config.retention_plan')
    .orWhere('user_config.retention_plan', 1)
).map((item) => item.user_id);
```

### 2. Habitual Trip Pattern Analysis
```javascript
// For GoEzy project
if (project == 'goezy') {
  return await knex('cm_activity_location')
    .whereIn('user_id', userIds)
    .andWhere('travel_mode', '=', 1)           // Driving trips
    .andWhere('trip_count_quarterly', '>=', 2)  // Minimum frequency
    .andWhere('bayes_count', '>=', 1);         // ML confidence threshold
} else {
  // For HCS project - uses MongoDB clustering
  const filter = {
    user_id: { $in: userIds },
    "travel_mode_percentages.driving": { $exists: true, $gte: 0.5 }
  };
  return await ClusterTrips.find(filter);
}
```

### 3. Mode Prediction Analysis
```javascript
const getMODsById = async (htrip) => {
  return await ModResults.find({
    cluster_id: htrip._id.toString(),
  });
};

// Extract second-best travel mode
let modeList = [...mods[0].mode_results];
modeList.sort((a, b) => b.probability - a.probability);
secondMode = modeList[1].travel_mode;
```

### 4. Timezone and Scheduling Calculation
```javascript
// Geographic timezone detection
const timezone = find(
  userODT.common_start_location.coordinates[1],
  userODT.common_start_location.coordinates[0],
);

// Seasonal offset adjustment
const currentTZOffset = moment().tz(timezone[0]).utcOffset();
const habitualTZOffset = moment(departureTime).tz(timezone[0]).utcOffset();

// Schedule calculations
const deliverTime = tz.tz(newDepartureTime, 'YYYY-MM-DD HH:mm:ss', timezone[0])
  .utc().subtract(2, 'hours').format('HH:mm:ss');  // Info tile: 2 hours before
const actDeliverTime = tz.tz(newDepartureTime, 'YYYY-MM-DD HH:mm:ss', timezone[0])
  .utc().subtract(1, 'hours').format('HH:mm:ss');  // Action tile: 1 hour before
```

## Data Models

### Clustered Trip Structure
```javascript
{
  _id: ObjectId,
  user_id: number,
  day_of_week: number,                    // 1-7 (Monday-Sunday)
  common_start_location: {
    type: "Point",
    coordinates: [longitude, latitude]
  },
  common_end_location: {
    type: "Point", 
    coordinates: [longitude, latitude]
  },
  departure_time_range: {
    earliest: "HH:mm:ss",
    latest: "HH:mm:ss"
  },
  travel_mode_percentages: {
    driving: number,
    transit: number,
    walking: number,
    bicycling: number
  }
}
```

### Mode Results Structure
```javascript
{
  cluster_id: string,
  mode_results: [
    {
      travel_mode: "driving|transit|walking|bicycling",
      probability: number
    }
  ]
}
```

### M3 Experiment Tile Schema
```javascript
{
  user_id: number,
  activity_location_id: number,
  group_id: string,                       // Crypto-generated UUID
  weekday: number,                        // 1-7 (Monday-Sunday)
  notification_type: number,              // 1=info, 4=action
  points: number,                         // Generated incentive points
  random_mode: string,                    // "second best" | ""
  send_mode: string,                      // "public transit|cycling|walking|no message"
  msg_title: string,
  msg_content: string,
  deliver_time: datetime,
  campaign_id: number                     // Links to campaign system
}
```

### M3 Compensation Schema
```javascript
{
  experiment_id: number,                  // Links to m3_experiment_tile
  user_id: number,
  campaign_id: number,                    // Links to action tile campaign
  specified_mode: number,                 // Expected travel mode (1-7)
  points: number,                         // Reward points
  deliver_time: datetime,                 // Experiment start time
  validate_time: datetime                 // Validation deadline
}
```

## Business Logic

### Travel Mode Conversion
```javascript
const convertTravelMode = (msg) => {
  switch (msg) {
    case 'public transit': return 5;      // Intermodal
    case 'walking': return 3;             // Walking
    case 'cycling': return 4;             // Biking
  }
};
```

### Weekday Pattern Matching
```javascript
const checkWeekdayWeekend = (number) => {
  if (number > 5) {
    return 'weekend';
  } else {
    return 'weekday';
  }
};

// Only send if weekday patterns match
if (checkWeekdayWeekend(nextWeekDay) == checkWeekdayWeekend(habitualWeekDay)) {
  // Process experiment tile
}
```

### Incentive Calculation
```javascript
const getRandomParam = (m3Config, mode) => {
  const random_incentive = m3Config.random_incentive;
  for (const k in random_incentive) {
    if (random_incentive[k].mode == mode) {
      return {
        maximum_value: random_incentive[k].maximum_value,
        minimum_value: random_incentive[k].minimum_value,
        mean: random_incentive[k].mean,
        beta: random_incentive[k].beta
      };
    }
  }
};

const points = util.random_decimal_generator(
  param.maximum_value,
  param.minimum_value,
  param.mean,
  param.beta,
);
```

### Time Slot Conversion
```javascript
const convertDeliverTime = (departureTime, qty) => {
  const depDataAry = departureTime.split(' ');
  const deliverAry = depDataAry[1].split(':');
  const totalMinutes = parseInt(deliverAry[0] * 60) + parseInt(deliverAry[1]);
  
  let currentSlots;
  if (totalMinutes % 15 == 0 && deliverAry[2] == 0) {
    currentSlots = Math.floor(totalMinutes / 15);
  } else {
    currentSlots = Math.floor(totalMinutes / 15) + 1;
  }
  
  // Handle day boundary crossing
  if (currentSlots - qty < 0) {
    timeSlots = currentSlots - qty + 96;  // 96 = 24 hours * 4 (15-min slots)
  } else {
    timeSlots = currentSlots - qty;
  }
  
  const finalMinutes = timeSlots * 15;
  const hours = String(parseInt((finalMinutes / 60) % 24)).padStart(2, '0');
  const mins = String(parseInt(finalMinutes % 60)).padStart(2, '0');
  return hours + ':' + mins + ':00';
};
```

## Campaign Integration

### Info Tile Campaign Creation
```javascript
const notifyData = {
  description: 'sent for m3 info tile',
  sendtime: deliverTime,
  timezone: 'UTC',
  name: 'M3 Info Tile',
  title: msg.title,
  body: msgBody,
};
const m3InfoTileId = await util.addToInfoTile(notifyData, userODT.user_id, 'M3');
```

### Action Tile Campaign Creation
```javascript
const notifyActionData = {
  description: 'sent for m3 action tile',
  sendtime: actDeliverTime,
  timezone: 'UTC',
  name: 'M3 Action Tile',
  title: msgAction.title,
  body: msgAction.body,
  changeModeTransport: travelMode,
  points: points,
  oid: c_id,
  did: c_id,
  departureTime: actDepartureTime,
  endDate: endDateTime
};
const m3ActionTileId = await util.addToActionTile(notifyActionData, userODT.user_id, 'M3');
```

## Advanced Features

### Dynamic Message Content
```javascript
// Replace placeholder with actual points
if (points > 0) {
  msgBody = msg.body.replace(
    '[in exchange for] [$XX.XX] [in reward Coins]',
    'in exchange for ' + points + ' in reward Coins',
  );
} else {
  msgBody = msg.body.replace(
    '[in exchange for] [$XX.XX] [in reward Coins]',
    '',
  );
}
```

### Group ID Generation
```javascript
const groupID = crypto.randomBytes(16).toString('hex');
```

### Validation Time Calculation
```javascript
const validateDateTimeUTC = tz(endDateTime)
  .add(2, 'hours')
  .format('YYYY-MM-DD HH:mm:ss');
```

## Performance Considerations

### MongoDB Query Optimization
- **Indexed Queries**: Uses cluster_id indexes for efficient lookups
- **Projection**: Only fetches required fields from large documents
- **Aggregation**: Leverages MongoDB aggregation pipeline for complex queries

### Batch Processing
- **Sequential Processing**: Processes users sequentially to manage memory
- **Database Connection Pooling**: Efficient connection management
- **Transaction Management**: Proper transaction handling for data consistency

### Memory Management
- **Streaming Processing**: Processes large datasets without loading all into memory
- **Connection Cleanup**: Proper resource cleanup after processing
- **Error Isolation**: Individual user failures don't affect batch processing

## Integration Points

### Campaign Management System
- **Info Tile Integration**: Links with campaign management for notifications
- **Action Tile Integration**: Creates interactive campaigns for behavior change
- **Progress Tracking**: Monitors user engagement and completion

### Incentive System
- **Point Calculation**: Dynamic incentive generation based on user patterns
- **Reward Distribution**: Integration with user wallet and compensation systems
- **Performance Tracking**: Monitors incentive effectiveness

### Machine Learning Pipeline
- **Cluster Analysis**: Uses ML-generated trip clusters for pattern recognition
- **Mode Prediction**: Leverages ML models for travel mode recommendations
- **Behavioral Modeling**: Applies statistical models for intervention timing

## Error Handling
```javascript
try {
  // Main processing logic
} catch (err) {
  logger.error(err.message);
}
```

## Monitoring and Analytics
```javascript
logger.info('Total Executed Records: ' + executed);
logger.info('Total Insert Records: ' + records * 2);

await util.addUpcomingEvents({
  brand: brand,
  service_name: 'M3',
  job_name: 'M3 experiment tile',
  job_purpose: 'M3 experiment 2',
  start_date: currentDate,
  end_date: endDate,
  audience_rule: 'Users on user_signup table',
  frequency: 'Daily',
  message_title: '',
  message_type: 'Push notification',
  message_content: '',
});
```

## Usage Scenarios
- **Mobility Behavior Research**: Academic research on travel mode choice
- **Smart City Initiatives**: Municipal transportation demand management
- **Sustainability Programs**: Environmental impact reduction through mode shift
- **Transit Optimization**: Public transit ridership enhancement
- **Corporate Mobility**: Employee transportation behavior modification

## Configuration Dependencies
- **Project Configuration**: `config.get('app.project')` for GoEzy vs HCS differences
- **M3 Tiles Configuration**: `assets/{project}/m3_tiles.json` for messaging content
- **Random Incentive Parameters**: Configurable statistical distributions per mode
- **Geographic Data**: Coordinate-based timezone detection requirements

## Notes
- **Research-Grade Precision**: Designed for academic and municipal research requirements
- **Scalable Architecture**: Supports large-scale multi-city deployments
- **ML Integration**: Seamlessly integrates with machine learning prediction models
- **Multi-Project Support**: Configurable for different mobility projects (GoEzy, HCS)
- **Comprehensive Auditing**: Full audit trail for research reproducibility and compliance