# Migration Documentation: create_bytemark_ticket_refresh_log

## 📋 Migration Overview
- **Purpose:** Creates table to track Bytemark ticket refresh activities and scheduling
- **Date:** 2023-04-19 15:04:07
- **Ticket:** N/A
- **Risk Level:** Low

## 🔧 Schema Changes
```sql
CREATE TABLE bytemark_ticket_refresh_log (
  id int AUTO_INCREMENT PRIMARY KEY,
  user_id int UNSIGNED NOT NULL DEFAULT 0,
  activity_type int UNSIGNED NOT NULL DEFAULT 0,
  status int UNSIGNED NOT NULL DEFAULT 0,
  note varchar(256) NULL,
  scheduled_on datetime NULL,
  created_on datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified_on datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx__user_id__status__001 (user_id, status)
);
```

## 📝 Changes Summary
| Operation | Table/Collection | Field/Index | Description |
|-----------|-----------------|-------------|-------------|
| CREATE TABLE | bytemark_ticket_refresh_log | - | Tracks ticket refresh activities |
| ADD | bytemark_ticket_refresh_log | activity_type | 1=immediate check, 2=scheduled status change, 3=free pass notification |
| ADD | bytemark_ticket_refresh_log | status | Activity status tracking |
| CREATE INDEX | bytemark_ticket_refresh_log | idx__user_id__status__001 | Performance optimization for user/status queries |

## ⬆️ Up Migration
- Creates new table for logging Bytemark ticket refresh operations
- Includes scheduling capabilities with scheduled_on field
- Supports multiple activity types for different refresh scenarios

## ⬇️ Down Migration
- Drops the entire bytemark_ticket_refresh_log table
- All refresh log data will be lost

## ⚠️ Important Notes
- Activity types are predefined: 1=immediate check, 2=scheduled change, 3=notification
- Table includes automatic timestamp management
- Index optimizes queries by user_id and status combination

## 🏷️ Tags
**Keywords:** bytemark, ticket, refresh, logging, scheduling
**Category:** #migration #database #schema #transit #logging