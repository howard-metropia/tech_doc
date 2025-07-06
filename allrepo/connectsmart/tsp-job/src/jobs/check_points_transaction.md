# check_points_transaction.js - Points Transaction Migration Validation Job

## Quick Summary

The `check_points_transaction.js` job is a sophisticated data validation system designed to verify the integrity of points transaction migration across different activity types. This job systematically validates that all records from the legacy `points_transaction` table have been properly migrated to the `points_transaction_upgrade` table with the correct pairing relationships. The job performs comprehensive checks across 12 different activity types, ensuring that transaction pairs and reference relationships are maintained correctly during migration.

## Technical Analysis

### Core Architecture

The job implements a comprehensive validation strategy that operates across multiple activity types, performing detailed mapping verification between original and upgraded transaction records. The validation process handles both simple single-record migrations and complex paired transaction scenarios.

### Activity Type Processing

The job validates 12 distinct activity types, each representing different transaction categories:
```javascript
const checkActivityType = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
```

Each activity type corresponds to specific business logic:
- **Type 1-3**: Basic transaction types
- **Type 4-6**: Reward and incentive transactions  
- **Type 7-9**: Service-related transactions
- **Type 10-12**: Advanced transaction scenarios

### Validation Logic Implementation

#### Primary Validation Query
```javascript
const SQL = `SELECT *,COUNT(ori_id) AS count FROM points_transaction_upgrade WHERE activity_type = ${activityType} GROUP BY ori_id;`;
```

This query groups upgraded transactions by their original ID, counting how many records exist for each original transaction. The expected count is typically 2 (for paired transactions).

#### Pairing Validation Logic
```javascript
const checkPtuData = ptuDataResult.filter((item) => {
  return item.count !== 2;
});
```

Records with counts other than 2 indicate potential migration issues that require deeper investigation.

#### Reference Transaction Validation
```javascript
for (let j = 0; j < checkPtData.length; j++) {
  if (checkPtData[j].ref_transaction_id !== '') {
    const idIndex = needCheckId.indexOf(checkPtData[j].id);
    if (idIndex !== -1) {
      needCheckId.splice(idIndex, 1);
    }
    const rfIdIindex = needCheckId.indexOf(checkPtData[j].ref_transaction_id);
    if (rfIdIindex !== -1) {
      needCheckId.splice(rfIdIindex, 1);
    }
  }
}
```

This logic validates that reference transaction relationships are properly maintained, removing validated IDs from the check list.

### Performance Optimization

The job implements efficient batch processing:
```javascript
const total = (ptuDataResult.length - checkPtuData.length) * 2 + checkPtuData.length;
```

This calculation optimizes the validation process by pre-calculating expected totals and focusing validation efforts on potentially problematic records.

### Error Detection and Reporting

The job provides detailed logging for each validation phase:
```javascript
logger.info(`[checkout-point-transaction] : checkout activity type ${activityType} total ${total}.`);
```

Failed validations are reported with specific transaction IDs:
```javascript
logger.info(`[checkout-point-transaction] : checkout activity type ${activityType} fail, points_transaction id ${needCheckId.join(',')} not mapping points_transaction_upgrade.`);
```

## Usage/Integration

### Execution Context

This job is executed as part of the points transaction migration validation pipeline, typically after the primary migration process has completed. The job is designed to run as a comprehensive integrity check across all activity types.

### Validation Workflow

1. **Iterative Processing** - Sequentially validates each activity type
2. **Anomaly Detection** - Identifies records with unexpected pairing counts
3. **Reference Validation** - Verifies transaction reference relationships
4. **Completion Reporting** - Provides success/failure status for each activity type

### Integration Points

- **Migration Pipeline** - Executed after points transaction migration
- **Quality Assurance** - Part of comprehensive migration validation
- **Monitoring Systems** - Logs consumed by operational monitoring
- **Alert Systems** - Failures trigger immediate operational alerts

### Performance Characteristics

The job implements time tracking for performance monitoring:
```javascript
const start = new Date().getTime();
// ... validation logic ...
const end = new Date().getTime();
logger.info(`Time taken: ${(end - start) / 1000} secs`);
```

## Dependencies

### Core Framework Dependencies
- **@maas/core/mysql** - Database connectivity and raw SQL execution capabilities
- **@maas/core/log** - Structured logging infrastructure for detailed validation reporting

### Database Requirements
- **MySQL Portal Database** - Read access to both legacy and upgraded transaction tables
- **Connection Pool Management** - Sufficient connections for concurrent queries across activity types
- **Index Optimization** - Proper indexing on `ori_id` and `activity_type` fields for query performance

### Schema Dependencies
- **points_transaction_upgrade** - Target migration table with activity type grouping
- **points_transaction** - Source legacy table with reference transaction relationships
- **Database Constraints** - Foreign key relationships between transaction tables

## Code Examples

### Manual Activity Type Validation
```javascript
async function validateActivityType(activityType) {
  const SQL = `SELECT *,COUNT(ori_id) AS count FROM points_transaction_upgrade WHERE activity_type = ${activityType} GROUP BY ori_id;`;
  const [results] = await knex.raw(SQL);
  
  const anomalies = results.filter(item => item.count !== 2);
  
  if (anomalies.length === 0) {
    console.log(`Activity type ${activityType} validation: SUCCESS`);
    return true;
  } else {
    console.log(`Activity type ${activityType} validation: ${anomalies.length} anomalies found`);
    return false;
  }
}
```

### Reference Transaction Validation
```javascript
async function validateTransactionReferences(transactionIds) {
  const SQL = `SELECT * FROM points_transaction WHERE id IN (${transactionIds}) OR ref_transaction_id IN (${transactionIds});`;
  const [results] = await knex.raw(SQL);
  
  const unmatched = [];
  for (const transaction of results) {
    if (transaction.ref_transaction_id !== '' && !transactionIds.includes(transaction.ref_transaction_id)) {
      unmatched.push(transaction.id);
    }
  }
  
  return unmatched;
}
```

### Comprehensive Migration Check
```javascript
async function runFullValidation() {
  const activityTypes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
  const results = {};
  
  for (const type of activityTypes) {
    try {
      const isValid = await validateActivityType(type);
      results[type] = isValid ? 'SUCCESS' : 'FAILED';
    } catch (error) {
      results[type] = `ERROR: ${error.message}`;
    }
  }
  
  return results;
}
```

### Batch Validation with Error Handling
```javascript
async function validateWithErrorHandling() {
  try {
    const start = Date.now();
    const validationResults = await runFullValidation();
    const end = Date.now();
    
    const failedTypes = Object.entries(validationResults)
      .filter(([type, result]) => result !== 'SUCCESS')
      .map(([type, result]) => ({ type, result }));
    
    if (failedTypes.length > 0) {
      throw new Error(`Validation failed for activity types: ${failedTypes.map(f => f.type).join(', ')}`);
    }
    
    console.log(`Validation completed successfully in ${(end - start) / 1000} seconds`);
  } catch (error) {
    console.error(`Validation job failed: ${error.message}`);
    throw error;
  }
}
```

This validation job ensures the integrity of points transaction migration by systematically verifying that all transaction records have been properly migrated with correct pairing relationships maintained across all activity types. The job's comprehensive approach to validation makes it a critical component in the migration quality assurance process.