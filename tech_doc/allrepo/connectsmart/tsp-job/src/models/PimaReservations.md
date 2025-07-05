# PimaReservations Model

## Overview
PIMA County reservation management model for the TSP Job system. Handles county-specific booking services, paratransit reservations, and regional transportation scheduling.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class PimaReservations extends Model {
  static get tableName() {
    return 'pima_reservations';
  }
}
module.exports = PimaReservations.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `pima_reservations`
- **ORM**: Objection.js with Knex query builder

## Purpose
- County reservation management
- Paratransit booking coordination
- Regional service scheduling
- Government service reservations

## Reservation Types
- **Paratransit**: Specialized accessibility services
- **Medical Transport**: Healthcare appointments
- **Government Services**: Official transportation
- **Regional Routes**: Inter-county connections

## Key Features
- ADA compliance support
- Specialized service booking
- Government integration
- Accessibility-focused design

## Service Categories
- **Door-to-Door**: Full service transport
- **Curb-to-Curb**: Standard pickup service
- **Shared Rides**: Cost-effective options
- **Priority Services**: Medical/emergency transport

## Integration Points
- **PimaTrips**: County trip execution
- **PimaUsers**: Regional user management
- **Reservations**: General reservation system
- **Enterprises**: Government partnerships

## Compliance Features
- ADA accessibility requirements
- Government service standards
- Privacy regulation adherence
- Public service compliance

## Scheduling Features
- Advance booking support
- Recurring reservation management
- Flexible scheduling options
- Priority booking for medical needs

## Quality Assurance
- Service reliability monitoring
- Accessibility compliance verification
- User satisfaction tracking
- Performance metrics reporting

## Related Models
- PimaTrips: County transportation
- PimaUsers: Regional users
- Reservations: General bookings
- Enterprises: Government accounts

## Development Notes
- Government compliance critical
- Accessibility requirements paramount
- Public service optimization
- Regional coordination essential