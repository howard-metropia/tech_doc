# Update ParkMobile Token Job

## Quick Summary
**Purpose**: Maintains valid OAuth2 access tokens for ParkMobile API authentication by refreshing them before expiration.

**Key Features**:
- Automatic token renewal using client credentials flow
- Proactive token management to prevent API failures
- Cleanup of expired tokens from database
- Secure credential handling

**Functionality**: Periodically requests new access tokens from ParkMobile's OAuth2 server and stores them in the database while removing expired tokens to maintain a clean token store.

## Technical Analysis

### Code Structure
Simple job wrapper around the token update service:

```javascript
module.exports = {
  inputs: {},
  fn: updateToken
};
```

### Implementation Details

1. **OAuth2 Client Credentials Flow**:
   ```javascript
   const getToken = async () => {
     const data = qs.stringify({
       grant_type: 'client_credentials',
       client_id: pmConfig.clientId,
       client_secret: pmConfig.clientSecret,
     });

     const options = {
       method: 'post',
       url: 'connect/token',
       headers: {
         'Content-Type': 'application/x-www-form-urlencoded',
       },
       data,
     };
     
     const resp = await http.request(options);
     return resp.data;
   };
   ```

2. **Token Storage Strategy**:
   ```javascript
   const updateToken = async () => {
     const tokenInfo = await getToken();
     
     // Store new token with calculated expiration
     await PmApiToken.query().insert({
       token: tokenInfo.access_token,
       expires: moment.utc().add(tokenInfo.expires_in, 'seconds').toISOString(),
     });
     
     // Clean up expired tokens
     await PmApiToken.query()
       .where('expires', '<=', moment.utc().add(1, 'minute').toISOString())
       .delete();
   };
   ```

3. **Security Features**:
   - Credentials stored in secure configuration
   - No token logging for security
   - HTTPS-only communication
   - Token validation before storage

### Authentication Flow

1. **Token Request**:
   - Uses ParkMobile's OAuth2 endpoint
   - Client credentials grant type
   - Returns access token with expiration time

2. **Token Management**:
   - Stores token with precise expiration timestamp
   - Maintains token history for debugging
   - Removes tokens expiring within 1 minute

## Usage/Integration

### Scheduling Configuration
- **Frequency**: Every 30 minutes (or based on token lifetime)
- **Timing**: Continuous throughout the day
- **Priority**: Critical - API access depends on valid tokens

### Cron Expression
```
*/30 * * * * // Every 30 minutes
```

### Integration Points
1. **ParkMobile OAuth2 Server**: Token provider
2. **Database**: Token storage
3. **ParkMobile API Services**: Token consumers

## Dependencies

### Required Modules
```javascript
const { updateToken } = require('@app/src/services/parkMobile');
```

### Service Dependencies
```javascript
// From parkMobile service:
const axios = require('axios');
const qs = require('qs');
const moment = require('moment');
const PmApiToken = require('@app/src/models/PmApiToken');
const { logger } = require('@maas/core/log');
```

### External Services
1. **ParkMobile Auth Server**: `https://auth.parkmobile.io`
2. **MySQL Database**: Token persistence
3. **Configuration Service**: Credential management

### Configuration Requirements
```javascript
// config/default.js or environment variables
{
  vendor: {
    pm: {
      clientId: 'YOUR_CLIENT_ID',
      clientSecret: 'YOUR_CLIENT_SECRET'
    }
  }
}
```

## Code Examples

### Manual Token Refresh
```javascript
// Force token refresh
const job = require('./update-parkmobile-token');
await job.fn();
```

### Token Retrieval for API Calls
```javascript
// Get current valid token
const getValidToken = async () => {
  const token = await PmApiToken.query()
    .where('expires', '>', moment.utc().toISOString())
    .orderBy('expires', 'desc')
    .first();
    
  if (!token) {
    await updateToken();
    return await getValidToken();
  }
  
  return token.token;
};
```

### Error Handling
```javascript
try {
  const tokenInfo = await getToken();
  await checkParams(tokenInfo, 'token'); // Validates token structure
  // Process token
} catch (err) {
  logger.error(`[park-mobile.updateToken]${err.message}`);
  logger.error(`[park-mobile.updateToken]${err.stack}`);
  throw err;
}
```

### Token Validation Schema
The service validates token responses:
```javascript
// Expected token response structure
{
  access_token: 'string',
  expires_in: 3600, // seconds
  token_type: 'Bearer',
  scope: 'api'
}
```

### HTTP Client Configuration
```javascript
const httpClient = () => {
  let options = {
    baseURL: 'https://auth.parkmobile.io',
    timeout: 10000,
  };
  
  // Proxy support for development
  if (process.env.PROJECT_STAGE === 'local') {
    const { HttpsProxyAgent } = require('https-proxy-agent');
    options.httpsAgent = new HttpsProxyAgent('http://proxy.connectsmartx.com:8888');
  }
  
  return axios.create(options);
};
```

### Best Practices

1. **Token Refresh Timing**:
   - Refresh before 80% of token lifetime
   - Account for clock skew between servers
   - Add buffer time for network delays

2. **Error Recovery**:
   - Retry logic for network failures
   - Fallback to cached tokens if available
   - Alert on repeated failures

3. **Security Considerations**:
   - Never log token values
   - Use secure configuration storage
   - Implement token rotation strategies
   - Monitor for unauthorized token usage

### Monitoring Recommendations
- Track token refresh success rate
- Monitor token expiration patterns
- Alert on authentication failures
- Log token request latency