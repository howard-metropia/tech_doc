# PimaTrips Model

## Overview
PIMA (Pima County) specific trip model for the TSP Job system. Handles regional transportation data, local transit integration, and county-specific trip management.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class PimaTrips extends Model {
  static get tableName() {
    return 'pima_trips';
  }
}
module.exports = PimaTrips.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `pima_trips`
- **ORM**: Objection.js with Knex query builder

## Purpose
- Pima County trip management
- Regional transportation tracking
- Local transit integration
- County-specific analytics

## Regional Features
- **Local Transit**: Pima County transit systems
- **Regional Routes**: County-wide transportation
- **Multi-Modal**: Combined local services
- **Specialized Services**: County-specific offerings

## Key Features
- County-specific trip tracking
- Local transit integration
- Regional service coordination
- Government partnership support

## Service Types
- **Public Transit**: County bus services
- **Paratransit**: Specialized transportation
- **Regional Connections**: Inter-county travel
- **Government Services**: Official transportation

## Integration Points
- **Trips**: General trip system
- **PimaReservations**: County reservations
- **PimaUsers**: Regional user management
- **TransitAlert**: Local service alerts

## County-Specific Data
- Local route information
- Regional service schedules
- County fare structures
- Government reporting requirements

## Compliance Features
- Government reporting standards
- Accessibility compliance
- Public service requirements
- Data privacy regulations

## Analytics Applications
- Regional transportation planning
- Public service optimization
- County mobility metrics
- Government performance reporting

## Related Models
- Trips: General trip system
- PimaReservations: County bookings
- PimaUsers: Regional users
- TransitAlert: Service notifications

## Development Notes
- Government partnership requirements
- Regional service focus
- Compliance-driven design
- Public service optimization