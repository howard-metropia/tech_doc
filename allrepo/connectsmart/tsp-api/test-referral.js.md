# test-referral.js Technical Documentation

## Purpose

Comprehensive integration test suite for the user referral program, testing referral code validation, geographic restrictions, time limits, and tier-based reward distribution.

## Core Functionality

### Referral System

#### API Endpoint
- **Route**: `createReferral`
- **Method**: POST
- **Endpoint**: `/api/v2/referral`
- **Authentication**: Bearer token + User ID header required
- **Purpose**: Process referral code submissions for new users

#### Request Structure
```javascript
const referralRequest = {
  referral_code: 'ENCODED_USER_ID'  // Hashids-encoded referrer ID
};
```

#### Response Structure
```javascript
const successResponse = {
  result: 'success',
  data: {
    referral_id: 123,  // Database record ID
    toast: {
      title: 'Congratulations!',
      message: 'We've added 1 Coin to your Wallet!'
    }
  }
};
```

## Test Architecture

### Test Setup
```javascript
describe('Referral', async () => {
  const userId = 1003;
  let auth = { 
    userid: userId, 
    'Content-Type': 'application/json', 
    authorization: '' 
  };
  let referralCode, selfReferral;

  before('Prepare testing data', async () => {
    // Enable debug mode for test user
    await AuthUsers.query().where('id', userId).patch({ is_debug: 1 });
    
    // Generate JWT token
    const token = await authToken(userId);
    auth.authorization = `Bearer ${token}`;
    
    // Mock tier service
    stub1 = sinon.stub(tierService, 'getUserTier')
      .resolves({ level: 'green', points: 1 });
    
    // Generate referral codes
    const referralHash = new Hashids(config.projectTitle, 10);
    referralCode = referralHash.encode(1005);      // Valid referrer
    selfReferral = referralHash.encode(1003);      // Self-referral (invalid)
  });
});
```

### Hashids Configuration
- **Salt**: Project title from config
- **Length**: 10 characters minimum
- **Purpose**: Encode/decode user IDs for referral codes

## Validation Rules

### Geographic Restrictions
```javascript
// Houston area validation
const houstonCoordinates = {
  registration_latitude: -95.3903099765997,
  registration_longitude: 29.715986269476915
};

// Outside Houston (Taiwan coordinates) - should fail
const taiwanCoordinates = {
  registration_latitude: 121.60914728082417,
  registration_longitude: 23.977284023650093
};
```

### Time Restrictions
- **Eligibility Window**: 5 days from account creation
- **Validation**: `created_on` must be within 5 days of referral submission

### User Validation
- **Self-Referral Prevention**: Users cannot refer themselves
- **Single Use**: Each user can only submit one referral code
- **Referrer Existence**: Referral code must decode to valid user ID

## Error Scenarios

### Authentication Errors
```javascript
it('should get a fail 10004', async () => {
  const resp = await request.post(url).unset('userid').send({});
  const { result, error } = resp.body;
  
  expect(result).to.eq('fail');
  expect(error).to.include({
    code: 10004,
    msg: 'Request header has something wrong',
  });
});
```

### Validation Errors
```javascript
it('should get a fail 10002 as missing id', async () => {
  const resp = await request.set(auth).post(url).send({});
  const { result, error } = resp.body;
  
  expect(result).to.eq('fail');
  expect(error).to.includes({
    code: 10002,
    msg: '"referral_code" is required',
  });
});
```

### Business Logic Errors

#### Invalid Referral Code
```javascript
it('should get a fail 47001', async () => {
  const resp = await request
    .set(auth)
    .post(url)
    .send({ referral_code: 'ABCDE12345' });
  
  const { result, error } = resp.body;
  expect(result).to.eq('fail');
  expect(error).to.includes({
    code: 47001,
    msg: 'The referral code you entered does not exist.',
  });
});
```

#### Self-Referral Prevention
```javascript
it('should get a fail 47003', async () => {
  const resp = await request
    .set(auth)
    .post(url)
    .send({ referral_code: selfReferral });
  
  const { result, error } = resp.body;
  expect(result).to.eq('fail');
  expect(error).to.includes({
    code: 47003,
    msg: `Please don't submit your own referral code.`,
  });
});
```

#### Expired Time Window
```javascript
it('should get a fail 47004', async () => {
  // Set user creation date beyond 5-day window
  await AuthUsers.query()
    .where('id', 1003)
    .update({
      created_on: moment.utc().subtract(6, 'days').format('YYYY-MM-DD HH:mm:ss'),
    });
  
  const resp = await request
    .set(auth)
    .post(url)
    .send({ referral_code: referralCode });
  
  expect(error).to.includes({
    code: 47004,
    msg: `Sorry, but this referral code offer has expired.`,
  });
});
```

#### Geographic Restriction
```javascript
it('should get a fail 47005', async () => {
  // Set user location outside Houston area
  await AuthUsers.query()
    .where('id', 1003)
    .update({
      registration_latitude: 121.60914728082417,   // Taiwan
      registration_longitude: 23.977284023650093,
    });
  
  const resp = await request
    .set(auth)
    .post(url)
    .send({ referral_code: referralCode });
  
  expect(error).to.includes({
    code: 47005,
    msg: `You must reside in the Greater Houston area to receive this offer.`,
  });
});
```

#### Duplicate Submission
```javascript
it('should get a fail 47002', async () => {
  // After successful referral submission
  const resp = await request
    .set(auth)
    .post(url)
    .send({ referral_code: referralCode });
  
  expect(error).to.includes({
    code: 47002,
    msg: `You've already submitted a referral code.`,
  });
});
```

## Tier-Based Rewards

### Green Tier Rewards
```javascript
it('should execute referral procedure - tier level green', async () => {
  const resp = await request
    .set(auth)
    .post(url)
    .send({ referral_code: referralCode });
  
  const { result, data } = resp.body;
  const { referral_id: id, toast } = data;
  
  expect(result).to.eq('success');
  expect(id).to.gt(0);
  
  // Verify green tier message
  const coins = process.env.REFERRAL_COIN ? parseFloat(process.env.REFERRAL_COIN) : 1;
  const replacement = coins > 1 ? 'Coins' : 'Coin';
  let message = tierService.benefitsRule.green.referral.toast.message;
  message = message.replace('{1}', coins).replace('{2}', replacement);
  
  expect(toast).to.includes({
    title: tierService.benefitsRule.green.referral.toast.title,
    message,
  });
});
```

### Bronze Tier Rewards
```javascript
it('should execute referral procedure - tier level bronze', async () => {
  // Mock bronze tier
  stub1.restore();
  stub1 = sinon.stub(tierService, 'getUserTier')
    .resolves({ level: 'bronze', points: 501 });
  
  const resp = await request
    .set(auth)
    .post(url)
    .send({ referral_code: referralCode });
  
  const { toast } = resp.body.data;
  expect(toast).to.includes(tierService.benefitsRule.bronze.referral.toast);
});
```

### Silver and Gold Tiers
- Similar test structure with appropriate tier mock setup
- Validates tier-specific reward messages and amounts

## Data Models

### AuthUsers Model
```javascript
const userStructure = {
  id: 'integer',
  created_on: 'timestamp',
  registration_latitude: 'decimal',
  registration_longitude: 'decimal',
  is_debug: 'boolean'
};
```

### ReferralHistory Model
```javascript
const referralStructure = {
  id: 'integer',
  sender_user_id: 'integer',   // Referrer
  receiver_user_id: 'integer', // Referee
  referral_code: 'string',
  created_on: 'timestamp',
  reward_amount: 'decimal'
};
```

## Service Integration

### Tier Service Integration
```javascript
const tierService = require('@app/src/services/tier');

// Get user tier for reward calculation
const userTier = await tierService.getUserTier(userId);

// Get tier-specific benefits
const benefits = await tierService.getUserTierBenefits(userTier.level);
```

### Reward Calculation
- **Base Reward**: Environment variable `REFERRAL_COIN` (default: 1)
- **Tier Multiplier**: Applied based on user's tier level
- **Message Formatting**: Dynamic coin amount and pluralization

## Geographic Validation

### Houston Area Definition
- **Latitude Range**: Approximately 29.0° to 30.5° N
- **Longitude Range**: Approximately -96.0° to -94.5° W
- **Validation Logic**: Point-in-polygon or radius-based checking

### Location Data Sources
- **Registration Coordinates**: Captured during user signup
- **IP Geolocation**: Backup validation method
- **Address Validation**: Optional postal code verification

## Configuration Management

### Environment Variables
```javascript
const config = {
  REFERRAL_COIN: process.env.REFERRAL_COIN || 1,
  PROJECT_TITLE: config.portal.projectTitle,
  TIME_LIMIT_DAYS: 5,
  HOUSTON_BOUNDS: {
    // Geographic boundary definitions
  }
};
```

### Hashids Configuration
```javascript
const referralHash = new Hashids(config.projectTitle, 10);
const userId = referralHash.decode(referralCode)[0] || 0;
```

## Security Features

### Code Generation
- **Unpredictable**: Hashids prevent sequential guessing
- **Reversible**: Can decode to original user ID
- **Collision Resistant**: Unique codes per user

### Abuse Prevention
- **Time Limits**: Prevent old account referrals
- **Geographic Limits**: Restrict to service area
- **Single Use**: One referral per user
- **Self-Referral Block**: Prevent gaming system

## Performance Considerations

### Database Optimization
- **Indexed Lookups**: Efficient referral code validation
- **Geographic Queries**: Optimized location validation
- **Transaction Isolation**: Prevent duplicate submissions

### Cache Strategy
- **Tier Data**: Cache user tier information
- **Geographic Bounds**: Cache boundary data
- **Referral Validation**: Cache recent validations

## Usage Examples

### Generating Referral Code
```javascript
const Hashids = require('hashids');
const config = require('config');

const referralHash = new Hashids(config.portal.projectTitle, 10);
const referralCode = referralHash.encode(userId);
console.log(`Your referral code: ${referralCode}`);
```

### Submitting Referral
```javascript
const response = await fetch('/api/v2/referral', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer jwt_token',
    'userid': '1003'
  },
  body: JSON.stringify({
    referral_code: 'ABCDE12345'
  })
});

const result = await response.json();
if (result.result === 'success') {
  console.log(`Reward: ${result.data.toast.message}`);
}
```

This test suite ensures robust referral program functionality, covering code validation, geographic restrictions, time limits, tier-based rewards, and comprehensive security measures to prevent abuse.