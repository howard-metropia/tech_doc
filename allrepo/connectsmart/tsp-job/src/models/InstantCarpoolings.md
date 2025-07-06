# InstantCarpoolings Model

## Overview
Instant carpool matching and management model for the TSP Job system. Handles real-time carpooling requests, driver-passenger matching, and shared ride coordination.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class InstantCarpoolings extends Model {
  static get tableName() {
    return 'instant_carpoolings';
  }
}
module.exports = InstantCarpoolings.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `instant_carpoolings`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool

## Purpose
- Real-time carpool matching
- Instant ride sharing coordination
- Dynamic passenger-driver pairing
- Shared mobility optimization

## Key Features
- Real-time matching algorithms
- Dynamic route optimization
- Instant booking confirmation
- Flexible pickup/dropoff points

## Carpool Types
- **Commuter Carpools**: Regular work-related rides
- **Event Carpools**: Special occasion sharing
- **Airport Rides**: Shared airport transportation
- **Shopping Trips**: Retail destination sharing
- **Social Carpools**: Leisure and entertainment rides

## Matching Criteria
- **Route Compatibility**: Origin/destination alignment
- **Time Windows**: Departure/arrival flexibility
- **Preferences**: User compatibility factors
- **Vehicle Capacity**: Available seat management
- **Cost Sharing**: Fare splitting arrangements

## Integration Points
- **Trips**: Carpool trip execution
- **AuthUsers**: Driver and passenger management
- **UserRatings**: Carpool experience feedback
- **CoinTransaction**: Cost sharing transactions

## Usage Context
Used for sustainable transportation options, cost-effective travel, social mobility, and reduced traffic congestion.

## Matching Algorithm
- Geographic proximity analysis
- Time window compatibility
- User preference filtering
- Dynamic route optimization
- Real-time availability updates

## Business Logic
- Fair cost splitting calculations
- Safety and security verification
- Cancellation policy enforcement
- Quality assurance monitoring

## Performance Features
- Fast matching algorithms
- Real-time updates
- Scalable for high demand
- Efficient route calculations

## Safety Features
- User verification requirements
- Rating and feedback systems
- Emergency contact protocols
- Trip tracking and monitoring

## Related Models
- Trips: Executed carpools
- AuthUsers: Participant management
- UserRatings: Experience feedback
- Reservations: Advance carpool booking

## API Integration
- Real-time matching endpoints
- Carpool management APIs
- Route optimization services
- Safety and tracking features

## Environmental Impact
- Reduced vehicle usage
- Lower emissions per trip
- Traffic congestion reduction
- Sustainable transportation promotion

## Development Notes
- Complex matching algorithms
- Real-time processing critical
- Safety-first design approach
- Scalable for urban environments