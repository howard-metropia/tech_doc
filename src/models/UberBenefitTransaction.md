# Model Documentation: UberBenefitTransaction

## 📋 Model Overview
- **Purpose:** Tracks Uber benefit transactions and subsidy usage
- **Table/Collection:** uber_benefit_transaction
- **Database Type:** MySQL
- **Relationships:** Not defined in model (likely references users and transactions)

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
// Get all Uber benefit transactions for a user
const transactions = await UberBenefitTransaction.query()
  .where('user_id', userId);

// Create new benefit transaction
const transaction = await UberBenefitTransaction.query().insert({
  user_id: userId,
  amount: 10.00,
  transaction_type: 'subsidy',
  // other transaction details
});

// Get transactions by date range
const recentTransactions = await UberBenefitTransaction.query()
  .whereBetween('created_at', [startDate, endDate]);

// Calculate total benefits used
const total = await UberBenefitTransaction.query()
  .where('user_id', userId)
  .sum('amount as total');
```

## 🔗 Related Models
- AuthUsers - user_id likely references auth_users
- Transactions - may relate to general transaction records
- UberTrips - possibly linked to actual Uber trip data

## 📌 Important Notes
- Uses MySQL 'portal' connection
- Tracks ridehail subsidies and benefits
- Part of Objection.js ORM system
- Likely includes transaction amounts, dates, and status

## 🏷️ Tags
**Keywords:** uber, ridehail, benefits, subsidy, transactions
**Category:** #model #database #payments #ridehail #mysql

---