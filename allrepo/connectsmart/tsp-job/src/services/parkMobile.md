# ParkMobile Service

## Overview

The ParkMobile service provides comprehensive parking event management and notification system integration for the ParkMobile parking platform. This service handles API token management, parking event lifecycle monitoring, cache maintenance, and user notifications for parking meter expiration alerts.

## Service Information

- **Service Name**: ParkMobile Integration Service
- **File Path**: `/src/services/parkMobile.js`
- **Type**: Parking Service Integration
- **Dependencies**: Axios HTTP Client, ParkMobile API, MySQL, MongoDB, Notification Service

## Core Functions

### updateToken()

Manages OAuth token lifecycle for ParkMobile API authentication, ensuring continuous API access through automatic token refresh and cleanup.

**Purpose**: Maintain valid API authentication tokens
**Parameters**: None
**Returns**: Promise resolving to token update completion

**Token Management Process**:
1. Requests new access token using client credentials flow
2. Calculates token expiration based on API response
3. Stores new token in MySQL with UTC timestamp
4. Removes expired tokens to maintain clean token table

**Implementation Details**:
```javascript
const tokenInfo = await getToken();
await PmApiToken.query().insert({
  token: tokenInfo.access_token,
  expires: moment.utc().add(tokenInfo.expires_in, 'seconds').toISOString(),
});
await PmApiToken.query()
  .where('expires', '<=', moment.utc().add(1, 'minute').toISOString())
  .delete();
```

**Error Handling**:
- Comprehensive error logging with stack traces
- Token request failure management
- Database operation error recovery

### getToken()

Performs OAuth 2.0 client credentials authentication with ParkMobile API to obtain access tokens.

**Purpose**: Retrieve fresh API access tokens
**Parameters**: None
**Returns**: Token object with access_token and expires_in

**Authentication Flow**:
- Uses client_credentials grant type
- Sends client_id and client_secret
- Processes application/x-www-form-urlencoded request
- Validates response schema using Joi validation

**HTTP Configuration**:
```javascript
const options = {
  method: 'post',
  maxBodyLength: Infinity,
  url: 'connect/token',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  data: qs.stringify({
    grant_type: 'client_credentials',
    client_id: pmConfig.clientId,
    client_secret: pmConfig.clientSecret,
  }),
};
```

### purgeOutdatedCache()

Implements intelligent cache cleanup strategy to maintain optimal system performance and storage efficiency.

**Purpose**: Remove expired cache data based on retention policies
**Parameters**: None
**Returns**: Promise with deletion statistics

**Retention Policies**:
- **Price Objects**: 30-day retention period
- **Parking Events**: 90-day retention period
- **Date Calculation**: Uses moment.js for accurate date arithmetic

**Cleanup Implementation**:
```javascript
const thirtyDaysAgo = moment().subtract(30, 'days').toDate();
let result = await PmPriceObjects.deleteMany({
  createdAt: { $lt: thirtyDaysAgo },
});

const ninetyDaysAgo = moment().subtract(90, 'days').toDate();
result = await PmParkingEvents.deleteMany({
  createdAt: { $lt: ninetyDaysAgo },
});
```

**Performance Logging**:
- Reports deletion counts for monitoring
- Tracks cache cleanup efficiency
- Enables storage optimization analysis

### checkFinishedAndExpiredEvents(now)

Manages parking event status transitions based on temporal rules and business logic.

**Purpose**: Update event statuses based on time-based conditions
**Parameters**: 
- `now` (string): Current timestamp for status evaluation
**Returns**: Promise resolving to update completion

**Status Transition Logic**:

**Expired Events**:
- Events older than 24 hours from parking_stop_time_UTC
- Transitions from ON_GOING, ALERTED, or FINISHED to EXPIRED
- Uses minute-precision timestamps for accuracy

**Finished Events**:
- Events past their parking_stop_time_UTC
- Transitions from ON_GOING or ALERTED to FINISHED
- Real-time status updates for active parking sessions

**Database Operations**:
```javascript
const expiredCount = await PmParkingEvent.query()
  .whereIn('status', [status.ON_GOING, status.ALERTED, status.FINISHED])
  .andWhere('parking_stop_time_UTC', '<=', expiredTime)
  .update({
    status: status.EXPIRED,
  });
```

### checkOnGoingEvents(now)

Implements proactive parking meter expiration notification system with user engagement features.

**Purpose**: Send timely parking expiration alerts to users
**Parameters**: 
- `now` (string): Current timestamp for alert timing
**Returns**: Promise resolving to notification completion

**Alert Logic**:
- Queries events with ON_GOING status
- Filters events with configured alert_before values
- Identifies events within 5-minute alert window
- Processes batch notifications for efficiency

**Notification Generation**:
```javascript
const notifications = events.map((event) => {
  const title = 'Parking Reminder';
  const body = `Your meter will expire in ${event.alert_before} minutes.`;
  return {
    userId: event.user_id,
    title,
    body,
    meta: {
      title,
      body,
      id: event.id,
    },
  };
});
```

**Status Management**:
- Updates events to ALERTED status after notification
- Maintains event state consistency
- Validates notification delivery counts

## Technical Architecture

### HTTP Client Configuration

**Base Configuration**:
```javascript
const httpClient = () => {
  let options = {
    baseURL: 'https://auth.parkmobile.io',
    timeout: 10000,
  };
  return axios.create(options);
};
```

**Features**:
- 10-second timeout for API calls
- Configurable proxy support for development
- HTTPS-only communication
- Environment-specific customization

### Status Management System

**Event Status Constants**:
```javascript
const status = {
  ON_GOING: 'on-going',
  ALERTED: 'alerted',
  FINISHED: 'finished',
  EXPIRED: 'expired',
};
```

**Status Transition Rules**:
- **ON_GOING → ALERTED**: User notified of impending expiration
- **ALERTED → FINISHED**: Parking session completed
- **FINISHED → EXPIRED**: Historical archival after 24 hours
- **Any Status → EXPIRED**: Forced expiration for cleanup

### Data Models Integration

**MySQL Models (Objection.js)**:
- **PmApiToken**: OAuth token storage with expiration
- **PmParkingEvent**: Individual parking session tracking

**MongoDB Models (Mongoose)**:
- **PmParkingEvents**: Historical parking event collection
- **PmPriceObjects**: Pricing information cache

### Validation System

**Schema Validation**:
```javascript
const checkParams = async (params, schema) => {
  return await parkMobileValidator[schema].validateAsync(params);
};
```

**Supported Schemas**:
- **token**: OAuth token response validation
- **event**: Parking event data validation
- **pricing**: Price object structure validation

## Notification System Integration

### Push Notification Configuration

**Notification Type**: 97 (ParkMobile specific)
**Supported Features**:
- Multi-language support (en_us default)
- Rich metadata inclusion
- User targeting by ID
- Delivery confirmation

### Notification Flow

**Alert Timing**:
1. Identify events within 5-minute alert window
2. Generate user-specific notification content
3. Send parallel notifications using Promise.all
4. Update event status to prevent duplicate alerts
5. Log notification delivery statistics

**Content Customization**:
- Dynamic message generation with remaining time
- Consistent branding with "Parking Reminder" title
- Event-specific metadata for mobile app handling

## Error Handling Strategy

### API Error Management

**Token Request Failures**:
- HTTP client timeout handling
- OAuth error response parsing
- Automatic retry mechanisms
- Comprehensive error logging

**Database Error Recovery**:
- Transaction rollback for consistency
- Partial success handling
- Connection pool management
- Deadlock detection and recovery

### Logging Strategy

**Error Categories**:
- **API Communication Errors**: Network, timeout, authentication
- **Database Operation Errors**: Connection, query, constraint violations
- **Business Logic Errors**: Invalid state transitions, data inconsistencies
- **System Errors**: Memory, resource exhaustion, configuration issues

**Log Formatting**:
```javascript
logger.error(`[park-mobile.updateToken]${err.message}`);
logger.error(`[park-mobile.updateToken]${err.stack}`);
```

## Performance Optimization

### Database Query Optimization

**Efficient Querying**:
- Index utilization on timestamp fields
- Batch operations for bulk updates
- Range queries for time-based filtering
- Status-based partitioning strategies

**Connection Management**:
- Connection pooling for MySQL
- MongoDB connection optimization
- Query result streaming for large datasets

### Memory Management

**Cache Strategies**:
- Time-based cache invalidation
- Memory-efficient data structures
- Lazy loading for large collections
- Garbage collection optimization

### Batch Processing

**Notification Batching**:
- Parallel notification delivery
- Batch size optimization
- Error isolation between batches
- Delivery confirmation tracking

## Security Considerations

### API Security

**OAuth Token Management**:
- Secure token storage with encryption
- Token rotation and expiration
- Scope-limited API access
- Environment-specific credentials

**Data Transmission**:
- HTTPS-only communication
- Request/response validation
- API rate limiting compliance
- Error information sanitization

### Data Privacy

**User Data Protection**:
- Minimal data retention policies
- User consent compliance
- Data anonymization strategies
- Audit trail maintenance

**PCI Compliance**:
- Payment card data isolation
- Secure payment processing
- Compliance monitoring
- Regular security audits

## Integration Points

### Internal Services

**Notification Service**:
- Real-time alert delivery
- Multi-channel notification support
- Delivery confirmation tracking
- User preference management

**Job Scheduler**:
- Automated token refresh
- Periodic cache cleanup
- Event status monitoring
- System health checks

### External APIs

**ParkMobile API**:
- OAuth 2.0 authentication
- RESTful API consumption
- Real-time parking data
- Payment processing integration

## Deployment Considerations

### Environment Configuration

**API Endpoints**:
- Production: https://auth.parkmobile.io
- Staging: Configurable through environment
- Development: Proxy support available

**Database Configuration**:
- MySQL for transactional data
- MongoDB for event storage
- Connection string management
- Pool size optimization

### Monitoring and Alerting

**Key Metrics**:
- Token refresh success rates
- Notification delivery rates
- Event processing latency
- Cache cleanup efficiency

**Health Checks**:
- API connectivity monitoring
- Database connection validation
- Token expiration alerts
- Event processing status

## Usage Examples

### Basic Operations

```javascript
// Refresh API tokens
await updateToken();

// Clean expired cache data
await purgeOutdatedCache();

// Process parking events
const now = moment.utc().toISOString();
await checkFinishedAndExpiredEvents(now);
await checkOnGoingEvents(now);
```

### Error Handling Pattern

```javascript
try {
  await updateToken();
  logger.info('Token updated successfully');
} catch (error) {
  logger.error(`Token update failed: ${error.message}`);
  // Implement retry logic or alert administrators
}
```

## Limitations and Future Enhancements

### Current Limitations

**API Constraints**:
- Single tenant OAuth implementation
- Fixed timeout values
- Limited retry mechanisms
- Basic error recovery

**Notification System**:
- Single notification type support
- Limited customization options
- No delivery confirmation tracking
- Basic error handling

### Future Improvements

**Enhanced Features**:
- Multi-tenant API support
- Advanced retry strategies
- Real-time webhook integration
- Enhanced notification customization

**Performance Enhancements**:
- Async processing pipelines
- Advanced caching strategies
- Database sharding support
- Machine learning for optimal alert timing

## Dependencies

- **axios**: HTTP client for API communication
- **qs**: Query string parsing for form data
- **config**: Environment configuration management
- **moment**: Date/time manipulation and formatting
- **@maas/core/log**: Comprehensive logging system
- **ParkMobile Models**: Database models for data persistence
- **parkMobileValidator**: Joi-based schema validation
- **sendNotification**: Internal notification service