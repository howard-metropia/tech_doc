# ParkMobile Configuration Documentation

## Quick Summary

This configuration module manages the authentication credentials for integrating ParkMobile's parking services API into the TSP Job system. ParkMobile is a leading parking solution provider that enables users to find, reserve, and pay for parking through mobile applications. This configuration facilitates OAuth2-based authentication for accessing ParkMobile's partner API endpoints, enabling parking-related features within the transportation service platform.

## Technical Analysis

### Code Structure

```javascript
module.exports = {
  clientId: process.env.PARKMOBILE_CLIENT_ID || 'pm_partner_metropia',
  clientSecret: process.env.PARKMOBILE_CLIENT_SECRET || 'nNMqukdrlipF6koLAxpYaB2muHu7VtIma9bUH6uvvk95EYlNaYXbnJe3ngeK2mc8',
};
```

### Configuration Properties

1. **clientId**: OAuth2 client identifier
   - Sources from `PARKMOBILE_CLIENT_ID` environment variable
   - Defaults to 'pm_partner_metropia' indicating partner status
   - Used for identifying the application to ParkMobile's API

2. **clientSecret**: OAuth2 client secret
   - Sources from `PARKMOBILE_CLIENT_SECRET` environment variable
   - Contains sensitive authentication credential
   - Used in conjunction with clientId for secure API access

### Authentication Flow

The configuration supports OAuth2 Client Credentials Grant flow:
1. Application uses clientId and clientSecret to request access token
2. ParkMobile validates credentials and issues temporary access token
3. Access token is used for subsequent API requests
4. Token refresh occurs automatically when expired

## Usage/Integration

### Loading Configuration

```javascript
const parkmobileConfig = require('./config/vendor/parkmobile');

// Access credentials
const { clientId, clientSecret } = parkmobileConfig;
```

### OAuth2 Token Acquisition

```javascript
const axios = require('axios');
const parkmobileConfig = require('./config/vendor/parkmobile');

async function getParkMobileAccessToken() {
  const tokenUrl = 'https://api.parkmobile.io/oauth/token';
  
  const response = await axios.post(tokenUrl, {
    grant_type: 'client_credentials',
    client_id: parkmobileConfig.clientId,
    client_secret: parkmobileConfig.clientSecret
  }, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  });
  
  return response.data.access_token;
}
```

### Integration with ParkMobile Service

```javascript
const ParkMobileService = require('./services/parkMobile');
const config = require('./config/vendor/parkmobile');

class ParkMobileIntegration {
  constructor() {
    this.config = config;
    this.accessToken = null;
    this.tokenExpiry = null;
  }

  async ensureAuthenticated() {
    if (!this.accessToken || new Date() >= this.tokenExpiry) {
      await this.refreshToken();
    }
  }

  async refreshToken() {
    const response = await fetch('https://api.parkmobile.io/oauth/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        grant_type: 'client_credentials',
        client_id: this.config.clientId,
        client_secret: this.config.clientSecret
      })
    });

    const data = await response.json();
    this.accessToken = data.access_token;
    this.tokenExpiry = new Date(Date.now() + (data.expires_in * 1000));
  }
}
```

## Dependencies

### Internal Dependencies

1. **ParkMobile Service** (`services/parkMobile.js`): Primary consumer of configuration
2. **Token Update Job** (`update-parkmobile-token.js`): Manages token refresh cycles
3. **Event Monitoring Job** (`parkmobile-event-monitoring.js`): Uses credentials for API access
4. **Cache Management** (`purge-parkmobile-cache.js`): Authenticates cache operations

### External Dependencies

1. **ParkMobile API**: Third-party parking service provider
2. **OAuth2 Protocol**: Standard authentication framework
3. **Redis Cache**: Stores access tokens and API responses
4. **HTTP Clients**: axios, node-fetch, or native fetch for API requests

### Related Database Models

1. **PmApiToken**: Stores current access token and expiration
2. **pmParkingEvent**: Records parking session events
3. **pmParkingEvents**: Aggregated parking event data
4. **pmPriceObjects**: Parking rate information cache

## Code Examples

### Token Management Pattern

```javascript
const parkmobileConfig = require('./config/vendor/parkmobile');
const redis = require('./config/database/redis');

class ParkMobileTokenManager {
  constructor() {
    this.config = parkmobileConfig;
    this.tokenKey = 'parkmobile:access_token';
    this.expiryKey = 'parkmobile:token_expiry';
  }

  async getValidToken() {
    // Check cached token
    const cachedToken = await redis.get(this.tokenKey);
    const cachedExpiry = await redis.get(this.expiryKey);
    
    if (cachedToken && new Date() < new Date(cachedExpiry)) {
      return cachedToken;
    }
    
    // Request new token
    const newToken = await this.requestNewToken();
    await this.cacheToken(newToken);
    
    return newToken.access_token;
  }

  async requestNewToken() {
    const response = await fetch('https://api.parkmobile.io/oauth/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        grant_type: 'client_credentials',
        client_id: this.config.clientId,
        client_secret: this.config.clientSecret
      })
    });

    if (!response.ok) {
      throw new Error(`ParkMobile authentication failed: ${response.status}`);
    }

    return response.json();
  }

  async cacheToken(tokenData) {
    const expiryTime = new Date(Date.now() + (tokenData.expires_in * 1000));
    
    await redis.setex(
      this.tokenKey, 
      tokenData.expires_in - 60, // Expire 1 minute early
      tokenData.access_token
    );
    
    await redis.set(this.expiryKey, expiryTime.toISOString());
  }
}
```

### API Request Implementation

```javascript
const parkmobileConfig = require('./config/vendor/parkmobile');

class ParkMobileAPI {
  constructor(tokenManager) {
    this.tokenManager = tokenManager;
    this.baseUrl = 'https://api.parkmobile.io/v1';
  }

  async makeAuthenticatedRequest(endpoint, options = {}) {
    const token = await this.tokenManager.getValidToken();
    
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        ...options.headers,
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (response.status === 401) {
      // Token expired, retry with new token
      await this.tokenManager.requestNewToken();
      return this.makeAuthenticatedRequest(endpoint, options);
    }

    return response;
  }

  async getParkingZones(latitude, longitude, radius = 1000) {
    const endpoint = `/zones?lat=${latitude}&lng=${longitude}&radius=${radius}`;
    const response = await this.makeAuthenticatedRequest(endpoint);
    return response.json();
  }

  async startParkingSession(zoneId, vehicleId, duration) {
    const endpoint = '/parking-sessions';
    const response = await this.makeAuthenticatedRequest(endpoint, {
      method: 'POST',
      body: JSON.stringify({
        zone_id: zoneId,
        vehicle_id: vehicleId,
        duration_minutes: duration
      })
    });
    return response.json();
  }
}
```

### Environment Configuration

```javascript
// Development environment
if (process.env.NODE_ENV === 'development') {
  process.env.PARKMOBILE_CLIENT_ID = 'pm_partner_metropia_dev';
  process.env.PARKMOBILE_CLIENT_SECRET = 'dev_secret_key';
}

// Production validation
if (process.env.NODE_ENV === 'production') {
  if (!process.env.PARKMOBILE_CLIENT_ID || !process.env.PARKMOBILE_CLIENT_SECRET) {
    throw new Error('ParkMobile credentials must be set in production');
  }
}

// Load configuration with validation
const config = require('./config/vendor/parkmobile');

if (!config.clientId || !config.clientSecret) {
  console.error('Warning: ParkMobile configuration is incomplete');
}
```

### Scheduled Token Refresh Job

```javascript
const cron = require('node-cron');
const parkmobileConfig = require('./config/vendor/parkmobile');

// Schedule token refresh every 55 minutes
cron.schedule('*/55 * * * *', async () => {
  try {
    const tokenManager = new ParkMobileTokenManager();
    await tokenManager.requestNewToken();
    console.log('ParkMobile token refreshed successfully');
  } catch (error) {
    console.error('Failed to refresh ParkMobile token:', error);
    // Send alert to monitoring system
  }
});
```

## Security Considerations

1. **Credential Storage**:
   - Never commit secrets to version control
   - Use environment variables in all deployments
   - Implement secret rotation policies

2. **Token Security**:
   - Store tokens encrypted in cache
   - Implement token expiration handling
   - Log authentication failures for monitoring

3. **API Rate Limiting**:
   - Respect ParkMobile's rate limits
   - Implement request queuing if needed
   - Monitor API usage patterns

## Best Practices

1. **Configuration Management**:
   - Use separate credentials for each environment
   - Document all required environment variables
   - Validate configuration on startup

2. **Error Handling**:
   - Implement retry logic for transient failures
   - Log all API errors with context
   - Provide graceful degradation when API is unavailable

3. **Performance Optimization**:
   - Cache API responses appropriately
   - Batch API requests when possible
   - Monitor response times and optimize slow queries

This configuration module enables secure integration with ParkMobile's parking services, providing the foundation for parking-related features throughout the TSP Job system while maintaining security and reliability standards.