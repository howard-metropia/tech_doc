# test-redeem.js Technical Documentation

## Purpose

Integration test suite for gift card redemption system, testing the complete redemption workflow including balance validation, transaction processing, and daily limit enforcement.

## Core Functionality

### Gift Card Redemption

#### API Endpoint
- **Route**: `createRedeem`
- **Method**: POST
- **Endpoint**: `/api/v2/redeem`
- **Authentication**: User ID header required
- **Purpose**: Redeem gift cards for real-world value

#### Request Structure
```javascript
const redeemRequest = {
  id: giftCardId  // Gift card identifier
};
```

#### Response Structure
```javascript
const successResponse = {
  result: 'success',
  data: {
    balance: 0  // Remaining wallet balance after redemption
  }
};
```

## Test Architecture

### Test Data Setup
```javascript
describe('Redeem', () => {
  const userId = 1003;
  const auth = { userid: userId, 'Content-Type': 'application/json' };
  let giftCards = null;
  let postData = null;

  before('Prepare testing data', async () => {
    // Get available gift cards
    giftCards = await GiftCards.query().where({});
    postData = { id: giftCards[0].id };

    // Create redemption history
    await RedeemTransactions.query().insert({
      user_id: userId,
      giftcard_id: giftCards[0].id,
      points: -95.0,
      amount: 95,
      currency: 'USD',
      transaction_id: 'fake redeem Id',
      created_on: moment.utc().format('YYYY-MM-DD HH:mm:ss'),
    });

    // Add sufficient balance for redemption
    await UserWallets.query()
      .where('user_id', userId)
      .update({ balance: giftCards[0].points });
  });
});
```

### Data Models

#### GiftCards Model
```javascript
const giftCardStructure = {
  id: 'integer',
  name: 'string',
  description: 'string',
  points: 'decimal',      // Cost in platform coins
  amount: 'decimal',      // Real-world value
  currency: 'string',     // USD, EUR, etc.
  vendor: 'string',       // Gift card provider
  image_url: 'string',
  is_active: 'boolean'
};
```

#### RedeemTransactions Model
```javascript
const redeemTransactionStructure = {
  id: 'integer',
  user_id: 'integer',
  giftcard_id: 'integer',
  points: 'decimal',          // Negative value (deduction)
  amount: 'decimal',          // Gift card value
  currency: 'string',
  transaction_id: 'string',   // External reference
  created_on: 'timestamp'
};
```

#### UserWallets Model
```javascript
const userWalletStructure = {
  id: 'integer',
  user_id: 'integer',
  balance: 'decimal',         // Available coins
  auto_refill: 'boolean',
  below_balance: 'decimal',
  stripe_customer_id: 'string'
};
```

## Test Scenarios

### Successful Redemption
```javascript
it('should execute redeem procedure', async function () {
  this.timeout(10000);

  const resp = await request.set(auth).post(url).send(postData);
  const { result, data } = resp.body;
  const { balance } = data;

  expect(result).to.eq('success');
  expect(balance).to.eq(0);  // All coins used
});
```

### Error Scenarios

#### Authentication Failure
```javascript
it('should get a fail 10004', async () => {
  const resp = await request.post(url).unset('userid').send(postData);
  const { result, error } = resp.body;

  expect(result).to.eq('fail');
  expect(error).to.include({
    code: 10004,
    msg: 'Request header has something wrong',
  });
});
```

#### Missing Gift Card ID
```javascript
it('should get a fail 10002 as missing id', async () => {
  const resp = await request.set(auth).post(url).send({});
  const { result, error } = resp.body;

  expect(result).to.eq('fail');
  expect(error).to.includes({
    code: 10002,
    msg: '"id" is required',
  });
});
```

#### Invalid Gift Card
```javascript
it('should get a fail 10002 when giving wrong gift card id', async () => {
  const resp = await request.set(auth).post(url).send({ id: 1 });
  const { result, error } = resp.body;

  expect(result).to.eq('fail');
  expect(error).to.includes({
    code: 10002,
    msg: 'Request body not correct',
  });
});
```

#### Insufficient Balance
```javascript
it('should get a fail 23018', async function () {
  this.timeout(10000);

  const resp = await request
    .set(auth)
    .post(url)
    .send({ id: giftCards[0].id });
  
  const { result, error } = resp.body;

  expect(result).to.eq('fail');
  expect(error).to.includes({
    code: 23018,
    msg: 'Coin insufficient',
  });
});
```

#### Daily Limit Exceeded
```javascript
it('should get a fail 23034', async function () {
  this.timeout(10000);

  const resp = await request
    .set(auth)
    .post(url)
    .send({ id: giftCards[1].id });
  
  const { result, error } = resp.body;

  expect(result).to.eq('fail');
  expect(error).to.includes({
    code: 23034,
    msg: 'You have reached the daily gift card redemption limit of 100. Please try again tomorrow.',
  });
});
```

## Business Logic

### Redemption Validation
1. **User Authentication**: Verify user ID in headers
2. **Gift Card Existence**: Validate gift card ID exists
3. **Balance Check**: Ensure sufficient coin balance
4. **Daily Limits**: Enforce redemption frequency limits
5. **Availability**: Check gift card is still available

### Transaction Processing
1. **Coin Deduction**: Remove coins from user wallet
2. **Transaction Recording**: Log redemption transaction
3. **External Fulfillment**: Process with gift card vendor
4. **Balance Update**: Return updated wallet balance

### Daily Limits
- **Limit Amount**: $100 USD equivalent per day
- **Reset Time**: Daily limit resets at midnight UTC
- **Enforcement**: Cumulative redemption value tracking

## Error Codes

### Authentication Errors
- **10004**: Missing or invalid user ID header

### Validation Errors
- **10002**: Missing required fields or invalid data
- **20001**: Resource not found

### Business Logic Errors
- **23018**: Insufficient coin balance
- **23034**: Daily redemption limit exceeded

## Integration Points

### External Services
- **Gift Card Vendors**: Third-party fulfillment services
- **Payment Processing**: External transaction validation
- **Fraud Detection**: Anti-fraud monitoring

### Internal Dependencies
- **Wallet Service**: Balance management
- **Transaction Service**: Payment processing
- **User Management**: Authentication and limits

## Security Features

### Fraud Prevention
- **Daily Limits**: Prevent excessive redemptions
- **Transaction Monitoring**: Detect suspicious patterns
- **User Verification**: Validate legitimate users

### Data Protection
- **Transaction Encryption**: Secure sensitive data
- **Audit Trail**: Complete transaction history
- **PCI Compliance**: Handle payment data securely

## Performance Considerations

### Database Optimization
- **Transaction Isolation**: Prevent concurrent redemption issues
- **Index Strategy**: Optimize frequent lookups
- **Connection Pooling**: Efficient database usage

### External API Integration
- **Timeout Handling**: Graceful timeout management
- **Retry Logic**: Handle temporary vendor failures
- **Response Caching**: Cache vendor responses when appropriate

## Data Cleanup Strategy

```javascript
after('Delete testing data', async () => {
  await RedeemTransactions.query().where('user_id', userId).delete();
});
```

### Cleanup Requirements
- **Test Transactions**: Remove all test redemption records
- **Wallet Restoration**: Reset user wallet to original state
- **Gift Card Status**: Restore gift card availability

## Usage Examples

### Successful Redemption Flow
```javascript
// 1. Check available gift cards
const giftCards = await GiftCards.query().where({ is_active: true });

// 2. Verify user balance
const wallet = await UserWallets.query().where({ user_id: userId }).first();
const canAfford = wallet.balance >= giftCards[0].points;

// 3. Process redemption
const redemption = await request
  .post('/api/v2/redeem')
  .set({ userid: userId })
  .send({ id: giftCards[0].id });

// 4. Handle response
if (redemption.body.result === 'success') {
  console.log(`New balance: ${redemption.body.data.balance}`);
}
```

### Error Handling
```javascript
try {
  const response = await request
    .post('/api/v2/redeem')
    .set({ userid: userId })
    .send({ id: invalidGiftCardId });
} catch (error) {
  switch (error.body.error.code) {
    case 23018:
      console.log('Insufficient balance');
      break;
    case 23034:
      console.log('Daily limit exceeded');
      break;
    case 10002:
      console.log('Invalid gift card');
      break;
  }
}
```

## Monitoring and Analytics

### Key Metrics
- **Redemption Success Rate**: Percentage of successful redemptions
- **Daily Volume**: Total redemption value per day
- **Popular Cards**: Most frequently redeemed gift cards
- **User Patterns**: Redemption frequency by user tier

### Alert Conditions
- **High Failure Rate**: Unusual number of failed redemptions
- **Vendor Issues**: External service availability problems
- **Fraud Patterns**: Suspicious redemption activities

This test suite ensures reliable gift card redemption functionality, covering the complete redemption workflow with comprehensive validation, error handling, and business rule enforcement.