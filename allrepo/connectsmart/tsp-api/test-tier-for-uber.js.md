# test-tier-for-uber.js Technical Documentation

## Purpose

Comprehensive unit test suite for Uber ride refund processing with tier-based benefit calculations, testing complex financial transaction scenarios where estimated fares, actual fares, and tier benefits interact.

## Core Functionality

### Refund with Benefit System

#### Service: `refundWithBenefit`
- **Purpose**: Process Uber ride refunds considering tier benefits
- **Parameters**: 
  - `userId`: User receiving refund
  - `estimatedFare`: Original fare estimate
  - `actualFare`: Final charged amount
  - `benefit`: User's tier-based credit amount
  - `note`: Transaction description

#### Account Structure
```javascript
const UBER_ACCOUNT = 2107;     // Uber service account
const SYSTEM_ACCOUNT = 2002;   // Platform system account
```

## Refund Logic Categories

### Group 1: Actual Fare < Benefit
When the ride cost is less than available tier benefits:

#### Scenario 1: eFare: $6, aFare: $2, benefit: $8
```javascript
// Results:
// - User refund: $0 (no direct refund needed)
// - Benefit usage: $2 (only actual fare amount)
// - System transactions: -$2 (to Uber), +$6 (from estimated)
```

#### Scenario 2: eFare: $16, aFare: $2, benefit: $4  
```javascript
// Results:
// - User refund: $12 (estimated - benefit amount)
// - Benefit usage: $2 (actual fare covered by benefit)
// - System handles estimated vs actual difference
```

### Group 2: Actual Fare = Benefit
When ride cost exactly matches tier benefit:

#### Scenario: eFare: $25, aFare: $8, benefit: $8
```javascript
// Results:
// - User refund: $17 (estimated - benefit)
// - Benefit usage: $8 (full benefit consumed)
// - Clean transaction with exact benefit match
```

### Group 3: Actual Fare > Benefit  
When ride cost exceeds available benefits:

#### Scenario: eFare: $100, aFare: $10, benefit: $8
```javascript
// Results:
// - User refund: $90 (estimated - actual fare)
// - Benefit usage: $8 (full benefit applied)
// - User pays $2 out of pocket (actual - benefit)
```

## Transaction Flow Architecture

### Benefit Transaction Recording
```javascript
// Credit issuance (positive amount)
const creditTransaction = {
  user_id: userId,
  benefit_amount: 8,        // Tier benefit amount
  transaction_amount: 0,    // Associated user transaction
  transaction_id: tripId
};

// Credit usage (negative amount)  
const usageTransaction = {
  user_id: userId,
  benefit_amount: -2,       // Amount used
  transaction_amount: 12,   // User refund amount
  transaction_id: tripId
};
```

### Points Transaction Types
```javascript
// User refund transaction
const userTransaction = {
  user_id: userId,
  points: 12,              // Positive amount (refund)
  payer: UBER_ACCOUNT,     // From Uber account
  payee: userId,           // To user
  activity_type: 18        // Refund type
};

// System settlement transaction
const systemTransaction = {
  user_id: SYSTEM_ACCOUNT,
  points: -8,              // Negative amount (payment)
  payer: UBER_ACCOUNT,     // From Uber
  payee: SYSTEM_ACCOUNT,   // To system
  activity_type: 18
};
```

## Test Architecture

### Test User Setup
```javascript
const testUserId = 5566;

before(async () => {
  // Create test user
  await knex('auth_user').insert({
    id: testUserId,
    first_name: 'Test',
    last_name: 'User',
    email: 'test.refund@example.com',
    password: 'hashed_password',
    phone_number: '+1234567890',
  });

  // Create test wallet
  [testWalletId] = await knex('user_wallet').insert({
    user_id: testUserId,
    balance: 1000,
    auto_refill: 'F',
    below_balance: 5,
    stripe_customer_id: null,
  });
});
```

### Transaction Cleanup
```javascript
afterEach(async () => {
  // Clean up all test transactions
  await knex('points_transaction').where('user_id', testUserId).del();
  await knex('points_transaction')
    .where('user_id', UBER_ACCOUNT)
    .where('created_on', '>=', startAt)
    .del();
  await knex('uber_benefit_transaction').where('user_id', testUserId).del();
});
```

## Complex Scenarios

### Scenario Validation Patterns
```javascript
const validateRefundScenario = async (estimatedFare, actualFare, benefit) => {
  await refundWithBenefit(userId, estimatedFare, actualFare, benefit, 'Test case');

  // Verify user refund transaction
  const userRefundTx = await knex('points_transaction')
    .where('user_id', testUserId)
    .orderBy('id', 'desc')
    .first();

  // Verify system transactions
  const systemTxs = await knex('points_transaction')
    .where('user_id', SYSTEM_ACCOUNT)
    .where('created_on', '>=', testStartTime)
    .orderBy('id', 'desc');

  // Verify benefit transactions  
  const benefitTxs = await knex('uber_benefit_transaction')
    .where('user_id', testUserId)
    .orderBy('id', 'desc');

  return { userRefundTx, systemTxs, benefitTxs };
};
```

### Edge Cases

#### Zero Actual Fare (Free Ride)
```javascript
// eFare: $7.92, aFare: $0, benefit: $8
// Result: Only benefit usage transaction, no user refund needed
```

#### Exact Benefit Match
```javascript  
// eFare: $8, aFare: $8, benefit: $8
// Result: Perfect balance, no user refund
```

## Business Logic Rules

### Refund Calculation
1. **User Refund**: `max(0, estimatedFare - min(actualFare, benefit))`
2. **Benefit Usage**: `min(actualFare, benefit)`
3. **Out-of-Pocket**: `max(0, actualFare - benefit)`

### Transaction Requirements
- **Atomic Operations**: All related transactions must succeed/fail together
- **Balance Validation**: Ensure account balances remain consistent
- **Audit Trail**: Complete transaction history maintained

## Account Flow Diagrams

### Benefit Usage Flow
```
User Tier Benefit ($8) → Uber Ride ($2) → Remaining Benefit ($6)
                      ↓
System Records: +$8 benefit issued, -$2 benefit used
```

### Refund Flow  
```
Estimated Fare ($16) → Actual Fare ($2) → User Refund ($12)
                    ↓
Uber Account: -$16 → System: +$4 (benefit) → User: +$12
```

## Error Handling

### Transaction Failures
- **Rollback Strategy**: Reverse all related transactions on failure
- **Consistency Checks**: Validate account balances after operations
- **Error Logging**: Comprehensive error tracking and reporting

### Data Integrity
- **Foreign Key Constraints**: Maintain referential integrity
- **Amount Validation**: Prevent negative balances where inappropriate
- **Duplicate Prevention**: Avoid processing same transaction twice

## Performance Considerations

### Database Optimization
- **Transaction Batching**: Group related operations
- **Index Strategy**: Optimize frequent lookup patterns
- **Connection Pooling**: Efficient database connection management

### Memory Management
- **Large Datasets**: Handle high-volume transaction processing
- **Cleanup Strategy**: Automatic cleanup of old test data
- **Resource Limits**: Prevent memory leaks in long-running tests

## Integration Testing

### Mock Strategy
```javascript
beforeEach(() => {
  sandbox = sinon.createSandbox();
});

afterEach(() => {
  sandbox.restore();
});
```

### Test Isolation
- **Independent Tests**: Each test runs in isolation
- **Data Cleanup**: Thorough cleanup between tests
- **State Reset**: Reset all external dependencies

## Usage Examples

### Processing Complex Refund
```javascript
await refundWithBenefit(
  userId,
  13.45,  // Estimated fare
  5.17,   // Actual fare  
  4.00,   // Tier benefit
  'Complex refund scenario'
);

// Expected outcomes:
// - User refund: $8.28
// - Benefit used: $4.00
// - User pays: $1.17 out of pocket
```

### Validating Results
```javascript
const userTx = await knex('points_transaction')
  .where('user_id', userId)
  .orderBy('id', 'desc')
  .first();

expect(Number(userTx.points)).to.equal(8.28);

const benefitTxs = await knex('uber_benefit_transaction')
  .where('user_id', userId);

expect(benefitTxs).to.have.lengthOf(2);
expect(Number(benefitTxs[0].benefit_amount)).to.equal(-4);
expect(Number(benefitTxs[1].benefit_amount)).to.equal(4);
```

This test suite ensures accurate financial processing for Uber ride refunds, accounting for complex interactions between estimated fares, actual charges, and tier-based benefits while maintaining strict transaction integrity.