# Migration Documentation: add_new_notification_type

## 📋 Migration Overview
- **Purpose:** Adds instant carpool notification types for driver and rider notifications
- **Date:** 2022-08-16 17:22:28
- **Ticket:** N/A
- **Risk Level:** Low

## 🔧 Schema Changes
```sql
INSERT INTO notification_type (id, name) VALUES 
('INSTANT_CARPOOL_NOTIFY_DRIVER', 'INSTANT_CARPOOL: Notify driver');
INSERT INTO notification_type (id, name) VALUES 
('INSTANT_CARPOOL_NOTIFY_RIDER', 'INSTANT_CARPOOL: Notify riders');
```

## 📝 Changes Summary
| Operation | Table/Collection | Field/Index | Description |
|-----------|-----------------|-------------|-------------|
| INSERT | notification_type | INSTANT_CARPOOL_NOTIFY_DRIVER | Driver notification type for instant carpool |
| INSERT | notification_type | INSTANT_CARPOOL_NOTIFY_RIDER | Rider notification type for instant carpool |

## ⬆️ Up Migration
- Adds two new notification types for instant carpool feature
- References predefined notification type constants from application defines
- Enables driver and rider specific notifications for instant carpool matching

## ⬇️ Down Migration
- Removes both instant carpool notification types
- Existing notifications of these types will become orphaned

## ⚠️ Important Notes
- Uses application constants for notification type IDs
- Part of instant carpool feature implementation
- Enables targeted notifications for different user roles

## 🏷️ Tags
**Keywords:** notification, instant-carpool, driver, rider, matching
**Category:** #migration #database #data #notification #carpool