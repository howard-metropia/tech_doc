# Preference Model Documentation

## 📋 Model Overview
- **Purpose:** Stores user preferences and application settings
- **Table/Collection:** preference
- **Database Type:** MySQL
- **Relationships:** Belongs to users, references various preference categories

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| id | Integer | Yes | Primary key (auto-increment) |
| user_id | Integer | - | User who owns preferences |
| category | String | - | Preference category (notifications, privacy, etc.) |
| key | String | - | Specific preference key |
| value | Text | - | Preference value (JSON or string) |
| data_type | String | - | Value data type (string, boolean, json) |
| is_default | Boolean | - | Whether this is default setting |
| description | String | - | Human-readable description |
| is_active | Boolean | - | Whether preference is active |
| last_modified | DateTime | - | Last modification timestamp |
| created_at | DateTime | - | Record creation timestamp |
| updated_at | DateTime | - | Record update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** Likely on user_id, category, key, is_active
- **Unique Constraints:** Possibly user_id+category+key combination
- **Default Values:** Auto-generated timestamps, is_active default true

## 📝 Usage Examples
```javascript
// Set user preference
const preference = await Preference.query().insert({
  user_id: userId,
  category: 'notifications',
  key: 'push_enabled',
  value: 'true',
  data_type: 'boolean'
});

// Get user's notification preferences
const notificationPrefs = await Preference.query()
  .where('user_id', userId)
  .where('category', 'notifications')
  .where('is_active', true);

// Update preference value
await Preference.query()
  .where('user_id', userId)
  .where('key', 'theme')
  .patch({ 
    value: 'dark',
    last_modified: new Date()
  });

// Get preference with fallback to default
const pref = await Preference.query()
  .where('user_id', userId)
  .where('key', 'language')
  .first() || 
  await Preference.query()
    .where('is_default', true)
    .where('key', 'language')
    .first();
```

## 🔗 Related Models
- **AuthUsers**: Preferences belong to specific users
- **DefaultSettings**: System-wide default preferences
- **UserProfiles**: May reference profile-related preferences

## 📌 Important Notes
- Flexible key-value preference system
- Categorized preferences for organization
- Data type tracking for proper value handling
- Default preference system for new users
- Activity status for preference management
- Supports JSON values for complex preferences

## 🏷️ Tags
**Keywords:** preferences, settings, user-configuration, key-value
**Category:** #model #database #user-settings #preferences