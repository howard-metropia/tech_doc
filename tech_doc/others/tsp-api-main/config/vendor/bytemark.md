# Bytemark Transit Payment Configuration

### 📋 Configuration Overview
- **Purpose:** Configures Bytemark transit payment system integration for mobile ticketing
- **Module Type:** Service credentials and environment-specific API endpoints
- **Environment:** Production/UAT environments with different API endpoints

### 🔧 Configuration Values
| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `isProduction` | Boolean | No | Determines production vs UAT environment | `process.env.BYTEMARK_PRODUCTION === 'true'` |
| `inboxAddress` | String | No | Email address for Bytemark communications | `'info@metropia.com'` |
| `url.merchantApi` | String | No | Merchant API endpoint (environment-dependent) | Production/UAT URLs |
| `url.accountApi` | String | No | Account API endpoint (environment-dependent) | Production/UAT URLs |
| `url.customerApi` | String | No | Customer API endpoint (environment-dependent) | Production/UAT URLs |
| `url.account` | String | No | Account portal URL (environment-dependent) | Production/UAT URLs |
| `clientId` | String | Yes | Bytemark client ID for authentication | `process.env.BYTEMARK_CLIENT_ID` |
| `clinetSecret` | String | Yes | Bytemark client secret (note: typo in config) | `process.env.BYTEMARK_CLIENT_SECRET` |
| `mailPrefix` | String | No | Email prefix for Bytemark notifications | `process.env.BYTEMARK_MAIL_PREFIX` |
| `disableDayPass` | String | No | Flag to disable day pass functionality | `'true'` |

### 📝 Usage Example
```javascript
// How to import and use this configuration
const bytemarkConfig = require('./config/vendor/bytemark');

// Check environment and use appropriate API endpoints
if (bytemarkConfig.isProduction) {
  console.log('Using production Bytemark APIs');
} else {
  console.log('Using UAT Bytemark APIs');
}

// Make API request to merchant API
const response = await axios.post(`${bytemarkConfig.url.merchantApi}/api/tickets`, {
  // ticket data
}, {
  headers: {
    'Authorization': `Bearer ${bytemarkConfig.clientId}:${bytemarkConfig.clinetSecret}`
  }
});
```

### ⚠️ Security Notes
- **Sensitive Data:** `BYTEMARK_CLIENT_ID` and `BYTEMARK_CLIENT_SECRET` are sensitive credentials
- **Environment Management:** All credentials should be stored in environment variables
- **API Endpoints:** Different URLs for production vs UAT environments ensure proper isolation
- **Config Typo:** Note the typo in `clinetSecret` - should be `clientSecret`
- **Email Security:** Inbox address should be monitored for Bytemark communications

### 🏷️ Tags
**Keywords:** bytemark, transit-payment, mobile-ticketing, payment-gateway, oauth  
**Category:** #config #vendor #credentials #bytemark #payments

---
Note: Fix the typo in `clinetSecret` parameter name and ensure proper environment separation.