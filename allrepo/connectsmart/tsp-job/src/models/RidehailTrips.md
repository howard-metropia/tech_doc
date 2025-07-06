# RidehailTrips Model

## Overview
Ridehail-specific trip management model for the TSP Job system. Handles Uber, Lyft, and other ridehail service trips with provider-specific data.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class RidehailTrips extends Model {
  static get tableName() {
    return 'ridehail_trip';
  }
}
module.exports = RidehailTrips.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `ridehail_trip`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool

## Purpose
- Ridehail-specific trip tracking
- Provider integration management
- Fare and payment processing
- Service quality monitoring

## Supported Providers
- **Uber**: UberX, UberPool, UberBlack
- **Lyft**: Lyft, Lyft Shared, Lyft Lux
- **Local Services**: Regional ridehail providers
- **Corporate Services**: Enterprise transportation

## Key Features
- Provider-specific trip data
- Real-time ride tracking
- Fare calculation and billing
- Driver and vehicle information
- Service quality metrics

## Integration Points
- **Trips**: Parent trip relationship
- **UberFareEstimation**: Fare prediction
- **UberBenefitTransaction**: Benefit tracking
- **UberApiPayload**: API interaction logs

## Trip Lifecycle
1. **Request**: Ride booking and confirmation
2. **Matching**: Driver assignment
3. **Pickup**: Driver arrival and passenger pickup
4. **Transit**: Active ride tracking
5. **Dropoff**: Trip completion
6. **Payment**: Fare processing and payment

## Data Categories
- **Booking Data**: Request details, preferences
- **Driver Data**: Driver info, vehicle details
- **Route Data**: Actual path taken
- **Fare Data**: Cost breakdown, surge pricing
- **Quality Data**: Ratings, feedback, issues

## Performance Features
- Real-time trip status updates
- Efficient provider API integration
- Scalable for high-volume operations
- Optimized fare calculations

## Related Models
- Trips: Base trip entity
- UberFareEstimation: Fare predictions
- UberBenefitTransaction: Benefits
- Reservations: Advance bookings

## API Integration
- Provider API connections
- Real-time tracking endpoints
- Fare calculation services
- Trip management APIs

## Business Logic
- Surge pricing calculations
- Driver-passenger matching
- Route optimization
- Payment processing
- Quality assurance

## Development Notes
- Provider-specific implementations
- Real-time data synchronization
- High-frequency operations
- Critical for user experience