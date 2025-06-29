# Model Documentation: AccMemberPortal

## 📋 Model Overview
- **Purpose:** Manages carpool member portal access and account information
- **Table/Collection:** acc_member_portal
- **Database Type:** MySQL
- **Relationships:** Not defined in model (likely part of carpooling system)

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| *Schema not defined in model file* | - | - | Table structure exists in database |

## 🔑 Key Information
- **Primary Key:** Likely id (standard convention)
- **Indexes:** Database-defined
- **Unique Constraints:** Database-defined
- **Default Values:** Database-defined

## 📝 Usage Examples
```javascript
// Find all carpool portal members
const members = await AccMemberPortal.query();

// Find member by ID
const member = await AccMemberPortal.query().findById(memberId);

// Create new portal member
const newMember = await AccMemberPortal.query().insert({
  // member data fields
});

// Update member information
await AccMemberPortal.query()
  .patch({ status: 'active' })
  .where('id', memberId);

// Find active members
const activeMembers = await AccMemberPortal.query()
  .where('status', 'active');
```

## 🔗 Related Models
- Likely related to other carpool models in the carpooling database
- May reference AuthUsers for authentication

## 📌 Important Notes
- Uses MySQL 'carpooling' connection
- Part of carpool subsystem
- Minimal model definition - schema is database-driven
- Part of Objection.js ORM system

## 🏷️ Tags
**Keywords:** carpool, member, portal, access, account
**Category:** #model #database #carpooling #mysql

---