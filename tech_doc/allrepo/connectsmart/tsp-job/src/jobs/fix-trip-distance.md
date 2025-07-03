# Fix Trip Distance Job

## Overview
Job that automatically corrects missing or incorrect distance values in trip data by utilizing routing APIs (HERE Maps and Google Maps) to calculate accurate distances between origin and destination points. This job addresses data quality issues related to MET-13816 where trip distances are recorded as zero or invalid values.

## File Location
`/src/jobs/fix-trip-distance.js`

## Dependencies
- `moment-timezone` - Date/time manipulation and timezone handling
- `@maas/core/log` - Logging framework for operational monitoring
- `@app/src/models/Teleworks` - Telework trip data model
- `@app/src/models/TeleworkLogs` - Telework activity logs model
- `@app/src/models/Trips` - Main trip data model
- `@app/src/services/hereAPI` - HERE Maps routing service integration
- `@app/src/services/googleMap` - Google Maps direction service integration
- `@app/src/helpers/calculate-geodistance` - Geodesic distance calculation utility

## Job Configuration

### Inputs
```javascript
inputs: {
  manually: String  // Controls data source: 'false' for routine job, date string for manual execution
}
```

### Processing Logic
- **Routine Mode** (`manually: 'false'`): Processes previous day's data
- **Manual Mode** (date string): Processes data from specified date

## Core Distance Calculation Function

### fixTripDistance()
**Purpose**: Calculates accurate trip distance using multiple routing services with fallback strategy

**Parameters**:
```javascript
fixTripDistance(originLat, originLon, destinationLat, destinationLon, travelMode)
```

**Distance Calculation Strategy**:
1. **Direct Distance Check**: Calculate straight-line distance using geodesic calculation
2. **Minimum Distance Filter**: Skip routing if distance < 10 meters
3. **HERE Maps Routing**: Primary routing service with mode mapping:
   - `cycling` → `bicycle`
   - Other modes → `car`
4. **Google Maps Fallback**: Secondary routing service with comprehensive mode mapping:
   - `cycling` → `bicycling`
   - `walking` → `walking`
   - Default → `driving`

### Distance Validation Logic
```javascript
const MIN_DISTANCE = 10;
distance = calcDistance(originLon, originLat, destinationLon, destinationLat);
if (isNaN(distance)) return 0;
distance = parseInt(distance, 10);
```

## Routing Service Integration

### HERE Maps API Call
```javascript
const hereResult = await hereRouting(
  routeMode,
  `${originLat},${originLon}`,
  `${destinationLat},${destinationLon}`,
  'summary',
  'tsp-job-fix-trip-distance'
);
```

### Google Maps API Call
```javascript
const googleInput = {
  origin: `${originLat},${originLon}`,
  destination: `${destinationLat},${destinationLon}`,
  mode: routeMode
};
const googleResult = await fetchGoogleRoute(googleInput, 'tsp-job-fix-trip-distance');
```

## Data Processing Workflow

### Phase 1: Telework Logs Processing
**Query Logic**:
```javascript
const raws = await Teleworks.query()
  .select(
    'telework.id',
    'telework.trip_id',
    'telework_log.id as telework_log_id',
    'telework_log.travel_mode',
    'telework_log.origin_lat',
    'telework_log.origin_lng',
    'telework_log.destination_lat',
    'telework_log.destination_lng',
    'telework_log.distance'
  )
  .leftJoin('telework_log', 'telework_log.telework_id', 'telework.id')
  .where('telework.created_on', '>=', startDate)
  .where('telework_log.travel_mode', '<>', 'ridehail')
  .where('distance', 0);
```

**Processing Steps**:
1. Fetch telework records with zero distance
2. Exclude ridehail trips (handled separately)
3. Calculate distance for each record
4. Update telework_log distance
5. Update corresponding trip distance if also zero

### Phase 2: Trip Records Processing
**Query Logic**:
```javascript
const trips = await Trips.query()
  .where('ended_on', '>=', startDate)
  .where('distance', '<=', 0);
```

**Update Criteria**:
```javascript
if (trip.distance < 0 || (trip.distance === 0 && distance > 0)) {
  await Trips.query().update({ distance }).where('id', trip.id);
}
```

## Travel Mode Mapping

### HERE Maps Mode Conversion
```javascript
routeMode = travelMode === 'cycling' ? 'bicycle' : 'car';
```

### Google Maps Mode Conversion
```javascript
switch (travelMode) {
  case 'cycling':
    routeMode = 'bicycling';
    break;
  case 'walking':
    routeMode = 'walking';
    break;
  default:
    routeMode = 'driving';
}
```

## Error Handling and Logging

### Distance Validation
```javascript
if (isNaN(distance)) return 0;
logger.info(`The distance from Here: ${distance}`);
logger.info(`The distance from Google: ${distance}`);
```

### Processing Statistics
```javascript
logger.info(`Fetch data from ${startDate} length:${raws.length}`);
logger.info(`Updated telework count: ${updateTeleworkIds.length} ids: [${updateTeleworkIds}]`);
logger.info(`Updated trips count: ${updateTripIds.length} ids: [${updateTripIds}]`);
```

## Data Quality Improvements

### Telework Distance Correction
- Identifies telework logs with zero distance values
- Excludes ridehail trips (external service provides distance)
- Updates both telework_log and related trip records

### Trip Distance Correction
- Processes trips with distance ≤ 0
- Handles both negative distances (data errors) and zero distances (missing data)
- Travel mode inference: cycling (mode 4) vs driving (default)

## Performance Considerations

### API Rate Limiting
- Sequential processing to avoid API rate limits
- Service identification for API usage tracking
- Fallback strategy reduces API dependency

### Database Efficiency
- Targeted queries with date and distance filters
- Batch processing with progress tracking
- Separate processing phases for different data types

## Integration Points

### External Services
- HERE Maps routing API for primary distance calculation
- Google Maps Directions API for fallback routing
- Geodesic distance calculation for validation

### Data Models
- Teleworks and TeleworkLogs: Employee commute data
- Trips: General trip tracking data
- Cross-referencing via trip_id relationships

## Schedule Context
Typically scheduled to run daily in routine mode to automatically correct distance data quality issues. Can be executed manually for specific date ranges when data correction is needed for historical records.

## Business Impact
- Improves trip data accuracy for analytics and reporting
- Ensures proper mileage tracking for telework programs
- Maintains data quality for business intelligence and user experience features
- Supports accurate carbon footprint and sustainability reporting