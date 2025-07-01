# Static/Constants Documentation: error-code.js

## 📋 File Overview
- **Purpose:** Defines standardized error codes for API responses and error handling throughout the TSP API
- **Usage:** Used by controllers, services, and middleware for consistent error reporting and client-side error handling
- **Type:** Error codes / Constants

## 🔧 Main Exports
```javascript
module.exports = {
  ERROR_BAD_REQUEST_PARAMS: 10001,
  ERROR_TOKEN_EXPIRED: 10005,
  ERROR_USER_NOT_FOUND: 20001,
  ERROR_CHARGE_FAILED: 23003,
  ERROR_THIRD_PARTY_FAILED: 40000,
  // ... 90+ error codes organized by category
};
```

## 📝 Constants Reference
| Category | Range | Description | Examples |
|----------|-------|-------------|----------|
| Request Errors | 10xxx | Authentication, params, headers | TOKEN_EXPIRED, BAD_REQUEST_PARAMS |
| User Errors | 20xxx | User management, favorites, enterprise | USER_NOT_FOUND, ENTERPRISE_EMAIL_INVALID |
| DUO/Carpool | 21xxx | Group management, matching | DUPLICATE_DUO_GROUP_NAME, USER_ALREADY_IN_GROUP |
| Trip Management | 22xxx | Trip permissions, matching | NO_PERMISSIONS, NO_MATCHING |
| Wallet/Payment | 23xxx | Payment processing, cards, points | CHARGE_FAILED, POINT_INSUFFICIENT |
| External Services | 24xxx | Tolls, Google APIs | TOLLS_ROUTE_INVALID, GOOGLE_PHOTO_REFERENCE |
| Instant Carpool | 25xxx | Real-time carpooling | BALANCE_NOT_ENOUGH, INSTANT_CARPOOL_JOIN_FAILED |
| Third Party APIs | 40xxx | External service integrations | UBER_DETAIL, PARKING_TOKEN, BYTEMARK_PASS_DATA |
| Promo/Referral | 46xxx-47xxx | Promotional codes, referrals | PROMO_CODE_EXPIRED, REFERRAL_CODE_ALREADY_USED |
| Campaign Manager | 90xxx | Admin platform features | SUGGESTION_CARD_ID_NOT_FOUND |

## 💡 Usage Examples
```javascript
// Import error codes
const ERROR_CODES = require('./static/error-code');

// In controller error handling
if (!user) {
  return ctx.throw(404, 'User not found', { 
    code: ERROR_CODES.ERROR_USER_NOT_FOUND 
  });
}

// In payment service
if (chargeResult.failed) {
  throw new Error('Payment failed', { 
    code: ERROR_CODES.ERROR_CHARGE_FAILED 
  });
}

// Client-side error handling
if (response.error.code === ERROR_CODES.ERROR_TOKEN_EXPIRED) {
  // Redirect to login
}
```

## ⚠️ Important Notes
- Error codes are immutable once deployed to avoid breaking client integrations
- Range-based organization ensures scalability and prevents conflicts
- Third-party service errors (40xxx) help identify external system issues
- Guest account restrictions use specific error codes (20301)

## 🏷️ Tags
**Keywords:** error-handling, api-responses, status-codes, debugging, client-integration  
**Category:** #static #constants #error-codes #api-standards