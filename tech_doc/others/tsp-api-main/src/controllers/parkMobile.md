# TSP API ParkMobile Controller Documentation

## 🔍 Quick Summary (TL;DR)
The ParkMobile controller integrates with ParkMobile parking services, enabling users to check parking rates, start parking sessions, set reminders, and manage ongoing parking events through the TSP platform.

**Keywords:** parkmobile | parking-integration | mobile-parking | parking-rates | parking-sessions | parking-payment | zone-based-parking | reminder-system

**Primary use cases:** Mobile parking payments, parking rate lookup, parking session management, parking reminders

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, ParkMobile API integration

## ❓ Common Questions Quick Index
- **Q: How do I check parking rates for a zone?** → [Get Rate Zone](#get-rate-zone-get-pm_rate_zone) and [Get Rate Price](#get-rate-price-get-pm_rate_price)
- **Q: How do I start a parking session?** → [Start Parking](#start-parking-post-pm_parking)
- **Q: Can I set parking reminders?** → [Set Parking Reminder](#set-parking-reminder-put-pm_parking)
- **Q: How do I view my active parking sessions?** → [List Parking Events](#list-parking-events-get-pm_parking)
- **Q: What payment methods are supported?** → Configured payment types through ParkMobile integration
- **Q: What information do I need to start parking?** → Zone price ID, license plate number, state, payment method

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **digital parking meter on your phone**. Instead of walking to a physical parking meter and feeding coins, this controller lets you pay for parking through your mobile app. You can check how much parking costs in different areas, start your parking session digitally, set reminders so you don't get a ticket, and see all your active parking sessions in one place.

**Technical explanation:** 
A Koa.js REST controller that integrates with ParkMobile's parking services API, providing rate lookup, session management, and reminder functionality. It handles zone-based pricing, payment processing, and parking event lifecycle management through standardized REST endpoints.

**Business value explanation:**
Enables seamless integration of parking payments into the broader mobility platform, reducing friction in urban transportation by allowing users to handle parking as part of their trip planning and payment workflow.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/parkMobile.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** Third-party Integration Controller
- **File Size:** ~2.3 KB
- **Complexity Score:** ⭐⭐⭐ (Medium - External API integration with payment processing)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `@maas/core/response`: Standardized response formatting (**High**)
- `@app/src/middlewares/auth`: JWT authentication middleware (**Critical**)
- `@app/src/services/parkMobile`: ParkMobile integration service (**Critical**)

## 📝 Detailed Code Analysis

### Available Endpoints

#### Get Rate Zone (`GET /pm_rate_zone`)
Retrieves parking zone information and available rates for a specific zone.

#### Get Rate Price (`GET /pm_rate_price`)
Calculates parking costs based on zone, time blocks, and duration.

#### Start Parking (`POST /pm_parking`)
Initiates a parking session with payment processing and license plate registration.

#### Set Parking Reminder (`PUT /pm_parking`)
Configures reminder alerts for active parking sessions to prevent ticket violations.

#### List Parking Events (`GET /pm_parking`)
Retrieves user's current active parking sessions and history.

### Service Integration
All endpoints delegate to the ParkMobile service layer:
- **Input Validation:** `checkInputParams()` for schema validation
- **Rate Services:** `getRateZone()`, `getRatePrice()` for pricing information
- **Session Management:** `startParking()` for payment and session creation
- **Reminder System:** `setParkingReminder()` for notification management
- **Event Tracking:** `listOnGoingParkingEvents()` for session status

## 🚀 Usage Methods

### Check Parking Rates
```bash
# Get zone information
curl -X GET "https://api.tsp.example.com/api/v1/pm_rate_zone?zone=1234" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"

# Get specific rate pricing
curl -X GET "https://api.tsp.example.com/api/v1/pm_rate_price?zone=1234&timeBlockUnit=hour&timeBlockQuantity=2&timeBlockId=tb_001" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345"
```

### Start Parking Session
```bash
curl -X POST "https://api.tsp.example.com/api/v1/pm_parking" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "price_id": "price_abc123",
    "lpn": "ABC1234",
    "lpnState": "TX",
    "payment_type": "credit_card"
  }'
```

### Set Parking Reminder
```bash
curl -X PUT "https://api.tsp.example.com/api/v1/pm_parking?id=event_123" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "alert_before": 15
  }'
```

## 📊 Output Examples

### Rate Zone Response
```json
{
  "result": "success",
  "data": {
    "zone_id": "1234",
    "zone_name": "Downtown Main Street",
    "rate_structure": "hourly",
    "max_duration": 480,
    "available_blocks": [
      {"id": "tb_001", "duration": 60, "unit": "minute"},
      {"id": "tb_002", "duration": 120, "unit": "minute"}
    ]
  }
}
```

### Rate Price Response
```json
{
  "result": "success",
  "data": {
    "zone": "1234",
    "duration": 120,
    "price": 4.50,
    "currency": "USD",
    "price_id": "price_abc123",
    "time_block": "2 hours"
  }
}
```

### Start Parking Response
```json
{
  "result": "success", 
  "data": {
    "parking_event_id": "event_xyz789",
    "status": "active",
    "start_time": "2024-06-25T14:30:00Z",
    "end_time": "2024-06-25T16:30:00Z",
    "total_cost": 4.50,
    "license_plate": "ABC1234",
    "zone": "1234"
  }
}
```

### Active Parking Events
```json
{
  "result": "success",
  "data": {
    "active_events": [
      {
        "event_id": "event_xyz789",
        "zone": "Downtown Main Street",
        "license_plate": "ABC1234",
        "start_time": "2024-06-25T14:30:00Z",
        "end_time": "2024-06-25T16:30:00Z",
        "remaining_time": 85,
        "reminder_set": true
      }
    ]
  }
}
```

## ⚠️ Important Notes

### Payment Integration
- **ParkMobile Gateway:** Integrates with ParkMobile's payment processing system
- **Payment Types:** Supports various payment methods configured in ParkMobile
- **Transaction Security:** All payment processing handled by ParkMobile's secure systems

### Zone-Based Pricing
- **Rate Structures:** Different zones have different pricing models (hourly, daily, etc.)
- **Time Blocks:** Parking sold in predefined time increments
- **Duration Limits:** Maximum parking duration varies by zone

### Reminder System
- **Notification Timing:** Users can set alerts before parking expires
- **Ticket Prevention:** Helps users avoid parking violations
- **Customizable Alerts:** Alert timing configurable per parking session

### License Plate Management
- **State Registration:** Requires both license plate number and state
- **Multiple Vehicles:** Users can register multiple license plates
- **Validation:** License plate format validation by state requirements

### Session Management
- **Real-time Status:** Active parking sessions tracked in real-time
- **Event History:** Historical parking events maintained for user records
- **Automatic Expiration:** Sessions automatically end at configured time

## 🔗 Related File Links

- **ParkMobile Service:** `allrepo/connectsmart/tsp-api/src/services/parkMobile.js`
- **Authentication:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`

---
*This controller provides comprehensive ParkMobile integration for mobile parking payments and session management.*