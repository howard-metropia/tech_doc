# Travel Mode Definitions Mock Module

## Overview
A mock module that provides standardized travel mode constants for testing purposes. This module defines numeric identifiers for different transportation modes used throughout the TSP API testing framework.

## File Purpose
- **Primary Function**: Provide travel mode constants for testing
- **Type**: Mock constants module
- **Role**: Standardize travel mode identifiers in test scenarios

## Key Constants

### Travel Mode Definitions
```javascript
const travelMode = {
  WALKING: 3,
  DRIVING: 1,
  BIKING: 4,
  PUBLIC_TRANSIT: 2,
  INTERMODAL: 5,
  TRUCKING: 6,
  PARK_AND_RIDE: 7,
  RIDEHAIL: 8,
  DUO: 100,
  INSTANT_CARPOOL: 101
};
```

## Travel Mode Categories

### Standard Transportation Modes
- **WALKING (3)**: Pedestrian movement
- **DRIVING (1)**: Personal vehicle operation
- **BIKING (4)**: Bicycle transportation
- **PUBLIC_TRANSIT (2)**: Bus, train, subway systems

### Advanced Transportation Modes
- **INTERMODAL (5)**: Multi-modal trip combining different transport types
- **TRUCKING (6)**: Commercial vehicle transportation
- **PARK_AND_RIDE (7)**: Combined parking and public transit

### Ride-Sharing Services
- **RIDEHAIL (8)**: On-demand ride services (Uber, Lyft)
- **DUO (100)**: Paired/shared transportation service
- **INSTANT_CARPOOL (101)**: Real-time carpooling matching

## Usage Examples

### Test Data Setup
```javascript
const { travelMode } = require('./mocks/defines');

describe('Trip Validation', () => {
  it('should validate walking trip', () => {
    const testTrip = {
      mode: travelMode.WALKING,
      distance: 0.5
    };
    expect(validateTrip(testTrip)).toBe(true);
  });
});
```

### Mode Comparison Testing
```javascript
const { travelMode } = require('./mocks/defines');

test('ridehail vs driving comparison', () => {
  const ridehailTrip = { mode: travelMode.RIDEHAIL };
  const drivingTrip = { mode: travelMode.DRIVING };
  
  expect(getTripType(ridehailTrip)).toBe('shared');
  expect(getTripType(drivingTrip)).toBe('personal');
});
```

### Multi-Modal Trip Testing
```javascript
const { travelMode } = require('./mocks/defines');

test('intermodal trip handling', () => {
  const intermodalTrip = {
    mode: travelMode.INTERMODAL,
    segments: [
      { mode: travelMode.WALKING },
      { mode: travelMode.PUBLIC_TRANSIT },
      { mode: travelMode.WALKING }
    ]
  };
  
  expect(validateIntermodalTrip(intermodalTrip)).toBe(true);
});
```

## Technical Specifications

### Numeric Identification System
- **Standard Modes**: Use single-digit identifiers (1-8)
- **Extended Modes**: Use three-digit identifiers (100+)
- **Consistent Mapping**: Maintains compatibility with production systems

### Mode Grouping Strategy
- **Personal Transportation**: WALKING, DRIVING, BIKING
- **Public Transportation**: PUBLIC_TRANSIT, PARK_AND_RIDE
- **Shared Services**: RIDEHAIL, DUO, INSTANT_CARPOOL
- **Commercial**: TRUCKING
- **Complex**: INTERMODAL

## Integration Points

### Testing Framework Integration
- Used across all transportation-related tests
- Provides consistent mode identification
- Enables standardized test data creation

### Service Layer Testing
- Trip validation service tests
- Route planning algorithm tests
- Incentive calculation tests
- Carbon footprint calculation tests

### Database Testing
- Trip record validation
- Activity logging tests
- Reporting and analytics tests
- User preference tests

## Mock vs Production Alignment

### Consistency Requirements
- Mock values must match production definitions
- Numerical identifiers should be synchronized
- New modes require updates in both environments

### Test Coverage
- All production travel modes represented
- Special test-only modes may be added
- Maintains backward compatibility

## Mode-Specific Characteristics

### Environmental Impact
- **WALKING, BIKING**: Zero emissions
- **PUBLIC_TRANSIT**: Shared emissions
- **DRIVING**: Individual emissions
- **RIDEHAIL**: Shared individual emissions

### Infrastructure Requirements
- **WALKING, BIKING**: Minimal infrastructure
- **PUBLIC_TRANSIT**: Dedicated infrastructure
- **DRIVING**: Road network
- **PARK_AND_RIDE**: Combined facilities

### User Experience Patterns
- **INSTANT_CARPOOL**: Real-time matching
- **DUO**: Scheduled pairing
- **RIDEHAIL**: On-demand service
- **INTERMODAL**: Multi-step journey

## Testing Scenarios

### Mode Validation Tests
```javascript
describe('Travel Mode Validation', () => {
  Object.values(travelMode).forEach(mode => {
    it(`should validate mode ${mode}`, () => {
      expect(isValidTravelMode(mode)).toBe(true);
    });
  });
});
```

### Mode-Specific Logic Tests
```javascript
describe('Mode-Specific Features', () => {
  it('should calculate emissions for each mode', () => {
    expect(calculateEmissions(travelMode.WALKING)).toBe(0);
    expect(calculateEmissions(travelMode.DRIVING)).toBeGreaterThan(0);
  });
});
```

## Maintenance Notes

### Adding New Travel Modes
1. Add new mode constant with appropriate numeric identifier
2. Update documentation with mode characteristics
3. Ensure production system alignment
4. Add corresponding test cases

### Mode Retirement
- Mark deprecated modes clearly
- Maintain backward compatibility
- Update dependent test cases
- Document migration path

### Synchronization
- Regular review against production definitions
- Coordinate changes with development team
- Update integration tests after changes
- Maintain version compatibility