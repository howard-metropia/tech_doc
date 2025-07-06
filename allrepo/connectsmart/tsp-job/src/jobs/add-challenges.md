# add-challenges.js

## Overview
Job module responsible for adding challenges to the bingo card system. This job manages the automatic addition of challenges for users across different regional deployments and maintains the challenge distribution system.

## Purpose
- Add new challenges to the bingo card system
- Manage challenge distribution across different regions
- Support both global and region-specific challenge deployment
- Maintain automated challenge lifecycle management

## Key Features
- **Global Challenge Distribution**: Supports challenges available to all users
- **Error Handling**: Comprehensive error catching and logging
- **Service Integration**: Leverages bingo card service for challenge management
- **Flexible Deployment**: Originally PD-specific, now globally available

## Dependencies
```javascript
const { logger } = require('@maas/core/log');
const config = require('config').project;
const { addToChallengeSBTest, addToChallengePD } = require('@app/src/services/bingocard');
```

## Core Function Structure
```javascript
module.exports = {
  inputs: {},
  fn: async function () {
    // Process challenge addition with error handling
    // Execute global challenge distribution
    // Log results and handle exceptions
  }
};
```

## Processing Logic

### Main Execution Flow
1. **Initialize**: Start challenge addition process
2. **Execute**: Call bingo card service to add challenges
3. **Log Results**: Record successful challenge additions
4. **Error Handling**: Catch and log any processing errors

### Challenge Addition Process
```javascript
// Originally region-specific, now global
const result = await addToChallengePD();
logger.info(`[addChallenges] result: ${JSON.stringify(result)}`);
```

## Service Integration

### Bingo Card Service Methods
```javascript
// Available service methods
const { 
  addToChallengeSBTest,  // Test environment challenges
  addToChallengePD       // Production/Global challenges
} = require('@app/src/services/bingocard');
```

### Current Implementation
- Uses `addToChallengePD()` for global challenge distribution
- Previously limited to PD region, expanded globally as of 2024-11-19
- Alternative test method available for development environments

## Error Handling Strategy
```javascript
try {
  const result = await addToChallengePD();
  logger.info(`[addChallenges] result: ${JSON.stringify(result)}`);
} catch (e) {
  logger.error(`[addChallenges] error: ${e.message}`);
  logger.info(`[addChallenges] stack: ${e.stack}`);
}
```

## Logging and Monitoring

### Log Events
- **Start**: `[addChallenges] start` - Process initiation
- **Success**: `[addChallenges] result: {...}` - Successful execution with results
- **Error**: `[addChallenges] error: {...}` - Error message logging
- **Debug**: `[addChallenges] stack: {...}` - Stack trace for debugging

### Monitoring Points
- Process start and completion tracking
- Result data structure logging
- Error frequency and types
- Service response time monitoring

## Configuration
- Uses project configuration from `config` module
- Flexible deployment across different environments
- Region-agnostic challenge distribution

## Historical Context
- **Before 2024-11-19**: Limited to PD (specific region) only
- **After 2024-11-19**: Changed to globally available across all regions
- Maintains backward compatibility with regional configurations

## Integration Points
- **Bingo Card Service**: Primary integration for challenge management
- **Configuration System**: Project-specific settings and parameters
- **Logging System**: Comprehensive activity and error logging
- **Job Scheduler**: Automated execution timing

## Usage Patterns
- Scheduled execution for regular challenge updates
- Batch processing of challenge additions
- Global distribution of new user engagement content
- Maintenance of active challenge inventory

## Business Logic
- Automated challenge distribution to maintain user engagement
- Global availability ensures consistent user experience
- Service-based architecture allows for flexible challenge types
- Error resilience maintains system stability

## Performance Considerations
- Lightweight execution with minimal resource requirements
- Efficient service calls to bingo card system
- Proper error handling prevents job failures
- Comprehensive logging for operational monitoring

## Deployment Notes
- Safe for global deployment across all regions
- Compatible with existing bingo card infrastructure
- Maintains service separation for testing environments
- Flexible configuration support for different deployments

## Future Enhancements
- Potential for region-specific challenge customization
- Support for different challenge types and categories
- Enhanced error recovery and retry mechanisms
- Advanced analytics and success tracking