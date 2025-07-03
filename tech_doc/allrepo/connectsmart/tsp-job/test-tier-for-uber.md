# TSP Job Test: Uber Tier Refund Process Test Documentation

## Quick Summary

**Purpose**: Comprehensive test suite for Uber tier-based refund system that validates benefit credit calculations across different fare scenarios.

**Key Features**:
- Tests tier-based refund logic with benefit credits
- Validates transaction processing for estimated vs actual fares
- Ensures proper database updates for user wallets, system accounts, and benefit transactions
- Covers three main scenario groups: actual fare less than benefit, equal to benefit, and greater than benefit

**Technology Stack**: Mocha testing framework, Chai assertions, Sinon for mocking, Knex.js for database operations

## Technical Analysis

### Code Structure

The test file implements a comprehensive testing suite for the `refundWithBenefit` service with the following architecture:

```javascript
// Core dependencies and setup
require('@maas/core/bootstrap');
const { refundWithBenefit } = require('@app/src/services/uber/guest-ride');
const UberBenefitTransaction = require('@app/src/models/UberBenefitTransaction');
```

### Key Components

**Test Setup and Teardown**:
- Creates test user with ID 5566 and associated wallet
- Manages database cleanup with proper transaction isolation
- Uses Sinon sandbox for mocking external dependencies

**Database Transaction Management**:
- Tracks points transactions for user, Uber account (2107), and system account (2002)
- Validates benefit transaction records with proper linking
- Ensures atomic operations with proper rollback capabilities

**Test Scenario Organization**:
1. **Group 1**: Actual fare < benefit (4 test cases)
2. **Group 2**: Actual fare = benefit (4 test cases) 
3. **Group 3**: Actual fare > benefit (2 test cases)

### Implementation Details

**Account System Architecture**:
```javascript
const UBER_ACCOUNT = 2107;    // Uber service account
const SYSTEM_ACCOUNT = 2002;  // System refund account
```

**Refund Processing Logic**:
- Estimated fare determines initial charge
- Actual fare determines final settlement
- Benefit credit impacts refund calculation
- System generates compensating transactions

**Database Schema Interactions**:
- `points_transaction`: Core financial transactions
- `uber_benefit_transaction`: Benefit tracking and audit trail
- `user_wallet`: User balance management
- `auth_user`: User account information

## Usage/Integration

### Test Execution

**Running Tests**:
```bash
# Run specific test file
npm test test/test-tier-for-uber.js

# Run with coverage
npm run test:coverage test/test-tier-for-uber.js
```

**Test Environment Setup**:
```javascript
// Database connection
const knex = require('@maas/core/mysql')('portal');

// Time-based filtering
const startAt = moment.utc().add(-1, 'minute').toISOString();
```

### Integration Points

**Service Integration**:
- Integrates with `@app/src/services/uber/guest-ride` service
- Uses `UberBenefitTransaction` model for benefit tracking
- Requires MySQL portal database connection

**Mock Data Management**:
```javascript
// Test user creation
await knex('auth_user').insert({
  id: testUserId,
  first_name: 'Test',
  last_name: 'User',
  email: 'test.refund@example.com'
});

// Wallet setup
await knex('user_wallet').insert({
  user_id: testUserId,
  balance: 1000,
  auto_refill: 'F'
});
```

## Dependencies

### Core Dependencies

**Testing Framework**:
- `chai`: Assertion library for behavior-driven testing
- `sinon`: Mocking and stubbing framework
- `mocha`: Test runner (implied through describe/it structure)

**Database Layer**:
- `@maas/core/mysql`: MySQL connection manager
- `knex`: SQL query builder for database operations

**Business Logic**:
- `@app/src/services/uber/guest-ride`: Core refund processing service
- `@app/src/models/UberBenefitTransaction`: Benefit transaction model

**Utilities**:
- `moment-timezone`: Date/time manipulation for transaction timing
- `@maas/core/bootstrap`: Application initialization

### External Services

**Database Requirements**:
- MySQL portal database with proper schema
- Tables: `auth_user`, `user_wallet`, `points_transaction`, `uber_benefit_transaction`

**Configuration Dependencies**:
- Database connection configuration
- Test environment settings
- Transaction isolation levels

## Code Examples

### Basic Test Structure

```javascript
describe('Tier for Uber', () => {
  describe('Ridehail Refund Service', () => {
    let sandbox;
    let testUserId;
    let testWalletId;

    before(async () => {
      // Setup test data
      testUserId = 5566;
      await knex('auth_user').insert({
        id: testUserId,
        first_name: 'Test',
        last_name: 'User',
        email: 'test.refund@example.com'
      });
    });

    beforeEach(() => {
      sandbox = sinon.createSandbox();
    });

    afterEach(async () => {
      sandbox.restore();
      // Cleanup transactions
      await knex('points_transaction').where('user_id', testUserId).del();
    });
  });
});
```

### Refund Testing Pattern

```javascript
it('should process transaction with eFare: 6, aFare: 2, benefit: 8', async () => {
  const testCase = {
    estimatedFare: 6,
    actualFare: 2,
    benefit: 8,
    note: 'Test refund case 1'
  };

  await refundWithBenefit(
    testUserId,
    testCase.estimatedFare,
    testCase.actualFare,
    testCase.benefit,
    testCase.note
  );

  // Verify user refund transaction
  const userRefundTx = await knex('points_transaction')
    .where('user_id', testUserId)
    .orderBy('id', 'desc')
    .first();

  expect(userRefundTx).not.to.exist;

  // Verify system transactions
  const systemRefundTxs = await knex('points_transaction')
    .where('user_id', SYSTEM_ACCOUNT)
    .where('created_on', '>=', startAt)
    .orderBy('id', 'desc');

  expect(systemRefundTxs).to.have.lengthOf(2);
  expect(Number(systemRefundTxs[0].points)).to.equal(-2);
  expect(Number(systemRefundTxs[1].points)).to.equal(6);
});
```

### Benefit Transaction Validation

```javascript
// Verify benefit transactions
const benefitTxs = await knex('uber_benefit_transaction')
  .where('user_id', testUserId)
  .orderBy('id', 'desc');

expect(benefitTxs).to.have.lengthOf(2);
expect(Number(benefitTxs[0].benefit_amount)).to.equal(-2);
expect(Number(benefitTxs[0].transaction_amount)).to.equal(0);
expect(Number(benefitTxs[1].benefit_amount)).to.equal(6);
expect(Number(benefitTxs[1].transaction_amount)).to.equal(0);
```

### Database Cleanup Pattern

```javascript
after(async () => {
  // Clean up test data
  await knex('auth_user').where('id', testUserId).del();
  await knex('user_wallet').where('id', testWalletId).del();
  await UberBenefitTransaction.query()
    .where('user_id', testUserId)
    .delete();
});

afterEach(async () => {
  sandbox.restore();
  // Clean up transactions after each test
  await knex('points_transaction').where('user_id', testUserId).del();
  await knex('points_transaction')
    .where('user_id', UBER_ACCOUNT)
    .where('created_on', '>=', startAt)
    .del();
  await knex('uber_benefit_transaction').where('user_id', testUserId).del();
});
```

This comprehensive test suite ensures the Uber tier-based refund system handles all scenarios correctly, from simple refunds to complex benefit credit calculations, while maintaining data integrity across multiple database tables and account types.