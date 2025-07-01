# RedeemTransactions Model Documentation

## 📋 Model Overview
- **Purpose:** Records coin redemption transactions for rewards and incentives
- **Table/Collection:** redeem_transaction
- **Database Type:** MySQL (portal database)
- **Relationships:** Related to AuthUsers, wallet transactions, and reward items

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| id | INT | Yes | Primary key, auto-increment |
| user_id | INT | Yes | Foreign key to auth_user table |
| transaction_id | VARCHAR | Yes | Unique transaction identifier |
| redeem_item_id | INT | No | Foreign key to redeemable items |
| coin_amount | DECIMAL | Yes | Number of coins redeemed |
| status | VARCHAR | Yes | Transaction status (pending/completed/failed) |
| redemption_type | VARCHAR | No | Type of redemption (gift_card/discount/reward) |
| provider | VARCHAR | No | External provider name |
| provider_reference | VARCHAR | No | External provider transaction ID |
| metadata | JSON | No | Additional transaction details |
| created_at | TIMESTAMP | Yes | Transaction creation timestamp |
| completed_at | TIMESTAMP | No | Transaction completion timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** user_id, transaction_id (unique), status, created_at
- **Unique Constraints:** transaction_id
- **Default Values:** status = 'pending', created_at = CURRENT_TIMESTAMP

## 📝 Usage Examples
```javascript
// Basic query example
const transactions = await RedeemTransactions.query()
  .where('user_id', userId)
  .orderBy('created_at', 'desc');

// Get completed transactions
const completedRedemptions = await RedeemTransactions.query()
  .where('status', 'completed')
  .where('created_at', '>=', startDate);

// Calculate total coins redeemed
const totalRedeemed = await RedeemTransactions.query()
  .where('user_id', userId)
  .where('status', 'completed')
  .sum('coin_amount as total');
```

## 🔗 Related Models
- `AuthUsers` - Many-to-one relationship via user_id
- `CoinActivityLogs` - Tracks redemption activity limits
- Wallet/balance tables - Updates user coin balance
- Reward catalog tables - Links to redeemable items

## 📌 Important Notes
- Transaction_id ensures idempotency for redemptions
- Status workflow: pending → completed OR pending → failed
- Provider fields used for third-party gift cards/rewards
- Metadata stores provider-specific response data

## 🏷️ Tags
**Keywords:** redemption, coins, rewards, transactions, incentives
**Category:** #model #database #transactions #mysql

---
Note: Critical model for the platform's reward economy and user incentive system.