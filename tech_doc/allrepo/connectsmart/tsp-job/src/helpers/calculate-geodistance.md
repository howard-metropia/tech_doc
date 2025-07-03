# Calculate Geodistance Helper

## Overview
**File**: `src/helpers/calculate-geodistance.js`  
**Type**: Utility Function  
**Purpose**: Calculates linear distance between two geographical coordinates using Haversine formula

## Core Function

### Distance Calculation
```javascript
module.exports = (lat1, lng1, lat2, lng2) => {
  // Calculate distance in meters using Haversine formula
}
```

## Mathematical Implementation

### Constants
- **EARTH_RADIUS**: 6378.137 km (Earth's radius)

### Haversine Formula Steps
1. **Convert to Radians**: Convert latitude/longitude from degrees to radians
2. **Calculate Differences**: Compute differences between coordinates
3. **Apply Formula**: Use Haversine formula for great circle distance
4. **Convert Units**: Transform result from km to meters

### Formula Details
```javascript
const radLat1 = (lat1 * Math.PI) / 180.0;
const radLat2 = (lat2 * Math.PI) / 180.0;
const a = radLat1 - radLat2;
const b = radLng1 - radLng2;

let s = 2 * Math.asin(
  Math.sqrt(
    Math.pow(Math.sin(a / 2), 2) +
    Math.cos(radLat1) * Math.cos(radLat2) * Math.pow(Math.sin(b / 2), 2)
  )
);
```

## Input Parameters

### Required Parameters
- **lat1**: First point latitude (decimal degrees)
- **lng1**: First point longitude (decimal degrees) 
- **lat2**: Second point latitude (decimal degrees)
- **lng2**: Second point longitude (decimal degrees)

### Parameter Validation
- No explicit validation in current implementation
- Assumes valid coordinate inputs
- Uses standard floating-point arithmetic

## Output

### Return Value
- **Type**: Number
- **Unit**: Meters
- **Precision**: Floating point

### Distance Calculation
- Calculates straight-line (great circle) distance
- Does not account for terrain or road networks
- Provides theoretical minimum travel distance

## Dependencies

### External Libraries
- `@maas/core/log`: For logging distance calculations

### Standard Libraries
- Uses built-in Math functions
- No additional dependencies required

## Logging

### Information Logging
```javascript
logger.info(
  `linear distance between (${lat1}, ${lng1}) and (${lat2}, ${lng2}): ${s}`
);
```

### Log Content
- Input coordinates
- Calculated distance result
- Helps with debugging and monitoring

## Usage Examples

### Basic Usage
```javascript
const calculateDistance = require('./calculate-geodistance');

// Calculate distance between two points
const distance = calculateDistance(40.7128, -74.0060, 34.0522, -118.2437);
console.log(`Distance: ${distance} meters`);
```

### Integration Example
```javascript
// In route calculation
const startLat = trip.origin.latitude;
const startLng = trip.origin.longitude;
const endLat = trip.destination.latitude; 
const endLng = trip.destination.longitude;

const linearDistance = calculateDistance(startLat, startLng, endLat, endLng);
```

## Mathematical Background

### Haversine Formula
- Determines great-circle distance between two points on sphere
- Accounts for Earth's curvature
- More accurate than simple Euclidean distance for geographical coordinates

### Formula Accuracy
- **High Accuracy**: For most practical applications
- **Earth Model**: Assumes spherical Earth (6378.137 km radius)
- **Limitations**: Minor variations due to Earth's actual oblate spheroid shape

## Performance Characteristics

### Computational Complexity
- **Time Complexity**: O(1) - constant time
- **Space Complexity**: O(1) - constant space
- **Performance**: Fast trigonometric calculations

### Optimization Notes
- Single function call with minimal overhead
- Uses efficient Math library functions
- No loops or recursive operations

## Limitations

### Accuracy Considerations
- Assumes spherical Earth model
- Does not account for elevation differences
- Provides theoretical minimum distance only

### Use Case Restrictions
- **Linear Distance Only**: Not suitable for routing
- **No Terrain**: Ignores geographical obstacles
- **Great Circle**: Assumes direct path

## Error Handling

### Input Validation
- No explicit parameter validation
- Relies on JavaScript's automatic type conversion
- May produce NaN for invalid inputs

### Edge Cases
- **Same Point**: Returns 0 meters
- **Antipodal Points**: Maximum possible distance
- **Invalid Coordinates**: May return NaN or unexpected results

## Integration Points

### Common Use Cases
- **Distance Validation**: Check trip feasibility
- **Proximity Calculations**: Find nearby services
- **Billing Calculations**: Distance-based pricing
- **Analytics**: Trip distance metrics

### Related Functions
- Often used with route planning APIs
- Combined with other geographical calculations
- Integrated into trip validation workflows

## Constants Reference

### Earth Radius
- **Value**: 6378.137 km
- **Standard**: WGS84 approximation
- **Usage**: Converts angular distance to linear distance

### Unit Conversion
- **Formula Result**: Kilometers
- **Final Conversion**: Multiply by 1000 for meters
- **Output Unit**: Meters (standard MaaS platform unit)

## Security Considerations

### Data Privacy
- Coordinates logged for debugging
- Consider sensitive location data in logs
- No data persistence in this function

### Input Sanitization
- No validation of coordinate ranges
- Assumes trusted input sources
- May need additional validation in production use