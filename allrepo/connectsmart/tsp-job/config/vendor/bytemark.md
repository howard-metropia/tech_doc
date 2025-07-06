# Bytemark Configuration

## Overview
**File**: `config/vendor/bytemark.js`  
**Type**: Vendor Configuration  
**Purpose**: Provides environment-specific configuration for Bytemark transit API integration

## Configuration Structure

### Environment Detection
```javascript
const isProduction = process.env.BYTEMARK_PRODUCTION === 'true';
```

### URL Configuration
```javascript
url: defer(() => {
  return isProduction
    ? {
        merchantApi: 'https://merchant-api.bytemark.co',
        accountApi: 'https://accountapi.bytemark.co',
        customerApi: 'https://overture.bytemark.co',
        account: 'https://account.bytemark.co',
      }
    : {
        merchantApi: 'https://merchant-api-uat.bytemark.co',
        accountApi: 'https://accountapi-uat.bytemark.co',
        customerApi: 'https://overture-uat.bytemark.co',
        account: 'https://account-uat.bytemark.co',
      };
})
```

## API Endpoints

### Production URLs
- **merchantApi**: `https://merchant-api.bytemark.co`
- **accountApi**: `https://accountapi.bytemark.co`
- **customerApi**: `https://overture.bytemark.co`
- **account**: `https://account.bytemark.co`

### UAT/Development URLs
- **merchantApi**: `https://merchant-api-uat.bytemark.co`
- **accountApi**: `https://accountapi-uat.bytemark.co`
- **customerApi**: `https://overture-uat.bytemark.co`
- **account**: `https://account-uat.bytemark.co`

## Configuration Properties

### Environment Variables
- **BYTEMARK_PRODUCTION**: Boolean flag for production environment
- **BYTEMARK_CLIENT_ID**: OAuth client identifier
- **BYTEMARK_CLIENT_SECRET**: OAuth client secret
- **BYTEMARK_MAIL_PREFIX**: Email prefix for Bytemark communications

### Static Configuration
- **inboxAddress**: `'info@metropia.com'` (support email)

## API Components

### Merchant API
- **Purpose**: Merchant-facing operations
- **Functions**: Transaction management, merchant settings
- **Environment**: Separate production and UAT endpoints

### Account API
- **Purpose**: Account management operations
- **Functions**: User account creation, authentication
- **Environment**: Separate production and UAT endpoints

### Customer API (Overture)
- **Purpose**: Customer-facing operations
- **Functions**: Trip planning, ticket purchasing
- **Environment**: Separate production and UAT endpoints

### Account Portal
- **Purpose**: Web-based account management
- **Functions**: User interface for account operations
- **Environment**: Separate production and UAT endpoints

## Authentication

### OAuth Configuration
```javascript
{
  clientId: process.env.BYTEMARK_CLIENT_ID,
  clinetSecret: process.env.BYTEMARK_CLIENT_SECRET, // Note: typo in original
}
```

### Client Credentials
- **Client ID**: OAuth application identifier
- **Client Secret**: OAuth application secret
- **Grant Type**: Client credentials flow

## Usage Examples

### Environment Setup
```javascript
// Production
process.env.BYTEMARK_PRODUCTION = 'true';
process.env.BYTEMARK_CLIENT_ID = 'prod-client-id';
process.env.BYTEMARK_CLIENT_SECRET = 'prod-secret';

// Development
process.env.BYTEMARK_PRODUCTION = 'false';
process.env.BYTEMARK_CLIENT_ID = 'dev-client-id';
process.env.BYTEMARK_CLIENT_SECRET = 'dev-secret';
```

### Configuration Access
```javascript
const bytemarkConfig = require('./config/vendor/bytemark');

// Check environment
if (bytemarkConfig.isProduction) {
  console.log('Using production Bytemark APIs');
}

// Get API URLs
const apiUrl = bytemarkConfig.url.merchantApi;
const authParams = {
  client_id: bytemarkConfig.clientId,
  client_secret: bytemarkConfig.clinetSecret
};
```

### API Client Initialization
```javascript
const config = require('./config/vendor/bytemark');

const bytemarkClient = new BytemarkAPI({
  baseURL: config.url.merchantApi,
  clientId: config.clientId,
  clientSecret: config.clinetSecret,
  production: config.isProduction
});
```

## Dependencies

### Config Utilities
- **defer**: `require('config/defer').deferConfig`
- **Purpose**: Deferred configuration evaluation
- **Benefit**: Environment-dependent URL selection

### Environment Variables
- All configuration values sourced from environment variables
- No hardcoded secrets or URLs
- Environment-specific behavior

## Environment Management

### Production Environment
- **BYTEMARK_PRODUCTION**: `'true'`
- **URLs**: Production Bytemark endpoints
- **Credentials**: Production OAuth credentials

### Development/UAT Environment
- **BYTEMARK_PRODUCTION**: `'false'` or undefined
- **URLs**: UAT Bytemark endpoints
- **Credentials**: Development OAuth credentials

## Security Considerations

### Credential Management
- **Environment Variables**: Secure storage of credentials
- **No Hardcoding**: No secrets in code
- **Separation**: Different credentials per environment

### API Security
- **OAuth 2.0**: Standard authentication protocol
- **HTTPS**: All endpoints use secure connections
- **Client Credentials**: Appropriate for server-to-server communication

## Integration Points

### Bytemark APIs
- **Merchant Operations**: Payment processing, transaction management
- **Account Management**: User registration, profile management
- **Customer Services**: Trip booking, ticket purchasing
- **Portal Access**: Web-based user interface

### Internal Services
- **Payment Processing**: Transit payment integration
- **User Management**: Account synchronization
- **Trip Planning**: Route and fare calculation
- **Analytics**: Transaction and usage reporting

## Configuration Validation

### Required Variables
```bash
BYTEMARK_PRODUCTION=true
BYTEMARK_CLIENT_ID=your-client-id
BYTEMARK_CLIENT_SECRET=your-client-secret
BYTEMARK_MAIL_PREFIX=prefix-
```

### Validation Checks
- **Client ID**: Must be provided
- **Client Secret**: Must be provided
- **Production Flag**: Boolean validation
- **URL Generation**: Proper URL formation

## Error Handling

### Missing Configuration
- **Missing Variables**: May cause undefined behavior
- **Invalid Production Flag**: Defaults to development
- **Missing Credentials**: API calls will fail

### Configuration Issues
```javascript
if (!config.clientId || !config.clinetSecret) {
  throw new Error('Bytemark credentials not configured');
}
```

## Testing Configuration

### Test Environment
```javascript
// Test configuration
process.env.BYTEMARK_PRODUCTION = 'false';
process.env.BYTEMARK_CLIENT_ID = 'test-client';
process.env.BYTEMARK_CLIENT_SECRET = 'test-secret';
```

### Mock Configuration
```javascript
const mockConfig = {
  isProduction: false,
  url: {
    merchantApi: 'http://localhost:3001',
    accountApi: 'http://localhost:3002',
    customerApi: 'http://localhost:3003',
    account: 'http://localhost:3004'
  },
  clientId: 'mock-client',
  clinetSecret: 'mock-secret'
};
```

## Monitoring

### Configuration Logging
- **Environment Detection**: Log production vs development
- **URL Resolution**: Log resolved API endpoints
- **Credential Validation**: Log credential availability

### Health Checks
- **API Connectivity**: Verify endpoint accessibility
- **Authentication**: Test credential validity
- **Environment Consistency**: Verify configuration alignment

## Best Practices

### Environment Management
- **Clear Separation**: Distinct production and development configs
- **Secure Storage**: Environment variables for sensitive data
- **Validation**: Verify required configuration is present

### API Integration
- **Error Handling**: Graceful handling of API failures
- **Retry Logic**: Implement appropriate retry strategies
- **Rate Limiting**: Respect API rate limits

## Note on Typo

### Configuration Property
```javascript
clinetSecret: process.env.BYTEMARK_CLIENT_SECRET, // Typo: should be "clientSecret"
```

### Impact
- **Property Name**: Inconsistent with standard naming
- **Functionality**: Works but may cause confusion
- **Recommendation**: Consider fixing in future updates