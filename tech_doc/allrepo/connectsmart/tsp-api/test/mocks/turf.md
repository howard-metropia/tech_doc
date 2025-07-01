# Turf.js Mock Module for Geospatial Testing

## Overview
A simplified mock implementation of Turf.js geospatial functions designed for testing environments. This module provides basic geospatial operations without the complexity and dependencies of the full Turf.js library.

## File Purpose
- **Primary Function**: Mock geospatial operations for testing
- **Type**: Geospatial utility mock
- **Role**: Simplified spatial calculations in test scenarios

## Key Functions

### `point(coords)`
Creates a GeoJSON Point geometry from coordinates.

**Parameters:**
- `coords` (Array): Coordinate array `[longitude, latitude]`

**Returns:**
- GeoJSON Point object: `{ type: 'Point', coordinates: coords }`

**Usage:**
```javascript
const { point } = require('./mocks/turf');
const location = point([-122.4194, 37.7749]); // San Francisco
// Returns: { type: 'Point', coordinates: [-122.4194, 37.7749] }
```

### `lineString(coords)`
Creates a GeoJSON LineString geometry from coordinate array.

**Parameters:**
- `coords` (Array): Array of coordinate pairs `[[lng1, lat1], [lng2, lat2], ...]`

**Returns:**
- GeoJSON LineString object: `{ type: 'LineString', coordinates: coords }`

**Usage:**
```javascript
const { lineString } = require('./mocks/turf');
const route = lineString([
  [-122.4194, 37.7749],
  [-122.4094, 37.7849]
]);
// Returns: { type: 'LineString', coordinates: [[...], [...]] }
```

### `pointToLineDistance()`
Calculates distance from a point to a line (simplified mock implementation).

**Parameters:**
- Parameters ignored in mock implementation

**Returns:**
- `number`: Fixed distance value of 10 (units unspecified)

**Usage:**
```javascript
const { pointToLineDistance } = require('./mocks/turf');
const distance = pointToLineDistance(point, line);
// Always returns: 10
```

## GeoJSON Compatibility

### Standard GeoJSON Format
The mock functions return properly formatted GeoJSON objects compatible with:
- Mapping libraries (Leaflet, Mapbox GL JS)
- GeoJSON validation tools
- Other geospatial libraries

### Geometry Types Supported
- **Point**: Single coordinate location
- **LineString**: Sequence of connected coordinates
- **Distance Calculations**: Simplified numeric results

## Testing Patterns

### Location Testing
```javascript
const { point } = require('./mocks/turf');

describe('Location Services', () => {
  it('should create valid location point', () => {
    const location = point([-122.4194, 37.7749]);
    
    expect(location.type).toBe('Point');
    expect(location.coordinates).toEqual([-122.4194, 37.7749]);
  });
});
```

### Route Testing
```javascript
const { lineString } = require('./mocks/turf');

describe('Route Planning', () => {
  it('should create route geometry', () => {
    const route = lineString([
      [-122.4194, 37.7749],
      [-122.4094, 37.7849]
    ]);
    
    expect(route.type).toBe('LineString');
    expect(route.coordinates).toHaveLength(2);
  });
});
```

### Distance Calculation Testing
```javascript
const { pointToLineDistance } = require('./mocks/turf');

describe('Distance Calculations', () => {
  it('should calculate point to line distance', () => {
    const distance = pointToLineDistance();
    expect(distance).toBe(10);
  });
});
```

## Mock vs Production Behavior

### Simplified Operations
- **Mock**: Returns fixed/simple values for testing
- **Production**: Performs complex geospatial calculations
- **Purpose**: Enable testing without computational overhead

### Consistent Interface
- Function signatures match Turf.js API patterns
- Return types compatible with expected formats
- Enables drop-in replacement for testing

## Geospatial Use Cases

### Trip Planning
- Route geometry creation
- Waypoint management
- Distance calculations

### Location Services
- Point-of-interest representation
- User location tracking
- Geofencing operations

### Transportation Analysis
- Route comparison
- Service area calculations
- Stop proximity analysis

## Technical Specifications

### Coordinate Systems
- **Format**: `[longitude, latitude]` (GeoJSON standard)
- **Precision**: Maintains input precision
- **Validation**: No coordinate validation in mock

### Distance Units
- **Mock Behavior**: Returns unitless fixed value
- **Production Note**: Real Turf.js uses meters by default
- **Test Considerations**: Use for relative comparisons only

## Integration with Testing Framework

### Jest Integration
```javascript
jest.mock('turf', () => require('./mocks/turf'));

describe('Geospatial Service', () => {
  // Tests using mocked turf functions
});
```

### Mocha Integration
```javascript
const turf = require('./mocks/turf');

describe('Location Processing', () => {
  // Tests using mock turf functions
});
```

## Performance Benefits

### Testing Speed
- No complex mathematical calculations
- Instant function returns
- Reduced memory usage

### Dependency Management
- Eliminates large Turf.js library in tests
- Reduces test bundle size
- Faster test environment setup

## Limitations

### Accuracy Considerations
- Distance calculations are not accurate
- No actual geospatial computation
- Suitable for unit tests only

### Feature Coverage
- Limited subset of Turf.js functionality
- Only basic geometry creation
- Missing advanced spatial operations

## Extension Guidelines

### Adding New Functions
```javascript
module.exports = {
  // Existing functions...
  
  // New mock function
  buffer: (geometry, radius) => ({
    type: 'Polygon',
    coordinates: [[/* simplified polygon */]]
  })
};
```

### Mock Customization
- Return predictable values for testing
- Maintain GeoJSON format compatibility
- Consider test scenario requirements

## Real-World Integration

### Service Testing
- Trip validation services
- Location-based services
- Route optimization algorithms

### API Endpoint Testing
- Geospatial API responses
- Location search functionality
- Proximity calculations

## Maintenance Notes

### Turf.js Compatibility
- Monitor Turf.js API changes
- Update mock interfaces as needed
- Maintain backward compatibility

### Test Coverage
- Ensure mock functions cover test scenarios
- Add functions as testing requirements grow
- Document mock behavior limitations

### Performance Monitoring
- Track test execution speed benefits
- Monitor mock usage patterns
- Optimize mock implementations as needed