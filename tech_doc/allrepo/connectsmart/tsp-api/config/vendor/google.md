# Google Maps API Configuration

### 📋 Configuration Overview
- **Purpose:** Configures Google Maps API integration for mapping services and geocoding operations
- **Module Type:** Service credentials 
- **Environment:** All environments (dev/staging/prod)

### 🔧 Configuration Values
| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `maps.apiKey` | String | Yes | Google Maps API key from environment variable | `process.env.GOOGLE_MAPS_API_KEY` |
| `maps.url` | String | No | Base URL for Google Maps API | `'https://maps.googleapis.com'` |

### 📝 Usage Example
```javascript
// How to import and use this configuration
const googleConfig = require('./config/vendor/google');
console.log(googleConfig.maps.apiKey); // Your Google Maps API key
console.log(googleConfig.maps.url); // 'https://maps.googleapis.com'

// Typical usage in services
const response = await axios.get(`${googleConfig.maps.url}/maps/api/geocode/json`, {
  params: {
    key: googleConfig.maps.apiKey,
    address: '123 Main St'
  }
});
```

### ⚠️ Security Notes
- **Sensitive Data:** `GOOGLE_MAPS_API_KEY` contains API credentials and must be protected
- **Environment Management:** API key should be stored in environment variables, never hardcoded
- **Access Control:** Restrict API key usage by domain/IP in Google Cloud Console
- **Monitoring:** Monitor API usage to detect unauthorized access or quota breaches

### 🏷️ Tags
**Keywords:** google-maps, geocoding, mapping, api-integration, location-services  
**Category:** #config #vendor #credentials #google #maps

---
Note: Ensure Google Maps API key has appropriate restrictions and billing alerts configured.