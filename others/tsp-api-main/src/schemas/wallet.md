# Wallet Schema Documentation

### 📋 Schema Overview
- **Purpose:** Validates digital wallet settings and auto-refill configuration
- **Validation Library:** Joi
- **Related Controller:** wallet.js

### 🔧 Schema Structure
```javascript
// Wallet settings configuration
walletSetting: {
  auto_refill: boolean (required),
  below_balance: number (optional, nullable),
  refill_plan_id: number (optional, nullable, integer)
}
```

### 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| auto_refill | boolean | Yes | - | Enable/disable automatic refill |
| below_balance | number | No | nullable | Balance threshold for auto-refill |
| refill_plan_id | number | No | integer, nullable | Selected refill plan identifier |

### 💡 Usage Example
```javascript
// Enable auto-refill with threshold
{
  "auto_refill": true,
  "below_balance": 10.00,
  "refill_plan_id": 3
}

// Disable auto-refill
{
  "auto_refill": false,
  "below_balance": null,
  "refill_plan_id": null
}

// Enable auto-refill without specific plan
{
  "auto_refill": true,
  "below_balance": 5.00
}

// Invalid request - wrong data type
{
  "auto_refill": "yes", // Error: must be boolean
  "below_balance": "10" // Error: must be number
}
```

### ⚠️ Important Validations
- Auto-refill setting is required boolean field
- Balance threshold and plan ID are optional and nullable
- Refill plan ID must be integer when provided
- Below balance accepts decimal numbers for currency amounts
- All requests require header verification fields
- Null values are explicitly allowed for optional fields

### 🏷️ Tags
**Keywords:** wallet, payment, auto-refill, balance, digital-wallet
**Category:** #schema #validation #joi #wallet