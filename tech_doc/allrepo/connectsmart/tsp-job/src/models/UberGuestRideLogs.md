# UberGuestRideLogs Model

## Overview
MySQL-based model for logging Uber guest ride operations and transactions. This model provides comprehensive audit trail capabilities for tracking guest user interactions with Uber ridehail services, supporting both operational monitoring and business analytics within the TSP system.

## File Location
`/src/models/UberGuestRideLogs.js`

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class UberGuestRideLogs extends Model {
  static get tableName() {
    return 'uber_guest_ride_log';
  }
}

module.exports = UberGuestRideLogs.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance  
- **Table**: `uber_guest_ride_log`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool
- **Model Framework**: Extends global Model class (Objection.js)

## Purpose and Functionality
- **Guest Ride Tracking**: Monitor ridehail requests from non-authenticated users
- **Service Integration Logging**: Record interactions with Uber's API services
- **Business Analytics**: Collect data on guest user behavior and service utilization
- **Operational Monitoring**: Track service performance and availability for guest users

## Key Features
- **MySQL Reliability**: Leverages robust relational database for transactional integrity
- **Objection.js ORM**: Full-featured ORM with query building capabilities
- **Connection Pooling**: Efficient database connection management
- **Guest User Focus**: Specifically designed for non-authenticated user tracking

## Database Schema Structure
While the model doesn't explicitly define the schema in code, the `uber_guest_ride_log` table typically includes:

```sql
-- Typical table structure (implementation-dependent)
CREATE TABLE uber_guest_ride_log (
  id INT PRIMARY KEY AUTO_INCREMENT,
  guest_session_id VARCHAR(255),     -- Guest user session identifier
  request_timestamp DATETIME,        -- When ride was requested
  pickup_latitude DECIMAL(10,8),     -- Pickup location coordinates
  pickup_longitude DECIMAL(11,8),
  destination_latitude DECIMAL(10,8), -- Destination coordinates  
  destination_longitude DECIMAL(11,8),
  ride_type VARCHAR(50),             -- UberX, UberPool, etc.
  estimated_fare DECIMAL(10,2),     -- Estimated cost
  actual_fare DECIMAL(10,2),        -- Final charged amount
  ride_status VARCHAR(50),           -- requested, confirmed, completed, cancelled
  driver_id VARCHAR(255),            -- Uber driver identifier
  vehicle_info JSON,                 -- Vehicle details
  trip_duration INT,                 -- Duration in seconds
  trip_distance DECIMAL(8,2),       -- Distance in miles/km
  payment_method VARCHAR(50),        -- Payment type used
  cancellation_reason VARCHAR(255),  -- If cancelled, reason
  rating_given INT,                  -- Guest rating (1-5)
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## Usage Patterns

### Basic CRUD Operations
```javascript
// Create new guest ride log entry
const rideLog = await UberGuestRideLogs.query()
  .insert({
    guest_session_id: 'guest_12345',
    request_timestamp: new Date(),
    pickup_latitude: 37.7749,
    pickup_longitude: -122.4194,
    destination_latitude: 37.7849,
    destination_longitude: -122.4094,
    ride_type: 'UberX',
    estimated_fare: 15.50,
    ride_status: 'requested'
  });

// Update ride status
await UberGuestRideLogs.query()
  .findById(rideId)
  .patch({
    ride_status: 'completed',
    actual_fare: 14.75,
    trip_duration: 1200,
    trip_distance: 5.2
  });

// Query guest ride history
const guestRides = await UberGuestRideLogs.query()
  .where('guest_session_id', guestSessionId)
  .orderBy('request_timestamp', 'desc');
```

### Advanced Query Patterns
```javascript
// Analyze popular pickup locations
const popularPickups = await UberGuestRideLogs.query()
  .select('pickup_latitude', 'pickup_longitude')
  .count('* as ride_count')
  .groupBy('pickup_latitude', 'pickup_longitude')
  .having('ride_count', '>', 10)
  .orderBy('ride_count', 'desc');

// Calculate average fare by ride type
const fareAnalysis = await UberGuestRideLogs.query()
  .select('ride_type')
  .avg('actual_fare as avg_fare')
  .where('ride_status', 'completed')
  .groupBy('ride_type');
```

## Integration Points

### Uber API Integration
- **Ride Requests**: Log guest user ride requests to Uber services
- **Status Updates**: Track ride progression through Uber's system
- **Fare Estimation**: Record Uber's fare estimates and actual charges
- **Driver Assignment**: Log driver and vehicle information

### Guest User Management
- **Session Tracking**: Link rides to guest user sessions
- **Anonymous Analytics**: Analyze usage without personal identification
- **Conversion Tracking**: Monitor guest-to-registered user conversion
- **Service Quality**: Track guest user experience metrics

## Operational Workflows

### Ride Request Flow
1. **Guest Request**: Guest user requests ride through platform
2. **Uber API Call**: System calls Uber API for ride estimation/booking
3. **Initial Log**: Create log entry with request details
4. **Status Monitoring**: Update log as ride status changes
5. **Completion**: Final update with trip completion details

### Analytics Processing
1. **Data Collection**: Accumulate ride log data over time
2. **Pattern Analysis**: Identify usage patterns and trends
3. **Performance Metrics**: Calculate service performance indicators
4. **Business Intelligence**: Generate insights for business decisions

## Business Analytics Applications

### Guest User Behavior
- **Usage Patterns**: Analyze when and where guests request rides
- **Service Preferences**: Track preferred ride types and services
- **Geographic Analysis**: Identify popular pickup/destination areas
- **Conversion Metrics**: Monitor guest to registered user conversion rates

### Service Performance
- **Completion Rates**: Track successful vs cancelled rides
- **Response Times**: Monitor Uber service availability and response
- **Fare Accuracy**: Compare estimated vs actual fares
- **Driver Performance**: Analyze driver ratings and service quality

### Market Analysis
- **Demand Patterns**: Identify peak usage times and locations
- **Competitive Analysis**: Compare with other ridehail providers
- **Pricing Strategy**: Analyze fare sensitivity and pricing effectiveness
- **Service Coverage**: Evaluate service availability across regions

## Performance Considerations
- **Indexing Strategy**: Create indexes on frequently queried fields (guest_session_id, request_timestamp, ride_status)
- **Connection Pooling**: Leverage @maas/core MySQL connection management
- **Query Optimization**: Use Objection.js query optimization features
- **Batch Operations**: Support bulk operations for high-volume scenarios

## Data Privacy and Security
- **Anonymous Tracking**: Guest logs avoid personally identifiable information
- **Location Privacy**: Consider privacy implications of location data
- **Data Retention**: Implement appropriate data retention policies
- **Access Control**: Restrict access to sensitive ride information

## Monitoring and Alerting
- **Service Availability**: Monitor Uber API integration health
- **Error Rates**: Track failed ride requests and system errors
- **Volume Metrics**: Monitor guest ride request volumes
- **Performance Degradation**: Detect declining service quality

## Integration with Related Models
- **UberFareEstimation**: Fare calculation and estimation data
- **UberBenefitTransaction**: Financial transactions and benefits
- **UserActions**: User behavior tracking and analytics
- **RidehailTrips**: General ridehail trip management

## Data Quality and Validation
- **Coordinate Validation**: Ensure valid latitude/longitude values
- **Status Consistency**: Validate ride status transitions
- **Fare Validation**: Check fare reasonableness and consistency
- **Timestamp Accuracy**: Ensure proper chronological ordering

## Reporting and Analytics
- **Guest Usage Reports**: Regular reports on guest ride activity
- **Service Performance Dashboards**: Real-time monitoring of service metrics
- **Business Intelligence**: Integration with BI tools for advanced analytics
- **Operational Reports**: Daily/weekly operational summaries

## Development Considerations
- **Schema Evolution**: Plan for future schema changes and migrations
- **Error Handling**: Comprehensive error logging and recovery
- **Testing**: Include comprehensive test coverage for CRUD operations
- **Documentation**: Maintain accurate field definitions and business rules

## Future Enhancements
- **Real-time Tracking**: Add real-time ride progress tracking
- **Enhanced Analytics**: Include more detailed service quality metrics  
- **Integration Expansion**: Support additional ridehail providers
- **Machine Learning**: Enable predictive analytics on guest behavior