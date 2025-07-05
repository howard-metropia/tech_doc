# reverse_migration_points_transaction.js - Points Transaction Reverse Migration Job

## Quick Summary

The `reverse_migration_points_transaction.js` job is a specialized data recovery system designed to reverse points transaction migrations by converting upgraded double-entry records back to the legacy single-entry format. This job specifically processes records with `ori_id = 0` (indicating they were created during migration rather than upgraded from existing records) and reconstructs the original transaction relationships in the legacy tables. The job implements comprehensive data restoration including related escrow details, promotion redeems, and purchase transactions while maintaining referential integrity throughout the reverse migration process.

## Technical Analysis

### Core Architecture

The job implements a selective reverse migration strategy focused on migrated records that don't have original counterparts in the legacy system. The architecture includes:

1. **Selective Record Processing** - Targets only migration-generated records (`ori_id = 0`)
2. **Transaction Pair Handling** - Processes related transaction pairs together
3. **Related Data Restoration** - Reverses migration for associated tables
4. **Reference Relationship Restoration** - Rebuilds legacy reference relationships

### Target Record Identification

```javascript
const sql1 = `select * from points_transaction_upgrade where ori_id = 0;`;
const [rows1] = await knex.raw(sql1);
```

The job specifically targets records with `ori_id = 0`, which indicates these records were created during the upgrade process rather than being direct migrations of existing legacy records.

### Transaction Pair Processing Logic

#### Primary Transaction Processing
```javascript
if (element.ref_transaction_id !== 0) {
  const row = {
    user_id: element.user_id,
    activity_type: element.activity_type,
    points: Number(element.points),
    balance: Number(element.balance),
    note: element.note,
    created_on: element.created_on,
    payer: element.payer,
    payee: element.payee,
  };
  const _id = await knex('points_transaction').insert(row);
  // Process related data...
}
```

Primary transactions are inserted into the legacy table with their complete attribute set, excluding upgrade-specific fields.

#### Paired Transaction Handling
```javascript
let other = null;
rows1.some((r) => {
  if (r.id === element.ref_transaction_id) {
    other = r;
    return true;
  } else {
    return false;
  }
});

if (other && !done1.has(other.id)) {
  const row = {
    user_id: other.user_id,
    activity_type: other.activity_type,
    points: Number(other.points),
    balance: Number(other.balance),
    note: other.note,
    created_on: other.created_on,
    payer: other.payer,
    payee: other.payee,
    ref_transaction_id: _id,
  };
  const __id = await knex('points_transaction').insert(row);
  // Update primary transaction reference...
}
```

The job locates and processes paired transactions, maintaining the reference relationships in the legacy table structure.

### Related Data Migration Functions

#### Escrow Detail Restoration
```javascript
async function migrateEscrowDetail(from, to) {
  try {
    const sql2 = `select * from escrow_detail_upgrade where transaction_id = ?`;
    const [rows2] = await knex.raw(sql2, [from]);
    for (const element of rows2) {
      const row = {
        escrow_id: element.escrow_id,
        activity_type: element.activity_type,
        fund: Number(element.fund),
        offer_id: element.offer_id,
        created_on: element.created_on,
        modified_on: element.modified_on,
        transaction_id: to,
      };
      await knex('escrow_detail').insert(row);
    }
    return rows2.length;
  } catch (e) {
    logger.warn(e.message);
    return 0;
  }
}
```

This function restores escrow detail records by copying data from the upgrade table back to the legacy table structure, removing upgrade-specific fields like `ori_id`.

#### Promotion Redeem Restoration
```javascript
async function migratePromotionRedeem(from, to) {
  try {
    const sql3 = `select * from promotion_redeem_upgrade where point_transaction_id = ?;`;
    const [rows3] = await knex.raw(sql3, [from]);
    for (const element of rows3) {
      const row = {
        user_id: element.user_id,
        promotion_id: element.promotion_id,
        point_transaction_id: to,
        created_on: element.created_on,
      };
      await knex('promotion_redeem').insert(row);
    }
    return rows3.length;
  } catch (e) {
    logger.warn(e.message);
    return 0;
  }
}
```

### Reference Relationship Management

The job includes a critical bug in the reference update logic:
```javascript
await knex('points_transaciton')  // Note: typo in table name
  .where({ id: _id })
  .update({ ref_transaction_id: __id });
```

This typo (`points_transaciton` instead of `points_transaction`) would cause reference updates to fail silently, potentially breaking referential integrity.

### Error Handling and Logging

The job implements comprehensive error handling for related data migration:
```javascript
catch (e) {
  logger.warn(e.message);
  logger.warn(e.stack);
  return 0;
}
```

Errors in related data migration are logged but don't halt the primary migration process, allowing partial recovery to proceed.

## Usage/Integration

### Execution Context

This job is designed for rollback scenarios where points transaction upgrades need to be reversed, typically used in:
- Migration rollback procedures
- Data recovery operations
- Testing and validation environments
- Emergency restoration scenarios

### Restoration Workflow

1. **Target Identification** - Query upgrade records with `ori_id = 0`
2. **Transaction Pair Processing** - Handle primary and paired transactions together
3. **Legacy Record Creation** - Insert records into legacy transaction table
4. **Reference Relationship Restoration** - Establish proper cross-references
5. **Related Data Migration** - Restore escrow, promotion, and purchase data
6. **Performance Tracking** - Monitor execution metrics and record counts

### Integration Points

- **Rollback Procedures** - Part of comprehensive migration rollback strategy
- **Data Recovery** - Emergency data restoration workflows
- **Testing Environments** - Validation of migration reversibility
- **Quality Assurance** - Ensures migration processes are fully reversible

## Dependencies

### Core Framework Dependencies
- **@maas/core/mysql** - Database connectivity and transaction management
- **@maas/core/log** - Structured logging infrastructure

### Database Requirements
- **MySQL Portal Database** - Write access to legacy transaction tables
- **Referential Integrity** - Proper foreign key handling during restoration
- **Transaction Support** - ACID compliance for multi-table operations

### Schema Dependencies
- **points_transaction_upgrade** - Source upgraded transaction table
- **points_transaction** - Target legacy transaction table
- **escrow_detail_upgrade/escrow_detail** - Related escrow data tables
- **promotion_redeem_upgrade/promotion_redeem** - Related promotion tables
- **purchase_transaction_upgrade/purchase_transaction** - Related purchase tables

## Code Examples

### Basic Reverse Migration Execution
```javascript
const job = require('./reverse_migration_points_transaction');
try {
  await job.fn();
  console.log('Reverse migration completed successfully');
} catch (error) {
  console.error('Reverse migration failed:', error.message);
}
```

### Fixed Reference Update Logic
```javascript
async function fixedReferenceUpdate(primaryId, pairedId) {
  // Fixed version without typo
  await knex('points_transaction')
    .where({ id: primaryId })
    .update({ ref_transaction_id: pairedId });
}
```

### Manual Transaction Pair Restoration
```javascript
async function restoreTransactionPair(upgradeRecord) {
  if (!upgradeRecord.ref_transaction_id) {
    throw new Error('Record is not part of a transaction pair');
  }
  
  // Find the paired record
  const pairedRecord = await knex('points_transaction_upgrade')
    .where({ id: upgradeRecord.ref_transaction_id })
    .first();
  
  if (!pairedRecord) {
    throw new Error(`Paired record not found: ${upgradeRecord.ref_transaction_id}`);
  }
  
  // Restore primary transaction
  const primaryLegacyId = await restoreSingleTransaction(upgradeRecord);
  
  // Restore paired transaction
  const pairedLegacyId = await restoreSingleTransaction(pairedRecord);
  
  // Update reference relationships
  await knex('points_transaction')
    .where({ id: primaryLegacyId })
    .update({ ref_transaction_id: pairedLegacyId });
  
  await knex('points_transaction')
    .where({ id: pairedLegacyId })
    .update({ ref_transaction_id: primaryLegacyId });
  
  return { primaryLegacyId, pairedLegacyId };
}
```

### Single Transaction Restoration
```javascript
async function restoreSingleTransaction(upgradeRecord) {
  const legacyRecord = {
    user_id: upgradeRecord.user_id,
    activity_type: upgradeRecord.activity_type,
    points: Number(upgradeRecord.points),
    balance: Number(upgradeRecord.balance),
    note: upgradeRecord.note,
    created_on: upgradeRecord.created_on,
    payer: upgradeRecord.payer,
    payee: upgradeRecord.payee,
  };
  
  // Add ref_transaction_id if it exists
  if (upgradeRecord.ref_transaction_id && upgradeRecord.ref_transaction_id !== 0) {
    legacyRecord.ref_transaction_id = upgradeRecord.ref_transaction_id;
  }
  
  const [insertId] = await knex('points_transaction').insert(legacyRecord);
  
  // Restore related data
  await Promise.all([
    migrateEscrowDetail(upgradeRecord.id, insertId),
    migratePromotionRedeem(upgradeRecord.id, insertId),
    migratiePurchaseTransaction(upgradeRecord.id, insertId)
  ]);
  
  return insertId;
}
```

### Comprehensive Reverse Migration with Validation
```javascript
async function comprehensiveReverseMigration() {
  const start = Date.now();
  const metrics = {
    start_time: new Date().toISOString(),
    processed_records: 0,
    restored_pairs: 0,
    related_data_restored: {
      escrow_details: 0,
      promotion_redeems: 0,
      purchase_transactions: 0
    },
    errors: []
  };
  
  try {
    // Get all records that need reverse migration
    const upgradeRecords = await knex('points_transaction_upgrade')
      .where({ ori_id: 0 });
    
    const processedIds = new Set();
    
    for (const record of upgradeRecords) {
      if (processedIds.has(record.id)) {
        continue; // Already processed as part of a pair
      }
      
      try {
        if (record.ref_transaction_id !== 0) {
          // Process as transaction pair
          const result = await restoreTransactionPair(record);
          processedIds.add(record.id);
          processedIds.add(record.ref_transaction_id);
          metrics.restored_pairs++;
          metrics.processed_records += 2;
        } else {
          // Process as standalone transaction
          await restoreSingleTransaction(record);
          processedIds.add(record.id);
          metrics.processed_records++;
        }
      } catch (error) {
        metrics.errors.push({
          record_id: record.id,
          error: error.message
        });
      }
    }
    
    const end = Date.now();
    metrics.execution_time_ms = end - start;
    metrics.end_time = new Date().toISOString();
    metrics.status = 'SUCCESS';
    
    if (metrics.errors.length > 0) {
      console.warn(`Reverse migration completed with ${metrics.errors.length} errors`);
    }
    
    return metrics;
    
  } catch (error) {
    metrics.status = 'FAILED';
    metrics.error = error.message;
    metrics.execution_time_ms = Date.now() - start;
    throw error;
  }
}
```

### Data Integrity Validation
```javascript
async function validateReverseMigration() {
  const validation = {
    missing_references: [],
    orphaned_records: [],
    data_mismatches: []
  };
  
  // Check for missing reference relationships
  const unreferencedRecords = await knex('points_transaction')
    .whereNotNull('ref_transaction_id')
    .whereNotExists(function() {
      this.select('*')
        .from('points_transaction as pt2')
        .whereRaw('pt2.id = points_transaction.ref_transaction_id');
    });
  
  validation.missing_references = unreferencedRecords.map(r => r.id);
  
  // Check for orphaned related data
  const orphanedEscrow = await knex('escrow_detail')
    .whereNotExists(function() {
      this.select('*')
        .from('points_transaction')
        .whereRaw('points_transaction.id = escrow_detail.transaction_id');
    });
  
  validation.orphaned_records.push(...orphanedEscrow.map(r => ({
    type: 'escrow_detail',
    id: r.id,
    transaction_id: r.transaction_id
  })));
  
  return validation;
}
```

This reverse migration job provides essential rollback capabilities for the points transaction system, enabling recovery from migration issues and supporting comprehensive testing of migration processes. However, the table name typo in the reference update logic should be fixed to ensure proper referential integrity during reverse migrations.