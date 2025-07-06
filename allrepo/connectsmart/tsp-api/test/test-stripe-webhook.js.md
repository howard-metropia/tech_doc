# test-stripe-webhook.js

## Overview
Test suite for Stripe webhook integration in the TSP API. Tests the handling of Stripe payment dispute events, webhook signature verification, and automatic user blocking functionality.

## File Location
`/test/test-stripe-webhook.js`

## Dependencies
- **crypto**: Node.js cryptographic functionality for signature verification
- **stripe**: Stripe SDK for payment processing
- **supertest**: HTTP assertions for API testing
- **chai**: BDD/TDD assertion library
- **Models**: AuthUsers, UserWallets, BlockUsers
- **Config**: Stripe configuration (apiKey, webHookSecret)

## Test Configuration

### Test User
```javascript
const userId = 1001;
```

### Authentication Setup
- User ID: 1001
- Bearer token from AuthUsers table
- Content-Type: application/json
- Stripe signature header for webhook verification

## Stripe Integration

### Configuration
```javascript
const stripeConfig = require('config').vendor.stripe;
const stripe = require('stripe')(stripeConfig.apiKey);
```

### Test Charge Creation
```javascript
const charge = await stripe.charges.create({
  amount: 50,
  currency: 'usd',
  customer: userStripe.stripe_customer_id,
  description: `Purchase 0.5 coins.`
});
```

## Webhook Payload Structure

### Dispute Event Payload
```javascript
const payload = {
  id: 'evt_1NG8Du2eZvKYlo2CUI79vXWy',
  object: 'event',
  data: {
    object: {
      id: 'du_1PRoHxJDc0QAU0fl1Mbv8WA6',
      object: 'dispute',
      amount: 500,
      charge: chargeId
    }
  },
  type: 'charge.dispute.created'
};
```

### Event Types Handled
- **charge.dispute.created**: Payment dispute initiated by customer

## Security Implementation

### Webhook Signature Verification
```javascript
const unixTime = Math.floor(new Date().getTime() / 1000);
const signature = crypto
  .createHmac('sha256', stripeConfig.webHookSecret)
  .update(`${unixTime}.${JSON.stringify(payload)}`, 'utf8')
  .digest('hex');
auth['stripe-signature'] = `t=${unixTime},v1=${signature}`;
```

### Security Features
- **HMAC-SHA256**: Cryptographic signature verification
- **Timestamp Validation**: Prevents replay attacks
- **Webhook Secret**: Shared secret for signature generation
- **Header Format**: Stripe-standard signature format

## Test Cases

### 1. Successful Webhook Processing
**Endpoint**: `POST /stripe/webhook`

**Test Flow**:
1. Create valid Stripe charge
2. Generate dispute event payload
3. Calculate valid webhook signature
4. Send webhook request
5. Verify event processing success

**Expected Response**:
```json
{
  "received": true
}
```

### 2. User Blocking Verification
**Follow-up Test**: Access protected endpoint after dispute

**Process**:
1. Wait for async processing (2-second delay)
2. Attempt to access user favorites
3. Verify user is blocked

**Expected Error**:
```json
{
  "result": "fail",
  "error": {
    "code": 23030,
    "msg": "You have been blocked, please contact our customer service for support."
  }
}
```

### 3. Invalid Signature Handling
**Test**: Fake signature verification

**Process**:
1. Use invalid stripe-signature header
2. Send webhook request
3. Verify signature validation failure

**Expected Error**:
```json
{
  "result": "fail",
  "error": {
    "code": 10001,
    "msg": "Unable to extract timestamp and signatures from header"
  }
}
```

## Database Operations

### User Wallet Integration
```javascript
const userStripe = await UserWallets.query()
  .select('stripe_customer_id', 'payment_way')
  .where('user_id', userId)
  .first();
```

### User Blocking Logic
```javascript
// Block user when dispute is created
block_type: 1,        // Dispute-related block
is_deleted: 'F'       // Active block
```

### Cleanup Operations
```javascript
await BlockUsers.query()
  .where({
    user_id: userId,
    block_type: 1,
    is_deleted: 'F'
  })
  .delete();
```

## Business Logic

### Dispute Handling Process
1. **Webhook Reception**: Stripe sends dispute event
2. **Signature Verification**: Validate webhook authenticity
3. **Event Processing**: Parse dispute details
4. **User Blocking**: Automatically block disputed user
5. **Access Restriction**: Prevent further API access

### Block Types
- **Type 1**: Payment dispute block
- **is_deleted**: 'F' for active blocks

## Error Handling

### Error Codes
- **10001**: Webhook signature validation error
- **23030**: User blocked error

### Security Measures
- **Signature Validation**: Prevents webhook spoofing
- **Timestamp Checking**: Prevents replay attacks
- **Secret Key Protection**: Validates webhook source

## Integration Points

### Stripe Services
- **Charges API**: Create test charges
- **Webhooks**: Receive dispute notifications
- **Customer Management**: Link to UserWallets

### Internal Systems
- **Authentication**: JWT token validation
- **User Management**: BlockUsers integration
- **Wallet System**: UserWallets customer linking

## Testing Best Practices

### Real Stripe Integration
- Uses actual Stripe API for charge creation
- Tests real webhook signature verification
- Validates actual payment dispute flow

### Data Management
- **Setup**: Creates real Stripe charge for testing
- **Cleanup**: Removes test blocks after execution
- **Isolation**: Uses specific test user ID

### Async Processing
- **Delay Handling**: 2-second wait for async operations
- **State Verification**: Confirms blocking took effect
- **Real-world Simulation**: Tests actual webhook timing

## Security Considerations

### Webhook Security
- **Signature Verification**: Mandatory for all webhooks
- **Timestamp Validation**: Prevents old webhook replay
- **Secret Management**: Uses environment configuration

### User Protection
- **Immediate Blocking**: Prevents further fraudulent activity
- **Clear Error Messages**: Informs user of block status
- **Customer Service Contact**: Provides resolution path

## Payment Dispute Management

### Automatic Response
- **Immediate Action**: Block user upon dispute creation
- **No Manual Intervention**: Fully automated process
- **Audit Trail**: BlockUsers table maintains history

### Customer Impact
- **API Access**: Immediately restricted
- **Clear Communication**: Error messages explain situation
- **Resolution Process**: Customer service contact required

This test suite ensures the TSP API properly handles Stripe payment disputes, maintains security through webhook verification, and protects the platform from fraudulent activity through automatic user blocking mechanisms.