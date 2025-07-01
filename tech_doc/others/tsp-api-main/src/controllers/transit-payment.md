# TSP API Transit Payment Controller Documentation

## 🔍 Quick Summary (TL;DR)
The transit payment controller handles transit pass usage and activation for public transportation systems, enabling digital transit pass redemption and validation.

**Keywords:** transit-payment | pass-usage | transit-passes | public-transport | fare-validation | digital-ticketing | transit-activation | mobile-passes

**Primary use cases:** Activating transit passes, validating pass usage, processing transit fare redemption, managing digital transit tickets

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, transit payment systems

## ❓ Common Questions Quick Index
- **Q: What is pass usage?** → Activating/redeeming transit passes for travel
- **Q: Is authentication required?** → Yes, JWT authentication with user context
- **Q: How is timezone handled?** → Defaults to America/Chicago, can be overridden via header
- **Q: What data is validated?** → Pass details, user ID, and timezone information
- **Q: How does pass activation work?** → Processed through transit-payment service
- **Q: Are multiple pass types supported?** → Yes, based on service implementation

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **digital transit card scanner** on your phone. When you need to use your transit pass to ride the bus or train, this controller handles "tapping" your digital pass, just like you would tap a physical card at a transit station. It validates that you have a valid pass and records your usage for proper fare collection.

**Technical explanation:** 
A minimal Koa.js REST controller that processes transit pass usage requests. It validates pass activation data, handles user authentication and timezone context, then delegates to the transit payment service for actual pass processing and fare system integration.

**Business value explanation:**
Enables contactless transit fare collection through mobile devices, reducing physical infrastructure costs while improving user convenience. Supports digital transformation of public transit systems and provides real-time fare validation data for transit agencies.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/transit-payment.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** Transit Payment Controller
- **File Size:** ~0.6 KB
- **Complexity Score:** ⭐ (Low - Single endpoint with validation and service delegation)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `@app/src/middlewares/auth`: JWT authentication (**Critical**)
- `@maas/core/response`: Standardized response formatting (**High**)
- `@app/src/schemas/transitPayment`: Input validation schemas (**Critical**)
- `@app/src/services/transit-payment`: Core transit payment service (**Critical**)

## 📝 Detailed Code Analysis

### Pass Use Endpoint (`POST /transit_payment/pass_use`)

**Purpose:** Processes transit pass usage for fare validation and activation

**Processing Flow:**
1. **Authentication:** JWT validation via auth middleware
2. **Context Extraction:** Gets user ID and timezone from headers
3. **Input Preparation:** Merges request body with user context
4. **Validation:** Validates complete input against schema
5. **Service Processing:** Delegates to transit payment service
6. **Response:** Returns success with service result

**Input Processing:**
```javascript
const { userid: userId } = ctx.request.header;
const zone = ctx.request.header.zone ?? 'America/Chicago';
const input = { ...ctx.request.body, userId, zone };
```

**Validation and Service Call:**
```javascript
const data = await inputValidator.passUse.validateAsync(input);
const result = await passUse(ctx, data);
```

### Data Flow Architecture
- **Headers → Context:** User ID and timezone extraction
- **Body → Validation:** Pass details and payment information
- **Service → Processing:** Actual fare system integration
- **Response → Client:** Success confirmation or error details

## 🚀 Usage Methods

### Basic Pass Usage
```bash
curl -X POST "https://api.tsp.example.com/api/v2/transit_payment/pass_use" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "pass_id": "pass_67890",
    "pass_type": "day_pass",
    "transit_agency": "metro_transit",
    "route_id": "route_101"
  }'
```

### Pass Usage with Custom Timezone
```bash
curl -X POST "https://api.tsp.example.com/api/v2/transit_payment/pass_use" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "zone: America/New_York" \
  -H "Content-Type: application/json" \
  -d '{
    "pass_id": "pass_67890",
    "pass_type": "monthly_unlimited",
    "station_id": "station_grand_central",
    "entry_time": "2024-06-25T08:30:00Z"
  }'
```

### Multi-Ride Pass Usage
```bash
curl -X POST "https://api.tsp.example.com/api/v2/transit_payment/pass_use" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "pass_id": "pass_67890",
    "pass_type": "10_ride_pass",
    "vehicle_id": "bus_2043",
    "fare_zone": "zone_A",
    "boarding_location": {
      "lat": 37.7749,
      "lng": -122.4194,
      "stop_id": "stop_123"
    }
  }'
```

### JavaScript Client Example
```javascript
async function useTransitPass(authToken, userId, passData, timezone = null) {
  const headers = {
    'Authorization': `Bearer ${authToken}`,
    'userid': userId,
    'Content-Type': 'application/json'
  };
  
  if (timezone) {
    headers['zone'] = timezone;
  }

  try {
    const response = await fetch('/api/v2/transit_payment/pass_use', {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(passData)
    });
    
    const result = await response.json();
    
    if (result.result === 'success') {
      console.log('Pass activated successfully:', result.data);
      return result.data;
    } else {
      console.error('Pass activation failed:', result.error);
      throw new Error(result.error);
    }
  } catch (error) {
    console.error('Transit pass usage error:', error);
    throw error;
  }
}

// Usage examples
useTransitPass(token, 'usr_12345', {
  pass_id: 'pass_67890',
  pass_type: 'single_ride',
  route_id: 'bus_route_42'
});

useTransitPass(token, 'usr_12345', {
  pass_id: 'pass_67890',
  pass_type: 'weekly_pass',
  station_id: 'metro_downtown'
}, 'America/Los_Angeles');
```

## 📊 Output Examples

### Successful Pass Usage
```json
{
  "result": "success",
  "data": {
    "transaction_id": "txn_abc123456",
    "pass_id": "pass_67890",
    "usage_timestamp": "2024-06-25T08:30:00Z",
    "remaining_balance": 8.50,
    "remaining_rides": 9,
    "expires_at": "2024-06-30T23:59:59Z",
    "route_info": {
      "route_id": "route_101",
      "route_name": "Downtown Express",
      "fare_amount": 2.50
    }
  }
}
```

### Monthly Pass Usage
```json
{
  "result": "success",
  "data": {
    "transaction_id": "txn_def789012",
    "pass_id": "pass_67890",
    "pass_type": "monthly_unlimited",
    "usage_timestamp": "2024-06-25T14:15:00Z",
    "validity_period": {
      "start": "2024-06-01T00:00:00Z",
      "end": "2024-06-30T23:59:59Z"
    },
    "station_info": {
      "station_id": "station_union",
      "station_name": "Union Station",
      "zone": "A"
    }
  }
}
```

### Pass Validation Error
```json
{
  "error": "ValidationError",
  "message": "Invalid pass data",
  "details": [
    {
      "field": "pass_id",
      "message": "pass_id is required"
    },
    {
      "field": "pass_type",
      "message": "pass_type must be one of: single_ride, day_pass, weekly_pass, monthly_pass"
    }
  ]
}
```

### Insufficient Balance Error
```json
{
  "error": "INSUFFICIENT_PASS_BALANCE",
  "message": "Pass has insufficient balance for this fare",
  "data": {
    "current_balance": 1.25,
    "required_fare": 2.50,
    "pass_id": "pass_67890"
  }
}
```

### Expired Pass Error
```json
{
  "error": "PASS_EXPIRED",
  "message": "Transit pass has expired",
  "data": {
    "pass_id": "pass_67890",
    "expired_at": "2024-06-20T23:59:59Z",
    "current_time": "2024-06-25T08:30:00Z"
  }
}
```

## ⚠️ Important Notes

### Pass Types
Common transit pass types supported:
- **single_ride**: One-time use passes
- **day_pass**: Unlimited rides for one day
- **weekly_pass**: Seven-day unlimited access
- **monthly_pass**: Full month unlimited access
- **stored_value**: Pay-per-ride with balance
- **senior_discount**: Reduced fare passes
- **student_pass**: Educational institution passes

### Timezone Handling
- **Default Zone:** 'America/Chicago' if not specified
- **Header Override:** Custom timezone via 'zone' header
- **Impact:** Affects pass expiration and usage timestamps
- **Validation:** Ensures proper local time for fare calculations

### Authentication Requirements
- **JWT Token:** Required for all requests
- **User Context:** User ID extracted from headers
- **Pass Ownership:** Service validates user owns the pass
- **Security:** Prevents unauthorized pass usage

### Service Integration
- **External APIs:** May integrate with transit agency systems
- **Real-time Validation:** Checks pass status in real-time
- **Fare Calculation:** Handles complex fare structures
- **Usage Tracking:** Records all pass activations

### Error Handling
- **Validation Errors:** Input parameter validation failures
- **Authentication Errors:** Invalid or missing JWT tokens
- **Business Logic Errors:** Pass-specific validation failures
- **Service Errors:** Transit system integration failures

### Performance Considerations
- **Lightweight Controller:** Minimal processing overhead
- **Service Delegation:** Heavy lifting done in service layer
- **Caching:** Service may cache pass data for performance
- **Async Processing:** Non-blocking pass activation

### Data Privacy
- **User Association:** All pass usage tied to authenticated users
- **Location Data:** May include boarding location information
- **Audit Trail:** Maintains usage history for compliance
- **Data Retention:** Follows transit agency retention policies

## 🔗 Related File Links

- **Transit Payment Service:** `allrepo/connectsmart/tsp-api/src/services/transit-payment.js`
- **Validation Schema:** `allrepo/connectsmart/tsp-api/src/schemas/transitPayment.js`
- **Authentication:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`
- **Related Controllers:** `allrepo/connectsmart/tsp-api/src/controllers/tickets.js`

---
*This controller provides essential transit pass activation and validation functionality for digital fare collection systems.*