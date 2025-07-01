# Migration Documentation: 20231117161348_fix_incentive_type.js

## 📋 Migration Overview
- **Purpose:** Fix incentive notification queue by adding incentive_type field and modifying type field
- **Date:** 2023-11-17 16:13:48
- **Ticket:** N/A (descriptive filename)
- **Risk Level:** Medium

## 🔧 Schema Changes
```sql
ALTER TABLE incentive_notify_queue 
MODIFY COLUMN type VARCHAR(50) NOT NULL DEFAULT '' COMMENT '發送類型';

ALTER TABLE incentive_notify_queue 
ADD COLUMN incentive_type VARCHAR(50) NOT NULL DEFAULT '' COMMENT '發送類型' AFTER type;
```

## 📝 Changes Summary
| Operation | Table/Collection | Field/Index | Description |
|-----------|-----------------|-------------|-------------|
| MODIFY | incentive_notify_queue | type | Updates type field constraints |
| ADD | incentive_notify_queue | incentive_type | New field for specific incentive categorization |

## ⬆️ Up Migration
- Modifies existing type column to ensure NOT NULL constraint with default
- Adds new incentive_type column for granular incentive categorization
- Positioned after type column for logical field ordering
- Includes Chinese comments for field descriptions

## ⬇️ Down Migration
- Removes incentive_type column
- Reverts type field changes
- Existing type field functionality preserved

## ⚠️ Important Notes
- Enhances incentive notification system with better categorization
- Both fields use Chinese comments indicating multi-language support
- Backward compatible with existing notification queue processing
- Improves incentive tracking and reporting capabilities

## 🏷️ Tags
**Keywords:** incentive-notifications type-categorization queue-processing field-modification
**Category:** #migration #database #schema #incentives #notifications

---
Note: Focus on what changes and why, not the detailed SQL.