# DuoGroupMembers Model Documentation

## 📋 Model Overview
- **Purpose:** Manages membership in duo groups and group-based features
- **Table/Collection:** group_member
- **Database Type:** MySQL
- **Relationships:** References users, groups, and group types

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| id | Integer | Yes | Primary key (auto-increment) |
| group_id | Integer | - | Associated group identifier |
| user_id | Integer | - | Member user identifier |
| role | String | - | Member role (admin, member, etc.) |
| status | String | - | Active, pending, inactive, banned |
| joined_at | DateTime | - | When user joined group |
| invited_by | Integer | - | User who sent invitation |
| permissions | JSON | - | Member-specific permissions |
| nickname | String | - | Display name within group |
| is_active | Boolean | - | Whether membership is active |
| last_activity | DateTime | - | Last group activity timestamp |
| notification_settings | JSON | - | Member notification preferences |
| created_at | DateTime | - | Record creation timestamp |
| updated_at | DateTime | - | Record update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** Likely on group_id, user_id, status, role
- **Unique Constraints:** Possibly group_id+user_id combination
- **Default Values:** Auto-generated timestamps, is_active default true

## 📝 Usage Examples
```javascript
// Add member to group
const member = await DuoGroupMembers.query().insert({
  group_id: 123,
  user_id: 456,
  role: 'member',
  status: 'active',
  joined_at: new Date(),
  invited_by: adminUserId
});

// Get group members
const members = await DuoGroupMembers.query()
  .where('group_id', groupId)
  .where('status', 'active')
  .orderBy('joined_at');

// Update member role
await DuoGroupMembers.query()
  .where('group_id', groupId)
  .where('user_id', userId)
  .patch({
    role: 'admin',
    permissions: { can_invite: true, can_remove: true }
  });

// Remove member from group
await DuoGroupMembers.query()
  .where('id', memberId)
  .patch({ status: 'inactive', is_active: false });
```

## 🔗 Related Models
- **DuoGroups**: Members belong to specific groups
- **DuoGroupTypes**: Group type defines member limits and permissions
- **AuthUsers**: Members are application users

## 📌 Important Notes
- Role-based access control within groups
- Status tracking for membership lifecycle
- Invitation system with tracking
- Custom permissions per member
- Activity tracking for engagement metrics
- Soft delete pattern for membership history

## 🏷️ Tags
**Keywords:** groups, members, roles, permissions, duo
**Category:** #model #database #groups #membership