# TSP API Tickets Service Documentation

## 🔍 Quick Summary (TL;DR)
The Tickets service manages transit ticket purchasing through Bytemark integration, handling payment processing with coins and tokens, product searches with fare categorization, payment method validation, duplicate device checking, and comprehensive order tracking with event logging.

**Keywords:** transit-tickets | bytemark-integration | payment-processing | fare-management | order-tracking | device-fraud-prevention | wallet-integration | event-logging

**Primary use cases:** Purchasing transit tickets with coins or tokens, searching available ticket products, managing payment methods, preventing duplicate device usage, tracking order status

**Compatibility:** Node.js >= 16.0.0, Bytemark payment system, MySQL database, wallet services integration, event tracking system, cache management

## ❓ Common Questions Quick Index
- **Q: What payment methods are supported?** → Coins (user wallet balance) and tokens (agency-specific transit tokens)
- **Q: How are ticket products categorized?** → By search type: bus_metro, park_ride, and all with dynamic pricing
- **Q: What fraud prevention exists?** → Device duplication checking and user blocking validation
- **Q: How are orders processed?** → Two-phase: create order (POST), then complete payment (PUT)
- **Q: What happens when payment fails?** → Comprehensive error handling with specific error codes and rollback
- **Q: How are prices calculated?** → Fetches from bytemark_fare data with sale_price/cost_price logic

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **digital ticket booth** that lets users buy transit tickets using their earned coins or special transit tokens. It shows available ticket types, checks if users have enough money, processes the purchase through the transit system, and keeps track of everything for security and record-keeping.

**Technical explanation:** 
A comprehensive transit ticket purchasing service that integrates with Bytemark payment systems, manages multi-payment-type transactions (coins/tokens), implements fraud prevention through device tracking, provides dynamic product search with fare categorization, and maintains complete order lifecycle tracking with event logging.

**Business value explanation:**
Enables seamless transit ticket purchases with multiple payment options, reduces fraud through device tracking, provides flexible fare management for different transit types, supports revenue tracking through comprehensive order management, and enhances user experience with automated payment processing.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/tickets.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with Knex.js ORM and Bytemark SDK
- **Type:** Transit Ticket Purchase and Management Service
- **File Size:** ~18.1 KB
- **Complexity Score:** ⭐⭐⭐⭐⭐ (Very High - Complex payment processing with multiple integrations)

**Dependencies:**
- `@maas/services/BytemarkManager`: Bytemark payment system integration (**Critical**)
- `@app/src/services/wallet`: Wallet and token management services (**Critical**)
- `@app/src/services/bytemarkCache`: Ticket cache management (**High**)
- `@app/src/models/BytemarkFare`: Fare data model (**Critical**)
- `@app/src/helpers/send-event`: Event tracking system (**High**)
- `@app/src/helpers/insert-app-data`: App analytics tracking (**Medium**)

## 📝 Detailed Code Analysis

### Payment Method Retrieval

### getPayment Function
**Purpose:** Retrieves available payment methods for user including coins and tokens

```javascript
async function getPayment(bean) {
  logger.info(`[service.getPayment] enter, bean: ${JSON.stringify(bean)}`);
  const results = [];
  
  // Get user wallet balance
  const wallet = await knex('user_wallet').where({ user_id: bean.user_id });
  if (wallet.length > 0) {
    results.push({
      payment_id: 0,
      payment_type: 'coins',
      balance: parseFloat(wallet[0].balance),
      service_inbox: 'support@metropia.com',
    });
  } else {
    results.push({
      payment_id: 0,
      payment_type: 'coins',
      balance: 0,
      service_inbox: 'support@metropia.com',
    });
  }
  
  // Get available tokens
  const tokens = await getAvailableToken(bean.user_id);
  if (tokens.length > 0) {
    tokens.forEach((t) => {
      results.push({
        payment_id: t.payment_id,
        payment_type: 'tokens',
        balance: parseFloat(t.balance),
        agency: t.name,
        expire: t.expires,
        service_inbox: 'support@metropia.com',
      });
    });
  }
  
  return results;
}
```

**Payment Features:**
- **Wallet Integration:** Retrieves user coin balance from wallet service
- **Token Support:** Gets all available agency tokens with expiration dates
- **Standardized Response:** Consistent payment method structure
- **Support Information:** Includes service contact for each payment type

### Product Search System

### searchProduct Function
**Purpose:** Searches and categorizes available transit products based on search type

```javascript
async function searchProduct(bean) {
  logger.info(`[service.searchProduct] enter, bean: ${JSON.stringify(bean)}`);
  try {
    const data = await bytemarkFare.find();
    if (!data) {
      logger.warn(`[service.searchProduct] no maas_cache.bytemark_fare data found.`);
      throw new MaasError(
        ERROR_CODE.ERROR_TRANSIT_TICKET_SYSTEM,
        'error',
        'ERROR_TRANSIT_TICKET_SYSTEM',
        400,
      );
    }
    
    // Group products by name
    const ret = data.reduce((p, c) => {
      // Skip day pass if disabled
      if (config.vendor.bytemark.disableDayPass === 'true')
        if (c.name.indexOf('Local Day Pass') > -1) return p;
        
      const name = c.name.indexOf('-') > -1 ? c.name.split('-')[0].trim() : c.name.trim();
      if (!p[name]) p[name] = [];
      p[name].push({
        uuid: c.uuid,
        name: c.name,
        alert: c.alert_message,
        short_description: c.short_description,
        long_description: c.long_description,
        list_price: c.list_price,
        sale_price: c.sale_price,
        cost_price: c.cost_price,
      });
      return p;
    }, {});
    
    let results = [];
    switch (bean.searchType) {
      case 'bus_metro':
        // Bus and metro tickets processing
        break;
      case 'park_ride':
        // Park & ride tickets processing
        break;
      case 'all':
        // All tickets processing
        break;
      default:
        // Default processing
        break;
    }
    
    return results;
  } catch (e) {
    logger.warn(`[service.searchProduct] ${e.message}`);
    throw e;
  }
}
```

### Dynamic Price Selection Logic

#### Bus/Metro Products
```javascript
case 'bus_metro':
  results = Object.keys(ret).reduce((pre, cur) => {
    if (ret[cur].length > 1) {
      if (cur.indexOf('Local Single Ride') > -1 || cur.indexOf('Local Day Pass') > -1) {
        pre.push({
          uuid: ret[cur][0].sale_price === 0 ? ret[cur][0].uuid : ret[cur][1].uuid,
          name: cur,
          type: 'bus_metro',
          description: ret[cur][0].alert,
          sale_price: ret[cur][0].sale_price > 0 
            ? ret[cur][0].sale_price / 100 
            : ret[cur][1].sale_price / 100,
        });
      }
    }
    return pre;
  }, []);
  break;
```
- **Price Selection:** Chooses between different price variants based on sale_price
- **Category Filtering:** Filters for specific transit types
- **Price Conversion:** Converts from cents to dollars (division by 100)
- **Type Classification:** Assigns appropriate product types

### Payment Processing Pipeline

### payTicket Function
**Purpose:** Main payment processing function that coordinates different payment types

```javascript
async function payTicket(bean) {
  logger.info(`[service.payTicket] enter, bean: ${JSON.stringify(bean)}`);
  try {
    const items = bean.items;
    
    // Get user OAuth token
    const tokensData = await knex('bytemark_tokens').where({
      user_id: bean.user_id,
      status: 'used',
    });
    
    // Calculate total price
    const totalPrice = items.reduce((pre, cur) => {
      pre += cur.qty * cur.price;
      return pre;
    }, 0);
    
    let result = {};
    switch (bean.payment_type) {
      case 'coins':
        result = await payByCoins(bean, items, tokensData, totalPrice);
        break;
      case 'tokens':
        result = await payByTokens(bean, items, tokensData, totalPrice);
        break;
      default:
        logger.warn(`[service.payTicket] unknown payment_type.`);
        throw new MaasError(
          ERROR_CODE.ERROR_TRANSIT_TICKET_SYSTEM,
          'error',
          'ERROR_TRANSIT_TICKET_SYSTEM',
          400,
        );
    }
    
    // Refresh ticket cache
    await checkTicketCache(bean.user_id);
    return result;
  } catch (e) {
    logger.warn(`[service.payTicket] ${e.message}`);
    logger.warn(`[service.payTicket] ${e.stack}`);
    throw e;
  }
}
```

**Payment Coordination:**
- **Token Retrieval:** Gets user's Bytemark authentication token
- **Price Calculation:** Sums all item quantities and prices
- **Payment Routing:** Directs to appropriate payment method handler
- **Cache Management:** Updates ticket cache after successful payment

### Coin Payment Processing

### payByCoins Function
**Purpose:** Processes payment using user's coin balance

```javascript
async function payByCoins(bean, items, tokensData, totalPrice) {
  logger.info(`[service.payByCoins] enter, bean: ${JSON.stringify(bean)}, items: ${JSON.stringify(items)}, tokensData: ${JSON.stringify(tokensData)}, totalPrice: ${totalPrice}`);
  try {
    // Check if user is blocked
    await checkBlockUser(bean.user_id);
    
    const ctx = bean.ctx;
    const wallet = await knex('user_wallet').where({ user_id: bean.user_id });
    
    if (!wallet || wallet.length === 0) {
      logger.warn(`[service.payByCoins] error: no user_wallet record or coins balance is zero.`);
      throw new MaasError(
        ERROR_CODE.ERROR_TRANSIT_TICKET_TRANSACTION,
        'error',
        'ERROR_TRANSIT_TICKET_TRANSACTION',
        400,
      );
    }
    
    const balance = wallet[0].balance;
    if (balance < totalPrice / 100) {
      logger.warn(`[service.payByCoins] error: coins insufficient`);
      throw new MaasError(
        ERROR_CODE.ERROR_TRANSIT_TICKET_TRANSACTION,
        'error',
        'ERROR_TRANSIT_TICKET_TRANSACTION',
        400,
      );
    }
    
    // Create order data with zero prices (internal payment)
    const orderData = {
      payment_type: 'NA',
      process: true,
      items: items.reduce((pre, cur) => {
        cur.price = 0; // Set to 0 for internal payment
        pre.push(cur);
        return pre;
      }, []),
      payments: [],
    };
    
    const bytemark = getBytemarkManager(ctx);
    
    // Create order (POST)
    const [uuid, responseData1] = await postOrder(bytemark, tokensData[0].token, orderData);
    
    // Insert order record
    const newOrder = {
      user_id: bean.user_id,
      oauth_token: tokensData[0].token,
      order_uuid: uuid,
      amount: 0,
      card_uuid: '',
      status: 0,
      resultData: JSON.stringify(responseData1),
      postData: JSON.stringify(orderData),
      created_on: tz.utc().format('YYYY-MM-DD HH:mm:ss'),
      modified_on: tz.utc().format('YYYY-MM-DD HH:mm:ss'),
    };
    const [inserted] = await knex('bytemark_orders').insert(newOrder);
    
    // Send event tracking
    await sendEvent([{
      userIds: [bean.user_id],
      eventName: 'transit_ticket',
      eventMeta: {
        action: 'buy',
        bytemark_order_id: inserted,
      },
    }]);
    
    // Complete order (PUT)
    const [result, responseData2] = await putOrder(
      bytemark,
      tokensData[0].token,
      orderData,
      uuid,
      bean.payment_type,
    );
    
    // Update order status
    const updateData = {
      status: result.status,
      resultData: JSON.stringify(responseData2),
      created_on: tz.utc().format('YYYY-MM-DD HH:mm:ss'),
      modified_on: tz.utc().format('YYYY-MM-DD HH:mm:ss'),
    };
    await knex('bytemark_orders').where({ id: inserted }).update(updateData);
    
    // Record payment
    const orderPayment = {
      payment_id: bean.payment_id,
      payment_type: bean.payment_type,
      total_price: totalPrice,
      user_id: bean.user_id,
      order_id: inserted,
      order_uuid: uuid,
    };
    await knex('bytemark_order_payments').insert(orderPayment);
    
    // Deduct coins from wallet
    await pointsTransaction(bean.user_id, 11, 0 - totalPrice, uuid, false);
    
    // Insert app analytics data
    insertAppData(bean.user_id, bean.zone, 'PurchaseTicket');
    
    return result;
  } catch (e) {
    // Handle specific error codes
    if (e.code && [
      ERROR_CODE.ERROR_TRANSIT_TICKET_TRANSACTION,
      ERROR_CODE.ERROR_USER_COIN_SUSPENDED,
      ERROR_CODE.ERROR_REDEEM_DAILY_LIMIT,
    ].indexOf(e.code) > -1) {
      throw e;
    } else {
      logger.warn(`[service.payByCoins] ${e.message}`);
      throw new MaasError(
        ERROR_CODE.ERROR_TRANSIT_TICKET_TRANSACTION,
        'error',
        'ERROR_TRANSIT_TICKET_TRANSACTION',
        400,
      );
    }
  }
}
```

**Coin Payment Features:**
- **Balance Validation:** Checks wallet balance before processing
- **Blocked User Check:** Validates user is not blocked from transactions
- **Two-Phase Processing:** POST order creation followed by PUT completion
- **Zero Price Logic:** Sets item prices to 0 for internal payment processing
- **Transaction Recording:** Comprehensive order and payment tracking
- **Event Logging:** Tracks purchase events for analytics

### Token Payment Processing

### payByTokens Function
**Purpose:** Processes payment using agency transit tokens

```javascript
async function payByTokens(bean, items, tokensData, totalPrice) {
  logger.info(`[service.payByTokens] enter, bean: ${JSON.stringify(bean)}, items: ${JSON.stringify(items)}, tokensData: ${tokensData}, totalPrice: ${totalPrice}`);
  try {
    const ctx = bean.ctx;
    
    // Check for duplicate device usage
    if (await checkDuplicatedDeviceId(bean.user_id)) {
      throw new MaasError(
        ERROR_CODE.ERROR_USER_COIN_SUSPENDED,
        'error',
        'ERROR_USER_COIN_SUSPENDED',
        400,
      );
    }
    
    // Get user's specific token
    const token = await getUserToken(bean.payment_id, bean.user_id);
    logger.info(`[service.payByToken] returned: ${JSON.stringify(token)}`);
    
    token.balance = parseFloat(token.balance);
    token.expires = token.expires.replace(' ', 'T') + 'Z';
    
    // Validate token balance and expiration
    if ((token.balance && token.balance === 0) || new Date(token.expires) <= new Date()) {
      logger.warn(`[service.payByTokens] error: token balance not sufficient or token expired.`);
      throw new MaasError(
        ERROR_CODE.ERROR_TRANSIT_TICKET_PAYMENT,
        'error',
        'ERROR_TRANSIT_TICKET_PAYMENT',
        400,
      );
    }
    
    const balance = parseFloat(token.balance);
    if (balance < totalPrice / 100) {
      logger.warn(`[service.payByTokens] error: token balance insufficient.`);
      throw new MaasError(
        ERROR_CODE.ERROR_TRANSIT_TICKET_PAYMENT,
        'error',
        'ERROR_TRANSIT_TICKET_PAYMENT',
        400,
      );
    }
    
    // Process similar to coins but with token transaction
    // ... order creation and processing logic ...
    
    // Deduct tokens instead of coins
    await tokenTransaction(
      bean.user_id,
      2,
      0 - totalPrice,
      bean.payment_id,
      uuid,
    );
    
    insertAppData(bean.user_id, bean.zone, 'PurchaseTicket');
    
    return result;
  } catch (e) {
    // Error handling similar to coins
    if (e.code && [
      ERROR_CODE.ERROR_TRANSIT_TICKET_PAYMENT,
      ERROR_CODE.ERROR_USER_COIN_SUSPENDED,
    ].indexOf(e.code) > -1) {
      throw e;
    } else {
      logger.warn(`[service.payByTokens] ${e.message}`);
      throw new MaasError(
        ERROR_CODE.ERROR_TRANSIT_TICKET_PAYMENT,
        'error',
        'ERROR_TRANSIT_TICKET_PAYMENT',
        400,
      );
    }
  }
}
```

**Token Payment Features:**
- **Device Duplication Check:** Prevents fraud through device tracking
- **Token Validation:** Checks balance and expiration before processing
- **Expiration Handling:** Proper datetime formatting for expiration checks
- **Token Transaction:** Uses token-specific transaction recording
- **Similar Processing:** Follows same order lifecycle as coin payments

### Device Fraud Prevention

### checkDuplicatedDeviceId Function
**Purpose:** Prevents fraud by checking for duplicate device usage

```javascript
async function checkDuplicatedDeviceId(userId) {
  logger.info(`[checkDuplicatedDeviceId] enter, userId: ${userId}`);
  try {
    const user = await knex('device_check_duplication').where({
      user_id: userId,
      status: 0,
    });
    
    if (user) {
      logger.info(`[checkDuplicatedDeviceId] user exist in list`);
      if (user.length > 0) {
        logger.info(`[checkDuplicatedDeviceId] user length > 1`);
        return true;
      } else {
        return false;
      }
    } else {
      return false;
    }
  } catch (e) {
    logger.warn(`[checkDuplicatedDeviceId] Error: ${e.message}`);
    return false;
  }
}
```
- **Fraud Detection:** Checks for users flagged for duplicate device usage
- **Status Filtering:** Only checks active duplication records (status: 0)
- **Error Handling:** Returns false on error to avoid blocking legitimate users
- **Security Measure:** Prevents token abuse through device sharing

## 🚀 Usage Methods

### Basic Ticket Purchase Flow
```javascript
const ticketsService = require('@app/src/services/tickets');

// Get available payment methods
const paymentMethods = await ticketsService.getPayment({ user_id: 12345 });
console.log('Available payments:', paymentMethods);

// Search for tickets
const tickets = await ticketsService.searchProduct({ 
  searchType: 'bus_metro' 
});
console.log('Available tickets:', tickets);

// Purchase ticket with coins
const purchaseData = {
  user_id: 12345,
  payment_type: 'coins',
  payment_id: 0,
  ctx: requestContext,
  zone: 'houston',
  items: [
    {
      uuid: 'ticket-uuid-123',
      qty: 1,
      price: 250 // Price in cents
    }
  ]
};

const result = await ticketsService.payTicket(purchaseData);
console.log('Purchase result:', result);
```

### Advanced Ticket Management System
```javascript
class TicketPurchaseManager {
  constructor() {
    this.ticketsService = require('@app/src/services/tickets');
    this.purchaseHistory = new Map();
    this.deviceTracker = new Set();
  }

  async validatePurchaseEligibility(userId, paymentType, paymentId) {
    try {
      // Get available payment methods
      const paymentMethods = await this.ticketsService.getPayment({ user_id: userId });
      
      const selectedPayment = paymentMethods.find(p => 
        p.payment_type === paymentType && 
        (paymentType === 'coins' || p.payment_id === paymentId)
      );

      if (!selectedPayment) {
        return {
          eligible: false,
          reason: 'Payment method not available'
        };
      }

      if (selectedPayment.balance <= 0) {
        return {
          eligible: false,
          reason: 'Insufficient balance',
          balance: selectedPayment.balance
        };
      }

      // Check for token expiration
      if (paymentType === 'tokens' && selectedPayment.expire) {
        const expirationDate = new Date(selectedPayment.expire);
        if (expirationDate <= new Date()) {
          return {
            eligible: false,
            reason: 'Token expired',
            expiredOn: selectedPayment.expire
          };
        }
      }

      return {
        eligible: true,
        paymentMethod: selectedPayment,
        availableBalance: selectedPayment.balance
      };
    } catch (error) {
      console.error('Eligibility check failed:', error);
      return {
        eligible: false,
        reason: 'Validation failed',
        error: error.message
      };
    }
  }

  async getRecommendedTickets(searchType, userPreferences = {}) {
    try {
      const allTickets = await this.ticketsService.searchProduct({ searchType });
      
      // Apply user preferences and recommendations
      const recommendations = allTickets.map(ticket => {
        let score = 0;
        
        // Price preference scoring
        if (ticket.sale_price <= (userPreferences.maxPrice || 10)) {
          score += 30;
        }
        
        // Type preference scoring
        if (userPreferences.preferredType && ticket.type === userPreferences.preferredType) {
          score += 40;
        }
        
        // Frequency-based scoring
        if (this.isFrequentlyPurchased(ticket.uuid)) {
          score += 20;
        }
        
        // Day pass value scoring
        if (ticket.name.includes('Day Pass') && userPreferences.multipleTrips) {
          score += 50;
        }

        return {
          ...ticket,
          recommendationScore: score,
          isRecommended: score >= 50
        };
      });

      // Sort by recommendation score
      return recommendations.sort((a, b) => b.recommendationScore - a.recommendationScore);
    } catch (error) {
      console.error('Error getting recommendations:', error);
      return [];
    }
  }

  async processPurchaseWithValidation(purchaseData) {
    try {
      const startTime = Date.now();
      
      // Pre-purchase validation
      const eligibility = await this.validatePurchaseEligibility(
        purchaseData.user_id,
        purchaseData.payment_type,
        purchaseData.payment_id
      );

      if (!eligibility.eligible) {
        return {
          success: false,
          reason: eligibility.reason,
          details: eligibility
        };
      }

      // Calculate total cost
      const totalCost = purchaseData.items.reduce((sum, item) => 
        sum + (item.qty * item.price), 0) / 100;

      if (totalCost > eligibility.availableBalance) {
        return {
          success: false,
          reason: 'Insufficient funds',
          required: totalCost,
          available: eligibility.availableBalance
        };
      }

      // Process the purchase
      const result = await this.ticketsService.payTicket(purchaseData);
      const processingTime = Date.now() - startTime;

      // Track purchase history
      this.trackPurchase(purchaseData.user_id, purchaseData.items, result);

      return {
        success: true,
        result,
        processingTime,
        totalCost,
        remainingBalance: eligibility.availableBalance - totalCost,
        purchaseId: result.result?.bytemark_order_id || null
      };
    } catch (error) {
      console.error('Purchase processing failed:', error);
      return {
        success: false,
        reason: 'Purchase failed',
        error: error.message,
        errorCode: error.code
      };
    }
  }

  trackPurchase(userId, items, result) {
    const userHistory = this.purchaseHistory.get(userId) || [];
    
    const purchase = {
      timestamp: new Date(),
      items: items.map(item => ({ uuid: item.uuid, qty: item.qty })),
      success: result.status === 1,
      orderId: result.result?.bytemark_order_id
    };

    userHistory.push(purchase);
    this.purchaseHistory.set(userId, userHistory.slice(-20)); // Keep last 20 purchases
  }

  isFrequentlyPurchased(ticketUuid) {
    let count = 0;
    this.purchaseHistory.forEach(history => {
      count += history.filter(purchase => 
        purchase.items.some(item => item.uuid === ticketUuid)
      ).length;
    });
    return count >= 5; // Frequently purchased if bought 5+ times across all users
  }

  async batchPurchaseTickets(purchases) {
    const results = [];
    
    for (const purchase of purchases) {
      try {
        const result = await this.processPurchaseWithValidation(purchase);
        results.push({
          userId: purchase.user_id,
          ...result
        });
      } catch (error) {
        results.push({
          userId: purchase.user_id,
          success: false,
          error: error.message
        });
      }
    }

    const successful = results.filter(r => r.success).length;
    const failed = results.filter(r => !r.success).length;

    return {
      totalPurchases: purchases.length,
      successful,
      failed,
      successRate: (successful / purchases.length * 100).toFixed(2),
      results
    };
  }

  getUserPurchaseHistory(userId) {
    const history = this.purchaseHistory.get(userId) || [];
    
    const stats = {
      totalPurchases: history.length,
      successfulPurchases: history.filter(p => p.success).length,
      failedPurchases: history.filter(p => !p.success).length,
      favoriteTickets: this.getFavoriteTickets(history),
      recentPurchases: history.slice(-5),
      firstPurchase: history.length > 0 ? history[0].timestamp : null,
      lastPurchase: history.length > 0 ? history[history.length - 1].timestamp : null
    };

    return stats;
  }

  getFavoriteTickets(history) {
    const ticketCounts = {};
    
    history.forEach(purchase => {
      purchase.items.forEach(item => {
        ticketCounts[item.uuid] = (ticketCounts[item.uuid] || 0) + item.qty;
      });
    });

    return Object.entries(ticketCounts)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 3)
      .map(([uuid, count]) => ({ uuid, count }));
  }

  getSystemStatistics() {
    let totalPurchases = 0;
    let totalUsers = this.purchaseHistory.size;
    let totalSuccessful = 0;

    this.purchaseHistory.forEach(history => {
      totalPurchases += history.length;
      totalSuccessful += history.filter(p => p.success).length;
    });

    return {
      totalUsers,
      totalPurchases,
      totalSuccessful,
      successRate: totalPurchases > 0 ? (totalSuccessful / totalPurchases * 100).toFixed(2) : '0.00',
      averagePurchasesPerUser: totalUsers > 0 ? (totalPurchases / totalUsers).toFixed(2) : '0.00'
    };
  }
}

// Usage
const ticketManager = new TicketPurchaseManager();

// Validate purchase eligibility
const eligibility = await ticketManager.validatePurchaseEligibility(12345, 'coins', 0);
console.log('Purchase eligibility:', eligibility);

// Get recommended tickets
const recommendations = await ticketManager.getRecommendedTickets('bus_metro', {
  maxPrice: 5.00,
  preferredType: 'bus_metro',
  multipleTrips: true
});
console.log('Recommended tickets:', recommendations);

// Process purchase with validation
const purchaseResult = await ticketManager.processPurchaseWithValidation({
  user_id: 12345,
  payment_type: 'coins',
  payment_id: 0,
  ctx: requestContext,
  zone: 'houston',
  items: [{ uuid: 'ticket-uuid-123', qty: 1, price: 250 }]
});
console.log('Purchase result:', purchaseResult);
```

## 📊 Output Examples

### Payment Methods Response
```javascript
[
  {
    payment_id: 0,
    payment_type: "coins",
    balance: 15.75,
    service_inbox: "support@metropia.com"
  },
  {
    payment_id: 123,
    payment_type: "tokens",
    balance: 8.00,
    agency: "Houston Metro",
    expire: "2024-12-31T23:59:59Z",
    service_inbox: "support@metropia.com"
  }
]
```

### Ticket Search Results
```javascript
[
  {
    uuid: "local-single-ride-uuid",
    name: "Local Single Ride",
    type: "bus_metro",
    description: "Single ride on local bus or metro",
    sale_price: 1.25
  },
  {
    uuid: "local-day-pass-uuid", 
    name: "Local Day Pass",
    type: "bus_metro",
    description: "Unlimited rides for one day",
    sale_price: 3.00
  }
]
```

### Purchase Success Response
```javascript
{
  status: 1,
  result: {
    payment_type: "coins",
    success: true
  }
}
```

### Purchase Validation Response
```javascript
{
  success: true,
  result: {
    status: 1,
    result: { payment_type: "coins", success: true }
  },
  processingTime: 2340,
  totalCost: 2.50,
  remainingBalance: 13.25,
  purchaseId: 12345
}
```

### System Statistics
```javascript
{
  totalUsers: 1250,
  totalPurchases: 8450,
  totalSuccessful: 8120,
  successRate: "96.10",
  averagePurchasesPerUser: "6.76"
}
```

## ⚠️ Important Notes

### Payment Processing and Security
- **Two-Phase Processing:** POST order creation followed by PUT completion for transaction integrity
- **Balance Validation:** Pre-transaction balance checks prevent insufficient fund errors
- **Device Fraud Prevention:** Duplicate device checking prevents token abuse
- **User Blocking:** Integration with user blocking system for security compliance

### Bytemark Integration Requirements
- **OAuth Token Management:** Requires valid Bytemark authentication tokens
- **Order UUID Tracking:** Maintains unique order identifiers for transaction tracking
- **Error Code Mapping:** Specific error handling for different failure scenarios
- **Price Format:** Handles price conversion between cents (storage) and dollars (display)

### Transaction and Data Management
- **Comprehensive Logging:** Detailed transaction records for audit and debugging
- **Event Tracking:** Purchase events logged for analytics and user behavior analysis
- **Cache Management:** Automatic ticket cache refresh after successful purchases
- **App Data Integration:** Purchase tracking for application analytics

### Search and Product Management
- **Dynamic Categorization:** Products categorized by type (bus_metro, park_ride) with flexible pricing
- **Configuration Control:** Day pass availability controlled through configuration
- **Price Variant Handling:** Complex logic for selecting appropriate price variants
- **Product Grouping:** Intelligent grouping of related fare products

## 🔗 Related File Links

- **Wallet Services:** `allrepo/connectsmart/tsp-api/src/services/wallet.js`
- **Bytemark Cache:** `allrepo/connectsmart/tsp-api/src/services/bytemarkCache.js`
- **Fare Models:** `allrepo/connectsmart/tsp-api/src/models/BytemarkFare.js`
- **Event Helpers:** `allrepo/connectsmart/tsp-api/src/helpers/send-event.js`

---
*This service provides comprehensive transit ticket purchasing with multi-payment support, fraud prevention, and complete transaction management for the TSP platform.*