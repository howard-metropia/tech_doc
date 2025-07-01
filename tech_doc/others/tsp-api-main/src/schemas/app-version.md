# App Version Schema Documentation

### 📋 Schema Overview
- **Purpose:** Validates app version check and update endpoints
- **Validation Library:** Joi
- **Related Controller:** app-version.js

### 🔧 Schema Structure
```javascript
// Version check request
get: {
  version: string (optional),
  os: string (optional, 'ios' or 'android'),
  newversion: string (optional)
}
```

### 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| version | string | No | - | Current app version |
| os | string | No | 'ios', 'android' | Operating system |
| newversion | string | No | - | Target version for update |

### 💡 Usage Example
```javascript
// Version check request
{
  "version": "1.2.3",
  "os": "ios",
  "newversion": "1.3.0"
}

// Minimal request
{
  "version": "1.2.3"
}

// Platform-specific check
{
  "version": "1.2.3",
  "os": "android"
}

// Invalid request - wrong OS value
{
  "version": "1.2.3",
  "os": "windows" // Error: must be 'ios' or 'android'
}
```

### ⚠️ Important Validations
- All fields are optional for maximum flexibility
- OS field accepts only 'ios' or 'android' values
- Version strings have no format restrictions
- Simple schema focused on version comparison logic
- Typically used for app update notifications

### 🏷️ Tags
**Keywords:** app-version, update, ios, android, version-check
**Category:** #schema #validation #joi #app-version