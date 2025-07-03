# HNTB ETL Service

## Overview

The HNTB ETL service manages comprehensive data synchronization between portal and analytics databases for the Houston HNTB (Harkins New Transportation Bureau) project, processing user activities, trips, ratings, and transit data with geographic validation.

## Service Information

- **Service Name**: HNTB ETL
- **File Path**: `/src/services/hntb-etl.js`
- **Type**: Data Synchronization Service
- **Dependencies**: Moment.js, Turf.js, MongoDB, MySQL, Multiple Models

## Configuration

### Geographic Boundaries
- **US Coordinates**: Filters to continental United States
- **Latitude**: 24.520833 to 49.384358
- **Longitude**: -124.848974 to -66.885444
- **County Detection**: Uses GeoJSON county boundaries
- **Service Area**: Validates against market profile polygon

### Batch Processing
- **BATCH_SIZE**: 1000 records per iteration
- **Date Ranges**: Configurable start/end dates with intelligent defaults
- **User Filtering**: Target user identification and exclusion lists

## Core Functions

### checkTargetUser()

Identifies and synchronizes target users for HNTB analysis.

**Purpose**: Maintains list of local users excluding internal accounts
**Process**:
1. Identifies local_user and internal_user labels
2. Finds new local users not in target table
3. Excludes internal users from target list
4. Triggers full data sync for new target users

### syncTrip(start, end, excludeUserIds, assignUserId)

Synchronizes trip data with service area validation.

**Purpose**: Transfers trip records for target users within service boundaries
**Validation**:
- Geographic boundary filtering
- Service area validation via incentive engine
- Excludes trips with specific failed reasons
- County detection for origin points

### syncRating(start, end, excludeUserIds, assignUserId)

Synchronizes user rating data for completed trips.

**Purpose**: Transfers rating records linked to valid trips
**Features**:
- Links ratings to trip data
- Service area validation
- Travel mode preservation
- Geographic filtering

### Data Synchronization Functions

#### syncBytemarkPass()
- **Purpose**: Transit pass usage tracking
- **Data**: Pass usage times and user associations
- **Joins**: Links passes to orders and users

#### syncBytemarkOrderPayments()
- **Purpose**: Transit payment transaction tracking
- **Data**: Payment types, amounts, and timestamps
- **Fields**: Order IDs, payment methods, prices

#### syncTowAndGo()
- **Purpose**: Roadside assistance event tracking
- **Data**: Tow service requests and locations
- **Validation**: Service area geographic filtering

#### syncSchoolZone()
- **Purpose**: School zone interaction tracking
- **Data**: Entry events and speeding violations
- **Source**: User action events from MongoDB

#### syncPreTripAlert()
- **Purpose**: Alert interaction tracking
- **Data**: Alert sends and user read actions
- **Events**: Incident, closure, and flood alerts

## Geographic Processing

### County Detection
```javascript
const checkCounty = (lat, lon) => {
  // Uses GeoJSON features for county identification
  // Supports Polygon and MultiPolygon geometries
  // Returns county name or empty string
}
```

### Service Area Validation
```javascript
const checkArea = (lat, lon) => {
  // Uses market profile polygon
  // Turf.js point-in-polygon validation
  // WKT polygon parsing
}
```

## Data Processing Pipeline

### User Identification
1. **Target User Detection**: Local users excluding internal accounts
2. **Exclusion Lists**: Dynamic user exclusion based on labels
3. **Hash ID Generation**: Secure user identifier hashing

### Geographic Validation
1. **Boundary Filtering**: US coordinate validation
2. **Service Area Check**: Market profile polygon validation
3. **County Assignment**: Geographic county identification

### Data Transformation
1. **Field Mapping**: Source to target field transformation
2. **Date Conversion**: UTC timestamp handling
3. **Mode Classification**: Travel mode standardization

## Database Operations

### Source Tables (Portal)
- **trip**: Trip records with coordinates
- **user_rating**: User feedback data
- **bytemark_pass**: Transit pass usage
- **bytemark_order_payments**: Payment transactions
- **tow_and_go**: Roadside assistance
- **user_actions**: MongoDB user interactions
- **notification_record**: MongoDB alert data

### Target Tables (Dataset)
- **hntb_target_user**: Validated user list
- **hntb_trip**: Trip analytics data
- **hntb_rating**: Rating analytics
- **hntb_bytemark_pass**: Transit usage
- **hntb_bytemark_order_payments**: Payment analytics
- **hntb_tow_and_go**: Assistance analytics
- **hntb_school_zone**: School zone interactions
- **hntb_pre_trip_alert**: Alert interactions

## Error Handling

### Data Validation
- **Coordinate Validation**: Filters invalid GPS coordinates
- **Date Validation**: Handles invalid date ranges
- **Service Area**: Excludes out-of-area activities

### Processing Errors
- **Batch Processing**: Continues on individual record failures
- **Database Errors**: Comprehensive error logging
- **Geographic Errors**: Graceful handling of polygon failures

## Performance Optimization

### Batch Processing
- **1000 Record Batches**: Memory-efficient processing
- **Offset Pagination**: Handles large datasets
- **Parallel Processing**: Promise.all for concurrent operations

### Query Optimization
- **Indexed Queries**: Optimized database queries
- **Geographic Filtering**: Early coordinate filtering
- **Selective Fields**: Minimal data retrieval

## Integration Points

### Used By
- HNTB analytics reporting
- Transportation behavior analysis
- Service area effectiveness studies
- User engagement tracking

### External Dependencies
- **Incentive Engine**: Service area validation
- **Market Profile**: Geographic boundaries
- **MongoDB**: User action tracking
- **MySQL**: Portal and dataset databases

## Usage Guidelines

1. **Date Ranges**: Use incremental processing for efficiency
2. **User Filtering**: Maintain current exclusion lists
3. **Geographic Data**: Validate coordinate accuracy
4. **Performance**: Monitor batch processing times
5. **Data Quality**: Verify county assignments

## Dependencies

- **Moment.js**: Date manipulation and timezone handling
- **Turf.js**: Geographic calculations and validation
- **MongoDB**: User action and notification data
- **Multiple Models**: Database ORM operations
- **Market Profile Service**: Geographic boundary definitions