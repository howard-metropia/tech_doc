# HERE Device ID Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates HERE Maps device information logging for analytics
- **Validation Library:** Joi
- **Related Controller:** here-device-id controller

## 🔧 Schema Structure
```javascript
{
  logDeviceInfo: Joi.object({
    ...verifyHeaderFieldsByJoi,
    here_device_id: Joi.string().required(),
    platform: Joi.string().allow(null),
    device_model: Joi.string().allow(null),
    platform_device_id: Joi.string().allow(null),
    os_version: Joi.string().allow(null),
    app_version: Joi.string().allow(null)
  })
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| here_device_id | string | Yes | - | HERE Maps device identifier |
| platform | string | No | Allow null | Device platform (iOS/Android) |
| device_model | string | No | Allow null | Device model name |
| platform_device_id | string | No | Allow null | Platform-specific device ID |
| os_version | string | No | Allow null | Operating system version |
| app_version | string | No | Allow null | Application version |
| ...header fields | various | Yes | From verifyHeaderFieldsByJoi | Authentication and device info |

## 💡 Usage Example
```javascript
// Complete device info logging
{
  "here_device_id": "here_abc123xyz",
  "platform": "iOS",
  "device_model": "iPhone 14 Pro",
  "platform_device_id": "ABCD-1234-EFGH-5678",
  "os_version": "17.1.1",
  "app_version": "2.4.1"
}

// Minimal device info logging
{
  "here_device_id": "here_def456abc"
  // All other fields can be null or omitted
}

// Request example that fails validation
{
  "platform": "iOS"
  // Error: here_device_id is required
}
```

## ⚠️ Important Validations
- HERE device ID is mandatory and cannot be null
- All other device fields are optional and allow null values
- Includes standard header field validations for authentication
- Used for HERE Maps integration analytics and tracking
- Device information helps with platform-specific optimizations

## 🏷️ Tags
**Keywords:** HERE Maps, device tracking, analytics, platform detection, versioning
**Category:** #schema #validation #joi #here-device-id