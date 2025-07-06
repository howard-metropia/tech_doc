# 20240529153842_add_activity_type.js Seed Documentation

## 📋 Seed Overview
- **Purpose:** Adds Campaign Reward activity type for reward system
- **Environment:** All environments requiring campaign reward functionality
- **Dependencies:** activity_type table must exist
- **Idempotent:** No (may fail on duplicate key if run multiple times)

## 🔧 Data Summary
```javascript
{
  table: 'activity_type',
  data: [
    { id: 15, name: 'Campaign Reward' }
  ]
}
```

## 📝 Affected Tables
| Table | Records | Description |
|-------|---------|-------------|
| activity_type | 1 | Adds campaign reward activity classification |

## ⚠️ Important Notes
- Fixed ID (15) may cause conflicts if run multiple times
- Used for tracking reward distribution activities
- Essential for campaign reward processing and analytics
- Links to campaign and token systems

## 🏷️ Tags
**Keywords:** activity-type, campaign-rewards, classification, rewards  
**Category:** #seed #activity-types #rewards #campaigns

---
Note: Enables activity tracking for campaign reward distributions.