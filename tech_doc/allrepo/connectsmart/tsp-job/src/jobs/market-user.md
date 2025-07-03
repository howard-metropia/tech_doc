# market-user.js

## Overview
Job for managing user market assignments based on geographic location and updating user statistics. Synchronizes user data with market boundaries and maintains user activity metrics for incentive processing.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/market-user.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `@maas/core/mysql` - MySQL database connection (portal)
- `geo-point-in-polygon` - Geospatial point-in-polygon testing
- `@app/src/services/incentiveUtility` - Incentive utility functions
- `config` - Application configuration
- `moment` / `moment-timezone` - Date/time manipulation
- `@maas/core/log` - Logging utility

## Core Functions

### userInsertUpdate(row, marketGeo, incentiveEngine, userAPPData)
Main function for processing individual user market assignment and data updates.

**Parameters:**
- `row` - User compound data record
- `marketGeo` - Market geographic boundary configuration
- `incentiveEngine` - Incentive configuration by market
- `userAPPData` - User app usage data

**Process Flow:**
1. Extract user coordinates from app data
2. Check for existing market_user record
3. Determine if market recalculation is needed
4. Perform geospatial analysis to assign market
5. Update or insert user record with current stats

## Job Configuration

### Inputs
No input parameters required.

### Main Function
Processes all users for market assignment and statistics updates.

## Processing Flow

### 1. Data Collection
```javascript
const userComData = await util.getUserCompoundData();
const userAPPData = await util.getUserAppData(userComData[0], nowTime);
```

### 2. Configuration Loading
- Market geographic boundaries
- Incentive engine configurations per market
- Project-specific settings

### 3. User Processing
For each user in compound data:
- Perform market assignment geospatial analysis
- Update user statistics and trip data
- Configure incentive program parameters

## Market Assignment Logic

### Geographic Analysis
```javascript
if (geoPointInPolygon(userPoint, dataPolygon[j])) {
  userInMarket = targetMarket;
  break;
}
```

### Default Assignment
- Users outside defined markets get 'general' assignment
- First matching market takes precedence
- Handles overlapping polygon scenarios

### Recalculation Triggers
- Market configuration file is newer than user creation
- Ensures users get updated market assignments
- Updates creation timestamp after recalculation

## Data Models

### market_user Table
```javascript
{
  user_id: number,
  registration_latitude: number,
  registration_longitude: number,
  registered_on: datetime,
  user_in_market: string,
  has_trip: boolean,
  trip_count: number,
  last_trip_time: datetime,
  user_days: number,
  open_app_days: number,
  make_trip_days: number,
  trip_to_now: number,
  retention_status: number,
  created_on: datetime
}
```

### User Compound Data Structure
```javascript
{
  id: number,
  registration_latitude: number,
  registration_longitude: number,
  created_on: datetime,
  trips: number,
  last_trip_time: datetime,
  user_days: number,
  trip_to_now: number
}
```

## Business Logic

### New User Processing
- Assigns market based on registration coordinates
- Sets initial incentive program parameters
- Initializes user statistics and retention status

### Existing User Updates
- Preserves existing incentive day settings if non-zero
- Updates trip statistics and activity flags
- Recalculates market assignment if configuration changed

### Incentive Configuration Integration
```javascript
const openAppDays = incentiveEngine[userInMarket].Incentive1_1_open_app.End_days;
const makeTripDays = incentiveEngine[userInMarket].Incentive1_2_make_trip.End_days;
```

## Geographic Processing

### Point-in-Polygon Testing
- Tests user coordinates against market boundaries
- Supports complex polygon shapes
- Handles nested and overlapping markets

### Coordinate Sources
- Primary: User app data coordinates
- Fallback: Registration coordinates
- Uses most recent location data available

## Performance Optimizations

### Configuration Caching
- Loads market and incentive configurations once
- Reuses across all user processing
- Minimizes file system access

### Database Efficiency
- Batch processing of user data
- Single transaction per user update
- Optimized queries for compound data

## Error Handling
- Graceful handling of missing coordinates
- Database error logging and continuation
- Robust polygon calculation error handling

## Integration Points
- User compound data service
- App usage tracking system
- Market boundary management
- Incentive program configuration
- Retention analysis system

## Configuration Dependencies
- Market attribute JSON files
- Incentive engine configuration
- Project-specific settings
- Geographic boundary definitions

## Usage Scenarios
- Daily user market assignment updates
- New user onboarding processing
- Market boundary changes rollout
- User activity statistics maintenance

## Logging and Monitoring
- Start and end time logging
- Error tracking for database operations
- Processing completion timestamps

## Notes
- Designed for daily scheduled execution
- Supports multiple markets and geographic regions
- Maintains backward compatibility with existing users
- Optimized for large-scale user processing