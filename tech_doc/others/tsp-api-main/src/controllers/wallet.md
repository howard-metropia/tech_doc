# Wallet Controller Documentation

## 🔍 Quick Summary (TL;DR)
This controller provides a comprehensive set of endpoints for managing all aspects of a user's wallet, including retrieving points history, getting a summary of all wallet contents (points, tokens), fetching available items in the point store, and managing user-specific wallet settings.

**Keywords:** wallet | points | tokens | incentives | rewards | transaction-history | point-store | user-wallet | digital-currency

**Primary use cases:** 
- Displaying a user's current points and token balances.
- Showing a detailed, paginated history of a user's points transactions.
- Listing items or plans available for purchase or redemption (e.g., refill plans, items in a point store).
- Getting and updating user-specific wallet settings, such as auto-refill.

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x.

## ❓ Common Questions Quick Index
- **Q: How do I get a user's current points balance?** → Use `GET /v2/wallet_summary`.
- **Q: How do I get a user's transaction history?** → Use `GET /v2/point_history` or `POST /v2/point_history`.
- **Q: Why are there v1 and v2 endpoints for the same thing?** → This indicates an evolution of the API. Clients should prefer the latest version (v2).
- **Q: What's the difference between `point_store` and `refill_plan`?** → `point_store` likely lists items redeemable with points, while `refill_plan` lists options to purchase more currency/tokens.
- **Q: How are wallet settings managed?** → `GET /v2/wallet_setting` retrieves them, and `PUT /v2/wallet_setting` updates them.
- **Q: Why does `pointsHistory` support both GET and POST?** → This is a flexible design. `GET` is for simple queries, while `POST` can handle more complex filter bodies if needed in the future.

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this controller as your **personal banker and loyalty program manager**.
- **Account Summary (`/wallet_summary`):** You can ask the banker for your current account statement, and they'll tell you exactly how many reward points and travel tokens you have.
- **Transaction History (`/point_history`):** You can ask for a detailed list of all your recent transactions—where you earned points and where you spent them.
- **The Rewards Catalog (`/point_store`):** The manager can show you a catalog of all the cool things you can buy with your reward points.
- **Buying More Tokens (`/refill_plan`):** If you're running low on travel tokens, the banker can show you all the available packages you can buy to top up your account.
- **Managing Your Account (`/wallet_setting`):** You can view your current account settings (like whether you have auto-refill enabled) and tell the banker to change those settings for you.

**Technical explanation:** 
A Koa.js controller that exposes numerous endpoints across two API versions (v1 and v2) to manage a user's digital wallet. The controller handles several distinct resources: `point_history`, `wallet_summary`, `point_store`, `refill_plan`, and `wallet_setting`. It follows a clean pattern of delegating all business logic to a centralized `walletService`. A notable feature is the `pointsHistory` function, which is reused for both `GET` and `POST` routes, providing flexible ways to query transaction data. Several endpoints are duplicated across v1 and v2, indicating API versioning and evolution over time.

**Business value explanation:**
The wallet is the central hub for all monetization and incentive strategies within the application. This controller provides the critical infrastructure for gamification (earning points), rewards (redeeming points in a store), and direct revenue (purchasing refill plans). A robust and clear wallet system is essential for building user trust and encouraging engagement with the platform's economic and reward systems. The ability for users to easily track their points and manage their settings is key to the success of any loyalty or incentive program.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/wallet.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** REST API Controller
- **File Size:** ~3 KB
- **Complexity Score:** ⭐⭐ (Low-Medium - The logic is straightforward and well-delegated, but the number of versioned endpoints adds some complexity.)

**Dependencies (Criticality Level):**
- `@koa/router`, `koa-bodyparser`: Core routing and body parsing (**Critical**).
- `@maas/core/response`: Standardized success response formatter (**High**).
- `@app/src/middlewares/auth`: JWT authentication middleware (**Critical**).
- `@app/src/services/wallet`: The service layer containing all business logic (**Critical**).
- `@app/src/helpers/fields-of-header`: Utility to extract user context from headers (**High**).
- `@app/src/schemas/wallet`: Joi schemas for input validation (**Critical**).

## 📝 Detailed Code Analysis

### `pointsHistory` (GET & POST `/v2/point_history`)
This function handles fetching the user's transaction history.
- It is cleverly assigned to both a `GET` and a `POST` route. This allows clients to either pass filter parameters (like `begin_date`, `end_date`) in the query string or in a request body.
- It contains default logic for the date range, defaulting to the last 7 days if no range is provided.
- It parses and validates all parameters before passing them in a structured `json` object to the `walletService.coinsHistory` function.

### `getWalletSummary` (GET `/v1/wallet_summary` & `/v2/wallet_summary`)
A simple endpoint that retrieves the currently authenticated user's ID and passes it to the `walletService.walletSummary` function to get a high-level overview of their wallet balances.

### `getPointStore` & `getRefillPlan`
These are simple, user-agnostic (for `refillPlan`) or user-specific (for `pointStore`) endpoints that fetch static or semi-static catalog data from the service layer.

### Wallet Settings Endpoints
- **`getWalletSetting1` & `getWalletSetting2`**: These functions call a common `walletService.getWalletSetting` function but pass a version string ('v1' or 'v2'). This suggests the service layer may return a different data structure depending on the requested version.
- **`putWalletSetting`**: This endpoint handles updates. It uses a Joi schema to validate the incoming request body and then passes the validated data to the `walletService.putWalletSetting` function.

## 🚀 Usage Methods

**Base URL:** `https://api.tsp.example.com/api`
**Headers:** All requests require `Authorization: Bearer <TOKEN>` and `userid: usr_...`

### Get Wallet Summary
```bash
curl -X GET "https://api.tsp.example.com/api/v2/wallet_summary" \
  -H "Authorization: Bearer <TOKEN>" -H "userid: usr_123"
```

### Get Points History for the Last 7 Days
```bash
curl -X GET "https://api.tsp.example.com/api/v2/point_history?offset=0&perpage=20" \
  -H "Authorization: Bearer <TOKEN>" -H "userid: usr_123"
```

### Get Items in the Point Store
```bash
curl -X GET "https://api.tsp.example.com/api/v1/point_store" \
  -H "Authorization: Bearer <TOKEN>" -H "userid: usr_123"
```

### Update Wallet Settings
```bash
curl -X PUT "https://api.tsp.example.com/api/v2/wallet_setting" \
  -H "Authorization: Bearer <TOKEN>" -H "userid: usr_123" \
  -H "Content-Type: application/json" \
  -d '{
    "auto_refill": true,
    "auto_refill_amount": 10
  }'
```

## ⚠️ Important Notes
- **API Versioning**: The presence of both `v1` and `v2` endpoints for `wallet_summary` and `wallet_setting` suggests that clients need to be aware of which version they are using. The backend supports both for backward compatibility.
- **Service-Oriented**: The controller is an excellent example of a thin controller. It contains almost no business logic itself, instead validating and passing requests to the `walletService`, which acts as the single source of truth for all wallet-related operations.
- **Empty Functions**: The `tokenSummary` and `tokenHistory` functions are stubbed out and empty. This indicates planned or deprecated functionality that is not currently implemented in the controller.

## 🔗 Related File Links
- **Business Logic Service:** `allrepo/connectsmart/tsp-api/src/services/wallet.js`
- **Input Validation Schemas:** `allrepo/connectsmart/tsp-api/src/schemas/wallet.js`
- **Authentication Middleware:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`

---
*This documentation was regenerated to provide a clear overview of the wallet controller, its various resources, and its versioned endpoints.* 