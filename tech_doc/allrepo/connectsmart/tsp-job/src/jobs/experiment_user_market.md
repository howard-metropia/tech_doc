# experiment_user_market.js

## Overview
Job for synchronizing user experiment assignments based on geographic market boundaries. Maps users who agreed to WTA (Washington Transit Agency) experiments to appropriate market regions using geospatial analysis.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/experiment_user_market.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `@maas/core/mysql` - MySQL database connection (portal)
- `moment` - Date/time manipulation
- `geo-point-in-polygon` - Geospatial point-in-polygon testing
- `@app/src/services/incentiveUtility` - Market utility functions
- `config` - Application configuration

## Core Functions

### getWtaAgreeUsers()
Retrieves users who agreed to WTA experiments, with time-based filtering for efficiency.

**Returns:** Array of user records from `wta_agree` table

**Logic:**
- On first run: Returns all users with `wta_agree = 1`
- On subsequent runs: Returns users modified in last 3 hours
- Uses `experiment_user_market` table count to determine first run

### getUserLocations(userId)
Fetches all recorded locations for a specific user.

**Parameters:**
- `userId` - Target user ID

**Returns:** Array of location records from `cm_location` table

### experimentSync(userId, row)
Synchronizes user experiment assignment, preventing duplicates.

**Parameters:**
- `userId` - Target user ID
- `row` - Experiment data object with experiment name and timezone

**Process:**
1. Check if user-experiment combination exists
2. Insert new record if not found
3. Prevents duplicate experiment assignments

## Job Configuration

### Inputs
No input parameters required.

### Main Function
Processes all WTA-agreed users against all available market polygons.

## Processing Flow

### 1. Market Data Loading
```javascript
const marketGeo = await util.getMarket(
  'assets/' + project + '/market_attribute.json'
);
```

### 2. User Data Retrieval
- Get all users who agreed to WTA experiments
- Filter based on modification time for efficiency

### 3. Geographic Processing
For each market in `Market_info`:

1. **Extract Market Data:**
   - Market name/identifier
   - Timezone information
   - Polygon coordinates

2. **Polygon Validation:**
   - Check if market has coordinate data
   - Skip markets without polygon information

3. **User Location Testing:**
   - For each user location
   - Test if point falls within market polygon
   - Assign user to market experiment if within bounds

### 4. Experiment Assignment
```javascript
if (geoPointInPolygon([longitude, latitude], polygon)) {
  await experimentSync(userId, {
    experiment: targetMarket,
    timezone: timezone
  });
}
```

## Data Models

### wta_agree Table
```javascript
{
  user_id: number,
  wta_agree: number, // 1 = agreed
  modified_on: datetime
}
```

### cm_location Table
```javascript
{
  user_id: number,
  longitude: number,
  latitude: number
}
```

### experiment_user_market Table
```javascript
{
  user_id: number,
  experiment: string, // Market identifier
  timezone: string
}
```

### Market Configuration Structure
```javascript
{
  Market_info: {
    [marketKey]: {
      Market: string,
      Timezone: string,
      coordinates: [
        [
          [
            [longitude, latitude], // Polygon points
            ...
          ]
        ]
      ]
    }
  }
}
```

## Geographic Analysis

### Point-in-Polygon Testing
Uses `geo-point-in-polygon` library for spatial analysis:
- Tests user coordinates against market boundaries
- Supports complex polygon shapes
- Handles multiple polygon rings per market

### Market Polygon Structure
- Nested coordinate arrays support complex shapes
- Multiple polygons per market supported
- GeoJSON-compatible coordinate format

## Business Logic

### First Run Behavior
- When `experiment_user_market` table is empty
- Processes all historical WTA-agreed users
- Establishes baseline experiment assignments

### Incremental Updates
- Processes only recently modified users
- Uses 3-hour lookback window
- Optimizes performance for scheduled runs

### Duplicate Prevention
- Checks existing experiment assignments
- Prevents duplicate user-experiment records
- Maintains data integrity

## Performance Optimizations

### Time-Based Filtering
- Processes only recent changes after initial run
- Reduces processing load on scheduled executions

### Nested Loop Optimization
- Processes markets sequentially
- Batches user location queries
- Minimizes database calls

## Error Handling
- Graceful handling of missing market data
- Continues processing if individual operations fail
- No explicit error logging (relies on system logging)

## Integration Points
- WTA agreement tracking system
- User location tracking
- Market boundary management
- Experiment assignment system

## Configuration Dependencies
- Project-specific market attribute files
- Geographic boundary data
- Timezone configurations

## Usage Scenarios
- Daily synchronization of user experiments
- Geographic market expansion
- User mobility pattern analysis
- Experiment population management

## Notes
- Designed for geographic experiment assignment
- Supports multiple markets and timezones
- Optimized for incremental processing
- Requires accurate location data for proper assignment