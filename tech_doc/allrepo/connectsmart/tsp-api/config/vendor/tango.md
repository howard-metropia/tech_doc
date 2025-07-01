# Tango Card API Configuration Documentation

## 🔍 Quick Summary (TL;DR)
Configuration module for Tango Card gift card and rewards integration platform providing digital reward fulfillment capabilities for transit loyalty programs.
**Keywords:** tango-card | gift-cards | rewards | api-integration | digital-fulfillment | loyalty-program | incentives | vouchers | payments | transit-rewards
**Use Cases:** Reward distribution, loyalty program integration, digital gift card fulfillment, user incentive systems
**Compatibility:** Node.js 16+, Koa.js framework, Tango Card RaaS API v2

## ❓ Common Questions Quick Index
- Q: How to configure Tango Card API credentials? → [Technical Specifications](#technical-specifications)
- Q: What environment variables control Tango settings? → [Configuration Parameters](#configuration-parameters)
- Q: How to set daily redemption limits? → [Usage Methods](#usage-methods)
- Q: What happens when gift card balance is insufficient? → [Important Notes](#important-notes)
- Q: How to customize email templates for rewards? → [Output Examples](#output-examples)
- Q: What are the production vs test configurations? → [Environment Configuration](#environment-configuration)
- Q: How to troubleshoot Tango API connection issues? → [Troubleshooting](#troubleshooting)
- Q: What security measures protect Tango credentials? → [Security Considerations](#security-considerations)

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a digital wallet configuration for a gift card vending machine. Like setting up a Point-of-Sale system, you configure which gift card provider to use (Tango Card), set spending limits, and define who gets notified when the cash register runs low. It's similar to configuring an ATM - you need bank credentials, withdrawal limits, and alert settings for maintenance.

**Technical explanation:**
Configuration object that centralizes Tango Card RaaS (Rewards as a Service) API integration settings, providing environment-specific parameters for digital reward fulfillment within the transit service platform. Implements configuration-driven architecture with environment variable overrides.

**Business value:** Enables automated digital reward distribution for transit loyalty programs, reducing manual gift card processing and providing scalable incentive mechanisms to encourage public transportation usage.

**System context:** Core component of the rewards subsystem within the TSP API, interfacing with user wallet services, payment processing, and campaign management systems.

## 🔧 Technical Specifications

**File Information:**
- Name: tango.js
- Path: /config/vendor/tango.js
- Language: JavaScript (Node.js module)
- Type: Configuration module
- Size: 18 lines
- Complexity: Low (configuration-only)

**Dependencies:**
- Environment variables (process.env) - Runtime configuration
- Node.js process module - Built-in (critical)
- Tango Card RaaS API v2 - External service dependency

**Configuration Parameters:**
```javascript
{
  url: 'https://integration-api.tangocard.com/raas/v2/',  // API endpoint
  platformName: 'MetropiaTest',                          // Platform identifier
  platformKey: '[64-char API key]',                      // Authentication key
  accountId: 'metrotest1',                               // Account identifier
  customerId: 'metrotest1',                              // Customer identifier
  senderEmail: 'info@h-connectsmart.org',               // Email sender
  senderName: 'ConnectSmart',                           // Display name
  alertNotifyEmail: 'sibu.wang@metropia.com',           // Alert recipient
  insufficientLevel: '30',                              // Balance threshold ($)
  redeemLimit: '100',                                   // Daily limit ($)
  redeemAlertLimit: '50',                               // Alert threshold ($)
  emailTemplateId: 'E000000'                           // Template identifier
}
```

## 📝 Detailed Code Analysis

**Module Structure:**
```javascript
module.exports = {
  // Configuration object with environment variable fallbacks
  // Each property follows pattern: process.env.VAR_NAME || 'default_value'
}
```

**Design Patterns:**
- **Configuration Pattern:** Centralized settings management
- **Environment Override Pattern:** Flexible deployment configuration
- **Default Fallback Pattern:** Graceful degradation for missing variables

**Key Properties Analysis:**
- `url`: API endpoint with versioned path structure (v2)
- `platformKey`: Sensitive authentication credential (should be encrypted)
- `insufficientLevel`: Financial threshold triggering low balance alerts
- `redeemLimit/redeemAlertLimit`: Daily spending controls and monitoring

## 🚀 Usage Methods

**Basic Integration:**
```javascript
const tangoConfig = require('./config/vendor/tango');
const TangoService = require('@maas/services/tango');

const tangoClient = new TangoService(tangoConfig);
```

**Environment Configuration:**
```bash
# Production settings
export TANGO_URL="https://api.tangocard.com/raas/v2/"
export TANGO_PLATFORM_NAME="MetropiaProduction"
export TANGO_PLATFORM_KEY="your_production_key"
export TANGO_ACCOUNT_ID="metroprod1"
export REDEEM_DAILY_LIMIT="500"
```

**Daily Limit Management:**
```javascript
// Monitor daily redemptions
if (dailyRedemptions >= tangoConfig.redeemLimit) {
  throw new Error('Daily redemption limit exceeded');
}

// Alert when approaching limit
if (dailyRedemptions >= tangoConfig.redeemAlertLimit) {
  await sendAlertEmail(tangoConfig.alertNotifyEmail);
}
```

## 📊 Output Examples

**Configuration Object Output:**
```javascript
{
  url: 'https://integration-api.tangocard.com/raas/v2/',
  platformName: 'MetropiaTest',
  platformKey: 'lCbocjESjaU&jFoj!MgJOhiGaTnvmgzVQKMIroxyBuQBln',
  accountId: 'metrotest1',
  customerId: 'metrotest1',
  senderEmail: 'info@h-connectsmart.org',
  senderName: 'ConnectSmart',
  alertNotifyEmail: 'sibu.wang@metropia.com',
  insufficientLevel: '30',
  redeemLimit: '100',
  redeemAlertLimit: '50',
  emailTemplateId: 'E000000'
}
```

**API Response Examples:**
```json
{
  "success": true,
  "account_balance": 150.00,
  "daily_redeemed": 45.00,
  "remaining_limit": 55.00,
  "alert_triggered": false
}
```

## ⚠️ Important Notes

**Security Considerations:**
- Platform key contains sensitive API credentials - use environment variables in production
- Never commit production keys to version control
- Implement key rotation procedures for compromised credentials
- Monitor API usage for unauthorized access patterns

**Performance Considerations:**
- Configuration is loaded once at startup - no runtime performance impact
- Daily limits prevent API quota exhaustion
- Alert thresholds enable proactive monitoring

**Common Issues:**
- **Invalid Platform Key:** Verify key format and account association
- **Daily Limit Exceeded:** Check current usage against configured limits
- **Email Delivery Failure:** Validate sender email domain and template ID
- **Insufficient Balance:** Monitor account balance against threshold

## 🔗 Related File Links

**Configuration Dependencies:**
- `/config/default.js` - Main application configuration
- `/config/environment.js` - Environment-specific overrides
- `/src/services/tango.js` - Tango Card service implementation

**Related Services:**
- `/src/controllers/wallet.js` - User wallet management
- `/src/controllers/giftcard.js` - Gift card processing
- `/src/services/email.js` - Email notification service

## 📈 Use Cases

**Daily Operations:**
- Transit users earn rewards through app usage
- Automated gift card distribution for loyalty milestones
- Daily spending limit enforcement for budget control
- Low balance alerts for proactive account management

**Development Scenarios:**
- Test environment configuration for feature development
- Integration testing with sandbox Tango Card accounts
- Configuration validation in CI/CD pipelines

**Production Scaling:**
- High-volume reward processing during campaigns
- Multi-tenant configuration for different transit agencies
- Monitoring and alerting for service health

## 🛠️ Improvement Suggestions

**Security Enhancements:**
- Implement encrypted configuration storage (Medium effort, High security benefit)
- Add configuration validation middleware (Low effort, Medium benefit)
- Implement audit logging for configuration changes (Medium effort, High compliance benefit)

**Operational Improvements:**
- Add dynamic configuration reloading (High effort, Medium benefit)
- Implement configuration versioning (Medium effort, Low benefit)
- Add health check endpoints for Tango connectivity (Low effort, High benefit)

**Monitoring Enhancements:**
- Real-time spending analytics dashboard (High effort, High benefit)
- Automated balance replenishment triggers (Medium effort, High benefit)

## 🏷️ Document Tags

**Keywords:** tango-card, gift-cards, rewards, api-configuration, digital-payments, loyalty-programs, transit-incentives, raas-api, spending-limits, email-notifications, balance-management, vendor-integration

**Technical Tags:** #config #vendor-integration #tango-card #rewards-api #payment-processing #environment-variables #koa-config

**Target Roles:** Backend developers (intermediate), DevOps engineers (beginner), Product managers (basic understanding)

**Difficulty Level:** ⭐⭐☆☆☆ (Low-Medium) - Simple configuration with business logic implications

**Maintenance Level:** Low - Configuration changes driven by business requirements

**Business Criticality:** High - Direct impact on user rewards and payment processing

**Related Topics:** API integration, payment processing, rewards systems, configuration management, environment variables, vendor management