# Wallet Notification Service - walletNotify.js

## 🔍 Quick Summary (TL;DR)
The walletNotify service automatically triggers email alerts when users attempt to purchase coins that exceed daily limits, protecting against potential fraud and suspicious activity in the TSP API MaaS platform.

**Keywords:** wallet | notification | email | alert | fraud | security | tango | coins | purchase | daily-quota | anti-fraud | transaction-monitoring | user-protection

**Primary Use Cases:**
- Fraud detection for large coin purchases
- Daily quota limit monitoring
- Automated security alerts to administrators
- User notification for suspicious activities

**Compatibility:** Node.js 16+, Koa.js, @maas/core, Config 3.x

## ❓ Common Questions Quick Index
1. **Q: What triggers a wallet notification?** → [Usage Methods](#-usage-methods)
2. **Q: How do I configure notification recipients?** → [Technical Specifications](#-technical-specifications)
3. **Q: What information is included in fraud alerts?** → [Output Examples](#-output-examples)
4. **Q: How to customize notification templates?** → [Detailed Code Analysis](#-detailed-code-analysis)
5. **Q: What if emails aren't being sent?** → [Important Notes](#-important-notes)
6. **Q: How to test notification functionality?** → [Usage Methods](#-usage-methods)
7. **Q: Can I modify the alert thresholds?** → [Technical Specifications](#-technical-specifications)
8. **Q: What happens during email delivery failures?** → [Important Notes](#-important-notes)
9. **Q: How to add new notification types?** → [Improvement Suggestions](#-improvement-suggestions)
10. **Q: What security measures are in place?** → [Important Notes](#-important-notes)

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this service as a bank's fraud detection system - when someone tries to make an unusually large purchase of coins (like loyalty points), it automatically sends an alert email to the security team, similar to how your credit card company texts you about suspicious transactions. It's like having a digital security guard that watches for unusual spending patterns and immediately notifies the right people.

**Technical explanation:**
A notification service module that monitors wallet transactions and automatically triggers email alerts when coin purchase attempts exceed configured thresholds. Implements template-based email generation with dual notification paths: administrative alerts for internal monitoring and user notifications for fraud verification.

**Business Value:**
Protects revenue and user accounts from fraudulent activities, reduces chargebacks, maintains platform security compliance, and provides early warning system for suspicious financial behavior in the MaaS ecosystem.

**System Context:**
Integrated within the TSP API's wallet management system, works alongside payment processing, user management, and email delivery services to provide comprehensive transaction monitoring and security alerting.

## 🔧 Technical Specifications

**File Information:**
- Name: walletNotify.js
- Path: /src/services/walletNotify.js
- Language: JavaScript (Node.js)
- Type: Service Module
- Size: ~88 lines
- Complexity: Low-Medium

**Dependencies:**
- `@maas/core/log` (Critical) - Logging infrastructure
- `@app/src/helpers/send_mail` (Critical) - Email delivery service
- `config` (Critical) - Configuration management, version 3.x

**Configuration Parameters:**
- `TANGO_ALERT_NOTIFY_EMAIL` (env var) - Comma-separated admin email list
- `config.portal.projectTitle` - Project branding name
- Default recipients: ['fillano.feng@metropia.com', 'sibu.wang@metropia.com']

**System Requirements:**
- Node.js 16+ (recommended 18+)
- Email service configuration
- Project configuration setup
- Logging system initialization

## 📝 Detailed Code Analysis

**Main Functions:**
```javascript
// Generate admin notification content
genEmailNotifyContent(project, now, userId, email, firstName, lastName, amount)
// Returns: HTML formatted string with user and transaction details

// Generate user fraud notification content  
genEmailNotifyUserContent(firstName, project)
// Returns: HTML formatted fraud alert message

// Send admin notification
emailNotify(user, points)
// Sends alert to administrators about suspicious activity

// Send user notification
emailNotifyUser(user)
// Sends fraud alert directly to user
```

**Execution Flow:**
1. Function called with user object and transaction amount
2. Timestamp generated in UTC format
3. Email content generated using template functions
4. Recipients determined from environment or defaults
5. Email sent via send_mail helper
6. Logging performed at each step

**Design Patterns:**
- Template Method Pattern for email generation
- Factory Pattern for content creation
- Dependency Injection for configuration and logging

**Error Handling:**
Uses async/await pattern with implicit error propagation to calling functions. Relies on send_mail helper for email delivery error handling.

## 🚀 Usage Methods

**Basic Admin Notification:**
```javascript
const { emailNotify } = require('./walletNotify');

const user = {
  id: 12345,
  email: 'user@example.com',
  name: {
    first_name: 'John',
    last_name: 'Doe'
  }
};

// Trigger admin notification for large purchase
await emailNotify(user, 1000);
```

**User Fraud Alert:**
```javascript
const { emailNotifyUser } = require('./walletNotify');

// Send fraud alert to user
await emailNotifyUser(user);
```

**Environment Configuration:**
```bash
# Set custom admin notification recipients
export TANGO_ALERT_NOTIFY_EMAIL="admin1@company.com,security@company.com"
```

**Integration Example:**
```javascript
// In wallet purchase flow
if (purchaseAmount > dailyLimit) {
  await emailNotify(user, purchaseAmount);
  await emailNotifyUser(user);
  // Block transaction
}
```

## 📊 Output Examples

**Admin Notification Email:**
```
Subject: [GoMyWay] Purchase Coins Daily Quota Alert (user_id: 12345)

Project: GoMyWay<br />
Time: 2024-01-15 14:30:22(UTC)<br />
user_id: 12345<br />
Email: user@example.com<br />
First name: John<br />
Last name: Doe<br />
Coins attempt to purchase: 1000
```

**User Fraud Alert Email:**
```
Subject: Customer Support at GoMyWay

Good afternoon, John, this is Aranza with GoMyWay. I wanted to reach out 
to you because our system triggered a potential fraud alert based on your 
large purchase of Coins through the app...
```

**Console Logging Output:**
```
[INFO] [genEmailNotifyContent] enter, project: GoMyWay, now: 2024-01-15 14:30:22, userId: 12345...
[INFO] [emailNotify] enter, user: [object Object], points: 1000, config.portal.projectTitle: GoMyWay
```

## ⚠️ Important Notes

**Security Considerations:**
- Email content contains sensitive user information (PII)
- No input validation on user object structure
- Hardcoded default email recipients in code
- Email delivery is asynchronous without confirmation

**Common Troubleshooting:**
- **Emails not sent:** Check send_mail helper configuration and SMTP settings
- **Wrong recipients:** Verify TANGO_ALERT_NOTIFY_EMAIL environment variable
- **Template errors:** Ensure user object has required name structure
- **Missing timestamps:** Verify system clock and timezone settings

**Performance Considerations:**
- Synchronous HTML template generation
- Blocking email operations without queuing
- No rate limiting on notification frequency
- Memory usage minimal for template generation

**Dependencies:**
- Requires functional email delivery service
- Config module must be properly initialized
- Logger must be available from @maas/core

## 🔗 Related File Links

**Dependencies:**
- `/src/helpers/send_mail.js` - Email delivery implementation
- `/config/default.js` - Project configuration settings
- `@maas/core/log` - Logging service

**Integration Points:**
- Wallet service controllers
- Payment processing modules
- User management services
- Fraud detection systems

**Configuration:**
- Environment variable files (.env)
- Project configuration files
- Email service configuration

## 📈 Use Cases

**Daily Operations:**
- Automated fraud monitoring during business hours
- Large transaction alerts for financial oversight
- User protection against account compromise
- Compliance reporting for suspicious activities

**Development Scenarios:**
- Testing notification workflows
- Debugging email delivery issues
- Customizing alert templates
- Integration with new payment providers

**Scaling Considerations:**
- High-volume transaction monitoring
- Multi-tenant notification routing
- Batch processing for multiple alerts
- Performance optimization for template generation

## 🛠️ Improvement Suggestions

**Code Optimization:**
- Add input validation for user object structure (2 hours)
- Implement async template generation (1 hour)
- Add email delivery confirmation and retry logic (4 hours)
- Create configurable template system (6 hours)

**Feature Enhancements:**
- Multi-language notification support (8 hours)
- SMS notification integration (6 hours)
- Configurable alert thresholds (3 hours)
- Rich HTML email templates (4 hours)

**Technical Debt:**
- Remove hardcoded email recipients (1 hour)
- Add comprehensive error handling (2 hours)
- Implement notification queuing system (8 hours)
- Add unit tests for all functions (4 hours)

## 🏷️ Document Tags

**Keywords:** wallet, notification, email, alert, fraud, security, tango, coins, purchase, daily-quota, anti-fraud, transaction-monitoring, user-protection, maas, koa, javascript, service, template, smtp

**Technical Tags:** #service #notification #email #fraud-detection #wallet #security #koa-service #maas-platform #transaction-monitoring

**Target Roles:** Backend Developers (mid-level), DevOps Engineers, Security Engineers, System Administrators

**Difficulty Level:** ⭐⭐⭐ (3/5) - Moderate complexity due to email templating and security considerations

**Maintenance Level:** Low - Stable functionality with occasional template updates

**Business Criticality:** High - Essential for fraud prevention and user security

**Related Topics:** Email services, fraud detection, wallet management, user notifications, security monitoring, MaaS platform