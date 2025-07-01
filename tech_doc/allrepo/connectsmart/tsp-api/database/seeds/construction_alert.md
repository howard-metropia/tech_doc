# Construction Alert Notification Type Seed

## 📋 Seed Overview
- **Purpose:** Adds construction alert notification type for traffic/construction zone notifications
- **Environment:** All environments (extends notification system)
- **Dependencies:** notification_type table must exist
- **Idempotent:** Yes (checks existence before inserting)

## 🔧 Data Summary
```javascript
// Construction notification type
{
  table: 'notification_type',
  data: {
    id: 105,
    name: 'Construction'
  }
}
```

## 📝 Affected Tables
| Table | Records | Description |
|-------|---------|-------------|
| notification_type | 1 | Construction alert notification category |

## ⚠️ Important Notes
- **Specific ID:** Uses ID 105 for construction notifications
- **Traffic Management:** Enables construction zone and road work alerts
- **Existence Check:** Safe to run multiple times without duplication
- **Notification System:** Extends core notification types for traffic alerts
- **Construction Integration:** Works with construction zone monitoring systems

## 🏷️ Tags
**Keywords:** construction-alert, notification-type, traffic-management, road-work
**Category:** #seed #data #notification #construction #traffic #alerts