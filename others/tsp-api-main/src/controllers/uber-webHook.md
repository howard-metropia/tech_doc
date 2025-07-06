# TSP API Uber Webhook Controller Documentation

## 🔍 Quick Summary (TL;DR)
The Uber webhook controller processes real-time event notifications from Uber's platform, handling ride status updates, trip completions, and driver events with signature verification for security.

**Keywords:** uber-webhook | rideshare-events | uber-integration | ride-notifications | trip-status | webhook-handler | uber-api | ridehail-events

**Primary use cases:** Processing Uber ride status updates, handling trip completion events, managing driver state changes, receiving real-time rideshare notifications

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, Uber API webhooks

## ❓ Common Questions Quick Index
- **Q: What Uber events are handled?** → Ride status changes, trip updates, driver events
- **Q: How is webhook security handled?** → Signature verification using Uber's signing mechanism
- **Q: What happens if signature fails?** → Returns 401 Unauthorized error
- **Q: Is this endpoint authenticated?** → No JWT required, uses Uber signature verification
- **Q: What environments are supported?** → Production and sandbox via x-uber-environment header
- **Q: How are webhook events processed?** → Validated and delegated to processing service

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **real-time messenger from Uber** to your app. When something happens with an Uber ride - like a driver accepts a trip, arrives at pickup, starts the ride, or completes it - Uber sends an instant notification to this controller. It's like having a direct phone line to Uber that tells you exactly what's happening with rides in real-time.

**Technical explanation:** 
A secure Koa.js webhook endpoint that receives and processes real-time event notifications from Uber's platform. It implements signature verification for security, validates incoming event data, and delegates processing to specialized services for handling different types of ride-related events.

**Business value explanation:**
Essential for real-time rideshare integration, enabling immediate response to ride status changes. Provides seamless user experience by keeping ride information current, supports automated trip management, and enables integration with broader transportation platforms and user notifications.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/uber-webHook.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** Webhook Event Handler
- **File Size:** ~0.9 KB
- **Complexity Score:** ⭐⭐⭐ (Medium - Webhook security and event processing)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `@maas/core/response`: Standardized response formatting (**High**)
- `@maas/core/log`: Logging infrastructure (**High**)
- `@app/src/services/uber-webhook`: Webhook processing services (**Critical**)
- `@app/src/static/error-code`: Error code definitions (**High**)

## 📝 Detailed Code Analysis

### Uber Webhook Endpoint (`POST /`)

**Purpose:** Receives and processes Uber platform webhook events

**Security Flow:**
1. **Environment Detection:** Extracts Uber environment from headers
2. **Signature Verification:** Validates webhook authenticity using Uber's signature
3. **Authorization Check:** Rejects requests with invalid signatures
4. **Data Validation:** Validates event data structure
5. **Event Processing:** Delegates to service for actual event handling

**Signature Verification:**
```javascript
const headers = ctx.request.header;
const body = ctx.request.body;
const passed = checkSignature(headers, body);
if (!passed) {
  ctx.body = fail({
    code: ERROR_BAD_REQUEST_PARAMS,
    message: 'Unauthorized',
  });
  ctx.status = 401;
  return;
}
```

**Event Processing:**
```javascript
const data = await inputValidation(body);
await processing(data);
ctx.body = success('Webhook received successfully');
```

### Environment Handling
```javascript
const env = headers['x-uber-environment'] || null;
logger.info(`[uber-webhook] env: ${env}`);
```

## 🚀 Usage Methods

### Webhook Configuration
Configure in Uber Developer Dashboard:
- **Endpoint URL:** `https://api.tsp.example.com/api/v2/uber/webhook`
- **Events:** Select relevant ride and driver events
- **Signature verification:** Enable for security

### Testing with Uber Sandbox
```bash
# Uber sends webhooks automatically, but you can test with curl
curl -X POST "https://api.tsp.example.com/api/v2/uber/webhook" \
  -H "x-uber-environment: sandbox" \
  -H "x-uber-signature: sha256=<signature>" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "requests.status_changed",
    "event_time": "2024-06-25T14:30:00Z",
    "resource_type": "request",
    "resource_id": "request_123",
    "data": {
      "status": "driver_accepted",
      "request_id": "request_123",
      "driver": {
        "name": "John Driver",
        "phone_number": "+1234567890",
        "vehicle": {
          "make": "Toyota",
          "model": "Camry",
          "license_plate": "ABC123"
        }
      }
    }
  }'
```

### Production Webhook Example
```bash
# Production webhook from Uber
curl -X POST "https://api.tsp.example.com/api/v2/uber/webhook" \
  -H "x-uber-environment: production" \
  -H "x-uber-signature: sha256=<computed_signature>" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "requests.status_changed",
    "event_time": "2024-06-25T14:30:00Z",
    "resource_type": "request",
    "resource_id": "request_456",
    "data": {
      "status": "completed",
      "request_id": "request_456",
      "fare": {
        "amount": 15.50,
        "currency": "USD"
      },
      "trip": {
        "distance_miles": 5.2,
        "duration_minutes": 18
      }
    }
  }'
```

## 📊 Output Examples

### Successful Webhook Processing
```json
{
  "result": "success",
  "data": "Webhook received successfully"
}
```

### Signature Verification Failure
```json
{
  "result": "fail",
  "code": "ERROR_BAD_REQUEST_PARAMS",
  "message": "Unauthorized"
}
```

### Common Uber Webhook Events

**Driver Accepted Event:**
```json
{
  "event_type": "requests.status_changed",
  "event_time": "2024-06-25T14:30:00Z",
  "resource_type": "request",
  "resource_id": "request_123",
  "data": {
    "status": "driver_accepted",
    "request_id": "request_123",
    "driver": {
      "name": "John Driver",
      "phone_number": "+1234567890",
      "picture_url": "https://uber-driver-photos.s3.amazonaws.com/driver123.jpg",
      "vehicle": {
        "make": "Toyota",
        "model": "Camry",
        "license_plate": "ABC123",
        "color": "Silver"
      },
      "location": {
        "latitude": 37.7749,
        "longitude": -122.4194,
        "bearing": 180
      }
    },
    "eta": 5
  }
}
```

**Trip Completed Event:**
```json
{
  "event_type": "requests.status_changed",
  "event_time": "2024-06-25T15:15:00Z",
  "resource_type": "request",
  "resource_id": "request_123",
  "data": {
    "status": "completed",
    "request_id": "request_123",
    "fare": {
      "amount": 18.75,
      "currency": "USD",
      "breakdown": {
        "base_fare": 5.00,
        "distance": 8.25,
        "time": 3.50,
        "surge": 2.00
      }
    },
    "trip": {
      "distance_miles": 6.8,
      "duration_minutes": 22,
      "start_time": "2024-06-25T14:45:00Z",
      "end_time": "2024-06-25T15:07:00Z"
    }
  }
}
```

**Driver Arrival Event:**
```json
{
  "event_type": "requests.status_changed",
  "event_time": "2024-06-25T14:35:00Z",
  "resource_type": "request",
  "resource_id": "request_123",
  "data": {
    "status": "arriving",
    "request_id": "request_123",
    "eta": 2,
    "driver_location": {
      "latitude": 37.7849,
      "longitude": -122.4094,
      "bearing": 90
    }
  }
}
```

## ⚠️ Important Notes

### Webhook Security
- **Signature Verification:** Critical for preventing unauthorized webhook calls
- **HTTPS Required:** Webhooks must use secure connections
- **Environment Headers:** Distinguish between sandbox and production
- **Replay Protection:** Uber includes timestamp to prevent replay attacks

### Event Types
Common Uber webhook events:
- **requests.status_changed**: Ride status updates
- **requests.receipt_ready**: Trip receipt available
- **driver.status_changed**: Driver availability changes
- **requests.scheduled**: Scheduled ride events
- **requests.reminder**: Ride reminders

### Status Values
Typical ride status progression:
- **processing**: Request being matched with driver
- **driver_accepted**: Driver accepted the request
- **arriving**: Driver is en route to pickup
- **driver_arrived**: Driver arrived at pickup location
- **in_progress**: Trip is in progress
- **completed**: Trip finished successfully
- **driver_canceled**: Driver canceled the trip
- **rider_canceled**: Rider canceled the trip

### Environment Support
- **Sandbox:** Testing environment with simulated events
- **Production:** Live environment with real rides
- **Headers:** x-uber-environment indicates environment type
- **Configuration:** Different settings per environment

### Error Handling
- **401 Unauthorized:** Invalid or missing signature
- **Validation Errors:** Invalid event data structure
- **Processing Errors:** Service layer handles business logic errors
- **Logging:** All events and errors are logged for debugging

### Rate Limiting
- **Uber's Limits:** Uber may rate limit webhook deliveries
- **Retry Logic:** Uber retries failed webhook deliveries
- **Timeout Handling:** Webhook responses should be quick
- **Acknowledgment:** Always respond to acknowledge receipt

### Data Processing
- **Async Processing:** Heavy processing should be asynchronous
- **Idempotency:** Handle duplicate webhook deliveries gracefully
- **Error Recovery:** Implement proper error handling for processing failures
- **Data Storage:** Store relevant event data for audit and analysis

## 🔗 Related File Links

- **Uber Webhook Service:** `allrepo/connectsmart/tsp-api/src/services/uber-webhook.js`
- **Error Codes:** `allrepo/connectsmart/tsp-api/src/static/error-code.js`
- **Related Controllers:** `allrepo/connectsmart/tsp-api/src/controllers/ridehail.js`

---
*This controller provides critical real-time integration with Uber's platform for seamless rideshare event processing.*