# Handling Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates error handling requests for API failure reporting
- **Validation Library:** Joi
- **Related Controller:** Handling controller for error tracking and debugging

## 🔧 Schema Structure
```javascript
// Main schema definition
{
  result: Joi.string().valid('fail').required(),
  error: Joi.object({
    code: Joi.number().integer().required(),
    msg: Joi.string().required(),
    api: Joi.string().required(),
    user_id: Joi.number().integer().required(),
    time: Joi.string().required(),
    response: Joi.object().required(),
  }).required(),
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| result | string | Yes | Must be 'fail' | Fixed value indicating failure |
| error | object | Yes | Complex object | Complete error information |
| error.code | number | Yes | Integer | Error code identifier |
| error.msg | string | Yes | Any string | Error message description |
| error.api | string | Yes | Any string | API endpoint that failed |
| error.user_id | number | Yes | Integer | User ID associated with error |
| error.time | string | Yes | Any string | Timestamp of error occurrence |
| error.response | object | Yes | Any object | Original API response data |

## 💡 Usage Example
```javascript
// Request example that passes validation
{
  "result": "fail",
  "error": {
    "code": 500,
    "msg": "Internal server error",
    "api": "/api/v2/trips",
    "user_id": 12345,
    "time": "2024-01-15T10:30:00Z",
    "response": { "status": "error", "details": "Database connection failed" }
  }
}

// Request example that fails validation
{
  "result": "success", // Error: must be 'fail'
  "error": {
    "code": 500
    // Missing required fields: msg, api, user_id, time, response
  }
}
```

## ⚠️ Important Validations
- Result field must always be 'fail' - no other values accepted
- All error object fields are required for complete error tracking
- User ID must be a valid integer for user association
- Response object can contain any structure for debugging flexibility

## 🏷️ Tags
**Keywords:** error-handling, debugging, failure-tracking, api-monitoring
**Category:** #schema #validation #joi #error-handling