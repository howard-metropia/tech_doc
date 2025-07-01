# GiftCardCategory Model

## 📋 Model Overview
- **Purpose:** Manages categories for gift card classification and organization
- **Table/Collection:** giftcard_category
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
const categories = await GiftCardCategory.query().where('status', 'active');

// Get all categories
const allCategories = await GiftCardCategory.query();
```

## 🔗 Related Models
- No explicit relationships defined
- Likely referenced by gift card models

## 📌 Important Notes
- Minimal model with only table name definition
- Part of gift card management system
- Uses Objection.js ORM with MySQL portal database

## 🏷️ Tags
**Keywords:** giftcard, category, classification, rewards
**Category:** #model #database #giftcard #category