# Migration Documentation: add_coins_history_index

## 📋 Migration Overview
- **Purpose:** Adds performance indexes to transaction-related tables
- **Date:** 2022-10-18 13:30:00
- **Ticket:** N/A
- **Risk Level:** Low

## 🔧 Schema Changes
```sql
ALTER TABLE points_transaction ADD INDEX coins_history_idx_1 (user_id, created_on, activity_type, id);
ALTER TABLE redeem_transaction ADD INDEX transaction_id_idx_1 (transaction_id);
ALTER TABLE bytemark_orders ADD INDEX order_uuid_idx_1 (order_uuid);
```

## 📝 Changes Summary
| Operation | Table/Collection | Field/Index | Description |
|-----------|-----------------|-------------|-------------|
| CREATE INDEX | points_transaction | coins_history_idx_1 | Optimizes coins history queries by user and time |
| CREATE INDEX | redeem_transaction | transaction_id_idx_1 | Improves redemption transaction lookups |
| CREATE INDEX | bytemark_orders | order_uuid_idx_1 | Speeds up order UUID searches |

## ⬆️ Up Migration
- Adds composite index on points_transaction for coins history queries
- Creates index on redeem_transaction for transaction ID lookups
- Adds index on bytemark_orders for UUID-based searches
- Improves query performance for frequently accessed data patterns

## ⬇️ Down Migration
- Removes all three created indexes
- Query performance will revert to pre-optimization levels
- No data loss, only performance impact

## ⚠️ Important Notes
- Pure performance optimization migration
- No schema changes, only index additions
- Targets commonly queried patterns in transaction tables
- Safe to run with minimal risk

## 🏷️ Tags
**Keywords:** index, performance, optimization, coins, transaction, history
**Category:** #migration #database #performance #index #transaction