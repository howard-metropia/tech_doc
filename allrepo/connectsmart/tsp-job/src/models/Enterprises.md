# Enterprises Model

## Overview
Enterprise account management model for the TSP Job system. Handles corporate accounts, multi-tenant organizations, and business entity management.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class Enterprises extends Model {
  static get tableName() {
    return 'enterprise';
  }
}
module.exports = Enterprises.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `enterprise`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool

## Purpose
- Corporate account management
- Multi-tenant organization handling
- Business entity administration
- Enterprise-level feature control

## Key Features
- Multi-tenant architecture support
- Corporate account hierarchy
- Enterprise-specific configurations
- Business relationship management

## Enterprise Types
- **Corporate Clients**: Large business accounts
- **Government Agencies**: Public sector organizations
- **Educational Institutions**: Schools and universities
- **Healthcare Systems**: Medical organizations
- **Transit Authorities**: Public transportation agencies

## Integration Points
- **AuthUsers**: Enterprise user management
- **InternalUserTag**: Enterprise user classification
- **UserConfig**: Enterprise-specific settings
- **TeleworkLogs**: Enterprise telework tracking

## Usage Context
Used for managing corporate accounts, multi-tenant configurations, enterprise billing, and business-level features.

## Database Schema
Typical enterprise fields:
- Organization identification
- Contact and billing information
- Service level agreements
- Feature access controls
- Subscription and billing data

## Multi-Tenancy Support
- Tenant isolation
- Resource allocation
- Custom branding
- Enterprise-specific features
- Data segregation

## Business Logic
- Account hierarchy management
- Billing and subscription handling
- Feature access control
- Compliance requirements
- Service level management

## Performance Considerations
- Tenant-aware query optimization
- Efficient enterprise lookups
- Scaled for multiple organizations
- Resource isolation

## Related Models
- AuthUsers: Enterprise users
- InternalUserTag: User classification
- UserConfig: Enterprise settings
- TeleworkLogs: Enterprise tracking

## API Integration
- Enterprise management endpoints
- Multi-tenant configuration APIs
- Billing and subscription services
- Corporate reporting

## Security Features
- Tenant data isolation
- Enterprise access controls
- Compliance monitoring
- Audit trail maintenance

## Development Notes
- Critical for B2B operations
- Supports complex organizational structures
- Scalable multi-tenant design
- Enterprise-grade security requirements