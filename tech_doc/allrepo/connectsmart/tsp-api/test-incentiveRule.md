# Test Documentation: Incentive Rule API

## Overview
This test suite validates the Incentive Rule functionality, which manages transportation mode incentive calculations and rule updates within the TSP system. The test covers multiple dated rule versions that have been deployed over time to adjust incentive parameters for different transportation modes.

## Test Configuration
- **File**: `test/test-incentiveRule.js`
- **Framework**: Mocha with Chai assertions
- **Models Used**: `TripIncentiveRules` (MongoDB)
- **Service**: `@app/src/services/incentiveRule`
- **Market**: HCS (Houston ConnectSmart)
- **Authentication**: Not required (service-level testing)

## Rule Versions Tested

### 1. Rule 20240819 (August 19, 2024)
**Parameters**:
- **D**: 300 (Duration parameter)
- **h**: 2 (Hours parameter)
- **d1**: 500 (Distance parameter 1)
- **d2**: 500 (Distance parameter 2)
- **L**: 20 (Limit parameter)
- **W**: 0.99 (Weight factor)
- **MC**: false (Multi-criteria flag)

### 2. Rule 20240823 (August 23, 2024)
**Key Changes**:
- **L**: 5 (reduced from 20)
- **MC**: true (enabled multi-criteria)
- **Ridehail**: Reduced incentives (mean: 0.01, max: 0)

### 3. Rule 20240912 (September 12, 2024)
**Key Changes**:
- **L**: 20 (restored from 5)
- **MC**: false (disabled multi-criteria)
- **Ridehail**: Restored incentives (mean: 15, max: 5)

### 4. Rule 20240920 (September 20, 2024)
**Key Changes**:
- **L**: 5 (reduced again)
- **MC**: true (re-enabled multi-criteria)
- **Ridehail**: Minimal incentives (mean: 0.01, max: 0)

### 5. Rule 20241002 (October 2, 2024)
**Key Changes**:
- **D**: 50000 (massive increase from 300)
- **L**: 5 (maintained)
- **MC**: false (disabled multi-criteria)
- **Driving/Duo**: Enhanced incentives (mean: 0.8, min: 0.5, max: 1, beta: 0.4)
- **Biking**: Reduced incentives (mean: 0.2, min: 0.1, max: 0.4)

### 6. Rule 20241231 (December 31, 2024)
**Key Changes**:
- **L**: 30 (increased from 5)
- **Ridehail**: High incentives (mean: 50, max: 20)

### 7. Rule 20250101 (January 1, 2025)
**Key Changes**:
- **L**: 5 (reset to low value)
- **Ridehail**: Minimal incentives (mean: 0.01, max: 0)

## Transportation Mode Incentive Structure

### Mode Categories
All rules support 9 transportation modes:
1. **intermodal** - Combined transportation methods
2. **driving** - Single-occupancy vehicle
3. **duo** - Carpooling/ridesharing
4. **instant_duo** - On-demand carpooling
5. **biking** - Bicycle transportation
6. **walking** - Pedestrian travel
7. **public_transit** - Bus, rail, and other transit
8. **trucking** - Commercial vehicle transport
9. **ridehail** - Commercial rideshare services

### Incentive Parameters
Each mode has 5 incentive parameters:
- **distance**: Minimum distance threshold for incentives
- **mean**: Average incentive value
- **min**: Minimum incentive value
- **max**: Maximum incentive value
- **beta**: Beta coefficient for incentive calculation

## Detailed Mode Configurations

### Consistent Modes (Across Most Rules)
**Intermodal**:
- distance: 2, mean: 0.6, min: 0.3, max: 0.8, beta: 0.3

**Public Transit**:
- distance: 2, mean: 0.6, min: 0.3, max: 0.8, beta: 0.3

**Walking**:
- distance: 0.5, mean: 0.1, min: 0.05, max: 0.25, beta: 0.05

**Trucking**:
- distance: 2, mean: 0.5, min: 0.25, max: 0.75, beta: 0.25

### Variable Modes (Changed Across Rules)

**Driving & Duo**:
- Early rules: mean: 0.5, min: 0, max: 0.75, beta: 0.25
- Rule 20241002+: mean: 0.8, min: 0.5, max: 1, beta: 0.4

**Biking**:
- Early rules: mean: 0.5, min: 0.25, max: 0.75, beta: 0.1
- Rule 20241002+: mean: 0.2, min: 0.1, max: 0.4, beta: 0.1

**Ridehail** (Most Variable):
- Rules 20240819, 20240912: mean: 15, min: 0, max: 5, beta: 0.5
- Rules 20240823, 20240920, 20250101: mean: 0.01, min: 0, max: 0, beta: 0.5
- Rule 20241002: mean: 0.01, min: 0, max: 0, beta: 0.5
- Rule 20241231: mean: 50, min: 0, max: 20, beta: 0.5

## Test Operations

### Test Scenarios
Each rule version tests two scenarios:
1. **Create New Rule**: Tests rule creation when no existing rule exists
2. **Update Existing Rule**: Tests rule update when rule already exists

### Test Process
1. **Cleanup**: Remove existing HCS market rule if present
2. **Service Call**: Execute rule creation/update service
3. **Verification**: Query database for created/updated rule
4. **Parameter Validation**: Assert all rule parameters match expected values
5. **Mode Validation**: Verify all 9 transportation modes and their parameters

### Validation Pattern
```javascript
expect(newRule).to.exist;
expect(newRule).to.have.property('market', 'HCS');
expect(newRule).to.have.property('D', expectedValue);
// ... validate all parameters
expect(newRule).to.have.property('modes');
const modes = newRule.modes;
expect(keys).to.have.length(9);
// ... validate each mode's parameters
```

## Business Logic

### Market-Specific Rules
- Rules are market-specific (HCS = Houston ConnectSmart)
- Each market can have different incentive parameters
- Rules support A/B testing and gradual rollout strategies

### Dynamic Incentive Adjustment
- Frequent rule updates suggest active incentive optimization
- Parameters adjusted based on usage patterns and business goals
- Ridehail incentives most frequently modified (policy-driven)

### Multi-Criteria Support
- MC flag enables/disables multi-criteria decision making
- Affects how multiple transportation modes are evaluated
- Toggled frequently suggesting experimental feature

### Distance-Based Incentives
- Different modes have different minimum distance thresholds
- Walking has lowest threshold (0.5), most others use 2.0
- Biking uses intermediate threshold (1.0)

## Key Insights from Rule Evolution

### Policy Trends
1. **Ridehail Regulation**: Frequent changes suggest policy experimentation
2. **Carpooling Promotion**: Duo modes consistently incentivized
3. **Transit Support**: Public transit maintains stable incentives
4. **Active Transportation**: Walking/biking receive consistent but modest incentives

### Parameter Volatility
- **Most Stable**: Walking, public transit, intermodal
- **Most Variable**: Ridehail incentives
- **Strategic Adjustments**: L parameter frequently modified
- **Major Overhaul**: Rule 20241002 with significant parameter increases

### Business Experimentation
- Short-lived experiments (20240823 → 20240912)
- Seasonal adjustments (20241231 → 20250101)
- A/B testing patterns evident in rapid rule changes

## Test Coverage

### Functional Testing
- ✅ Rule creation for non-existing rules
- ✅ Rule updates for existing rules
- ✅ Parameter persistence and retrieval
- ✅ Mode configuration validation
- ✅ Market-specific rule isolation

### Data Integrity
- ✅ All required parameters present
- ✅ Correct data types for all fields
- ✅ Mode enumeration completeness
- ✅ Parameter value ranges within expected bounds

### Service Integration
- ✅ Service method execution
- ✅ Database persistence
- ✅ Rule versioning support
- ✅ Market segmentation

## Implications for Transportation Policy

### Incentive Strategy
- System supports complex, dynamic incentive structures
- Real-time policy adjustment capabilities
- Mode-specific targeting for behavioral change
- Market-specific customization for regional needs

### Data-Driven Optimization
- Frequent rule updates suggest data-driven decision making
- A/B testing capabilities for policy experimentation
- Ability to quickly respond to usage pattern changes
- Fine-grained control over transportation mode promotion

This test suite ensures the incentive rule system can reliably manage complex, evolving transportation incentive policies within the TSP platform.