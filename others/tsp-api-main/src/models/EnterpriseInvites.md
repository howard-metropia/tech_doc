# EnterpriseInvites Model Documentation

## 📋 Model Overview
- **Purpose:** Manages enterprise user invitations and onboarding process
- **Table/Collection:** enterprise_invites
- **Database Type:** MySQL
- **Relationships:** References enterprises and invited users

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| id | Integer | Yes | Primary key (auto-increment) |
| enterprise_id | Integer | - | Associated enterprise |
| email | String | - | Invited user email address |
| role | String | - | Intended role (admin, user, etc.) |
| status | String | - | Pending, accepted, rejected, expired |
| invited_by | Integer | - | User ID who sent invitation |
| token | String | - | Unique invitation token |
| expires_at | DateTime | - | Invitation expiration time |
| accepted_at | DateTime | - | When invitation was accepted |
| created_at | DateTime | - | Record creation timestamp |
| updated_at | DateTime | - | Record update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** Likely on enterprise_id, email, token, status
- **Unique Constraints:** Possibly token, combination of enterprise_id+email
- **Default Values:** Auto-generated timestamps

## 📝 Usage Examples
```javascript
// Send enterprise invitation
const invite = await EnterpriseInvites.query().insert({
  enterprise_id: 123,
  email: 'user@company.com',
  role: 'admin',
  invited_by: currentUserId,
  token: generateInviteToken(),
  expires_at: new Date(Date.now() + 7*24*60*60*1000) // 7 days
});

// Accept invitation
await EnterpriseInvites.query()
  .where('token', inviteToken)
  .where('status', 'pending')
  .patch({ 
    status: 'accepted',
    accepted_at: new Date()
  });

// Get pending invites for enterprise
const pendingInvites = await EnterpriseInvites.query()
  .where('enterprise_id', enterpriseId)
  .where('status', 'pending')
  .where('expires_at', '>', new Date());
```

## 🔗 Related Models
- **Enterprises**: Invites belong to specific enterprises
- **AuthUsers**: invited_by references user table
- **EnterpriseUsers**: Accepted invites create enterprise user records

## 📌 Important Notes
- Token-based invitation system for security
- Time-limited invitations with expiration
- Role-based access control for enterprise features
- Status tracking for invitation lifecycle

## 🏷️ Tags
**Keywords:** enterprise, invitations, onboarding, roles
**Category:** #model #database #enterprise #invitations