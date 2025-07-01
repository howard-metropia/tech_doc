# Model Documentation: MarketUsers

## 📋 Model Overview
- **Purpose:** Manages market-specific user data and configurations
- **Table/Collection:** market_user
- **Database Type:** MySQL
- **Relationships:** Not defined in model (likely references auth_users)

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
// Find all market users
const marketUsers = await MarketUser.query();

// Find market user by ID
const user = await MarketUser.query().findById(1);

// Create new market user
const newUser = await MarketUser.query().insert({
  // field values depend on actual schema
});

// Update market user
await MarketUser.query()
  .patch({ /* updated fields */ })
  .where('id', userId);
```

## 🔗 Related Models
- Likely related to AuthUsers model for user authentication

## 📌 Important Notes
- Uses MySQL 'portal' connection
- Minimal model definition - schema is database-driven
- Part of Objection.js ORM system
- Actual table structure needs to be checked in database

## 🏷️ Tags
**Keywords:** market, user, portal, configuration
**Category:** #model #database #user-management #mysql

---