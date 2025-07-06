# uber-guest-ride.js Documentation

## 🔍 Quick Summary (TL;DR)

Service module for managing Uber guest ride functionality including authentication, trip estimation, booking, and sandbox testing capabilities.

**Keywords:** Uber integration | guest rides | ridehail | trip estimation | OAuth authentication | sandbox testing | API client | ride booking | fare calculation

**Primary Use Cases:**
- Guest user ride booking without Uber account
- Trip fare estimation and ETA calculation
- Sandbox environment testing for ride flows

**Compatibility:** Node.js 14+, Redis cache, MongoDB

## ❓ Common Questions Quick Index

- [How to authenticate with Uber API?](#usage-methods)
- [How to estimate trip fare?](#usage-methods)
- [How to book a guest ride?](#usage-methods)
- [What is sandbox mode?](#detailed-code-analysis)
- [How to handle API failures?](#important-notes)
- [How to troubleshoot authentication errors?](#important-notes)
- [What are the retry mechanisms?](#detailed-code-analysis)
- [How to test ride flows in development?](#usage-methods)

## 📋 Functionality Overview

**Non-technical explanation:** This service acts as a bridge between your app and Uber, allowing users to book Uber rides without having an Uber account. It's like having a concierge who can call Uber for you, get price estimates, and handle the entire booking process on your behalf.

**Technical explanation:** OAuth2-based integration service that manages Uber API authentication, provides guest ride booking capabilities, handles trip lifecycle management, and includes sandbox environment support for testing ride flows without real drivers.

**Business value:** Enables seamless ridehail integration for users without requiring Uber accounts, expanding transportation options and improving user experience through unified booking platform.

**System context:** Core component of the ridehail module, working with payment services and trip management to provide complete ride-hailing functionality.

## 🔧 Technical Specifications

- **File:** uber-guest-ride.js
- **Path:** /src/services/uber-guest-ride.js
- **Type:** Service module
- **Size:** ~10KB
- **Complexity:** High

**Dependencies:**
- `axios` - HTTP client for API calls
- `moment-timezone` - Time handling
- `perf_hooks` - Performance monitoring
- `@maas/services` - Slack notifications
- `@maas/core/redis` - Token caching
- `@maas/core/log` - Logging

**Configuration:**
- `config.vendor.uber` - Uber API credentials
- Environment: `PROJECT_STAGE`, `PROJECT_NAME`

**Redis Keys:**
- `{stage}:uber:token` - OAuth access token
- `{stage}:uber:sandbox:runid` - Sandbox run ID
- `{stage}:uber:tx:{requestId}` - Transaction locks

## 📝 Detailed Code Analysis

**Authentication Flow:**
1. Check Redis cache for valid token
2. If expired/missing, request new token via OAuth2
3. Cache token with 24hr buffer before expiry
4. Return token for API usage

**Key Functions:**

**getUberToken(forceUpdate)**
- OAuth2 client credentials flow
- 30-day token expiration
- Automatic refresh handling
- Error alerting via Slack

**getTripEstimation(data)**
- POST to Uber ETA endpoint
- Sandbox header injection for testing
- Performance monitoring
- Request/response caching

**orderRideTrip(data)**
- Creates actual ride request
- Handles sandbox environments
- Comprehensive error tracking
- Duration logging

**Sandbox Functions:**
- `createSandboxRun()` - Initialize test environment
- `changeDriverStatus()` - Simulate driver actions

**Error Handling:**
- 3x retry mechanism for GET requests
- Slack alerts for specific HTTP codes (400, 401, 404, 429, 500)
- API payload caching for debugging

## 🚀 Usage Methods

**Basic Authentication:**
```javascript
const uberService = require('./services/uber-guest-ride');

// Get authenticated token
const token = await uberService.getUberToken();

// Force token refresh
const newToken = await uberService.getUberToken(true);
```

**Trip Estimation:**
```javascript
// Estimate fare and ETA
const estimationData = {
  pickup: {
    latitude: 37.7749,
    longitude: -122.4194
  },
  dropoff: {
    latitude: 37.7849,
    longitude: -122.4094
  }
};

const estimation = await uberService.getTripEstimation(estimationData);
// Returns: fare details, ETA, available products
```

**Booking a Ride:**
```javascript
// Book actual ride
const bookingData = {
  fare_id: 'fare_12345',
  pickup: { /* location */ },
  dropoff: { /* location */ },
  rider: { /* guest info */ }
};

const trip = await uberService.orderRideTrip(bookingData);
```

**Sandbox Testing:**
```javascript
// Create sandbox environment
const runId = await uberService.createSandboxRun(pickup, dropoff);

// Simulate driver acceptance
await uberService.changeDriverStatus('accepted', runId);

// Simulate driver arrival
await uberService.changeDriverStatus('arrived', runId);
```

## 📊 Output Examples

**Token Response:**
```javascript
{
  access_token: "Bearer eyJ0eXAiOiJKV1...",
  expires_in: 2592000, // 30 days
  token_type: "Bearer"
}
```

**Trip Estimation Response:**
```javascript
{
  fare: {
    fare_id: "d7e6c5a4-...",
    display: "$15-20",
    expires_at: "2024-01-01T12:00:00Z"
  },
  trip: {
    distance_estimate: 5.2,
    duration_estimate: 900 // seconds
  }
}
```

**Ride Booking Response:**
```javascript
{
  request_id: "b5512127-...",
  status: "processing",
  driver: null,
  eta: 5, // minutes
  surge_multiplier: 1.0
}
```

## ⚠️ Important Notes

**Security Considerations:**
- Tokens stored in Redis with encryption
- Client credentials never exposed
- Request/response logging excludes sensitive data

**Common Troubleshooting:**
1. **401 Errors:** Token expired, force refresh
2. **429 Rate Limit:** Implement exponential backoff
3. **Sandbox Issues:** Ensure run_id is valid (6hr expiry)

**Performance Tips:**
- Cache trip estimations (5min TTL)
- Reuse sandbox runs in development
- Monitor API response times

**Rate Limits:**
- Authentication: 1000/hour
- Trip operations: 10000/hour
- Respect Uber's rate limit headers

## 🔗 Related File Links

**Models:**
- `/models/UberApiPayload.js` - API request/response storage

**Controllers:**
- `/controllers/ridehail.js` - Ridehail endpoints
- `/controllers/guest.js` - Guest user management

**Related Services:**
- `/services/ridehail.js` - Multi-vendor ridehail
- `/services/wallet.js` - Payment processing

## 📈 Use Cases

**Production Usage:**
- Airport transfer bookings
- Last-mile connectivity
- Corporate guest transportation

**Development/Testing:**
- Full ride flow simulation
- Error scenario testing
- Performance benchmarking

**Analytics:**
- API usage tracking
- Error rate monitoring
- Cost optimization analysis

## 🛠️ Improvement Suggestions

**Code Optimization:**
- Implement circuit breaker pattern
- Add request queuing for rate limits
- Cache zone data for frequent lookups

**Feature Expansion:**
- Support for scheduled rides
- Multiple waypoint support
- Ride sharing options

**Monitoring:**
- Add DataDog APM integration
- Implement detailed metrics collection
- Create API health dashboard

## 🏷️ Document Tags

**Keywords:** Uber API | guest rides | ridehail integration | OAuth2 | trip booking | fare estimation | sandbox testing | API client | ride hailing | transportation | guest booking

**Technical Tags:** #service #uber-api #oauth #ridehail #integration

**Target Roles:** Backend Developer (Senior), Integration Engineer, DevOps

**Difficulty Level:** ⭐⭐⭐⭐ (Complex integration with external API)

**Maintenance Level:** High (API changes, token management)

**Business Criticality:** High (core transportation feature)

**Related Topics:** OAuth2 authentication, API integration, Ridehail services, Payment processing