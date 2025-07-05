# Coin Transaction Service

## Overview

The Coin Transaction service synchronizes points/coins transaction data from portal to analytics databases, handling comprehensive financial transaction tracking with market segmentation and user anonymization.

## Service Information

- **Service Name**: Coin Transaction
- **File Path**: `/src/services/coin_transaction.js`
- **Type**: Financial Transaction Synchronization Service
- **Dependencies**: Moment.js, InfluxDB, MySQL

## Core Functions

### writeCoinTransaction(start, end)

Synchronizes points transaction data to analytics database with market filtering.

**Purpose**: Transfers coin/points transaction data for financial analytics
**Parameters**:
- `start` (string): Start date filter (optional)
- `end` (string): End date filter (optional)

**Process Flow**:
1. **Date Range Calculation**: Determines synchronization period with latest record fallback
2. **Market User Integration**: Joins with market segmentation data
3. **MTC Signup Detection**: Identifies MTC program participants
4. **Test Account Filtering**: Excludes identified testing accounts
5. **User Anonymization**: Applies hash ID transformation
6. **Batch Processing**: 1000 records per batch for memory efficiency

## Data Sources

### Database Joins
```sql
FROM points_transaction coin
JOIN hybrid.market_user mkt ON coin.user_id = mkt.user_id
WHERE mkt.user_in_market != 'MET_TEST'
```

### Field Mapping
- **coin.id** → transaction_id
- **coin.user_id** → user_id (hashed)
- **coin.activity_type** → activity_type
- **coin.points** → coin
- **coin.balance** → balance
- **coin.note** → transaction
- **coin.created_on** → created_on
- **mkt.user_in_market** → market (with MTC override)

## Market Segmentation

### Market Categories
- **MET_TEST**: Excluded from synchronization
- **MTC_signup**: Special handling for MTC participants
- **Other Markets**: Various regional/program classifications

### MTC Integration
```javascript
// MTC signup user detection
const mtcSignupUsers = await portalKnex
  .select('user_id')
  .from('mtc_user_signup');

// Override market classification
if (mtcSignupUserIds.includes(row.user_id)) {
  row.market = 'MTC_signup';
}
```

## Test Account Management

### Testing User IDs
```javascript
const TESTING_USER_IDS = [
  10313, 10794, 11430, 10376, 10288, 10614, 10615, 10302,
  10401, 11429, 1015, 11333, 11081, 10624, 10301, 10649,
  10829, 11058, 11227, 10797, 11184, 11058, 11231
];
```

### Test Account Detection
- **Hardcoded List**: Known testing account identification
- **Future Enhancement**: Internal user tag integration planned
- **Flag Setting**: test_account field for analytics filtering

## Date Range Processing

### Date Logic
- **Default Start**: 2021-01-01 for empty databases
- **Incremental**: Uses last update timestamp for continuous sync
- **UTC Processing**: All dates processed in UTC format
- **No Buffer**: Unlike ticket transactions, no delay buffer needed

### Date Conversion
```javascript
if (start !== 'null' && moment(start).isValid()) {
  startDate = moment.utc(start).format('YYYY-MM-DDT00:00:00');
} else {
  const latestLog = await CoinTransaction.query()
    .orderBy('update', 'desc')
    .limit(1)
    .first();
  startDate = latestLog
    ? moment.utc(latestLog.update).format('YYYY-MM-DDT00:00:00')
    : '2021-01-01T00:00:00';
}
```

## Data Validation

### Duplicate Prevention
- **Transaction ID Check**: Prevents re-insertion of existing records
- **Batch Filtering**: Excludes already processed transactions
- **Atomic Operations**: Ensures data consistency

### Market Filtering
- **Test Exclusion**: Filters out MET_TEST market users
- **Market Validation**: Ensures valid market classifications
- **MTC Override**: Special handling for MTC program users

## Performance Optimization

### Batch Processing
- **Batch Size**: 1000 records per iteration
- **Memory Management**: Efficient large dataset handling
- **Offset Pagination**: Scalable data processing

### Database Efficiency
- **Cross-Database Joins**: Optimized portal-hybrid joins
- **Indexed Queries**: Fast lookups on user_id and transaction_id
- **Selective Processing**: Only processes new records

## Activity Types

### Transaction Categories
Points transactions include various activity types:
- **Purchases**: Coin purchases and payments
- **Incentives**: Earned rewards and bonuses
- **Transfers**: Escrow and inter-user transfers
- **Adjustments**: Manual balance corrections
- **Fees**: Transaction and service fees

### Financial Tracking
- **Balance Tracking**: Maintains running balance
- **Transaction History**: Complete audit trail
- **Activity Classification**: Categorized for analytics

## Error Handling

### Processing Errors
- **Database Connection**: Handles cross-database join failures
- **Data Validation**: Manages missing or invalid data
- **Transaction Safety**: Maintains referential integrity

### Recovery Mechanisms
- **Incremental Sync**: Supports restart from any point
- **Date Range Flexibility**: Custom range processing
- **Error Logging**: Comprehensive failure tracking

## Integration Points

### Used By
- Financial analytics and reporting
- User spending behavior analysis
- Revenue tracking systems
- Market performance analysis

### External Dependencies
- **Points Transaction Table**: Source financial data
- **Market User Table**: User segmentation data
- **MTC Signup Table**: Program participation tracking
- **InfluxDB**: Performance monitoring

## Security Features

### User Privacy
- **Hash ID**: User identifier anonymization
- **Financial Data**: Secure transaction handling
- **Test Data Exclusion**: Prevents test data pollution

### Data Integrity
- **Duplicate Prevention**: Ensures transaction uniqueness
- **Cross-Reference Validation**: Maintains data relationships
- **Audit Trail**: Complete processing history

## Monitoring

### InfluxDB Metrics
```javascript
const influxData = {
  measurement: 'scheduling-job',
  tags: { job: 'analytic-database' },
  fields: { successfully, sub_job: 'writeCoinTransaction' },
};
```

### Performance Tracking
- **Processing Count**: Number of synchronized transactions
- **Execution Time**: Job completion duration
- **Success Rate**: Transaction processing efficiency

## Usage Guidelines

1. **Regular Sync**: Run daily for current transaction data
2. **Market Monitoring**: Verify market classifications
3. **Test Data**: Maintain current testing user lists
4. **Performance**: Monitor batch processing efficiency
5. **Data Quality**: Validate cross-database relationships

## Dependencies

- **Moment.js**: Date manipulation and formatting
- **InfluxDB Helper**: Performance metrics tracking
- **Hash Helper**: User ID anonymization
- **Portal/Hybrid Databases**: Cross-database data sources
- **Analytics Database**: Target data storage