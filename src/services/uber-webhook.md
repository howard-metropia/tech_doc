# uber-webhook.js Documentation

## 🔍 Quick Summary (TL;DR)

Webhook handler service for processing Uber ride status updates, receipts, and trip lifecycle events with signature verification and comprehensive state management.

**Keywords:** Uber webhook | ride status | receipt processing | trip lifecycle | signature verification | refund handling | incentive processing | notification system

**Primary Use Cases:**
- Process real-time ride status updates
- Handle receipt and fare reconciliation
- Manage trip state transitions and notifications

**Compatibility:** Node.js 14+, Objection.js ORM, Redis locking

## ❓ Common Questions Quick Index

- [How does webhook signature verification work?](#detailed-code-analysis)
- [What trip statuses are supported?](#technical-specifications)
- [How are refunds processed?](#detailed-code-analysis)
- [What notifications are sent to users?](#functionality-overview)
- [How to handle duplicate webhook events?](#important-notes)
- [What happens when a driver cancels?](#detailed-code-analysis)
- [How is fare reconciliation handled?](#output-examples)
- [How to troubleshoot missing webhooks?](#important-notes)

## 📋 Functionality Overview

**Non-technical explanation:** This service is like a real-time messenger between Uber and your app. When something happens with a ride (driver accepts, arrives, completes trip), Uber sends updates to this service, which then updates your app's database and notifies the user about what's happening with their ride.

**Technical explanation:** HMAC-based webhook handler that processes Uber's real-time events including trip status changes and receipt availability. Implements idempotent processing, distributed locking, comprehensive state management, and automated fare reconciliation with refund capabilities.

**Business value:** Provides real-time ride tracking, accurate fare processing, automated refund handling, and timely user notifications, ensuring transparency and reliability in the ridehail experience.

**System context:** Critical component of the ridehail ecosystem, interfacing with payment services, notification system, and incentive processing to maintain accurate trip state across the platform.

## 🔧 Technical Specifications

- **File:** uber-webhook.js
- **Path:** /src/services/uber-webhook.js
- **Type:** Webhook handler service
- **Size:** ~20KB
- **Complexity:** High

**Dependencies:**
- `crypto` - HMAC signature verification
- `moment-timezone` - Time handling
- `@maas/services` - Slack notifications
- Multiple models - Database operations
- Redis - Distributed locking

**Webhook Types:**
- `trips.status_changed` - Trip status updates
- `trips.receipt_ready` - Receipt availability
- `health.ping` - Health check

**Trip Statuses:**
- processing, accepted, arriving, in_progress
- completed, rider_canceled, driver_canceled
- no_drivers_available, driver_redispatched

## 📝 Detailed Code Analysis

**Signature Verification:**
```javascript
HMAC-SHA256(clientSecret, requestBody) === x-uber-signature
```

**State Transition Rules:**
- Each status has specific allowed previous states
- Invalid transitions are ignored
- State updates include relevant metadata

**Update Strategies:**
- **accepted**: Driver info, vehicle details, ETAs
- **arriving**: Updates ETAs, maintains driver info
- **in_progress**: Adds pickup time
- **completed**: Adds dropoff time, final status
- **canceled**: Initiates refund process

**Receipt Processing:**
1. Acquire distributed lock
2. Fetch receipt details
3. Calculate actual fare
4. Reconcile with estimated fare
5. Process refunds if needed
6. Update trip records

**Notification Flow:**
- Status-specific messages
- Multi-language support
- Push notification integration

## 🚀 Usage Methods

**Webhook Endpoint Setup:**
```javascript
// In controller
app.post('/uber/webhook', async (ctx) => {
  const isValid = checkSignature(ctx.headers, ctx.request.body);
  if (!isValid) {
    ctx.status = 401;
    return;
  }
  
  const validated = await inputValidation(ctx.request.body);
  await processing(validated);
  ctx.status = 200;
});
```

**Manual Status Update:**
```javascript
// Process specific status update
await updateRideRequest('request_123', 'completed');
```

**Receipt Processing:**
```javascript
// Process receipt manually
await processReceipt('request_123');
```

**Fare Audit:**
```javascript
// Audit fare discrepancies
await auditFare('request_123', {
  estimatedFare: 15.50,
  actualFare: 18.25,
  tripStatus: 'completed',
  tripId: 'trip_456'
});
```

## 📊 Output Examples

**Status Update Event:**
```javascript
{
  event_id: "evt_123",
  event_type: "trips.status_changed",
  event_time: 1234567890,
  meta: {
    status: "accepted",
    resource_id: "request_123"
  },
  resource_href: "https://api.uber.com/v1/guests/trips/request_123"
}
```

**Database Updates (Accepted):**
```javascript
{
  driver_name: "John Doe",
  driver_image_url: "https://...",
  vehicle_color: "Black",
  vehicle_lpn: "ABC123",
  vehicle_make: "Toyota",
  vehicle_model: "Camry",
  pickup_eta: "2024-01-01T12:00:00Z",
  dropoff_eta: "2024-01-01T12:30:00Z",
  trip_status: "accepted"
}
```

**User Notification:**
```javascript
{
  type: "RIDEHAIL_TRIP",
  title: "",
  message: "Uber has found a driver for you.",
  data: {
    trip_id: "trip_456"
  }
}
```

## ⚠️ Important Notes

**Security Considerations:**
- Always verify webhook signatures
- Use distributed locks for concurrent requests
- Sanitize data before database storage

**Common Issues:**
1. **Duplicate events:** Check existing status before update
2. **Out-of-order events:** Validate state transitions
3. **Missing receipts:** Implement retry mechanism

**Performance Tips:**
- Use Redis locks with appropriate TTL
- Batch notification sending
- Implement webhook event logging

**Error Handling:**
- Graceful degradation on lock failures
- Comprehensive error logging
- Slack alerts for critical failures

## 🔗 Related File Links

**Models:**
- `/models/RidehailTrips.js` - Trip records
- `/models/UberGuestRideLogs.js` - Event logging
- `/models/Trips.js` - General trip data
- `/models/Teleworks.js` - Telework tracking

**Services:**
- `/services/ridehail.js` - Refund processing
- `/services/uber-guest-ride.js` - API client
- `/services/incentive.js` - Rewards processing

## 📈 Use Cases

**Real-time Tracking:**
- Live driver location updates
- ETA adjustments
- Trip progress monitoring

**Financial Operations:**
- Fare reconciliation
- Automated refunds
- Incentive calculations

**User Communication:**
- Status change notifications
- Completion surveys
- Cancellation alerts

## 🛠️ Improvement Suggestions

**Reliability Enhancements:**
- Implement webhook retry queue
- Add circuit breaker for Uber API
- Create webhook replay mechanism

**Performance Optimization:**
- Cache frequently accessed trip data
- Implement bulk notification sending
- Optimize database queries

**Monitoring:**
- Add webhook processing metrics
- Track state transition timings
- Monitor fare discrepancy rates

## 🏷️ Document Tags

**Keywords:** Uber webhook | ridehail | trip status | receipt processing | fare reconciliation | refund | notification | HMAC | signature verification | state management | distributed locking

**Technical Tags:** #webhook #uber-integration #state-machine #notification #payment

**Target Roles:** Backend Developer (Senior), Integration Engineer, DevOps

**Difficulty Level:** ⭐⭐⭐⭐ (Complex state management and integration)

**Maintenance Level:** High (External API dependencies)

**Business Criticality:** Critical (Real-time trip tracking and payments)

**Related Topics:** Webhook security, State machines, Distributed systems, Payment processing