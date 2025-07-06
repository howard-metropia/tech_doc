# upgrade-new-points-transaction-schema.js - Points Transaction Schema Upgrade Job

## Quick Summary

The `upgrade-new-points-transaction-schema.js` job is a comprehensive data synchronization system that upgrades related transaction tables (escrow details, purchase transactions, and promotion redeems) to align with the new points transaction schema structure. This job processes three critical related tables by migrating data from legacy formats to upgraded schemas while maintaining proper relationships with the migrated points transactions. The job implements sophisticated relationship mapping, excludes system agency accounts, and ensures data consistency across the entire transaction ecosystem.

## Technical Analysis

### Core Architecture

The job implements a three-phase upgrade process targeting related transaction tables:

1. **Escrow Detail Upgrade** - Migrates escrow details with transaction ID mapping
2. **Purchase Transaction Upgrade** - Upgrades purchase records with points transaction relationships  
3. **Promotion Redeem Upgrade** - Migrates promotional redemption data with updated references

Each phase includes table truncation, data transformation, and relationship establishment with the upgraded points transaction system.

### Escrow Detail Upgrade Logic

#### Data Extraction with Joins
```javascript
const edList = await knex('escrow_detail')
  .leftJoin('escrow', 'escrow.id', '=', 'escrow_detail.escrow_id')
  .orderBy('escrow_detail.id')
  .select(
    'escrow_detail.escrow_id as escrow_id',
    'escrow_detail.activity_type as activity_type',
    'escrow_detail.fund as fund',
    'escrow_detail.offer_id as offer_id',
    'escrow_detail.created_on as created_on',
    'escrow_detail.modified_on as modified_on',
    'escrow_detail.id as id',
    'escrow_detail.transaction_id as transaction_id',
  );
```

The query extracts complete escrow detail records with their parent escrow context, providing all necessary data for the upgrade transformation.

#### Transaction ID Mapping Logic
```javascript
let newId = 0;
if (ed.transaction_id && ed.transaction_id > 0) {
  const pt = await knex('points_transaction_upgrade')
    .whereNotIn('user_id', [2000, 2001, 2002, 2100, 2101, 2102, 2103])
    .andWhere('ori_id', '=', ed.transaction_id);
  if (pt.length > 0) {
    newId = pt[0].id;
  }
}
```

This critical logic maps legacy transaction IDs to new upgraded transaction IDs while excluding system agency accounts from the mapping process.

#### Record Insertion
```javascript
await knex('escrow_detail_upgrade').insert({
  escrow_id: ed.escrow_id,
  activity_type: ed.activity_type,
  fund: ed.fund,
  offer_id: ed.offer_id,
  created_on: ed.created_on,
  modified_on: ed.modified_on,
  transaction_id: newId,
  ori_id: ed.id,
});
```

### Purchase Transaction Upgrade Logic

#### Complex Join Query
```javascript
const ptList = await knex('purchase_transaction')
  .join(
    'points_transaction_upgrade',
    'points_transaction_upgrade.ori_id',
    '=',
    'purchase_transaction.point_transaction_id',
  )
  .whereNotIn(
    'points_transaction_upgrade.user_id',
    [2000, 2001, 2002, 2100, 2101, 2102, 2103],
  )
  .orderBy('purchase_transaction.id')
  .select(
    'purchase_transaction.*',
    'points_transaction_upgrade.id as new_id',
  );
```

This sophisticated join ensures that only purchase transactions with corresponding upgraded points transactions are processed, while excluding system agency accounts.

#### Data Transformation
```javascript
for (const pt of ptList) {
  await knex('purchase_transaction_upgrade').insert({
    user_id: pt.user_id,
    point_transaction_id: pt.new_id,
    points: pt.points,
    amount: pt.amount,
    currency: pt.currency,
    transaction_id: pt.transaction_id,
    created_on: pt.created_on,
    ori_id: pt.id,
  });
}
```

### Promotion Redeem Upgrade Logic

#### Relationship-Based Processing
```javascript
const prList = await knex('promotion_redeem')
  .join(
    'points_transaction_upgrade',
    'points_transaction_upgrade.ori_id',
    '=',
    'promotion_redeem.point_transaction_id',
  )
  .whereNotIn(
    'points_transaction_upgrade.user_id',
    [2000, 2001, 2002, 2100, 2101, 2102, 2103],
  )
  .orderBy('promotion_redeem.id')
  .select('promotion_redeem.*', 'points_transaction_upgrade.id as new_id');
```

The promotion redeem upgrade follows the same pattern as purchase transactions, ensuring relationship consistency across all upgraded tables.

### System Account Exclusion Strategy

All three upgrade phases consistently exclude system agency accounts:
```javascript
.whereNotIn('points_transaction_upgrade.user_id', [2000, 2001, 2002, 2100, 2101, 2102, 2103])
```

This exclusion ensures that:
- System accounts don't interfere with user transaction processing
- Agency-to-agency transactions are handled separately
- User-focused transactions maintain proper relationships

### Table Truncation Strategy

Each phase begins with table truncation:
```javascript
await knex('escrow_detail_upgrade').truncate();
await knex('purchase_transaction_upgrade').truncate();
await knex('promotion_redeem_upgrade').truncate();
```

This ensures clean slate processing and prevents duplicate data issues during repeated job executions.

## Usage/Integration

### Execution Context

This job is executed after the primary points transaction migration has been completed, serving as a critical follow-up step to ensure all related transaction data is properly synchronized with the new schema structure.

### Upgrade Workflow

1. **Escrow Detail Processing** - Migrate escrow details with transaction ID mapping
2. **Purchase Transaction Processing** - Upgrade purchase records with relationship preservation
3. **Promotion Redeem Processing** - Migrate promotional data with updated references
4. **Relationship Validation** - Ensure all relationships are properly established
5. **Data Consistency Check** - Verify no orphaned records exist

### Integration Points

- **Schema Migration Pipeline** - Executes after primary points transaction migration
- **Related Systems** - Synchronizes escrow, purchase, and promotion systems
- **Data Integrity** - Ensures relational consistency across upgraded tables
- **System Performance** - Optimizes related table structures for new schema

## Dependencies

### Core Framework Dependencies
- **@maas/core/mysql** - Database connectivity and transaction management

### Database Requirements
- **MySQL Portal Database** - Full read/write access to related transaction tables
- **Foreign Key Support** - Proper handling of inter-table relationships
- **Transaction Support** - ACID compliance for multi-table operations

### Schema Dependencies
- **points_transaction_upgrade** - Primary upgraded points transaction table (must exist)
- **escrow_detail/escrow_detail_upgrade** - Escrow detail tables
- **purchase_transaction/purchase_transaction_upgrade** - Purchase transaction tables
- **promotion_redeem/promotion_redeem_upgrade** - Promotion redemption tables
- **escrow** - Parent escrow table for relationship context

## Code Examples

### Complete Schema Upgrade Execution
```javascript
const job = require('./upgrade-new-points-transaction-schema');
await job.fn();
console.log('Related table schema upgrade completed');
```

### Manual Escrow Detail Upgrade
```javascript
async function upgradeEscrowDetails() {
  // Clear existing upgrade data
  await knex('escrow_detail_upgrade').truncate();
  
  // Get all escrow details with parent context
  const escrowDetails = await knex('escrow_detail')
    .leftJoin('escrow', 'escrow.id', '=', 'escrow_detail.escrow_id')
    .orderBy('escrow_detail.id')
    .select('escrow_detail.*');
  
  for (const detail of escrowDetails) {
    let mappedTransactionId = 0;
    
    // Map to upgraded transaction ID
    if (detail.transaction_id && detail.transaction_id > 0) {
      const upgradedTransaction = await knex('points_transaction_upgrade')
        .whereNotIn('user_id', [2000, 2001, 2002, 2100, 2101, 2102, 2103])
        .andWhere('ori_id', '=', detail.transaction_id)
        .first();
      
      if (upgradedTransaction) {
        mappedTransactionId = upgradedTransaction.id;
      }
    }
    
    // Insert upgraded record
    await knex('escrow_detail_upgrade').insert({
      escrow_id: detail.escrow_id,
      activity_type: detail.activity_type,
      fund: detail.fund,
      offer_id: detail.offer_id,
      created_on: detail.created_on,
      modified_on: detail.modified_on,
      transaction_id: mappedTransactionId,
      ori_id: detail.id,
    });
  }
}
```

### Batch Processing with Progress Tracking
```javascript
async function batchUpgradeWithProgress() {
  const batchSize = 100;
  const phases = [
    { name: 'Escrow Details', fn: upgradeEscrowDetailsBatch },
    { name: 'Purchase Transactions', fn: upgradePurchaseTransactionsBatch },
    { name: 'Promotion Redeems', fn: upgradePromotionRedeemsBatch }
  ];
  
  for (const phase of phases) {
    console.log(`Starting ${phase.name} upgrade...`);
    const start = Date.now();
    
    const result = await phase.fn(batchSize);
    
    const end = Date.now();
    console.log(
      `${phase.name} completed: ${result.processed} records, ` +
      `${result.mapped} mapped, ${(end - start) / 1000}s`
    );
  }
}
```

### Relationship Validation
```javascript
async function validateUpgradeRelationships() {
  const validation = {
    escrow_orphans: 0,
    purchase_orphans: 0,
    promotion_orphans: 0,
    mapping_issues: []
  };
  
  // Check for orphaned escrow details
  const orphanedEscrow = await knex('escrow_detail_upgrade')
    .where('transaction_id', '>', 0)
    .whereNotExists(function() {
      this.select('*')
        .from('points_transaction_upgrade')
        .whereRaw('points_transaction_upgrade.id = escrow_detail_upgrade.transaction_id');
    });
  
  validation.escrow_orphans = orphanedEscrow.length;
  
  // Check for orphaned purchase transactions
  const orphanedPurchase = await knex('purchase_transaction_upgrade')
    .whereNotExists(function() {
      this.select('*')
        .from('points_transaction_upgrade')
        .whereRaw('points_transaction_upgrade.id = purchase_transaction_upgrade.point_transaction_id');
    });
  
  validation.purchase_orphans = orphanedPurchase.length;
  
  // Check for orphaned promotion redeems
  const orphanedPromotion = await knex('promotion_redeem_upgrade')
    .whereNotExists(function() {
      this.select('*')
        .from('points_transaction_upgrade')
        .whereRaw('points_transaction_upgrade.id = promotion_redeem_upgrade.point_transaction_id');
    });
  
  validation.promotion_orphans = orphanedPromotion.length;
  
  return validation;
}
```

### Transaction ID Mapping Verification
```javascript
async function verifyTransactionMapping() {
  const mappingReport = {
    total_legacy_records: 0,
    successfully_mapped: 0,
    unmapped_records: [],
    excluded_agencies: 0
  };
  
  // Verify escrow detail mappings
  const escrowDetails = await knex('escrow_detail')
    .where('transaction_id', '>', 0);
  
  mappingReport.total_legacy_records = escrowDetails.length;
  
  for (const detail of escrowDetails) {
    const upgraded = await knex('points_transaction_upgrade')
      .where('ori_id', '=', detail.transaction_id)
      .first();
    
    if (upgraded) {
      if ([2000, 2001, 2002, 2100, 2101, 2102, 2103].includes(upgraded.user_id)) {
        mappingReport.excluded_agencies++;
      } else {
        mappingReport.successfully_mapped++;
      }
    } else {
      mappingReport.unmapped_records.push({
        escrow_detail_id: detail.id,
        legacy_transaction_id: detail.transaction_id
      });
    }
  }
  
  return mappingReport;
}
```

### Rollback Capability
```javascript
async function rollbackSchemaUpgrade() {
  console.log('Rolling back schema upgrade...');
  
  try {
    // Truncate all upgrade tables
    await Promise.all([
      knex('escrow_detail_upgrade').truncate(),
      knex('purchase_transaction_upgrade').truncate(),
      knex('promotion_redeem_upgrade').truncate()
    ]);
    
    console.log('Schema upgrade rollback completed successfully');
    return { status: 'SUCCESS', rollback_time: new Date().toISOString() };
    
  } catch (error) {
    console.error('Rollback failed:', error.message);
    throw error;
  }
}
```

### Comprehensive Upgrade with Monitoring
```javascript
async function monitoredSchemaUpgrade() {
  const start = Date.now();
  const metrics = {
    start_time: new Date().toISOString(),
    phases: {},
    total_records_processed: 0,
    relationship_mappings: 0,
    excluded_agencies: 0
  };
  
  try {
    // Phase 1: Escrow Details
    const escrowStart = Date.now();
    await upgradeEscrowDetails();
    const escrowCount = await knex('escrow_detail_upgrade').count('id as count').first();
    metrics.phases.escrow_details = {
      duration_ms: Date.now() - escrowStart,
      records_processed: escrowCount.count
    };
    
    // Phase 2: Purchase Transactions
    const purchaseStart = Date.now();
    await upgradePurchaseTransactions();
    const purchaseCount = await knex('purchase_transaction_upgrade').count('id as count').first();
    metrics.phases.purchase_transactions = {
      duration_ms: Date.now() - purchaseStart,
      records_processed: purchaseCount.count
    };
    
    // Phase 3: Promotion Redeems
    const promotionStart = Date.now();
    await upgradePromotionRedeems();
    const promotionCount = await knex('promotion_redeem_upgrade').count('id as count').first();
    metrics.phases.promotion_redeems = {
      duration_ms: Date.now() - promotionStart,
      records_processed: promotionCount.count
    };
    
    metrics.total_records_processed = 
      escrowCount.count + purchaseCount.count + promotionCount.count;
    
    // Validation
    const validation = await validateUpgradeRelationships();
    metrics.validation = validation;
    
    const end = Date.now();
    metrics.total_duration_ms = end - start;
    metrics.end_time = new Date().toISOString();
    metrics.status = 'SUCCESS';
    
    console.log('Schema upgrade completed:', metrics);
    return metrics;
    
  } catch (error) {
    metrics.status = 'FAILED';
    metrics.error = error.message;
    metrics.total_duration_ms = Date.now() - start;
    
    console.error('Schema upgrade failed:', metrics);
    throw error;
  }
}
```

This schema upgrade job ensures that all related transaction tables are properly synchronized with the new points transaction schema, maintaining data integrity and relationship consistency across the entire transaction ecosystem while excluding system agency accounts from user-focused processing.