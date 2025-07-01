# TSP API Test Suite - Ridehail Incentive Tests

## Overview
The `test-ridehail-incentive.js` file contains comprehensive tests for the ridehail incentive system, focusing on tier-based rewards, guest trip ordering, wallet management, and payment processing for ridehail services.

## File Location
`/allrepo/connectsmart/tsp-api/test/test-ridehail-incentive.js`

## Dependencies
- **chai**: Testing assertions and expectations
- **sinon**: Test doubles, mocking, and stubbing
- **nock**: HTTP mocking for external API calls
- **@maas/core/redis**: Cache management
- **config**: Configuration management

## Test Architecture

### Service Integration
```javascript
const ridehailService = require('@app/src/services/ridehail');
const uberWebhookService = require('@app/src/services/uber-webhook');
```

### Model Dependencies
```javascript
const UberFareEstimation = require('@app/src/models/UberFareEstimation');
const RidehailTrips = require('@app/src/models/RidehailTrips');
const UberGuestRideLogs = require('@app/src/models/UberGuestRideLogs');
const Trips = require('@app/src/models/Trips');
const Teleworks = require('@app/src/models/Teleworks');
const TeleworkLogs = require('@app/src/models/TeleworkLogs');
```

### Configuration Setup
```javascript
const config = require('config');
const uberConfig = config.vendor.uber;
const incentiveConfig = config.vendor.incentive;
const knex = require('@maas/core/mysql')('portal');
```

## Guest Trip Ordering System

### Test Data Setup
```javascript
describe('Ridehail Service with Tier', () => {
  describe('orderGuestTrip', () => {
    let testUserId = 5566;
    let testWalletId;
    let mockInput;

    const mockInput = {
      userId: testUserId,
      zone: 'America/Chicago',
      guest: {
        phone_number: '+1234567890'
      },
      pickup: {
        latitude: 40.7128,
        longitude: -74.006
      },
      dropoff: {
        latitude: 40.7589,
        longitude: -73.9851
      },
      origin: {
        latitude: 40.7128,
        longitude: -74.006,
        address: 'New York Downtown'
      },
      destination: {
        latitude: 40.7589,
        longitude: -73.9851,
        address: 'Empire State Building'
      },
      ridehail_trip: {
        product_id: '9c0fd086-b4bd-44f1-a278-bdae3cdb3d9f',
        fare_id: 'fare123',
        note_for_driver: 'Meet at main entrance',
        benefit_credit: 8
      }
    };
  });
});
```

### Database Test Data Preparation
```javascript
before(async () => {
  // Create test user
  await knex('auth_user').insert({
    id: testUserId,
    first_name: 'Test',
    last_name: 'User',
    email: 'test.user@example.com',
    password: 'hashed_password',
    phone_number: '+1234567890'
  });

  // Create user wallet with sufficient balance
  [testWalletId] = await knex('user_wallet').insert({
    user_id: mockInput.userId,
    balance: 1000, // Sufficient balance
    auto_refill: 'F',
    below_balance: 5,
    stripe_customer_id: null
  });

  // Ensure Uber wallet exists
  const [uberWallet] = await knex('user_wallet')
    .where({ user_id: 2107 }) // Uber's user ID
    .select('id');

  if (!uberWallet) {
    await knex('user_wallet').insert({
      user_id: 2107,
      balance: 0,
      auto_refill: 'F',
      below_balance: 0,
      stripe_customer_id: null
    });
  }
});
```

## Incentive System Architecture

### Tier-Based Reward Structure
```javascript
const INCENTIVE_TIERS = {
  BRONZE: {
    level: 1,
    ridehailDiscount: 0.05,  // 5% discount
    maxBenefit: 10,          // $10 max benefit per trip
    minimumSpend: 15         // $15 minimum trip cost
  },
  SILVER: {
    level: 2,
    ridehailDiscount: 0.10,  // 10% discount
    maxBenefit: 15,          // $15 max benefit per trip
    minimumSpend: 12         // $12 minimum trip cost
  },
  GOLD: {
    level: 3,
    ridehailDiscount: 0.15,  // 15% discount
    maxBenefit: 20,          // $20 max benefit per trip
    minimumSpend: 10         // $10 minimum trip cost
  }
};
```

### Benefit Credit Calculation
```javascript
const calculateBenefitCredit = (fareAmount, userTier, tripType) => {
  const tier = INCENTIVE_TIERS[userTier];
  if (!tier || fareAmount < tier.minimumSpend) {
    return 0;
  }

  const discountAmount = fareAmount * tier.ridehailDiscount;
  const benefitCredit = Math.min(discountAmount, tier.maxBenefit);

  // Additional bonuses for specific trip types
  if (tripType === 'FIRST_RIDEHAIL') {
    benefitCredit += 5; // $5 first ride bonus
  }

  if (tripType === 'INTERMODAL') {
    benefitCredit *= 1.2; // 20% bonus for multi-modal trips
  }

  return Math.round(benefitCredit * 100) / 100; // Round to 2 decimal places
};
```

## Wallet Management System

### Balance Validation
```javascript
const validateWalletBalance = async (userId, requiredAmount) => {
  const wallet = await knex('user_wallet')
    .where('user_id', userId)
    .first();

  if (!wallet) {
    throw new Error('Wallet not found');
  }

  if (wallet.balance < requiredAmount) {
    throw new Error('Insufficient balance');
  }

  return wallet;
};
```

### Transaction Processing
```javascript
const processRidehailTransaction = async (userId, fareAmount, benefitCredit) => {
  const transaction = await knex.transaction();
  
  try {
    // Deduct user balance
    await transaction('user_wallet')
      .where('user_id', userId)
      .decrement('balance', fareAmount);

    // Add benefit credit if applicable
    if (benefitCredit > 0) {
      await transaction('user_wallet')
        .where('user_id', userId)
        .increment('balance', benefitCredit);
    }

    // Credit Uber wallet
    await transaction('user_wallet')
      .where('user_id', 2107) // Uber's user ID
      .increment('balance', fareAmount - benefitCredit);

    // Record transaction
    await transaction('wallet_transactions').insert({
      user_id: userId,
      amount: -fareAmount,
      type: 'RIDEHAIL_PAYMENT',
      description: 'Uber ride payment',
      benefit_credit: benefitCredit
    });

    await transaction.commit();
    return { success: true, benefitCredit };
  } catch (error) {
    await transaction.rollback();
    throw error;
  }
};
```

## Guest Ride Management

### Guest Trip Lifecycle
```javascript
describe('Guest Trip Management', () => {
  it('should create guest trip with proper incentives', async () => {
    const guestTripData = {
      ...mockInput,
      guest: {
        phone_number: '+1234567890',
        first_name: 'Guest',
        last_name: 'User'
      }
    };

    const result = await ridehailService.orderGuestTrip(guestTripData);

    expect(result).to.have.property('trip_id');
    expect(result).to.have.property('uber_request_id');
    expect(result).to.have.property('benefit_applied');
    expect(result.benefit_applied).to.be.greaterThan(0);
  });

  it('should handle insufficient balance for guest trips', async () => {
    // Set wallet balance to insufficient amount
    await knex('user_wallet')
      .where('user_id', testUserId)
      .update({ balance: 5 });

    try {
      await ridehailService.orderGuestTrip(mockInput);
      expect.fail('Should have thrown insufficient balance error');
    } catch (error) {
      expect(error.code).to.equal(ERROR_CODE.ERROR_POINT_INSUFFICIENT);
    }
  });
});
```

### Guest User Creation
```javascript
const createGuestUser = async (guestInfo, sponsorUserId) => {
  const guestUser = await knex('auth_user').insert({
    first_name: guestInfo.first_name || 'Guest',
    last_name: guestInfo.last_name || 'User',
    phone_number: guestInfo.phone_number,
    email: `guest_${Date.now()}@example.com`,
    is_guest: true,
    sponsor_user_id: sponsorUserId,
    created_at: new Date()
  });

  // Create wallet for guest user
  await knex('user_wallet').insert({
    user_id: guestUser[0],
    balance: 0,
    auto_refill: 'F',
    below_balance: 0
  });

  return guestUser[0];
};
```

## Error Handling

### Insufficient Balance Handling
```javascript
const { ERROR_POINT_INSUFFICIENT } = require('@app/src/static/error-code');

describe('Error Scenarios', () => {
  it('should handle insufficient wallet balance', async () => {
    const lowBalanceInput = {
      ...mockInput,
      ridehail_trip: {
        ...mockInput.ridehail_trip,
        fare_id: 'expensive_fare_id' // High cost fare
      }
    };

    try {
      await ridehailService.orderGuestTrip(lowBalanceInput);
      expect.fail('Should throw insufficient balance error');
    } catch (error) {
      expect(error.code).to.equal(ERROR_POINT_INSUFFICIENT);
      expect(error.message).to.include('Insufficient balance');
    }
  });
});
```

### External API Failure Handling
```javascript
describe('External Service Failures', () => {
  it('should handle Uber API failures gracefully', async () => {
    // Mock Uber API failure
    nock(uberConfig.baseUrl)
      .post('/guests/trips')
      .reply(500, { error: 'Internal Server Error' });

    try {
      await ridehailService.orderGuestTrip(mockInput);
      expect.fail('Should throw API error');
    } catch (error) {
      expect(error.message).to.include('External service failure');
    }
  });
});
```

## Notification Integration

### Trip Status Notifications
```javascript
const sendTripNotifications = async (tripId, status, userIds) => {
  const notifications = userIds.map(userId => ({
    user_id: userId,
    trip_id: tripId,
    type: 'RIDEHAIL_STATUS',
    title: `Trip ${status}`,
    message: `Your ridehail trip is now ${status}`,
    data: { trip_id: tripId, status }
  }));

  await knex('notifications').insert(notifications);

  // Send push notifications
  const sqsClient = new SQSClient({ region: 'us-east-1' });
  await sqsClient.send(new SendMessageCommand({
    QueueUrl: config.aws.sqs.notificationQueue,
    MessageBody: JSON.stringify({
      type: 'TRIP_NOTIFICATION',
      notifications
    })
  }));
};
```

## Performance Monitoring

### Cache Integration
```javascript
const cache = require('@maas/core/redis')('cache');

const cacheUserTier = async (userId, tier) => {
  await cache.setex(`user_tier:${userId}`, 3600, JSON.stringify(tier));
};

const getCachedUserTier = async (userId) => {
  const cached = await cache.get(`user_tier:${userId}`);
  return cached ? JSON.parse(cached) : null;
};
```

### Performance Tests
```javascript
describe('Performance Tests', () => {
  it('should process guest trip order within acceptable time', async () => {
    const startTime = Date.now();
    
    const result = await ridehailService.orderGuestTrip(mockInput);
    
    const endTime = Date.now();
    const processingTime = endTime - startTime;
    
    expect(processingTime).to.be.lessThan(5000); // 5 seconds max
    expect(result).to.have.property('trip_id');
  });
});
```

## Quality Assurance

### Data Integrity Validation
- **Wallet Balance Consistency**: Ensure accurate balance tracking
- **Transaction Atomicity**: All-or-nothing transaction processing
- **Benefit Calculation Accuracy**: Correct incentive calculations
- **Guest User Management**: Proper guest account handling

### Security Considerations
- **Payment Security**: Secure financial transaction processing
- **User Data Protection**: Guest user information privacy
- **Authorization Validation**: Proper access control for guest trips
- **Fraud Prevention**: Suspicious activity detection

This comprehensive test suite ensures the ridehail incentive system provides accurate tier-based rewards, reliable guest trip management, and secure payment processing while maintaining high performance and data integrity standards.