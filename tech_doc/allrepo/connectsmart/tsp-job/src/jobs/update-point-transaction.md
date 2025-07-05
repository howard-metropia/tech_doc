# update-point-transaction.js

## Overview
Job for migrating and upgrading point transaction records from the legacy system to a new schema with enhanced agency account tracking and double-entry bookkeeping. Processes incremental updates to maintain data consistency.

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/jobs/update-point-transaction.js`
- **Module Type**: Scheduled Job
- **Export**: Job configuration with async function

## Key Dependencies
- `@maas/core/mysql` - MySQL database connection (portal)
- `@maas/core/log` - Logging utility

## Core Functions

### Main Processing Function
Processes point transaction records incrementally, converting legacy format to new double-entry system.

**Process Flow:**
1. Find last processed record in upgrade table
2. Query new records from source table
3. Calculate agency balances
4. Transform records to new format
5. Insert upgraded records

### Helper Functions

#### restoreActivityType(escrowType)
Maps escrow types to activity types for proper categorization.

**Returns:**
- `9` for escrow types: [1, 2, 3, 4, 5, 12, 13, 24]
- `10` for escrow types: [6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25]
- `0` for unknown types

#### getAgencyPayerAccount(activityType, userId)
Determines payer account based on activity type and user ID.

#### getAgencyPayeeAccount(activityType, userId)
Determines payee account based on activity type and user ID.

## Job Configuration

### Inputs
No input parameters required.

### Agency Account IDs
```javascript
const agencyBalance = [
  { agency_id: 2000, balance: 0 },
  { agency_id: 2001, balance: 0 },
  { agency_id: 2002, balance: 0 },
  { agency_id: 2100, balance: 0 },
  { agency_id: 2101, balance: 0 },
  { agency_id: 2102, balance: 0 },
  { agency_id: 2103, balance: 0 }
];
```

## Processing Flow

### 1. Incremental Processing
```sql
SELECT * FROM points_transaction_upgrade ORDER BY ori_id DESC LIMIT 1;
SELECT pt.*, ed.activity_type as escrow_type 
FROM points_transaction as pt 
LEFT JOIN escrow_detail as ed ON pt.id = ed.transaction_id 
WHERE pt.id > ${lastProcessedId} 
ORDER BY pt.id;
```

### 2. Balance Calculation
For each agency account:
```sql
SELECT * FROM points_transaction_upgrade 
WHERE user_id = ${agency.agency_id} 
ORDER BY id DESC LIMIT 1;
```

### 3. Record Transformation
For each transaction:
- Determine if it's a reference transaction or original
- Apply appropriate transformation logic
- Create double-entry records where needed

## Transaction Types

### Reference Transactions (ref_transaction_id !== 0)
Simple balance updates with activity type preservation:
```javascript
const row = {
  user_id: element.user_id,
  activity_type: element.activity_type,
  points: Number(element.points),
  balance: updatedBalance,
  note: element.note,
  created_on: element.created_on,
  payer: element.payer,
  payee: element.payee,
  ori_id: element.ref_transaction_id
};
```

### Original Transactions (ref_transaction_id === 0)
Double-entry bookkeeping with agency account management:

#### Transaction A (User Record)
```javascript
const rowA = {
  user_id: element.user_id,
  activity_type: activityType,
  points: Number(element.points),
  balance: Number(element.balance),
  note: element.note,
  created_on: element.created_on,
  payer: getAgencyPayerAccount(activityType, element.user_id),
  payee: getAgencyPayeeAccount(activityType, element.user_id),
  ori_id: element.id
};
```

#### Transaction B (Agency Record)
```javascript
const rowB = {
  user_id: agencyUserId,
  activity_type: activityType,
  points: 0 - Number(element.points),
  balance: updatedAgencyBalance,
  note: element.note,
  created_on: element.created_on,
  payer: getAgencyPayerAccount(activityType, element.user_id),
  payee: getAgencyPayeeAccount(activityType, element.user_id),
  ori_id: element.id
};
```

## Activity Type Mapping

### Payer Account Rules
- **Type 1**: System (0)
- **Type 2**: Agency 2100
- **Type 3**: User
- **Type 4**: Agency 2000
- **Type 5**: Agency 2100
- **Type 6**: Agency 2002
- **Type 7**: Agency 2001
- **Type 8-12**: Various user/agency combinations

### Payee Account Rules
- **Type 1**: System (0)
- **Type 2**: User
- **Type 3**: Agency 2102
- **Type 4**: User
- **Type 5**: User
- **Type 6**: User
- **Type 7**: User
- **Type 8-12**: Various user/agency combinations

## Data Models

### Source Table (points_transaction)
```javascript
{
  id: number,
  user_id: number,
  activity_type: number,
  points: number,
  balance: number,
  note: string,
  created_on: datetime,
  payer: number,
  payee: number,
  ref_transaction_id: number
}
```

### Target Table (points_transaction_upgrade)
```javascript
{
  id: number, // Auto-increment
  user_id: number,
  activity_type: number,
  points: number,
  balance: number,
  note: string,
  created_on: datetime,
  payer: number,
  payee: number,
  ori_id: number // Original transaction ID
}
```

### Escrow Detail Reference
```javascript
{
  transaction_id: number,
  activity_type: number // Used for escrow type restoration
}
```

## Business Logic

### Escrow Type Handling
For activity type 8 (escrow transactions):
- Check escrow_detail table for original activity type
- Restore appropriate activity type (9 or 10)
- Maintain transaction integrity

### Balance Tracking
- Real-time agency balance calculation
- Sequential processing maintains accuracy
- Double-entry system ensures balance integrity

### Data Integrity
- Preserves original transaction IDs
- Maintains audit trail through ori_id field
- Handles both user and agency accounts

## Performance Considerations
- Incremental processing reduces load
- Batch insertion for efficiency
- Agency balance caching during processing
- Sequential processing ensures data consistency

## Error Handling
```javascript
try {
  // Main processing logic
} catch (err) {
  logger.info(`[update-point-transaction] : update failed : ${err}`);
}
```

## Integration Points
- Legacy point transaction system
- Escrow detail tracking
- Agency account management
- Balance reconciliation system

## Usage Scenarios
- Daily incremental data migration
- System upgrade processing
- Data consistency maintenance
- Balance reconciliation

## Notes
- Designed for one-time migration or incremental updates
- Maintains backward compatibility through ori_id tracking
- Supports complex agency account structures
- Ensures double-entry bookkeeping compliance
- Critical for financial data integrity