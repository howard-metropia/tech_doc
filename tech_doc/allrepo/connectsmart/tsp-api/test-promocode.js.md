# test-promocode.js Technical Documentation

## Purpose

Integration test suite for promotional code system, testing promo code validation, redemption process, and tier-based reward distribution.

## Core Functionality

### Promo Code System

#### API Endpoint
- **Route**: `keyin_promo_code`
- **Method**: POST
- **Endpoint**: `/api/v2/promocode`
- **Authentication**: Bearer token required
- **Purpose**: Validate and redeem promotional codes

#### Request Structure
```javascript
const promoCodeRequest = {
  promo_code: 'TESTINGPROMOCODE'
};
```

#### Response Structure
```javascript
const successResponse = {
  result: 'success',
  data: {
    type: 'raffle ticket',
    toast: {
      title: 'Congratulations!',
      message: 'Reward message based on user tier'
    }
  }
};
```

## Test Architecture

### Mock Strategy
```javascript
const tierService = require('@app/src/services/tier');
const Axios = require('axios');

// Mock tier service
const tierStub = sinon.stub(tierService, 'getUserTier')
  .resolves({ tier_level: 'green', tier_points: 1 });

// Mock benefits
const benefitsStub = sinon.stub(tierService, 'getUserTierBenefits')
  .resolves({
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
        message: 'We've added 0.5 Coins to your Wallet!' 
      } 
    }
  });

// Mock external API call
const axiosStub = sinon.stub(Axios, 'post')
  .resolves({ 
    data: { 
      result: 'success', 
      data: { type: 'raffle ticket' } 
    } 
  });
```

### Authentication Setup
```javascript
const userId = 1003;
let auth = { 
  userid: userId, 
  'Content-Type': 'application/json',
  authorization: '' 
};

before(async () => {
  const token = await authToken(userId);
  auth.authorization = `Bearer ${token}`;
});
```

## Test Scenarios

### Success Path Testing
```javascript
describe('promocode success test', () => {
  it('normal happy case', async () => {
    const result = await request
      .post(url)
      .send({ promo_code: 'TESTINGPROMOCODE' })
      .set(auth);
    
    expect(result.body.result).eq('success');
    expect(result.body.data).to.includes.keys(['type', 'toast']);
  });
});
```

### Failure Path Testing

#### Invalid Promo Code
```javascript
it('should send promocode token fail 46001', async () => {
  const result = await request
    .post(url)
    .send({ promo_code: 'TESTINGPROMOCODE' })
    .set(auth);
  
  expect(result.body.result).eq('fail');
  expect(result.body.error).to.includes({
    code: 46001,
    msg: 'Oops, the promo code you entered is not valid.',
  });
});
```

#### Missing Required Field
```javascript
it('should send promocode token fail 10002', async () => {
  const result = await request
    .post(url)
    .send({})
    .set('userid', 1);
  
  expect(result.body.result).eq('fail');
  expect(result.body.error).to.includes({
    code: 10002,
    msg: '"promo_code" is required',
  });
});
```

#### Authentication Failure
```javascript
it('should send promocode token fail 10004', async () => {
  const result = await request
    .post(url)
    .send({ promo_code: 'TESTINGPROMOCODE' });
  
  expect(result.body.result).eq('fail');
  expect(result.body.error).to.includes({
    code: 10004,
    msg: 'Request header has something wrong',
  });
});
```

## Error Codes

### Validation Errors
- **10002**: Missing required field (`promo_code`)
- **10004**: Authentication header issues

### Business Logic Errors
- **46001**: Invalid or expired promotional code

## Integration Points

### External Services
- **Promotion Service**: Validates promo codes via Axios HTTP call
- **Tier Service**: Determines user tier and benefits
- **Reward System**: Distributes rewards based on promo type

### Internal Dependencies
- **Authentication**: JWT token validation
- **User Management**: User tier status
- **Wallet System**: Reward distribution

## Reward Types

### Raffle Tickets
- **Type**: Contest entries
- **Tier Impact**: Magnification based on user tier
- **Toast Message**: Tier-specific congratulatory message

### Coin Rewards
- **Type**: Platform currency
- **Amount**: Variable based on promotion
- **Tier Bonus**: Potential multipliers for higher tiers

## Service Integration Flow

### Successful Redemption Flow
1. **Authentication**: Validate Bearer token
2. **Tier Check**: Get user's current tier status
3. **Code Validation**: External API validates promo code
4. **Reward Calculation**: Apply tier-based multipliers
5. **Reward Distribution**: Credit rewards to user account
6. **Response**: Return success with reward details

### Error Handling Flow
1. **Input Validation**: Check required fields
2. **Authentication**: Verify user credentials
3. **External API**: Handle promotion service failures
4. **Business Rules**: Apply promotional restrictions
5. **Error Response**: Return appropriate error codes

## Mock Configuration

### Success Scenario Mocks
```javascript
// Tier service returns green tier
stub1 = sinon.stub(tierService, 'getUserTier')
  .resolves({ tier_level: 'green', tier_points: 1 });

// Benefits service returns green benefits
stub2 = sinon.stub(tierService, 'getUserTierBenefits')
  .resolves(greenTierBenefits);

// External API returns success
stub3 = sinon.stub(Axios, 'post')
  .resolves({ data: { result: 'success', data: { type: 'raffle ticket' } } });
```

### Failure Scenario Mocks
```javascript
// No external API mock = network failure
// This simulates promotion service unavailable
```

## Security Features

### Authentication Requirements
- **Bearer Token**: JWT authentication required
- **User Validation**: Verify user exists and is active
- **Request Validation**: Sanitize and validate input

### Rate Limiting
- **Per User**: Limit promo code attempts per user
- **Per Code**: Limit total redemptions per code
- **Time Windows**: Prevent rapid-fire attempts

## Business Rules

### Promo Code Validation
- **Expiration**: Check code validity period
- **Usage Limits**: Enforce per-user and total usage limits
- **Geographic**: Apply location-based restrictions
- **Tier Requirements**: Some codes may require minimum tier

### Reward Distribution
- **Tier Multipliers**: Higher tiers receive enhanced rewards
- **Reward Types**: Coins, raffle tickets, service credits
- **Maximum Limits**: Daily/monthly reward caps

## Performance Considerations

### Response Times
- **Local Validation**: Fast input validation
- **External Calls**: Optimized promotion service integration
- **Tier Lookup**: Cached tier information

### Scalability
- **Concurrent Redemptions**: Handle simultaneous code usage
- **Load Balancing**: Distribute promotion service load
- **Cache Strategy**: Cache frequently used promo codes

## Usage Examples

### Successful Redemption
```javascript
const response = await fetch('/api/v2/promocode', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer jwt_token',
    'userid': '1003'
  },
  body: JSON.stringify({
    promo_code: 'SUMMER2024'
  })
});

// Expected response:
{
  result: 'success',
  data: {
    type: 'raffle ticket',
    toast: {
      title: 'Congratulations!',
      message: 'You\'re entered into the giveaway. Good luck!'
    }
  }
}
```

### Error Response
```javascript
// Invalid code response:
{
  result: 'fail',
  error: {
    code: 46001,
    msg: 'Oops, the promo code you entered is not valid.'
  }
}
```

## Testing Strategy

### Mock Management
- **Service Isolation**: Mock external dependencies
- **State Management**: Clean mock state between tests
- **Realistic Responses**: Use production-like mock data

### Test Coverage
- **Happy Path**: Successful code redemption
- **Error Cases**: All possible failure scenarios
- **Edge Cases**: Boundary conditions and limits
- **Integration**: End-to-end flow validation

This test suite ensures reliable promotional code functionality, covering validation, redemption, and tier-based reward distribution while maintaining security and performance standards.