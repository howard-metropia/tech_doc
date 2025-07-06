# DuoReservations Model

## Overview
Database model for Duo carpool reservation management in the TSP Job system. Handles carpool reservation data, matching processes, and reservation lifecycle management for the Duo carpooling service.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class DuoReservations extends Model {
  static get tableName() {
    return 'duo_reservation';
  }
}
module.exports = DuoReservations.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `duo_reservation`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool

## Purpose
- Duo carpool reservation management
- Carpool matching and pairing
- Reservation lifecycle tracking
- Carpool validation processing
- User coordination for shared rides

## Key Features
- Complete reservation lifecycle management
- Real-time matching capabilities
- Reservation status tracking
- User pairing and coordination
- Validation and verification support

## Technical Implementation
The model manages the complete Duo carpool reservation process, from initial reservation creation through matching, confirmation, and trip completion. It integrates with the carpool validation system and user management services.

### Database Schema
The `duo_reservation` table contains:
- Reservation identification and metadata
- User information for driver and passenger
- Trip origin and destination details
- Reservation timing and scheduling
- Matching status and pairing information
- Validation results and verification data
- Payment and incentive calculation fields
- Reservation lifecycle timestamps

### Reservation Operations
```javascript
// Create new Duo reservation
const reservation = await DuoReservations.query().insert({
  user_id: userId,
  origin_lat: originLat,
  origin_lng: originLng,
  dest_lat: destLat,
  dest_lng: destLng,
  departure_time: departureTime,
  reservation_type: 'driver', // or 'passenger'
  status: 'pending'
});

// Find matching reservations
const matches = await DuoReservations.query()
  .where('status', 'pending')
  .andWhere('reservation_type', '!=', userType)
  .andWhere('departure_time', '>=', timeWindow.start)
  .andWhere('departure_time', '<=', timeWindow.end)
  .andWhereRaw('ST_Distance_Sphere(POINT(origin_lng, origin_lat), POINT(?, ?)) <= ?', 
    [userOriginLng, userOriginLat, maxDistance]);

// Update reservation status
await DuoReservations.query()
  .findById(reservationId)
  .patch({
    status: 'matched',
    matched_with: matchedReservationId,
    matched_at: new Date()
  });
```

## Reservation Lifecycle
### Status Flow
1. **Pending**: Initial reservation state
2. **Matching**: System searching for compatible pairs
3. **Matched**: Successfully paired with another user
4. **Confirmed**: Both users confirmed the carpool
5. **Active**: Trip in progress
6. **Completed**: Trip successfully finished
7. **Cancelled**: Reservation cancelled by user or system
8. **Failed**: Matching or validation failed

### Matching Algorithm
- Geographic proximity matching
- Time window compatibility
- User preference alignment
- Historical performance scoring
- Real-time availability verification

## Integration Points
- **Carpool Validation**: Trip verification and validation
- **User Management**: Driver and passenger coordination
- **Payment System**: Cost sharing and incentive distribution
- **Notification Service**: Real-time user communication
- **Trip Processing**: Integration with trip lifecycle management

## Carpool Types
- **Driver Reservations**: Users offering rides
- **Passenger Reservations**: Users seeking rides
- **Flexible Reservations**: Users open to either role
- **Corporate Reservations**: Enterprise carpool programs
- **Event-based Reservations**: Special event transportation

## Usage Context
Essential for:
- Carpool matching and pairing
- Reservation management workflows
- Trip validation processes
- User coordination and communication
- Incentive program calculations
- Performance analytics and reporting

## Performance Considerations
- Efficient geographic indexing for proximity matching
- Real-time matching algorithm optimization
- Connection pooling for high concurrency
- Caching for frequently accessed reservation data
- Batch processing for reservation analytics

## Validation Integration
Works closely with:
- **DuoValidatedResult**: Validation outcome tracking
- **Trip Validation Services**: Real-time trip verification
- **GPS Tracking**: Location validation during trips
- **Payment Validation**: Cost sharing verification

## Security Features
- User privacy protection for location data
- Secure reservation data handling
- Access control for reservation modifications
- Audit logging for reservation lifecycle events
- Data encryption for sensitive information

## Related Models
- DuoValidatedResult: Validation results tracking
- AuthUsers: User account information
- Trips: Trip execution records
- Reservations: General reservation system
- UserWallet: Payment and incentive processing

## API Integration
Core for:
- Carpool reservation endpoints
- Matching service APIs
- Real-time status updates
- User notification systems
- Analytics and reporting services

## Business Logic Support
- Dynamic matching algorithms
- Cost sharing calculations
- Incentive distribution logic
- Quality scoring systems
- Performance optimization metrics

## Development Notes
- Optimized for real-time matching operations
- Supports complex geographic queries
- Designed for high-availability operations
- Compatible with mobile application requirements
- Follows microservices architecture patterns

## Monitoring and Analytics
- Reservation success rate tracking
- Matching efficiency metrics
- User satisfaction scoring
- Geographic usage patterns
- Temporal demand analysis

## Data Quality Management
- Reservation data validation and verification
- Duplicate reservation detection
- Location accuracy verification
- Time window consistency checks
- User eligibility validation

## Scalability Considerations
- Horizontal scaling support for high-demand periods
- Efficient indexing for large reservation datasets
- Caching strategies for improved performance
- Load balancing for reservation processing
- Real-time synchronization across service instances