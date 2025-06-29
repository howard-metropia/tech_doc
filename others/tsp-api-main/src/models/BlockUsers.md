# BlockUsers Model Documentation

## 📋 Model Overview
- **Purpose:** Manages user blocking/restriction records for moderation and safety
- **Table/Collection:** block_users
- **Database Type:** MySQL (portal database)
- **Relationships:** Links users who have blocked each other or been restricted

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| id | INT | Yes | Primary key, auto-increment |
| blocker_user_id | INT | Yes | Foreign key to auth_user who initiated the block |
| blocked_user_id | INT | Yes | Foreign key to auth_user who was blocked |
| reason | VARCHAR | No | Reason for blocking (harassment, spam, inappropriate) |
| block_type | VARCHAR | No | Type of block (user_initiated, system_automated, admin) |
| status | VARCHAR | No | Block status (active, removed, expired) |
| created_at | TIMESTAMP | Yes | Block creation timestamp |
| updated_at | TIMESTAMP | Yes | Last update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** blocker_user_id, blocked_user_id, status
- **Unique Constraints:** Unique combination of blocker_user_id and blocked_user_id
- **Default Values:** status = 'active', created_at = CURRENT_TIMESTAMP

## 📝 Usage Examples
```javascript
// Check if user is blocked
const isBlocked = await BlockUsers.query()
  .where('blocker_user_id', currentUserId)
  .where('blocked_user_id', targetUserId)
  .where('status', 'active')
  .first();

// Get all users blocked by a user
const blockedUsers = await BlockUsers.query()
  .where('blocker_user_id', userId)
  .where('status', 'active');

// Block a user
await BlockUsers.query().insert({
  blocker_user_id: currentUserId,
  blocked_user_id: targetUserId,
  reason: 'inappropriate_behavior',
  block_type: 'user_initiated'
});
```

## 🔗 Related Models
- `AuthUsers` - Many-to-one relationship via blocker_user_id and blocked_user_id
- `Reservations` - Affects reservation matching and interactions
- `DuoReservationMatches` - Prevents matching between blocked users

## 📌 Important Notes
- Supports bidirectional blocking relationships
- Used in matching algorithms to prevent unwanted pairings
- Includes both user-initiated and system-automated blocks
- Essential for platform safety and user moderation

## 🏷️ Tags
**Keywords:** blocking, moderation, safety, users, restrictions
**Category:** #model #database #moderation #safety #mysql

---
Note: This model provides user blocking functionality for platform safety and moderation.