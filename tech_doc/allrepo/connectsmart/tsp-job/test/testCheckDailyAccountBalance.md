# Daily Account Balance Verification Test Suite

## Overview
Comprehensive test suite for the daily account balance verification service that validates the integrity of user point transactions by comparing calculated balances against stored wallet balances, detecting discrepancies that could indicate data corruption or transaction processing errors.

## File Location
`/test/testCheckDailyAccountBalance.js`

## Dependencies
- `chai` - Assertion library with expect interface
- `moment` - Date and time manipulation library
- `@maas/core/bootstrap` - Application initialization
- `@app/src/models/PointsTransaction` - Points transaction model
- `@app/src/models/UserWallet` - User wallet balance model

## Test Architecture

### Service Functions Under Test
```javascript
const {
  process,
  getPeriod,
  calculateSum,
} = require('@app/src/services/check-account');
```

### Test Categories
1. **Unit Testing**: Individual function validation
2. **Integration Testing**: Database operations with mock data
3. **Edge Case Testing**: Error conditions and boundary scenarios

## Mock Data Utilities

### Wallet Record Creation
```javascript
const mockWalletRecord = async (data) => {
  await Promise.all(
    data.map(async (record) => {
      const walletRecord = {
        user_id: record.userId,
        balance: record.balance,
        modified_on: moment
          .utc(record.modified ?? '1970-01-02 00:00:00')
          .format('YYYY-MM-DD HH:mm:ss'),
      };
      await UserWallet.query().insert(walletRecord);
    }),
  );
};
```

### Transaction Record Creation
```javascript
const mockTransactionRecord = async (data) => {
  const transactionRecords = data.map((row) => {
    return {
      user_id: row.user_id,
      activity_type: 5,
      points: row.points,
      balance: row.balance,
      created_on: moment
        .utc(row.modified ?? '1970-01-01 06:00:00')
        .format('YYYY-MM-DD HH:mm:ss'),
      payer: 7788,
      payee: row.user_id,
      ref_transaction_id: 0,
    };
  });
  
  for (const record of transactionRecords) {
    await PointsTransaction.query().insert(record);
  }
};
```

## Unit Testing: Core Functions

### Period Calculation Testing
```javascript
describe('getPeriod test', function () {
  it('should return the correct period for a given date', () => {
    const dateTime = moment.utc('2023-03-10T12:30:00');
    const expectedPeriod = ['2023-03-09 12:30:00', '2023-03-10 12:30:00'];

    const result = getPeriod(dateTime);

    expect(result[0].format('YYYY-MM-DD HH:mm:ss')).deep.eq(expectedPeriod[0]);
    expect(result[1].format('YYYY-MM-DD HH:mm:ss')).deep.eq(expectedPeriod[1]);
  });
});
```

#### Period Logic
- **24-Hour Window**: Calculates previous 24-hour period
- **UTC Alignment**: Uses UTC timestamps for consistency
- **Configurable Base**: Accepts custom datetime or uses current time
- **Format**: Returns moment objects for flexible manipulation

### Sum Calculation Testing
```javascript
describe('calculateSum', () => {
  describe('numbers only', () => {
    it('should return the correct sum of two positive numbers', () => {
      const num1 = 3.5;
      const num2 = 2.75;
      const expectedSum = 6.25;
      const result = calculateSum(num1, num2);
      expect(expectedSum).to.eq(result);
    });
  });
});
```

#### Calculation Features
- **Decimal Precision**: Handles floating-point arithmetic accurately
- **String Numbers**: Converts string representations to numbers
- **Mixed Types**: Handles combinations of numbers and strings
- **Edge Cases**: Manages zero values and negative numbers

### Advanced Sum Testing Scenarios
```javascript
describe('mixed', () => {
  it('should correctly sum a number and a number string (random position swap)', () => {
    const testData = [
      [5.25, '3.75', 9],
      [10.5, '-7.25', 3.25],
      [2.75, '0', 2.75],
      [1.3333, '2.6666', 4],
      [-8.5, '4.75', -3.75],
    ];

    testData.forEach(([num1, num2, num3]) => {
      const expectedSum = num3;
      // Randomly swap positions of arguments
      const [arg1, arg2] = Math.random() < 0.5 ? [num1, num2] : [num2, num1];
      const result = calculateSum(arg1, arg2);
      expect(expectedSum).to.eq(result);
    });
  });
});
```

## Integration Testing: Database Operations

### Test User Configuration
```javascript
const userIdTest0 = 5566;   // Production filter test user (< 20000)
const userIdTest1 = 25566;  // Standard test user
const userIdTest2 = 25577;  // Multi-user test user
const userIdTest3 = 25588;  // Multi-user test user
```

### Data Cleanup Strategy
```javascript
afterEach(async () => {
  await UserWallet.query()
    .delete()
    .where('user_id', 'in', [userIdTest0, userIdTest1, userIdTest2, userIdTest3])
    .where('modified_on', '<', '1970-01-03');
    
  await PointsTransaction.query()
    .delete()
    .where('user_id', 'in', [userIdTest0, userIdTest1, userIdTest2, userIdTest3])
    .where('created_on', '<', '1970-01-03');
});
```

## Happy Path Testing

### Single User Normal Case
```javascript
it('should return empty array while given a normal record', async function () {
  await mockWalletRecord([{
    userId: userIdTest1,
    balance: 5,
  }]);

  await mockTransactionRecord([{
    user_id: userIdTest1,
    points: 5,
    balance: 5,
  }]);

  const result = await process(defaultPeriod);
  expect(result).empty;
});
```

### Multiple Transaction Case
```javascript
it('should return empty array while given normal records', async function () {
  await mockWalletRecord([{
    userId: userIdTest1,
    balance: 10,
  }]);

  await mockTransactionRecord([
    {
      user_id: userIdTest1,
      points: 5,
      balance: 5,
    },
    {
      user_id: userIdTest1,
      points: 5,
      balance: 10,
      modified: '1970-01-02 00:00:00',
    },
  ]);

  const result = await process(defaultPeriod);
  expect(result).empty;
});
```

### Production Environment Filtering
```javascript
it('should return empty array while the stage is production and the user id is smaller than 20000', async function () {
  // Mock data for internal user (ID < 20000)
  await mockWalletRecord([{
    userId: userIdTest0, // 5566 < 20000
    balance: 10,
  }]);

  await mockTransactionRecord([
    {
      user_id: userIdTest0,
      points: 5,
      balance: 5,
    },
    {
      user_id: userIdTest0,
      points: -6,
      balance: -1,
      modified: '1970-01-02 00:00:00',
    },
  ]);

  const result = await process(defaultPeriod, 'production');
  expect(result).empty; // Filtered out in production
});
```

## Race Condition Testing

### Concurrent Transaction Handling
```javascript
it('should return empty array while the race condition occurs', async function () {
  await mockWalletRecord([{
    userId: userIdTest1,
    balance: 18,
    modified: '1970-01-02 05:00:15'
  }]);

  await mockTransactionRecord([
    {
      user_id: userIdTest1,
      points: 5,
      balance: 5,
    },
    {
      user_id: userIdTest1,
      points: 6,
      balance: 11,
      modified: '1970-01-02 00:00:00',
    },
    {
      user_id: userIdTest1,
      points: 7,
      balance: 18,
      modified: '1970-01-02 05:00:15', // Same timestamp as wallet
    },
  ]);

  const result = await process(defaultPeriod);
  expect(result).empty; // Race condition handled correctly
});
```

## Error Detection Testing

### Missing Wallet Record
```javascript
it('should return the abnormal record while no wallet record exist', async function () {
  await mockTransactionRecord([{
    user_id: userIdTest1,
    points: 5,
    balance: 5,
  }]);

  const result = await process(defaultPeriod);

  const expected = [{
    pointSum: 5,
    transactionBalance: 5,
    userId: userIdTest1,
    walletBalance: NaN, // Missing wallet record
  }];
  expect(result).not.empty;
  expect(result).deep.eq(expected);
});
```

### Balance Mismatch Detection
```javascript
it('should return the abnormal record while given a wrong transaction record', async function () {
  await mockWalletRecord([{
    userId: userIdTest1,
    balance: 7,
  }]);

  await mockTransactionRecord([
    {
      user_id: userIdTest1,
      points: 5,
      balance: 5,
    },
    {
      user_id: userIdTest1,
      points: 2,
      balance: 7,
      modified: '1970-01-02 05:00:03', // Outside period
    },
  ]);

  const result = await process(defaultPeriod);

  const expected = [{
    pointSum: 5,           // Only first transaction in period
    transactionBalance: 5, // Last transaction balance in period
    userId: userIdTest1,
    walletBalance: 7,      // Current wallet balance
  }];
  expect(result).not.empty;
  expect(result).deep.eq(expected);
});
```

## Multi-User Testing

### Multiple User Validation
```javascript
it('should return the abnormal records while given multiple wrong transaction records', async function () {
  await mockWalletRecord([
    { userId: userIdTest1, balance: 10 },
    { userId: userIdTest2, balance: 10 },
  ]);

  await mockTransactionRecord([
    { user_id: userIdTest1, points: 5, balance: 5 },
    { user_id: userIdTest1, points: 3, balance: 8 },
    { user_id: userIdTest2, points: 5, balance: 5 },
    { user_id: userIdTest2, points: 4, balance: 9 },
    { user_id: userIdTest2, points: 6, balance: 15 },
  ]);
  
  const result = await process(defaultPeriod);

  const expected = [
    {
      pointSum: 8,
      transactionBalance: 8,
      userId: userIdTest1,
      walletBalance: 10,
    },
    {
      pointSum: 15,
      transactionBalance: 15,
      userId: userIdTest2,
      walletBalance: 10,
    },
  ];
  expect(result).not.empty;
  expect(result).deep.eq(expected);
});
```

## Data Validation Logic

### Balance Calculation Algorithm
1. **Transaction Sum**: Sum all point changes within period
2. **Final Balance**: Get last transaction balance in period
3. **Wallet Balance**: Current wallet balance
4. **Comparison**: Detect mismatches between calculated and stored balances

### Time Window Processing
```javascript
const defaultPeriod = ['1970-01-01 05:00:00', '1970-01-02 05:00:00'];
```
- **Period Definition**: 24-hour window for transaction analysis
- **Boundary Handling**: Inclusive start, exclusive end timestamps
- **Race Condition Logic**: Handles concurrent updates at period boundaries

## Error Response Structure

### Abnormal Record Format
```javascript
{
  pointSum: 5,           // Calculated points within period
  transactionBalance: 5, // Last transaction balance in period
  userId: 25566,         // User identifier
  walletBalance: 7       // Current wallet balance (or NaN if missing)
}
```

### Error Indicators
- **Missing Wallet**: `walletBalance: NaN`
- **Balance Mismatch**: `pointSum !== walletBalance`
- **Transaction Inconsistency**: Gaps in transaction history
- **Race Conditions**: Timing-related balance discrepancies

## Performance Considerations

### Database Efficiency
- **Batch Operations**: Uses Promise.all for parallel inserts
- **Targeted Cleanup**: Specific user and date filtering
- **Index Usage**: Relies on proper indexing for user_id and timestamps

### Memory Management
- **Mock Data Size**: Minimal test datasets for fast execution
- **Cleanup Strategy**: Immediate cleanup after each test
- **Transaction Scope**: Limited to test period boundaries

## Quality Assurance

### Test Coverage Areas
1. **Period Calculation**: Time window accuracy
2. **Sum Calculation**: Mathematical precision
3. **Data Integrity**: Transaction-wallet consistency
4. **Edge Cases**: Missing data and error conditions
5. **Environment Filtering**: Production vs development logic

### Assertion Strategies
- **Deep Equality**: Exact object matching for error records
- **Empty Arrays**: Validation of successful processing
- **Type Checking**: NaN handling for missing records
- **Timing Logic**: Race condition simulation and handling

## Business Rules

### Production Environment Filtering
- **Internal Users**: User IDs < 20000 filtered in production
- **Test Users**: User IDs >= 20000 processed in all environments
- **Data Integrity**: Maintains separation between internal and customer data

### Balance Reconciliation
- **Daily Validation**: Regular balance verification
- **Error Detection**: Immediate identification of discrepancies
- **Audit Trail**: Complete transaction history preservation
- **Correction Workflow**: Framework for balance correction procedures

## Maintenance Considerations

### Data Model Evolution
- **Schema Changes**: Transaction and wallet table modifications
- **New Fields**: Additional balance tracking requirements
- **Performance Optimization**: Query and index improvements

### Test Data Management
- **Consistent IDs**: Stable test user identifiers
- **Realistic Scenarios**: Representative transaction patterns
- **Cleanup Reliability**: Bulletproof test isolation procedures