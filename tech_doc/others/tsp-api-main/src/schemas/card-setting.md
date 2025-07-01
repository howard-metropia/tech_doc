# Card Setting Schema Documentation

### 📋 Schema Overview
- **Purpose:** Validates payment card management operations (CRUD)
- **Validation Library:** Joi
- **Related Controller:** card-setting.js

### 🔧 Schema Structure
```javascript
// Get card settings
get: {
  // Only header verification fields
}

// Create new card
create: {
  transaction_token: string (required)
}

// Update existing card
update: {
  card_id: string (required),
  expire_year: number (optional),
  expire_month: number (optional),
  postal_code: string (optional),
  default: boolean (optional),
  security_key: string (optional)
}

// Delete card
delete: {
  card_id: string (required)
}
```

### 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| transaction_token | string | Yes | - | Token for card creation |
| card_id | string | Yes | - | Unique card identifier |
| expire_year | number | No | - | Card expiration year |
| expire_month | number | No | - | Card expiration month |
| postal_code | string | No | - | Billing postal code |
| default | boolean | No | - | Set as default payment method |
| security_key | string | No | - | Additional security key |

### 💡 Usage Example
```javascript
// Create card request
{
  "transaction_token": "tok_1234567890abcdef"
}

// Update card request
{
  "card_id": "card_1234567890",
  "expire_year": 2025,
  "expire_month": 12,
  "postal_code": "12345",
  "default": true
}

// Delete card request
{
  "card_id": "card_1234567890"
}

// Invalid request - missing required field
{
  "expire_year": 2025 // Error: card_id required for update
}
```

### ⚠️ Important Validations
- All operations require header verification fields
- Create operation only needs transaction_token
- Update and delete operations require card_id
- All update fields are optional except card_id
- Boolean default field for setting primary payment method

### 🏷️ Tags
**Keywords:** payment, credit-card, billing, stripe, transaction
**Category:** #schema #validation #joi #card-setting