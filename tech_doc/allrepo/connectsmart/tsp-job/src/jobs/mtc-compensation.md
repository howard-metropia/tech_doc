# mtc-compensation.js

## Overview
Job for processing and validating MTC (Metropolitan Transportation Commission) experiment compensation based on user travel behavior changes. This sophisticated validation system analyzes actual trip data against experimental parameters to determine reward eligibility and automatically distributes incentive payments to qualifying users.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/mtc-compensation.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `@maas/core/mysql` - MySQL database connection (portal)
- `@maas/core/log` - Structured logging utility
- `@app/src/services/incentiveUtility` - Incentive management and notification services
- `moment-timezone` - Timezone-aware date/time operations
- `haversine-distance` - Geographic distance calculations
- `config` - Application configuration management
- `@app/src/services/wallet` - User wallet and payment processing

## Core Functions

### Trip Validation Engine
Implements sophisticated validation logic for experiment compensation:
- **Geographic Validation**: Uses Haversine distance calculations for origin/destination matching
- **Temporal Validation**: Verifies trip timing within experimental parameters
- **Mode Validation**: Confirms travel mode compliance with experiment requirements
- **Distance Requirements**: Enforces minimum trip distance (1 mile) for compensation eligibility

### Automated Compensation Processing
Manages complete compensation workflow:
- **Campaign Status Verification**: Checks user campaign completion status
- **Trip Matching**: Correlates experimental suggestions with actual user behavior
- **Point Calculation**: Calculates and distributes reward points
- **Notification Delivery**: Sends compensation notifications to users

### Wallet Integration
Seamless integration with user wallet system:
- **Balance Calculation**: Maintains accurate user point balances
- **Transaction Recording**: Creates comprehensive transaction audit trails
- **Activity Tracking**: Records compensation activity for reporting

## Processing Flow

### 1. Compensation Queue Retrieval
```javascript
async function getCompensations() {
  const currentDate = tz.utc().format('YYYY-MM-DD HH:mm:ss');
  return await knex('mtc_compensation')
    .where('processed', 0)
    .andWhere('validate_time', '<=', currentDate);
}
```

### 2. Campaign Completion Verification
```javascript
async function checkCampaignGetPoints(campaignId) {
  return await knex('cm_campaign_user')
    .innerJoin('cm_campaign', 'cm_campaign_user.campaign_id', 'cm_campaign.id')
    .innerJoin('cm_user_record', 'cm_campaign_user.campaign_id', 'cm_user_record.campaign_id')
    .where('cm_campaign_user.campaign_id', campaignId)
    .andWhere('cm_user_record.reply_status', 2)      // Completed
    .andWhere('cm_campaign_user.status', 3)          // Active
    .andWhere('cm_campaign_user.reply_status', 1);   // Responded
}
```

### 3. Geographic Location Retrieval
```javascript
async function getHabitualLatLon(experimentId) {
  const location = await knex('cm_activity_location')
    .innerJoin('mtc_experiment_tile', 'cm_activity_location.id', 'mtc_experiment_tile.activity_location_id')
    .where('mtc_experiment_tile.id', experimentId);
    
  const oLatLon = await knex('cm_location').where('id', oID);
  const dLatLon = await knex('cm_location').where('id', dID);
  
  return {
    origin: [oLatLon[0]['latitude'], oLatLon[0]['longitude']],
    destination: [dLatLon[0]['latitude'], dLatLon[0]['longitude']]
  };
}
```

### 4. Trip Validation Process
```javascript
async function checkTrips(userId, startDate, endDate) {
  const limitMeter = 1609;  // 1 mile minimum
  return await knex('trip')
    .innerJoin('telework', 'trip.id', 'telework.trip_id')
    .where('trip.user_id', userId)
    .andWhere('telework.is_active', 1)
    .andWhere('telework.is_autolog', 1)
    .andWhere('telework.started_on', '>=', startDate)
    .andWhere('telework.started_on', '<', endDate)
    .whereIn('trip.travel_mode', [2, 3, 4, 5])  // Non-driving modes
    .andWhere('trip.distance', '>', limitMeter)
    .orderBy('telework.started_on', 'asc');
}
```

## Data Models

### MTC Compensation Schema
```javascript
{
  id: number,                             // Primary key
  experiment_id: number,                  // Links to mtc_experiment_tile
  user_id: number,                        // User identifier
  campaign_id: number,                    // Campaign reference (nullable)
  specified_mode: number,                 // Expected travel mode
  points: number,                         // Reward amount
  deliver_time: datetime,                 // Experiment start time
  validate_time: datetime,                // Validation deadline
  processed: number,                      // Processing status (0/1)
  changed_mode: number,                   // Actual travel mode (nullable)
  trip_id: number,                        // Validated trip ID (nullable)
  campaign_incentive: number,             // Campaign completion flag (nullable)
  campaign_trip_id: number,               // Campaign trip reference (nullable)
  points_transaction_id: number,          // Wallet transaction reference (nullable)
  msg_title: string,                      // Notification title (nullable)
  msg_content: string,                    // Notification content (nullable)
  deliver: number                         // Notification delivery status (nullable)
}
```

### Trip Validation Structure
```javascript
{
  trip_id: number,
  user_id: number,
  travel_mode: number,                    // 1=driving, 2=transit, 3=walking, 4=biking, 5=intermodal
  origin_latitude: number,
  origin_longitude: number,
  destination_latitude: number,
  destination_longitude: number,
  distance: number,                       // Meters
  started_on: datetime
}
```

### Geographic Coordinates
```javascript
{
  origin: [latitude, longitude],          // Habitual trip origin
  destination: [latitude, longitude],     // Habitual trip destination
  limitMeter: 5000                       // 5km tolerance for matching
}
```

## Business Logic

### Validation Criteria
```javascript
const compensateProcess = async (compensation) => {
  const habituals = await getHabitualLatLon(compensation.experiment_id);
  const limitMeter = 5000;  // 5km radius for origin/destination matching
  
  const tripResult = await checkTrips(
    compensation.user_id,
    compensation.deliver_time,
    compensation.validate_time,
  );
  
  for (const trip of tripResult) {
    const originDistance = haversine(habituals.origin, [
      trip.origin_latitude,
      trip.origin_longitude,
    ]);
    const destinationDistance = haversine(habituals.destination, [
      trip.destination_latitude,
      trip.destination_longitude,
    ]);
    
    // Validation: within 5km of both origin and destination
    if (originDistance <= limitMeter && destinationDistance <= limitMeter) {
      // Trip qualifies for compensation
      return true;
    }
  }
  return false;
};
```

### Travel Mode Requirements
- **Eligible Modes**: Transit (2), Walking (3), Biking (4), Intermodal (5)
- **Excluded Modes**: Driving (1), Trucking (6), Other (7+)
- **Distance Requirement**: Minimum 1 mile (1609 meters) trip distance
- **Active Trip**: Must be active telework trip with auto-logging enabled

### Payment Processing
```javascript
// Calculate new balance
const currentBalance = parseFloat(pointsTransaction[0].balance);
const updateTripBalance = currentBalance + parseFloat(compensation.points);

// Create wallet transaction
const pointsTransactionId = await util.userWalletSync(compensation.user_id, {
  activity_type: 6,                       // Compensation activity
  points: parseFloat(compensation.points),
  balance: updateTripBalance,
  note: 'mtc trip compensation',
});

// Update compensation record
await knex('mtc_compensation').where('id', compensation.id).update({
  points_transaction_id: pointsTransactionId,
});
```

## Geographic Calculations

### Haversine Distance Formula
```javascript
const haversine = require('haversine-distance');

const originDistance = haversine(habituals.origin, [
  trip.origin_latitude,
  trip.origin_longitude,
]);

const destinationDistance = haversine(habituals.destination, [
  trip.destination_latitude,
  trip.destination_longitude,
]);
```

### Distance Thresholds
- **Trip Matching**: 5000 meters (5km) radius for origin/destination matching
- **Minimum Distance**: 1609 meters (1 mile) minimum trip length
- **Precision**: Meter-level accuracy for geographic validation

## Notification System

### Message Template Processing
```javascript
const mtcJSON = await util.getMarket('assets/' + project + '/mtc_tiles_new.json');
const mtcNotification = mtcJSON.MTC.sendcoins_message_content[0];

let msg = {};
msg.title = mtcNotification.title;
msg.body = mtcNotification.body;
msg.body = msg.body.replace('[$xx.xx]', compensation.points);

await util.sendNotification(msg, [compensation.user_id]);
```

### Notification Tracking
```javascript
await knex('mtc_compensation').where('id', compensation.id).update({
  msg_title: msg.title,
  msg_content: msg.body,
  deliver: 1,
});
```

## Database Operations

### Complex Join Queries
```javascript
// Campaign completion verification
const campaignResult = await knex('cm_campaign_user')
  .innerJoin('cm_campaign', 'cm_campaign_user.campaign_id', 'cm_campaign.id')
  .innerJoin('cm_user_record', 'cm_campaign_user.campaign_id', 'cm_user_record.campaign_id')
  .where('cm_campaign_user.campaign_id', campaignId)
  .andWhere('cm_user_record.reply_status', 2)
  .andWhere('cm_campaign_user.status', 3)
  .andWhere('cm_campaign_user.reply_status', 1);
```

### Transaction Management
```javascript
// Atomic compensation processing
await knex('mtc_compensation').where('id', compensation.id).update({
  campaign_incentive: 1,
  changed_mode: compensation.specified_mode,
  campaign_trip_id: trip[0].id,
  processed: 1,
});
```

## Error Handling

### Data Validation
```javascript
if (!(location.length > 0)) {
  logger.info('cm_location id not exist experimentId : ' + experimentId);
  return;
}

if (!(oLatLon.length > 0)) {
  logger.info('cm_location oID not exist : ' + oID);
  return;
}
```

### Graceful Degradation
```javascript
// Continue processing even if individual compensation fails
try {
  const passValidation = await compensateProcess(compensation);
  // Process compensation
} catch (error) {
  logger.error(`Compensation processing failed for ID ${compensation.id}: ${error.message}`);
  // Continue with next compensation
}
```

## Performance Considerations

### Batch Processing
- **Single Pass**: Processes all pending compensations in one execution
- **Efficient Queries**: Uses appropriate joins and indexes
- **Resource Management**: Controlled database connection usage

### Geographic Optimization
- **Haversine Calculations**: Optimized for large-scale distance computations
- **Index Usage**: Leverages spatial indexes where available
- **Memory Efficiency**: Processes trips sequentially to manage memory

## Integration Points

### Wallet Service
- **Balance Management**: Integrates with user wallet system
- **Transaction Logging**: Creates audit trail for all payments
- **Activity Tracking**: Records compensation activities

### Campaign System
- **Status Verification**: Checks campaign completion status
- **Trip Correlation**: Links campaigns to actual trip data
- **User Engagement**: Tracks user interaction with campaigns

### Notification Service
- **Message Delivery**: Sends compensation notifications
- **Template Processing**: Uses configurable message templates
- **Delivery Tracking**: Monitors notification delivery status

## Monitoring and Analytics
```javascript
console.log('mtcConfig : ', mtcNotification);
logger.info(`Processing compensation ID: ${compensation.id}`);
logger.info(`Trip validation result: ${passValidation}`);
```

## Usage Scenarios
- **Transportation Research**: Academic studies on mobility behavior change
- **Municipal Programs**: City-sponsored sustainable transportation initiatives
- **Corporate Mobility**: Employee transportation incentive programs
- **Environmental Initiatives**: Carbon reduction through mode shift rewards
- **Transit Optimization**: Public transit ridership enhancement programs

## Configuration Dependencies
- **Project Configuration**: `config.get('app.project')` for project-specific settings
- **MTC Notification Templates**: `assets/{project}/mtc_tiles_new.json`
- **Database Configuration**: MySQL portal database connection
- **Wallet Configuration**: Target table configuration for point transactions

## Notes
- **Research-Grade Validation**: Implements rigorous validation for academic research standards
- **Automated Processing**: Fully automated compensation workflow reduces manual intervention
- **Geographic Precision**: Uses professional-grade geographic calculations for accuracy
- **Financial Integration**: Seamless integration with user wallet and payment systems
- **Comprehensive Auditing**: Full audit trail for financial and research compliance
- **Scalable Architecture**: Designed for large-scale multi-city transportation programs