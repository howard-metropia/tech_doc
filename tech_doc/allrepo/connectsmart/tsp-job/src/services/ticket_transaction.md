# Ticket Transaction Service

## Overview

The Ticket Transaction service manages synchronization of Bytemark transit ticket purchase data from portal to analytics databases, handling comprehensive transaction tracking with user anonymization and test account filtering.

## Service Information

- **Service Name**: Ticket Transaction
- **File Path**: `/src/services/ticket_transaction.js`
- **Type**: Transaction Data Synchronization Service
- **Dependencies**: Moment.js, InfluxDB, MySQL, MongoDB

## Core Functions

### writeTicketTransaction(start, end)

Synchronizes Bytemark ticket transaction data to analytics database.

**Purpose**: Transfers ticket purchase data for analytics and reporting
**Parameters**:
- `start` (string): Start date filter (optional)
- `end` (string): End date filter (optional)

**Process Flow**:
1. **Date Range Calculation**: Determines synchronization period
2. **Data Extraction**: Complex joins across multiple Bytemark tables
3. **Test Account Filtering**: Excludes identified testing accounts
4. **User Anonymization**: Applies hash ID transformation
5. **Timezone Conversion**: UTC to US/Central conversion
6. **Batch Processing**: 1000 records per batch for efficiency

### recheckActiveTime()

Updates missing active time data from Bytemark pass records.

**Purpose**: Backfills missing activation timestamps for ticket usage
**Process**:
1. Finds ticket transactions with active_time = 0
2. Looks up corresponding pass usage times
3. Updates records with converted timestamps
4. Logs completion statistics

## Data Sources

### Database Joins
```sql
FROM bytemark_order_payments order
JOIN bytemark_order_items items ON items.order_uuid = order.order_uuid  
LEFT JOIN bytemark_pass pass ON pass.pass_uuid = items.pass_uuid
LEFT JOIN bytemark_tokens token ON token.user_id = order.user_id
```

### Field Mapping
- **order.payment_type** → payment_type
- **order.total_price** → total_price  
- **order.user_id** → user_id (hashed)
- **order.created_on** → order_time (converted to Central)
- **items.id** → ticket_item_id
- **pass.time_used** → active_time (converted to Central)
- **token.token** → user_uuid

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

## Date Processing

### Date Range Logic
- **Default Start**: 2021-01-01 for empty databases
- **Incremental**: Uses last update timestamp minus 2 days
- **Delay Handling**: 2-day buffer for delayed data creation
- **Timezone**: All processing in UTC, converted for storage

### Time Conversion
```javascript
// UTC to US/Central conversion
row.order_time = moment
  .utc(row.order_time)
  .tz('US/Central')
  .format('YYYY-MM-DD HH:mm:ss');
```

## Data Validation

### Duplicate Prevention
- **Existing Check**: Queries existing ticket_item_id values
- **Batch Exclusion**: Filters out already processed records
- **Atomic Processing**: Prevents partial duplicate insertion

### Data Quality
- **Active Time Validation**: Handles missing activation timestamps
- **User Validation**: Ensures valid user associations
- **Price Validation**: Confirms transaction amounts

## Performance Optimization

### Batch Processing
- **Batch Size**: 1000 records per iteration
- **Memory Efficiency**: Processes data in manageable chunks
- **Offset Pagination**: Efficient large dataset handling

### Database Efficiency
- **Indexed Queries**: Optimized joins on primary keys
- **Selective Fields**: Minimizes data transfer
- **Batch Inserts**: Efficient bulk data operations

## Error Handling

### Processing Errors
- **Database Failures**: Comprehensive error logging
- **Data Validation**: Handles missing or invalid data
- **Transaction Safety**: Maintains data consistency

### Recovery Mechanisms
- **Reprocessing**: Can restart from any date range
- **Incremental Updates**: Supports partial reprocessing
- **Data Verification**: Active time backfill process

## Integration Points

### Used By
- Transit usage analytics
- Revenue reporting systems
- User behavior analysis
- Bytemark service monitoring

### External Dependencies
- **Bytemark Tables**: Multiple portal database tables
- **InfluxDB**: Performance monitoring
- **Analytics Database**: Target data storage

## Security Features

### User Privacy
- **Hash ID**: User identifier anonymization
- **Data Minimization**: Only necessary fields transferred
- **Test Account Filtering**: Excludes development data

### Data Integrity
- **Duplicate Prevention**: Ensures data uniqueness
- **Transaction Consistency**: Atomic operations
- **Audit Trail**: Complete processing logs

## Monitoring

### InfluxDB Metrics
```javascript
const influxData = {
  measurement: 'scheduling-job',
  tags: { job: 'analytic-database' },
  fields: { successfully, sub_job: 'writeTicketTransaction' },
};
```

### Success Tracking
- **Record Count**: Number of processed transactions
- **Processing Time**: Job execution duration
- **Error Rate**: Failed operation tracking

## Usage Guidelines

1. **Incremental Processing**: Use for daily synchronization
2. **Full Refresh**: Specify date ranges for complete rebuilds
3. **Test Data**: Regularly update testing user ID list
4. **Performance**: Monitor batch sizes for optimal processing
5. **Data Quality**: Run active time checks after major updates

## Dependencies

- **Moment.js**: Date manipulation and timezone conversion
- **InfluxDB Helper**: Performance metrics tracking
- **Hash Helper**: User ID anonymization
- **Multiple Models**: Portal and analytics database models
- **Portal/Dataset Databases**: Source and target connections