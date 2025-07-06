# Migration Documentation: 20240415071147_ridehail_uber_integration.js

## 📋 Migration Overview
- **Purpose:** Create ridehail_trip and uber_guest_ride_log tables for Uber integration
- **Date:** 2024-04-15 07:11:47
- **Ticket:** N/A
- **Risk Level:** High

## 🔧 Schema Changes
```sql
CREATE TABLE ridehail_trip (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  user_id INT REFERENCES auth_user(id) ON DELETE CASCADE,
  trip_id INT UNIQUE REFERENCES trip(id) ON DELETE CASCADE,
  uber_fare_id VARCHAR(36) NOT NULL,
  uber_request_id VARCHAR(36) NOT NULL,
  uber_product_id VARCHAR(36) NOT NULL,
  estimated_fare DECIMAL(10,2),
  -- ... additional 30+ fields for comprehensive ridehail data
);

CREATE TABLE uber_guest_ride_log (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  resource_id VARCHAR(36),
  event_id VARCHAR(36),
  event_type VARCHAR(50),
  event_time INT,
  status VARCHAR(50),
  webhook_meta JSON,
  resource_backup JSON
);
```

## 📝 Changes Summary
| Operation | Table/Collection | Field/Index | Description |
|-----------|-----------------|-------------|-------------|
| CREATE TABLE | ridehail_trip | - | Complete ridehail trip management |
| CREATE TABLE | uber_guest_ride_log | - | Uber webhook event logging |
| ADD FOREIGN KEYS | ridehail_trip | user_id, trip_id | Referential integrity |
| CREATE INDEX | ridehail_trip | uber_request_id | Query optimization |

## ⬆️ Up Migration
- Creates comprehensive ridehail_trip table with 30+ fields
- Creates uber_guest_ride_log table for webhook event tracking
- Establishes foreign key relationships with CASCADE deletion
- Includes comprehensive error handling with automatic cleanup
- Uses logging for error tracking

## ⬇️ Down Migration
- Drops both tables completely
- Safe cleanup with dropTableIfExists

## ⚠️ Important Notes
- **Major Schema Addition:** Introduces complete Uber integration infrastructure
- Foreign key constraints ensure data integrity
- JSON fields store webhook metadata and resource backups
- Comprehensive fare, trip status, and vehicle information tracking
- Error handling includes cleanup of partially created tables
- Enables full ridehail functionality with guest ride support

## 🏷️ Tags
**Keywords:** ridehail uber integration webhooks major-schema foreign-keys
**Category:** #migration #database #schema #ridehail #uber #integration #major