# TransitAlertRoute Model

## Overview
Transit alert route association model for the TSP Job system. Manages relationships between transit alerts and affected routes for targeted alert delivery.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('gtfs');
class TransitAlertRoute extends Model {
  static get tableName() {
    return 'ridemetro_transit_alert_join_route';
  }
}
module.exports = TransitAlertRoute.bindKnex(knex);
```

## Database Configuration
- **Database**: GTFS MySQL instance
- **Table**: `ridemetro_transit_alert_join_route`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool

## Purpose
- Alert-route relationship management
- Targeted alert delivery
- Route-specific impact tracking
- Service disruption mapping

## Key Features
- Many-to-many relationship support
- Route-specific targeting
- Impact scope definition
- Alert distribution optimization

## Relationship Types
- **Direct Impact**: Routes directly affected
- **Secondary Impact**: Connected service effects
- **Alternative Routes**: Suggested alternatives
- **Service Modifications**: Route changes

## Integration Points
- **TransitAlert**: Parent alert entity
- **GTFS Routes**: Transit route data
- **Trips**: Trip impact analysis
- **Notifications**: Targeted messaging

## Usage Context
Used for precise alert targeting, route-specific notifications, service impact assessment, and alternative route suggestions.

## Alert Targeting
- Route-specific user filtering
- Geographic impact mapping
- Service level targeting
- Time-based relevance

## Performance Features
- Efficient route lookups
- Fast alert distribution
- Optimized relationship queries
- Scalable for transit networks

## Related Models
- TransitAlert: Alert information
- Trips: Trip impact assessment
- Notifications: Alert delivery
- TripDetail: Route analysis

## API Integration
- Route-specific alert endpoints
- Targeted notification services
- Impact assessment APIs
- Alternative route suggestions

## Development Notes
- Critical for transit operations
- Real-time processing needs
- Multi-route alert support
- User experience optimization