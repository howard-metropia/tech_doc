# AppUpdate Model Documentation

## 📋 Model Overview
- **Purpose:** Manages application update information and version control
- **Table/Collection:** app_update
- **Database Type:** MySQL
- **Relationships:** None (standalone model)

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| id | Integer | Yes | Primary key (auto-increment) |
| version | String | - | Application version number |
| platform | String | - | Target platform (iOS/Android) |
| release_date | DateTime | - | Release date of the update |
| mandatory | Boolean | - | Whether update is mandatory |
| description | Text | - | Update description/changelog |
| download_url | String | - | URL for update download |
| created_at | DateTime | - | Record creation timestamp |
| updated_at | DateTime | - | Record update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** None explicitly defined
- **Unique Constraints:** None
- **Default Values:** Auto-generated timestamps

## 📝 Usage Examples
```javascript
// Check latest app update
const latestUpdate = await AppUpdate.query()
  .orderBy('release_date', 'desc')
  .first();

// Get mandatory updates
const mandatoryUpdates = await AppUpdate.query()
  .where('mandatory', true);
```

## 🔗 Related Models
- None - standalone model for app version management

## 📌 Important Notes
- Model class name is "AppUpdata" (typo in original code)
- Uses Objection.js ORM with MySQL portal database
- Primarily used for mobile app update notifications

## 🏷️ Tags
**Keywords:** app-update, version-control, mobile-app
**Category:** #model #database #app-management