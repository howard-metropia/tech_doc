# Incentive System Configuration

### 📋 Configuration Overview
- **Purpose:** Configures incentive system integration for user rewards and micro-survey functionality
- **Module Type:** Service URLs and encryption configuration
- **Environment:** All environments (dev/staging/prod)

### 🔧 Configuration Values
| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `incentiveAdminUrl` | String | No | URL for incentive administration panel | `process.env.INCENTIVE_ADMIN_URL` |
| `incentiveHookUrl` | String | No | Webhook URL for incentive system callbacks | `process.env.INCENTIVE_HOOK_URL` |
| `microSurveyEncryption` | String | Yes | Encryption key for micro-survey data protection | `process.env.ENCRYPTION_KEY` |

### 📝 Usage Example
```javascript
// How to import and use this configuration
const incentiveConfig = require('./config/vendor/incentive');

// Access incentive admin panel
const adminUrl = incentiveConfig.incentiveAdminUrl;
console.log(`Admin panel available at: ${adminUrl}`);

// Set up webhook endpoint for incentive callbacks
app.post('/incentive-webhook', (req, res) => {
  // Process incentive webhook data
  const webhookData = req.body;
  // Handle incentive events
});

// Encrypt micro-survey data
const crypto = require('crypto');
const cipher = crypto.createCipher('aes-256-gcm', incentiveConfig.microSurveyEncryption);
let encrypted = cipher.update(surveyData, 'utf8', 'hex');
encrypted += cipher.final('hex');
```

### ⚠️ Security Notes
- **Sensitive Data:** `ENCRYPTION_KEY` is highly sensitive and used for data protection
- **Encryption Security:** Encryption key should be randomly generated and kept secure
- **Environment Management:** All configuration values should be stored in environment variables
- **Webhook Security:** Incentive hook URL should be protected and validate incoming requests
- **Key Rotation:** Consider implementing encryption key rotation for enhanced security

### 🏷️ Tags
**Keywords:** incentive, rewards, micro-survey, encryption, webhooks, user-engagement  
**Category:** #config #vendor #incentive #encryption #rewards

---
Note: Ensure encryption key is properly generated and stored securely across all environments.