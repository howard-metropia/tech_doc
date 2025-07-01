# Wallet Service Documentation

## 🔍 Quick Summary (TL;DR)
Comprehensive wallet service managing user coin balances, auto-refill, Stripe payments, and transaction history for MaaS platform.

**Keywords:** wallet | coins | points | balance | stripe | payment | transaction | auto-refill | refill | tokens | escrow | purchase | redemption | mobility | finance

**Primary Use Cases:**
- User coin balance management and tracking
- Auto-refill when balance drops below threshold  
- Stripe payment processing for coin purchases
- Transaction history with detailed activity types
- Token management for transit systems

**Compatibility:** Node.js 16+, Koa.js, Stripe API, MySQL, MongoDB

## ❓ Common Questions Quick Index
1. [How to get user wallet balance?](#wallet-balance) - `getUserWallet()` function
2. [How to add/subtract coins?](#points-transaction) - `pointsTransaction()` function  
3. [How to enable auto-refill?](#auto-refill) - `putWalletSetting()` function
4. [How to process Stripe payments?](#stripe-payments) - `stripeCharge()` function
5. [How to get transaction history?](#transaction-history) - `coinsHistory()` function
6. [What are activity types?](#activity-types) - 18 different transaction types
7. [How to handle token transactions?](#token-management) - `tokenTransaction()` function
8. [How to check daily coin limits?](#daily-limits) - `exceedCoinDailyLimit()` function
9. [How to troubleshoot failed payments?](#payment-troubleshooting) - Error handling
10. [How to view available coin packages?](#coin-packages) - `pointStore()` function

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a digital wallet for a transportation app - like a prepaid card system at a subway station. Users can load money (coins) onto their account, set up automatic top-ups when running low, and spend coins on various services like parking, transit tickets, or rideshare. The system tracks every transaction and can handle special promotions.

**Technical explanation:**
Service layer implementing wallet operations with database transactions, Stripe integration, and activity tracking. Uses MySQL for persistent storage, implements double-entry bookkeeping, and supports multiple payment methods including coins, tokens, and escrow accounts.

**Business value:** Enables monetization through prepaid coin system, reduces friction for mobility payments, and provides comprehensive financial tracking for user spending patterns.

## 🔧 Technical Specifications

**File:** `/src/services/wallet.js` (1,477 lines, High complexity)
**Dependencies:**
- `@maas/core` - Core utilities and database connections
- `stripe` - Payment processing API
- `moment-timezone` - Date/time handling
- `knex` - SQL query builder
- `config` - Configuration management

**Configuration Parameters:**
- `config.vendor.stripe.apiKey` - Stripe API key
- `config.vendor.stripe.buyCoinLimit` - Daily purchase limit
- `config.portal.pointsTransactionSchema` - Database schema

**System Requirements:**
- MySQL database with wallet tables
- Stripe account for payment processing
- Redis for session management

## 📝 Detailed Code Analysis

**Main Functions:**
```javascript
// Core wallet operations
pointsTransaction(userId, activityType, points, note, notify, time, payer, payee)
getUserWallet(trx, userId) 
stripeCharge(amount, currency, coins, userId, customerId, token)
coinsHistory(json) // Get transaction history
```

**Activity Types (18 types):**
1. Adjustment - Admin balance adjustments
2. Purchase - Coin purchases via Stripe
3. Redemption - Gift card redemptions
4. Promotion - Promotional code rewards
5. Auto-refill - Automatic balance top-ups
6. Incentive - Rewards from campaigns
7. Carpool Driver - Carpool earnings
8. Carpool Rider - Carpool payments
9. Into Escrow - Funds held in escrow
10. From Escrow - Funds released from escrow
11. Transit - Transit ticket purchases
12. Fee - Platform fees
13. Parking Fee - ParkMobile parking charges
14. Transaction Fee - Processing fees
15. Campaign Reward - Campaign completions
16. Ridehail - Uber fare payments
17. Challenge Reward - Challenge completions
18. Uber Benefit - Tier benefit refunds

**Double-entry Bookkeeping:**
Every transaction creates paired entries for payer/payee accounts, ensuring balance integrity.

## 🚀 Usage Methods

**Basic Balance Check:**
```javascript
const wallet = await getUserWallet(userId);
console.log(`Balance: ${wallet.balance} coins`);
```

**Add Coins:**
```javascript
const result = await pointsTransaction(
  userId,
  2, // Purchase activity type
  50, // Amount in coins
  'Credit card purchase',
  true, // Send notification
  null, // Use current time
  2100, // Stripe payer ID
  userId // User payee ID
);
```

**Enable Auto-refill:**
```javascript
const setting = await putWalletSetting({
  userId: 12345,
  auto_refill: true,
  below_balance: 10,
  refill_plan_id: 1
});
```

**Process Stripe Payment:**
```javascript
const charge = await stripeCharge(
  1000, // $10.00 in cents
  'usd',
  50, // 50 coins
  userId,
  'cus_stripe_customer_id'
);
```

## 📊 Output Examples

**Successful Wallet Response:**
```json
{
  "id": 12345,
  "balance": 47.50,
  "auto_refill": true,
  "below_balance": 10,
  "stripe_customer_id": "cus_abc123",
  "refill_plan": {
    "id": 1,
    "points": 50,
    "amount": 1000,
    "currency": "usd",
    "display_rate": 100
  }
}
```

**Transaction History Response:**
```json
{
  "total_count": 25,
  "next_offset": 20,
  "balance": 47.50,
  "auto_reload": true,
  "pending_total": 5.00,
  "transactions": [
    {
      "id": 98765,
      "points": -2.50,
      "activity_type": 11,
      "subtitle": "METRO",
      "note": "1 ticket",
      "created_on": "2024-01-15T10:30:00+00:00",
      "balance": 47.50
    }
  ]
}
```

**Error Response:**
```json
{
  "error": "ERROR_POINT_INSUFFICIENT",
  "message": "Insufficient coins for transaction",
  "code": 400
}
```

## ⚠️ Important Notes

**Security Considerations:**
- All database operations use transactions to prevent race conditions
- Daily coin purchase limits prevent fraud
- User blocking mechanism for suspicious activity
- Stripe webhooks validate payment authenticity

**Performance Gotchas:**
- Database locks during balance updates can cause contention
- Large transaction history queries need pagination
- Auto-refill can trigger during high-load periods

**Common Issues:**
- **Insufficient Balance:** Check user balance before transactions
- **Stripe Failures:** Verify API keys and customer IDs
- **Auto-refill Loops:** Monitor daily limits and user blocking
- **Currency Mismatches:** Ensure consistent currency handling

## 🔗 Related File Links

**Dependencies:**
- `/src/models/PointsTransaction.js` - Transaction model
- `/src/models/BlockUsers.js` - User blocking model
- `/src/services/walletNotify.js` - Email notifications
- `/src/services/user.js` - User profile service

**Configuration:**
- `/config/default.js` - Service configuration
- Database schemas: `user_wallet`, `points_transaction`, `purchase_transaction`

## 📈 Use Cases

**Daily Operations:**
- Users purchasing coins for mobility services
- Auto-refill triggering when balance drops
- Admin adjusting balances for customer service
- Processing refunds for cancelled services

**Integration Scenarios:**
- Mobile app requesting wallet balance
- Transit system deducting fare costs
- Parking service charging fees
- Promotional campaigns adding bonus coins

**Scaling Considerations:**
- Database connection pooling for high concurrency
- Caching wallet balances for frequent reads
- Async processing for non-critical operations

## 🛠️ Improvement Suggestions

**Performance Optimizations:**
- Add wallet balance caching (Redis) - 50% faster reads
- Implement batch transaction processing
- Add database indexes on user_id + created_on

**Feature Enhancements:**
- Multi-currency support expansion
- Real-time balance notifications
- Transaction categorization and analytics
- Integration with more payment providers

**Security Improvements:**
- Enhanced fraud detection algorithms
- PCI compliance documentation
- Audit trail for all balance changes

## 🏷️ Document Tags

**Keywords:** wallet, coins, points, balance, stripe, payment, transaction, auto-refill, refill, tokens, escrow, purchase, redemption, mobility, finance, currency, charge, credit, debit

**Technical Tags:** #wallet-service #payment-processing #stripe-integration #koa-service #mysql-transactions #double-entry-bookkeeping #auto-refill #coin-management

**Target Roles:** Backend developers (intermediate), DevOps engineers, Payment system integrators, Mobile app developers

**Difficulty Level:** ⭐⭐⭐⭐ (High - Financial transactions, complex business logic, external API integration)

**Maintenance Level:** High (Payment processing, regulatory compliance, security updates)

**Business Criticality:** Critical (Core monetization system, user payments, regulatory compliance)

**Related Topics:** Payment processing, Financial services, Mobile payments, Transportation technology, API integration, Database transactions, Security compliance