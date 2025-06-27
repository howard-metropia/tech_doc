# TSP API Redeem Controller Documentation

## 🔍 Quick Summary (TL;DR)
The redeem controller handles the redemption of rewards, points, or gift cards within the TSP platform, integrating with wallet services to ensure users aren't blocked before processing redemption requests.

**Keywords:** redeem | redemption | rewards | gift-cards | points | wallet-integration | user-verification | loyalty-rewards | reward-fulfillment

**Primary use cases:** Redeeming loyalty points for rewards, gift card redemption, reward fulfillment, wallet verification

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, @koa/router v10.x

## ❓ Common Questions Quick Index
- **Q: How do I redeem my points for rewards?** → [Create Redemption](#create-redemption-post-redeem)
- **Q: What happens if my account is blocked?** → Wallet service blocks redemption for flagged users
- **Q: What types of items can be redeemed?** → Gift cards, discounts, physical rewards (via service configuration)
- **Q: Is there a redemption limit?** → Limits handled by service layer and wallet verification
- **Q: What authentication is required?** → JWT authentication with user context headers
- **Q: How is redemption processed?** → Service layer handles fulfillment and inventory management

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **reward redemption counter** at a store. When you want to exchange your loyalty points for a gift card or reward, this controller acts like the clerk who first checks that your account is in good standing (not blocked for any reason), verifies your redemption request, and then processes the exchange to give you your reward.

**Technical explanation:** 
A minimal Koa.js REST controller that provides redemption functionality for the platform's reward system. It integrates wallet verification to ensure user eligibility, validates redemption requests, and delegates fulfillment processing to the service layer.

**Business value explanation:**
Critical for completing the rewards ecosystem and user engagement cycle. Enables users to receive tangible value from platform participation, increasing loyalty and encouraging continued usage while providing revenue opportunities through premium redemption options.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/redeem.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** Redemption/Rewards Controller
- **File Size:** ~0.7 KB
- **Complexity Score:** ⭐ (Low - Single endpoint with service delegation and basic validation)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `@maas/core/response`: Standardized response formatting (**High**)
- `@app/src/middlewares/auth`: JWT authentication middleware (**Critical**)
- `@app/src/helpers/fields-of-header`: Header field extraction utility (**High**)
- `@app/src/services/wallet`: Wallet and user verification service (**Critical**)
- `@app/src/schemas/redeem`: Input validation schemas (**Critical**)
- `@app/src/services/redeem`: Redemption business logic service (**Critical**)

## 📝 Detailed Code Analysis

### Create Redemption Endpoint (`POST /redeem`)

**Purpose:** Processes reward redemption requests with user verification

**Flow:**
1. **Authentication:** JWT authentication via auth middleware
2. **Input Validation:** Combines header fields and request body for validation
3. **User Verification:** Calls `checkBlockUser(userId)` to ensure account eligibility
4. **Service Delegation:** Passes validated input to redemption service
5. **Response:** Returns service result in standardized success format

**Key Processing Steps:**
```javascript
// 1. Input aggregation and validation
const input = await inputValidator.create.validateAsync({
  ...fetchFieldsFromHeader(ctx.request.header),
  ...ctx.request.body,
});

// 2. Wallet/user status verification
await checkBlockUser(input.userId);

// 3. Service delegation
const result = await service.create(input);
```

### Wallet Integration
- **User Verification:** `checkBlockUser()` prevents blocked users from redeeming
- **Account Status:** Ensures users meet redemption eligibility requirements
- **Fraud Prevention:** Wallet service may block suspicious accounts

### Input Processing
- **Header Extraction:** Uses `fetchFieldsFromHeader()` for user context
- **Body Validation:** Validates redemption request data
- **Combined Validation:** Merges header and body data for comprehensive validation

## 🚀 Usage Methods

### Redeem Gift Card
```bash
curl -X POST "https://api.tsp.example.com/api/v1/redeem" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "item_type": "gift_card",
    "item_id": "gc_starbucks_25",
    "quantity": 1,
    "points_cost": 2500,
    "delivery_method": "email",
    "delivery_address": "user@example.com"
  }'
```

### Redeem Physical Reward
```bash
curl -X POST "https://api.tsp.example.com/api/v1/redeem" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "item_type": "physical_reward",
    "item_id": "backpack_branded",
    "quantity": 1,
    "points_cost": 5000,
    "delivery_method": "shipping",
    "shipping_address": {
      "name": "John Doe",
      "street": "123 Main St",
      "city": "Houston",
      "state": "TX",
      "zip": "77001"
    }
  }'
```

### JavaScript Client Example
```javascript
async function redeemReward(authToken, userId, redemptionData) {
  try {
    const response = await fetch('/api/v1/redeem', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'userid': userId,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(redemptionData)
    });
    
    if (response.ok) {
      const result = await response.json();
      console.log('Redemption successful:', result.data);
      return result.data;
    } else {
      const error = await response.json();
      throw new Error(error.message || 'Redemption failed');
    }
  } catch (error) {
    console.error('Redemption error:', error);
    throw error;
  }
}

// Usage example
const redemption = {
  item_type: 'gift_card',
  item_id: 'gc_amazon_50',
  quantity: 1,
  points_cost: 5000,
  delivery_method: 'email'
};

redeemReward(authToken, userId, redemption);
```

## 📊 Output Examples

### Successful Redemption Response
```json
{
  "result": "success",
  "data": {
    "redemption_id": "redeem_abc123xyz",
    "item_type": "gift_card",
    "item_name": "$25 Starbucks Gift Card",
    "quantity": 1,
    "points_deducted": 2500,
    "remaining_points": 1250,
    "delivery_method": "email",
    "estimated_delivery": "2024-06-25T16:00:00Z",
    "status": "processing",
    "tracking_info": {
      "confirmation_code": "CONF123456",
      "fulfillment_partner": "GiftCardProvider"
    }
  }
}
```

### Blocked User Error
```json
{
  "error": "UserBlockedError",
  "message": "Account is temporarily restricted from redemptions",
  "code": 403
}
```

### Insufficient Points Error
```json
{
  "error": "InsufficientPointsError",
  "message": "Not enough points for this redemption",
  "details": {
    "required_points": 2500,
    "current_points": 1200,
    "shortage": 1300
  }
}
```

### Validation Error
```json
{
  "error": "ValidationError",
  "message": "Invalid redemption request",
  "details": [
    {
      "field": "item_id",
      "message": "item_id is required"
    },
    {
      "field": "delivery_method",
      "message": "delivery_method must be 'email' or 'shipping'"
    }
  ]
}
```

## ⚠️ Important Notes

### User Verification Process
- **Wallet Integration:** `checkBlockUser()` ensures account eligibility
- **Block Reasons:** Users may be blocked for fraud, policy violations, or account issues
- **Real-time Check:** Verification performed for each redemption attempt
- **Security Measure:** Prevents abuse of redemption system

### Redemption Types
- **Digital Rewards:** Gift cards, discount codes, digital content
- **Physical Rewards:** Branded merchandise, promotional items
- **Service Credits:** Platform credits, subscription benefits
- **Experience Rewards:** Event tickets, exclusive access

### Processing Flow
- **Immediate Validation:** Input validation and user verification happen first
- **Asynchronous Fulfillment:** Actual reward fulfillment may be processed asynchronously
- **Status Tracking:** Redemption status tracked through completion
- **Inventory Management:** Service layer handles stock and availability

### Business Logic Features
- **Point Deduction:** Automatic point balance updates
- **Inventory Tracking:** Real-time availability checking
- **Delivery Management:** Multiple delivery methods supported
- **Partner Integration:** May integrate with third-party fulfillment services

### Error Handling
- **Account Blocks:** Graceful handling of restricted accounts
- **Insufficient Funds:** Clear messaging for point shortages
- **Inventory Issues:** Handling of out-of-stock items
- **Service Failures:** Fallback mechanisms for fulfillment issues

## 🔗 Related File Links

- **Redeem Service:** `allrepo/connectsmart/tsp-api/src/services/redeem.js`
- **Wallet Service:** `allrepo/connectsmart/tsp-api/src/services/wallet.js`
- **Validation Schemas:** `allrepo/connectsmart/tsp-api/src/schemas/redeem.js`
- **Authentication:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`
- **Header Helpers:** `allrepo/connectsmart/tsp-api/src/helpers/fields-of-header.js`

---
*This controller provides essential reward redemption functionality for the platform's loyalty and engagement system.*