# Migration Documentation: 20240701072514_update-block-users.js

## 📋 Migration Overview
- **Purpose:** Update block_users table to change reason field from integer to text
- **Date:** 2024-07-01 07:25:14
- **Ticket:** N/A
- **Risk Level:** Medium

## 🔧 Schema Changes
```sql
-- Up migration
ALTER TABLE block_users DROP COLUMN block_type, DROP COLUMN reason;
ALTER TABLE block_users ADD COLUMN block_type INT NOT NULL DEFAULT 0 AFTER user_id 
  COMMENT 'default 0 is block user can not buy coins. 1 is block user can not access APIs.';
ALTER TABLE block_users ADD COLUMN reason TEXT NOT NULL DEFAULT '' AFTER block_type
  COMMENT 'reserved for the reason why the user been blocked';

-- Down migration  
ALTER TABLE block_users DROP COLUMN block_type, DROP COLUMN reason;
ALTER TABLE block_users ADD COLUMN block_type INT NOT NULL DEFAULT '0' AFTER user_id
  COMMENT 'reserved for the type of the function to block';
ALTER TABLE block_users ADD COLUMN reason INT NOT NULL DEFAULT '0' AFTER block_type
  COMMENT 'reserved for the reason why the user been blocked';
```

## 📝 Changes Summary
| Operation | Table/Collection | Field/Index | Description |
|-----------|-----------------|-------------|-------------|
| ALTER | block_users | block_type | Updated comment and default value |
| ALTER | block_users | reason | Changed from INT to TEXT for detailed reasons |

## ⬆️ Up Migration
- Drops existing block_type and reason columns
- Recreates block_type as integer with updated comment explaining block types
- Recreates reason as TEXT field to allow detailed blocking explanations
- Maintains NOT NULL constraints with appropriate defaults

## ⬇️ Down Migration
- Reverts reason field back to integer type
- Restores original comments for both fields
- Maintains data structure compatibility

## ⚠️ Important Notes
- **Data Loss Risk:** Existing text reasons will be lost during rollback
- Block type meanings: 0 = cannot buy coins, 1 = cannot access APIs
- Reason field change from integer to text enables detailed explanations
- Migration involves column recreation, not simple alteration

## 🏷️ Tags
**Keywords:** user-blocking access-control data-types schema-modification
**Category:** #migration #database #schema #user-management #blocking