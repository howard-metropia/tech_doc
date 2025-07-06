# TSP API Promocode Controller Documentation

## 🔍 Quick Summary (TL;DR)
The promocode controller manages promotional code validation and raffle ticket distribution, integrating with an external admin platform to verify codes and provide user rewards through the loyalty system.

**Keywords:** promocode | promo-code | raffle-tickets | rewards | promotional-campaigns | code-validation | loyalty-integration | tier-benefits | admin-platform

**Primary use cases:** Promotional code redemption, raffle ticket distribution, campaign management, user engagement rewards

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, Axios for external API integration

## ❓ Common Questions Quick Index
- **Q: How do I redeem a promotional code?** → [Redeem Promocode](#redeem-promocode-post-promocode)
- **Q: How do I view my raffle tickets?** → [Get Raffle Tickets](#get-raffle-tickets-get-raffle-ticket-list)
- **Q: What happens when I use a promocode?** → Code validation, reward distribution, tier benefit application
- **Q: Where are promocodes validated?** → External admin platform API integration
- **Q: What types of rewards are available?** → Raffle tickets with tier-based magnification
- **Q: Why might a promocode fail?** → Code doesn't exist, expired, already used, or user not found

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **digital coupon redemption system**. When you have a promotional code (like from a marketing campaign), this controller acts like a store cashier who checks if your coupon is valid, hasn't expired, and hasn't been used before. If everything checks out, it gives you rewards like raffle tickets, with VIP customers (higher tier users) getting bonus rewards.

**Technical explanation:** 
A Koa.js REST controller that integrates with an external admin platform to validate promotional codes and distribute rewards. It handles user authentication, tier-based benefit calculation, external API integration, and comprehensive error handling for various promocode validation scenarios.

**Business value explanation:**
Essential for marketing campaigns and user engagement. Enables promotional code distribution for user acquisition, retention campaigns, and loyalty program integration while providing detailed analytics and fraud prevention through external validation.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/promocode.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** External Integration Controller
- **File Size:** ~4.5 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High - External API integration, error handling, tier system integration)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `axios`: HTTP client for external API calls (**Critical**)
- `@maas/core/response`: Standardized response formatting (**High**)
- `@app/src/middlewares/auth`: JWT authentication middleware (**Critical**)
- `@app/src/schemas/promocode`: Input validation schemas (**Critical**)
- `@app/src/services/promocode`: Promocode business logic (**Critical**)
- `@app/src/services/tier`: User tier and benefits service (**Critical**)

## 📝 Detailed Code Analysis

### Available Endpoints

#### Redeem Promocode (`POST /promocode`)
- **Purpose:** Validates and redeems promotional codes for rewards
- **External Integration:** Calls admin platform API for validation
- **Tier Integration:** Applies tier-based benefit magnification
- **Error Handling:** Maps specific promocode errors to user-friendly responses

#### Get Raffle Tickets (`GET /raffle-ticket-list`)
- **Purpose:** Retrieves user's raffle ticket history with pagination
- **External Integration:** Fetches data from admin platform
- **Pagination:** Supports limit, page, and search functionality

### Promocode Validation Flow
```javascript
// 1. User and tier validation
const authUser = await userService.getById(userId);
const tier = await tierService.getUserTier(userId);
const tierBenefits = await tierService.getUserTierBenefits(tier.level);

// 2. External API call with tier magnification
await Axios.post(process.env.ADMIN_PLATFORM_URL + '/promocode/check', 
  { 
    promocode: data.promo_code, 
    magnification: tierBenefits.raffle.magnification 
  },
  { headers: { authorization, user_id: userId, device_id: authUser.device_id } }
);
```

### Error Code Mapping
- **140002/140003:** Code doesn't exist → `ERROR_PROMO_CODE_NOT_EXIST`
- **140005:** Code expired → `ERROR_PROMO_CODE_EXPIRED`  
- **140007/140010:** Already used → `ERROR_PROMO_CODE_ALREADY_USED`
- **Default:** Generic not exist error

## 🚀 Usage Methods

### Redeem Promotional Code
```bash
curl -X POST "https://api.tsp.example.com/api/v2/promocode" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "promo_code": "SUMMER2024"
  }'
```

### Get Raffle Ticket List
```bash
curl -X GET "https://api.tsp.example.com/api/v2/raffle-ticket-list?limit=20&current_page=1&search=SUMMER" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"
```

### JavaScript Client Example
```javascript
async function redeemPromocode(authToken, userId, promoCode) {
  try {
    const response = await fetch('/api/v2/promocode', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'userid': userId,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ promo_code: promoCode })
    });
    
    if (response.ok) {
      const result = await response.json();
      return result.data;
    }
  } catch (error) {
    console.error('Promocode redemption failed:', error);
  }
}

async function getRaffleTickets(authToken, userId, page = 1, limit = 10) {
  try {
    const response = await fetch(`/api/v2/raffle-ticket-list?current_page=${page}&limit=${limit}`, {
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
    console.error('Failed to fetch raffle tickets:', error);
  }
}
```

## 📊 Output Examples

### Successful Promocode Redemption
```json
{
  "result": "success",
  "data": {
    "type": "raffle ticket",
    "toast": "Congratulations! You earned 2x raffle tickets with your Gold tier status!"
  }
}
```

### Raffle Ticket List Response
```json
{
  "result": "success",
  "data": {
    "tickets": [
      {
        "id": "ticket_123",
        "promocode": "SUMMER2024",
        "type": "raffle ticket",
        "quantity": 2,
        "created_at": "2024-06-25T14:30:00Z",
        "campaign": "Summer Promotion"
      }
    ],
    "pagination": {
      "current_page": 1,
      "total_pages": 5,
      "limit": 10
    }
  }
}
```

### Promocode Error Responses
```json
// Code doesn't exist
{
  "error": "ERROR_PROMO_CODE_NOT_EXIST",
  "message": "Promotional code does not exist",
  "code": 200
}

// Code expired
{
  "error": "ERROR_PROMO_CODE_EXPIRED", 
  "message": "Promotional code has expired",
  "code": 200
}

// Already used
{
  "error": "ERROR_PROMO_CODE_ALREADY_USED",
  "message": "Promotional code has already been used",
  "code": 200
}
```

## ⚠️ Important Notes

### External API Integration
- **Admin Platform Dependency:** Relies on external admin platform for validation
- **Environment Configuration:** Uses `ADMIN_PLATFORM_URL` environment variable
- **Authentication Forwarding:** Passes user authentication to external system
- **Device ID Tracking:** Includes device identification for fraud prevention

### Tier System Integration
- **Benefit Magnification:** Higher tier users receive multiplied rewards
- **Dynamic Benefits:** Tier benefits fetched in real-time for each redemption
- **Personalized Messages:** Tier-specific success messages and toasts

### Error Handling Strategy
- **Specific Error Mapping:** Different promocode error codes mapped to specific responses
- **Graceful Degradation:** Network errors handled with generic error responses
- **Logging Integration:** Comprehensive logging for debugging and monitoring
- **User-Friendly Messages:** Technical errors converted to user-understandable messages

### Security Considerations
- **Authentication Required:** All operations require valid JWT tokens
- **External Validation:** Promocode validation handled by secure external system
- **Device Tracking:** Device ID included for security and fraud detection
- **Authorization Forwarding:** Maintains authentication chain to external services

### Business Logic Features
- **Campaign Management:** Supports complex promotional campaigns
- **Usage Tracking:** Prevents duplicate redemptions
- **Expiration Handling:** Automatic expiration date validation
- **Reward Distribution:** Automated reward distribution upon successful validation

## 🔗 Related File Links

- **Promocode Service:** `allrepo/connectsmart/tsp-api/src/services/promocode.js`
- **Tier Service:** `allrepo/connectsmart/tsp-api/src/services/tier.js`
- **User Service:** `allrepo/connectsmart/tsp-api/src/services/user.js`
- **Validation Schemas:** `allrepo/connectsmart/tsp-api/src/schemas/promocode.js`
- **Error Codes:** `allrepo/connectsmart/tsp-api/src/static/error-code.js`

---
*This controller provides essential promotional code management and reward distribution functionality for marketing campaigns and user engagement.*