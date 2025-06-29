# InternalUserTag Model

## 📋 Model Overview
- **Purpose:** Manages internal user tags for classification and organization
- **Table/Collection:** internal_user_tag
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
const userTags = await InternalUserTag.query().where('user_id', 123);

// Get tags by type
const betaTags = await InternalUserTag.query().where('tag_type', 'beta_user');
```

## 🔗 Related Models
- No explicit relationships defined
- Related to user management and classification

## 📌 Important Notes
- Minimal model with only table name definition
- Used for internal user classification and tagging
- Uses Objection.js ORM with MySQL portal database
- Part of user management and analytics system

## 🏷️ Tags
**Keywords:** internal, user, tag, classification, management
**Category:** #model #database #user #tag #internal