# Transit Alert Job

## Overview
Comprehensive transit alert management job that monitors ongoing and cleared transit events, identifies affected users through their favorite routes and reservations, and delivers targeted notifications about service disruptions and restorations. The job implements sophisticated filtering to prevent notification spam while ensuring critical transit information reaches affected users.

## File Location
`/src/jobs/transit-alert.js`

## Dependencies
- `@app/src/services/transitAlert` - Comprehensive transit alert service layer containing all business logic

### Transit Alert Service Functions
```javascript
const {
  searchOngoingEvents,      // Find active transit disruptions
  searchClearEvents,        // Find recently resolved transit issues  
  notifyFavoriteRoute,      // Send notifications to favorite route users
  notifyReservation,        // Send notifications to reservation holders
  fetchOngoingRouteFavorites,   // Get users with favorite routes affected by ongoing events
  fetchOngoingReservations,     // Get users with reservations affected by ongoing events
  fetchClearFavorites,          // Get users with favorite routes for cleared events
  fetchClearReservations,       // Get users with reservations for cleared events
  filterNotificationByUserConfig,  // Filter based on user notification preferences
  filterExistingNotifications,     // Prevent duplicate notifications
  NotificationType,               // Notification type constants
} = require('@app/src/services/transitAlert');
```

## Job Configuration

### Module Structure
```javascript
module.exports = {
  inputs: {},
  fn: job,  // Delegates to main job function
};
```

### Notification Types
```javascript
NotificationType.OngoingAlert  // For active disruptions
NotificationType.ClearAlert    // For resolved issues
```

## Core Workflow Architecture

### Main Job Execution Flow
```javascript
const job = async () => {
  // 1. Event Discovery Phase
  const ongoingEvents = await searchOngoingEvents();
  const clearedEvents = await searchClearEvents();

  // 2. User Impact Analysis Phase  
  const ongoingFavorites = await fetchOngoingRouteFavorites(ongoingEvents);
  const ongoingReservations = await fetchOngoingReservations(ongoingEvents);
  const clearFavorites = await fetchClearFavorites(clearedEvents);
  const clearReservations = await fetchClearReservations(clearedEvents);

  // 3. User Preference Filtering Phase
  const filteredOngoingRoutes = await filterNotificationByUserConfig(ongoingFavorites);
  const filteredOngoingReservations = await filterNotificationByUserConfig(ongoingReservations);
  const requiredClearedFavorites = await filterNotificationByUserConfig(clearFavorites);
  const requiredClearedReservations = await filterNotificationByUserConfig(clearReservations);

  // 4. Duplicate Prevention Phase
  const requiredOngoingFavorites = await filterExistingNotifications(filteredOngoingRoutes);
  const requiredOngoingReservations = await filterExistingNotifications(filteredOngoingReservations);

  // 5. Notification Delivery Phase
  await notifyFavoriteRoute(NotificationType.OngoingAlert, requiredOngoingFavorites);
  await notifyFavoriteRoute(NotificationType.ClearAlert, requiredClearedFavorites);
  await notifyReservation(NotificationType.OngoingAlert, requiredOngoingReservations);
  await notifyReservation(NotificationType.ClearAlert, requiredClearedReservations);
};
```

## Event Discovery Phase

### Ongoing Events Detection
```javascript
const ongoingEvents = await searchOngoingEvents();
```

**Ongoing Event Criteria**:
- Active transit service disruptions
- Route delays and cancellations
- Station closures and accessibility issues
- Equipment failures affecting service
- Weather-related service impacts

### Cleared Events Detection
```javascript
const clearedEvents = await searchClearEvents();
```

**Cleared Event Criteria**:
- Recently resolved service disruptions
- Restored normal service operations
- Reopened stations and routes
- Fixed equipment and infrastructure
- Ended weather-related impacts

## User Impact Analysis

### Favorite Route Analysis
```javascript
const ongoingFavorites = await fetchOngoingRouteFavorites(ongoingEvents);
const clearFavorites = await fetchClearFavorites(clearedEvents);
```

**Favorite Route Logic**:
- **User Route Preferences**: Matches events to user's saved favorite routes
- **Route-Event Correlation**: Identifies overlapping routes and affected segments
- **Impact Assessment**: Determines severity and duration of route impacts
- **Historical Patterns**: Considers user's typical travel patterns

### Reservation Impact Analysis
```javascript
const ongoingReservations = await fetchOngoingReservations(ongoingEvents);
const clearReservations = await fetchClearReservations(clearedEvents);
```

**Reservation Logic**:
- **Active Reservations**: Finds users with current or upcoming transit reservations
- **Route Matching**: Correlates reservations with affected transit services
- **Time Sensitivity**: Prioritizes notifications for imminent travel times
- **Alternative Options**: Provides information about alternate routes or services

## User Preference Filtering

### Notification Configuration Filtering
```javascript
const filteredOngoingRoutes = await filterNotificationByUserConfig(ongoingFavorites);
const filteredOngoingReservations = await filterNotificationByUserConfig(ongoingReservations);
const requiredClearedFavorites = await filterNotificationByUserConfig(clearFavorites);
const requiredClearedReservations = await filterNotificationByUserConfig(clearReservations);
```

**User Configuration Options**:
- **Transit Alerts Enabled/Disabled**: Global transit notification preference
- **Severity Threshold**: Minimum disruption level for notifications
- **Time Window**: Hours before travel time to receive alerts
- **Route Specificity**: Notifications only for specific routes vs all favorites
- **Notification Channels**: Push, SMS, email preferences

### Configuration Processing Logic
The service layer handles complex user preference logic including:
- **Quiet Hours**: Respecting user's do-not-disturb settings
- **Frequency Limits**: Preventing notification spam
- **Priority Levels**: Different handling for severe vs minor disruptions
- **Channel Preferences**: Routing notifications to preferred delivery methods

## Duplicate Prevention System

### Existing Notification Filtering
```javascript
const requiredOngoingFavorites = await filterExistingNotifications(filteredOngoingRoutes);
const requiredOngoingReservations = await filterExistingNotifications(filteredOngoingReservations);
```

**Duplicate Prevention Logic**:
- **Notification History**: Tracks previously sent notifications per user/event
- **Time Window**: Prevents duplicate notifications within specified timeframe
- **Event Changes**: Only notifies on significant event updates
- **Status Changes**: Tracks event status transitions (ongoing → resolved)

### Smart Notification Management
```javascript
// Only ongoing events need duplicate filtering
// Cleared events are inherently unique state changes
```

**Filtering Strategy**:
- **Ongoing Alerts**: Require duplicate filtering to prevent spam
- **Clear Alerts**: Don't require duplicate filtering (state change is unique)
- **Event Evolution**: Tracks how events change over time
- **User Fatigue**: Prevents over-notification of the same issue

## Notification Delivery Phase

### Favorite Route Notifications
```javascript
await notifyFavoriteRoute(NotificationType.OngoingAlert, requiredOngoingFavorites);
await notifyFavoriteRoute(NotificationType.ClearAlert, requiredClearedFavorites);
```

**Favorite Route Messaging**:
- **Route-Specific**: Tailored messages mentioning specific route names
- **Impact Details**: Duration, severity, and affected segments
- **Alternative Suggestions**: Recommended alternate routes
- **Time Estimates**: Expected resolution times when available

### Reservation Notifications
```javascript
await notifyReservation(NotificationType.OngoingAlert, requiredOngoingReservations);
await notifyReservation(NotificationType.ClearAlert, requiredClearedReservations);
```

**Reservation Messaging**:
- **Time-Sensitive**: Urgent notifications for imminent reservations
- **Cancellation Options**: Easy access to reservation modification
- **Rebooking Assistance**: Alternative time slots and routes
- **Refund Information**: Policy details for affected reservations

## Service Layer Architecture

### Comprehensive Service Integration
The job delegates all business logic to the `transitAlert` service, which provides:

- **Event Management**: Detection and categorization of transit events
- **User Matching**: Sophisticated algorithms for user-event correlation  
- **Preference Engine**: Complex user notification preference processing
- **Delivery System**: Multi-channel notification delivery infrastructure
- **Analytics**: User engagement and notification effectiveness tracking

### Service Benefits
- **Separation of Concerns**: Job focuses on orchestration, service handles logic
- **Testability**: Service functions can be tested independently
- **Reusability**: Service functions used by other components
- **Maintainability**: Business logic centralized in service layer

## Performance Characteristics

### Efficient Processing Pipeline
```javascript
// Sequential processing with minimal data transfer
const events = await searchEvents();                    // Fetch once
const userMatches = await fetchAffectedUsers(events);   // Process matches
const filtered = await applyFilters(userMatches);       // Apply preferences
await deliverNotifications(filtered);                   // Send notifications
```

**Performance Optimizations**:
- **Batch Processing**: Handles multiple events and users efficiently
- **Minimal Database Calls**: Optimized query patterns
- **Parallel Operations**: Where possible, concurrent processing
- **Memory Management**: Streams large datasets without memory issues

### Scalability Considerations
- **Event Volume**: Handles high numbers of simultaneous transit events
- **User Base**: Scales to large numbers of affected users
- **Notification Load**: Manages burst notification delivery
- **Database Performance**: Optimized for real-time event processing

## Integration Points

### Transit Data Sources
- **Real-time Feeds**: GTFS-RT feeds from transit agencies
- **Service Alerts**: Direct API connections to transit systems
- **Weather Services**: Integration with weather impact data
- **Traffic Systems**: Coordination with traffic management centers

### User Systems
- **Favorite Routes**: User preference management system
- **Reservations**: Transit booking and scheduling system
- **User Profiles**: Notification preferences and settings
- **Activity Tracking**: User behavior and pattern analysis

### Notification Infrastructure
- **Push Notifications**: Mobile app push notification system
- **SMS Gateway**: Text messaging for critical alerts
- **Email System**: Email notifications for detailed information
- **In-App Messaging**: Real-time app-based notifications

## Operational Monitoring

### Job Execution Tracking
The job provides implicit monitoring through service layer logging:
- **Event Processing**: Number of events discovered and processed
- **User Impact**: Count of affected users by category
- **Notification Delivery**: Success/failure rates for notification sending
- **Performance Metrics**: Processing time and resource utilization

### Alert Management
- **Service Health**: Monitoring of dependent transit alert services
- **Data Quality**: Validation of incoming transit event data
- **User Engagement**: Tracking of notification click-through rates
- **System Performance**: Database and service response times

## Error Handling Strategy

### Service Layer Error Management
Error handling is primarily managed by the transit alert service layer:
- **Service Availability**: Graceful handling of downstream service failures
- **Data Validation**: Robust validation of transit event data
- **User Data**: Handling of missing or invalid user preference data
- **Delivery Failures**: Retry logic for failed notification deliveries

The job itself focuses on high-level orchestration and relies on the service layer for detailed error handling and recovery mechanisms.