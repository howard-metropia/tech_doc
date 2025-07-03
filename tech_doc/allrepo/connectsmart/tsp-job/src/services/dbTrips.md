# Database Trips Service

## Overview

The Database Trips service manages comprehensive trip data synchronization from portal to analytics databases, handling trips, reservations, and telework data with extensive data transformation and schema migration capabilities.

## Service Information

- **Service Name**: Database Trips
- **File Path**: `/src/services/dbTrips.js`
- **Type**: Data Synchronization Service
- **Dependencies**: Moment.js, InfluxDB, Multiple Trip Models

## Core Functions

### writeDBTrip(start, end)

Main synchronization function for trip data migration.

**Purpose**: Transfers trip data from portal to analytics database
**Parameters**:
- `start` (string): Start date filter (optional)
- `end` (string): End date filter (optional)

**Process Selection**:
- **writeByUser()**: For complete rebuilds or custom date ranges
- **writeByTrip()**: For incremental daily updates

### Data Processing Functions

#### getTripObject(trip, fromScratch)
Transforms trip records into DBTrips format with comprehensive data enrichment:
- **Travel Mode Mapping**: Converts mode IDs to boolean flags
- **Distance Calculation**: Uses trajectory_distance when available
- **Route History**: Fetches detailed route information
- **Rating Integration**: Links user ratings and comments
- **Points Calculation**: Queries incentive campaign points
- **Completion Status**: Determines verification status

#### getReservationObj(oneRev, fromScratch)
Processes reservation data for analytics:
- **Action Type**: Set to 2 for reservations
- **Travel Mode**: Maps reservation modes to standard format
- **Location Data**: Preserves origin/destination coordinates

#### getTeleworkObj(oneTelework, fromScratch)
Handles telework/manual trip entries:
- **Mode Support**: Extensive travel mode mapping including strings
- **Manual Entry**: LogOrActual = 1 for manual entries
- **Distance Conversion**: Meters to miles conversion
- **Date Standardization**: Uses trip_date for timing

## Database Schema Management

### Schema Migration Scripts
- **scriptMet11675()**: Adds is_HGAC column and trajectory distance updates
- **scriptMet13160()**: Adds add_log_time column for creation tracking
- **scriptMet16233()**: Adds travel_mode and navigation_app columns
- **scriptMet16463()**: Adds car_navigation_system column
- **scriptMet16489()**: Adds trip_completion verification status

### Default Object Structure
```javascript
const DBTRIP_DEFAULT_OBJECT = {
  UserID: 0, TripID: '(N/A)', Action: 0,
  StartTimeSearch: null, OriginPOI: '', OriginLat: 0,
  ModeDriving: 0, ModeTransit: 0, ModeWalking: 0,
  ModeCycling: 0, ModeCarpool: 0, ModeTelework: 0,
  // ... additional 30+ fields
};
```

## Travel Mode Processing

### Mode Mapping
- **1**: Driving (ModeDriving = 1)
- **2**: Transit (ModeTransit = 1)
- **3**: Walking (ModeWalking = 1)
- **4**: Cycling (ModeCycling = 1)
- **100/101**: Carpool (ModeCarpool = 1)
- **5-8**: Extended modes (intermodal, trucking, park_and_ride, ridehail)

### String Mode Support (Telework)
- **'driving', 'transit', 'walking', 'cycling'**: Standard modes
- **'carpool_driver', 'carpool_rider'**: Carpool variations
- **'instant_carpool_driver', 'instant_carpool_rider'**: Instant carpool
- **'telework'**: Remote work (ModeTelework = 1)

## Data Validation

### Duplicate Prevention
```javascript
const isInDBTrip = async (userId, OriginPOI, DestPOI, StartTimeSearch, StartTimeSchedule) => {
  // Checks for existing trips to prevent duplicates
  // Uses binary UserID comparison for accuracy
};
```

### User Validation
- **isInDBUser()**: Ensures user exists in analytics database
- **Hash ID**: Secure user identifier transformation
- **America Timezone Filter**: Regional user filtering

## Performance Optimization

### Batch Processing
- **writeByUser()**: 100 users per batch for memory efficiency
- **writeByTrip()**: 1000 trips per batch for speed
- **Schema Updates**: Chunked processing for large datasets

### Processing Strategies
- **Incremental**: Daily updates using last processed date
- **Full Rebuild**: Complete data synchronization from specified date
- **User-Based**: Memory-efficient processing for large datasets

## Data Enrichment

### Route Details
- **MongoDB Integration**: Fetches route history from routes_historys
- **Distance Calculation**: Sums step distances for search distance
- **ETA Processing**: Extracts estimated arrival times

### Point System Integration
- **Campaign Points**: Links to incentive campaigns
- **SQL Joins**: Complex queries across trip, step, and record tables
- **Point Calculation**: Aggregates earned points per trip

### Verification Status
- **Telework Integration**: Checks auto-verification status
- **Completion Flag**: Determines if trip was verified
- **Status Values**: 'completed', 'incomplete', '(N/A)'

## Error Handling

### Data Integrity
- **Duplicate Detection**: Prevents re-insertion of existing records
- **Transaction Safety**: Database transactions for consistency
- **Schema Validation**: Ensures column existence before updates

### Monitoring
- **InfluxDB Metrics**: Records processing statistics
- **Progress Logging**: Detailed batch processing logs
- **Success Tracking**: Counts for trips, reservations, telework

## Integration Points

### Used By
- Analytics and reporting systems
- Trip behavior analysis
- Transportation planning studies
- User engagement tracking

### External Dependencies
- **Multiple Models**: Trip, Reservation, Telework, Rating data
- **MongoDB**: Route history storage
- **InfluxDB**: Performance monitoring
- **Hash Helper**: User ID anonymization

## Usage Guidelines

1. **Date Ranges**: Use incremental processing for daily updates
2. **Memory Management**: Use writeByUser for large datasets
3. **Schema Updates**: Run migration scripts for new columns
4. **Monitoring**: Check InfluxDB metrics for job health
5. **Data Quality**: Validate trip completion and verification status

## Dependencies

- **Moment.js**: Date manipulation and timezone conversion
- **Multiple Models**: Trip, Reservation, Telework, Rating models
- **InfluxDB**: Performance monitoring and metrics
- **Hash Helper**: User ID anonymization
- **Portal/Dataset Databases**: Source and target data stores