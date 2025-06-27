# Park Mobile Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates ParkMobile parking payment and session management
- **Validation Library:** Joi
- **Related Controller:** parkMobile controller

## 🔧 Schema Structure
```javascript
{
  getRateZone: { zone: number },
  getRatePrice: { zone, timeBlockUnit, timeBlockQuantity, timeBlockId },
  startParking: { price_id: uuid, lpn: string, lpnState: string, payment_type, payment_id },
  setReminderRequestParams: { id: string|number },
  setReminderRequestBody: { alert_before: number }
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| zone | number | Yes | - | Parking zone identifier |
| price_id | string | Yes | UUID format | Price calculation ID |
| lpn | string | Yes | Alphanumeric, max 10 chars | License plate number |
| lpnState | string | Yes | Exactly 2 characters | License plate state code |
| payment_type | string | Yes | 'token' or 'coin' | Payment method type |
| payment_id | number | Conditional | Required if payment_type='token' | Payment method ID |
| timeBlockUnit | string | Yes | 'minutes'/'hours'/'days' | Time duration unit |
| timeBlockQuantity | number | Yes | ≥ 1 | Duration quantity |
| alert_before | number | Yes | 0,5,10,15,20,25,30,35,40 | Minutes before expiry |

## 💡 Usage Example
```javascript
// Start parking session
{
  "price_id": "550e8400-e29b-41d4-a716-446655440000",
  "lpn": "ABC123",
  "lpnState": "CA",
  "payment_type": "token",
  "payment_id": 456
}

// Get rate pricing
{
  "zone": 1001,
  "timeBlockUnit": "hours",
  "timeBlockQuantity": 2,
  "timeBlockId": "block_123"
}

// Set parking reminder
{
  "id": "session_789",
  "alert_before": 15
}
```

## ⚠️ Important Validations
- License plates must be alphanumeric and max 10 characters
- State codes must be exactly 2 characters
- Payment ID required only when using token payment
- Time block units restricted to predefined values
- Alert timing limited to specific minute intervals
- Zone must be a valid number identifier
- Price ID must be valid UUID format

## 🏷️ Tags
**Keywords:** parking, parkmobile, payment, sessions, reminders, zones
**Category:** #schema #validation #joi #park-mobile