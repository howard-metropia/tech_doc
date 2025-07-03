# AuthUserTokens Model

## Overview
Authentication token management model for the TSP Job system. Handles JWT tokens, refresh tokens, and session management for secure user authentication.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class AuthUserTokens extends Model {
  static get tableName() {
    return 'auth_user_tokens';
  }
}
module.exports = AuthUserTokens.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `auth_user_tokens`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool

## Purpose
- JWT token lifecycle management
- Refresh token handling
- Session security enforcement
- Multi-device authentication support

## Key Features
- Secure token storage
- Token expiration management
- Device-specific token tracking
- Automatic token rotation

## Token Types
- **Access Tokens**: Short-lived authentication tokens
- **Refresh Tokens**: Long-lived token renewal
- **Device Tokens**: Device-specific authentication
- **Session Tokens**: Browser session management

## Security Features
- Token encryption at rest
- Secure token generation
- Automatic expiration handling
- Revocation capabilities
- Rate limiting support

## Integration Points
- **AuthUsers**: Token ownership
- **UserConfig**: Authentication preferences
- **AuthUserLabel**: User categorization

## Usage Context
Used in authentication middleware, session management, token validation, and secure API access across the TSP platform.

## Performance Optimization
- Indexed token lookups
- Efficient expiration queries
- Cached token validation
- Minimal database overhead

## Token Lifecycle
1. Token generation on login
2. Validation on API requests
3. Automatic refresh before expiration
4. Secure revocation on logout
5. Cleanup of expired tokens

## Related Models
- AuthUsers: User authentication
- UserConfig: Auth preferences
- AuthUserLabel: User management

## API Integration
- Authentication endpoints
- Token refresh services
- Session management APIs
- Security validation middleware

## Development Notes
- Critical security component
- Requires careful token handling
- Supports multi-device scenarios
- Analytics for security monitoring