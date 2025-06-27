# AuthUserLabel Model Documentation

## 📋 Model Overview
- **Purpose:** Associates user accounts with classification labels for segmentation and analytics
- **Table/Collection:** auth_user_label
- **Database Type:** MySQL
- **Relationships:** 
  - belongsTo: AuthUsers (via user_id), UserLabel (via label_id)

## 🔧 Schema Definition
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | int(11) | Yes | Primary key, auto-increment |
| user_id | int(11) | Yes | User ID (foreign key to auth_users) |
| label_id | int(11) | Yes | Label ID (foreign key to user_label) |
| sheet_added_on | datetime | Yes | When label was added to spreadsheet |
| created_on | datetime | Yes | Record creation timestamp |
| modified_on | datetime | Yes | Last modification timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** user_label_idx__0 (user_id, label_id) - UNIQUE composite index
- **Unique Constraints:** user_id + label_id combination must be unique
- **Default Values:** 
  - created_on: CURRENT_TIMESTAMP
  - modified_on: CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

## 📝 Usage Examples
```javascript
// Assign label to user
const userLabel = await AuthUserLabel.query().insert({
  user_id: 123,
  label_id: 1, // 'pioneer' label
  sheet_added_on: new Date()
});

// Get all labels for a user
const userLabels = await AuthUserLabel.query()
  .where('user_id', 123)
  .withGraphFetched('label');

// Find users with specific label
const pioneerUsers = await AuthUserLabel.query()
  .where('label_id', 1)
  .withGraphFetched('user');

// Check if user has specific label
const hasPioneerLabel = await AuthUserLabel.query()
  .where({ user_id: 123, label_id: 1 })
  .first();
```

## 🔗 Related Models
- `AuthUsers` - User account information
- `UserLabel` - Label definitions and names
- Used for user segmentation and analytics

## 📌 Important Notes
- Many-to-many relationship between users and labels
- Unique constraint prevents duplicate user-label assignments
- Tracks when labels were originally added to spreadsheet
- Supports user classification for targeted campaigns
- Default 'pioneer' label created during migration
- Useful for A/B testing and user cohort analysis

## 🏷️ Tags
**Keywords:** user-labels, classification, segmentation, analytics, tagging
**Category:** #model #database #user-management #analytics #labeling