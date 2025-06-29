# Migration Documentation: improve_trip_activity_mapping

## 📋 Migration Overview
- **Purpose:** Major enhancement of trip_activity_mapping table structure and primary key changes
- **Date:** 2023-06-02 02:35:01
- **Ticket:** MET-12322
- **Risk Level:** High

## 🔧 Schema Changes
```sql
-- Primary key restructuring
ALTER TABLE trip_activity_mapping 
  DROP PRIMARY KEY (trip_id, activity_id),
  ADD PRIMARY KEY (trip_id);

-- Make activity_id nullable
ALTER TABLE trip_activity_mapping MODIFY activity_id INT NULL;

-- Add comprehensive trip tracking fields
ADD COLUMN user_id INT UNSIGNED NOT NULL COMMENT 'auth_user table id',
ADD COLUMN o_id INT UNSIGNED DEFAULT 0 COMMENT 'origin cm_location id',
ADD COLUMN d_id INT UNSIGNED DEFAULT 0 COMMENT 'destination cm_location id',
ADD COLUMN departure_time_utc DATETIME NULL COMMENT 'departure time in UTC',
ADD COLUMN trip_time_zone VARCHAR(32) NULL COMMENT 'trip time zone',
ADD COLUMN time_slot_local TINYINT DEFAULT 0 COMMENT '15-minute timeslots (1-96)',
ADD COLUMN is_weekday_local TINYINT(1) DEFAULT 0 COMMENT 'weekday=1, weekend=0',
ADD COLUMN travel_mode SMALLINT UNSIGNED DEFAULT 0 COMMENT 'travel mode',
ADD COLUMN created_on DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN modified_on DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;
```

## 📝 Changes Summary
| Operation | Table/Collection | Field/Index | Description |
|-----------|-----------------|-------------|-------------|
| DROP PRIMARY KEY | trip_activity_mapping | (trip_id, activity_id) | Removes composite primary key |
| ADD PRIMARY KEY | trip_activity_mapping | (trip_id) | Simplifies to single primary key |
| MODIFY | trip_activity_mapping | activity_id | Makes activity_id nullable |
| ADD | trip_activity_mapping | user_id | Links to auth_user table |
| ADD | trip_activity_mapping | o_id, d_id | Origin and destination location IDs |
| ADD | trip_activity_mapping | departure_time_utc | Trip departure time in UTC |
| ADD | trip_activity_mapping | trip_time_zone | Time zone information |
| ADD | trip_activity_mapping | time_slot_local | 15-minute time slot classification |
| ADD | trip_activity_mapping | is_weekday_local | Weekday/weekend classification |
| ADD | trip_activity_mapping | travel_mode | Transportation mode |
| ADD | trip_activity_mapping | created_on, modified_on | Timestamp tracking |

## ⬆️ Up Migration
- Restructures primary key from composite to single field
- Makes activity_id optional to support flexible mapping
- Adds comprehensive trip metadata tracking
- Implements time zone and temporal analysis capabilities
- Includes standard timestamp auditing fields

## ⬇️ Down Migration
- Removes all added fields
- Note: Primary key rollback may be problematic due to structure changes
- High risk of data loss during rollback

## ⚠️ Important Notes
- High risk migration affecting core trip tracking functionality
- Primary key change may impact existing foreign key relationships
- Critical for trip analytics and machine learning features
- Rollback complexity requires careful planning

## 🏷️ Tags
**Keywords:** trip-activity-mapping, primary-key, restructure, analytics, metadata
**Category:** #migration #database #schema #analytics #restructure #high-risk