# m3_compensation Job Documentation

## Overview
The m3_compensation job processes M3 experiment compensation validation and reward distribution. It validates participant trip behavior against experimental conditions and automatically distributes point rewards for successful behavior modifications.

## Core Functionality

### Compensation Validation System
- Validates M3 experiment participant behavior changes
- Processes compensation based on trip validation
- Manages point distribution for successful interventions
- Coordinates campaign-based and trip-based reward systems

### Trip Validation Process
- Analyzes participant trips against habitual patterns
- Validates geographic proximity to experimental origins/destinations
- Confirms minimum distance requirements (>1 mile)
- Verifies transportation mode changes

## Processing Architecture

### Compensation Selection
```javascript
const getCompensations = async () => {
  return await knex('m3_compensation')
    .where('processed', 0)
    .andWhere('validate_time', '<=', currentDate);
};
```

### Geographic Validation
- **Origin Validation**: Checks proximity to habitual trip origins
- **Destination Validation**: Confirms destination accuracy
- **Distance Threshold**: 5km proximity requirement
- **Minimum Trip Distance**: 1 mile (1609.344m) requirement

### Trip Analysis Algorithm
```javascript
const compensateProcess = async (compensation) => {
  const habituals = await getHabitualLatLon(compensation.experiment_id);
  const limitMeter = 5000;
  
  const tripResult = await checkTrips(
    compensation.user_id,
    compensation.deliver_time,
    compensation.validate_time
  );
  
  // Distance validation using Haversine formula
  for (let trip of tripResult) {
    const originDistance = haversine(habituals.origin, [
      trip.origin_latitude, trip.origin_longitude
    ]);
    const destinationDistance = haversine(habituals.destination, [
      trip.destination_latitude, trip.destination_longitude
    ]);
    
    if (originDistance <= limitMeter && destinationDistance <= limitMeter) {
      return true; // Validation passed
    }
  }
};
```

## Compensation Types

### Campaign-Based Compensation
- **Campaign Validation**: Checks campaign completion and point earning
- **Card Correlation**: Links campaign steps to trip records
- **Status Updates**: Tracks campaign incentive status
- **Trip Association**: Correlates campaigns with actual trips

### Trip-Based Compensation
- **Direct Validation**: Validates trips against experimental parameters
- **Geographic Matching**: Confirms trip origin/destination proximity
- **Mode Verification**: Checks transportation mode compliance
- **Point Distribution**: Automatic reward distribution for valid trips

## Reward Distribution System

### Point Calculation
- **Balance Management**: Calculates current user point balance
- **Compensation Amount**: Applies configured compensation points
- **Transaction Creation**: Creates point transaction records
- **Wallet Synchronization**: Updates user wallet balance

### Notification System
```javascript
let msg = {};
msg.title = m3Notification.title;
msg.body = m3Notification.body.replace('[$xx.xx]', compensation.points);
await util.sendNotification(msg, [compensation.user_id]);
```

## Database Operations

### Cluster Trip Analysis
- **MongoDB Integration**: Queries ClusterTrips collection
- **Geographic Extraction**: Retrieves common start/end locations
- **Coordinate Transformation**: Converts MongoDB coordinates to lat/lon
- **Spatial Analysis**: Calculates geographic proximity

### Transaction Management
- **Points Transaction**: Creates reward transaction records
- **Balance Updates**: Maintains accurate user point balances
- **Audit Trail**: Preserves compensation processing history
- **Status Tracking**: Updates processing completion status

## Integration Points

### External Services
- **Wallet Service**: Point balance and transaction management
- **Notification Service**: User notification delivery
- **Cluster Analysis**: Trip pattern recognition
- **Geographic Services**: Haversine distance calculations

### Configuration Management
- **Market Configuration**: Market-specific compensation settings
- **Message Templates**: Localized notification content
- **Validation Parameters**: Geographic and distance thresholds
- **Reward Amounts**: Configurable compensation values

## Validation Logic

### Trip Qualification Criteria
1. **Distance Requirement**: Minimum 1 mile trip distance
2. **Geographic Proximity**: Within 5km of habitual locations
3. **Time Window**: Within experiment validation period
4. **Mode Compliance**: Matches specified transportation modes
5. **Activity Status**: Active telework logging required

### Error Handling
- **Geographic Data Missing**: Graceful handling of missing coordinates
- **Trip Validation Failure**: Proper status updates for failed validation
- **Notification Errors**: Error handling for failed notifications
- **Database Failures**: Transaction rollback and error recovery

## Performance Optimization
- **Batch Processing**: Efficient processing of multiple compensations
- **Database Indexing**: Optimized queries for large datasets
- **Memory Management**: Efficient handling of geographic calculations
- **Connection Pooling**: Optimized database connection usage

## Monitoring and Logging
- **Process Tracking**: Comprehensive logging of compensation processing
- **Validation Results**: Detailed logging of trip validation outcomes
- **Error Logging**: Complete error capture and stack traces
- **Performance Metrics**: Processing time and success rate tracking

## Business Logic

### Compensation Eligibility
- **Experiment Participation**: Active M3 experiment enrollment
- **Behavior Change**: Verified transportation behavior modification
- **Geographic Compliance**: Trip proximity to experimental parameters
- **Temporal Compliance**: Trips within validation time windows

### Reward Distribution
- **Automatic Processing**: Hands-free compensation distribution
- **Fraud Prevention**: Multiple validation layers for legitimacy
- **User Notification**: Immediate notification of earned rewards
- **Audit Compliance**: Complete transaction tracking

## Related Components
- **M3 Experiment System**: Experimental framework and management
- **Wallet Service**: Point transaction and balance management
- **Trip Analysis Engine**: Transportation behavior analytics
- **Notification System**: User communication and engagement

## Future Enhancements
- **Machine Learning Validation**: AI-powered trip pattern recognition
- **Real-time Processing**: Immediate compensation validation
- **Advanced Analytics**: Enhanced behavior change measurement
- **Multi-modal Analysis**: Complex transportation pattern recognition
- **Predictive Modeling**: Proactive compensation optimization