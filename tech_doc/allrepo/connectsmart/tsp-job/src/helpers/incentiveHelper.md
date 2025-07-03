# Incentive Helper

## Overview
**File**: `src/helpers/incentiveHelper.js`  
**Type**: Utility Module  
**Purpose**: Manages incentive reward calculations and travel mode mappings using statistical distributions

## Core Constants

### Travel Mode Mapping
```javascript
const travelModes = {
  [travelMode.DRIVING]: 'driving',
  [travelMode.PUBLIC_TRANSIT]: 'public_transit',
  [travelMode.WALKING]: 'walking',
  [travelMode.BIKING]: 'biking',
  [travelMode.INTERMODAL]: 'intermodal',
  [travelMode.RIDEHAIL]: 'ridehail'
};
```

### Incentive Constants
- **INCENTIVE_FIRST_TRIP_REWARD**: 0.99 (default first trip reward)

## Key Functions

### Reward Point Calculation
```javascript
async function getIncentiveRewardPoint(isFirstTrip, rule, modeRule) {
  if (isFirstTrip) {
    return rule.W || INCENTIVE_FIRST_TRIP_REWARD;
  }
  const { max: maxValue, min: minValue, mean, beta } = modeRule;
  return randomDecimalGenerator(maxValue, minValue, mean, beta);
}
```

### Random Number Generation
```javascript
function randomDecimalGenerator(max, min, mean, beta) {
  const alpha = Math.round(mean / beta);
  const raw = rGamma(alpha, beta);
  const ramNum = Math.round(raw * 100) / 100;
  
  if (ramNum <= min) return 0;
  if (ramNum > max) return max;
  return ramNum;
}
```

## Statistical Implementation

### Gamma Distribution
- **Function**: `rGamma(alpha, beta)`
- **Purpose**: Generates random numbers following gamma distribution
- **Algorithm**: Uses R.C.H. Cheng method for alpha > 1

### Distribution Parameters
- **Alpha**: Calculated as mean/beta
- **Beta**: Shape parameter from mode rule
- **Mean**: Expected value
- **Min/Max**: Boundary constraints

## Mathematical Functions

### Distance Calculation
```javascript
function calculateDistance(lat1, lng1, lat2, lng2) {
  const earth_radius = 6378.137;
  // Haversine formula implementation
  // Returns distance in meters
}
```

### Gamma Distribution Algorithm
```javascript
function rGamma(alpha, beta) {
  if (alpha > 1) {
    // Uses R.C.H. Cheng algorithm
  } else if (alpha === 1) {
    // Exponential distribution
  } else {
    // ALGORITHM GS of Statistical Computing
  }
}
```

## Dependencies

### External Libraries
- `@maas/core/log`: Logging functionality
- `@app/src/static/defines`: Travel mode constants

### Internal Dependencies
- Travel mode definitions
- Static configuration constants

## Usage Examples

### Reward Calculation
```javascript
const { getIncentiveRewardPoint } = require('./incentiveHelper');

// First trip reward
const firstTripReward = await getIncentiveRewardPoint(true, rule, null);

// Regular trip reward
const regularReward = await getIncentiveRewardPoint(false, rule, {
  max: 5.0,
  min: 0.5,
  mean: 2.0,
  beta: 0.8
});
```

### Travel Mode Mapping
```javascript
const { travelModes } = require('./incentiveHelper');

const mode = travelModes[travelMode.DRIVING]; // 'driving'
```

### Distance Calculation
```javascript
const { calculateDistance } = require('./incentiveHelper');

const distance = calculateDistance(40.7128, -74.0060, 34.0522, -118.2437);
```

## Reward Logic

### First Trip Handling
- **Priority**: Uses rule.W if available
- **Fallback**: INCENTIVE_FIRST_TRIP_REWARD constant
- **Type**: Fixed reward amount

### Regular Trip Rewards
- **Distribution**: Gamma distribution based
- **Parameters**: max, min, mean, beta from mode rule
- **Constraints**: Enforces min/max boundaries

## Logging

### Incentive Parameters
```javascript
logger.info(
  `[incentive-engine] incentive_parm: ${rule.market} - ${maxValue}, ${minValue}, ${mean}, ${beta} [${point}]`
);
```

### Zero Rewards
```javascript
logger.info(`[incentive-engine] ram_num: ${ramNum} <= min_value: ${min}`);
logger.info(`[incentive-engine] ram_num: ${ramNum} > max_value: ${max}`);
```

## Algorithm Details

### Random Generation Process
1. **Calculate Alpha**: alpha = mean / beta
2. **Generate Raw Value**: Using gamma distribution
3. **Round to Precision**: 2 decimal places
4. **Apply Constraints**: Enforce min/max boundaries
5. **Return Result**: Final reward amount

### Boundary Enforcement
- **Below Minimum**: Returns 0
- **Above Maximum**: Returns maximum value
- **Within Range**: Returns calculated value

## Travel Mode Support

### Supported Modes
- **DRIVING**: Personal vehicle
- **PUBLIC_TRANSIT**: Bus, train, metro
- **WALKING**: Pedestrian travel
- **BIKING**: Bicycle transportation
- **INTERMODAL**: Multi-modal trips
- **TRUCKING**: Commercial vehicles
- **PARK_AND_RIDE**: Combined parking + transit
- **DUO**: Carpooling
- **RIDEHAIL**: Uber, Lyft services
- **INSTANT_CARPOOL**: Real-time carpooling

## Performance Considerations

### Mathematical Complexity
- **Gamma Function**: Computationally intensive
- **Precision**: Limited to 2 decimal places
- **Caching**: No result caching implemented

### Optimization Opportunities
- **Pre-computed Tables**: For common parameter sets
- **Approximation**: Faster algorithms for high-volume use
- **Memoization**: Cache results for identical parameters

## Error Handling

### Invalid Parameters
- **Zero Maximum**: Returns 0 immediately
- **Invalid Distribution**: May produce unexpected results
- **Boundary Violations**: Handled by constraint logic

### Edge Cases
- **Negative Values**: Constrained to minimum
- **Infinite Values**: Constrained to maximum
- **NaN Results**: Not explicitly handled

## Integration Points

### Rule Engine
- **Market Rules**: Per-market incentive configuration
- **Mode Rules**: Transportation mode-specific parameters
- **User Rules**: First trip detection

### Analytics
- **Reward Tracking**: Logs reward calculations
- **Parameter Monitoring**: Tracks distribution parameters
- **Performance Metrics**: Distance and reward correlation

## Configuration Requirements

### Rule Structure
```javascript
{
  W: 0.99,           // First trip reward
  market: 'austin',   // Market identifier
  // other rule properties
}
```

### Mode Rule Structure
```javascript
{
  max: 5.0,    // Maximum reward
  min: 0.5,    // Minimum reward  
  mean: 2.0,   // Expected value
  beta: 0.8    // Distribution shape
}
```

## Testing Considerations

### Statistical Testing
- **Distribution Validation**: Verify gamma distribution
- **Boundary Testing**: Min/max constraint enforcement
- **First Trip Logic**: Special case handling

### Mock Data
```javascript
const mockRule = { W: 0.99, market: 'test' };
const mockModeRule = { max: 5, min: 0.5, mean: 2, beta: 1 };
```

## Security Notes

### Data Privacy
- **No Personal Data**: Only statistical calculations
- **Logging**: Contains market and parameter information
- **Audit Trail**: Reward calculation logging for compliance

### Validation
- **Parameter Bounds**: Enforced at calculation time
- **Input Sanitization**: Relies on caller validation
- **Configuration Security**: Rule data should be validated