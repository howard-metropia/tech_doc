# PointsTransaction Model Documentation

## 📋 Model Overview
- **Purpose:** Manages point/coin transactions for user rewards, purchases, and payments within the MaaS platform
- **Table/Collection:** points_transaction or points_transaction_upgrade (configurable)
- **Database Type:** MySQL
- **Relationships:** 
  - belongsTo: AuthUsers (via user_id), ActivityTypes (via activity_type)
  - Self-referencing for payer/payee relationships

## 🔧 Schema Definition
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| id | int(11) | Yes | Primary key, auto-increment |
| user_id | int(11) | Yes | User ID who owns the transaction |
| activity_type | int(11) | Yes | Activity type (see static methods) |
| points | decimal(10,2) | Yes | Points amount (positive/negative) |
| balance | decimal(10,2) | Yes | User's balance after transaction |
| note | varchar(200) | No | Transaction description/note |
| created_on | datetime | Yes | Transaction timestamp |
| payer | int(11) | Yes | User ID who pays coins, default 0 |
| payee | int(11) | Yes | User ID who receives coins, default 0 |
| ref_transaction_id | int(11) | Yes | Cross-reference transaction ID, default 0 |
| ori_id | int(11) | No | Original ID for upgrade table only |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** 
  - activity_type__idx (activity_type)
  - coins_history_idx_1 (user_id, created_on, activity_type, id)
- **Unique Constraints:** None
- **Default Values:** payer: 0, payee: 0, ref_transaction_id: 0
- **Foreign Keys:** activity_type → activity_type.id

## 📝 Usage Examples
```javascript
// Record incentive points
const transaction = await PointsTransaction.query().insert({
  user_id: 123,
  activity_type: PointsTransaction.activityTypes.incentive,
  points: 50.00,
  balance: 150.00,
  note: 'Trip completion reward'
});

// Get user's transaction history
const history = await PointsTransaction.query()
  .where('user_id', 123)
  .orderBy('created_on', 'desc')
  .limit(10);

// Check activity type constants
console.log(PointsTransaction.activityTypes.purchase); // 2
console.log(PointsTransaction.activityTypeNames[2]); // 'purchase'
```

## 🔗 Related Models
- `AuthUsers` - User ownership and balance tracking
- `ActivityType` - Transaction type definitions
- `EscrowDetail` - Related carpool payment details
- `UserWallets` - User wallet management

## 📌 Important Notes
- Configurable table name based on pointsTransactionSchema setting
- Double-ledger system with payer/payee for transfers
- Rich activity type system with 18+ predefined types
- Balance field maintains running total for user
- Support for carpool, ridehail, transit, and parking transactions
- Cross-referencing enables transaction traceability

## 🏷️ Tags
**Keywords:** transactions, points, coins, payments, rewards, wallet, financial
**Category:** #model #database #financial #transactions #rewards