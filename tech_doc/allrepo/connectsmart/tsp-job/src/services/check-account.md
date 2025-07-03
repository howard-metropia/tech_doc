# Check Account Service

## Overview

The Check Account service provides comprehensive account balance validation and reconciliation functionality, comparing wallet balances against transaction histories to identify discrepancies and ensure financial data integrity.

## Service Information

- **Service Name**: Check Account
- **File Path**: `/src/services/check-account.js`
- **Type**: Financial Validation Service
- **Dependencies**: Moment.js, User Models

## Core Functions

### process(period, stage)

Main account validation function that compares wallet balances with transaction histories.

**Purpose**: Identifies account balance discrepancies for financial auditing
**Parameters**:
- `period` (array): Date range for validation [start, end]
- `stage` (string): Environment ('production', 'sandbox', 'develop')

**Returns**: Array of accounts with balance discrepancies

### getBalanceByUserId(userId, period)

Retrieves transaction history for specific user within date range.

**Purpose**: Fetches user's transaction records for balance calculation
**Parameters**:
- `userId` (number): User identifier
- `period` (array): Date range for transaction lookup

**Returns**: Array of transactions with points and balance data

### getAllBalanceGroupByUserId(period, stage)

Groups all transactions by user ID within specified period and environment.

**Purpose**: Aggregates transaction data for batch processing
**Parameters**:
- `period` (array): Date range for transaction queries
- `stage` (string): Environment filter for user ID ranges

**Returns**: Object with user IDs as keys and transaction arrays as values

## Balance Validation Logic

### Comparison Process
1. **Current Wallet Balance**: From user_wallet table
2. **Final Transaction Balance**: Latest transaction balance
3. **Point Sum Calculation**: Sum of transaction points (excluding first)
4. **Race Condition Handling**: Checks for transactions after job execution

### Discrepancy Detection
```javascript
if (
  walletBalance !== finalTransactionBalance ||
  walletBalance < 0 ||
  finalTransactionBalance < 0 ||
  calculateSum(initialTransactionBalance, pointSum) !== walletBalance
) {
  // Mark as discrepancy
}
```

### Race Condition Management
```javascript
if (wallet && moment.utc(wallet.updatedAt).isAfter(moment.utc(period[1]))) {
  // Query latest transactions to handle race conditions
  data = await getBalanceByUserId(userId, [period[0], wallet.updatedAt]);
}
```

## Environment Filtering

### User ID Ranges
- **Production/Sandbox**: user_id >= 20000 (excludes reserved accounts)
- **Development**: user_id >= 10000 (includes more test accounts)
- **Reserved Accounts**: Below thresholds excluded per MET-14798

### Stage Configuration
```javascript
if (stage === 'production' || stage === 'sandbox') {
  queryBuilder.where('user_id', '>=', 20000);
} else if (stage === 'develop') {
  queryBuilder.where('user_id', '>=', 10000);
}
```

## Mathematical Operations

### calculateSum(num1, num2)

Precise decimal addition with rounding to prevent floating-point errors.

**Purpose**: Accurate financial calculations
**Parameters**:
- `num1` (number|string): First number
- `num2` (number|string): Second number

**Returns**: Rounded sum to 2 decimal places

**Implementation**:
```javascript
const sum = parseFloat(num1) + parseFloat(num2);
const roundedSum = sum.toFixed(2);
return parseFloat(roundedSum);
```

## Utility Functions

### getPeriod(inputDateTime)

Generates 24-hour period ending at specified time.

**Purpose**: Creates standardized validation periods
**Parameters**:
- `inputDateTime` (string|null): Target end time (defaults to current UTC)

**Returns**: Array with [start, end] moment objects

### formatSubject(project, stage)

Creates standardized alert subject lines for different environments.

**Purpose**: Consistent notification formatting
**Parameters**:
- `project` (string): Project identifier ('hcs', 'goezy', 'smart')
- `stage` (string): Environment ('production', 'sandbox', 'develop')

**Returns**: Formatted subject string

**Examples**:
- `[HCS][PD] Daily Account Alert`
- `[ST][DEV] Daily Account Alert`

## Data Processing

### Transaction Aggregation
- **Descending Order**: Latest transactions first for accurate balance tracking
- **Point Calculation**: Excludes earliest transaction to avoid double-counting
- **Balance Verification**: Compares multiple balance sources

### Memory Efficiency
- **Batch Processing**: Groups transactions by user for efficient processing
- **Selective Querying**: Only processes users with transactions in period
- **Result Filtering**: Returns only accounts with discrepancies

## Error Detection Categories

### Balance Mismatches
- **Wallet vs Transaction**: Different balances between systems
- **Negative Balances**: Invalid negative wallet or transaction balances
- **Calculation Errors**: Point sum doesn't match expected balance

### Anomaly Patterns
- **Missing Transactions**: Gaps in transaction history
- **Duplicate Entries**: Repeated transaction processing
- **Timing Issues**: Race conditions between wallet updates and transaction logs

## Integration Points

### Used By
- Daily account reconciliation jobs
- Financial audit systems
- Balance verification workflows
- Alert notification systems

### External Dependencies
- **PointsTransaction Model**: Transaction history data
- **UserWallet Model**: Current balance information
- **Moment.js**: Date manipulation and comparison

## Performance Considerations

### Query Optimization
- **Indexed Lookups**: Efficient user_id and date range queries
- **Batch Processing**: Groups operations for database efficiency
- **Memory Management**: Processes data in manageable chunks

### Scalability
- **User Filtering**: Environment-based user range limits
- **Date Boundaries**: Configurable validation periods
- **Result Limitation**: Only returns problematic accounts

## Security Considerations

### Data Privacy
- **User ID Exposure**: Returns actual user IDs for investigation
- **Balance Information**: Contains sensitive financial data
- **Access Control**: Should be restricted to financial administrators

### Audit Trail
- **Validation History**: Tracks when checks were performed
- **Discrepancy Records**: Maintains history of identified issues
- **Resolution Tracking**: Supports investigation workflows

## Usage Guidelines

1. **Daily Execution**: Run as part of regular financial reconciliation
2. **Environment Awareness**: Use appropriate stage settings
3. **Period Selection**: Use 24-hour periods for consistent validation
4. **Alert Integration**: Connect with notification systems for immediate alerts
5. **Investigation Process**: Follow up on all identified discrepancies

## Dependencies

- **Moment.js**: Date manipulation and timezone handling
- **PointsTransaction Model**: Database ORM for transaction queries
- **UserWallet Model**: Database ORM for wallet balance queries
- **@maas/core/log**: Centralized logging for validation results