# UserDeviceLog Model Documentation

## 📋 Model Overview
- **Purpose:** Tracks user device information and login sessions for security and analytics
- **Table/Collection:** user_device_log
- **Database Type:** MySQL (portal database)
- **Relationships:** Links device information to user accounts

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| id | INT | Yes | Primary key, auto-increment |
| user_id | INT | Yes | Foreign key to auth_user |
| device_id | VARCHAR | Yes | Unique device identifier |
| device_type | VARCHAR | No | Device type (ios, android, web) |
| device_model | VARCHAR | No | Device model information |
| os_version | VARCHAR | No | Operating system version |
| app_version | VARCHAR | No | Application version |
| ip_address | VARCHAR | No | IP address of the device |
| user_agent | TEXT | No | Browser/app user agent string |
| last_active | TIMESTAMP | No | Last activity timestamp |
| created_at | TIMESTAMP | Yes | First login timestamp |
| updated_at | TIMESTAMP | Yes | Last update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** user_id, device_id, device_type, last_active
- **Unique Constraints:** Combination of user_id and device_id
- **Default Values:** created_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP

## 📝 Usage Examples
```javascript
// Get user's active devices
const userDevices = await UserDeviceLog.query()
  .where('user_id', userId)
  .where('last_active', '>', oneWeekAgo);

// Log device activity
await UserDeviceLog.query().upsert({
  user_id: userId,
  device_id: deviceId,
  device_type: 'ios',
  app_version: '2.1.0',
  last_active: new Date()
});

// Find devices by type
const iosDevices = await UserDeviceLog.query()
  .where('device_type', 'ios')
  .where('last_active', '>', oneMonthAgo);
```

## 🔗 Related Models
- `AuthUsers` - Many-to-one relationship via user_id
- `AuthUserTokens` - Related for session management
- `Notifications` - Device targeting for push notifications

## 📌 Important Notes
- Used for device-specific push notifications
- Helps track app usage patterns and device adoption
- IP address logging for security monitoring
- Supports multi-device user sessions
- Essential for app analytics and user behavior tracking

## 🏷️ Tags
**Keywords:** devices, logging, analytics, sessions, tracking
**Category:** #model #database #analytics #devices #mysql

---
Note: This model provides device tracking and analytics capabilities for user sessions.