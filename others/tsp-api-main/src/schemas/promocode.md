# Promocode Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates promotional code verification and raffle ticket listing
- **Validation Library:** Joi
- **Related Controller:** promocode controller

## 🔧 Schema Structure
```javascript
{
  checkPromocode: Joi.object({
    promo_code: Joi.string().required()
  }),
  raffleTicketListSchema: Joi.object({
    limit: Joi.number().integer().min(1),
    current_page: Joi.number().integer().min(1),
    search: Joi.string().default('')
  })
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| promo_code | string | Yes | - | Promotional code to validate |
| limit | number | No | Integer ≥ 1 | Number of tickets per page |
| current_page | number | No | Integer ≥ 1 | Current page number |
| search | string | No | Defaults to empty string | Search filter for tickets |

## 💡 Usage Example
```javascript
// Check promocode request
{
  "promo_code": "SUMMER2024"
}

// Raffle ticket list request
{
  "limit": 20,
  "current_page": 1,
  "search": "winner"
}

// Minimal raffle ticket request (uses defaults)
{
  // limit and current_page default if not provided
  // search defaults to empty string
}

// Request example that fails validation
{
  "promo_code": "",  // Error: required field cannot be empty
  "limit": 0  // Error: must be at least 1
}
```

## ⚠️ Important Validations
- Promotional code is mandatory for validation requests
- Pagination parameters must be positive integers when provided
- Search parameter defaults to empty string if not specified
- Limit and current_page must start from 1, not 0

## 🏷️ Tags
**Keywords:** promotional codes, raffle tickets, pagination, validation
**Category:** #schema #validation #joi #promocode