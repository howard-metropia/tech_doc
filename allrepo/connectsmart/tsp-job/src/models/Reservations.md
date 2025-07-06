# Reservations Model

## Overview
Advance reservation management model for the TSP Job system. Handles pre-booked transportation services, scheduled trips, and reservation lifecycle management.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class Reservations extends Model {
  static get tableName() {
    return 'reservations';
  }
}
module.exports = Reservations.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `reservations`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool

## Purpose
- Advance trip booking management
- Scheduled transportation coordination
- Reservation lifecycle tracking
- Multi-modal reservation support

## Reservation Types
- **Transit Tickets**: Pre-purchased transit passes
- **Ridehail Scheduled**: Future ridehail bookings
- **Parking Spots**: Reserved parking spaces
- **Bike Sharing**: Advance bike reservations
- **Corporate Transport**: Business travel bookings
- **Multi-Modal**: Combined service reservations

## Key Features
- Advance booking capabilities
- Multi-provider reservation support
- Automated confirmation and reminders
- Flexible cancellation policies
- Payment processing integration

## Reservation Lifecycle
1. **Booking**: Initial reservation creation
2. **Confirmation**: Service provider confirmation
3. **Reminder**: Pre-trip notifications
4. **Activation**: Trip commencement
5. **Completion**: Service delivery
6. **Settlement**: Payment and billing

## Integration Points
- **Trips**: Trip execution from reservations
- **ReservationPolyline**: Route visualization
- **PimaReservations**: PIMA-specific bookings
- **DuoReservations**: Duo service reservations

## Business Logic
- Availability checking
- Pricing and fare calculation
- Cancellation policy enforcement
- Conflict resolution
- Payment authorization

## Performance Features
- Efficient booking lookups
- Real-time availability checks
- Scalable reservation processing
- Optimized for booking workflows

## Quality Assurance
- Booking validation
- Duplicate prevention
- Service availability verification
- User notification reliability

## Related Models
- Trips: Executed reservations
- ReservationPolyline: Route planning
- PimaReservations: Specialized reservations
- DuoReservations: Duo service bookings

## API Integration
- Booking management endpoints
- Availability checking services
- Payment processing APIs
- Notification delivery systems

## User Experience
- Seamless booking workflows
- Real-time confirmation
- Proactive communication
- Easy modification and cancellation

## Development Notes
- Complex booking logic
- Multi-provider integration
- Time-sensitive operations
- Critical for user satisfaction