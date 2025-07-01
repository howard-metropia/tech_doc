# CoinActivityLogs Model Documentation

## 📋 Model Overview
- **Purpose:** Tracks coin-related activities and enforces daily limits for purchases and redemptions
- **Table/Collection:** coin_activity_log
- **Database Type:** MySQL (portal database)
- **Relationships:** Related to AuthUsers and coin transaction tables

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| id | INT | Yes | Primary key, auto-increment |
| user_id | INT | Yes | Foreign key to auth_user table |
| activity_type | INT | Yes | Type of activity (see static types) |
| amount | DECIMAL | No | Coin amount involved |
| transaction_id | VARCHAR | No | Related transaction identifier |
| timestamp | TIMESTAMP | Yes | Activity timestamp |
| ip_address | VARCHAR | No | User's IP address |
| device_id | VARCHAR | No | Device identifier |
| created_at | TIMESTAMP | Yes | Record creation timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** user_id, activity_type, timestamp, transaction_id
- **Unique Constraints:** None
- **Default Values:** created_at = CURRENT_TIMESTAMP

### Activity Types (Static Constants)
```javascript
{
  PURCHASE_COIN_DAILY_LIMIT: 1,      // Daily purchase limit reached
  REDEEM_DAILY_LIMIT: 2,             // Daily redemption limit reached
  PURCHASE_COIN_TWICE_VIOLATION_24HR: 3,  // Multiple purchase violation
  REDEEM_TWICE_VIOLATION_24HR: 4     // Multiple redemption violation
}
```

## 📝 Usage Examples
```javascript
// Basic query example
const logs = await CoinActivityLogs.query()
  .where('user_id', userId)
  .orderBy('timestamp', 'desc');

// Check for daily limit violations
const dailyLimitHit = await CoinActivityLogs.query()
  .where('user_id', userId)
  .where('activity_type', CoinActivityLogs.types.PURCHASE_COIN_DAILY_LIMIT)
  .where('timestamp', '>=', todayStart);

// Get all violation logs for a user
const violations = await CoinActivityLogs.query()
  .where('user_id', userId)
  .whereIn('activity_type', [
    CoinActivityLogs.types.PURCHASE_COIN_TWICE_VIOLATION_24HR,
    CoinActivityLogs.types.REDEEM_TWICE_VIOLATION_24HR
  ]);
```

## 🔗 Related Models
- `AuthUsers` - Many-to-one relationship via user_id
- `RedeemTransactions` - Related via transaction_id
- Coin purchase/wallet tables - Related via transaction_id

## 📌 Important Notes
- Used for fraud prevention and limit enforcement
- 24-hour violations track rapid successive transactions
- Daily limits reset at midnight (system timezone)
- IP and device tracking helps identify suspicious patterns

## 🏷️ Tags
**Keywords:** coins, activity, limits, violations, fraud-prevention
**Category:** #model #database #security #mysql

---
Note: This model is critical for maintaining coin economy integrity and preventing abuse.