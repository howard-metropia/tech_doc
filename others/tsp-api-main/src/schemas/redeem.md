# Redeem Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates gift card or reward redemption requests
- **Validation Library:** Joi
- **Related Controller:** redeem controller

## 🔧 Schema Structure
```javascript
{
  create: Joi.object({
    ...verifyHeaderFieldsByJoi,
    id: Joi.number().integer().min(1).required(),
    email: Joi.string(),
    security_key: Joi.string()
  })
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| id | number | Yes | Integer ≥ 1 | Redemption item ID |
| email | string | No | - | User email for redemption |
| security_key | string | No | - | Frontend encryption key |
| ...header fields | various | Yes | From verifyHeaderFieldsByJoi | Authentication and device info |

## 💡 Usage Example
```javascript
// Request example that passes validation
{
  "id": 123,
  "email": "user@example.com",
  "security_key": "encrypted_key_here"
}

// Minimal valid request
{
  "id": 1
}

// Request example that fails validation
{
  "id": 0,  // Error: must be at least 1
  "email": "invalid-email"  // Error: must be valid email format
}
```

## ⚠️ Important Validations
- ID is required and must be a positive integer
- Email validation follows standard email format when provided
- Security key used for frontend encryption processes
- Includes standard header field validations for authentication
- Chinese comment indicates frontend encryption functionality

## 🏷️ Tags
**Keywords:** redemption, gift cards, rewards, encryption, validation
**Category:** #schema #validation #joi #redeem