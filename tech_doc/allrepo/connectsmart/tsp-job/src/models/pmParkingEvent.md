# pmParkingEvent Model Documentation

## Overview
PmParkingEvent is a Knex.js-based model that manages ParkMobile parking event data in the portal MySQL database. This model handles parking transaction events, session tracking, and integration with the ParkMobile parking service platform.

## Class Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class PmParkingEvent extends Model {
  static get tableName() {
    return 'pm_parking_event';
  }
}
module.exports = PmParkingEvent.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL (`portal`)
- **Table**: `pm_parking_event`
- **ORM**: Knex.js with Model base class
- **Connection**: Managed through @maas/core/mysql

## Core Functionality

### Parking Event Management
- Records all ParkMobile parking events and transactions
- Tracks parking session lifecycle (start, duration, end)
- Manages payment processing events
- Maintains event history for audit and analysis

### Transaction Tracking
- Links parking events to user accounts
- Correlates events with payment transactions
- Tracks parking zone and location data
- Manages event status and completion

## Usage Patterns

### Event Recording
```javascript
const PmParkingEvent = require('./pmParkingEvent');

// Record parking event
const parkingEvent = await PmParkingEvent.query().insert({
  user_id: userId,
  session_id: sessionId,
  event_type: 'parking_start',
  zone_id: zoneId,
  location_data: JSON.stringify(locationInfo),
  timestamp: new Date(),
  amount: parkingFee,
  payment_method: 'credit_card',
  status: 'completed'
});

// Query user parking history
const userEvents = await PmParkingEvent.query()
  .where('user_id', userId)
  .where('event_type', 'parking_session')
  .orderBy('timestamp', 'desc');
```

### Session Management
- Parking session initiation tracking
- Real-time session monitoring
- Session completion and billing
- Session modification and extensions

## Event Types and Categories

### Session Events
- **Session Start**: Parking session initiation
- **Session Active**: Ongoing parking monitoring
- **Session Extension**: Duration extension requests
- **Session End**: Parking session completion
- **Session Cancel**: Cancelled parking sessions

### Payment Events
- **Payment Processing**: Transaction initiation
- **Payment Success**: Completed transactions
- **Payment Failed**: Failed payment attempts
- **Refund Processing**: Refund transaction handling
- **Payment Adjustment**: Fee adjustments and corrections

### System Events
- **Zone Updates**: Parking zone configuration changes
- **Rate Changes**: Pricing update notifications
- **System Maintenance**: Service maintenance events
- **Error Notifications**: System error tracking

## Integration Points

### ParkMobile Platform
- **API Integration**: Real-time event synchronization
- **Zone Management**: Parking zone data integration
- **Rate Management**: Dynamic pricing integration
- **User Management**: Account correlation

### Internal Systems
- **User Accounts**: Customer profile integration
- **Payment Processing**: Transaction correlation
- **Location Services**: Geographic data integration
- **Analytics**: Usage pattern analysis

### External Services
- **Mapping Services**: Location validation
- **Payment Processors**: Transaction processing
- **Notification Systems**: User alert integration
- **Municipal Systems**: Parking authority integration

## Data Flow
1. **Event Generation**: ParkMobile system generates events
2. **API Reception**: Events received via webhook/API
3. **Data Processing**: Event validation and enrichment
4. **Storage**: Event persistence in MySQL
5. **Analytics**: Event analysis and reporting

## Performance Considerations
- High-volume event processing optimization
- Real-time event streaming capabilities
- Efficient indexing for time-based queries
- Bulk event processing for historical data

## Data Quality Features
- Event validation and verification
- Duplicate event detection
- Data consistency checks
- Error handling and recovery

## Security Measures
- Secure API communication with ParkMobile
- Event data encryption for sensitive information
- Access control for event data
- Audit logging for compliance

## Analytics Capabilities
- Parking usage pattern analysis
- Revenue tracking and reporting
- User behavior analysis
- Zone performance metrics

## Related Components
- **pmParkingEvents**: MongoDB event caching
- **pmPriceObjects**: Pricing data management
- **Payment Systems**: Transaction processing
- **Location Services**: Geographic integration
- **Analytics Dashboard**: Performance monitoring

## Monitoring and Alerting
- Real-time event processing monitoring
- Failed event detection and alerting
- Performance metric tracking
- System health monitoring

## Compliance Requirements
- PCI compliance for payment data
- Municipal parking regulation compliance
- Data privacy law adherence
- Audit trail maintenance

## Maintenance Operations
- Regular event data cleanup
- Performance optimization
- System integration monitoring
- Data consistency validation

## Future Enhancements
- Real-time event streaming
- Machine learning analytics
- Advanced fraud detection
- Multi-provider integration
- Enhanced mobile integration