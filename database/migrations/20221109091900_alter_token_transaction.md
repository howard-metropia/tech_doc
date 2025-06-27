# Migration Documentation: alter_token_transaction

## 📋 Migration Overview
- **Purpose:** Enhances token_transaction table with agency, campaign, and notification tracking
- **Date:** 2022-11-09 09:19:00
- **Ticket:** N/A
- **Risk Level:** Medium

## 🔧 Schema Changes
```sql
-- Modify existing column
ALTER TABLE token_transaction MODIFY user_id INT(11) NOT NULL DEFAULT 0;

-- Add new columns
ALTER TABLE token_transaction ADD f_agency_id INT(11) NOT NULL DEFAULT 0;
ALTER TABLE token_transaction ADD agency_name VARCHAR(255) NOT NULL DEFAULT '';
ALTER TABLE token_transaction ADD f_token_id INT(11) NOT NULL DEFAULT 0;
ALTER TABLE token_transaction ADD token_name VARCHAR(255) NOT NULL DEFAULT '';
ALTER TABLE token_transaction ADD f_campaign_id INT(11) NOT NULL DEFAULT 0;
ALTER TABLE token_transaction ADD campaign_name VARCHAR(255) NOT NULL DEFAULT '';
ALTER TABLE token_transaction ADD issued_on DATETIME DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE token_transaction ADD expired_on DATETIME DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE token_transaction ADD dist_notify_status TINYINT(1) NOT NULL DEFAULT 0;
ALTER TABLE token_transaction ADD expire_notify_status TINYINT(1) NOT NULL DEFAULT 0;
ALTER TABLE token_transaction ADD subtitle VARCHAR(255) NOT NULL DEFAULT '';

-- Add to related table
ALTER TABLE bytemark_order_payments ADD f_token_id INT(11) NOT NULL DEFAULT 0;

-- Add indexes
CREATE INDEX main_query_index_1 ON token_transaction (user_id, activity_type, f_agency_id, f_token_id, issued_on, expired_on);
CREATE INDEX notification_index_1 ON token_transaction (dist_notify_status, expire_notify_status);
```

## 📝 Changes Summary
| Operation | Table/Collection | Field/Index | Description |
|-----------|-----------------|-------------|-------------|
| MODIFY | token_transaction | user_id | Changes type to INT from DOUBLE |
| ADD | token_transaction | f_agency_id, agency_name | Agency reference and name |
| ADD | token_transaction | f_token_id, token_name | Token reference and name |
| ADD | token_transaction | f_campaign_id, campaign_name | Campaign reference and name |
| ADD | token_transaction | issued_on, expired_on | Token validity period |
| ADD | token_transaction | dist_notify_status, expire_notify_status | Notification tracking |
| CREATE INDEX | token_transaction | main_query_index_1, notification_index_1 | Query optimization |

## ⬆️ Up Migration
- Enhances token transactions with comprehensive tracking
- Adds foreign key references to agencies, tokens, and campaigns
- Implements notification status tracking for token distribution and expiration
- Creates optimized indexes for common query patterns

## ⬇️ Down Migration
- Reverts user_id type back to DOUBLE
- Removes all added columns and indexes
- Removes token reference from bytemark_order_payments

## ⚠️ Important Notes
- Changes user_id data type which may affect existing queries
- Adds comprehensive token lifecycle management
- Critical for token-based payment system functionality

## 🏷️ Tags
**Keywords:** token, transaction, agency, campaign, notification, lifecycle
**Category:** #migration #database #schema #token #payment #notification