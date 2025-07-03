# add-local-user-label.js

## Overview
Job module responsible for managing local user labels based on geographic activity analysis. This system automatically classifies users as local or non-local based on their registration location, app usage patterns, and travel behavior within defined service areas.

## Purpose
- Automatically classify users as local or non-local based on geographic activity
- Analyze user behavior across multiple data points (registration, app usage, trips)
- Manage user label transitions using state machine pattern
- Support region-specific bounding box configurations

## Key Features
- **Multi-Source Analysis**: Combines registration, app usage, and trip data
- **Geographic Filtering**: Uses project-specific bounding boxes for service areas
- **State Machine Integration**: Manages label transitions through controlled state changes
- **Comprehensive Checking**: Analyzes origins, destinations, and trajectory data
- **Project Flexibility**: Supports multiple deployment regions

## Dependencies
```javascript
const { logger } = require('@maas/core/log');
const service = require('@app/src/services/localUserLabel');
const AuthUserLabel = require('@app/src/models/AuthUserLabel');
const AppData = require('@app/src/models/AppData');
const User = require('@app/src/models/AuthUsers');
const Trip = require('@app/src/models/Trips');
```

## Geographic Configuration

### Bounding Box Definitions
```javascript
const boundingBox = {
  connectsmart: [
    [29.2, 30.45],      // Latitude range
    [-96.05, -94.3],    // Longitude range
  ],
  gomywayva: [
    [38.5, 39.15],      // Virginia area
    [-77.65, -76.9],
  ]
};
```

### Project Detection
```javascript
function getBoundingBox() {
  return boundingBox[process.env.PROJECT_TITLE.toLowerCase()] || null;
}
```

## Core Processing Functions

### 1. Initial User Scanning
```javascript
async function scanAll() {
  // Find users without labels or with non-local labels
  const list = await User.query()
    .leftJoin('auth_user_label', 'auth_user_label.user_id', 'auth_user.id')
    .whereNull('auth_user_label.label_id')
    .orWhereNotIn('auth_user_label.label_id', [2, 3]);
  
  // Set initial non-local status
  for (const user of list) {
    await service.setNonLocalUser(user.id);
  }
}
```

### 2. Registration Location Analysis
```javascript
async function checkRegistration() {
  // Check users with potential local status (label_id: 3)
  const list = await AuthUserLabel.query().where('label_id', 3);
  
  // Verify registration coordinates against service area
  if (service.checkServiceArea(lat, lon)) {
    service.getStateMachine(userId).send({ type: 'SWITCH_TO_LOCAL_USER' });
  }
}
```

### 3. App Usage Location Analysis
```javascript
async function checkOpenApp() {
  // Analyze OpenApp events within bounding box
  const appData = await AppData.query()
    .where('user_action', 'OpenApp')
    .whereBetween('lat', getBoundingBox()[0])
    .whereBetween('lon', getBoundingBox()[1]);
  
  // Check service area for app usage locations
}
```

### 4. Trip Origin Analysis
```javascript
async function checkOrigin(userId) {
  const trips = await Trip.query()
    .where('user_id', userId)
    .whereNotNull('origin_latitude')
    .whereBetween('origin_latitude', getBoundingBox()[0])
    .whereBetween('origin_longitude', getBoundingBox()[1]);
  
  // Verify trip origins against service area
}
```

### 5. Trip Destination Analysis
```javascript
async function checkDestination(userId) {
  const trips = await Trip.query()
    .where('user_id', userId)
    .whereNotNull('final_destination_latitude')
    .whereBetween('final_destination_latitude', getBoundingBox()[0])
    .whereBetween('final_destination_longitude', getBoundingBox()[1]);
  
  // Verify trip destinations against service area
}
```

## Label Classification System

### Label Types
- **Label ID 2**: Local user status
- **Label ID 3**: Potential local user (pending verification)
- **No Label**: Non-local user

### State Machine Transitions
```javascript
// Promote to local user status
service.getStateMachine(userId).send({ type: 'SWITCH_TO_LOCAL_USER' });

// Initial non-local classification
await service.setNonLocalUser(user.id);
```

## Processing Pipeline

### Main Execution Flow
```javascript
module.exports = {
  inputs: {},
  fn: async function () {
    await scanAll();           // Initialize unlabeled users
    await checkRegistration(); // Verify registration locations
    await checkOpenApp();      // Analyze app usage patterns
    await checkTrips();        // Check trip origins and destinations
  }
};
```

### Trip Analysis Pipeline
```javascript
async function checkTrips() {
  for (const user of potentialLocalUsers) {
    let result = await checkOrigin(userId);
    if (result) continue;
    
    result = await checkDestination(userId);
    if (result) continue;
    
    result = await checkTrajectory(userId);
    // Continue processing or move to next user
  }
}
```

## Performance Optimizations

### Database Efficiency
- Indexed queries on user_id and geographic coordinates
- Bounding box pre-filtering to reduce service area checks
- Batch processing with controlled sleep intervals

### Processing Control
```javascript
async function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Rate limiting between operations
await sleep(3 * 1000);
```

## Error Handling Strategy
```javascript
try {
  // Process user analysis
} catch (e) {
  logger.error(`[checkTrips] User: ${userId}, ${e.message}`);
  logger.info(`[checkTrips] ${e.stack}`);
  continue; // Continue with next user
}
```

### Resilience Features
- Individual user error isolation
- Comprehensive error logging with stack traces
- Graceful degradation for missing data
- Process continuation despite individual failures

## Integration Points
- **Local User Label Service**: Core business logic and state management
- **Database Models**: User, trip, and app data access
- **State Machine Service**: Controlled label transitions
- **Geographic Service**: Service area validation

## Monitoring and Logging
- Process start and completion tracking
- User-specific operation logging
- Error frequency and pattern analysis
- Geographic analysis result tracking

## Usage Patterns
- Scheduled execution for batch user classification
- New user onboarding label assignment
- Periodic re-evaluation of user classifications
- Service area expansion support

## Business Logic
- Local users receive enhanced service features
- Geographic analysis ensures accurate service targeting
- Multi-factor verification improves classification accuracy
- Automated system reduces manual intervention requirements