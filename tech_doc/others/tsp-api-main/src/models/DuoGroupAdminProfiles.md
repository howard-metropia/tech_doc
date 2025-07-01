# DuoGroupAdminProfiles Model

## 📋 Model Overview
- **Purpose:** Manages administrator profiles for Duo group management system
- **Table/Collection:** group_admin_profile
- **Database Type:** MySQL (portal)
- **Relationships:** None defined

## 🔧 Schema Definition
*Schema fields are not explicitly defined in the model. Database table structure would need to be verified.*

## 🔑 Key Information
- **Primary Key:** Not explicitly defined (likely `id`)
- **Indexes:** Not specified
- **Unique Constraints:** Not specified
- **Default Values:** Not specified

## 📝 Usage Examples
```javascript
// Basic query example
const admins = await DuoGroupAdminProfiles.query().where('status', 'active');

// Get admin by group
const groupAdmin = await DuoGroupAdminProfiles.query().where('group_id', 123);
```

## 🔗 Related Models
- No explicit relationships defined
- Part of Duo group management system

## 📌 Important Notes
- Minimal model with only table name definition
- Part of group administration and management
- Uses Objection.js ORM with MySQL portal database

## 🏷️ Tags
**Keywords:** duo, group, admin, profile, management
**Category:** #model #database #duo #group #admin