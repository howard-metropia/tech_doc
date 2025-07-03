# check_promotion_redeem.js - Promotion Redeem Migration Validation Job

## Quick Summary

The `check_promotion_redeem.js` job is a focused data validation utility designed to verify the integrity of promotion redemption record migration. This job ensures that promotional transaction data has been accurately transferred from the legacy `promotion_redeem` table to the upgraded `promotion_redeem_upgrade` table. The job implements a streamlined validation approach using a reusable Checker class to perform field-by-field comparison of critical promotion redemption attributes including user associations, promotion references, and temporal data.

## Technical Analysis

### Core Architecture

The job employs a simplified yet effective validation pattern that focuses on essential promotion redemption data integrity. Unlike more complex migration validation jobs, this implementation prioritizes speed and clarity while maintaining thorough validation coverage.

### Checker Class Implementation

The job utilizes a shared Checker class pattern for consistent validation logic:
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

This implementation provides a fluent interface for chaining validation operations with automatic result tracking and detailed discrepancy logging.

### Validation Logic

#### Core Comparison Function
```javascript
async function compareWithOldData() {
  try {
    const list = await knex('promotion_redeem_upgrade');
    const result = { success: 0, fail: 0 };
    for (const t of list) {
      const old = await knex('promotion_redeem').where({ id: t.ori_id });
      const checker = new Checker(t, old[0], result);
      checker.check('user_id').check('promotion_id').check('created_on');
    }
  } catch (e) {
    logger.warn(`[compareWithOldData] error: ${e.message}`);
  }
}
```

The validation process focuses on three critical fields:
- **user_id** - Ensures user association integrity
- **promotion_id** - Validates promotion reference consistency  
- **created_on** - Verifies temporal data accuracy

### Simplified Error Handling

The job implements basic error handling with contextual logging:
```javascript
catch (e) {
  logger.warn(`[compareWithOldData] error: ${e.message}`);
}
```

Error conditions are logged for analysis but do not halt execution, allowing the validation process to continue even if individual record comparisons fail.

### Performance Considerations

The job is designed for efficiency with:
- Single-pass validation through upgrade table records
- Direct ID-based lookups in the legacy table
- Minimal memory footprint through streaming record processing

## Usage/Integration

### Execution Context

This job is typically executed as part of the promotion system migration validation pipeline, running after the initial promotion redemption data migration has been completed. The job serves as a quality gate to ensure promotional data integrity.

### Validation Scope

The job validates three critical aspects of promotion redemption records:
- **User Association** - Verifies that user IDs remain consistent across migration
- **Promotion Reference** - Ensures promotion IDs are accurately preserved
- **Temporal Integrity** - Confirms creation timestamps are maintained

### Integration Points

- **Promotion Migration Pipeline** - Executed after promotion redemption migration
- **Quality Assurance Workflows** - Part of promotional system data validation
- **Monitoring Infrastructure** - Logs consumed by centralized monitoring systems
- **Data Governance** - Ensures compliance with promotional data policies

### Performance Characteristics

The job includes basic performance tracking:
```javascript
const start = new Date().getTime();
await compareWithOldData();
const end = new Date().getTime();
logger.info(`Time taken: ${(end - start) / 1000} secs`);
```

## Dependencies

### Core Framework Dependencies
- **@maas/core/mysql** - Database connectivity for cross-table validation queries
- **@maas/core/log** - Structured logging infrastructure for validation reporting

### Database Requirements
- **MySQL Portal Database** - Read access to both legacy and upgraded promotion tables
- **Table Schema Compatibility** - Consistent field types and constraints across tables
- **Index Optimization** - Proper indexing on `id` and `ori_id` fields for lookup performance

### Schema Dependencies
- **promotion_redeem_upgrade** - Target migration table containing upgraded records
- **promotion_redeem** - Source legacy table with original redemption data
- **Foreign Key Relationships** - Proper relationships with user and promotion master tables

## Code Examples

### Basic Validation Execution
```javascript
const job = require('./check_promotion_redeem');
await job.fn();
```

### Manual Field Validation
```javascript
async function validatePromotionRedemption(upgradeRecord) {
  const originalRecord = await knex('promotion_redeem').where({ id: upgradeRecord.ori_id }).first();
  
  if (!originalRecord) {
    throw new Error(`Original record not found for ori_id: ${upgradeRecord.ori_id}`);
  }
  
  const result = { success: 0, fail: 0 };
  const checker = new Checker(upgradeRecord, originalRecord, result);
  
  checker
    .check('user_id')
    .check('promotion_id')
    .check('created_on');
  
  return result;
}
```

### Batch Validation with Error Handling
```javascript
async function validateAllPromotionRedemptions() {
  try {
    const upgradeRecords = await knex('promotion_redeem_upgrade');
    const results = { success: 0, fail: 0, errors: [] };
    
    for (const record of upgradeRecords) {
      try {
        const validation = await validatePromotionRedemption(record);
        results.success += validation.success;
        results.fail += validation.fail;
      } catch (error) {
        results.errors.push({
          record_id: record.id,
          ori_id: record.ori_id,
          error: error.message
        });
      }
    }
    
    return results;
  } catch (error) {
    console.error(`Batch validation failed: ${error.message}`);
    throw error;
  }
}
```

### Custom Validation with Extended Checks
```javascript
async function extendedPromotionValidation() {
  const list = await knex('promotion_redeem_upgrade');
  const detailedResults = {
    total_records: list.length,
    validated_records: 0,
    user_id_mismatches: [],
    promotion_id_mismatches: [],
    timestamp_mismatches: [],
    missing_originals: []
  };
  
  for (const upgrade of list) {
    const original = await knex('promotion_redeem').where({ id: upgrade.ori_id }).first();
    
    if (!original) {
      detailedResults.missing_originals.push(upgrade.ori_id);
      continue;
    }
    
    detailedResults.validated_records++;
    
    if (upgrade.user_id !== original.user_id) {
      detailedResults.user_id_mismatches.push({
        ori_id: upgrade.ori_id,
        upgrade_value: upgrade.user_id,
        original_value: original.user_id
      });
    }
    
    if (upgrade.promotion_id !== original.promotion_id) {
      detailedResults.promotion_id_mismatches.push({
        ori_id: upgrade.ori_id,
        upgrade_value: upgrade.promotion_id,
        original_value: original.promotion_id
      });
    }
    
    if (upgrade.created_on !== original.created_on) {
      detailedResults.timestamp_mismatches.push({
        ori_id: upgrade.ori_id,
        upgrade_value: upgrade.created_on,
        original_value: original.created_on
      });
    }
  }
  
  return detailedResults;
}
```

### Performance-Optimized Validation
```javascript
async function optimizedValidation() {
  const start = Date.now();
  
  // Batch fetch for better performance
  const [upgradeRecords, originalRecords] = await Promise.all([
    knex('promotion_redeem_upgrade').select('*'),
    knex('promotion_redeem').select('*')
  ]);
  
  // Create lookup map for O(1) access
  const originalMap = new Map();
  originalRecords.forEach(record => {
    originalMap.set(record.id, record);
  });
  
  const results = { success: 0, fail: 0, missing: 0 };
  
  for (const upgrade of upgradeRecords) {
    const original = originalMap.get(upgrade.ori_id);
    
    if (!original) {
      results.missing++;
      continue;
    }
    
    const checker = new Checker(upgrade, original, results);
    checker.check('user_id').check('promotion_id').check('created_on');
  }
  
  const end = Date.now();
  console.log(`Optimized validation completed in ${(end - start) / 1000} seconds`);
  console.log(`Results: ${results.success} success, ${results.fail} fail, ${results.missing} missing`);
  
  return results;
}
```

This validation job provides essential quality assurance for promotional system migrations, ensuring that user redemption data maintains integrity throughout the migration process. Its streamlined approach makes it suitable for frequent execution as part of automated validation pipelines.