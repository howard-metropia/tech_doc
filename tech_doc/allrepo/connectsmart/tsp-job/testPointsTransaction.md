# Points Transaction Service Test Suite

## Overview
Comprehensive test suite for the wallet points transaction system that validates all activity types, auto-refill functionality, transaction integrity, user wallet management, and daily spending limits. This extensive test covers the complete financial transaction lifecycle within the MaaS platform's point-based economy.

## File Location
`/test/testPointsTransaction.js`

## Technical Analysis

### Core Service Under Test
```javascript
const {
  pointsTransaction,
  getUserWallet,
  writePointsTransaction,
  updatePointsTransaction,
  targetTable,
} = require('@app/src/services/wallet');
```

The wallet service manages all point-based transactions, including rewards, deductions, refills, and complex financial operations with multiple activity types.

### Dependencies
- `@maas/core/mysql` - MySQL database connection for portal operations
- `chai` - Assertion library with expect interface for validation
- `@maas/core` - Core MaaS error handling and utilities
- `@app/src/static/error-code` - Application-specific error code definitions

### Transaction Activity Types

The test validates 11 different activity types representing various transaction scenarios:

#### Activity Type Categories
- **Type 2**: Credit/reward transactions (positive amounts)
- **Type 3**: Debit/consumption transactions (negative amounts)  
- **Type 4**: Bonus/incentive transactions (positive amounts)
- **Type 5**: Promotional credits (positive amounts)
- **Type 6**: Compensation/adjustment transactions (positive amounts)
- **Type 7**: Referral rewards (positive amounts)
- **Type 8**: Service charges with specific parameters (negative amounts)
- **Type 9**: General deductions (negative amounts)
- **Type 10**: Special credits (positive amounts)
- **Type 11**: Premium service charges (negative amounts)
- **Type 18**: Partner transaction with additional parameters

### Test Architecture Pattern

#### Standard Transaction Test Structure
```javascript
describe('test activity_type=X', () => {
  it('successful case', async () => {
    let userId = (await knex('user_wallet').select())[0].user_id;
    let uw1 = await getUserWallet(userId);
    let amount = X; // positive or negative based on activity type
    
    const { balance, _id } = await pointsTransaction(
      userId,
      activityType,
      amount,
      '',
      false,
    );
    
    let pts1 = await knex(targetTable).where({ id: _id }).select();
    expect(pts1.length).to.be.above(0);
    
    let uw2 = await getUserWallet(userId);
    expect(parseFloat(uw2.balance) - parseFloat(uw1.balance)).to.be.equal(amount);
  });
});
```

### Auto-Refill Testing Framework

#### Blocked User Scenario
```javascript
describe('Blocked user test', async () => {
  before(async () => {
    await knex('block_users').insert({
      user_id: userId,
      is_deleted: 'F',
    });
  });
  
  it('expect to throw exception', async () => {
    try {
      await pointsTransaction(userId, 11, -1.25, '', false);
    } catch(e) {
      const cmp = new MaasError(
        ERROR_CODE.ERROR_USER_COIN_SUSPENDED,
        'warn',
        'ERROR_USER_COIN_SUSPENDED',
        403,
      );
      expect(e.message).to.eq(cmp.message);
      expect(e.code).to.eq(ERROR_CODE.ERROR_USER_COIN_SUSPENDED);
    }
  });
});
```

#### Daily Limit Enforcement
```javascript
describe('with auto-refill enabled and exceed daily limit', async () => {
  it('test first time exceed', async () => {
    try {
      await pointsTransaction(userId, 11, -1.75, '', false);
    } catch(e) {
      const cmp = new MaasError(
        ERROR_CODE.ERROR_COIN_PURCHASE_DAILY_LIMIT,
        'warn',
        'ERROR_COIN_PURCHASE_DAILY_LIMIT',
        403,
      );
      expect(e.message).to.eq(cmp.message);
      expect(e.code).to.eq(ERROR_CODE.ERROR_COIN_PURCHASE_DAILY_LIMIT);
      
      const newUw = await getUserWallet(userId);
      expect(Number(newUw.balance)).to.be.eq(newBalance - 1.75);
      expect(newUw.auto_refill).to.be.eq(false);
    }
  });
});
```

## Usage/Integration

### Transaction Flow Validation

#### Successful Transaction Pattern
1. **Pre-transaction State**: Capture initial wallet balance
2. **Transaction Execution**: Perform points transaction with specified parameters
3. **Database Verification**: Confirm transaction record creation
4. **Balance Validation**: Verify correct balance adjustment
5. **State Consistency**: Ensure wallet state matches transaction history

#### Transaction Parameters
```javascript
const { balance, _id } = await pointsTransaction(
  userId,        // Target user identifier
  activityType,  // Transaction type (2-11, 18)
  amount,        // Transaction amount (positive/negative)
  description,   // Transaction description/reference
  skipValidation // Skip additional validation checks
);
```

### Auto-Refill Functionality

#### Refill Configuration
```javascript
const plan = await knex('refill_plan').where({ points: 10 }).first();
await knex('user_wallet').update({
  auto_refill: 'T',
  refill_plan_id: plan.id,
  below_balance: 9,
  balance: newBalance,
});
```

#### Refill Trigger Conditions
- **Balance Threshold**: Automatic refill when balance falls below configured amount
- **Daily Limits**: Enforcement of maximum daily spending/refill amounts
- **Payment Method**: Integration with Stripe customer payment methods
- **Error Handling**: Graceful degradation when payment methods unavailable

## Code Examples

### Basic Transaction Execution
```javascript
// Credit transaction (Activity Type 2)
const { balance, _id } = await pointsTransaction(
  1003,     // userId
  2,        // activityType
  5.00,     // amount (positive for credit)
  'Daily reward',
  false     // skipValidation
);

console.log(`Transaction ID: ${_id}, New Balance: ${balance}`);
```

### Transaction with Extended Parameters
```javascript
// Service charge with additional parameters (Activity Type 8)
const { balance, _id } = await pointsTransaction(
  userId,
  8,           // activityType
  -2.00,       // amount (negative for charge)
  'Service fee',
  false,       // skipValidation
  null,        // additional param 1
  null,        // additional param 2
  2000         // service identifier
);
```

### New User Wallet Creation
```javascript
describe('test call pointsTransaction with new user without user_wallet', () => {
  it('it should create user_wallet and points_transaction', async () => {
    const { balance, _id } = await pointsTransaction(
      9999999,    // Non-existent user
      6,          // Incentive activity type
      5,          // Credit amount
      'referral coin',
      false
    );
    
    expect(_id).to.above(0);
    expect(Number(balance)).to.eq(5);
    
    // Verify wallet creation
    const uw = await knex('user_wallet').where({ user_id: 9999999 }).first();
    expect(uw).to.not.be.null;
    expect(Number(uw.balance)).to.eq(5);
  });
});
```

### Error Handling Patterns
```javascript
// Blocked user validation
try {
  await pointsTransaction(blockedUserId, 11, -1.25, '', false);
} catch (error) {
  expect(error.code).to.eq(ERROR_CODE.ERROR_USER_COIN_SUSPENDED);
}

// Daily limit enforcement
try {
  await pointsTransaction(userId, 11, -largeAmount, '', false);
} catch (error) {
  expect(error.code).to.eq(ERROR_CODE.ERROR_COIN_PURCHASE_DAILY_LIMIT);
}
```

## Integration Points

### Database Integration
- **User Wallet Management**: Primary wallet balance and configuration
- **Transaction History**: Complete audit trail of all point movements
- **Purchase Tracking**: Daily spending limits and refill history
- **Refill Plans**: Configurable auto-refill packages and pricing

### Payment System Integration
- **Stripe Integration**: Automated payment processing for refills
- **Daily Limit Enforcement**: Spending control and fraud prevention
- **Auto-Refill Logic**: Intelligent balance maintenance
- **Payment Method Validation**: Customer payment status verification

### Business Logic Validation
- **Activity Type Processing**: Different transaction types with specific rules
- **Balance Calculations**: Precise financial arithmetic with rounding
- **User Status Checking**: Blocked user and account status validation
- **Audit Trail**: Complete transaction history and accountability

### Error Handling Framework
- **User Suspension**: Blocked user transaction prevention
- **Daily Limits**: Spending limit enforcement with graceful degradation
- **Payment Failures**: Auto-refill error handling and user notification
- **Data Integrity**: Transaction rollback on validation failures

This comprehensive test suite ensures the points transaction system maintains financial integrity, implements proper business rules, handles edge cases gracefully, and provides reliable wallet management functionality across all supported activity types and user scenarios.