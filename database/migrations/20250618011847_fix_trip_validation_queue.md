# Migration Documentation

## 📋 Migration Overview
- **Purpose:** Fix trip validation queue run_at field data type to support larger timestamps
- **Date:** 2025-06-18 01:18:47
- **Ticket:** N/A
- **Risk Level:** Low

## 🔧 Schema Changes
```sql
ALTER TABLE trip_validation_queue MODIFY COLUMN run_at BIGINT NOT NULL COMMENT 'The time at which the validation should run';
```

## 📝 Changes Summary
| Operation | Table/Collection | Field/Index | Description |
|-----------|-----------------|-------------|-------------|
| MODIFY | trip_validation_queue | run_at | Change data type to BIGINT for larger timestamps |

## ⬆️ Up Migration
- Modifies run_at column from INT to BIGINT
- Maintains NOT NULL constraint
- Supports larger timestamp values for scheduling
- Updates column comment for clarity

## ⬇️ Down Migration
- No rollback implemented (empty down function)
- Change is considered forward-compatible
- BIGINT can safely store smaller values

## ⚠️ Important Notes
- **Data Type Expansion:** INT to BIGINT for timestamp storage
- No data loss expected during migration
- Supports Unix timestamps beyond 2038 limit
- Improves long-term scheduling capabilities

## 🏷️ Tags
**Keywords:** trip, validation, queue, timestamp, bigint, scheduling
**Category:** #migration #database #schema #trip #validation #timestamp