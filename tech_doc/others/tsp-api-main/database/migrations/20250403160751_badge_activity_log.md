# Migration Documentation

## 📋 Migration Overview
- **Purpose:** Create user badge activity logging system for tracking badge-related events
- **Date:** 2025-04-03 16:07:51
- **Ticket:** N/A
- **Risk Level:** Low

## 🔧 Schema Changes
```sql
CREATE TABLE user_badge_related_activity_log (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  activity_id VARCHAR(255) NOT NULL,
  activity_name VARCHAR(255) NOT NULL,
  activity_datetime DATETIME NOT NULL,
  related_badge_id INT NOT NULL,
  related_badge_name VARCHAR(45) NOT NULL,
  related_badge_status VARCHAR(255) NOT NULL,
  related_campaign_id INT NULL,
  related_campaign_name VARCHAR(255) NULL
);
```

## 📝 Changes Summary
| Operation | Table/Collection | Field/Index | Description |
|-----------|-----------------|-------------|-------------|
| CREATE | user_badge_related_activity_log | - | Badge activity tracking table |
| ADD | user_badge_related_activity_log | activity_id, activity_name | Activity identification |
| ADD | user_badge_related_activity_log | related_badge_id, related_badge_name | Badge information |
| ADD | user_badge_related_activity_log | related_badge_status | Badge status tracking |
| ADD | user_badge_related_activity_log | related_campaign_id, related_campaign_name | Campaign association |

## ⬆️ Up Migration
- Creates comprehensive badge activity logging table
- Tracks user activities that relate to badge progression
- Links activities to specific badges and campaigns
- Records activity timing and badge status changes
- Includes table existence check for safe creation

## ⬇️ Down Migration
- Drops user_badge_related_activity_log table if it exists
- Removes all badge activity tracking capabilities

## ⚠️ Important Notes
- Badge names limited to 45 characters
- Activity and campaign names support 255 characters
- Campaign fields are optional (nullable)
- Comprehensive activity-to-badge relationship tracking

## 🏷️ Tags
**Keywords:** badge, activity, log, tracking, campaign, user, gamification
**Category:** #migration #database #schema #badge #activity #tracking #gamification