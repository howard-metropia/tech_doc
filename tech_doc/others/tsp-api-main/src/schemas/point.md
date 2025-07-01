# Point Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates point/reward transactions and payment processing
- **Validation Library:** Joi
- **Related Controller:** point controller

## 🔧 Schema Structure
```javascript
{
  post: Joi.object({
    userId: Joi.number().integer().required(),
    zone: Joi.string().required(),
    product_id: Joi.number().integer().required(),
    transaction_token: Joi.string().optional().allow(null),
    payment_way: Joi.number().integer().optional().allow(null),
    lat: Joi.number().optional().allow(null),
    lon: Joi.number().optional().allow(null)
  })
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| userId | number | Yes | Integer | User making the transaction |
| zone | string | Yes | - | Geographic zone identifier |
| product_id | number | Yes | Integer | Product being purchased |
| transaction_token | string | No | Allow null | Payment transaction token |
| payment_way | number | No | Integer, allow null | Payment method identifier |
| lat | number | No | Allow null | Transaction latitude |
| lon | number | No | Allow null | Transaction longitude |

## 💡 Usage Example
```javascript
// Complete point transaction request
{
  "userId": 123,
  "zone": "downtown",
  "product_id": 456,
  "transaction_token": "tx_abc123",
  "payment_way": 1,
  "lat": 37.7749,
  "lon": -122.4194
}

// Minimal point transaction request
{
  "userId": 123,
  "zone": "suburb",
  "product_id": 789
  // Optional fields can be null or omitted
}

// Request example that fails validation
{
  "userId": "invalid",  // Error: must be a number
  "zone": "",  // Error: required field cannot be empty
  "product_id": -1  // Error: negative IDs typically not allowed
}
```

## ⚠️ Important Validations
- User ID and product ID are mandatory integers
- Zone field is required and cannot be empty
- Optional fields explicitly allow null values
- Coordinates are optional for location-based transactions
- Transaction token used for payment processing verification

## 🏷️ Tags
**Keywords:** points, rewards, transactions, payments, geolocation
**Category:** #schema #validation #joi #point