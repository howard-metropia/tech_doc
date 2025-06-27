# 20231117164537_fix_incentive_type.js Seed Documentation

## 📋 Seed Overview
- **Purpose:** Fixes incentive type data by copying from type field to incentive_type field
- **Environment:** All environments requiring incentive data migration
- **Dependencies:** incentive_notify_queue table with both type and incentive_type columns
- **Idempotent:** Yes (safe to run multiple times)

## 🔧 Data Summary
```javascript
{
  operation: 'UPDATE',
  table: 'incentive_notify_queue', 
  update: {
    incentive_type: 'COPY FROM type column'
  }
}
```

## 📝 Affected Tables
| Table | Records | Description |
|-------|---------|-------------|
| incentive_notify_queue | All records | Updates incentive_type field from type field |

## ⚠️ Important Notes
- Data migration seed, not data creation
- Uses raw SQL to copy column values
- Safe to run multiple times (idempotent)
- Fixes data consistency in incentive notification system
- Required for proper incentive processing

## 🏷️ Tags
**Keywords:** data-migration, incentive-types, fix-data, column-update  
**Category:** #seed #data-migration #incentives #fix

---
Note: Migrates incentive type data to standardize field usage across the system.