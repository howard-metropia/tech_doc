# Enterprise Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates enterprise-related operations including email verification and telework management
- **Validation Library:** Joi
- **Related Controller:** Enterprise controller for business user management

## 🔧 Schema Structure
```javascript
// Email verification schema
{
  ...verifyHeaderFieldsByJoi,
  email: Joi.string().required(),
  verify_type: Joi.string().required(),
  group_id: Joi.number().integer().min(1),
  security_key: Joi.string(),
}

// Telework update schema
{
  ...verifyHeaderFieldsByJoi,
  enterprise_id: Joi.number().integer().min(1).required(),
  chk_telework: Joi.boolean().required(),
  security_key: Joi.string(),
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| email | string | Yes | Any string | User email address |
| verify_type | string | Yes | Any string | Type of verification process |
| group_id | number | No | Min: 1 | Enterprise group identifier |
| security_key | string | No | Any string | Frontend encryption security key |
| verify_token | string | Yes (verify) | Any string | Email verification token |
| user_id | number | Yes (delete) | Min: 1 | User identifier |
| enterprise_id | number | Yes (update/delete) | Min: 1 | Enterprise identifier |
| chk_telework | boolean | Yes (telework) | true/false | Telework status flag |
| zone | string | Yes (verify) | Any string | Geographic zone |
| lang | string | Yes (verify) | Any string | Language preference |

## 💡 Usage Example
```javascript
// Send verification email
{
  "email": "user@company.com",
  "verify_type": "enterprise_join",
  "group_id": 123,
  "security_key": "encrypted_key_123"
}

// Update telework status
{
  "enterprise_id": 456,
  "chk_telework": true,
  "security_key": "encrypted_key_456"
}

// Email verification
{
  "zone": "US_EAST",
  "lang": "en",
  "verify_token": "abc123def456",
  "newversion": "2.1.0"
}

// Request that fails validation
{
  "email": "user@company.com",
  "verify_type": "enterprise_join",
  "group_id": 0 // Error: must be minimum 1
}
```

## ⚠️ Important Validations
- Email is required for verification and search operations
- Group ID and Enterprise ID must be positive integers when specified
- Security key is used for frontend encryption - optional but recommended
- Telework boolean flag is required for telework updates
- Zone and language are required for email verification process

## 🏷️ Tags
**Keywords:** enterprise, email-verification, telework, business-users, encryption
**Category:** #schema #validation #joi #enterprise