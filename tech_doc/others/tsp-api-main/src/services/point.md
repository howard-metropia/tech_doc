# TSP API Point Service Documentation

## 🔍 Quick Summary (TL;DR)
The Point service manages digital currency transactions for purchasing points/coins through Stripe payment processing, including product validation, daily limits, exclusive user checks, payment processing, and transaction logging with comprehensive fraud prevention mechanisms.

**Keywords:** points-purchase | digital-currency | stripe-payments | transaction-processing | daily-limits | exclusive-products | fraud-prevention | wallet-management

**Primary use cases:** Buying points with real money, checking user point balance, processing Stripe payments, enforcing purchase limits, managing exclusive product access, transaction logging

**Compatibility:** Node.js >= 16.0.0, Stripe payment integration, MySQL database, MongoDB for app states, comprehensive error handling

## ❓ Common Questions Quick Index
- **Q: What payment methods are supported?** → Stripe credit card payments and transaction tokens
- **Q: Are there purchase limits?** → Yes, daily coin purchase limits with potential user blocking
- **Q: What are exclusive products?** → Products only available to specific whitelisted users
- **Q: How is fraud prevented?** → User blocking, daily limits, suspicious activity detection
- **Q: Are transactions logged?** → Comprehensive logging in multiple tables for audit trail
- **Q: Can users check their balance?** → Yes, simple balance lookup from user wallet

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **digital coin store** where users can buy virtual coins with real money using their credit card. The system checks if they're allowed to buy (not blocked, within daily limits), processes the payment through Stripe, adds coins to their wallet, and keeps detailed records of every transaction for security and accounting.

**Technical explanation:** 
A comprehensive digital currency purchase system that handles Stripe payment processing, product validation, user authorization checks, daily purchase limits, exclusive access controls, and multi-table transaction logging. Implements fraud prevention through user blocking mechanisms and suspicious activity detection.

**Business value explanation:**
Enables monetization through digital currency sales, provides secure payment processing with fraud protection, supports exclusive product offerings for premium users, maintains comprehensive audit trails for compliance, and creates recurring revenue streams through point-based transactions.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/point.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with Stripe integration
- **Type:** Digital Currency and Payment Processing Service
- **File Size:** ~4.9 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High - Complex payment processing with fraud prevention)

**Dependencies:**
- `@maas/core/mysql`: Database connectivity (**Critical**)
- `@maas/core/log`: Logging infrastructure (**High**)
- `@app/src/models/AppStates`: User location tracking (**Medium**)
- `@app/src/services/wallet`: Payment and transaction services (**Critical**)
- Stripe payment processing integration (**Critical**)

## 📝 Detailed Code Analysis

### buyPointProduct Function

**Purpose:** Processes point purchase transactions with comprehensive validation and fraud prevention

**Parameters:**
- `data.userId`: Number - User identifier
- `data.product_id`: Number - Points store product ID
- `data.transaction_token`: String - Stripe payment token (optional)
- `data.payment_way`: String - Payment method preference (optional)
- `data.lat`: Number - User latitude (optional)
- `data.lon`: Number - User longitude (optional)

**Returns:** Promise resolving to user's new balance

**Complex Validation Flow:**

### 1. User Security Checks
```javascript
await checkBlockUser(data.userId);
```
- Verifies user is not blocked for suspicious activity
- Throws error if user is blocked from purchases

### 2. Location Tracking
```javascript
const [lastAppLocation] = await AppStates.find({ user_id: data.userId })
  .sort({ timestamp: -1 })
  .limit(1);
```
- Uses last known app location if coordinates not provided
- Important for fraud detection and analytics

### 3. Product Validation
```javascript
const row = await knex('points_store').where({ id: data.product_id }).first();

if (now < row.started_on || (!!row.ended_on && row.ended_on < now)) {
  throw new MaasError(ERROR_CODE.ERROR_POINT_PRODUCT_EXPIRED, ...);
}
```
- Validates product exists and is within active date range
- Checks product availability timeframe

### 4. Exclusive Product Access
```javascript
if (row.sales_type === salesType.SALE_TYPE_EXCLUSIVE) {
  const exu = await knex('exclusive_user').where({
    points_store_id: data.product_id,
    user_id: data.userId,
  });
  if (exu.length === 0) {
    throw new MaasError(ERROR_CODE.ERROR_POINT_PRODUCT_NOT_FOUND, ...);
  }
}
```
- Restricts exclusive products to whitelisted users only
- Ensures only authorized users can purchase premium products

### 5. Daily Limit Enforcement
```javascript
const exceed = await exceedCoinDailyLimit(data.userId, row.points);
if (exceed) {
  const whether = await whetherToBlock(data.userId, Number(row.points));
  if (whether) {
    throw new MaasError(ERROR_CODE.ERROR_USER_COIN_SUSPENDED, ...);
  } else {
    throw new MaasError(ERROR_CODE.ERROR_COIN_PURCHASE_DAILY_LIMIT, ...);
  }
}
```
- Checks if purchase would exceed daily coin limits
- May result in user blocking for suspicious activity
- Implements two-tier response: warning vs blocking

### 6. Payment Processing
```javascript
const charge = await stripeCharge(
  Number(row.amount),
  'usd',
  Number(row.points),
  data.userId,
  customerId,
  data.transaction_token,
);
```
- Processes payment through Stripe
- Supports both customer ID and transaction token methods
- Captures transaction ID and payment method details

### 7. Transaction Recording
```javascript
const { balance, _id } = await pointsTransaction(
  data.userId,
  ACTIVITY_TYPE_PURCHASE,
  Number(row.points),
  note,
  false,
  now,
);
```
- Records transaction in points system
- Updates user wallet balance
- Creates audit trail entry

### 8. Multi-Table Logging
```javascript
if (targetTable === 'points_transaction') {
  await knex('purchase_transaction').insert({...});
} else {
  await knex('purchase_transaction_upgrade').insert({...});
}
```
- Logs purchase in appropriate transaction table
- Maintains comprehensive purchase history
- Supports database upgrade scenarios

### 9. Analytics and Tracking
```javascript
await knex('app_data').insert({
  user_id: data.userId,
  user_action: 'PurchasePoints',
  ref_id: transactionId,
  points: row.points,
  price: row.amount,
  lat,
  lon,
  email: user.email,
  gmt_time: now,
  local_time: now,
});
```
- Records purchase event for analytics
- Includes location data for fraud detection
- Links to Stripe transaction ID

### getPoint Function

**Purpose:** Retrieves user's current point balance

**Parameters:**
- `userId`: Number - User identifier

**Returns:** Promise resolving to balance object

**Simple Implementation:**
```javascript
const uw = await knex('user_wallet').where({ user_id: userId }).first();
return uw ? { balance: Number(uw.balance) } : { balance: 0 };
```

## 🚀 Usage Methods

### Basic Point Purchase
```javascript
const pointService = require('@app/src/services/point');

async function purchasePoints(userId, productId, paymentToken) {
  try {
    const purchaseData = {
      userId: userId,
      product_id: productId,
      transaction_token: paymentToken,
      payment_way: 'stripe',
      lat: 29.7604,
      lon: -95.3698
    };
    
    const result = await pointService.buyPointProduct(purchaseData);
    
    console.log('Purchase successful:');
    console.log('New balance:', result.balance);
    
    return {
      success: true,
      newBalance: result.balance,
      message: 'Points purchased successfully'
    };
  } catch (error) {
    console.error('Purchase failed:', error.message);
    
    return {
      success: false,
      error: error.code || 'PURCHASE_FAILED',
      message: error.message,
      statusCode: error.statusCode || 500
    };
  }
}

// Usage
const result = await purchasePoints(12345, 1, 'tok_visa_4242');
```

### Point Balance Management
```javascript
class PointBalanceManager {
  constructor() {
    this.pointService = require('@app/src/services/point');
  }

  async getUserBalance(userId) {
    try {
      const balanceData = await this.pointService.getPoint(userId);
      return {
        userId,
        balance: balanceData.balance,
        currency: 'coins',
        lastUpdated: new Date().toISOString()
      };
    } catch (error) {
      console.error('Error getting user balance:', error);
      throw error;
    }
  }

  async checkSufficientFunds(userId, requiredPoints) {
    try {
      const balanceData = await this.getUserBalance(userId);
      
      return {
        userId,
        requiredPoints,
        currentBalance: balanceData.balance,
        hasSufficientFunds: balanceData.balance >= requiredPoints,
        shortfall: Math.max(0, requiredPoints - balanceData.balance)
      };
    } catch (error) {
      console.error('Error checking sufficient funds:', error);
      throw error;
    }
  }

  async formatBalanceForDisplay(userId) {
    try {
      const balanceData = await this.getUserBalance(userId);
      
      return {
        displayBalance: balanceData.balance.toLocaleString(),
        balanceLevel: this.categorizeBalance(balanceData.balance),
        recommendations: this.getTopUpRecommendations(balanceData.balance)
      };
    } catch (error) {
      console.error('Error formatting balance display:', error);
      throw error;
    }
  }

  categorizeBalance(balance) {
    if (balance >= 1000) return 'high';
    if (balance >= 100) return 'medium';
    if (balance >= 10) return 'low';
    return 'empty';
  }

  getTopUpRecommendations(currentBalance) {
    if (currentBalance < 10) {
      return ['Consider purchasing a starter pack', 'Top up to unlock premium features'];
    }
    if (currentBalance < 100) {
      return ['Bulk purchases offer better value', 'Top up before your next trip'];
    }
    return ['You have a healthy balance', 'Consider premium packages for extra value'];
  }
}
```

### Purchase Validation and Error Handling
```javascript
class PurchaseValidator {
  constructor() {
    this.pointService = require('@app/src/services/point');
    this.knex = require('@maas/core/mysql')('portal');
  }

  async validatePurchaseRequest(userId, productId) {
    const validation = {
      valid: true,
      errors: [],
      warnings: [],
      productInfo: null
    };

    try {
      // Check product exists and is active
      const product = await this.knex('points_store')
        .where({ id: productId })
        .first();

      if (!product) {
        validation.valid = false;
        validation.errors.push('Product not found');
        return validation;
      }

      validation.productInfo = {
        id: product.id,
        name: product.name,
        points: product.points,
        amount: product.amount,
        currency: product.currency,
        salesType: product.sales_type
      };

      // Check if product is active
      const now = new Date().toISOString().replace('T', ' ').split('.')[0];
      if (now < product.started_on) {
        validation.valid = false;
        validation.errors.push('Product not yet available');
      }

      if (product.ended_on && product.ended_on < now) {
        validation.valid = false;
        validation.errors.push('Product expired');
      }

      // Check exclusive access
      if (product.sales_type === 'exclusive') {
        const hasAccess = await this.checkExclusiveAccess(userId, productId);
        if (!hasAccess) {
          validation.valid = false;
          validation.errors.push('Product not available to this user');
        }
      }

      // Check daily limits (warning only)
      const wouldExceedLimit = await this.checkDailyLimitImpact(userId, product.points);
      if (wouldExceedLimit) {
        validation.warnings.push('Purchase may trigger daily limit restrictions');
      }

      return validation;
    } catch (error) {
      validation.valid = false;
      validation.errors.push(`Validation error: ${error.message}`);
      return validation;
    }
  }

  async checkExclusiveAccess(userId, productId) {
    const access = await this.knex('exclusive_user')
      .where({
        points_store_id: productId,
        user_id: userId
      })
      .first();

    return !!access;
  }

  async checkDailyLimitImpact(userId, points) {
    // This would use the same logic as exceedCoinDailyLimit
    // but return a boolean rather than throwing an error
    try {
      const { exceedCoinDailyLimit } = require('@app/src/services/wallet');
      return await exceedCoinDailyLimit(userId, points);
    } catch (error) {
      return false; // Assume no limit if check fails
    }
  }

  async getPurchaseRecommendations(userId) {
    try {
      const activeProducts = await this.knex('points_store')
        .where('started_on', '<=', this.knex.fn.now())
        .andWhere(function() {
          this.whereNull('ended_on').orWhere('ended_on', '>', this.knex.fn.now());
        })
        .orderBy('points', 'asc');

      const recommendations = [];

      for (const product of activeProducts) {
        const validation = await this.validatePurchaseRequest(userId, product.id);
        
        if (validation.valid) {
          recommendations.push({
            ...validation.productInfo,
            valueRatio: (product.points / product.amount).toFixed(2),
            recommended: this.calculateRecommendationScore(product)
          });
        }
      }

      // Sort by recommendation score
      recommendations.sort((a, b) => b.recommended - a.recommended);

      return recommendations;
    } catch (error) {
      console.error('Error getting purchase recommendations:', error);
      return [];
    }
  }

  calculateRecommendationScore(product) {
    // Higher score for better value and popular amounts
    let score = product.points / product.amount; // Points per dollar
    
    // Bonus for common purchase amounts
    if (product.points >= 100 && product.points <= 500) score += 0.5;
    if (product.points >= 1000) score += 0.3;
    
    return score;
  }
}
```

### Purchase Analytics and Monitoring
```javascript
class PurchaseAnalytics {
  constructor() {
    this.knex = require('@maas/core/mysql')('portal');
  }

  async getUserPurchaseHistory(userId, limit = 10) {
    try {
      const purchases = await this.knex('purchase_transaction')
        .where('user_id', userId)
        .orderBy('created_on', 'desc')
        .limit(limit)
        .select('*');

      return purchases.map(purchase => ({
        id: purchase.id,
        points: purchase.points,
        amount: purchase.amount,
        currency: purchase.currency,
        transactionId: purchase.transaction_id,
        date: purchase.created_on,
        type: 'purchase'
      }));
    } catch (error) {
      console.error('Error getting purchase history:', error);
      throw error;
    }
  }

  async getPurchaseStatistics(userId, days = 30) {
    try {
      const startDate = new Date();
      startDate.setDate(startDate.getDate() - days);

      const stats = await this.knex('purchase_transaction')
        .where('user_id', userId)
        .where('created_on', '>=', startDate.toISOString().split('T')[0])
        .select(
          this.knex.raw('COUNT(*) as purchase_count'),
          this.knex.raw('SUM(points) as total_points'),
          this.knex.raw('SUM(amount) as total_spent'),
          this.knex.raw('AVG(amount) as avg_purchase'),
          this.knex.raw('MAX(amount) as largest_purchase')
        )
        .first();

      return {
        userId,
        period: `${days} days`,
        statistics: {
          purchaseCount: parseInt(stats.purchase_count),
          totalPointsEarned: parseInt(stats.total_points || 0),
          totalAmountSpent: parseFloat(stats.total_spent || 0),
          averagePurchase: parseFloat(stats.avg_purchase || 0),
          largestPurchase: parseFloat(stats.largest_purchase || 0)
        }
      };
    } catch (error) {
      console.error('Error getting purchase statistics:', error);
      throw error;
    }
  }

  async detectSuspiciousActivity(userId) {
    try {
      const today = new Date().toISOString().split('T')[0];
      
      // Check for unusual purchase patterns
      const todayPurchases = await this.knex('purchase_transaction')
        .where('user_id', userId)
        .where('created_on', '>=', today)
        .count('* as count')
        .sum('amount as total_amount')
        .first();

      const avgDailySpending = await this.knex('purchase_transaction')
        .where('user_id', userId)
        .where('created_on', '>=', 
          new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0])
        .avg('amount as avg_amount')
        .first();

      const suspiciousFlags = [];

      // Flag high frequency
      if (parseInt(todayPurchases.count) > 5) {
        suspiciousFlags.push('High purchase frequency today');
      }

      // Flag high spending
      const todayAmount = parseFloat(todayPurchases.total_amount || 0);
      const avgAmount = parseFloat(avgDailySpending.avg_amount || 0);
      
      if (avgAmount > 0 && todayAmount > avgAmount * 3) {
        suspiciousFlags.push('Spending significantly above average');
      }

      return {
        userId,
        suspicious: suspiciousFlags.length > 0,
        flags: suspiciousFlags,
        todayActivity: {
          purchases: parseInt(todayPurchases.count),
          totalSpent: todayAmount
        },
        benchmarks: {
          averageDailySpending: avgAmount
        }
      };
    } catch (error) {
      console.error('Error detecting suspicious activity:', error);
      throw error;
    }
  }

  async generatePurchaseReport(startDate, endDate) {
    try {
      const purchases = await this.knex('purchase_transaction')
        .whereBetween('created_on', [startDate, endDate])
        .select(
          this.knex.raw('DATE(created_on) as purchase_date'),
          this.knex.raw('COUNT(*) as transaction_count'),
          this.knex.raw('SUM(points) as total_points_sold'),
          this.knex.raw('SUM(amount) as total_revenue'),
          this.knex.raw('COUNT(DISTINCT user_id) as unique_buyers')
        )
        .groupBy(this.knex.raw('DATE(created_on)'))
        .orderBy('purchase_date', 'desc');

      const summary = await this.knex('purchase_transaction')
        .whereBetween('created_on', [startDate, endDate])
        .select(
          this.knex.raw('COUNT(*) as total_transactions'),
          this.knex.raw('SUM(points) as total_points'),
          this.knex.raw('SUM(amount) as total_revenue'),
          this.knex.raw('COUNT(DISTINCT user_id) as total_buyers'),
          this.knex.raw('AVG(amount) as avg_transaction_amount')
        )
        .first();

      return {
        reportPeriod: { startDate, endDate },
        summary: {
          totalTransactions: parseInt(summary.total_transactions),
          totalPointsSold: parseInt(summary.total_points),
          totalRevenue: parseFloat(summary.total_revenue),
          uniqueBuyers: parseInt(summary.total_buyers),
          avgTransactionAmount: parseFloat(summary.avg_transaction_amount)
        },
        dailyBreakdown: purchases.map(day => ({
          date: day.purchase_date,
          transactions: parseInt(day.transaction_count),
          pointsSold: parseInt(day.total_points_sold),
          revenue: parseFloat(day.total_revenue),
          uniqueBuyers: parseInt(day.unique_buyers)
        }))
      };
    } catch (error) {
      console.error('Error generating purchase report:', error);
      throw error;
    }
  }
}
```

## 📊 Output Examples

### Successful Purchase Response
```json
{
  "balance": 1250
}
```

### Purchase Validation Result
```json
{
  "valid": true,
  "errors": [],
  "warnings": ["Purchase may trigger daily limit restrictions"],
  "productInfo": {
    "id": 1,
    "name": "Starter Pack",
    "points": 100,
    "amount": 4.99,
    "currency": "USD",
    "salesType": "general"
  }
}
```

### User Balance Response
```json
{
  "balance": 750
}
```

### Purchase History
```json
[
  {
    "id": 12345,
    "points": 500,
    "amount": 19.99,
    "currency": "USD",
    "transactionId": "txn_1234567890",
    "date": "2024-06-25T14:30:00Z",
    "type": "purchase"
  },
  {
    "id": 12344,
    "points": 100,
    "amount": 4.99,
    "currency": "USD", 
    "transactionId": "txn_0987654321",
    "date": "2024-06-20T10:15:00Z",
    "type": "purchase"
  }
]
```

### Purchase Recommendations
```json
[
  {
    "id": 3,
    "name": "Value Pack",
    "points": 500,
    "amount": 19.99,
    "currency": "USD",
    "valueRatio": "25.01",
    "recommended": 25.51
  },
  {
    "id": 1,
    "name": "Starter Pack", 
    "points": 100,
    "amount": 4.99,
    "currency": "USD",
    "valueRatio": "20.04",
    "recommended": 20.54
  }
]
```

### Suspicious Activity Detection
```json
{
  "userId": 12345,
  "suspicious": true,
  "flags": [
    "High purchase frequency today",
    "Spending significantly above average"
  ],
  "todayActivity": {
    "purchases": 7,
    "totalSpent": 89.95
  },
  "benchmarks": {
    "averageDailySpending": 15.50
  }
}
```

## ⚠️ Important Notes

### Security and Fraud Prevention
- **User Blocking:** Comprehensive user blocking system for suspicious activity
- **Daily Limits:** Enforced purchase limits with escalating responses
- **Exclusive Access:** Whitelist-based access control for premium products
- **Location Tracking:** Geographic data collection for fraud analysis

### Payment Processing
- **Stripe Integration:** Full Stripe payment processing with error handling
- **Token Support:** Supports both customer IDs and one-time tokens
- **Transaction Linking:** Links internal transactions to Stripe transaction IDs
- **Payment Method Tracking:** Records payment method details for user convenience

### Data Integrity and Audit Trail
- **Multi-Table Logging:** Comprehensive logging across multiple database tables
- **Transaction Atomicity:** Ensures data consistency across payment and wallet systems
- **Analytics Integration:** Detailed event logging for business intelligence
- **Upgrade Support:** Database schema upgrade compatibility

### Error Handling
- **Comprehensive Error Codes:** Specific error codes for different failure scenarios
- **User-Friendly Messages:** Clear error messages for different failure types
- **Graceful Degradation:** Service continues operation despite non-critical failures
- **Detailed Logging:** Full stack traces and context for debugging

### Performance Considerations
- **Database Optimization:** Efficient queries with proper indexing
- **Stripe API Efficiency:** Optimized Stripe API usage to minimize costs
- **Transaction Speed:** Fast transaction processing for better user experience
- **Concurrent Handling:** Safe handling of concurrent purchase attempts

### Business Logic
- **Product Lifecycle:** Support for time-limited product availability
- **Exclusive Products:** Premium product access control
- **Flexible Pricing:** Support for different currencies and pricing models
- **Purchase Analytics:** Comprehensive tracking for business intelligence

### Compliance and Audit
- **Financial Records:** Complete financial transaction audit trail
- **User Activity Tracking:** Detailed user activity logging
- **Regulatory Compliance:** Structured data for financial compliance reporting
- **Data Retention:** Proper data retention for legal requirements

## 🔗 Related File Links

- **Wallet Service:** `allrepo/connectsmart/tsp-api/src/services/wallet.js`
- **Error Codes:** `allrepo/connectsmart/tsp-api/src/static/error-code.js`
- **App States Model:** `allrepo/connectsmart/tsp-api/src/models/AppStates.js`
- **Sales Type Definitions:** `allrepo/connectsmart/tsp-api/src/static/defines.js`

---
*This service provides essential digital currency purchase capabilities with comprehensive fraud prevention, payment processing, and transaction management for the TSP platform.*