# WelcomeCoinHistory Model

## 📋 Model Overview
- **Purpose:** Tracks welcome coin rewards and transaction history
- **Table/Collection:** welcome_coin_history
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
const coinHistory = await WelcomeCoinHistory.query().where('user_id', 123);

// Get recent transactions
const recentCoins = await WelcomeCoinHistory.query()
  .where('created_at', '>', '2023-01-01');
```

## 🔗 Related Models
- No explicit relationships defined
- Related to user and reward models

## 📌 Important Notes
- Minimal model with only table name definition
- Part of welcome bonus and reward system
- Uses Objection.js ORM with MySQL portal database
- Tracks welcome coin distribution

## 🏷️ Tags
**Keywords:** welcome, coin, history, rewards, bonus
**Category:** #model #database #welcome #coin #rewards