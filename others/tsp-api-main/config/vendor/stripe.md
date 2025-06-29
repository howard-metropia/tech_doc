# Stripe Configuration Module

## 🔍 Quick Summary (TL;DR)

This configuration module centralizes Stripe payment gateway settings for the TSP API, providing environment-based configuration for API keys, transaction limits, webhooks, and alert notifications.

**Keywords:** stripe | payment | gateway | config | api-key | webhook | coin-purchase | transaction-limit | alert | notification | environment-variables | payment-processing

**Primary Use Cases:**
- Payment processing configuration for coin purchases
- Webhook endpoint security setup
- Transaction limit enforcement
- Alert notification management

**Compatibility:** Node.js 14+, Stripe API v2020-08-27+

## ❓ Common Questions Quick Index

- **Q: How do I set up Stripe API credentials?** → [Technical Specifications](#technical-specifications)
- **Q: What are the coin purchase limits?** → [Configuration Parameters](#configuration-parameters)
- **Q: How do webhooks work with this config?** → [Webhook Configuration](#webhook-configuration)
- **Q: How to configure alert notifications?** → [Alert System](#alert-system)
- **Q: What happens if environment variables are missing?** → [Error Handling](#error-handling)
- **Q: How to change daily purchase limits?** → [Usage Methods](#usage-methods)
- **Q: What security considerations exist?** → [Important Notes](#important-notes)
- **Q: How to troubleshoot payment issues?** → [Troubleshooting](#troubleshooting)

## 📋 Functionality Overview

**Non-technical Explanation:**
Think of this as a digital wallet's control panel - like setting spending limits on your credit card, choosing which bank to use, and deciding when to get notifications about transactions. Just as a store needs to know which payment processor to use and what their daily limits are, this configuration tells the system how to handle online payments safely.

**Technical Explanation:**
This module exports a configuration object that centralizes Stripe payment gateway settings, managing API authentication, transaction limits, webhook security, and notification preferences through environment variables.

**Business Value:**
Enables secure payment processing for coin purchases while maintaining configurable limits and audit trails, protecting both users and the platform from excessive transactions.

**System Context:**
Part of the TSP API's vendor configuration layer, integrating with the payment processing pipeline and user wallet management system.

## 🔧 Technical Specifications

**File Information:**
- **Name:** stripe.js
- **Path:** /config/vendor/stripe.js
- **Language:** JavaScript (CommonJS)
- **Type:** Configuration module
- **Size:** ~200 bytes
- **Complexity:** ⭐☆☆☆☆ (Simple configuration)

**Dependencies:**
- **Node.js process.env:** Built-in environment variable access (Critical)
- **Stripe SDK:** External payment processing (Critical)

**Configuration Parameters:**
- `STRIPE_API_KEY`: Stripe secret key (Required)
- `COIN_PURCHASE_DAILY_LIMIT`: Daily purchase limit (Default: '200')
- `COIN_PURCHASE_DAILY_ALERT_LIMIT`: Alert threshold (Default: '50')
- `STRIPE_WEBHOOK_SECRET`: Webhook signature verification (Required)
- `STRIPE_ALERT_NOTIFY_EMAIL`: Notification recipient (Optional)

**Security Requirements:**
- Environment-based secret management
- Webhook signature verification
- API key rotation capability

## 📝 Detailed Code Analysis

**Module Structure:**
```javascript
module.exports = {
  apiKey: process.env.STRIPE_API_KEY,           // Authentication
  buyCoinLimit: process.env.COIN_PURCHASE_DAILY_LIMIT || '200',
  buyCoinAlertLimit: process.env.COIN_PURCHASE_DAILY_ALERT_LIMIT || '50',
  webHookSecret: process.env.STRIPE_WEBHOOK_SECRET,  // Security
  alertNotifyEmail: process.env.STRIPE_ALERT_NOTIFY_EMAIL
};
```

**Design Patterns:**
- **Configuration Object Pattern:** Single source of truth for Stripe settings
- **Environment Variable Pattern:** External configuration management
- **Default Value Pattern:** Graceful fallbacks for non-critical settings

**Error Handling:**
- Missing required variables (`apiKey`, `webHookSecret`) will cause runtime errors
- Optional variables have sensible defaults or undefined values

## 🚀 Usage Methods

**Basic Import:**
```javascript
const stripeConfig = require('./config/vendor/stripe');
const stripe = require('stripe')(stripeConfig.apiKey);
```

**Environment Configuration (.env):**
```bash
STRIPE_API_KEY=sk_live_your_secret_key
COIN_PURCHASE_DAILY_LIMIT=500
COIN_PURCHASE_DAILY_ALERT_LIMIT=100
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
STRIPE_ALERT_NOTIFY_EMAIL=admin@company.com
```

**Production Setup:**
```javascript
// Validate required configuration
if (!stripeConfig.apiKey) {
  throw new Error('STRIPE_API_KEY environment variable is required');
}
if (!stripeConfig.webHookSecret) {
  throw new Error('STRIPE_WEBHOOK_SECRET environment variable is required');
}
```

**Webhook Integration:**
```javascript
const { webHookSecret } = require('./config/vendor/stripe');
const sig = req.headers['stripe-signature'];
const event = stripe.webhooks.constructEvent(req.body, sig, webHookSecret);
```

## 📊 Output Examples

**Successful Configuration Load:**
```javascript
{
  apiKey: 'sk_live_abc123...',
  buyCoinLimit: '500',
  buyCoinAlertLimit: '100',
  webHookSecret: 'whsec_xyz789...',
  alertNotifyEmail: 'admin@company.com'
}
```

**Default Values Applied:**
```javascript
{
  apiKey: 'sk_test_...',
  buyCoinLimit: '200',        // Default applied
  buyCoinAlertLimit: '50',    // Default applied
  webHookSecret: 'whsec_...',
  alertNotifyEmail: undefined  // Optional, not set
}
```

**Configuration Validation Error:**
```javascript
Error: STRIPE_API_KEY environment variable is required
    at Object.<anonymous> (/app/services/payment.js:15:11)
```

## ⚠️ Important Notes

**Security Considerations:**
- Never commit API keys to version control
- Use different keys for development/production environments
- Rotate webhook secrets regularly
- Implement API key validation before service startup

**Performance Impact:**
- Configuration loaded once at module initialization
- Environment variable access is synchronous and fast
- No runtime performance implications

**Common Issues:**
- **Missing API Key:** Service fails to start → Check environment variables
- **Invalid Limits:** String to number conversion needed → Validate numeric values
- **Webhook Failures:** Invalid secret → Verify webhook configuration in Stripe dashboard

**Rate Limiting:**
- Coin purchase limits are enforced at application level
- Stripe API has its own rate limits (100 requests/second)

## 🔗 Related File Links

**Dependencies:**
- `/services/payment.js` - Uses this configuration for Stripe initialization
- `/controllers/wallet.js` - Implements coin purchase limits
- `/middlewares/webhook-validator.js` - Uses webhook secret for verification

**Configuration Files:**
- `/config/default.js` - Main application configuration
- `/config/database.js` - Database connection settings
- `/.env` - Environment variables (not in repo)

**Test Files:**
- `/test/config/stripe.test.js` - Configuration validation tests
- `/test/services/payment.test.js` - Payment service integration tests

## 📈 Use Cases

**Development Environment:**
```bash
STRIPE_API_KEY=sk_test_development_key
COIN_PURCHASE_DAILY_LIMIT=10
```

**Production Deployment:**
- Higher purchase limits for live users
- Live API keys with proper security
- Email notifications for high-value transactions

**Testing Scenarios:**
- Mock Stripe configuration for unit tests
- Webhook simulation with test secrets
- Limit validation testing

**Monitoring Integration:**
- Alert system triggers based on purchase thresholds
- Transaction logging with configuration context

## 🛠️ Improvement Suggestions

**Security Enhancements:**
- Add configuration validation at startup (Priority: High, Effort: Low)
- Implement encrypted environment variable storage (Priority: Medium, Effort: High)
- Add configuration change audit logging (Priority: Medium, Effort: Medium)

**Feature Additions:**
- Support for multiple Stripe accounts (Priority: Low, Effort: High)
- Dynamic limit adjustment based on user tier (Priority: Medium, Effort: Medium)
- Configuration hot-reloading capability (Priority: Low, Effort: High)

**Maintenance Improvements:**
- Add JSDoc documentation (Priority: Low, Effort: Low)
- Create configuration schema validation (Priority: Medium, Effort: Low)

## 🏷️ Document Tags

**Keywords:** stripe, payment-gateway, configuration, api-key, webhook, environment-variables, coin-purchase, transaction-limits, security, notification, alert-system, payment-processing, nodejs, commonjs, config-management

**Technical Tags:** #stripe #payment #config #api #webhook #environment-variables #nodejs #commonjs #vendor-config #security

**Target Roles:** Backend Developers (Junior+), DevOps Engineers, Payment Integration Specialists, System Administrators

**Difficulty Level:** ⭐☆☆☆☆ (Beginner - Simple configuration object with clear structure)

**Maintenance Level:** Low (Occasional updates for new Stripe features or limit adjustments)

**Business Criticality:** High (Payment processing is core business functionality)

**Related Topics:** Payment Processing, API Configuration, Environment Management, Webhook Security, Transaction Monitoring