# TSP Job Test: Transit Alert Notification System Test Documentation

## Quick Summary

**Purpose**: Comprehensive integration test suite for transit alert notification system that manages real-time incident notifications for transit routes, favorite routes, and active reservations.

**Key Features**:
- Tests ongoing and cleared transit alert processing
- Validates notification filtering by user preferences
- Handles route favorites and active reservations
- Implements comprehensive mock data management
- Tests complete notification workflow from alert detection to user delivery
- Supports notification types: OngoingAlert and ClearAlert

**Technology Stack**: Mocha testing framework, Chai assertions, Sinon for mocking, Moment.js for date handling

## Technical Analysis

### Code Structure

The test file implements a complex integration testing framework for transit alert management:

```javascript
// Core job and service imports
const { fn: job } = require('@app/src/jobs/transit-alert');
const {
  searchOngoingEvents,
  searchClearEvents,
  filterNotificationByUserConfig,
  filterExistingNotifications,
  fetchOngoingReservations,
  fetchOngoingRouteFavorites,
  // ... other service functions
} = require('@app/src/services/transitAlert');
```

### Key Components

**Database Models Integration**:
- `TransitAlert`: Core alert definitions and lifecycle
- `TransitAlertRoute`: Alert-to-route mapping relationships
- `BusRouteFavorite`: User route preference management
- `Reservations`: Active trip reservations
- `TripDetail`: Detailed trip information with route steps
- `TransitAlertNotificationQueue`: Notification delivery tracking
- `UserConfig`: User notification preferences
- `Notification`: Core notification records

**Mock Data Architecture**:
The test creates comprehensive mock datasets covering:
- 6 transit alerts with varying expiration times
- Route mappings (ME07, ME09, ME12, ME13, TEST01, TEST02)
- User favorites and reservations
- Trip details with JSON step definitions
- Notification queue history
- User configuration preferences

**Alert Lifecycle Management**:
```javascript
// Alert status classification
const ongoingAlerts = alerts.filter(alert => 
  moment.unix(alert.expires).isAfter(moment.utc())
);

const expiredAlerts = alerts.filter(alert => 
  moment.unix(alert.expires).isBefore(moment.utc())
);
```

### Implementation Details

**Test Data Generation Patterns**:
```javascript
const mockTransitAlerts = mockDataList.map((row) => {
  alertIds.push(id);
  return {
    event_id: id++,
    type: 'TEST',
    effect_name: 'Delay',
    header_text: 'Route Test Header',
    short_header_text: 'Route Test Header',
    description_text: 'Route Test Description',
    start: row.start || moment.utc().add(-1, 'day').unix(),
    expires: row.expires || moment.utc().add(1, 'month').unix(),
    created_dt: row.created_dt || moment.utc().add(-1, 'day').unix(),
  };
});
```

**Route-Alert Mapping Structure**:
```javascript
const mockTransitAlertRouteMappings = [
  { event_id: 1234, route_id: 'ME07' },
  { event_id: 1235, route_id: 'ME09' },
  { event_id: 1236, route_id: 'ME12' },
  { event_id: 1237, route_id: 'ME13' },
  { event_id: 1238, route_id: 'TEST01' },
  { event_id: 1239, route_id: 'TEST02' }
];
```

**User Configuration Management**:
```javascript
const mockUserConfig = [
  {
    user_id: 5577,
    uis_setting: {
      transit_incident: true,  // Enabled notifications
    },
  },
  {
    user_id: 5588,
    uis_setting: {
      transit_incident: false, // Disabled notifications
    },
  },
];
```

**Trip Detail JSON Structure**:
```javascript
const tripSteps = [
  {
    type: 'pedestrian',
    transport: { mode: 'pedestrian' },
  },
  {
    type: 'transit',
    transport: {
      route_id: 'ME07',
      trip_id: '10146157',
      direction_id: '0',
      mode: 'bus',
      name: '007',
      category: 'Bus',
      headsign: '',
      shortName: '007',
      longName: 'Northshore Express',
      fare: 0,
      is_ticket: 0,
      product_id: '',
      color: '#004080',
    },
  },
  {
    type: 'pedestrian',
    transport: { mode: 'pedestrian' },
  }
];
```

## Usage/Integration

### Test Execution

**Running Transit Alert Tests**:
```bash
# Run complete transit alert test suite  
npm test test/testTransitAlert.js

# Run with extended timeout for integration tests
npm test test/testTransitAlert.js --timeout 10000
```

**Test Environment Setup**:
- Requires MySQL database with complete transit schema
- Message queue service for notification delivery
- Mock user accounts and route configurations

### Service Integration Flow

**Alert Processing Pipeline**:
1. **Search Events**: Identify ongoing and cleared alerts
2. **Fetch Recipients**: Find users with affected favorites/reservations
3. **Filter by Preferences**: Apply user notification settings
4. **Deduplicate**: Remove already-sent notifications
5. **Send Notifications**: Deliver via message queue
6. **Track Delivery**: Record in notification queue

**Integration Points**:
```javascript
// Service method integration
const events = await searchOngoingEvents();
const ongoingFavorites = await fetchOngoingRouteFavorites(events);
const ongoingReservations = await fetchOngoingReservations(events);

// Filtering and validation
const filteredRoutes = await filterNotificationByUserConfig(ongoingFavorites);
const requiredNotifications = await filterExistingNotifications(filteredRoutes);

// Notification delivery
await notifyFavoriteRoute(NotificationType.OngoingAlert, requiredNotifications);
await notifyReservation(NotificationType.OngoingAlert, requiredReservations);
```

### Mock Queue Integration

**Message Queue Stubbing**:
```javascript
const queue = require('@app/src/services/queue');
const mockQueue = stub(queue, 'sendTask');
mockQueue.callsFake((_, data) => {
  logger.debug(data);
  return true;
});
```

## Dependencies

### Core Dependencies

**Testing Framework**:
- `chai`: Assertion library with expect interface
- `sinon`: Mocking and stubbing framework for external services
- `mocha`: Test runner with extended timeout support

**Date/Time Management**:
- `moment`: Date manipulation and timezone handling
- UTC time standardization for alert expiration logic

**Database Layer**:
- `@maas/core/bootstrap`: Application initialization
- Multiple Objection.js models for database operations

### Service Dependencies

**Alert Management Services**:
- `@app/src/services/transitAlert`: Core alert processing logic
- `@app/src/jobs/transit-alert`: Scheduled job execution
- `@app/src/services/queue`: Message queue integration

**Database Models**:
- Transit alert and route mapping models
- User preference and configuration models
- Notification tracking and delivery models
- Trip and reservation management models

### External Service Integration

**Notification Delivery**:
- Message queue service for async notification delivery
- User notification preference management
- Multiple notification channels (push, email, SMS)

**Transit Data Sources**:
- Real-time transit feed integration
- Route and schedule data management
- Incident and service alert feeds

## Code Examples

### Mock Data Creation Pattern

```javascript
const mockData = async () => {
  // Create alerts with varying expiration times
  await mockTransitAlertData([
    { expires: moment.utc().add(1, 'month').unix() },    // Active
    { expires: moment.utc().add(1, 'month').unix() },    // Active
    { expires: moment.utc().add(-1, 'minute').unix() },  // Expired
    { expires: moment.utc().add(-1, 'minute').unix() },  // Expired
    { expires: moment.utc().add(-1, 'minute').unix() },  // Expired
    { expires: moment.utc().add(1, 'month').unix() },    // Active
  ]);

  // Create user favorites
  const mockFavoriteBusRoutes = [
    { user_id: 5566, route_id: 'ME01' },
    { user_id: 5566, route_id: 'ME07' },
    { user_id: 5577, route_id: 'ME12' },
    { user_id: 5588, route_id: 'ME13' },
    { user_id: 5599, route_id: 'TEST01' },
  ];

  await Promise.all(
    mockFavoriteBusRoutes.map(async (route) => {
      await BusRouteFavorite.query().insert(route);
    })
  );
};
```

### Functional Test Flow

```javascript
it('should return the non-empty result', async function () {
  // Search for ongoing events
  const events = await searchOngoingEvents();
  expect(events.length).to.gt(0);

  // Fetch affected routes and reservations
  const ongoingFavorites = await fetchOngoingRouteFavorites(events);
  const ongoingReservations = await fetchOngoingReservations(events);
  expect(ongoingFavorites.length).to.gt(0);
  expect(ongoingReservations.length).to.gt(0);

  // Search for cleared events
  const clearedEvents = await searchClearEvents();
  expect(clearedEvents.length).to.eq(3);

  // Apply user preferences
  const filteredOngoingRoutes = await filterNotificationByUserConfig(
    ongoingFavorites
  );
  const filteredOngoingReservations = await filterNotificationByUserConfig(
    ongoingReservations
  );

  // Filter out already-sent notifications
  const requiredOngoingFavorites = await filterExistingNotifications(
    filteredOngoingRoutes
  );
  const requiredOngoingReservations = await filterExistingNotifications(
    filteredOngoingReservations
  );

  // Validate results
  expect(requiredOngoingFavorites.length).to.eq(1);
  const ongoingFavorite = requiredOngoingFavorites[0];
  expect(ongoingFavorite.eventId).to.eq(1234);
  expect(ongoingFavorite.routeId).to.eq('ME07');
  expect(ongoingFavorite.userId).to.eq(5566);

  // Send notifications
  await notifyFavoriteRoute(
    NotificationType.OngoingAlert,
    requiredOngoingFavorites
  );
  await notifyReservation(
    NotificationType.OngoingAlert,
    requiredOngoingReservations
  );
});
```

### Job Integration Test

```javascript
describe('job test', async function () {
  this.timeout(10 * 1000);
  
  it('should be passed without any exception', async function () {
    try {
      await job();  // Execute the actual job
      expect(true).to.be.true;
    } catch (error) {
      expect.fail('job threw an exception: ' + error.message);
    }
  });
});
```

### Cleanup Pattern

```javascript
const clearMockData = async () => {
  await TransitAlert.query().delete().whereIn('event_id', alertIds);
  await TransitAlertRoute.query().delete().whereIn('event_id', alertIds);
  await BusRouteFavorite.query().delete().whereIn('user_id', testUserIds);
  await Reservations.query().delete().whereIn('id', reservationIds);
  await TripDetail.query().delete().whereIn('trip_detail_uuid', tripDetailUuids);
  await TransitAlertNotificationQueue.query().delete().whereIn('user_id', testUserIds);
  await UserConfig.query().delete().whereIn('user_id', testUserIds);
};

after(async () => {
  // Clear all testing notifications
  await Notification.query()
    .delete()
    .where('started_on', '>=', testUptime.toISOString())
    .whereIn('notification_type', [
      NotificationType.OngoingAlert,
      NotificationType.ClearAlert,
    ]);
});
```

This comprehensive test suite ensures the transit alert notification system correctly identifies affected users, respects notification preferences, avoids duplicate notifications, and delivers timely alerts for both ongoing incidents and incident resolutions across the complex multi-modal transit network.