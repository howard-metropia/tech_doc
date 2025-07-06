# test-tickets.js Technical Documentation

## Purpose

Integration test suite for transit ticket management, covering ticket search, payment processing, and bytemark ticketing system integration.

## Core Functionality

### Ticket Management APIs

#### 1. Find Payments
- **Route**: `find_payments`
- **Method**: GET
- **Endpoint**: `/api/v2/wallet/payments`
- **Purpose**: Retrieve user payment history
- **Authentication**: User ID header required

#### 2. Find Tickets
- **Route**: `find_tickets`
- **Method**: GET
- **Endpoint**: `/api/v2/tickets/search`
- **Purpose**: Search available transit tickets
- **Query Parameters**:
  - `type`: Ticket category ('bus_metro', 'park_ride', or empty)

#### 3. Pay for Tickets
- **Service**: `payTicket`
- **Purpose**: Process ticket purchases using platform coins
- **Integration**: Bytemark ticketing system

## Test Architecture

### User Setup
```javascript
describe('integration test ticket related api', () => {
  let userId = 0;
  
  before(async () => {
    userId = await knex('auth_user').insert({}, ['id']);
  });
  
  after(async () => {
    await knex('auth_user').where({ id: userId }).delete();
  });
});
```

### Ticket Types Tested

#### Bus/Metro Tickets
```javascript
it('search bus_metro', async () => {
  const response = await request
    .get(router.url('find_tickets'))
    .query({ type: 'bus_metro' })
    .set('userid', userId);
  expect(response.status).to.equal(200);
});
```

#### Park & Ride Tickets
```javascript
it('search park_ride', async () => {
  const response = await request
    .get(router.url('find_tickets'))
    .query({ type: 'park_ride' })
    .set('userid', userId);
  expect(response.status).to.equal(200);
});
```

#### General Search
```javascript
it('search empty', async () => {
  const response = await request
    .get(router.url('find_tickets'))
    .set('userid', userId);
  expect(response.status).to.equal(200);
});
```

## Payment Processing

### Coin-Based Payment
```javascript
const paymentData = {
  user_id: userId,
  zone: 'America/Chicago',
  payment_type: 'coins',
  items: [{
    product_uuid: 'e71c0399-1a5e-4a6a-94ce-48ad9f541144',
    qty: 1,
    price: 1.25,
  }],
  ctx: {
    request: {
      path: 'src/services/tickets.js/payTicket',
      method: 'UnitTest',
    },
  },
};
```

### Bytemark Integration
- **Product UUID**: `e71c0399-1a5e-4a6a-94ce-48ad9f541144`
- **Price**: $1.25 (Local Single Ride)
- **Payment Method**: Platform coins
- **Validation**: Bytemark system check before purchase

## Service Integration

### Prerequisites Setup
```javascript
before(async () => {
  // Add sufficient coins for purchase
  await pointsTransaction(userId, 6, 1.25, 'buy tickets unit test', false);
  
  // Validate bytemark integration
  await bytemarkCheck({
    request: {
      header: { userid: userId },
      method: 'UnitTest',
      path: 'test-tickets',
    },
  });
});
```

### Payment Transaction Flow
1. **Point Addition**: Add 1.25 coins to user wallet
2. **Bytemark Validation**: Verify system connectivity
3. **Ticket Purchase**: Process payment through `payTicket` service
4. **Response Validation**: Confirm successful transaction

## Response Structure

### Successful Payment Response
```javascript
const expectedResponse = {
  status: 1,
  result: {
    payment_type: 'coins',
    success: true,
    // Additional payment details
  }
};
```

### Response Validation
```javascript
it('Buy bytemark tickets by coins', async () => {
  const result = await payTicket(paymentData);
  
  expect(result).to.have.own.property('status');
  expect(result.status).to.eq(1);
  
  expect(result).to.have.own.property('result');
  expect(result.result).to.have.own.property('payment_type');
  expect(result.result.payment_type).to.eq('coins');
  
  expect(result.result).to.have.own.property('success');
  expect(result.result.success).to.eq(true);
});
```

## External Dependencies

### Bytemark Ticketing System
- **Purpose**: Third-party transit ticketing provider
- **Integration**: API-based ticket validation and purchasing
- **Products**: Local single ride, day passes, monthly passes

### Platform Services
- **Wallet Service**: Manages user coin balances
- **Points Transaction**: Handles coin deduction for purchases
- **Authentication**: User validation and authorization

## Data Models

### Ticket Products
- **Product UUID**: Unique identifier for ticket types
- **Pricing**: Fixed or dynamic pricing based on transit agency
- **Validity**: Time-based or usage-based ticket validation

### Payment Records
- **Transaction ID**: Unique payment identifier
- **User Association**: Links payment to user account
- **Payment Method**: Coins, credit card, or other methods
- **Status Tracking**: Success, failure, pending states

## Error Handling

### Authentication Errors
- **Missing User ID**: Return appropriate error code
- **Invalid User**: Reject unauthorized requests

### Payment Failures
- **Insufficient Funds**: Check coin balance before processing
- **Bytemark Errors**: Handle third-party service failures
- **Transaction Rollback**: Reverse partial transactions on failure

### Network Issues
- **Service Timeout**: Handle slow bytemark responses
- **Connection Failures**: Graceful degradation when services unavailable

## Integration Testing Strategy

### Test Isolation
- **User Creation**: Fresh user for each test suite
- **Data Cleanup**: Remove test data after completion
- **Service Mocking**: Mock external dependencies when needed

### End-to-End Validation
1. **User Setup**: Create test user with wallet
2. **Fund Wallet**: Add coins for ticket purchase
3. **Service Check**: Validate bytemark connectivity
4. **Purchase Flow**: Complete ticket buying process
5. **Verification**: Confirm all systems updated correctly

## Performance Considerations

### Response Times
- **API Endpoints**: Fast response for ticket searches
- **Payment Processing**: Optimized coin deduction
- **External Calls**: Efficient bytemark API integration

### Scalability
- **Concurrent Users**: Handle multiple simultaneous purchases
- **Peak Load**: Support high-traffic periods
- **Cache Strategy**: Cache ticket product information

## Security Features

### Payment Security
- **User Validation**: Verify user identity for all transactions
- **Amount Verification**: Validate payment amounts match ticket prices
- **Transaction Integrity**: Ensure atomic payment operations

### Data Protection
- **PCI Compliance**: Secure handling of payment information
- **User Privacy**: Protect personal and financial data
- **Audit Trail**: Maintain comprehensive transaction logs

## Business Logic

### Ticket Validation
- **Product Availability**: Check ticket availability before purchase
- **Price Verification**: Validate current pricing
- **Zone Restrictions**: Enforce geographic limitations

### Wallet Integration
- **Balance Checks**: Verify sufficient funds before processing
- **Transaction Recording**: Log all payment activities
- **Refund Processing**: Handle cancellations and refunds

## Usage Examples

### Searching for Tickets
```javascript
// Search all tickets
const response = await request
  .get('/api/v2/tickets/search')
  .set('userid', userId);

// Search specific type
const busTickets = await request
  .get('/api/v2/tickets/search')
  .query({ type: 'bus_metro' })
  .set('userid', userId);
```

### Processing Payment
```javascript
const purchase = await payTicket({
  user_id: userId,
  zone: 'America/Chicago',
  payment_type: 'coins',
  items: [{ product_uuid: 'ticket-uuid', qty: 1, price: 1.25 }]
});
```

This test suite ensures reliable ticket purchasing functionality, covering search capabilities, payment processing, and integration with the bytemark ticketing system while maintaining security and performance standards.