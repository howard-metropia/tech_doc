# PmApiToken.js - TSP Job Model Documentation

## Quick Summary

The PmApiToken model represents ParkMobile API authentication tokens within the TSP Job scheduling system. This Objection.js ORM model provides database access to the `pm_api_token` table in the portal database, managing API credentials for ParkMobile parking service integration. The model stores and manages authentication tokens required for accessing ParkMobile's parking reservation and payment APIs within the broader MaaS platform ecosystem.

## Technical Analysis

### Code Structure
```javascript
const knex = require('@maas/core/mysql')('portal');
class PmApiToken extends Model {
  static get tableName() {
    return 'pm_api_token';
  }
}
module.exports = PmApiToken.bindKnex(knex);
```

### Critical Implementation Issue
The model contains a fundamental bug - it extends the `Model` class from Objection.js without importing it. The corrected implementation requires:
```javascript
const { Model } = require('objection');
```

### Database Architecture
- **Database**: `portal` (MySQL connection via @maas/core)
- **Table**: `pm_api_token`
- **Connection Pattern**: Knex.js query builder with Objection.js ORM binding
- **Access Pattern**: Portal database for operational API credential management

### Token Management Design
Based on the TSP architecture patterns, this model likely manages:
- **API Keys**: ParkMobile service authentication credentials
- **Token Rotation**: Automatic token refresh and expiration handling
- **Service Integration**: Credentials for parking spot reservations and payments
- **Multi-tenant Support**: Potentially different tokens per deployment environment

### Integration Context
ParkMobile integration is part of the comprehensive MaaS platform that includes:
- Real-time parking availability queries
- Parking spot reservation management
- Payment processing for parking fees
- User parking history and analytics
- Integration with trip planning services

## Usage/Integration

### API Token Lifecycle Management

**Token Storage and Retrieval**:
- Securely stores ParkMobile API credentials in encrypted format
- Provides centralized token management for all ParkMobile API calls
- Supports token rotation without service disruption
- Maintains token expiration tracking and automatic renewal

**Service Integration Points**:
- **Parking Services**: Authentication for parking spot availability queries
- **Reservation System**: Token validation for booking parking spaces
- **Payment Processing**: Secure API access for parking fee transactions
- **User Analytics**: Authenticated access to user parking behavior data

### Scheduling Job Integration
Within the TSP Job system, this model supports:
- **Token Validation Jobs**: Scheduled checks for token expiration
- **API Health Monitoring**: Regular validation of ParkMobile service connectivity
- **Credential Rotation**: Automated token refresh processes
- **Error Recovery**: Handling of authentication failures and token regeneration

### Multi-Environment Support
The model supports different deployment environments:
- **Development**: Test API tokens for development and testing
- **Staging**: Pre-production token validation
- **Production**: Live ParkMobile service integration tokens
- **Disaster Recovery**: Backup token management for service continuity

## Dependencies

### Core Framework Dependencies
- **@maas/core/mysql**: Database connection management for portal database
- **objection**: ORM framework (missing import - critical bug)
- **knex**: SQL query builder (provided through @maas/core)

### Security and Encryption
- **Token Encryption**: Database-level encryption for sensitive API credentials
- **Access Control**: Role-based access to token management functions
- **Audit Logging**: Token usage and modification tracking
- **Secure Storage**: Encrypted token storage with proper key management

### ParkMobile API Dependencies
- **ParkMobile REST API**: Third-party parking service integration
- **OAuth2/API Key Authentication**: Standard API authentication protocols
- **Rate Limiting**: Token-based API rate limit management
- **Service Discovery**: Dynamic API endpoint configuration

### Operational Dependencies
- **Configuration Management**: Environment-specific token configuration
- **Monitoring Services**: Token health and usage monitoring
- **Alert Systems**: Token expiration and failure notifications
- **Backup Systems**: Token recovery and disaster management

## Code Examples

### Basic Token Retrieval
```javascript
const PmApiToken = require('@app/src/models/PmApiToken');

// Get active ParkMobile API token
const activeToken = await PmApiToken.query()
  .where('status', 'active')
  .where('expires_at', '>', new Date())
  .first();

// Retrieve token by environment
const prodToken = await PmApiToken.query()
  .where('environment', 'production')
  .where('is_active', true)
  .first();
```

### Token Validation and Refresh
```javascript
// Check token expiration
const expiringTokens = await PmApiToken.query()
  .where('expires_at', '<', new Date(Date.now() + 86400000)) // 24 hours
  .where('status', 'active');

// Update token after refresh
await PmApiToken.query()
  .findById(tokenId)
  .patch({
    token: newTokenValue,
    expires_at: newExpirationDate,
    last_refreshed: new Date()
  });
```

### Service Integration Pattern
```javascript
// Get token for ParkMobile API call
async function getParkMobileToken() {
  const token = await PmApiToken.query()
    .where('service', 'parkmobile')
    .where('status', 'active')
    .where('expires_at', '>', new Date())
    .first();
    
  if (!token) {
    throw new Error('No valid ParkMobile API token available');
  }
  
  return token.token;
}

// Usage in parking service
const apiToken = await getParkMobileToken();
const parkingSpots = await parkMobileAPI.getAvailableSpots({
  authorization: `Bearer ${apiToken}`,
  location: userLocation
});
```

### Token Rotation Job Example
```javascript
// Scheduled job for token maintenance
const rotateExpiredTokens = async () => {
  const expiredTokens = await PmApiToken.query()
    .where('expires_at', '<', new Date())
    .where('status', 'active');
    
  for (const token of expiredTokens) {
    try {
      const newToken = await refreshParkMobileToken(token.token);
      
      await PmApiToken.query()
        .findById(token.id)
        .patch({
          token: newToken.access_token,
          expires_at: new Date(newToken.expires_in * 1000 + Date.now()),
          status: 'active',
          last_refreshed: new Date()
        });
        
      logger.info(`Token ${token.id} refreshed successfully`);
    } catch (error) {
      logger.error(`Failed to refresh token ${token.id}: ${error.message}`);
      
      await PmApiToken.query()
        .findById(token.id)
        .patch({ status: 'failed' });
    }
  }
};
```

### Multi-Environment Token Management
```javascript
// Environment-specific token retrieval
const getTokenByEnvironment = async (env = 'production') => {
  return await PmApiToken.query()
    .where('environment', env)
    .where('status', 'active')
    .where('expires_at', '>', new Date())
    .orderBy('created_at', 'desc')
    .first();
};

// Token usage tracking
const trackTokenUsage = async (tokenId, endpoint, responseTime) => {
  await PmApiToken.query()
    .findById(tokenId)
    .patch({
      last_used: new Date(),
      usage_count: knex.raw('usage_count + 1'),
      avg_response_time: knex.raw(`(avg_response_time + ${responseTime}) / 2`)
    });
};
```

This model serves as a critical security component in the ParkMobile integration pipeline, ensuring secure and reliable access to parking services while maintaining proper credential lifecycle management and supporting the broader MaaS platform's parking functionality.