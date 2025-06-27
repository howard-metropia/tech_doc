# Transit Payment Schema Documentation

### 📋 Schema Overview
- **Purpose:** Validates transit pass usage and payment transactions
- **Validation Library:** Joi
- **Related Controller:** transit-payment.js

### 🔧 Schema Structure
```javascript
// Transit pass usage validation
passUse: {
  userId: number (required, integer),
  pass_uuid: string (required),
  event_uuid: string (required),
  zone: string (required)
}
```

### 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| userId | number | Yes | integer | User identifier |
| pass_uuid | string | Yes | - | Transit pass UUID |
| event_uuid | string | Yes | - | Transaction event UUID |
| zone | string | Yes | - | Transit zone identifier |

### 💡 Usage Example
```javascript
// Transit pass usage
{
  "userId": 12345,
  "pass_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "event_uuid": "550e8400-e29b-41d4-a716-446655440001",
  "zone": "zone_a"
}

// Invalid request - wrong data type
{
  "userId": "12345", // Error: must be number
  "pass_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "event_uuid": "550e8400-e29b-41d4-a716-446655440001",
  "zone": "zone_a"
}

// Invalid request - missing required field
{
  "userId": 12345,
  "pass_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "event_uuid": "550e8400-e29b-41d4-a716-446655440001"
  // Error: zone field required
}
```

### ⚠️ Important Validations
- User ID must be numeric integer
- Pass UUID and event UUID are string identifiers
- Zone string identifies transit fare zones
- All fields are required for pass usage validation
- Simple schema focused on transit payment events

### 🏷️ Tags
**Keywords:** transit, payment, pass, uuid, fare-zones
**Category:** #schema #validation #joi #transit-payment