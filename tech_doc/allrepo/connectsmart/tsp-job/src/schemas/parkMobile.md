# ParkMobile Schema

## Quick Summary
OAuth token validation schema for ParkMobile API integration in the TSP Job system. Provides structured validation for access tokens, token types, expiration times, and scope parameters required for secure communication with ParkMobile parking services.

## Technical Analysis

### Code Structure
```javascript
const Joi = require('joi');

module.exports = {
  token: Joi.object({
    access_token: Joi.string().required(),
    expires_in: Joi.alternatives().try(Joi.string(), Joi.number()),
    token_type: Joi.string().required(),
    scope: Joi.string().required(),
  }),
};
```

### Schema Components
- **Token Object**: Primary validation schema for OAuth token responses
- **access_token**: Required string field containing the JWT or bearer token
- **expires_in**: Flexible field accepting both string and number formats for expiration time
- **token_type**: Required string defining token type (typically "Bearer")
- **scope**: Required string specifying API access permissions

### Implementation Details
The schema follows OAuth 2.0 RFC specification standards for token validation. The flexible `expires_in` field handles variations in API response formats where some services return expiration as seconds (number) while others return formatted time strings.

## Usage/Integration

### Primary Use Cases
- **Token Validation**: Validates OAuth responses from ParkMobile API
- **API Integration**: Ensures proper token structure before storage
- **Service Authentication**: Validates credentials for parking service operations
- **Error Prevention**: Catches malformed token responses early in the pipeline

### Integration Points
```javascript
// Token validation in ParkMobile service
const { token } = require('../schemas/parkMobile');
const { error, value } = token.validate(tokenResponse);

// Usage in authentication flow
if (error) {
  throw new Error(`Invalid token format: ${error.message}`);
}
const validatedToken = value;
```

### Scheduling Context
This schema is utilized in scheduled jobs that refresh ParkMobile authentication tokens, typically running every 30-60 minutes to maintain active API sessions.

## Dependencies

### Core Dependencies
- **joi**: Schema validation library for JavaScript objects
- **@maas/core**: Core utilities for MaaS platform integration
- **parkMobile service**: Uses this schema for token validation

### External Service Dependencies
- **ParkMobile OAuth API**: Source of token data being validated
- **Redis Cache**: Stores validated tokens for reuse across services
- **MySQL Portal DB**: Logs authentication events and token refresh cycles

### Configuration Requirements
```javascript
// Environment variables required
PARKMOBILE_CLIENT_ID=your_client_id
PARKMOBILE_CLIENT_SECRET=your_client_secret
PARKMOBILE_API_URL=https://api.parkmobile.com
PARKMOBILE_TOKEN_CACHE_TTL=3600
```

## Code Examples

### Basic Token Validation
```javascript
const { token } = require('./schemas/parkMobile');

// Validate incoming OAuth response
const tokenResponse = {
  access_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  expires_in: 3600,
  token_type: "Bearer",
  scope: "read write parking"
};

const validation = token.validate(tokenResponse);
if (validation.error) {
  console.error('Token validation failed:', validation.error.details);
} else {
  console.log('Token validated successfully:', validation.value);
}
```

### Service Integration Pattern
```javascript
// In ParkMobile service authentication method
class ParkMobileService {
  async refreshToken() {
    const response = await this.oauth.getToken();
    
    // Validate response structure
    const { error, value } = token.validate(response);
    if (error) {
      throw new AuthenticationError(`Invalid token response: ${error.message}`);
    }
    
    // Store validated token
    await this.cache.setToken(value.access_token, value.expires_in);
    return value;
  }
}
```

### Error Handling Implementation
```javascript
// Comprehensive error handling with schema validation
const validateAndStoreToken = async (tokenData) => {
  try {
    const { error, value } = token.validate(tokenData);
    
    if (error) {
      // Log validation errors with context
      logger.error('ParkMobile token validation failed', {
        error: error.details,
        receivedData: tokenData,
        timestamp: new Date()
      });
      throw new ValidationError('Token validation failed');
    }
    
    // Handle different expires_in formats
    const expiresIn = typeof value.expires_in === 'string' 
      ? parseInt(value.expires_in, 10) 
      : value.expires_in;
    
    const expirationTime = new Date(Date.now() + (expiresIn * 1000));
    
    return {
      token: value.access_token,
      type: value.token_type,
      scope: value.scope,
      expiresAt: expirationTime
    };
  } catch (error) {
    logger.error('Token processing error', error);
    throw error;
  }
};
```

### Scheduled Job Integration
```javascript
// Token refresh job using schema validation
const refreshParkMobileToken = async () => {
  try {
    const newTokenData = await parkMobileAPI.refreshToken();
    
    // Validate token structure
    const { error, value } = token.validate(newTokenData);
    if (error) {
      await notificationService.alertAdmins('ParkMobile token refresh failed', error);
      return;
    }
    
    // Update cache and database
    await Promise.all([
      redis.setex(`parkmobile:token`, value.expires_in, value.access_token),
      mysql.query('UPDATE pm_api_token SET token = ?, expires_at = ?', [
        value.access_token,
        new Date(Date.now() + value.expires_in * 1000)
      ])
    ]);
    
    logger.info('ParkMobile token refreshed successfully');
  } catch (error) {
    logger.error('Token refresh job failed', error);
  }
};
```

## Related Components
- **parkMobile service**: Primary consumer of this validation schema
- **update-parkmobile-token job**: Scheduled token refresh using this schema
- **PmApiToken model**: Database model for token storage
- **OAuth middleware**: Authentication middleware utilizing token validation