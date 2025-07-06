# Uber Guest Ride Service

## Overview

The Uber Guest Ride Service provides comprehensive ridehail trip management capabilities for Uber's guest ride API integration. This service handles the complete ridehail lifecycle including OAuth token management, trip status monitoring, fare reconciliation, refund processing, and user notifications. It serves as the primary interface between the TSP system and Uber's guest transportation services.

## Service Information

- **Service Name**: Uber Guest Ride Integration Service
- **File Path**: `/src/services/uber/guest-ride.js`
- **Type**: Transportation Service Provider Integration
- **Dependencies**: Axios, Moment, Redis, Slack, Multiple Database Models
- **External APIs**: Uber Guest Rides API, Slack Notifications

## Core Authentication

### getUberToken(forceUpdate)

Manages OAuth 2.0 token lifecycle for Uber API authentication with intelligent caching and automatic refresh capabilities.

**Purpose**: Maintain valid API authentication tokens with minimal API calls
**Parameters**: 
- `forceUpdate` (boolean): Force token refresh regardless of cache status (default: false)
**Returns**: Access token string for Uber API authorization

**Token Management Strategy**:
1. **Cache Validation**: Checks Redis cache for existing valid token
2. **Automatic Refresh**: Requests new token when cache expires or forced
3. **Expiration Handling**: Sets cache expiration 24 hours before actual expiration
4. **Error Recovery**: Comprehensive error handling with Slack notifications

**Authentication Implementation**:
```javascript
const params = {
  grant_type: 'client_credentials',
  scope: 'guests.trips',
  client_id: uberConfig.clientId,
  client_secret: uberConfig.clientSecret,
};

const data = Object.keys(params)
  .map((key) => `${key}=${encodeURIComponent(params[key])}`)
  .join('&');
```

**Error Monitoring**:
- Slack integration for authentication failures
- Detailed error logging with context
- Automatic retry mechanisms
- Token validation and storage

### getResourceFromUrl(url)

Provides authenticated HTTP client for Uber API resource retrieval with comprehensive error handling.

**Purpose**: Standardized API resource access with authentication and error management
**Parameters**: 
- `url` (string): Uber API endpoint URL
**Returns**: API response data or null for 404 errors

**Request Configuration**:
```javascript
const options = {
  url,
  method: 'GET',
  headers: {
    Authorization: 'Bearer ' + token,
    Accept: 'application/json',
  },
};
```

**Error Handling Strategy**:
- HTTP 404 handling for missing resources
- Authentication error recovery
- Network error management
- Response validation and parsing

## Trip Status Management

### Trip Status Update Strategies

The service implements a sophisticated strategy pattern for handling different trip status transitions, ensuring data consistency and proper user experience.

**Status Update Functions**:

#### updateAccepted(previousStatus, log)
Handles trip acceptance with driver assignment and vehicle information.

**Driver Information Processing**:
```javascript
updateInfo.driver_name = driver.name;
updateInfo.driver_image_url = driver.picture_url;
updateInfo.vehicle_color = capitalizeLetters(vehicle.vehicle_color_name);
updateInfo.vehicle_lpn = vehicle.license_plate;
updateInfo.vehicle_make = vehicle.make;
updateInfo.vehicle_model = vehicle.model;
updateInfo.pickup_eta = pickup.eta;
updateInfo.dropoff_eta = destination.eta;
```

#### updateCompleted(previousStatus, log)
Processes trip completion with timing and final details.

**Completion Data Processing**:
```javascript
updateInfo.pickup_time = moment(log.begin_trip_time).utc().toISOString();
updateInfo.dropoff_time = moment(log.dropoff_time).utc().toISOString();
updateInfo.trip_status = TripStatus.COMPLETED;
```

#### updateDriverCancel(previousStatus, log)
Manages driver cancellation scenarios with refund initiation.

#### updateRiderCancel(previousStatus, log)
Handles rider cancellation with payment status updates.

#### updateNoDriversAvailable(previousStatus, log)
Processes no-driver scenarios with automatic refund processing.

### updateRideRequest(tripDetail)

Orchestrates comprehensive trip status updates with business logic enforcement and notification management.

**Purpose**: Central trip update processing with status validation and notifications
**Parameters**: 
- `tripDetail` (object): Complete trip information from Uber API
**Returns**: Promise resolving to update completion

**Update Process Flow**:
1. **Status Validation**: Verifies valid status transitions
2. **Data Retrieval**: Fetches existing trip record from database
3. **Strategy Selection**: Applies appropriate update strategy based on status
4. **Database Update**: Persists changes to trip record
5. **Notification Dispatch**: Sends user notifications for relevant status changes
6. **Trip Finalization**: Updates related trip logs and telework records

**Status Transition Logic**:
```javascript
switch (status) {
  case TripStatus.PROCESSING:
  case TripStatus.ACCEPTED:
  case TripStatus.ARRIVING:
  case TripStatus.IN_PROGRESS:
  case TripStatus.COMPLETED:
  case TripStatus.RIDER_CANCELED:
  case TripStatus.DRIVER_CANCELED:
  case TripStatus.NO_DRIVERS_AVAILABLE:
  case TripStatus.DRIVER_REDISPATCHED:
    updateInfo = await updateStrategy[status](previousStatus, tripDetail);
    break;
}
```

**Environment-Specific Handling**:
- Mock license plate numbers for non-production environments
- Development environment data simulation
- Staging environment testing support

## Financial Management

### Fare Reconciliation System

#### auditFare(requestId, tripRecord)

Implements comprehensive fare auditing to ensure pricing accuracy and handle discrepancies.

**Purpose**: Validate fare accuracy and trigger appropriate actions for discrepancies
**Parameters**: 
- `requestId` (string): Uber request identifier
- `tripRecord` (object): Trip record with fare information
**Returns**: Promise resolving to audit completion

**Audit Logic**:
1. **Fare Comparison**: Compares estimated vs actual fare amounts
2. **Discrepancy Handling**: Triggers refund process for canceled trips
3. **Alert Generation**: Sends Slack notifications for completed trip discrepancies
4. **Payment Status Updates**: Updates payment status based on audit results

**Discrepancy Resolution**:
```javascript
if (eFare !== aFare) {
  if (tripStatus === TripStatus.COMPLETED) {
    slack.sendVendorFailedMsg({
      vendor: 'Uber',
      errorMsg: 'estimated_fare is not equal to actual_fare',
      meta: JSON.stringify({
        uber_request_id: requestId,
        estimated_fare: eFare,
        actual_fare: aFare,
      }),
    });
  }
}
```

### Advanced Refund Processing

#### refund(requestId, refundType)

Handles complex refund scenarios including benefit credit processing and multi-party transactions.

**Purpose**: Process refunds with support for benefit credits and complex payment scenarios
**Parameters**: 
- `requestId` (string): Uber request identifier
- `refundType` (string): Type of refund (rider_canceled, driver_canceled, etc.)
**Returns**: Promise resolving to refund completion

**Refund Processing Logic**:
1. **Trip Data Retrieval**: Fetches complete trip financial information
2. **Benefit Analysis**: Determines if benefit credits were applied
3. **Refund Calculation**: Calculates appropriate refund amounts
4. **Transaction Processing**: Executes refund transactions through points system
5. **Status Updates**: Updates payment status in database

#### refundWithBenefit(userId, eFare, aFare, benefit, note)

Implements sophisticated multi-party refund processing for trips with benefit credit applications.

**Purpose**: Handle complex refund scenarios involving system benefit credits
**Parameters**: 
- `userId` (number): User receiving refund
- `eFare` (number): Estimated fare amount
- `aFare` (number): Actual fare charged by Uber
- `benefit` (number): Benefit credit amount applied
- `note` (string): Transaction description
**Returns**: Promise resolving to benefit refund completion

**Multi-Party Transaction Logic**:
```javascript
const returnBenefit = Math.min(eFare, benefit);
const newBenefitShouldPay = aFare >= benefit ? benefit : aFare;
const discountFare = eFare >= benefit ? eFare - benefit : 0;
const refundFare = discountFare - (aFare > benefit ? aFare - benefit : 0);
```

**Transaction Flow**:
1. **User Refund**: Returns excess charge to user account
2. **System Benefit Return**: Returns original benefit credit to system
3. **System Benefit Payment**: System pays actual benefit amount to Uber
4. **Transaction Logging**: Records all transactions in audit tables

## Automated Monitoring

### Trip Monitoring Systems

#### processZombieTrips()

Identifies and resolves stale trip records that haven't received proper status updates.

**Purpose**: Detect and update trips stuck in intermediate states
**Parameters**: None
**Returns**: Promise resolving to monitoring completion

**Zombie Detection Logic**:
- Identifies trips in ongoing states (PROCESSING, ACCEPTED, ARRIVING, IN_PROGRESS, DRIVER_REDISPATCHED)
- Filters trips updated more than 30 minutes ago
- Fetches current status from Uber API
- Updates local records with current information

**Monitoring Implementation**:
```javascript
const onGoingStatus = [
  TripStatus.PROCESSING,
  TripStatus.ACCEPTED,
  TripStatus.ARRIVING,
  TripStatus.IN_PROGRESS,
  TripStatus.DRIVER_REDISPATCHED,
];
const thirtyMinutesAgo = moment.utc().add(-30, 'minutes').toISOString();
```

#### processRefundingTrips()

Manages automated refund processing for trips with pending refund status.

**Purpose**: Process trips requiring refund with timeout handling
**Parameters**: None
**Returns**: Promise resolving to refund processing completion

**Refund Processing Strategy**:
1. **Pending Trip Identification**: Finds trips with REFUND_IN_PROGRESS status
2. **Receipt Validation**: Checks for available receipts from Uber
3. **Timeout Handling**: Processes refunds for trips older than 24 hours
4. **Lock Management**: Prevents concurrent processing of same trip

### Receipt Processing

#### processReceipt(tripDetail, requestId)

Handles comprehensive receipt data processing with distance validation and fare reconciliation.

**Purpose**: Process final trip receipts with distance and fare validation
**Parameters**: 
- `tripDetail` (object): Receipt information from Uber API
- `requestId` (string): Uber request identifier
**Returns**: Promise resolving to receipt processing completion

**Receipt Data Processing**:
```javascript
const updateInfo = {
  actual_fare: convertCurrencyToNumber(totalFare),
  receipt_distance: distance,
  receipt_duration: moment.duration(duration).asSeconds(),
};
```

**Distance Validation**:
- Converts distance from miles to meters
- Validates distance label consistency
- Mocks distance for sandbox environments
- Updates trip logs with accurate distance data

## Incentive Integration

### processIncentive(log, record)

Integrates completed trips with the incentive engine system for reward processing.

**Purpose**: Process completed trips through incentive calculation system
**Parameters**: 
- `log` (object): Trip completion log from Uber
- `record` (object): Local trip record
**Returns**: Promise resolving to incentive processing completion

**Version Validation**:
```javascript
const checkVersion = (version) => {
  const mainVersion = extractVersion(version);
  return mainVersion >= 125;
};
```

**Incentive Data Preparation**:
```javascript
const mti = {
  origin_latitude: log.pickup.latitude,
  origin_longitude: log.pickup.longitude,
  real_origin_latitude: log.pickup.latitude,
  real_origin_longitude: log.pickup.longitude,
  destination_latitude: log.destination.latitude,
  destination_longitude: log.destination.longitude,
  real_destination_latitude: log.destination.latitude,
  real_destination_longitude: log.destination.longitude,
  started_on: moment(log.begin_trip_time).utc().toISOString(),
  real_started_on: moment(log.begin_trip_time).utc().toISOString(),
};
```

## Notification System

### User Communication

**Notification Messages**:
```javascript
const notificationMessages = {
  accepted: 'Uber has found a driver for you.',
  arriving: 'Your Uber driver is arriving at the pickup point.',
  completed: 'How was your ride? Share your thoughts with us.',
  no_drivers_available: 'We're sorry, Uber is not able to find a driver at this moment.',
  driver_canceled: 'Oops! Looks like you didn't make it to the pickup point.',
  rider_canceled: 'Your trip has been canceled. We will notify you when your refund is ready.',
  refunded: 'Your Uber refund is complete and the Coins have been returned to your Wallet.',
  driver_redispatched: "Oops! Your driver had to be re-dispatched. Hang tight while Uber finds you another driver.",
};
```

**Notification Processing**:
- Status-based message selection
- User-specific targeting
- Rich metadata inclusion
- Multi-language support (en_us default)

## Data Management

### Cache Management

#### clearOutdatedCaches()

Implements intelligent cache cleanup for performance optimization and storage management.

**Purpose**: Remove expired cache data to maintain system performance
**Parameters**: None
**Returns**: Promise resolving to cache cleanup completion

**Cleanup Strategy**:
```javascript
const threeMonthsAgo = new Date(Date.now() - 60 * 60 * 1000 * 24 * 90);

let result = await UberFareEstimation.deleteMany({
  modified_at: { $lt: threeMonthsAgo },
});

result = await UberApiPayload.deleteMany({
  created_at: { $lt: threeMonthsAgo },
});
```

**Performance Benefits**:
- Reduces database storage requirements
- Improves query performance
- Maintains optimal cache hit ratios
- Enables predictable resource usage

### Distance Calculation

#### mockTripDistance(tripRecord, distance)

Provides distance calculation fallback for development and testing environments.

**Purpose**: Calculate trip distance when API doesn't provide accurate data
**Parameters**: 
- `tripRecord` (object): Trip record with coordinates
- `distance` (number): Current distance value
**Returns**: Calculated or original distance value

**Distance Calculation**:
```javascript
if (tripRecord.trip_status === TripStatus.COMPLETED && distance === 0) {
  const {
    pickup_latitude: lat1,
    pickup_longitude: lng1,
    dropoff_latitude: lat2,
    dropoff_longitude: lng2,
  } = tripRecord;
  distance = calcDistance(lat1, lng1, lat2, lng2);
}
```

## Concurrency Management

### Transaction Locking

#### acquireLock(requestId, expireTime)

Implements distributed locking to prevent concurrent processing of trip operations.

**Purpose**: Ensure transaction safety for financial operations
**Parameters**: 
- `requestId` (string): Unique identifier for lock
- `expireTime` (number): Lock expiration time in seconds (default: 5)
**Returns**: Boolean indicating lock acquisition success

**Lock Implementation**:
```javascript
const key = `${stage}:uber:tx:${requestId}`;
const value = new Date().getTime() + expireTime * 1000 + 1;
const acquired = await cache.set(key, value, 'NX', 'EX', expireTime);
return acquired === 'OK';
```

#### releaseLock(requestId)

Releases distributed locks after transaction completion.

**Purpose**: Clean up locks after operation completion
**Parameters**: 
- `requestId` (string): Lock identifier to release
**Returns**: Promise resolving to lock release completion

## Error Handling Strategy

### Comprehensive Error Management

**Error Categories**:
- **Authentication Errors**: Token refresh failures, API access issues
- **Network Errors**: Timeout, connectivity, rate limiting
- **Data Errors**: Invalid responses, missing data, format issues
- **Business Logic Errors**: Invalid state transitions, constraint violations
- **Financial Errors**: Payment processing, refund failures, audit discrepancies

**Error Recovery Patterns**:
```javascript
try {
  await updateRideRequest(tripDetails);
} catch (err) {
  logger.error(`[uber-zombie-killer] error updating uber_request_id=${requestId}`);
  logger.error(err.message);
  logger.error(err.stack);
}
```

**Slack Integration for Monitoring**:
- Real-time error notifications
- Vendor API failure alerts
- Financial discrepancy warnings
- System health monitoring

## Performance Optimization

### Batch Processing

**Notification Batching**:
```javascript
await Promise.all(
  notifications.map(async (notification) => {
    const { userId, title, body, meta } = notification;
    return await sendNotification(
      [userId],
      NotificationType,
      title,
      body,
      meta,
      'en_us',
      false,
    );
  }),
);
```

**Database Optimization**:
- Bulk update operations
- Efficient query patterns
- Connection pooling
- Index utilization

### Memory Management

- Streaming for large datasets
- Efficient object allocation
- Garbage collection optimization
- Memory leak prevention

## Usage Examples

### Basic Trip Monitoring

```javascript
// Process zombie trips
await processZombieTrips();

// Handle refunding trips
await processRefundingTrips();

// Process rider canceled trips
await processRiderCanceledTrips();

// Clear outdated caches
await clearOutdatedCaches();
```

### Error Handling Implementation

```javascript
async function safeProcessTrip(requestId) {
  let isLocked = false;
  
  try {
    isLocked = await acquireLock(requestId);
    if (!isLocked) {
      logger.warn(`Transaction already locked: ${requestId}`);
      return false;
    }
    
    const receipt = await checkReceipt(requestId);
    if (receipt) {
      await processReceipt(receipt, requestId);
    }
    
    return true;
  } catch (error) {
    logger.error(`Trip processing failed: ${requestId}`, error);
    return false;
  } finally {
    if (isLocked) {
      await releaseLock(requestId);
    }
  }
}
```

## Integration Points

### Internal Services

- **Notification Service**: User communication system
- **Wallet Service**: Points transaction processing
- **Incentive Engine**: Reward calculation system
- **Telework System**: Trip logging and tracking

### External APIs

- **Uber Guest Rides API**: Primary transportation provider
- **Slack API**: Monitoring and alerting system
- **Payment Processing**: Financial transaction handling

## Limitations and Future Enhancements

### Current Limitations

**API Constraints**:
- Single tenant Uber integration
- Limited error recovery options
- Basic retry mechanisms
- Fixed timeout values

**Financial Processing**:
- Simple refund logic
- Limited multi-party transaction support
- Basic audit capabilities
- Manual reconciliation processes

### Future Improvements

**Enhanced Features**:
- Multi-vendor ridehail support
- Advanced retry strategies
- Real-time status monitoring
- Enhanced financial processing

**Performance Enhancements**:
- Parallel processing pipelines
- Advanced caching strategies
- Database optimization
- Memory usage optimization

## Dependencies

- **axios**: HTTP client for API communication
- **moment-timezone**: Date/time manipulation with timezone support
- **config**: Environment configuration management
- **@maas/services**: Slack integration and shared services
- **@maas/core/redis**: Distributed caching and locking
- **@maas/core/log**: Comprehensive logging system
- **Multiple Database Models**: Trip, user, and financial data models
- **Notification Service**: User communication system
- **Wallet Service**: Points and transaction processing
- **Utility Functions**: Distance calculation, data processing helpers