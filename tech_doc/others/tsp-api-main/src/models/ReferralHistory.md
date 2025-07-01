# ReferralHistory Model

## 📋 Model Overview
- **Purpose:** Tracks user referral activities and history
- **Table/Collection:** referral_history
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
const history = await referralHistory.query().where('user_id', 123);

// Get successful referrals
const successful = await referralHistory.query().where('status', 'completed');
```

## 🔗 Related Models
- No explicit relationships defined
- Likely related to user and reward models

## 📌 Important Notes
- Minimal model with only table name definition
- Part of referral reward system
- Uses Objection.js ORM with MySQL portal database
- Class name uses camelCase (referralHistory)

## 🏷️ Tags
**Keywords:** referral, history, rewards, tracking
**Category:** #model #database #referral #history #rewards