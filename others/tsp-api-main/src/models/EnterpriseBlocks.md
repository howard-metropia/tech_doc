# EnterpriseBlocks Model Documentation

## 📋 Model Overview
- **Purpose:** Manages access restrictions and blocking for enterprise users/features
- **Table/Collection:** enterprise_blocks
- **Database Type:** MySQL
- **Relationships:** References enterprises and blocked entities

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| id | Integer | Yes | Primary key (auto-increment) |
| enterprise_id | Integer | - | Associated enterprise |
| blocked_type | String | - | Type of block (user, feature, etc.) |
| blocked_id | Integer | - | ID of blocked entity |
| reason | String | - | Reason for blocking |
| blocked_by | Integer | - | Administrator who applied block |
| expires_at | DateTime | - | Block expiration (null = permanent) |
| status | String | - | Active, expired, removed |
| metadata | JSON | - | Additional block configuration |
| created_at | DateTime | - | Record creation timestamp |
| updated_at | DateTime | - | Record update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** Likely on enterprise_id, blocked_type+blocked_id, status
- **Unique Constraints:** Possibly enterprise_id+blocked_type+blocked_id
- **Default Values:** Auto-generated timestamps

## 📝 Usage Examples
```javascript
// Block user access to enterprise
const block = await EnterpriseBlocks.query().insert({
  enterprise_id: 123,
  blocked_type: 'user',
  blocked_id: 456,
  reason: 'Policy violation',
  blocked_by: adminUserId,
  status: 'active'
});

// Check if user is blocked
const isBlocked = await EnterpriseBlocks.query()
  .where('enterprise_id', enterpriseId)
  .where('blocked_type', 'user')
  .where('blocked_id', userId)
  .where('status', 'active')
  .first();

// Remove block
await EnterpriseBlocks.query()
  .where('id', blockId)
  .patch({ status: 'removed' });
```

## 🔗 Related Models
- **Enterprises**: Blocks are specific to enterprises
- **AuthUsers**: Can block users or track who applied blocks
- **EnterpriseUsers**: Affects enterprise user access

## 📌 Important Notes
- Flexible blocking system for various entity types
- Support for temporary and permanent blocks
- Audit trail with reason and administrator tracking
- Status-based block management for easy administration

## 🏷️ Tags
**Keywords:** enterprise, blocking, access-control, restrictions
**Category:** #model #database #enterprise #security