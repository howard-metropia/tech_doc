# Incentive Make Trip Notification Seed

## 📋 Seed Overview
- **Purpose:** Adds notification type for trip completion incentive notifications
- **Environment:** All environments (supports incentive system notifications)
- **Dependencies:** notification_type table must exist
- **Idempotent:** No (will fail if ID 98 already exists)

## 🔧 Data Summary
```javascript
// Trip incentive notification type
{
  table: 'notification_type',
  data: {
    id: 98,
    name: 'Incentive: Make Trip'
  }
}
```

## 📝 Affected Tables
| Table | Records | Description |
|-------|---------|-------------|
| notification_type | 1 | Trip completion incentive notifications |

## ⚠️ Important Notes
- **Incentive System:** Enables notifications for trip completion rewards
- **ID Conflict:** Will fail if notification_type ID 98 already exists
- **User Engagement:** Motivates users with trip completion incentives
- **Reward Notifications:** Notifies users when they earn trip incentives
- **Error Handling:** Throws errors on failure with transaction rollback

## 🏷️ Tags
**Keywords:** incentive, make-trip, notification-type, rewards, trip-completion
**Category:** #seed #data #notification #incentive #rewards #trip