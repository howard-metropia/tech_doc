# Model Documentation: UserActions

## 📋 Model Overview
- **Purpose:** Tracks and logs user actions and activities within the platform
- **Table/Collection:** user_actions
- **Database Type:** MongoDB
- **Relationships:** References users by userId

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| userId | Number | No | User identifier (indexed) |
| action | String | No | Action performed by user (text indexed) |
| attributes | Object | No | Additional action-specific data |
| createdAt | Date | Auto | Timestamp when action was created |
| updatedAt | Date | Auto | Timestamp when action was last updated |

## 🔑 Key Information
- **Primary Key:** _id (auto-generated)
- **Indexes:** 
  - userId (standard index)
  - action (text index for full-text search)
  - Default MongoDB _id index
- **Unique Constraints:** None
- **Default Values:** timestamps auto-generated

## 📝 Usage Examples
```javascript
// Log a user action
const action = await UserActions.create({
  userId: 12345,
  action: 'trip_completed',
  attributes: { tripId: 'T001', distance: 5.2 }
});

// Find all actions for a user
const userActions = await UserActions.find({ userId: 12345 });

// Search actions by text
const searchResults = await UserActions.find({
  $text: { $search: 'payment' }
});

// Get recent actions
const recentActions = await UserActions.find()
  .sort({ createdAt: -1 })
  .limit(10);
```

## 🔗 Related Models
- AuthUsers - userId references user records

## 📌 Important Notes
- Uses MongoDB 'cache' connection
- Timestamps are automatically managed
- No version key tracking (_v field disabled)
- Action field has text index for efficient searching
- Attributes field stores flexible JSON data

## 🏷️ Tags
**Keywords:** user activity, logging, tracking, analytics, audit
**Category:** #model #database #user-tracking #analytics

---