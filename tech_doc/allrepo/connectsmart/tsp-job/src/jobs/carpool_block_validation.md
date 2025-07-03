# carpool_block_validation.js

## Overview
Job module that performs carpool block validation processing through trajectory analysis. This job runs every 3 minutes to validate carpool trip blocks and ensure data integrity for carpool matching and verification systems.

## Purpose
- Validate carpool trip blocks for data integrity
- Process trajectory data for carpool verification
- Maintain carpool matching accuracy through regular validation
- Support real-time carpool validation workflows

## Key Features
- **Frequent Execution**: Designed for 3-minute intervals for near real-time processing
- **Trajectory Integration**: Leverages trajectory service and DAO for spatial analysis
- **Error Resilience**: Comprehensive error handling with detailed logging
- **Service Delegation**: Clean separation through trajectory service architecture

## Dependencies
```javascript
const { logger } = require('@maas/core/log');
const service = require('@app/src/services/trajectoryService');
const dao = require('@app/src/services/trajectoryDao');
```

## Core Function Structure
```javascript
module.exports = {
  inputs: {},
  fn: async function() {
    // Run every 3 minutes for carpool validation
    logger.info('[carpool_block_validation] start');
    service.setDao(dao);
    await service.carpoolBlockValidationJob();
    logger.info('[carpool_block_validation] end');
  }
};
```

## Processing Logic
- Service configuration with trajectory DAO
- Carpool block validation through trajectory service
- Error handling with stack trace logging
- Process timing and status logging

## Service Integration
- **Trajectory Service**: Core validation logic provider
- **Trajectory DAO**: Data access layer for spatial queries
- **Dependency Injection**: DAO set into service for flexibility

## Execution Schedule
- **Frequency**: Every 3 minutes
- **Purpose**: Near real-time carpool validation
- **Performance**: Optimized for frequent execution

## Error Handling
```javascript
try {
  await service.carpoolBlockValidationJob();
} catch(e) {
  logger.error(`[carpool_block_validation] ${e.message}`);
  logger.warn(e.stack);
}
```

## Integration Points
- Trajectory analysis system
- Carpool matching algorithms
- Data validation pipelines
- Real-time processing infrastructure

## Operational Notes
- Lightweight execution for frequent scheduling
- Minimal resource requirements
- Compatible with high-frequency job scheduling
- Service-level business logic isolation