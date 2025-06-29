# TSP API Test Suite - Trip Incentive System Tests

## Overview
The `test-trip-incentive.js` file contains comprehensive tests for the trip-based incentive system, validating reward calculations, service profile intersections, and geographic eligibility for transportation mode incentives.

## File Location
`/allrepo/connectsmart/tsp-api/test/test-trip-incentive.js`

## Dependencies
- **@turf/turf**: Geometric calculations and GIS operations
- **wkt**: Well-Known Text parsing for geographic data
- **geo-point-in-polygon**: Point-in-polygon calculations
- **@maas/core**: Core framework components
- **chai**: Testing assertions

## Test Architecture

### Core Components
- `incentiveHelper`: Core incentive calculation service
- `tripIncentiveRules`: Market-specific incentive rule definitions
- `TripTrajectory`: Trip path and movement tracking
- `getServiceProfile`: Market profile and geographic boundary services

## Test Categories

### 1. Incentive Helper Unit Tests

**Test Subject**: `incentiveHelper.getIncentiveRewardPoint`

**Market Configuration**: Houston ConnectSmart (HCS)

**Travel Mode Testing**:

#### First Trip Bonus
```javascript
it('test first trip', async () => {
  const modeRule = rules.modes['driving'];
  const point = await incentiveHelper.getIncentiveRewardPoint(true, rules, modeRule);
  expect(point).to.be.a('number');
  expect(point).to.be.eq(rules['W']); // Welcome bonus
});
```

#### Travel Mode Incentive Validation

**Driving Mode**:
- Tests reward point generation across 10,000 iterations
- Validates points within defined range [0, modeRule.max]
- Ensures statistical distribution consistency

**Intermodal Mode**:
- Multi-modal transportation incentives
- Combined transport method rewards
- Integration between different transport types

**Duo Mode (Carpool)**:
- Shared ride incentive calculations
- Driver/passenger role-based rewards
- Social transportation encouragement

**Instant Duo Mode**:
- Real-time carpool matching rewards
- Dynamic ride-sharing incentives
- Immediate availability bonuses

**Active Transportation**:
- **Walking**: Pedestrian activity rewards
- **Biking**: Cycling encouragement incentives
- Health and environmental benefit points

**Public Transit**:
- Mass transportation adoption rewards
- Transit system usage incentives
- Environmental impact bonuses

**Trucking Mode**:
- Commercial vehicle incentives
- Freight transportation rewards
- Business logistics optimization

### 2. Incentive Rule Structure

**Rule Configuration**:
```javascript
{
  market: 'HCS',
  W: number,           // Welcome bonus for first trip
  modes: {
    driving: { max: number },
    intermodal: { max: number },
    duo: { max: number },
    instant_duo: { max: number },
    walking: { max: number },
    biking: { max: number },
    public_transit: { max: number },
    trucking: { max: number }
  }
}
```

### 3. Service Profile Polygon Intersection

**Test Subject**: Geographic boundary validation for incentive eligibility

**Components Tested**:
- Market boundary definitions
- Trip trajectory intersection calculations
- Geographic eligibility determination

**Intersection Logic**:
```javascript
// Trip data structure for geographic testing
const tripData = {
  trip_id: string,
  user_id: number,
  coordinates: [
    { latitude: number, longitude: number, timestamp: string }
  ],
  market: string
}
```

**Validation Process**:
1. **Boundary Parsing**: Convert WKT polygon definitions to GeoJSON
2. **Point Testing**: Check trajectory points against service area
3. **Eligibility Calculation**: Determine incentive qualification
4. **Reward Computation**: Calculate final incentive points

## Geographic Validation

### Service Area Definition
- Market-specific polygon boundaries
- Well-Known Text (WKT) format parsing
- Multi-polygon service area support

### Intersection Algorithms
- **Point-in-Polygon**: Individual coordinate validation
- **Turf.js Integration**: Advanced geometric operations
- **Buffer Zones**: Boundary tolerance handling

### Market Profiles
- Houston ConnectSmart (HCS) boundaries
- Service area coordinate systems
- Geographic coordinate validation

## Incentive Calculation Logic

### Reward Point Generation
```javascript
const incentiveHelper = {
  getIncentiveRewardPoint: async (isFirstTrip, rules, modeRule) => {
    if (isFirstTrip) {
      return rules.W; // Welcome bonus
    }
    
    // Mode-specific calculation logic
    const basePoints = calculateBasePoints(modeRule);
    const randomFactor = applyRandomization(modeRule);
    const finalPoints = Math.min(basePoints * randomFactor, modeRule.max);
    
    return Math.floor(finalPoints);
  }
}
```

### Randomization Factors
- Statistical distribution across reward ranges
- Gamification elements for user engagement
- Consistent randomness for fairness

### Bonus Multipliers
- First trip welcome bonuses
- Mode-specific multipliers
- Geographic bonus areas
- Time-based incentives

## Market-Specific Rules

### Houston ConnectSmart (HCS)
- Local transportation priorities
- Regional environmental goals
- Traffic congestion reduction incentives
- Multi-modal integration rewards

### Rule Validation
- Maximum point limits per mode
- Minimum guaranteed rewards
- Statistical consistency checks
- Edge case boundary testing

## Testing Methodology

### Statistical Validation
```javascript
// 10,000 iteration testing for consistency
for (let i=0; i<10000; i++) {
  const point = await incentiveHelper.getIncentiveRewardPoint(false, rules, modeRule);
  expect(point).to.be.at.least(0);
  expect(point).to.be.at.most(modeRule.max);
}
```

### Boundary Testing
- Minimum/maximum value validation
- Type checking (numeric results)
- Range compliance verification
- Distribution analysis

## Integration Points

### Trip Management
- Integration with core trip services
- Real-time incentive calculation
- Trip completion reward processing

### User Wallet System
- Point accumulation tracking
- Reward redemption handling
- Balance management integration

### Market Configuration
- Dynamic rule loading
- Market-specific customization
- Geographic boundary management

## Performance Considerations

### Calculation Efficiency
- Optimized reward algorithms
- Cached rule lookups
- Minimal database operations

### Geographic Processing
- Efficient polygon intersection
- Coordinate system optimization
- Spatial index utilization

## Quality Assurance

### Test Coverage
- All transportation modes tested
- Statistical distribution validation
- Geographic boundary verification
- Edge case scenario handling

### Validation Criteria
- Numeric result validation
- Range compliance checking
- Consistency across iterations
- Performance benchmarking

## Business Logic

### Incentive Goals
- **Environmental**: Encourage sustainable transport
- **Social**: Promote shared transportation
- **Economic**: Optimize transportation costs
- **Health**: Support active transportation modes

### Reward Strategy
- Progressive reward structures
- Mode-specific targeting
- Geographic optimization
- User engagement maximization

This comprehensive test suite ensures the incentive system accurately rewards users for their transportation choices while maintaining fairness, consistency, and alignment with market-specific transportation goals.