# migration-point-transaction.js - Complete Points Transaction Migration Job

## Quick Summary

The `migration-point-transaction.js` job is a comprehensive data migration system that performs a complete transformation of the points transaction schema from legacy single-entry to a modern double-entry accounting system. This job rebuilds the entire points transaction structure by creating paired transaction records, managing agency account balances, and establishing proper payer/payee relationships across all activity types. The job implements sophisticated balance tracking, activity type restoration logic, and creates a completely new table structure optimized for the upgraded points system architecture.

## Technical Analysis

### Core Architecture

The job implements a complete schema transformation approach with the following key phases:

1. **Data Extraction and Analysis** - Retrieves all legacy transactions with escrow type analysis
2. **Agency Balance Management** - Tracks running balances for all agency accounts
3. **Transaction Pair Generation** - Creates double-entry records for each transaction
4. **Activity Type Restoration** - Restores proper activity types from escrow data
5. **Table Recreation** - Drops and recreates the upgrade table with optimized schema
6. **Bulk Data Insertion** - Performs efficient batch insertion of all transformed records

### Legacy Data Extraction Query

```javascript
const SQL = `
SELECT pt.*, ed.activity_type as escrow_type 
from points_transaction as pt 
left join escrow_detail as ed on pt.id = ed.transaction_id 
group by pt.id
order by pt.id;`;
```

This complex query joins transaction data with escrow details to capture additional context needed for proper activity type restoration and migration logic.

### Agency Balance Tracking System

#### Agency Account Initialization
```javascript
const agencyBalance = [
  { agency_id: 2000, balance: 0 },
  { agency_id: 2001, balance: 0 },
  { agency_id: 2002, balance: 0 },
  { agency_id: 2100, balance: 0 },
  { agency_id: 2101, balance: 0 },
  { agency_id: 2102, balance: 0 },
  { agency_id: 2103, balance: 0 },
];
```

The system maintains running balances for seven different agency accounts, each representing different business entities within the platform ecosystem.

### Transaction Processing Logic

#### Referenced Transaction Handling
```javascript
if (element.ref_transaction_id !== 0) {
  let oBalance = element.balance;
  const activityType = element.activity_type;
  agencyBalance.map((agency) => {
    if (agency.agency_id === element.user_id) {
      oBalance = agency.balance + Number(element.points);
      agency.balance = oBalance;
    }
    return agency;
  });
  // Create primary transaction record...
}
```

For transactions with existing reference relationships, the job maintains the original balance calculation logic while updating agency balance tracking.

#### Standalone Transaction Processing
```javascript
else {
  let bUserId = element.user_id;
  let bBalance = 0;
  let activityType = element.activity_type;

  if (element.activity_type === 8) {
    if (
      restoreActivityType(element.escrow_type) === 9 ||
      restoreActivityType(element.escrow_type) === 10
    ) {
      activityType = restoreActivityType(element.escrow_type);
    }
  }
  // Create transaction pairs...
}
```

Standalone transactions undergo activity type restoration and generate paired transactions with proper payer/payee relationships.

### Activity Type Restoration Logic

```javascript
function restoreActivityType(escrowType) {
  const type9 = [1, 2, 3, 4, 5, 12, 13, 24];
  const type10 = [6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25];

  if (type9.indexOf(Number(escrowType)) !== -1) {
    return 9;
  } else if (type10.indexOf(Number(escrowType)) !== -1) {
    return 10;
  } else {
    return 0;
  }
}
```

This function maps legacy escrow types to standardized activity types, ensuring consistent categorization across the migrated data.

### Table Recreation Process

#### Dynamic Table Creation
```javascript
const createTableSQL = `CREATE TABLE points_transaction_upgrade (
  id int(11) NOT NULL AUTO_INCREMENT,
  user_id int(11) NOT NULL,
  activity_type int(11) NOT NULL,
  points decimal(10,2) NOT NULL,
  balance decimal(10,2) NOT NULL,
  note varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  created_on datetime NOT NULL,
  payer int(11) NOT NULL DEFAULT '0' COMMENT 'who pay the coins',
  payee int(11) NOT NULL DEFAULT '0' COMMENT 'who receive the coins',
  ori_id int(11) NOT NULL DEFAULT '0',
  ref_transaction_id int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (id),
  KEY activity_type__idx (activity_type),
  KEY ori_id__idx (ori_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;`;
```

The new schema includes enhanced fields for payer/payee tracking, reference transaction relationships, and optimized indexing for performance.

### Bulk Data Insertion Strategy

```javascript
let insertValues = '';
transArray.forEach((row) => {
  insertValues =
    insertValues +
    `( ${row.id}, ${row.user_id}, ${row.activity_type}, ${row.points}, ${row.balance}, '${row.note}', '${row.created_on}', ${row.payer}, ${row.payee}, ${row.ori_id}, ${row.ref_transaction_id}),`;
});

insertValues = insertValues.slice(0, -1);
const insertSql = 'INSERT INTO points_transaction_upgrade VALUES ' + insertValues + ';';
await knex.raw(insertSql);
```

The job constructs a single massive INSERT statement for optimal performance during bulk data insertion.

## Usage/Integration

### Execution Context

This job is designed for complete system migration scenarios where the entire points transaction system needs to be upgraded from single-entry to double-entry accounting. The job should be executed during planned maintenance windows due to its comprehensive table recreation process.

### Migration Workflow

1. **Data Extraction** - Retrieve all legacy transactions with escrow context
2. **Transaction Processing** - Transform each record into double-entry format
3. **Balance Calculation** - Maintain running balances across agency accounts
4. **Activity Type Restoration** - Apply business rules for proper categorization
5. **Table Recreation** - Drop existing upgrade table and create optimized schema
6. **Bulk Insertion** - Insert all transformed records in single operation
7. **Performance Reporting** - Log execution metrics and record counts

### Integration Points

- **Complete Migration Pipeline** - Executes as primary migration job
- **Schema Transformation** - Handles fundamental database structure changes
- **Agency Account Management** - Integrates with multi-tenant account systems
- **Performance Monitoring** - Provides detailed execution metrics

## Dependencies

### Core Framework Dependencies
- **@maas/core/mysql** - Database connectivity and raw SQL execution
- **@maas/core/log** - Structured logging infrastructure

### Database Requirements
- **MySQL Portal Database** - Full DDL and DML privileges for table operations
- **Transaction Support** - ACID compliance for schema changes and data insertion
- **Memory Resources** - Sufficient memory for large data set processing
- **Storage Space** - Additional space for duplicate table during migration

### Schema Dependencies
- **points_transaction** - Source legacy transaction table
- **escrow_detail** - Reference table for activity type restoration
- **points_transaction_upgrade** - Target table (recreated during execution)

## Code Examples

### Complete Migration Execution
```javascript
const job = require('./migration-point-transaction');
await job.fn();
console.log('Complete points transaction migration finished');
```

### Manual Activity Type Restoration
```javascript
function customActivityTypeRestore(escrowType, originalActivityType) {
  // Custom logic for activity type restoration
  if (originalActivityType === 8) {
    const type9Escrows = [1, 2, 3, 4, 5, 12, 13, 24];
    const type10Escrows = [6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25];
    
    if (type9Escrows.includes(Number(escrowType))) {
      return 9;
    } else if (type10Escrows.includes(Number(escrowType))) {
      return 10;
    }
  }
  
  return originalActivityType;
}
```

### Agency Balance Tracking
```javascript
class AgencyBalanceTracker {
  constructor() {
    this.balances = new Map([
      [2000, 0], [2001, 0], [2002, 0], [2100, 0], 
      [2101, 0], [2102, 0], [2103, 0]
    ]);
  }
  
  updateBalance(agencyId, points) {
    const currentBalance = this.balances.get(agencyId) || 0;
    const newBalance = currentBalance + Number(points);
    this.balances.set(agencyId, newBalance);
    return newBalance;
  }
  
  getBalance(agencyId) {
    return this.balances.get(agencyId) || 0;
  }
  
  getAllBalances() {
    return Object.fromEntries(this.balances);
  }
}
```

### Transaction Pair Generator
```javascript
function createTransactionPair(originalTransaction, activityType, agencyTracker) {
  const userId = originalTransaction.user_id;
  const points = Number(originalTransaction.points);
  
  // Determine payer and payee accounts
  const payer = getAgencyPayerAccount(activityType, userId);
  const payee = getAgencyPayeeAccount(activityType, userId);
  
  // Determine paired account
  const pairedUserId = (payer !== userId) ? payer : payee;
  
  // Update balances
  const userBalance = agencyTracker.updateBalance(userId, points);
  const pairedBalance = agencyTracker.updateBalance(pairedUserId, -points);
  
  // Create primary transaction
  const primaryTransaction = {
    user_id: userId,
    activity_type: activityType,
    points: points,
    balance: userBalance,
    note: originalTransaction.note,
    created_on: originalTransaction.created_on,
    payer: payer,
    payee: payee,
    ori_id: originalTransaction.id,
  };
  
  // Create paired transaction
  const pairedTransaction = {
    user_id: pairedUserId,
    activity_type: activityType,
    points: -points,
    balance: pairedBalance,
    note: originalTransaction.note,
    created_on: originalTransaction.created_on,
    payer: payer,
    payee: payee,
    ori_id: originalTransaction.id,
  };
  
  return { primaryTransaction, pairedTransaction };
}
```

### Migration Validation
```javascript
async function validateMigration() {
  const originalCount = await knex('points_transaction').count('id as count').first();
  const upgradedCount = await knex('points_transaction_upgrade').count('id as count').first();
  
  console.log(`Original records: ${originalCount.count}`);
  console.log(`Upgraded records: ${upgradedCount.count}`);
  
  // Each original record should generate 2 upgraded records (primary + paired)
  const expectedCount = originalCount.count * 2;
  
  if (upgradedCount.count !== expectedCount) {
    throw new Error(
      `Migration validation failed: expected ${expectedCount} records, got ${upgradedCount.count}`
    );
  }
  
  // Validate balance integrity
  const balanceCheck = await knex('points_transaction_upgrade')
    .select('user_id')
    .sum('points as total_points')
    .groupBy('user_id')
    .having('total_points', '!=', 0);
  
  if (balanceCheck.length > 0) {
    console.warn('Balance discrepancies found for users:', balanceCheck.map(b => b.user_id));
  }
  
  return {
    original_count: originalCount.count,
    upgraded_count: upgradedCount.count,
    validation_passed: upgradedCount.count === expectedCount,
    balance_issues: balanceCheck.length
  };
}
```

### Performance Monitoring
```javascript
async function executeMigrationWithMonitoring() {
  const start = Date.now();
  const metrics = {
    start_time: new Date().toISOString(),
    records_processed: 0,
    agency_balances: {},
    execution_phases: {}
  };
  
  try {
    // Phase 1: Data extraction
    const phaseStart = Date.now();
    const originalRecords = await extractLegacyData();
    metrics.execution_phases.extraction = Date.now() - phaseStart;
    metrics.records_processed = originalRecords.length;
    
    // Phase 2: Transaction processing
    const processStart = Date.now();
    const transformedRecords = await processTransactions(originalRecords);
    metrics.execution_phases.processing = Date.now() - processStart;
    
    // Phase 3: Table recreation
    const recreateStart = Date.now();
    await recreateUpgradeTable();
    metrics.execution_phases.table_recreation = Date.now() - recreateStart;
    
    // Phase 4: Bulk insertion
    const insertStart = Date.now();
    await bulkInsertRecords(transformedRecords);
    metrics.execution_phases.bulk_insertion = Date.now() - insertStart;
    
    const end = Date.now();
    metrics.total_execution_time_ms = end - start;
    metrics.end_time = new Date().toISOString();
    metrics.status = 'SUCCESS';
    
    console.log('Migration completed successfully:', metrics);
    return metrics;
    
  } catch (error) {
    metrics.status = 'FAILED';
    metrics.error = error.message;
    metrics.total_execution_time_ms = Date.now() - start;
    
    console.error('Migration failed:', metrics);
    throw error;
  }
}
```

This comprehensive migration job serves as the foundation for transforming the entire points transaction system from a legacy single-entry model to a modern double-entry accounting system with enhanced tracking and agency account management capabilities.