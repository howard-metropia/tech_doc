# UserWallets Model

## 📋 Model Overview
- **Purpose:** Manages user digital wallet information and balances
- **Table/Collection:** user_wallet
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
const wallets = await UserWallets.query().where('user_id', 123);

// Get active wallets
const activeWallets = await UserWallets.query().where('status', 'active');
```

## 🔗 Related Models
- No explicit relationships defined
- Likely related to user and transaction models

## 📌 Important Notes
- Minimal model with only table name definition
- Part of payment and reward system
- Uses Objection.js ORM with MySQL portal database

## 🏷️ Tags
**Keywords:** wallet, payment, balance, user, financial
**Category:** #model #database #wallet #payment #user