# Parking Services Configuration

### 📋 Configuration Overview
- **Purpose:** Configures multiple parking service provider integrations for different regions
- **Module Type:** Multi-vendor service credentials and API endpoints
- **Environment:** All environments (dev/staging/prod) with region-specific services

### 🔧 Configuration Values
| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `parkinglotapp.url` | String | No | 停車大聲公 API URL (Taiwan only) | `'https://third-party-api-sandbox.parkinglotapp.com'` |
| `parkinglotapp.auth.client_id` | String | Yes | ParkingLotApp client ID | `process.env.PARKINGLOTAPP_CLIENT_ID` |
| `parkinglotapp.auth.client_secret` | String | Yes | ParkingLotApp client secret | `process.env.PARKINGLOTAPP_CLIENT_SECRET` |
| `inrix.auth_url` | String | No | Inrix authentication URL (US only) | `'https://uas-api.inrix.com'` |
| `inrix.url` | String | No | Inrix ParkMe API URL | `'https://api.parkme.com'` |
| `inrix.auth.appId` | String | Yes | Inrix application ID | `process.env.INRIX_APPID` |
| `inrix.auth.hashToken` | String | Yes | Inrix hash token for authentication | `process.env.INRIX_HASHTOKEN` |
| `smarking.url` | String | No | Smarking API URL (Houston only) | `'https://my.smarking.net'` |
| `smarking.auth.token` | String | Yes | Smarking authentication token | `process.env.SMARKING_TOKEN` |

### 📝 Usage Example
```javascript
// How to import and use this configuration
const parkingConfig = require('./config/vendor/parking');

// Taiwan - ParkingLotApp integration
const parkingLotResponse = await axios.get(`${parkingConfig.parkinglotapp.url}/api/parking`, {
  params: {
    client_id: parkingConfig.parkinglotapp.auth.client_id,
    client_secret: parkingConfig.parkinglotapp.auth.client_secret
  }
});

// US - Inrix ParkMe integration
const inrixAuth = await axios.post(`${parkingConfig.inrix.auth_url}/auth`, {
  appId: parkingConfig.inrix.auth.appId,
  hashToken: parkingConfig.inrix.auth.hashToken
});

// Houston - Smarking integration
const smarkingData = await axios.get(`${parkingConfig.smarking.url}/api/spots`, {
  headers: {
    'Authorization': `Bearer ${parkingConfig.smarking.auth.token}`
  }
});
```

### ⚠️ Security Notes
- **Sensitive Data:** All authentication credentials (`client_secret`, `hashToken`, `token`) are sensitive
- **Environment Management:** Store all credentials in environment variables, never in code
- **Regional Isolation:** Different services for different regions - ensure proper routing
- **API Keys:** Each service has different authentication methods - handle appropriately
- **Rate Limiting:** Monitor usage across all parking service providers

### 🏷️ Tags
**Keywords:** parking, multi-vendor, taiwan, houston, inrix, smarking, parkinglotapp, regional-services  
**Category:** #config #vendor #credentials #parking #regional

---
Note: Each parking service serves different geographic regions with unique authentication requirements.