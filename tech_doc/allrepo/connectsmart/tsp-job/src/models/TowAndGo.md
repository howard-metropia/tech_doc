# TowAndGo Model

## Overview
Tow and emergency vehicle service management model for the TSP Job system. Handles emergency transportation services, vehicle assistance, and roadside support coordination.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class TowAndGo extends Model {
  static get tableName() {
    return 'tow_and_go';
  }
}
module.exports = TowAndGo.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `tow_and_go`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool

## Purpose
- Emergency vehicle assistance
- Roadside support coordination
- Towing service management
- Alternative transportation provision

## Service Types
- **Vehicle Towing**: Disabled vehicle removal
- **Roadside Assistance**: On-site repairs and support
- **Emergency Transportation**: Alternative mobility solutions
- **Jump Start Services**: Battery assistance
- **Tire Replacement**: Flat tire support
- **Fuel Delivery**: Emergency fuel services

## Key Features
- Emergency response coordination
- Real-time service dispatch
- Alternative transportation booking
- Service provider network management

## Integration Points
- **TowAndGoModel**: Service model definitions
- **HntbTowAndGo**: HNTB-specific implementations
- **Trips**: Alternative transportation trips
- **Notifications**: Emergency communication

## Usage Context
Used for emergency situations, vehicle breakdowns, roadside assistance, and ensuring mobility continuity during vehicle issues.

## Emergency Response
- Rapid service dispatch
- Location-based provider matching
- Real-time status updates
- Alternative transportation coordination

## Service Workflow
1. **Emergency Request**: User initiates assistance request
2. **Location Verification**: GPS and address confirmation
3. **Service Dispatch**: Provider assignment and dispatch
4. **Service Delivery**: On-site assistance provision
5. **Alternative Transport**: Backup mobility if needed
6. **Completion**: Service completion and billing

## Provider Network
- Towing companies
- Roadside assistance services
- Emergency mechanics
- Alternative transportation providers

## Quality Assurance
- Response time monitoring
- Service quality tracking
- User satisfaction measurement
- Provider performance evaluation

## Related Models
- TowAndGoModel: Service definitions
- HntbTowAndGo: Specialized services
- Trips: Emergency transportation
- Notifications: Emergency alerts

## API Integration
- Emergency request endpoints
- Service dispatch APIs
- Real-time tracking services
- Provider network management

## Business Logic
- Emergency priority handling
- Cost calculation and billing
- Insurance coordination
- Service availability management

## Development Notes
- Critical emergency service
- Real-time response requirements
- High reliability needs
- Integration with emergency services