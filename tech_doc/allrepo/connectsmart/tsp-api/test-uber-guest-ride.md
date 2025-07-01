# TSP API Test Suite - Uber Guest Ride Tests

## Overview
The `test-uber-guest-ride.js` file contains comprehensive tests for Uber guest ride functionality, covering fare estimation, trip ordering, status tracking, and error handling for guest ridehail services.

## File Location
`/allrepo/connectsmart/tsp-api/test/test-uber-guest-ride.js`

## Dependencies
- **chai**: Testing assertions and expectations
- **nock**: HTTP mocking for external API calls
- **sinon**: Test doubles and stubbing
- **@maas/core/bootstrap**: Core framework initialization
- **moment**: Date/time manipulation

## Test Architecture

### Service Integration
```javascript
const uberService = require('@app/src/services/ridehail');
const { uber: uberDefines } = require('@app/src/static/defines');
const dataValidator = require('@app/src/schemas/ridehail');
const mockData = require('@app/src/static/mock-data/ridehail');
```

### Model Dependencies
```javascript
const RidehailTrips = require('@app/src/models/RidehailTrips');
const UberFareEstimation = require('@app/src/models/UberFareEstimation');
const Trips = require('@app/src/models/Trips');
const Teleworks = require('@app/src/models/Teleworks');
const TeleworkLogs = require('@app/src/models/TeleworkLogs');
```

### Configuration Setup
```javascript
const uberConfig = require('config').vendor.uber;
const tripStatus = uberDefines.tripStatus;
const paymentStatus = uberDefines.paymentStatus;
const ERROR_CODE = require('@app/src/static/error-code');
```

## Uber API Integration Testing

### Mock API Setup
```javascript
const stubApiResponse = (code, data) => {
  nock(uberConfig.baseUrl)
    .post('/trips/estimates')
    .reply(code, data);
};
```

### Estimation API Tests

#### Happy Path - Fare Response
```javascript
describe('get estimation', () => {
  describe('happy path', () => {
    it('should return the correct format of response while mock response with fare', async () => {
      stubApiResponse(200, mockData.etaWithFareResponse);
      
      const pickup = {
        latitude: 29.7427741,
        longitude: -95.4011076
      };
      const dropoff = {
        latitude: 29.717299,
        longitude: -95.402483
      };
      
      const res = await uberService.getUberEstimation(pickup, dropoff);
      
      expect(res).not.empty;
      dataValidation(res);
    });
  });
});
```

#### Data Validation Function
```javascript
const dataValidation = (dataList) => {
  dataList.forEach((data) => {
    expect(data).to.includes.keys([
      'product_id',
      'product_display',
      'fare_display',
      'fare_currency',
      'pickup_eta',
      'trip_duration',
      'no_cars_available'
    ]);
    
    const regex = /^\$\d+\.\d{2}$/;
    expect(data.fare_display).to.match(regex);
  });
};
```

#### Estimation Without Fare
```javascript
it('should return the correct format of response while mock response with estimation', async () => {
  stubApiResponse(200, mockData.etaWithEstimationResponse);
  
  const pickup = {
    latitude: 29.7427741,
    longitude: -95.4011076
  };
  const dropoff = {
    latitude: 29.717299,
    longitude: -95.402483
  };
  
  const res = await uberService.getUberEstimation(pickup, dropoff);
  expect(res).to.be.empty;
});
```

## Guest Ride Service Architecture

### Guest Trip Data Structure
```javascript
const guestTripRequest = {
  guest: {
    phone_number: '+1234567890',
    first_name: 'Guest',
    last_name: 'User',
    email: 'guest@example.com'
  },
  pickup: {
    latitude: 40.7128,
    longitude: -74.0060,
    address: 'New York, NY',
    nickname: 'Downtown'
  },
  dropoff: {
    latitude: 40.7589,
    longitude: -73.9851,
    address: 'Empire State Building',
    nickname: 'ESB'
  },
  ridehail_trip: {
    product_id: '9c0fd086-b4bd-44f1-a278-bdae3cdb3d9f',
    fare_id: 'fare123',
    note_for_driver: 'Meet at main entrance',
    requested_by: 1003,
    benefit_credit: 8
  }
};
```

### Guest User Management
```javascript
const createGuestUser = async (guestInfo, sponsorUserId) => {
  const guestUser = {
    first_name: guestInfo.first_name || 'Guest',
    last_name: guestInfo.last_name || 'User',
    phone_number: guestInfo.phone_number,
    email: guestInfo.email || generateGuestEmail(),
    is_guest: true,
    sponsor_user_id: sponsorUserId,
    created_at: new Date(),
    status: 'active'
  };
  
  const [guestId] = await Trips.knex('auth_user').insert(guestUser);
  
  // Create guest wallet
  await Trips.knex('user_wallet').insert({
    user_id: guestId,
    balance: 0,
    auto_refill: 'F',
    below_balance: 0
  });
  
  return guestId;
};
```

## Trip Status Management

### Status Definitions
```javascript
const TRIP_STATUS = {
  PROCESSING: 'processing',
  ACCEPTED: 'accepted',
  ARRIVING: 'arriving',
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled'
};
```

### Status Tracking
```javascript
const updateTripStatus = async (tripId, status, metadata = {}) => {
  await RidehailTrips.query()
    .where('id', tripId)
    .update({
      status: status,
      status_updated_at: new Date(),
      metadata: JSON.stringify(metadata)
    });
  
  // Log status change
  await UberGuestRideLogs.create({
    trip_id: tripId,
    event_type: 'STATUS_CHANGE',
    old_status: metadata.oldStatus,
    new_status: status,
    timestamp: new Date(),
    details: metadata
  });
};
```

## Error Handling and Validation

### API Error Responses
```javascript
describe('error handling', () => {
  it('should handle wrong format response gracefully', async () => {
    stubApiResponse(200, mockData.etaWithWrongFormatResponse);
    
    const pickup = {
      latitude: 29.7427741,
      longitude: -95.4011076
    };
    const dropoff = {
      latitude: 29.717299,
      longitude: -95.402483
    };
    
    const res = await uberService.getUberEstimation(pickup, dropoff);
    expect(res).to.be.empty; // Should filter out invalid responses
  });

  it('should handle API server errors', async () => {
    stubApiResponse(500, { error: 'Internal Server Error' });
    
    try {
      await uberService.getUberEstimation(pickup, dropoff);
      expect.fail('Should have thrown an error');
    } catch (error) {
      expect(error.message).to.include('API request failed');
    }
  });
});
```

### Input Validation
```javascript
const validateGuestRideRequest = (request) => {
  const schema = dataValidator.guestRideSchema;
  const { error, value } = schema.validate(request);
  
  if (error) {
    throw new ValidationError(error.details[0].message);
  }
  
  return value;
};
```

## Slack Integration for Monitoring

### Error Notifications
```javascript
const SlackManager = require('@maas/services/src/slack');
const sandbox = sinon.createSandbox();

const incorrectMsgStub = sandbox.stub(
  SlackManager.prototype,
  'sendVendorIncorrectMsg'
);

const vendorFailedMsgStub = sandbox.stub(
  SlackManager.prototype,
  'sendVendorFailedMsg'
);

describe('slack notifications', () => {
  it('should send notification for vendor failures', async () => {
    stubApiResponse(500, { error: 'Service Unavailable' });
    
    try {
      await uberService.getUberEstimation(pickup, dropoff);
    } catch (error) {
      expect(vendorFailedMsgStub.calledOnce).to.be.true;
    }
  });
});
```

## Mock Data Structure

### Fare Response Mock
```javascript
const etaWithFareResponse = {
  estimates: [
    {
      product_id: '9c0fd086-b4bd-44f1-a278-bdae3cdb3d9f',
      display_name: 'UberX',
      estimate: '$12.50',
      currency_code: 'USD',
      pickup_estimate: 5,
      duration_estimate: 15,
      distance_estimate: 3.2,
      no_cars_available: false
    },
    {
      product_id: 'a1111c8c-c720-46c3-8534-2fcdd730040d',
      display_name: 'UberPool',
      estimate: '$8.75',
      currency_code: 'USD',
      pickup_estimate: 7,
      duration_estimate: 18,
      distance_estimate: 3.2,
      no_cars_available: false
    }
  ]
};
```

### Estimation Response Mock
```javascript
const etaWithEstimationResponse = {
  estimates: [
    {
      product_id: '9c0fd086-b4bd-44f1-a278-bdae3cdb3d9f',
      display_name: 'UberX',
      estimate: null,
      pickup_estimate: 5,
      duration_estimate: 15,
      no_cars_available: false
    }
  ]
};
```

## Payment Integration

### Payment Processing
```javascript
const processGuestRidePayment = async (sponsorUserId, fareAmount, guestTripId) => {
  const transaction = await Trips.knex.transaction();
  
  try {
    // Validate sponsor balance
    const sponsorWallet = await transaction('user_wallet')
      .where('user_id', sponsorUserId)
      .first();
    
    if (sponsorWallet.balance < fareAmount) {
      throw new Error('Insufficient sponsor balance');
    }
    
    // Deduct from sponsor
    await transaction('user_wallet')
      .where('user_id', sponsorUserId)
      .decrement('balance', fareAmount);
    
    // Credit Uber account
    await transaction('user_wallet')
      .where('user_id', 2107) // Uber's user ID
      .increment('balance', fareAmount);
    
    // Record transaction
    await transaction('wallet_transactions').insert({
      user_id: sponsorUserId,
      amount: -fareAmount,
      type: 'GUEST_RIDE_PAYMENT',
      reference_id: guestTripId,
      description: `Guest ride payment for trip ${guestTripId}`
    });
    
    await transaction.commit();
    return { success: true, transaction_id: generateTransactionId() };
  } catch (error) {
    await transaction.rollback();
    throw error;
  }
};
```

## Real-time Updates

### WebSocket Integration
```javascript
const notifyTripUpdate = async (tripId, update) => {
  const trip = await RidehailTrips.query().findById(tripId);
  
  // Notify sponsor user
  await websocketManager.sendToUser(trip.sponsor_user_id, {
    type: 'GUEST_TRIP_UPDATE',
    trip_id: tripId,
    status: update.status,
    timestamp: new Date(),
    data: update
  });
  
  // Notify guest user if exists
  if (trip.guest_user_id) {
    await websocketManager.sendToUser(trip.guest_user_id, {
      type: 'TRIP_UPDATE',
      trip_id: tripId,
      status: update.status,
      timestamp: new Date(),
      data: update
    });
  }
};
```

## Performance Testing

### Load Testing
```javascript
describe('performance tests', () => {
  it('should handle multiple concurrent estimation requests', async () => {
    const requests = Array(10).fill().map(() => 
      uberService.getUberEstimation(pickup, dropoff)
    );
    
    const startTime = Date.now();
    const results = await Promise.all(requests);
    const endTime = Date.now();
    
    expect(endTime - startTime).to.be.lessThan(5000); // 5 seconds for 10 requests
    expect(results.every(result => Array.isArray(result))).to.be.true;
  });
});
```

## Quality Assurance

### Data Integrity
- **Guest User Creation**: Proper guest account management
- **Payment Processing**: Accurate financial transactions
- **Status Tracking**: Reliable trip status updates
- **Error Recovery**: Graceful failure handling

### Security Considerations
- **Guest Data Protection**: Secure guest information handling
- **Payment Security**: Secure financial transactions
- **API Security**: Proper authentication with Uber API
- **Access Control**: Appropriate sponsor/guest permissions

This comprehensive test suite ensures the Uber guest ride system provides reliable fare estimation, secure payment processing, and effective trip management while maintaining high performance and data integrity standards for guest ridehail services.