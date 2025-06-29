# test-tier.js Technical Documentation

## Purpose

Unit test suite for the user tier/gamification system, testing tier level calculations, benefit distributions, and Uber credit management across different membership levels.

## Core Functionality

### Tier System Overview

#### Tier Levels
1. **Green**: Entry level (1-500 points)
2. **Bronze**: Mid level (501-1000 points)  
3. **Silver**: Advanced level (1001-1500 points)
4. **Gold**: Premium level (1501+ points)

#### Tier Benefits
- **Raffle Magnification**: Multiplier for contest entries
- **Referral Bonuses**: Enhanced referral rewards
- **Uber Credits**: Ride subsidies for higher tiers

## Test Architecture

### Mock Strategy
```javascript
const superagent = require('superagent');
const stub = sinon.stub(superagent, 'get').resolves({ 
  body: { 
    data: { 
      tier_points: points, 
      tier_level: level 
    } 
  } 
});
```

### Test Data Structure
```javascript
const testScenarios = {
  green: { points: 1, level: 'green', uber_benefit: 0 },
  bronze: { points: 501, level: 'bronze', uber_benefit: 4 },
  silver: { points: 1001, level: 'silver', uber_benefit: 6 },
  gold: { points: 1501, level: 'gold', uber_benefit: 8 }
};
```

## Tier Benefits Configuration

### Green Tier Benefits
```javascript
const greenBenefits = {
  raffle: { 
    magnification: 1, 
    toast: { 
      title: 'Congratulations!', 
      message: 'You\'re entered into the giveaway. Good luck!' 
    } 
  },
  referral: { 
    magnification: 1, 
    toast: { 
      title: 'Congratulations!', 
      message: 'We've added {1} {2} to your Wallet!' 
    } 
  },
  uber: { benefit: 0 }
};
```

### Bronze Tier Benefits
```javascript
const bronzeBenefits = {
  raffle: { 
    magnification: 2, 
    toast: { 
      title: 'Congratulations!', 
      message: 'Bronze member! You\'ve earned 2x raffle tickets from contests and challenges!' 
    } 
  },
  referral: { 
    magnification: 1.15, 
    toast: { 
      title: 'Congratulations!', 
      message: 'Bronze member! You\'ve earned a 15% bonus on your referral incentive!' 
    } 
  },
  uber: { benefit: 4 }
};
```

### Tier Progression
- **Raffle Magnification**: 1x → 2x → 3x → 4x
- **Referral Bonus**: 1.0x → 1.15x → 1.25x → 1.5x  
- **Uber Credits**: $0 → $4 → $6 → $8

## Uber Benefit System

### Credit Allocation
- **Bronze**: $4.00 monthly credit
- **Silver**: $6.00 monthly credit
- **Gold**: $8.00 monthly credit
- **Green**: No Uber benefits

### Transaction Tracking
```javascript
// Credit issued
await UberBenefitTransaction.query().insert({
  user_id: userId,
  benefit_amount: 4,      // Credit amount
  transaction_amount: 8,  // Associated transaction
  transaction_id: 1
});

// Credit used (negative amount)
await UberBenefitTransaction.query().insert({
  user_id: userId,
  benefit_amount: -4,     // Credit deduction
  transaction_amount: -8, // Refund amount
  transaction_id: 1      // Same transaction (cancellation)
});
```

### Credit Balance Calculation
- **Available Credits**: Sum of positive benefit_amount
- **Used Credits**: Sum of negative benefit_amount
- **Net Balance**: Available - Used credits

## Test Scenarios

### Green Tier Tests
```javascript
describe('unit tests for tier service - green', () => {
  const userId = 1003;
  let points = 1;
  let level = 'green';
  let uber_benefit = 0;

  it('should return tier level and points', async () => {
    const result = await tierService.getUserTier(userId);
    expect(result).to.deep.eq({ points, level, uber_benefit });
  });

  it('should return tier benefits', async () => {
    const result = await tierService.getUserTierBenefits(level);
    expect(result).to.deep.eq(expectedGreenBenefits);
  });
});
```

### Bronze Tier with Credit Usage
```javascript
describe('unit tests for Tier Uber Credit Benefit with one ride', () => {
  before(async () => {
    await UberBenefitTransaction.query().insert({
      user_id: userId,
      benefit_amount: 4,
      transaction_amount: 8,
      transaction_id: 1
    });
  });

  it('should return tier level and points', async () => {
    const result = await tierService.getUserTier(userId);
    expect(result.uber_benefit).to.eq(0); // Credits used
  });
});
```

### Credit Refund Scenario
```javascript
describe('unit tests for Tier Uber Credit Benefit with ride canceled', () => {
  before(async () => {
    // Original transaction
    await UberBenefitTransaction.query().insert({
      user_id: userId,
      benefit_amount: 4,
      transaction_amount: 8,
      transaction_id: 1
    });
    
    // Cancellation/refund
    await UberBenefitTransaction.query().insert({
      user_id: userId,
      benefit_amount: -4,
      transaction_amount: -8,
      transaction_id: 1
    });
  });

  it('should restore credit balance', async () => {
    const result = await tierService.getUserTier(userId);
    expect(result.uber_benefit).to.eq(4); // Credits restored
  });
});
```

## Service Integration

### External API Communication
- **Incentive Hook Service**: Retrieves user tier data
- **URL Pattern**: `https://sb-incentive-hook.connectsmartx.com/tier/{userId}`
- **Response Format**: `{ data: { tier_points, tier_level } }`

### Error Handling
- **Network Failures**: Graceful degradation with default values
- **Invalid Responses**: Fallback to previous tier data
- **Service Unavailable**: Default to green tier benefits

## Data Models

### UberBenefitTransaction
```javascript
const transactionStructure = {
  user_id: 'integer',
  benefit_amount: 'decimal',      // Credit amount (+/-)
  transaction_amount: 'decimal',  // Associated transaction value
  transaction_id: 'integer',      // Reference transaction
  created_at: 'timestamp'
};
```

### Tier Calculation Logic
```javascript
const getTierFromPoints = (points) => {
  if (points >= 1501) return 'gold';
  if (points >= 1001) return 'silver';
  if (points >= 501) return 'bronze';
  return 'green';
};
```

## Gamification Features

### Raffle System
- **Entry Multipliers**: Higher tiers get more contest entries
- **Toast Messages**: Tier-specific congratulatory messages
- **Benefit Tracking**: Log enhanced participation rates

### Referral Program
- **Bonus Percentages**: Tier-based referral reward multipliers
- **Dynamic Messaging**: Personalized reward notifications
- **Calculation Logic**: `baseReward * tierMultiplier`

## Performance Optimization

### Caching Strategy
- **Tier Data**: Cache user tier information
- **Benefit Rules**: Static benefit configuration
- **Credit Balance**: Cache Uber credit calculations

### Database Efficiency
- **Aggregation Queries**: Efficient credit balance calculations
- **Index Strategy**: Optimize transaction lookups
- **Batch Operations**: Process multiple tier updates

## Testing Strategy

### Mock Management
```javascript
let stub1;
before(async () => {
  stub1 = sinon.stub(tierService, 'getUserTier')
    .resolves({ level: 'bronze', points: 501 });
});

after(async () => {
  stub1.restore();
});
```

### Data Cleanup
```javascript
after(async () => {
  await UberBenefitTransaction.query()
    .delete()
    .where('user_id', userId);
});
```

## Business Rules

### Tier Advancement
- **Point Thresholds**: Fixed point requirements for each tier
- **Retroactive Benefits**: Benefits apply immediately upon tier change
- **Degradation**: Users can drop tiers if points decrease

### Credit Management
- **Monthly Allocation**: Credits reset monthly based on tier
- **Unused Credits**: May expire based on business rules
- **Transaction Linking**: Credits tied to specific ride transactions

## Integration Points

### External Services
- **Incentive System**: Point calculation and tier determination
- **Uber API**: Ride booking and credit application
- **Notification System**: Tier change and benefit notifications

### Internal Systems
- **User Management**: Tier status in user profiles
- **Wallet System**: Credit balance integration
- **Analytics**: Tier distribution and benefit usage tracking

## Usage Examples

### Getting User Tier
```javascript
const tierData = await tierService.getUserTier(userId);
// Returns: { points: 501, level: 'bronze', uber_benefit: 4 }
```

### Applying Tier Benefits
```javascript
const benefits = await tierService.getUserTierBenefits('bronze');
const raffleEntries = baseEntries * benefits.raffle.magnification;
const referralBonus = baseReward * benefits.referral.magnification;
```

This test suite ensures the tier system correctly calculates user levels, applies appropriate benefits, and manages Uber credit allocations while maintaining data consistency and business rule compliance.