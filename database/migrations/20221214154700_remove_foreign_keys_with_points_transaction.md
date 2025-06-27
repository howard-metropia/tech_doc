# Migration Documentation: remove_foreign_keys_with_points_transaction

## 📋 Migration Overview
- **Purpose:** Removes foreign key constraints and creates upgraded transaction tables
- **Date:** 2022-12-14 15:47:00
- **Ticket:** N/A
- **Risk Level:** High

## 🔧 Schema Changes
```sql
-- Remove foreign keys
ALTER TABLE purchase_transaction DROP FOREIGN KEY purchase_transaction_ibfk_1;
ALTER TABLE promotion_redeem DROP FOREIGN KEY promotion_redeem_ibfk_2;

-- Add reference field
ALTER TABLE points_transaction_upgrade ADD ref_transaction_id INT(11) NOT NULL DEFAULT 0;

-- Create upgrade tables
CREATE TABLE escrow_detail_upgrade (...);
CREATE TABLE promotion_redeem_upgrade (...);
CREATE TABLE purchase_transaction_upgrade (...);
```

## 📝 Changes Summary
| Operation | Table/Collection | Field/Index | Description |
|-----------|-----------------|-------------|-------------|
| DROP FK | purchase_transaction | purchase_transaction_ibfk_1 | Removes foreign key constraint |
| DROP FK | promotion_redeem | promotion_redeem_ibfk_2 | Removes foreign key constraint |
| ADD | points_transaction_upgrade | ref_transaction_id | Cross reference for double ledger |
| CREATE TABLE | escrow_detail_upgrade | - | Upgraded escrow detail tracking |
| CREATE TABLE | promotion_redeem_upgrade | - | Upgraded promotion redemption |
| CREATE TABLE | purchase_transaction_upgrade | - | Upgraded purchase transactions |

## ⬆️ Up Migration
- Removes foreign key constraints for transaction flexibility
- Creates upgrade versions of transaction tables
- Adds cross-reference field for double ledger system
- Includes migration tracking with ori_id fields

## ⬇️ Down Migration
- Drops all upgrade tables
- Removes ref_transaction_id field
- Note: Foreign key constraints cannot be automatically restored

## ⚠️ Important Notes
- High risk migration affecting payment and transaction integrity
- Foreign key restoration requires manual intervention
- Creates parallel "upgrade" tables for migration purposes
- Critical for payment system refactoring

## 🏷️ Tags
**Keywords:** foreign-key, transaction, payment, upgrade, escrow, points
**Category:** #migration #database #schema #payment #transaction