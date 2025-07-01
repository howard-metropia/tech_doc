# Migration Documentation

## 📋 Migration Overview
- **Purpose:** Fix enterprise email unique constraints by removing email indexes
- **Date:** 2024-01-02 12:07:04
- **Ticket:** N/A
- **Risk Level:** Medium

## 🔧 Schema Changes
```sql
ALTER TABLE enterprise_blocks DROP INDEX enterprise_blocks_email_unique;
ALTER TABLE enterprise_invites DROP INDEX enterprise_invites_email_unique;
```

## 📝 Changes Summary
| Operation | Table/Collection | Field/Index | Description |
|-----------|-----------------|-------------|-------------|
| DROP INDEX | enterprise_blocks | enterprise_blocks_email_unique | Removes email uniqueness constraint |
| DROP INDEX | enterprise_invites | enterprise_invites_email_unique | Removes email uniqueness constraint |

## ⬆️ Up Migration
- Removes unique email constraints from enterprise_blocks table
- Removes unique email constraints from enterprise_invites table
- Allows duplicate emails across enterprise systems
- Includes error handling with logging for failed index drops

## ⬇️ Down Migration
- Restores unique email constraints to enterprise_blocks table
- Restores unique email constraints to enterprise_invites table
- May fail if duplicate emails exist in the data

## ⚠️ Important Notes
- **Constraint Change:** Allows duplicate emails in enterprise systems
- Includes comprehensive error handling and logging
- Rollback may fail if data contains duplicate emails
- Consider data cleanup before applying rollback

## 🏷️ Tags
**Keywords:** enterprise, email, unique, constraint, index, fix
**Category:** #migration #database #schema #enterprise #constraint #email