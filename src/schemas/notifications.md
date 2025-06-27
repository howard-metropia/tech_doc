# Notifications Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates notification retrieval and status update requests
- **Validation Library:** Joi
- **Related Controller:** notifications controller

## 🔧 Schema Structure
```javascript
{
  get: Joi.object({
    ...verifyHeaderFieldsByJoi,
    offset: Joi.number().integer().default(0),
    perpage: Joi.number().integer().default(10),
    status: Joi.string().pattern(/[0-9,]+/).default('0,1,2,5'),
    type: Joi.string().pattern(/[0-9,]+/),
    category: Joi.string().valid('general', 'incentive', '')
  }),
  update: Joi.object({
    ...verifyHeaderFieldsByJoi,
    id: Joi.number().integer(),
    status: Joi.number().integer().valid(0, 1, 2, 3, 4, 5).default(3)
  })
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| offset | number | No | Integer, default 0 | Pagination offset |
| perpage | number | No | Integer, default 10 | Items per page |
| status | string | No | Pattern: numbers/commas, default '0,1,2,5' | Notification status filter |
| type | string | No | Pattern: numbers/commas | Notification type filter |
| category | string | No | 'general'/'incentive'/empty | Notification category |
| id | number | No | Integer | Notification ID to update |
| status | number | No | 0-5, default 3 | New status value |

## 💡 Usage Example
```javascript
// Get notifications with filters
{
  "offset": 20,
  "perpage": 15,
  "status": "0,1,2",
  "type": "1,3,5",
  "category": "general"
}

// Update notification status
{
  "id": 123,
  "status": 1
}

// Get notifications with defaults
{
  // Uses default offset=0, perpage=10, status='0,1,2,5'
}
```

## ⚠️ Important Validations
- Status and type filters use comma-separated number patterns
- Status values restricted to 0-5 range for updates
- Category must be specific predefined values or empty
- Pagination parameters default if not provided
- Header fields required for authentication
- Update status defaults to 3 if not specified

## 🏷️ Tags
**Keywords:** notifications, status updates, pagination, filtering, categories
**Category:** #schema #validation #joi #notifications