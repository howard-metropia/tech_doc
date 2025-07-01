# test-pointstransaction.js Technical Documentation

## Purpose

Comprehensive unit test suite for the points transaction system, testing various transaction types, auto-refill functionality, user blocking, and wallet management across different activity scenarios.

## Core Functionality

### Points Transaction System

#### Service: `pointsTransaction`
- **Purpose**: Process all types of point transactions in the system
- **Parameters**: User ID, activity type, amount, note, verification flag, payer, payee, reference accounts
- **Returns**: New balance and transaction ID
- **Integration**: Wallet management, auto-refill, blocking system

#### Supported Activity Types
1. **Type 2**: Credit/purchase transactions
2. **Type 3**: Debit/spending transactions  
3. **Type 4**: Reward/incentive transactions
4. **Type 5**: Refund transactions
5. **Type 6**: Bonus/promotional transactions
6. **Type 7**: Administrative adjustments
7. **Type 8**: Service fees (with reference account)
8. **Type 9**: Penalty/fine transactions
9. **Type 10**: Transfer transactions
10. **Type 11**: Withdrawal transactions
11. **Type 18**: Complex multi-party transactions

## Test Architecture

### Service Imports
```javascript
const {
  pointsTransaction,
  getUserWallet,
  writePointsTransaction,
  updatePointsTransaction,
  targetTable,
} = require('@app/src/services/wallet');
```

### Table Determination
- **Production**: `points_transaction`
- **Upgrade**: `points_transaction_upgrade`
- **Dynamic**: Determined by `targetTable` variable

### Test Structure
```javascript
describe('test pointsTransaction interface', () => {
  before(async () => {
    let userId = (await knex('user_wallet').select())[0].user_id;
    await knex('user_wallet').where({ user_id: userId }).update({ auto_refill: 'F' });
  });
});
```

## Transaction Type Testing

### Activity Type 2 (Credit/Purchase)
```javascript
describe('test activity_type=2', () => {
  it('successful case', async () => {
    let userId = (await knex('user_wallet').select())[0].user_id;
    let uw1 = await getUserWallet(userId);
    let amount = 5;
    
    const { balance, _id } = await pointsTransaction(
      userId,
      2,        // Activity type
      amount,   // Positive amount
      '',       // Note
      false,    // Verification flag
    );
    
    let pts1 = await knex(targetTable).where({ id: _id }).select();
    expect(pts1.length).to.be.above(0);
    
    let uw2 = await getUserWallet(userId);
    expect(parseFloat(uw2.balance) - parseFloat(uw1.balance)).to.be.equal(amount);
  });
});
```

### Activity Type 3 (Debit/Spending)
```javascript
describe('test activity_type=3', () => {
  it('successful case', async () => {
    let amount = -5;  // Negative amount for debit
    
    const { balance, _id } = await pointsTransaction(
      userId,
      3,
      amount,
      '',
      false,
    );
    
    // Verify balance decrease
    let uw2 = await getUserWallet(userId);
    expect(parseFloat(uw2.balance) - parseFloat(uw1.balance)).to.be.equal(amount);
  });
});
```

### Activity Type 8 (Service Fees with Reference)
```javascript
describe('test activity_type=8', () => {
  it('successful case', async () => {
    let amount = -2;
    
    const { balance, _id } = await pointsTransaction(
      userId,
      8,
      amount,
      '',
      false,
      null,     // Payer
      null,     // Payee  
      2000,     // Reference account
    );
    
    // Verify transaction recorded with reference
    let pts1 = await knex(targetTable).where({ id: _id }).select();
    expect(pts1.length).to.be.above(0);
  });
});
```

### Activity Type 18 (Multi-Party Transactions)
```javascript
describe('test activity_type=18', () => {
  it('successful case', async () => {
    const userId = 2002;  // System account
    let amount = -5;
    
    const { balance, _id } = await pointsTransaction(
      userId,
      11,       // Activity type
      amount,
      '',
      false,
      null,
      2002,     // Payer account
      2107      // Payee account
    );
    
    // Verify system account transaction
    expect(parseFloat(uw2.balance) - parseFloat(uw1.balance)).to.be.equal(amount);
  });
});
```

## Auto-Refill System Testing

### Blocked User Auto-Refill Prevention
```javascript
describe('Blocked user test', async () => {
  before(async () => {
    // Add initial balance
    await pointsTransaction(userId, 6, 1.25, 'compensation', false);
    
    // Block the user
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

### Auto-Refill with Daily Limit Exceeded
```javascript
describe('with auto-refill enabled and exceed daily limit', async () => {
  before(async () => {
    // Setup user with auto-refill
    await knex('user_wallet')
      .where({ id: uw.id })
      .update({
        auto_refill: 'T',
        refill_plan_id: plan.id,
        below_balance: 9,
        balance: newBalance,
      });
    
    // Create prior purchase to trigger daily limit
    await knex(purchaseTable).insert({
      user_id: userId,
      points: 199,      // High amount to trigger limit
      amount: 199,
      currency: 'USD',
    });
  });

  it('test first time exceed', async () => {
    try {
      await pointsTransaction(userId, 11, -1.75, '', false);
    } catch(e) {
      expect(e.code).to.eq(ERROR_CODE.ERROR_COIN_PURCHASE_DAILY_LIMIT);
      
      // Verify balance still updated despite auto-refill failure
      const newUw = await getUserWallet(userId);
      expect(Number(newUw.balance)).to.be.eq(newBalance - 1.75);
      expect(newUw.auto_refill).to.be.eq(false);  // Auto-refill disabled
    }
  });
});
```

### Auto-Refill Without Customer ID
```javascript
describe('user without stripe_customer_id but auto-refill enabled', async () => {
  before(async () => {
    await knex('user_wallet')
      .where({ user_id: userId })
      .update({ 
        stripe_customer_id: null, 
        auto_refill: 'T' 
      });
  });

  it('test auto refill without customerId', async () => {
    const uw = await knex('user_wallet').where({ user_id: userId }).first();
    consume = Number(uw.below_balance) - Number(uw.balance) - 1;
    
    const { balance, _id } = await pointsTransaction(
      userId, 
      11, 
      consume, 
      'unit-test-uuid', 
      false
    );
    
    expect(_id).to.above(0);
    const exp = Math.round((Number(uw.balance) + Number(consume)) * 100) / 100;
    expect(Number(balance)).to.eq(exp);
  });
});
```

## New User Wallet Creation

### First Transaction Creates Wallet
```javascript
describe('test call pointsTransaction with new user without user_wallet', () => {
  const userId = 9999999;
  
  before(async () => {
    await knex('user_wallet').where({ user_id: userId }).delete();
  });

  it('it should create user_wallet and points_transaction', async () => {
    const { balance, _id } = await pointsTransaction(
      userId, 
      6,      // Incentive type
      5,      // Amount
      'referral coin', 
      false
    );
    
    expect(_id).to.above(0);
    expect(Number(balance)).to.eq(5);
    
    // Verify wallet created
    const uw = await knex('user_wallet').where({ user_id: userId }).first();
    expect(uw).to.not.be.null;
    expect(Number(uw.balance)).to.eq(5);
  });
});
```

## Error Handling

### User Blocking Errors
```javascript
const cmp = new MaasError(
  ERROR_CODE.ERROR_USER_COIN_SUSPENDED,
  'warn',
  'ERROR_USER_COIN_SUSPENDED',
  403,
);
```

### Daily Limit Errors
```javascript
const cmp = new MaasError(
  ERROR_CODE.ERROR_COIN_PURCHASE_DAILY_LIMIT,
  'warn',
  'ERROR_COIN_PURCHASE_DAILY_LIMIT',
  403,
);
```

## Database Schema

### points_transaction / points_transaction_upgrade
```javascript
const transactionStructure = {
  id: 'integer',
  user_id: 'integer',
  activity_type: 'integer',
  points: 'decimal',
  note: 'string',
  payer: 'integer',
  payee: 'integer',
  ref_transaction_id: 'integer',
  created_on: 'timestamp'
};
```

### user_wallet
```javascript
const walletStructure = {
  id: 'integer',
  user_id: 'integer',
  balance: 'decimal',
  auto_refill: 'boolean',
  below_balance: 'decimal',
  refill_plan_id: 'integer',
  stripe_customer_id: 'string'
};
```

### purchase_transaction / purchase_transaction_upgrade
```javascript
const purchaseStructure = {
  id: 'integer',
  user_id: 'integer',
  point_transaction_id: 'integer',
  points: 'decimal',
  amount: 'decimal',
  currency: 'string',
  transaction_id: 'string',
  created_on: 'timestamp'
};
```

## Business Rules

### Auto-Refill Logic
1. **Trigger**: Balance falls below `below_balance` threshold
2. **Validation**: Check for valid Stripe customer ID
3. **Daily Limits**: Respect daily purchase limits
4. **Failure Handling**: Disable auto-refill on limit exceeded

### Blocking System
- **Automatic**: System blocks users exceeding limits
- **Manual**: Administrators can block users
- **Transaction Prevention**: Blocked users cannot make transactions

### Balance Management
- **Precision**: Handle decimal precision correctly
- **Atomic Operations**: Ensure transaction atomicity
- **Consistency**: Maintain balance consistency across operations

## Performance Considerations

### Database Optimization
- **Table Selection**: Use appropriate transaction table
- **Indexed Queries**: Optimize frequent lookups
- **Transaction Batching**: Group related operations

### Memory Management
- **Large Datasets**: Handle high-volume transactions
- **Connection Pooling**: Efficient database connections
- **Cleanup Strategy**: Regular old data cleanup

## Usage Examples

### Basic Transaction
```javascript
const { balance, _id } = await pointsTransaction(
  userId,           // User ID
  6,               // Activity type (incentive)
  10.50,           // Amount
  'Daily bonus',   // Note
  false            // Verification flag
);

console.log(`New balance: ${balance}, Transaction ID: ${_id}`);
```

### Multi-Party Transaction
```javascript
const { balance, _id } = await pointsTransaction(
  systemUserId,    // System account
  18,              // Multi-party transaction
  -5.00,           // Amount
  'Service fee',   // Note
  false,           // Verification
  null,            // Default payer
  systemUserId,    // Payer account
  serviceAccount   // Payee account
);
```

### Error Handling
```javascript
try {
  await pointsTransaction(userId, 11, -10, 'Purchase', false);
} catch (error) {
  if (error.code === ERROR_CODE.ERROR_USER_COIN_SUSPENDED) {
    console.log('User account suspended');
  } else if (error.code === ERROR_CODE.ERROR_COIN_PURCHASE_DAILY_LIMIT) {
    console.log('Daily purchase limit exceeded');
  }
}
```

This test suite ensures robust points transaction functionality, covering all transaction types, auto-refill scenarios, user blocking, and edge cases while maintaining data consistency and business rule compliance.