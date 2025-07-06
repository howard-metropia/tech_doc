# set_welcome_coin Seed Documentation

### 📋 Seed Overview
- **Purpose:** Initialize welcome coin history for existing users who don't have records
- **Environment:** All environments (dev, staging, production)
- **Dependencies:** auth_user and welcome_coin_history tables must exist
- **Idempotent:** Yes (checks for existing records before insertion)

### 🔧 Data Summary
```javascript
{
  operation: 'INSERT welcome_coin_history for users without existing records',
  device_id_fallback: 'register_device_id || device_id || "{user_id}-missing-device-id"',
  target_users: 'all auth_user records without welcome_coin_history'
}
```

### 📝 Affected Tables
| Table | Records | Description |
|-------|---------|-------------|
| welcome_coin_history | variable | Creates welcome coin records for existing users |

### ⚠️ Important Notes
- Processes all existing users and creates missing welcome coin history
- Uses fallback logic for device_id (register_device_id -> device_id -> generated)
- Error handling with logging for individual record failures
- Updates counter logged for tracking
- Related to MET-13987 ticket

### 🏷️ Tags
**Keywords:** welcome-coin, user-onboarding, backfill-data, MET-13987
**Category:** #seed #data #backfill #welcome-coins #user-onboarding

---
Note: This seed ensures all existing users have welcome coin history records for the onboarding reward system.