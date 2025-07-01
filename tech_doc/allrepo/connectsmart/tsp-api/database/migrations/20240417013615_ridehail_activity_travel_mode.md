# Migration Documentation: 20240417013615_ridehail_activity_travel_mode.js

## 📋 Migration Overview
- **Purpose:** Add ridehail travel mode, activity type, and notification type to system tables
- **Date:** 2024-04-17 01:36:15
- **Ticket:** N/A
- **Risk Level:** Low

## 🔧 Schema Changes
```sql
INSERT INTO travel_mode (id, name) VALUES (8, 'ridehail');
INSERT INTO activity_type (id, name, description, created_on, modified_on) 
VALUES (16, 'Ridehail fare', 'Ridehail fare or refund fare(Uber)', NOW(), NOW());
INSERT INTO notification_type (id, name) VALUES (100, 'Ridehail');
```

## 📝 Changes Summary
| Operation | Table/Collection | Field/Index | Description |
|-----------|-----------------|-------------|-------------|
| INSERT | travel_mode | id=8 | New ridehail travel mode |
| INSERT | activity_type | id=16 | Ridehail fare activity type |
| INSERT | notification_type | id=100 | Ridehail notification type |

## ⬆️ Up Migration
- Inserts ridehail travel mode with id=8
- Inserts ridehail fare activity type with id=16 for Uber fare tracking
- Inserts ridehail notification type with id=100
- Uses moment.js for UTC timestamp generation

## ⬇️ Down Migration
- Removes all three inserted records by their specific IDs
- Clean rollback of all ridehail-related configuration data

## ⚠️ Important Notes
- Fixed IDs ensure consistency across environments
- Activity type specifically mentions Uber fare/refund tracking
- No error handling for duplicate key insertions
- Uses moment.js for proper UTC timestamp formatting
- Enables ridehail functionality across the system

## 🏷️ Tags
**Keywords:** ridehail travel-mode activity-type notification-type uber
**Category:** #migration #database #data #ridehail #system-config