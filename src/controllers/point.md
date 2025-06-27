# TSP API Points Controller Documentation

## 🔍 Quick Summary (TL;DR)
The points controller manages the loyalty points system, allowing users to view their point balance and purchase point products through the TSP platform's rewards program.

**Keywords:** points | loyalty-program | rewards | point-balance | point-purchase | digital-currency | incentives | user-engagement

**Primary use cases:** Checking point balance, purchasing point packages, reward system management, user engagement incentives

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, @koa/router v10.x

## ❓ Common Questions Quick Index
- **Q: How do I check my point balance?** → [Get Points](#get-points-get-points)
- **Q: How can I buy more points?** → [Buy Point Product](#buy-point-product-post-points)
- **Q: What payment methods are supported for buying points?** → Configured through point purchase service
- **Q: Are points tied to timezone?** → Yes, uses 'America/Chicago' as default timezone
- **Q: What authentication is required?** → JWT authentication with userid header
- **Q: How are points earned besides purchasing?** → Through various platform activities (handled by service layer)

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as your **digital rewards wallet**. Just like earning and spending points at a coffee shop, this controller lets you check how many reward points you have earned through using the transportation services, and lets you buy additional points if you want to. You can then use these points to get discounts, gift cards, or other rewards in the app.

**Technical explanation:** 
A simple Koa.js REST controller that provides read and purchase operations for the platform's loyalty points system. It handles point balance retrieval and point purchasing with timezone-aware processing and input validation.

**Business value explanation:**
Essential for user engagement and retention through gamification and rewards. Points systems increase user loyalty, encourage platform usage, and provide additional revenue streams through point sales.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/point.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** Loyalty/Rewards Controller
- **File Size:** ~0.8 KB
- **Complexity Score:** ⭐ (Low - Simple CRUD operations with service delegation)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `@maas/core/response`: Standardized response formatting (**High**)
- `@app/src/middlewares/auth`: JWT authentication middleware (**Critical**)
- `@app/src/schemas/point`: Input validation schemas (**Critical**)
- `@app/src/services/point`: Points business logic service (**Critical**)

## 📝 Detailed Code Analysis

### Available Endpoints

#### Get Points (`GET /points`)
- **Purpose:** Retrieves user's current point balance and related information
- **Authentication:** Required via JWT token
- **User Context:** Extracts userId from request header
- **Service Call:** Delegates to `getPoint(userId)` service method

#### Buy Point Product (`POST /points`)
- **Purpose:** Allows users to purchase point packages or products
- **Authentication:** Required via JWT token
- **Timezone Handling:** Uses zone header with 'America/Chicago' default
- **Input Validation:** Validates request body against point schema
- **Service Call:** Delegates to `buyPointProduct(data)` with validated input

### Function-Based Architecture
The controller uses separate async functions for each operation:
```javascript
async function getPointAction(ctx) {
  const { userid: userId } = ctx.request.header;
  const result = await getPoint(userId);
  ctx.body = success(result);
}

async function buyPointProductAction(ctx) {
  const { userid: userId } = ctx.request.header;
  const zone = ctx.request.header.zone ?? 'America/Chicago';
  const input = { ...ctx.request.body, userId, zone };
  const data = await inputValidator.post.validateAsync(input);
  const result = await buyPointProduct(data);
  ctx.body = success(result);
}
```

### Input Processing
- **User Identification:** Extracts userId from authentication headers
- **Timezone Awareness:** Processes timezone for transaction timestamping
- **Input Validation:** Comprehensive validation through Joi schemas
- **Service Integration:** Clean delegation to business logic layer

## 🚀 Usage Methods

### Check Point Balance
```bash
curl -X GET "https://api.tsp.example.com/api/v1/points" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"
```

### Purchase Point Package
```bash
curl -X POST "https://api.tsp.example.com/api/v1/points" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "zone: America/Chicago" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "points_100",
    "quantity": 1,
    "payment_method": "credit_card",
    "payment_token": "pm_1abc123"
  }'
```

### JavaScript Client Example
```javascript
async function getPointBalance(authToken, userId) {
  try {
    const response = await fetch('/api/v1/points', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'userid': userId
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      return data.data;
    }
  } catch (error) {
    console.error('Failed to fetch points:', error);
  }
}

async function buyPoints(authToken, userId, productData) {
  try {
    const response = await fetch('/api/v1/points', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'userid': userId,
        'zone': 'America/Chicago',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(productData)
    });
    
    if (response.ok) {
      const result = await response.json();
      return result.data;
    }
  } catch (error) {
    console.error('Point purchase failed:', error);
  }
}
```

## 📊 Output Examples

### Point Balance Response
```json
{
  "result": "success",
  "data": {
    "user_id": "usr_12345",
    "current_balance": 1250,
    "lifetime_earned": 3450,
    "lifetime_spent": 2200,
    "pending_points": 50,
    "expiring_points": {
      "amount": 100,
      "expiry_date": "2024-12-31"
    },
    "tier_status": "silver",
    "next_tier_points": 750
  }
}
```

### Point Purchase Response
```json
{
  "result": "success",
  "data": {
    "transaction_id": "txn_abc123xyz",
    "product_name": "100 Points Package",
    "points_purchased": 100,
    "amount_paid": 9.99,
    "currency": "USD",
    "new_balance": 1350,
    "transaction_date": "2024-06-25T14:30:00Z",
    "payment_method": "credit_card"
  }
}
```

### Validation Error Response
```json
{
  "error": "ValidationError",
  "message": "Invalid point product request",
  "details": [
    {
      "field": "product_id",
      "message": "product_id is required"
    },
    {
      "field": "payment_method",
      "message": "payment_method must be a valid payment type"
    }
  ]
}
```

## ⚠️ Important Notes

### Points System Architecture
- **Balance Tracking:** Real-time point balance management
- **Transaction History:** Complete audit trail of point earnings and spending
- **Expiration Management:** Points may have expiration dates for business policy compliance
- **Tier System:** Point accumulation may unlock different user tiers or benefits

### Timezone Handling
- **Default Timezone:** 'America/Chicago' used when zone header not provided
- **Transaction Timestamping:** All purchases timestamped with user's timezone
- **Consistency:** Ensures consistent time handling across point operations

### Security Considerations
- **Authentication Required:** All operations require valid JWT tokens
- **User Scoping:** All operations scoped to authenticated user
- **Payment Security:** Payment processing handled securely by service layer
- **Input Validation:** Comprehensive validation prevents malformed requests

### Business Logic Integration
- **Point Earning:** Points earned through various platform activities (handled by other services)
- **Point Spending:** Points can be spent on rewards, discounts, gift cards
- **Promotional Systems:** May integrate with promotional campaigns and bonuses
- **Analytics:** Point usage tracked for user engagement analytics

### Payment Integration
- **Multiple Payment Methods:** Supports various payment methods for point purchases
- **Secure Processing:** Payment tokens and sensitive data handled by service layer
- **Transaction Records:** Complete transaction history maintained for accounting

## 🔗 Related File Links

- **Points Service:** `allrepo/connectsmart/tsp-api/src/services/point.js`
- **Validation Schema:** `allrepo/connectsmart/tsp-api/src/schemas/point.js`
- **Authentication:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`

---
*This controller provides essential loyalty points management functionality for user engagement and retention.*