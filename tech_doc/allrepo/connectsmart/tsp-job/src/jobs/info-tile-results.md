# info-tile-results.js

## Overview
Job for analyzing and processing travel behavior change results from WTA (Washington Transit Agency) info tile experiments. This job validates whether users modified their travel behavior according to experimental suggestions by comparing actual trips with recommended travel modes and departure times.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/info-tile-results.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `@maas/core/mysql` - MySQL database connection (portal)
- `moment-timezone` - Timezone-aware date/time manipulation
- `@maas/core/log` - Structured logging utility

## Core Functions

### Main Processing Logic
Analyzes completed info tile experiments to determine behavior change effectiveness by:
- Matching actual trips with suggested travel modes
- Validating trip timing within 15-minute tolerance
- Calculating geographic proximity between suggested and actual routes
- Recording successful behavior changes for experiment tracking

### Behavior Change Detection
The job implements sophisticated logic to detect two types of behavior changes:
1. **Change Mode**: Same origin-destination (OD) pairs with travel mode matching tile suggestions
2. **Change Time**: Same OD pairs with driving mode and departure time within ±15 minutes

## Processing Flow

### 1. Experiment Results Query
```sql
SELECT
  GROUP_CONCAT(hybrid.trip.id SEPARATOR ',') AS trip_id,
  hybrid.wta_info_tile.id AS id,
  (CASE
    WHEN hybrid.wta_info_tile.travel_mode = 'transit' THEN 3
    WHEN hybrid.wta_info_tile.travel_mode = 'walking' THEN 2
    WHEN hybrid.wta_info_tile.travel_mode = 'bicycling' THEN 1
    ELSE 0
  END) AS suggestion,
  hybrid.trip.travel_mode,
  -- Geographic distance calculations for origin/destination validation
FROM hybrid.wta_info_tile LEFT JOIN hybrid.trip
  ON hybrid.wta_info_tile.user_id = hybrid.trip.user_id
WHERE hybrid.wta_info_tile.sent_process = 0 
  AND hybrid.wta_info_tile.results <= current_time
HAVING o_distance <= 300 AND d_distance <= 300
  AND hybrid.trip.started_on >= start_date 
  AND hybrid.trip.started_on <= end_date
  AND diff_time >= -900 AND diff_time <= 900
  AND suggestion = hybrid.trip.travel_mode
```

### 2. Geographic Validation
Uses Haversine formula to calculate distances between:
- **Origin Matching**: Tile suggestion origin vs actual trip origin (≤300m)
- **Destination Matching**: Tile suggestion destination vs actual trip destination (≤300m)

### 3. Temporal Validation
Validates trip timing using:
- **Time Difference**: `TIME_TO_SEC(timediff(trip_time, suggested_time))`
- **Tolerance Window**: ±900 seconds (15 minutes)
- **Date Range**: Trip must occur within experiment period

### 4. Travel Mode Mapping
```javascript
// Travel mode conversion for comparison
const travelModeMapping = {
  'transit': 3,    // Public transit
  'walking': 2,    // Walking
  'bicycling': 1,  // Cycling
  'driving': 0     // Default/baseline
};
```

## Data Models

### Experiment Results Structure
```javascript
{
  trip_id: "comma,separated,trip,ids",
  id: number,                    // wta_info_tile.id
  suggestion: number,            // Converted travel mode
  travel_mode: number,           // Actual trip mode
  o_lat: number,                 // Origin latitude
  o_lng: number,                 // Origin longitude
  origin_latitude: number,       // Trip origin latitude
  origin_longitude: number,      // Trip origin longitude
  o_distance: number,            // Origin distance (meters)
  d_lat: number,                 // Destination latitude
  d_lng: number,                 // Destination longitude
  destination_latitude: number,  // Trip destination latitude
  destination_longitude: number, // Trip destination longitude
  d_distance: number,            // Destination distance (meters)
  started_on: datetime,          // Trip start time
  diff_time: number,             // Time difference (seconds)
  trip_departure: time,          // Trip departure time
  start_date: datetime,          // Experiment start
  end_date: datetime            // Experiment end
}
```

### Database Updates
```sql
-- Record successful behavior change
UPDATE hybrid.wta_info_tile 
SET change_behavior = '{trip_ids}' 
WHERE id = '{tile_id}';

-- Mark experiment as processed
UPDATE hybrid.wta_info_tile 
SET sent_process = '1' 
WHERE results <= current_time;
```

## Validation Criteria

### Geographic Proximity
- **Origin Distance**: ≤300 meters from suggested origin
- **Destination Distance**: ≤300 meters from suggested destination
- **Calculation Method**: Haversine distance formula using latitude/longitude

### Temporal Matching
- **Time Window**: ±15 minutes from suggested departure time
- **Date Range**: Trip must occur between experiment start and end dates
- **Timezone Handling**: UTC-based time comparisons

### Mode Matching  
- **Exact Match**: Trip travel mode must exactly match tile suggestion
- **Mode Priority**: Transit (3) > Walking (2) > Bicycling (1) > Driving (0)

## Business Logic

### Experiment Phases
```javascript
// Phase 1: Info tile delivery (Week 1)
// Phase 4: Results analysis (Week 1 Saturday 00:00)
// Phase 5: Decision point for Phase 2 experiments
```

### Behavior Change Types
1. **Mode Change**: User switches from driving to suggested alternative mode
2. **Time Change**: User adjusts departure time by ±15 minutes while maintaining driving mode
3. **No Change**: User maintains original travel pattern

### Success Metrics
- **Trip Completion**: Must be completed trips (not planned or cancelled)
- **Geographic Accuracy**: Origin/destination within 300m tolerance
- **Temporal Accuracy**: Departure time within 15-minute window
- **Mode Compliance**: Exact match with suggested travel mode

## Integration Points

### Campaign Management System
- Links with `cm_campaign` and `cm_campaign_user` tables
- Tracks experiment completion status
- Manages user experiment lifecycle

### Trip Validation Engine
- Interfaces with trip validation systems
- Validates trip completion and accuracy
- Ensures data quality for analysis

### Activity Location Mapping
- Uses `cm_activity_location` for origin/destination mapping
- Integrates with `cm_location` for coordinate data
- Supports habitual trip pattern analysis

## Performance Considerations

### Query Optimization
- Uses GROUP_CONCAT for efficient trip ID aggregation
- LEFT JOIN structure minimizes unnecessary data retrieval
- HAVING clause filters results efficiently

### Geographic Calculations
- Haversine formula implemented in SQL for server-side processing
- Distance calculations cached within query results
- Optimized for large-scale trip matching

### Batch Processing
- Processes all eligible experiments in single execution
- Updates performed in batches for efficiency
- Minimizes database connection overhead

## Error Handling
- Graceful handling of missing location data
- Validates experiment date ranges before processing
- Comprehensive logging of all validation steps
- Continues processing despite individual record failures

## Monitoring and Logging
```javascript
console.log(SQL);              // Query logging
console.log(Rows);             // Results logging
console.log(Rows[index].id);   // Individual record processing
```

## Usage Scenarios
- **Research Analysis**: Academic research on travel behavior modification
- **Campaign Effectiveness**: Measuring success rates of mobility campaigns
- **Policy Evaluation**: Assessing impact of transportation policies
- **User Engagement**: Understanding user response to mobility suggestions

## Experiment Framework Integration
This job is part of the comprehensive WTA experiment framework:
1. **Phase 1**: Initial info tile delivery
2. **Phase 2**: Follow-up experiments if no behavior change
3. **Phase 4**: Results analysis (this job)
4. **Phase 5**: Decision point for experiment continuation

## Data Flow
```
Info Tile Delivery → User Behavior Period → Trip Data Collection → 
Results Analysis (this job) → Experiment Conclusion/Continuation
```

## Configuration Dependencies
- Database connection configuration for 'portal' MySQL instance
- Timezone configuration for accurate time comparisons
- Geographic coordinate systems for distance calculations

## Notes
- Designed specifically for WTA travel behavior experiments
- Implements rigorous validation criteria for research accuracy
- Supports multiple concurrent experiments per user
- Provides comprehensive audit trail for research reproducibility
- Critical component in measuring mobility intervention effectiveness