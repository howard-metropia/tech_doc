# Guest Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates guest user login requests for anonymous access
- **Validation Library:** Joi
- **Related Controller:** Guest controller for temporary user authentication

## 🔧 Schema Structure
```javascript
// Main schema definition
{
  security_key: Joi.string().required(),
  guest_token: Joi.string().allow(null),
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| security_key | string | Yes | Any string | Security key for guest authentication |
| guest_token | string | No | Allow null | Optional existing guest token |

## 💡 Usage Example
```javascript
// Request example that passes validation
{
  "security_key": "abc123xyz456",
  "guest_token": "guest_789def"
}

// Request example with null token
{
  "security_key": "abc123xyz456",
  "guest_token": null
}

// Request example that fails validation
{
  // Error: security_key is required
  "guest_token": "guest_789def"
}
```

## ⚠️ Important Validations
- Security key is mandatory for all guest login attempts
- Guest token can be null for first-time guest users
- Simple validation structure for lightweight guest access
- No complex authentication requirements for guest users

## 🏷️ Tags
**Keywords:** guest-login, anonymous-access, temporary-authentication
**Category:** #schema #validation #joi #guest-login