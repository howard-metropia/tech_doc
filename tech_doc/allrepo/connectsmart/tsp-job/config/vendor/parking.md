# Parking Vendor Configuration

## Overview
**File**: `config/vendor/parking.js`  
**Type**: Vendor Configuration  
**Purpose**: Provides configuration for multiple parking service providers across different regions

## Service Providers

### ParkingLotApp (Taiwan Only)
```javascript
parkinglotapp: {
  url: 'https://third-party-api-sandbox.parkinglotapp.com',
  auth: {
    client_id: process.env.PARKINGLOTAPP_CLIENT_ID,
    client_secret: process.env.PARKINGLOTAPP_CLIENT_SECRET,
  },
}
```

### Inrix (US Only)
```javascript
inrix: {
  auth_url: 'https://uas-api.inrix.com',
  url: 'https://api.parkme.com',
  auth: {
    appId: process.env.INRIX_APPID,
    hashToken: process.env.INRIX_HASHTOKEN,
  },
}
```

### Smarking (Houston Only)
```javascript
smarking: {
  url: 'https://my.smarking.net',
  auth: {
    token: process.env.SMARKING_TOKEN,
  },
}
```

## Regional Configuration

### Taiwan - ParkingLotApp
- **Provider**: 停車大聲公 (Parking Loudhailer)
- **Coverage**: Taiwan market
- **API Type**: RESTful API with OAuth
- **Environment**: Sandbox endpoint

### United States - Inrix
- **Provider**: Inrix/ParkMe
- **Coverage**: US market
- **API Type**: RESTful API with app-based authentication
- **Documentation**: https://docs.inrix.com/

### Houston - Smarking
- **Provider**: Smarking
- **Coverage**: Houston specific
- **API Type**: Token-based authentication
- **Reference**: MET-8396 (Metropia ticket)

## Authentication Methods

### OAuth 2.0 (ParkingLotApp)
- **client_id**: Application identifier
- **client_secret**: Application secret
- **Flow**: Client credentials grant

### App-Based Auth (Inrix)
- **appId**: Application identifier
- **hashToken**: Pre-computed hash token
- **Endpoints**: Separate auth and API URLs

### Token-Based Auth (Smarking)
- **token**: Bearer token for API access
- **Simple**: Single token authentication

## Environment Variables

### Required Variables
```bash
# ParkingLotApp (Taiwan)
PARKINGLOTAPP_CLIENT_ID=your_client_id
PARKINGLOTAPP_CLIENT_SECRET=your_client_secret

# Inrix (US)
INRIX_APPID=your_app_id
INRIX_HASHTOKEN=your_hash_token

# Smarking (Houston)
SMARKING_TOKEN=your_token
```

## API Endpoints

### ParkingLotApp URLs
- **Base URL**: `https://third-party-api-sandbox.parkinglotapp.com`
- **Environment**: Sandbox (development/testing)
- **Protocol**: HTTPS with OAuth

### Inrix URLs
- **Auth URL**: `https://uas-api.inrix.com`
- **API URL**: `https://api.parkme.com`
- **Split Architecture**: Separate authentication and data endpoints

### Smarking URLs
- **Base URL**: `https://my.smarking.net`
- **Unified**: Single endpoint for all operations

## Usage Examples

### ParkingLotApp Integration
```javascript
const config = require('./config/vendor/parking');

const parkingClient = new ParkingLotAppAPI({
  baseURL: config.parkinglotapp.url,
  clientId: config.parkinglotapp.auth.client_id,
  clientSecret: config.parkinglotapp.auth.client_secret
});
```

### Inrix Integration
```javascript
const config = require('./config/vendor/parking');

const inrixClient = new InrixAPI({
  authURL: config.inrix.auth_url,
  apiURL: config.inrix.url,
  appId: config.inrix.auth.appId,
  hashToken: config.inrix.auth.hashToken
});
```

### Smarking Integration
```javascript
const config = require('./config/vendor/parking');

const smarkingClient = new SmarkingAPI({
  baseURL: config.smarking.url,
  token: config.smarking.auth.token
});
```

## Service Capabilities

### ParkingLotApp Features
- **Real-time Availability**: Live parking space data
- **Pricing Information**: Dynamic pricing updates
- **Location Data**: Detailed parking facility information
- **Regional Coverage**: Taiwan-specific locations

### Inrix Features
- **Comprehensive Coverage**: US-wide parking data
- **ParkMe Integration**: Established parking database
- **Historical Data**: Parking pattern analytics
- **API Documentation**: Well-documented API

### Smarking Features
- **Smart Parking**: IoT-enabled parking solutions
- **Houston Focus**: City-specific implementation
- **Real-time Monitoring**: Live occupancy tracking
- **Custom Integration**: Tailored for Metropia needs

## Configuration Structure

### Consistent Pattern
```javascript
{
  url: 'api_endpoint',
  auth: {
    // authentication parameters
  }
}
```

### Provider-Specific Auth
- **Flexibility**: Each provider uses different auth methods
- **Standardization**: Consistent configuration structure
- **Security**: Environment variable-based credential storage

## Integration Points

### Common Use Cases
- **Parking Search**: Find available parking spaces
- **Pricing Queries**: Get parking rates and fees
- **Reservation**: Book parking spaces in advance
- **Real-time Updates**: Live availability information

### Service Selection
```javascript
const getParkingProvider = (region) => {
  switch (region) {
    case 'taiwan':
      return config.parkinglotapp;
    case 'houston':
      return config.smarking;
    case 'us':
    default:
      return config.inrix;
  }
};
```

## Security Considerations

### Credential Management
- **Environment Variables**: Secure credential storage
- **No Hardcoding**: No credentials in source code
- **Per-Provider**: Separate credentials for each service

### API Security
- **HTTPS**: All endpoints use secure connections
- **Authentication**: Proper authentication for each provider
- **Token Management**: Secure token handling

## Error Handling

### Configuration Validation
```javascript
const validateConfig = (provider) => {
  if (!provider.url) {
    throw new Error('Provider URL not configured');
  }
  
  if (!provider.auth || Object.keys(provider.auth).length === 0) {
    throw new Error('Provider authentication not configured');
  }
};
```

### Provider Availability
- **Fallback Logic**: Handle provider outages
- **Circuit Breaker**: Prevent cascading failures
- **Monitoring**: Track provider health

## Testing Configuration

### Test Environment
```javascript
const testConfig = {
  parkinglotapp: {
    url: 'http://localhost:3001',
    auth: {
      client_id: 'test-client',
      client_secret: 'test-secret'
    }
  }
};
```

### Mock Providers
- **Local Testing**: Use localhost endpoints
- **Mock Responses**: Simulate provider responses
- **Test Credentials**: Non-production credentials

## Monitoring

### Provider Health
- **Endpoint Monitoring**: Track API availability
- **Response Times**: Monitor performance
- **Error Rates**: Track failed requests

### Usage Analytics
- **Request Volume**: Track API usage per provider
- **Regional Distribution**: Monitor usage by region
- **Cost Tracking**: Monitor API costs

## Documentation References

### External Documentation
- **Inrix**: https://docs.inrix.com/
- **Metropia Ticket**: MET-8396 (Smarking integration)
- **Provider Support**: Individual provider documentation

### Internal Documentation
- Integration guides for each provider
- Authentication setup procedures
- Regional deployment guides

## Best Practices

### Configuration Management
- **Environment Separation**: Different configs per environment
- **Credential Rotation**: Regular credential updates
- **Access Control**: Limit configuration access

### API Integration
- **Rate Limiting**: Respect provider rate limits
- **Caching**: Cache responses appropriately
- **Error Handling**: Graceful degradation strategies

## Future Considerations

### Scalability
- **New Providers**: Easy addition of new parking providers
- **Regional Expansion**: Support for additional regions
- **Feature Parity**: Standardize feature sets across providers

### Enhancement Opportunities
- **Unified Interface**: Common interface for all providers
- **Load Balancing**: Distribute requests across providers
- **Analytics**: Enhanced usage and performance analytics