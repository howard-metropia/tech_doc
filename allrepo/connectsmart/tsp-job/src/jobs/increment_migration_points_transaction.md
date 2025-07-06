# increment_migration_points_transaction.js - Incremental Points Transaction Migration Job

## Quick Summary

The `increment_migration_points_transaction.js` job is a sophisticated data migration system designed to incrementally migrate points transaction records from the legacy `points_transaction` table to the new `points_transaction_upgrade` schema. This job implements a comprehensive migration strategy that handles complex business logic including balance calculations, agency account management, and related data migration for escrow details, promotion redeems, and purchase transactions. The system ensures data integrity through proper balance tracking and synchronized wallet updates while supporting incremental processing of unmigrated records.

## Technical Analysis

### Core Architecture

The job implements a multi-phase incremental migration approach with the following key components:

1. **Incremental Record Processing** - Identifies and processes only unmigrated records
2. **Balance Synchronization** - Maintains accurate running balances across migrations
3. **Agency Account Management** - Handles complex payer/payee relationships
4. **Related Data Migration** - Cascades migration to dependent tables
5. **Wallet Synchronization** - Updates user wallet balances post-migration

### Migration Query Logic

#### Incremental Record Selection
```javascript
const sql1 = `select * from points_transaction pt 
where not exists (select 1 from points_transaction_upgrade ptu where ptu.ori_id = pt.id) and 
user_id not in (2000, 2001, 2002, 2100, 2101, 2102);`;
```

This query efficiently identifies unmigrated records while excluding system agency accounts from processing, enabling incremental migration runs without duplicate processing.

### Balance Calculation System

#### Primary Transaction Processing
```javascript
const balance1 = await syncBalance(element.user_id);
const row = {
  user_id: element.user_id,
  activity_type: element.activity_type,
  points: Number(element.points),
  balance: balance1 + Number(element.points),
  note: element.note,
  created_on: element.created_on,
  payer: getAgencyPayerAccount(element.activity_type, element.user_id),
  payee: getAgencyPayeeAccount(element.activity_type, element.user_id),
  ori_id: element.id,
};
```

The system calculates accurate running balances by synchronizing current wallet state before applying new transactions.

#### Paired Transaction Generation
```javascript
const balance2 = await syncBalance(bUserId);
const row1 = {
  user_id: bUserId,
  activity_type: element.activity_type,
  points: 0 - Number(element.points),
  balance: balance2 - Number(element.points),
  note: element.note,
  created_on: element.created_on,
  payer: getAgencyPayerAccount(element.activity_type, element.user_id),
  payee: getAgencyPayeeAccount(element.activity_type, element.user_id),
  ori_id: 0,
  ref_transaction_id: _id,
};
```

Each transaction generates a corresponding paired transaction to maintain double-entry accounting principles with proper agency account handling.

### Agency Account Management

The job implements sophisticated agency account logic through dedicated functions:

#### Payer Account Logic
```javascript
function getAgencyPayerAccount(activityType, userId) {
  switch (activityType) {
    case 1: return 0;
    case 2: return 2100;
    case 3: return userId;
    case 4: return 2000;
    case 5: return 2100;
    case 6: return 2002;
    case 7: return 2001;
    case 8: return userId;
    case 9: return userId;
    case 10: return 2001;
    case 11: return userId;
    case 12: return userId;
    default: return 0;
  }
}
```

#### Payee Account Logic
```javascript
function getAgencyPayeeAccount(activityType, userId) {
  switch (activityType) {
    case 1: return 0;
    case 2: return userId;
    case 3: return 2102;
    case 4: return userId;
    case 5: return userId;
    case 6: return userId;
    case 7: return userId;
    case 8: return 2000;
    case 9: return 2001;
    case 10: return userId;
    case 11: return 2101;
    case 12: return 2000;
    default: return 0;
  }
}
```

These functions define complex business rules for different activity types, ensuring proper fund flow between users and agency accounts.

### Related Data Migration

#### Escrow Detail Migration
```javascript
async function migrateEscrowDetail(from, to) {
  const sql2 = `select * from escrow_detail where transaction_id = ?`;
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
      ori_id: element.id,
    };
    await knex('escrow_detail_upgrade').insert(row);
  }
  return rows2.length;
}
```

### Wallet Synchronization System

#### Balance Synchronization Logic
```javascript
async function syncBalance(userId) {
  const now = tz.utc().format('YYYY-MM-DD HH:mm:ss');
  const balance = (
    await knex('points_transaction_upgrade')
      .where({ user_id: userId })
      .sum('points as balance')
      .first()
  ).balance;
  
  await knex('user_wallet')
    .insert({
      user_id: userId,
      balance,
      auto_refill: 'F',
      modified_on: now,
    })
    .onConflict('user_id')
    .merge({
      balance,
      modified_on: now,
    });
    
  return Number(balance);
}
```

This system ensures wallet balances remain synchronized with transaction history using upsert operations for efficient updates.

## Usage/Integration

### Execution Context

This job is designed for incremental migration scenarios where points transactions need to be migrated in batches while maintaining system availability. The job can be executed multiple times safely, processing only unmigrated records each time.

### Migration Workflow

1. **Record Identification** - Query unmigrated transactions excluding agency accounts
2. **Balance Synchronization** - Calculate current balances before processing
3. **Transaction Pair Creation** - Generate primary and paired transactions
4. **Related Data Migration** - Migrate associated escrow, promotion, and purchase data
5. **Reference Updates** - Establish proper cross-references between paired transactions
6. **Wallet Updates** - Synchronize user wallet balances
7. **Performance Reporting** - Log execution metrics and migration counts

### Integration Points

- **Migration Pipeline** - Part of incremental migration strategy
- **Balance Management** - Integrates with wallet synchronization systems
- **Related Systems** - Cascades migration to escrow, promotion, and purchase systems
- **Monitoring** - Provides detailed execution metrics and progress tracking

## Dependencies

### Core Framework Dependencies
- **@maas/core/mysql** - Database connectivity and transaction management
- **@maas/core/log** - Structured logging infrastructure
- **moment-timezone** - Timezone-aware timestamp generation

### Database Requirements
- **MySQL Portal Database** - Write access to multiple transaction tables
- **Transaction Support** - ACID compliance for multi-table operations
- **Index Optimization** - Proper indexing on `ori_id`, `user_id`, and foreign key fields

### Schema Dependencies
- **points_transaction** - Source legacy transaction table
- **points_transaction_upgrade** - Target migration table
- **escrow_detail/escrow_detail_upgrade** - Related escrow data tables
- **promotion_redeem/promotion_redeem_upgrade** - Related promotion tables
- **purchase_transaction/purchase_transaction_upgrade** - Related purchase tables
- **user_wallet** - User balance tracking table

## Code Examples

### Manual Incremental Migration
```javascript
async function runIncrementalMigration() {
  const start = Date.now();
  let migratedCount = 0;
  
  try {
    const unmigrated = await knex.raw(`
      SELECT * FROM points_transaction pt 
      WHERE NOT EXISTS (
        SELECT 1 FROM points_transaction_upgrade ptu 
        WHERE ptu.ori_id = pt.id
      ) AND user_id NOT IN (2000, 2001, 2002, 2100, 2101, 2102)
      LIMIT 1000
    `);
    
    const [records] = unmigrated;
    console.log(`Processing ${records.length} unmigrated records`);
    
    for (const record of records) {
      await migrateTransactionRecord(record);
      migratedCount++;
    }
    
    const end = Date.now();
    console.log(`Migrated ${migratedCount} records in ${(end - start) / 1000} seconds`);
    
  } catch (error) {
    console.error(`Migration failed: ${error.message}`);
    throw error;
  }
}
```

### Single Transaction Migration
```javascript
async function migrateTransactionRecord(transaction) {
  const userId = transaction.user_id;
  const currentBalance = await syncBalance(userId);
  
  // Create primary transaction record
  const primaryRecord = {
    user_id: userId,
    activity_type: transaction.activity_type,
    points: Number(transaction.points),
    balance: currentBalance + Number(transaction.points),
    note: transaction.note,
    created_on: transaction.created_on,
    payer: getAgencyPayerAccount(transaction.activity_type, userId),
    payee: getAgencyPayeeAccount(transaction.activity_type, userId),
    ori_id: transaction.id,
  };
  
  const [primaryId] = await knex('points_transaction_upgrade').insert(primaryRecord);
  
  // Determine paired account
  const pairedUserId = getAgencyPayerAccount(transaction.activity_type, userId) !== userId
    ? getAgencyPayerAccount(transaction.activity_type, userId)
    : getAgencyPayeeAccount(transaction.activity_type, userId);
  
  const pairedBalance = await syncBalance(pairedUserId);
  
  // Create paired transaction record
  const pairedRecord = {
    user_id: pairedUserId,
    activity_type: transaction.activity_type,
    points: 0 - Number(transaction.points),
    balance: pairedBalance - Number(transaction.points),
    note: transaction.note,
    created_on: transaction.created_on,
    payer: getAgencyPayerAccount(transaction.activity_type, userId),
    payee: getAgencyPayeeAccount(transaction.activity_type, userId),
    ori_id: 0,
    ref_transaction_id: primaryId,
  };
  
  const [pairedId] = await knex('points_transaction_upgrade').insert(pairedRecord);
  
  // Update primary record with reference
  await knex('points_transaction_upgrade')
    .where({ id: primaryId })
    .update({ ref_transaction_id: pairedId });
  
  // Migrate related data
  await Promise.all([
    migrateEscrowDetail(transaction.id, primaryId),
    migratePromotionRedeem(transaction.id, primaryId),
    migratiePurchaseTransaction(transaction.id, primaryId)
  ]);
  
  return { primaryId, pairedId };
}
```

### Balance Verification System
```javascript
async function verifyBalanceIntegrity(userId) {
  // Calculate balance from transactions
  const transactionBalance = await knex('points_transaction_upgrade')
    .where({ user_id: userId })
    .sum('points as total')
    .first();
  
  // Get wallet balance
  const walletBalance = await knex('user_wallet')
    .where({ user_id: userId })
    .select('balance')
    .first();
  
  const calculatedBalance = Number(transactionBalance.total || 0);
  const recordedBalance = Number(walletBalance?.balance || 0);
  
  if (calculatedBalance !== recordedBalance) {
    throw new Error(
      `Balance mismatch for user ${userId}: ` +
      `calculated=${calculatedBalance}, recorded=${recordedBalance}`
    );
  }
  
  return {
    user_id: userId,
    balance: calculatedBalance,
    verified: true
  };
}
```

### Batch Migration with Progress Tracking
```javascript
async function batchMigrationWithProgress(batchSize = 100) {
  let totalMigrated = 0;
  let hasMore = true;
  
  while (hasMore) {
    const unmigrated = await knex.raw(`
      SELECT * FROM points_transaction pt 
      WHERE NOT EXISTS (
        SELECT 1 FROM points_transaction_upgrade ptu 
        WHERE ptu.ori_id = pt.id
      ) AND user_id NOT IN (2000, 2001, 2002, 2100, 2101, 2102)
      ORDER BY pt.id
      LIMIT ?
    `, [batchSize]);
    
    const [records] = unmigrated;
    
    if (records.length === 0) {
      hasMore = false;
      break;
    }
    
    console.log(`Processing batch of ${records.length} records...`);
    
    for (const record of records) {
      try {
        await migrateTransactionRecord(record);
        totalMigrated++;
        
        if (totalMigrated % 50 === 0) {
          console.log(`Progress: ${totalMigrated} records migrated`);
        }
      } catch (error) {
        console.error(`Failed to migrate record ${record.id}: ${error.message}`);
        throw error;
      }
    }
  }
  
  console.log(`Migration completed: ${totalMigrated} total records migrated`);
  return totalMigrated;
}
```

This incremental migration job provides a robust foundation for migrating points transaction data while maintaining system integrity and supporting continuous operation during migration processes.