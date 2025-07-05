# MOD Service

## Overview

The MOD (Mobility-on-Demand) service provides trip planning and route calculation functionality, integrating with Google Maps Directions API to support various transportation modes and trip data retrieval.

## Service Information

- **Service Name**: MOD
- **File Path**: `/src/services/mod.js`
- **Type**: Trip Planning Service
- **Dependencies**: Google Maps Service, MySQL Portal

## Functions

### directions(mode, origin, destination, departureTime)

Calculates directions for different transportation modes with mode-specific configurations.

**Purpose**: Provides route calculation with transportation mode optimization
**Parameters**:
- `mode` (string): Transportation mode (transit, driving, walking, cycling)
- `origin` (string): Starting location (address, coordinates, or place ID)
- `destination` (string): Ending location (address, coordinates, or place ID)
- `departureTime` (string): Departure time for timing calculations

**Returns**: Google Maps Directions API response

**Transportation Modes**:
- **Transit**: Configured for bus and rail options
- **Driving**: Standard vehicle routing
- **Walking**: Pedestrian pathfinding
- **Cycling**: Bicycle route optimization

**Example**:
```javascript
const result = await directions(
  'transit',
  '123 Main St, Seattle, WA',
  '456 Oak Ave, Portland, OR',
  '2023-12-25T10:00:00Z'
);
// Returns: Complete route with transit options
```

### getTrip(id)

Retrieves comprehensive trip information from the database with location and timing details.

**Purpose**: Fetches complete trip data including coordinates, timing, and timezone information
**Parameters**:
- `id` (number): Trip activity ID

**Returns**: Trip object with location and timing data

**Trip Data Fields**:
- **departure_time**: Scheduled departure time
- **origin_latitude/longitude**: Starting point coordinates
- **destination_latitude/longitude**: Ending point coordinates
- **time_zone**: Trip-specific timezone information

**Database Query**:
- Joins multiple tables (cm_activity_location, cm_location, trip_activity_mapping)
- Retrieves comprehensive location and timing data
- Returns single trip record

**Example**:
```javascript
const trip = await getTrip(12345);
// Returns: {
//   departure_time: '2023-12-25T10:00:00Z',
//   origin_latitude: 47.6062,
//   origin_longitude: -122.3321,
//   destination_latitude: 45.5152,
//   destination_longitude: -122.6784,
//   time_zone: 'America/Los_Angeles'
// }
```

## Transportation Mode Configuration

### Transit Mode
- **Transit Types**: Bus and rail services
- **Configuration**: `transit_mode = 'bus|rail'`
- **Optimization**: Public transportation scheduling
- **Features**: Real-time transit data integration

### Other Modes
- **Driving**: Default vehicle routing without special configuration
- **Walking**: Pedestrian-optimized pathfinding
- **Cycling**: Bicycle-friendly route selection
- **Mixed Mode**: Supports multi-modal trip planning

## Database Integration

### Trip Data Structure
- **Activity Location**: Core trip activity data
- **Location Details**: Origin and destination coordinates
- **Activity Mapping**: Trip-to-activity relationships
- **Timezone Information**: Location-specific time zones

### Query Optimization
- **Efficient Joins**: Optimized multi-table joins
- **Indexed Lookups**: Fast retrieval by activity ID
- **Single Record**: Returns first matching record
- **Coordinate Precision**: High-precision location data

## Integration Points

### Used By
- Trip planning applications
- Route optimization services
- Multi-modal transportation planning
- Travel time estimation systems

### External Dependencies
- **Google Maps Service**: Route calculation and directions
- **MySQL Portal**: Trip and location data storage
- **@maas/core/mysql**: Database connection management
- **@maas/core/log**: Centralized logging

## Google Maps Integration

### API Utilization
- **Directions API**: Primary routing service
- **Mode Support**: All Google Maps transportation modes
- **Timing Integration**: Departure time optimization
- **Real-time Data**: Traffic and transit updates

### Request Configuration
- **Dynamic Parameters**: Mode-specific configuration
- **Flexible Input**: Multiple location format support
- **Error Handling**: Graceful API failure management
- **Performance**: Optimized request structure

## Error Handling

### API Failures
- **Google Maps Errors**: Handled by underlying map service
- **Network Issues**: Automatic retry mechanisms
- **Invalid Parameters**: Validation at request level
- **Rate Limiting**: Managed by Google Maps service

### Database Errors
- **Connection Issues**: Handled by database connection pool
- **Query Failures**: Logged and propagated appropriately
- **Data Validation**: Ensures trip ID validity
- **Transaction Safety**: Maintains data consistency

## Performance Considerations

### Route Calculation
- **API Efficiency**: Optimized Google Maps API usage
- **Caching**: Leverages Google's response caching
- **Parallel Processing**: Supports concurrent requests
- **Timeout Management**: Handled by underlying services

### Database Operations
- **Query Optimization**: Efficient multi-table joins
- **Index Usage**: Leverages database indexes
- **Connection Pooling**: Efficient resource utilization
- **Result Caching**: Optimized data retrieval

## Security Considerations

- **API Key Management**: Secure Google Maps API key handling
- **Input Validation**: Location parameter validation
- **Data Privacy**: Trip data access controls
- **Query Injection**: Parameterized database queries

## Usage Guidelines

1. **Mode Selection**: Choose appropriate transportation mode
2. **Location Format**: Use consistent location formats
3. **Timing**: Provide accurate departure times for optimization
4. **Error Handling**: Always handle potential API failures
5. **Performance**: Consider caching for frequently requested routes

## Dependencies

- **Google Maps Service**: Internal Google Maps integration
- **@maas/core/mysql**: Database connection management
- **@maas/core/log**: Centralized logging system
- **Knex.js**: SQL query builder for database operations