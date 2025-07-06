# test-point.js Technical Documentation

## Purpose

Comprehensive test suite for coin purchasing system, covering product purchases, daily limits, user blocking, and email notification systems with both unit and integration testing approaches.

## Core Functionality

### Coin Purchase System

#### Service: `buyPointProduct`
- **Purpose**: Process coin purchases using Stripe payment integration
- **Parameters**: User ID, timezone, product ID
- **Returns**: Updated wallet balance after purchase
- **Integration**: Stripe payment processing, email notifications

#### API Endpoint
- **Route**: `buyPointProduct`
- **Method**: POST
- **Endpoint**: `/api/v2/points/buy`
- **Authentication**: User ID header required

## Test Architecture

### Database Cleanup Strategy
```javascript
beforeEach(async () => {
  const yesterday = new Date(new Date().getTime() - 1000 * 60 * 60 * 24)
    .toISOString()
    .replace('T', ' ')
    .split('.')[0];
  
  // Clean up test data from yesterday onwards
  await knex('coin_activity_log').where({ user_id: userId }).andWhere('created_on', '>=', yesterday).delete();
  await knex('block_users').where({ user_id: userId }).delete();
  await knex('purchase_transaction').where({ user_id: userId }).andWhere('created_on', '>=', yesterday).delete();
  await knex('purchase_transaction_upgrade').where({ user_id: userId }).andWhere('created_on', '>=', yesterday).delete();
  await knex('points_transaction').where({ user_id: userId, activity_type: 2 }).andWhere('created_on', '>=', yesterday).delete();
  await knex('points_transaction_upgrade').where({ user_id: userId, activity_type: 2 }).andWhere('created_on', '>=', yesterday).delete();
});
```

### Email Notification Mocking
```javascript
const walletNotify = require('@app/src/services/walletNotify');
const spy1 = sandbox.spy(walletNotify, 'emailNotify');
const spy2 = sandbox.spy(walletNotify, 'emailNotifyUser');
```

## Test Scenarios

### Unit Tests

#### Successful Purchase
```javascript
it('unit test - normal happy case', async () => {
  const uw = await walletService.getUserWallet(userId);
  const product = await knex('points_store').where({ id: 1 }).first();
  
  const data = {
    userId,
    zone: 'America/Chicago',
    product_id: 1,
  };
  
  const { balance } = await buyPointProduct(data);
  expect(balance).to.eq(uw.balance + Number(product.points));
});
```

#### Blocked User Prevention
```javascript
it('unit test - blocked user cannot buy coins', async () => {
  const data = {
    userId,
    zone: 'America/Chicago',
    product_id: 1,
  };
  
  await knex('block_users').insert({ user_id: userId, is_deleted: 'F' });
  
  await expect(buyPointProduct(data)).to.be.rejectedWith(
    'ERROR_USER_COIN_SUSPENDED',
  );
});
```

#### Daily Limit Enforcement
```javascript
it('unit test - exceed daily limit', async () => {
  const uw = await walletService.getUserWallet(userId);
  const product6 = await knex('points_store').where({ id: 6 }).first();
  
  // First purchase - should succeed
  const { balance: balance1 } = await buyPointProduct(data6);
  expect(balance1).to.eq(uw.balance + Number(product6.points));
  expect(spy1.callCount).to.eq(1);  // Email notification sent
  
  // Second purchase - should succeed
  const { balance: balance2 } = await buyPointProduct(data6);
  expect(balance2).to.eq(uw1.balance + Number(product6.points));
  expect(spy1.callCount).to.eq(2);  // Second email notification
  
  // Third purchase - should fail (daily limit exceeded)
  await expect(buyPointProduct(data1)).to.be.rejectedWith(
    'ERROR_COIN_PURCHASE_DAILY_LIMIT',
  );
  expect(spy1.callCount).to.eq(3);  // Limit warning email
  
  // Fourth attempt - user gets suspended
  await expect(buyPointProduct(data1)).to.be.rejectedWith(
    'ERROR_USER_COIN_SUSPENDED',
  );
  expect(spy1.callCount).to.eq(4);  // Suspension email
  expect(spy2.callCount).to.eq(1);  // User notification email
});
```

### Integration Tests

#### API Endpoint Testing
```javascript
it('integration test - normal happy case', async () => {
  const uw = await walletService.getUserWallet(userid);
  const product = await knex('points_store').where({ id: 1 }).first();
  
  const pointProduct = {
    product_id: product.id,
  };
  
  const resp = await request.set(auth).post(url).send(pointProduct);
  const { result, data } = resp.body;
  
  expect(result).to.eq('success');
  expect(data).to.include.keys(['balance']);
  expect(data.balance).to.eq(uw.balance + Number(product.points));
});
```

#### Blocked User API Response
```javascript
it('integration test - blocked user cannot buy coins', async () => {
  await knex('block_users').insert({ user_id: userid, is_deleted: 'F' });
  
  const resp = await request.set(auth).post(url).send(pointProduct);
  const { result, error } = resp.body;
  
  expect(result).to.eq('fail');
  expect(error).to.include.keys(['code', 'msg']);
  expect(error.code).to.eq(23032);
  expect(error.msg).to.eq(
    'For your protection, we have temporarily limited your account. Please check your email for more information.',
  );
});
```

## Error Handling

### Error Codes

#### User Blocking
- **ERROR_USER_COIN_SUSPENDED**: User account suspended for excessive purchases
- **Code**: 23032
- **Message**: "For your protection, we have temporarily limited your account..."

#### Purchase Limits
- **ERROR_COIN_PURCHASE_DAILY_LIMIT**: Daily purchase limit exceeded
- **Trigger**: Multiple high-value purchases in single day

#### Product Validation
- **ERROR_POINT_PRODUCT_NOT_FOUND**: Invalid product ID specified
- **ERROR_BAD_REQUEST_BODY**: Missing Stripe customer ID

#### Payment Processing
- **ERROR_CHARGE_FAILED**: Stripe payment processing failure

## Business Logic

### Daily Limit System
1. **Purchase Tracking**: Monitor daily purchase amounts per user
2. **Threshold Detection**: Flag users exceeding configured limits
3. **Progressive Enforcement**: Warning → Limit → Suspension
4. **Email Notifications**: Notify users and administrators

### User Blocking System
- **Automatic Blocking**: System blocks users exceeding limits
- **Manual Blocking**: Administrators can manually block users
- **Block Status**: `is_deleted: 'F'` indicates active block

### Product Configuration
```javascript
const productStructure = {
  id: 'integer',
  name: 'string',
  points: 'decimal',      // Coin amount
  price: 'decimal',       // USD price
  currency: 'string',     // USD
  is_active: 'boolean'
};
```

## Email Notification System

### Notification Types
1. **Purchase Confirmation**: Successful coin purchase
2. **Limit Warning**: Approaching daily limit
3. **Account Suspension**: Account temporarily blocked
4. **User Notification**: Direct user communication

### Email Service Integration
```javascript
const walletNotify = require('@app/src/services/walletNotify');

// Administrative notifications
await walletNotify.emailNotify(userId, 'purchase_limit_exceeded');

// User notifications  
await walletNotify.emailNotifyUser(userId, 'account_suspended');
```

## Payment Integration

### Stripe Requirements
- **Customer ID**: User must have valid Stripe customer ID
- **Payment Method**: Default payment method attached
- **Error Handling**: Graceful handling of payment failures

### Transaction Recording
```javascript
const transactionRecord = {
  user_id: userId,
  product_id: productId,
  points: productPoints,
  amount: productPrice,
  currency: 'USD',
  stripe_transaction_id: 'stripe_charge_id',
  status: 'completed'
};
```

## Database Schema

### Key Tables

#### points_store
- **Purpose**: Available coin products
- **Fields**: ID, name, points, price, currency

#### purchase_transaction / purchase_transaction_upgrade
- **Purpose**: Purchase history tracking
- **Fields**: User ID, product details, amounts, timestamps

#### block_users
- **Purpose**: User blocking management
- **Fields**: User ID, block status, timestamps

#### coin_activity_log
- **Purpose**: Detailed coin transaction logging
- **Fields**: User ID, activity type, amounts, timestamps

## Performance Considerations

### Database Optimization
- **Indexed Queries**: Optimize frequent lookups by user ID and date
- **Cleanup Strategy**: Regular cleanup of old transaction data
- **Connection Pooling**: Efficient database connection management

### Email Performance
- **Async Processing**: Email notifications sent asynchronously
- **Batch Processing**: Group multiple notifications when possible
- **Rate Limiting**: Prevent email spam from system errors

## Security Features

### Fraud Prevention
- **Daily Limits**: Prevent excessive purchases
- **User Blocking**: Automatic suspension for suspicious activity
- **Payment Validation**: Stripe integration provides fraud protection

### Data Protection
- **PCI Compliance**: Secure payment data handling
- **Transaction Encryption**: Sensitive data encryption
- **Audit Trails**: Complete transaction history

## Monitoring and Analytics

### Key Metrics
- **Purchase Volume**: Track daily coin purchase volumes
- **User Behavior**: Monitor purchase patterns
- **Block Rate**: Track user blocking frequency
- **Email Delivery**: Monitor notification success rates

### Alert Conditions
- **High Block Rate**: Unusual number of user blocks
- **Payment Failures**: Increased payment processing errors
- **System Errors**: Service availability issues

## Usage Examples

### Purchasing Coins
```javascript
const purchaseData = {
  userId: 1006,
  zone: 'America/Chicago',
  product_id: 1
};

try {
  const result = await buyPointProduct(purchaseData);
  console.log(`New balance: ${result.balance} coins`);
} catch (error) {
  switch (error.message) {
    case 'ERROR_USER_COIN_SUSPENDED':
      console.log('Account suspended');
      break;
    case 'ERROR_COIN_PURCHASE_DAILY_LIMIT':
      console.log('Daily limit exceeded');
      break;
    case 'ERROR_CHARGE_FAILED':
      console.log('Payment failed');
      break;
  }
}
```

### API Integration
```javascript
const response = await fetch('/api/v2/points/buy', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'userid': '1006',
    'zone': 'America/Chicago'
  },
  body: JSON.stringify({
    product_id: 1
  })
});

const result = await response.json();
if (result.result === 'success') {
  console.log(`Balance: ${result.data.balance}`);
}
```

This test suite ensures robust coin purchasing functionality with comprehensive fraud prevention, user protection, and system monitoring capabilities.