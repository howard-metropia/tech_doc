# TSP API Ticket Payment Controller Documentation

## 🔍 Quick Summary (TL;DR)
The ticket payment controller manages transit ticket payment account creation and verification through Bytemark integration, enabling seamless mobile ticketing for public transit systems.

**Keywords:** ticket-payment | transit-payment | bytemark | mobile-ticketing | transit-passes | payment-accounts | public-transit | fare-management

**Primary use cases:** Creating transit payment accounts, checking account status, managing mobile ticketing credentials, integrating with Bytemark ticketing platform

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, MySQL, Bytemark API

## ❓ Common Questions Quick Index
- **Q: What is Bytemark?** → Third-party mobile ticketing platform for transit agencies
- **Q: How are accounts created?** → Automatically generated with unique email/password
- **Q: What endpoints are available?** → Create/check account for both ticket_payment and transit_payment
- **Q: Is this ConnectSmart specific?** → Yes, only active for ConnectSmart projects
- **Q: How is authentication handled?** → JWT auth required, OAuth tokens stored for Bytemark
- **Q: What happens if account creation fails?** → Returns error with retry capability

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **digital wallet setup** for public transit. When you want to buy bus or train tickets on your phone, this controller creates a special payment account for you behind the scenes. It's like having a transit card on your phone that automatically sets itself up the first time you use it, so you can start buying tickets right away without filling out forms.

**Technical explanation:** 
A Koa.js controller that manages Bytemark transit payment account lifecycle. It automatically provisions payment accounts with generated credentials, handles OAuth token management, and provides account status verification for mobile ticketing integration in public transit systems.

**Business value explanation:**
Enables frictionless mobile ticketing adoption by eliminating manual account creation. Reduces barriers to transit usage, increases fare collection efficiency, and provides seamless integration with existing transit agency ticketing systems through Bytemark's platform.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/ticket-payment.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** Payment Integration Controller
- **File Size:** ~4.5 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High - External API integration with account provisioning)

**Dependencies:**
- `@maas/core/mysql`: Database connection for user data (**Critical**)
- `@koa/router`: HTTP routing framework (**Critical**)
- `@maas/core/response`: Standardized response formatting (**High**)
- `@maas/core/log`: Logging infrastructure (**High**)
- `@app/src/middlewares/auth`: JWT authentication (**Critical**)
- `@maas/services`: BytemarkManager service (**Critical**)
- `config`: Configuration for Bytemark integration (**Critical**)

## 📝 Detailed Code Analysis

### Core Functionality - bytemarkCheck Function

**Purpose:** Handles account creation and verification for Bytemark payment integration

**Processing Flow:**
1. **Project Validation:** Checks if current project is ConnectSmart
2. **User Lookup:** Fetches user data with existing Bytemark credentials
3. **Account Creation:** If no account exists, creates one automatically
4. **Token Management:** Handles OAuth token generation and storage
5. **Response Formatting:** Returns account status and payment URLs

### Account Creation Logic
```javascript
// Generate secure password with alphanumeric requirements
do {
  password = randomText(12, 2);
} while (!validPass(password));

// Create unique email for Bytemark account
const bytemarkEmail = `${config.vendor.bytemark.mailPrefix}.${userId}@mail.connectsmartx.com`;

// Store credentials in database
await knex('bytemark_tokens').insert({
  email: bytemarkEmail,
  user_id: userId,
  password,
  status: 'used',
});
```

### OAuth Token Management
```javascript
// Login to Bytemark if no token exists
if (!user.bytemark_token) {
  const loginInfo = await bytemark.login(
    user.bytemark_email,
    user.bytemark_password,
  );
  
  // Store OAuth token for future use
  await knex('bytemark_tokens').update({
    token: loginInfo.data.oauth_token,
  }).where('id', user.bytemark_id);
}
```

## 🚀 Usage Methods

### Create Ticket Payment Account
```bash
curl -X GET "https://api.tsp.example.com/api/v2/ticket_payment/create_account" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"
```

### Check Account Status
```bash
curl -X GET "https://api.tsp.example.com/api/v2/ticket_payment/check_account" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"
```

### Transit Payment Endpoints
```bash
# Create transit payment account
curl -X GET "https://api.tsp.example.com/api/v2/transit_payment/create_account" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"

# Check transit payment status
curl -X GET "https://api.tsp.example.com/api/v2/transit_payment/check_account" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"
```

## 📊 Output Examples

### Successful Account Creation/Check
```json
{
  "result": "success",
  "data": {
    "bytemark_email": "user@example.com",
    "bytemark_token_status": true,
    "bytemark_payment_status": true,
    "payment_url": "https://account.bytemark.com",
    "service_inbox": "support@bytemark.com",
    "auth_status": "success",
    "error_data": {}
  }
}
```

### Non-ConnectSmart Project Response
```json
{
  "result": "success",
  "data": {
    "bytemark_email": "",
    "bytemark_token_status": true,
    "bytemark_payment_status": true,
    "payment_url": "https://account.bytemark.com",
    "service_inbox": "support@bytemark.com",
    "auth_status": "success",
    "error_data": {}
  }
}
```

### Account Creation Error
```json
{
  "error": "ERROR_BYTEMARK_PASS_DATA",
  "message": "Failed to create Bytemark account",
  "code": 400
}
```

## ⚠️ Important Notes

### Security Considerations
- **Password Generation:** Uses cryptographically secure random generation
- **Password Validation:** Ensures alphanumeric combination
- **Credential Storage:** Passwords stored in database (consider encryption)
- **OAuth Tokens:** Stored for API access, should have expiration handling
- **Email Generation:** Uses predictable pattern - consider security implications

### Bytemark Integration
- **Project Specific:** Only active for ConnectSmart deployments
- **Account Provisioning:** Automatic account creation on first use
- **Email Format:** `prefix.userId@mail.connectsmartx.com`
- **Name Defaults:** Uses "FirstName LastName" if not provided
- **Token Persistence:** OAuth tokens stored for reuse

### Database Schema
Required tables and fields:
- **auth_user:** id, email, first_name, last_name
- **bytemark_tokens:** id, email, user_id, password, token, status

### Configuration Requirements
```javascript
{
  portal: {
    projectTitle: 'ConnectSmart', // Must contain 'connectsmart'
    projectStage: 'production'
  },
  vendor: {
    bytemark: {
      mailPrefix: 'user',
      url: {
        account: 'https://account.bytemark.com',
        accountApi: 'https://api.bytemark.com'
      },
      clientId: 'client_id_here',
      inboxAddress: 'support@bytemark.com'
    },
    slack: {
      token: 'slack_token',
      channelId: 'channel_id'
    }
  }
}
```

### Error Handling
- **Account Creation Failures:** Logged and returned as 400 errors
- **Login Failures:** Treated as account creation errors
- **Database Errors:** Caught and logged with stack traces
- **Bytemark API Errors:** Wrapped in MaasError with specific codes

### Endpoint Duplication
Note that all four endpoints use the same handler function:
- `/ticket_payment/create_account`
- `/ticket_payment/check_account`
- `/transit_payment/create_account`
- `/transit_payment/check_account`

This suggests they serve the same purpose with different naming conventions.

## 🔗 Related File Links

- **BytemarkManager Service:** `@maas/services` (external package)
- **Random Text Helper:** `allrepo/connectsmart/tsp-api/src/helpers/random_text.js`
- **Error Codes:** `allrepo/connectsmart/tsp-api/src/static/error-code.js`
- **Database Schema:** Check migrations for bytemark_tokens table structure

---
*This controller provides critical transit payment account management for mobile ticketing integration.*