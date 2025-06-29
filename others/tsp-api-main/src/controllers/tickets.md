# TSP API Tickets Controller Documentation

## 🔍 Quick Summary (TL;DR)
The tickets controller manages transit ticket purchasing, payment processing, and ticket search functionality for mobile transit ticketing systems.

**Keywords:** transit-tickets | ticket-payment | mobile-ticketing | transit-wallet | ticket-search | fare-payment | public-transit | ticket-purchase

**Primary use cases:** Searching available ticket types, processing ticket payments, retrieving payment history, managing transit wallet transactions

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, transit ticketing APIs

## ❓ Common Questions Quick Index
- **Q: What ticket types can be searched?** → Based on searchType parameter (various transit products)
- **Q: How are tickets paid for?** → Currently disabled - returns error immediately
- **Q: What payment methods are supported?** → Wallet-based payments with user verification
- **Q: Can I view payment history?** → Yes, via `/wallet/payments` endpoint
- **Q: Is user blocking supported?** → Yes, blocked users cannot make payments
- **Q: What happens if payment fails?** → Returns specific error codes based on failure type

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as the **ticket booth for your phone**. When you want to buy bus or train tickets, this controller helps you see what tickets are available, handles your payment, and keeps track of your ticket purchases. It's like having a digital ticket counter that can show you all available fares and process your payment securely.

**Technical explanation:** 
A Koa.js REST controller that provides comprehensive transit ticketing functionality including ticket search, payment processing, and transaction history. Integrates with wallet services for user verification and supports multiple payment types with detailed error handling for transit-specific scenarios.

**Business value explanation:**
Enables mobile-first transit ticketing solutions that increase fare collection efficiency, reduce operational costs for transit agencies, and provide convenient payment options for passengers. Supports revenue optimization through digital payment processing and user engagement tracking.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/tickets.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** Transit Ticketing Controller
- **File Size:** ~3.0 KB
- **Complexity Score:** ⭐⭐⭐ (Medium - Payment processing with user verification)

**Dependencies:**
- `@maas/core/bootstrap`: Application initialization (**Critical**)
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `@app/src/middlewares/auth`: JWT authentication (**Critical**)
- `@maas/core/response`: Standardized response formatting (**High**)
- `@app/src/services/tickets`: Core ticketing business logic (**Critical**)
- `@app/src/services/wallet`: User wallet verification (**Critical**)
- `@maas/core/log`: Logging infrastructure (**High**)

## 📝 Detailed Code Analysis

### Find Payments Endpoint (`GET /wallet/payments`)

**Purpose:** Retrieves user's payment history and transaction records

**Flow:**
1. **Authentication:** JWT validation via auth middleware
2. **User Context:** Extracts userId from request headers
3. **Payment Retrieval:** Calls getPayment service with user context
4. **Response:** Returns payment history in standardized format

**Implementation:**
```javascript
const response = await getPayment({
  ctx,
  user_id: ctx.request.headers.userid,
});
ctx.body = success({
  payments: response,
});
```

### Find Tickets Endpoint (`GET /tickets/search`)

**Purpose:** Searches available ticket products based on specified criteria

**Flow:**
1. **Authentication:** JWT validation required
2. **Query Parsing:** Extracts search type from query parameters
3. **Product Search:** Delegates to searchProduct service
4. **Response:** Returns filtered ticket list

**Search Parameters:**
```javascript
const type = ctx.request.query.type;
const response = await searchProduct({
  ctx,
  searchType: type,
  user_id: ctx.request.header.userid,
});
```

### Pay Tickets Endpoint (`POST /tickets/pay`)

**Purpose:** Processes ticket purchase payments
**Status:** ⚠️ **CURRENTLY DISABLED** - Returns error immediately

**Intended Flow (when enabled):**
1. **Authentication:** JWT validation required
2. **User Verification:** Checks if user is blocked (for free payments)
3. **Payment Processing:** Constructs payment bean with all required data
4. **Transaction:** Processes payment through payTicket service
5. **Response:** Returns payment confirmation or detailed error

**Payment Bean Structure:**
```javascript
const bean = {
  payment_id: ctx.request.body.payment_id,
  payment_type: ctx.request.body.payment_type,
  items: ctx.request.body.items,
  user_id: userId,
  zone: ctx.request.headers.zone || 'America/Chicago',
  ctx: ctx
};
```

## 🚀 Usage Methods

### Search Available Tickets
```bash
curl -X GET "https://api.tsp.example.com/api/v2/tickets/search?type=bus_pass" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"
```

### Search by Ticket Type
```bash
# Search for different ticket types
curl -X GET "https://api.tsp.example.com/api/v2/tickets/search?type=single_ride" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"

curl -X GET "https://api.tsp.example.com/api/v2/tickets/search?type=day_pass" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"
```

### Get Payment History
```bash
curl -X GET "https://api.tsp.example.com/api/v2/wallet/payments" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"
```

### Pay for Tickets (Currently Disabled)
```bash
# This will return an error - endpoint is disabled
curl -X POST "https://api.tsp.example.com/api/v2/tickets/pay" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "payment_id": 1,
    "payment_type": "credit_card",
    "items": [
      {
        "ticket_type": "single_ride",
        "quantity": 1,
        "price": 2.50
      }
    ]
  }'
```

## 📊 Output Examples

### Successful Ticket Search
```json
{
  "result": "success",
  "data": {
    "list": [
      {
        "id": 1,
        "name": "Single Ride",
        "price": 2.50,
        "description": "One-time transit ticket",
        "validity": "2 hours",
        "zones": ["A", "B"]
      },
      {
        "id": 2,
        "name": "Day Pass",
        "price": 8.00,
        "description": "Unlimited rides for one day",
        "validity": "24 hours",
        "zones": ["A", "B", "C"]
      }
    ]
  }
}
```

### Payment History Response
```json
{
  "result": "success",
  "data": {
    "payments": [
      {
        "id": 101,
        "amount": 8.00,
        "payment_type": "credit_card",
        "ticket_type": "day_pass",
        "timestamp": "2024-06-25T10:30:00Z",
        "status": "completed"
      },
      {
        "id": 100,
        "amount": 2.50,
        "payment_type": "wallet",
        "ticket_type": "single_ride",
        "timestamp": "2024-06-24T15:45:00Z",
        "status": "completed"
      }
    ]
  }
}
```

### Payment Endpoint Error (Current Status)
```json
{
  "error": "ERROR_TRANSIT_TICKET_SYSTEM",
  "message": "Transit ticket system error",
  "code": 400
}
```

### User Blocked Error
```json
{
  "error": "ERROR_USER_COIN_SUSPENDED",
  "message": "User account suspended for coin transactions",
  "code": 400
}
```

## ⚠️ Important Notes

### Payment Endpoint Status
- **Currently Disabled:** The pay_tickets endpoint immediately throws an error
- **Error Code Mismatch:** Returns `ERROR_UBER_DETAIL` instead of ticket-related error
- **Commented Code:** Implementation exists but is unreachable due to immediate error
- **Activation Required:** Endpoint needs error removal to become functional

### Error Handling Strategy
The controller implements sophisticated error handling with specific error codes:
- `ERROR_TRANSIT_TICKET_TRANSACTION`: Transaction processing failures
- `ERROR_TRANSIT_TICKET_PAYMENT`: Payment method issues
- `ERROR_USER_COIN_SUSPENDED`: User account restrictions
- `ERROR_REDEEM_DAILY_LIMIT`: Daily transaction limits exceeded
- `ERROR_TRANSIT_TICKET_SYSTEM`: General system errors

### User Verification
- **Blocked User Check:** Applied only for payment_id = 0 (free tickets)
- **Authentication Required:** All endpoints require valid JWT tokens
- **User Context:** userId extracted from headers for all operations

### Timezone Support
- **Default Zone:** 'America/Chicago' if not specified
- **Header Override:** Timezone can be set via 'zone' header
- **Payment Processing:** Timezone affects transaction timestamps

### Commented Features
The code contains commented endpoints that suggest additional functionality:
- `find_park_ride_tickets`: Park and ride ticket search
- `pass_use`: Ticket usage/activation

These may represent future features or deprecated functionality.

### Payment Types
Based on the payment processing logic, the system supports:
- Credit card payments
- Wallet-based payments
- Free ticket redemption (with user verification)
- Multiple item purchases in single transaction

## 🔗 Related File Links

- **Tickets Service:** `allrepo/connectsmart/tsp-api/src/services/tickets.js`
- **Wallet Service:** `allrepo/connectsmart/tsp-api/src/services/wallet.js`
- **Error Codes:** `allrepo/connectsmart/tsp-api/src/static/error-code.js`
- **Authentication:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`

---
*This controller provides essential transit ticketing functionality with comprehensive payment processing and user verification capabilities.*