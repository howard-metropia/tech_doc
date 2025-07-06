# Favorites Model

## 📋 Model Overview
- **Purpose:** Manages user favorite locations and preferences
- **Table/Collection:** user_favorites
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
const favorites = await Favorites.query().where('user_id', 123);

// Get favorites by type
const homeFavorites = await Favorites.query().where('type', 'home');
```

## 🔗 Related Models
- No explicit relationships defined
- Related to user and location models

## 📌 Important Notes
- Minimal model with only table name definition
- Part of user preference and location system
- Uses Objection.js ORM with MySQL portal database
- Table name is 'user_favorites' but class is 'Favorites'

## 🏷️ Tags
**Keywords:** favorites, user, location, preference
**Category:** #model #database #favorites #user #location