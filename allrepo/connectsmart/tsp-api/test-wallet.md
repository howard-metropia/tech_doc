# Test Documentation: Wallet API

## Overview
This comprehensive test suite validates the Wallet functionality within the TSP system, covering digital wallet management, payment processing, token systems, auto-refill capabilities, and Stripe integration. The wallet system supports both coins and tokens as digital currencies for the transportation platform.

## Test Configuration
- **File**: `test/test-wallet.js`
- **Framework**: Mocha with Chai assertions and Supertest for HTTP testing
- **External Dependencies**: Stripe payment processing, moment-timezone for date handling
- **Database**: MySQL portal database with multiple wallet-related tables
- **Authentication**: Bearer token-based authentication (userid: 1003)

## Service Functions Tested

### 1. getUserWallet(userId)
**Purpose**: Retrieves comprehensive wallet information including auto-refill settings

**Test Validation**:
```javascript
const wallet = await getUserWallet(userId);
expect(wallet).to.have.property('balance');           // Current coin balance
expect(wallet.balance).is.a('number');
expect(wallet).to.have.property('auto_refill');       // Auto-refill enabled
expect(wallet.auto_refill).is.a('boolean');
expect(wallet).to.have.property('below_balance');     // Refill trigger threshold
expect(wallet.below_balance).is.a('number');
expect(wallet).to.have.property('stripe_customer_id'); // Stripe integration
expect(wallet.stripe_customer_id).is.a('string');
expect(wallet).to.have.property('refill_plan');       // Selected refill plan
expect(wallet.refill_plan).to.have.property('points');
expect(wallet.refill_plan).to.have.property('amount');
expect(wallet.refill_plan).to.have.property('currency');
expect(wallet.refill_plan).to.have.property('display_rate');
```

### 2. getUserToken(tokenId, userId)
**Purpose**: Retrieves specific token information for user

**Test Validation**:
```javascript
const userToken = await getUserToken(1, userId);
expect(userToken).to.have.property('balance');    // Token balance
expect(userToken.balance).is.a('string');
expect(userToken).to.have.property('name');       // Token name
expect(userToken.name).is.a('string');
expect(userToken).to.have.property('expires');    // Expiration date
expect(userToken.expires).is.a('string');
```

### 3. getAvailableToken(userId)
**Purpose**: Retrieves all available tokens for user

**Test Validation**:
```javascript
const availableTokens = await getAvailableToken(userId);
expect(availableTokens.length).to.not.equal(0);  // Has available tokens
```

## API Endpoints Tested

### 1. GET /wallet/summary (v1 & v2)
**Purpose**: Retrieves comprehensive wallet overview

**Response Structure**:
```javascript
{
  result: 'success',
  data: {
    balance: {
      coins: Number,        // Coin balance
      tokens: Number        // Token balance
    },
    auto_refill: {
      enable: Boolean,      // Auto-refill status
      below_balance: Number, // Trigger threshold
      refill_points: Number  // Refill amount
    },
    first_time_coins: Boolean,    // First-time user flags
    first_time_tokens: Boolean,
    free_points: Boolean,         // Available free points
    messages: Boolean,            // Wallet messages
    special_sale: Boolean         // Special offers
  }
}
```

**V2 Additional Fields**:
- Enhanced auto-refill configuration
- Additional wallet metadata

### 2. GET /point_store
**Purpose**: Retrieves available point packages for purchase

**Response Structure**:
```javascript
{
  result: 'success',
  data: {
    general_products: [
      {
        id: Number,              // Product ID
        points: Number,          // Points included
        amount: Number,          // Price
        original_amount: Number, // Original price (before discounts)
        currency: String,        // Currency code
        display_rate: Number,    // Points per dollar
        ended_on: Date          // Sale end date
      }
    ],
    special_products: [
      // Same structure as general_products
    ]
  }
}
```

### 3. GET /refill_plan
**Purpose**: Retrieves available auto-refill plans

**Response Structure**:
```javascript
{
  result: 'success',
  data: {
    plans: [
      {
        id: Number,           // Plan ID
        points: Number,       // Points per refill
        amount: Number,       // Cost per refill
        currency: String,     // Currency
        display_rate: Number  // Points per dollar
      }
    ]
  }
}
```

### 4. GET /wallet/setting (v1 & v2)
**Purpose**: Retrieves wallet configuration settings

**Response Structure**:
```javascript
{
  result: 'success',
  data: {
    customer: Boolean,        // Stripe customer status
    auto_refill: Boolean,     // Auto-refill enabled
    below_balance: Number,    // Refill trigger
    refill_plan: {           // Current refill plan
      id: Number,
      points: Number,
      amount: Number,
      currency: String,
      display_rate: Number
    }
  }
}
```

**V2 Additional Fields**:
```javascript
{
  auto_reload_max_point: Number,   // Maximum reload amount
  auto_reload_min_point: Number,   // Minimum reload amount
  auto_reload_step_size: Number    // Reload increment size
}
```

### 5. PUT /wallet/setting (v1 & v2)
**Purpose**: Updates wallet configuration settings

**Request Structure**:
```javascript
{
  auto_refill: Boolean,      // Enable/disable auto-refill
  below_balance: Number,     // Trigger threshold
  refill_plan_id: Number     // Selected refill plan
}
```

**Success Response**:
```javascript
{
  result: 'success',
  data: {
    auto_refill: Boolean,
    below_balance: Number,
    refill_points: Number     // Points from selected plan
  }
}
```

**Error Response (Invalid Plan)**:
```javascript
{
  result: 'fail',
  error: {
    code: 23008,
    msg: 'Refill plan not found'
  }
}
```

## Database Schema Integration

### Core Tables
- **user_wallet**: Main wallet data with balance and Stripe integration
- **token_transaction**: Token transaction history
- **points_transaction**: Coin transaction history  
- **purchase_transaction**: Purchase history
- **refill_plan**: Available auto-refill plans
- **notification_type**: Wallet notification types

### Test Data Management
```javascript
before(async () => {
  // Setup wallet with Stripe customer
  await knex('user_wallet').where('user_id', userId).update({
    auto_refill: 'F',
    balance: 0,
    stripe_customer_id: 'cus_IF4ZsdQTbeP8y7',
    payment_way: 1
  });
  
  // Create token transaction for testing
  const tokenTransaction = await knex('token_transaction').insert({
    user_id: userId,
    activity_type: 1,
    tokens: 5,
    balance: 5,
    note: 'metropia test',
    campaign_id: 1,
    issued_on: moment.utc().subtract(1, 'days').format('YYYY-MM-DD HH:mm:ss'),
    expired_on: moment.utc().add(1, 'days').format('YYYY-MM-DD HH:mm:ss')
  });
});

after(async () => {
  // Cleanup test data
  await knex('user_wallet').where('user_id', userId).update({
    stripe_customer_id: null,
    payment_way: null
  });
});
```

## Payment Integration

### Stripe Integration
- **Customer Management**: Stripe customer ID storage and management
- **Auto-Refill**: Automated payment processing when balance falls below threshold
- **Payment Methods**: Credit card processing through Stripe API
- **Transaction Tracking**: Comprehensive transaction history

### Currency Support
- **Multi-Currency**: Support for different currencies (USD, EUR, etc.)
- **Display Rates**: Points per currency unit for user transparency
- **Pricing Tiers**: Different pricing for general vs. special products

## Auto-Refill System

### Configuration Options
- **Enable/Disable**: Toggle auto-refill functionality
- **Threshold**: Balance level that triggers auto-refill
- **Refill Amount**: Points to purchase during auto-refill
- **Plan Selection**: Choose from available refill plans

### Business Logic
```javascript
// Auto-refill trigger logic
if (userBalance < belowBalance && autoRefillEnabled) {
  const refillPlan = await getRefillPlan(userRefillPlanId);
  await processStripePayment(refillPlan.amount, stripeCustomerId);
  await addPointsToWallet(userId, refillPlan.points);
}
```

### Validation Rules
- **Customer Required**: Must have Stripe customer ID for auto-refill
- **Plan Validation**: Refill plan must exist and be active
- **Balance Limits**: Configurable min/max reload amounts
- **Step Size**: Reload amounts must follow defined increments

## Token System

### Token Types
- **Campaign Tokens**: Earned through specific campaigns
- **Agency Tokens**: Issued by transportation agencies
- **Promotional Tokens**: Special promotions and events
- **Expiring Tokens**: Time-limited token validity

### Token Management
- **Balance Tracking**: Individual token balance per type
- **Expiration Handling**: Automatic expiration of time-limited tokens
- **Transaction History**: Complete audit trail of token transactions
- **Campaign Integration**: Token issuance through marketing campaigns

## Business Logic Validation

### Wallet State Validation
```javascript
it('shall put wallet setting successfully for v1 api', async () => {
  const response = await request.put(url).set(auth).send({
    auto_refill: true,
    below_balance: 5,
    refill_plan_id: 1
  });
  
  // Validate database state changes
  const userWallet = await knex('user_wallet').where('user_id', userId).first();
  expect(userWallet.auto_refill).to.equal('T');
  expect(Number(userWallet.below_balance)).to.equal(5);
  
  // Validate plan points match response
  const plan = await knex('refill_plan').where('id', 1).first();
  expect(Number(plan.points)).to.equal(response.body.data.refill_points);
});
```

### Error Handling
- **Invalid Plans**: Proper error when refill plan doesn't exist
- **Authentication**: Secure access to wallet operations
- **Data Validation**: Input validation for all parameters
- **Transaction Safety**: Atomic operations for financial transactions

## Security Features

### Authentication
- Bearer token required for all wallet operations
- User ownership validation for all wallet access
- Secure token storage and transmission

### Financial Security
- Stripe PCI compliance for payment processing
- Transaction logging for audit trails
- Auto-refill fraud prevention
- Secure customer ID management

### Data Protection
- Encrypted sensitive financial data
- Secure API communication
- Transaction history protection
- User privacy compliance

## Performance Optimization

### Caching Strategy
- Wallet balance caching for frequent access
- Token balance optimization
- Plan data caching for quick retrieval

### Database Optimization
- Efficient wallet queries with proper indexing
- Transaction history pagination
- Batch processing for token operations

## Test Coverage

### Unit Test Coverage
- ✅ Wallet service functions
- ✅ Token management operations
- ✅ Auto-refill logic validation
- ✅ Database integration

### API Test Coverage
- ✅ Wallet summary endpoints (v1 & v2)
- ✅ Point store functionality
- ✅ Refill plan management
- ✅ Wallet settings CRUD operations

### Integration Test Coverage
- ✅ Stripe payment integration
- ✅ Database transaction consistency
- ✅ Auto-refill workflow
- ✅ Token expiration handling

### Error Scenario Coverage
- ✅ Invalid refill plan handling
- ✅ Authentication failures
- ✅ Payment processing errors
- ✅ Data validation failures

## Business Value

### User Experience
- Seamless payment processing
- Automated wallet management
- Transparent pricing and rates
- Multiple currency support

### Revenue Generation
- Point sales and refill plans
- Auto-refill increases transaction volume
- Special promotions and discounts
- Token-based marketing campaigns

### Operational Efficiency
- Automated payment processing
- Comprehensive transaction tracking
- Fraud prevention and security
- Scalable financial infrastructure

This test suite ensures the wallet system provides reliable, secure, and user-friendly financial services within the TSP platform.