# UserLabel Model Documentation

## 📋 Model Overview
- **Purpose:** Defines user classification labels for segmentation, analytics, and targeted campaigns
- **Table/Collection:** user_label
- **Database Type:** MySQL
- **Relationships:** 
  - hasMany: AuthUserLabel (via label_id)

## 🔧 Schema Definition
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | int(11) | Yes | Primary key, auto-increment |
| name | varchar(255) | Yes | Label name/identifier |
| created_on | datetime | Yes | Creation timestamp |
| modified_on | datetime | Yes | Last modification timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** None specified in schema
- **Unique Constraints:** None
- **Default Values:** 
  - created_on: CURRENT_TIMESTAMP
  - modified_on: CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

## 📝 Usage Examples
```javascript
// Create a new user label
const label = await UserLabel.query().insert({
  name: 'early_adopter'
});

// Get all available labels
const allLabels = await UserLabel.query()
  .orderBy('name');

// Find specific label
const pioneerLabel = await UserLabel.query()
  .where('name', 'pioneer')
  .first();

// Get label with associated users
const labelWithUsers = await UserLabel.query()
  .withGraphFetched('userAssignments.user')
  .findById(1);
```

## 🔗 Related Models
- `AuthUserLabel` - Many-to-many relationship with users
- `AuthUsers` - Users who have these labels assigned
- Used for campaign targeting and user segmentation

## 📌 Important Notes
- Reference table for user classification system
- Default 'pioneer' label created during migration
- Supports user segmentation for analytics
- Enables targeted marketing campaigns
- Labels can be used for A/B testing cohorts
- Simple name-based identification system

## 🏷️ Tags
**Keywords:** user-labels, classification, segmentation, analytics, targeting, reference-data
**Category:** #model #database #user-management #analytics #reference-data #segmentation