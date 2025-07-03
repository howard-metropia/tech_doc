# AuthUsers Model

## Overview
Core authentication model for user accounts in the TSP Job system. Provides foundational user authentication and account management functionality.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class AuthUsers extends Model {
  static get tableName() {
    return 'auth_user';
  }
}
module.exports = AuthUsers.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `auth_user`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool

## Purpose
- Primary user authentication entity
- Stores core user account information
- Foundation for user session management
- Links to other user-related models

## Key Features
- Simple Objection.js model structure
- Portal database connectivity
- Extensible for authentication workflows
- Thread-safe database operations

## Integration Points
- **UserWallet**: Account financial operations
- **UserConfig**: User preference management
- **AuthUserTokens**: Token-based authentication
- **Notifications**: User communication system

## Usage Context
Used in authentication flows, user management operations, and as the base model for user-related data access across the TSP job processing system.

## Database Schema
The model maps to the `auth_user` table which typically contains:
- User identification fields
- Authentication credentials
- Account status information
- Timestamps for account lifecycle

## Performance Considerations
- Indexes on authentication fields for login performance
- Connection pooling through @maas/core
- Efficient query patterns for user lookups
- Minimal model overhead for high-frequency operations

## Security Features
- Database-level security through connection management
- No sensitive data exposure in model definition
- Secure credential handling patterns
- Audit trail capabilities through timestamps

## Related Models
- AuthUserTokens: Token management
- AuthUserLabel: User categorization
- UserConfig: User preferences
- Enterprises: Multi-tenant user management
- InternalUserTag: Internal user classification

## API Integration
Primarily used by:
- Authentication services
- User management endpoints
- Session validation middleware
- Account creation workflows

## Development Notes
- Simple model structure allows for easy extension
- Follows standard TSP Job model patterns
- Compatible with existing authentication infrastructure
- Supports multi-database architecture through connection specification