# check_purchase_transaction.js - Purchase Transaction Migration Validation Job

## Quick Summary

The `check_purchase_transaction.js` job is a comprehensive validation system designed to ensure the integrity of purchase transaction migration between legacy and upgraded database schemas. This job performs both data consistency validation and relational integrity verification for purchase transactions, ensuring that financial transaction records maintain accuracy and proper relationships with points transactions throughout the migration process. The job implements strict assertion-based validation with detailed logging and cross-table relationship verification.

## Technical Analysis

### Core Architecture

The job implements a dual-phase validation approach combining data field validation with complex relationship verification. This ensures both individual record accuracy and system-wide relational integrity across the purchase transaction migration.

### Checker Class Implementation

The job utilizes a standardized Checker class for consistent field-by-field validation:
```javascript
function Checker(obj1, obj2, result) {
  this.obj1 = obj1;
  this.obj2 = obj2;
  this.result = result;
  this.check = function (key) {
    if (this.obj1[key] === this.obj2[key]) {
      this.result.success++;
    } else {
      logger.warn(`${key} check failed ${this.obj1[key]} : ${this.obj2[key]}`);
      this.result.fail++;
    }
    return this;
  };
}
```

This implementation provides fluent interface chaining with automatic result aggregation and detailed discrepancy logging for troubleshooting.

### Data Comparison Logic

#### Purchase Transaction Field Validation
```javascript
async function compareWithOldData() {
  try {
    const list = await knex('purchase_transaction_upgrade');
    const result = { success: 0, fail: 0 };
    for (const t of list) {
      const old = await knex('purchase_transaction').where({ id: t.ori_id });
      const checker = new Checker(t, old[0], result);
      checker
        .check('user_id')
        .check('points')
        .check('amount')
        .check('currency')
        .check('transaction_id')
        .check('created_on');
    }
    return result;
  } catch (e) {
    logger.warn(`[compareWithOldData] error: ${e.message}`);
  }
}
```

The validation covers critical financial transaction fields:
- **user_id** - User association integrity
- **points** - Points value accuracy
- **amount** - Monetary amount consistency
- **currency** - Currency code preservation
- **transaction_id** - External transaction reference
- **created_on** - Temporal data integrity

### Relationship Validation Logic

#### Cross-Table Relationship Verification
```javascript
async function checkRelation() {
  try {
    const list = await knex('purchase_transaction_upgrade');
    const result = { success: 0, fail: 0 };
    for (const t of list) {
      const old = await knex('purchase_transaction').where({ id: t.ori_id });
      if (old.length > 0) {
        const tr1 = await knex('points_transaction_upgrade').where({
          id: t.point_transaction_id,
        });
        const tr2 = await knex('points_transaction').where({
          id: old[0].point_transaction_id,
        });
        if (tr1.length > 0 && tr2.length > 0) {
          if (tr1[0].ori_id === tr2[0].id) {
            result.success++;
          } else {
            result.fail++;
          }
        }
      } else {
        result.fail++;
      }
    }
    return result;
  } catch (e) {
    logger.warn(`[checkRelation] error: ${e.message}`);
  }
}
```

This complex validation ensures that:
- Purchase transactions correctly reference their associated points transactions
- Relationships between upgraded and legacy records are maintained
- Foreign key integrity is preserved across migration

### Assertion-Based Validation

The job implements strict validation with assertion enforcement:
```javascript
const check1 = await compareWithOldData();
assert(check1.fail === 0, 'expect compareWithOldData fail number is zero');
const check2 = await checkRelation();
assert(check2.fail === 0, 'expect checkRelation fail number is zero');
```

Any validation failure triggers immediate job termination with descriptive error messages.

## Usage/Integration

### Execution Context

This job is executed as part of the purchase transaction migration validation pipeline, typically running after both purchase transaction and points transaction migrations have been completed. The job serves as a critical quality gate for financial data integrity.

### Validation Workflow

1. **Data Consistency Phase** - Validates field-by-field accuracy between tables
2. **Relationship Integrity Phase** - Verifies cross-table relationship consistency
3. **Assertion Enforcement** - Ensures zero-tolerance for validation failures
4. **Performance Reporting** - Provides execution timing metrics

### Integration Points

- **Financial Migration Pipeline** - Executed after purchase transaction migration
- **Quality Assurance Gates** - Mandatory validation before production deployment
- **Monitoring Systems** - Assertion failures trigger immediate alerts
- **Audit Trail** - Detailed logging for compliance and troubleshooting

### Error Handling Strategy

The job prioritizes data integrity over fault tolerance:
- Assertion failures halt execution immediately
- Detailed error logging captures specific failure points
- Performance metrics enable optimization analysis

## Dependencies

### Core Framework Dependencies
- **@maas/core/mysql** - Database connectivity and transaction management
- **@maas/core/log** - Structured logging infrastructure
- **chai** - Assertion library for strict validation enforcement

### Database Requirements
- **MySQL Portal Database** - Read access to financial transaction tables
- **Transaction Isolation** - Consistent read isolation during validation
- **Index Optimization** - Proper indexing on `id`, `ori_id`, and `point_transaction_id` fields

### Schema Dependencies
- **purchase_transaction_upgrade** - Target migration table
- **purchase_transaction** - Source legacy table
- **points_transaction_upgrade** - Related upgraded points transactions
- **points_transaction** - Related legacy points transactions

## Code Examples

### Basic Job Execution
```javascript
const job = require('./check_purchase_transaction');
try {
  await job.fn();
  console.log('Purchase transaction validation completed successfully');
} catch (error) {
  console.error('Validation failed:', error.message);
}
```

### Manual Data Comparison
```javascript
async function validatePurchaseRecord(purchaseId) {
  const upgrade = await knex('purchase_transaction_upgrade').where({ id: purchaseId }).first();
  const original = await knex('purchase_transaction').where({ id: upgrade.ori_id }).first();
  
  const result = { success: 0, fail: 0 };
  const checker = new Checker(upgrade, original, result);
  
  const validation = checker
    .check('user_id')
    .check('points')
    .check('amount')
    .check('currency')
    .check('transaction_id')
    .check('created_on');
  
  return result;
}
```

### Relationship Validation
```javascript
async function validatePurchaseRelationships(purchaseId) {
  const purchase = await knex('purchase_transaction_upgrade').where({ id: purchaseId }).first();
  const originalPurchase = await knex('purchase_transaction').where({ id: purchase.ori_id }).first();
  
  if (!originalPurchase) {
    throw new Error(`Original purchase record not found for ID: ${purchase.ori_id}`);
  }
  
  // Validate points transaction relationship
  const [upgradeTransaction, originalTransaction] = await Promise.all([
    knex('points_transaction_upgrade').where({ id: purchase.point_transaction_id }).first(),
    knex('points_transaction').where({ id: originalPurchase.point_transaction_id }).first()
  ]);
  
  if (!upgradeTransaction || !originalTransaction) {
    throw new Error('Related points transactions not found');
  }
  
  if (upgradeTransaction.ori_id !== originalTransaction.id) {
    throw new Error('Points transaction relationship integrity violated');
  }
  
  return {
    purchase_valid: true,
    relationship_valid: true,
    upgrade_transaction_id: upgradeTransaction.id,
    original_transaction_id: originalTransaction.id
  };
}
```

### Comprehensive Validation with Reporting
```javascript
async function comprehensiveValidation() {
  const start = Date.now();
  const report = {
    total_records: 0,
    data_validation: { success: 0, fail: 0 },
    relationship_validation: { success: 0, fail: 0 },
    errors: []
  };
  
  try {
    // Data validation phase
    const dataResult = await compareWithOldData();
    report.data_validation = dataResult;
    
    // Relationship validation phase
    const relationResult = await checkRelation();
    report.relationship_validation = relationResult;
    
    // Calculate totals
    report.total_records = await knex('purchase_transaction_upgrade').count('id as count').first();
    
    const end = Date.now();
    report.execution_time_seconds = (end - start) / 1000;
    
    // Validate assertions
    if (dataResult.fail > 0) {
      throw new Error(`Data validation failed: ${dataResult.fail} failures`);
    }
    
    if (relationResult.fail > 0) {
      throw new Error(`Relationship validation failed: ${relationResult.fail} failures`);
    }
    
    report.status = 'SUCCESS';
    return report;
    
  } catch (error) {
    report.status = 'FAILED';
    report.error = error.message;
    throw error;
  }
}
```

### Financial Integrity Verification
```javascript
async function verifyFinancialIntegrity() {
  const purchaseRecords = await knex('purchase_transaction_upgrade');
  const integrityReport = {
    total_amount: 0,
    total_points: 0,
    currency_distribution: {},
    validation_errors: []
  };
  
  for (const record of purchaseRecords) {
    try {
      const original = await knex('purchase_transaction').where({ id: record.ori_id }).first();
      
      if (!original) {
        integrityReport.validation_errors.push({
          error: 'Missing original record',
          record_id: record.id,
          ori_id: record.ori_id
        });
        continue;
      }
      
      // Accumulate financial totals
      integrityReport.total_amount += parseFloat(record.amount);
      integrityReport.total_points += parseFloat(record.points);
      
      // Track currency distribution
      integrityReport.currency_distribution[record.currency] = 
        (integrityReport.currency_distribution[record.currency] || 0) + 1;
      
      // Validate financial consistency
      if (record.amount !== original.amount) {
        integrityReport.validation_errors.push({
          error: 'Amount mismatch',
          record_id: record.id,
          upgrade_amount: record.amount,
          original_amount: original.amount
        });
      }
      
    } catch (error) {
      integrityReport.validation_errors.push({
        error: error.message,
        record_id: record.id
      });
    }
  }
  
  return integrityReport;
}
```

This validation job serves as a critical financial data integrity checkpoint, ensuring that purchase transaction migrations maintain both data accuracy and relational consistency essential for financial system operations.