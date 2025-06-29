# ParkMobile Integration Notification Seed

## 📋 Seed Overview
- **Purpose:** Adds notification type for ParkMobile on-street parking reminders
- **Environment:** All environments (supports ParkMobile parking integration)
- **Dependencies:** notification_type table must exist
- **Idempotent:** No (will fail if ID 97 already exists)

## 🔧 Data Summary
```javascript
// ParkMobile parking notification type
{
  table: 'notification_type',
  data: {
    id: 97,
    name: 'On-street parking: Parking Reminder'
  }
}
```

## 📝 Affected Tables
| Table | Records | Description |
|-------|---------|-------------|
| notification_type | 1 | ParkMobile parking reminder notifications |

## ⚠️ Important Notes
- **ParkMobile Integration:** Enables notifications for on-street parking services
- **ID Conflict:** Will fail if notification_type ID 97 already exists
- **Parking Reminders:** Notifies users about parking session status
- **Third-Party Integration:** Supports ParkMobile API notification system
- **Error Handling:** Throws errors on failure with transaction rollback

## 🏷️ Tags
**Keywords:** parkmobile, parking-reminder, notification-type, on-street-parking
**Category:** #seed #data #notification #parkmobile #parking #integration