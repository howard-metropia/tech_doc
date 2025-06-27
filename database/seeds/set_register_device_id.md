# set_register_device_id Seed Documentation

### 📋 Seed Overview
- **Purpose:** Sync device_id to register_device_id for users missing this field
- **Environment:** All environments (dev, staging, production)
- **Dependencies:** auth_user table must exist with device_id and register_device_id columns
- **Idempotent:** Yes (only updates records where register_device_id is null)

### 🔧 Data Summary
```javascript
{
  operation: 'UPDATE auth_user SET register_device_id = device_id',
  condition: 'WHERE device_id IS NOT NULL AND register_device_id IS NULL',
  target_users: 'users with device_id but missing register_device_id'
}
```

### 📝 Affected Tables
| Table | Records | Description |
|-------|---------|-------------|
| auth_user | variable | Updates register_device_id field with device_id values |

### ⚠️ Important Notes
- Data synchronization operation
- Logs count of affected records for tracking
- Error handling with logging for individual record failures
- Only processes records where register_device_id is null
- Ensures device registration consistency

### 🏷️ Tags
**Keywords:** device-id, register-device-id, data-sync, user-devices
**Category:** #seed #data #sync #device-registration #user-management

---
Note: This seed ensures device registration consistency by copying device_id to register_device_id where missing.