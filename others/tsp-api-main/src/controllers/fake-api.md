# TSP API Fake Events Controller Documentation

## 🔍 Quick Summary (TL;DR)
Testing controller that generates fake incident events and weather notifications for development and QA purposes, simulating real-world traffic incidents and weather alerts.

**Keywords:** fake-api | testing | incident-simulation | weather-alerts | development-tools | qa-testing | mock-events | notification-testing

**Primary use cases:** Development testing, QA validation, notification system testing, incident response simulation

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, AWS SQS, MongoDB

## ❓ Common Questions Quick Index
- **Q: What is this controller used for?** → Testing and development simulation of events
- **Q: How do I create a fake incident?** → [Fake Incident Creation](#fake-incident-endpoint)
- **Q: How does weather notification testing work?** → [Weather Notification Testing](#weather-notification-testing)
- **Q: What parameters are required for testing?** → [Required Parameters](#required-parameters)
- **Q: Is this safe to use in production?** → This is for development/testing only
- **Q: How does the notification system work?** → [Notification Flow](#notification-flow)

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **movie set for emergency scenarios**. Just like filmmakers create fake accidents and disasters for movies, this controller creates fake traffic incidents and weather alerts so developers can test how the app responds to emergencies without waiting for real events to happen.

**Technical explanation:** 
A development/testing controller that simulates incident events and weather notifications by creating mock data, triggering notification systems, and updating databases with test scenarios. It integrates with the same notification infrastructure used by real events.

**Business value explanation:**
Essential for quality assurance and development workflows, allowing teams to test emergency notification systems, user experience flows, and system behavior under various incident conditions without relying on unpredictable real-world events.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/fake-api.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** Development/Testing Controller
- **Complexity Score:** ⭐⭐⭐ (Medium - Event simulation and notification integration)

**Dependencies:**
- `@koa/router`, `koa-bodyparser`: HTTP framework (**Critical**)
- `mongoose`: MongoDB ODM for data persistence (**Critical**)
- `@aws-sdk/client-sqs`: AWS SQS for notification queuing (**Critical**)
- `moment-timezone`: Date/time handling (**High**)

## 📝 Detailed Code Analysis

### Fake Incident Endpoint (`POST /fake_incident_event`)
Creates simulated traffic incidents with notification triggers:

**Key Features:**
- **Geographic Simulation:** Creates incident polygons around specified coordinates
- **Location Resolution:** Uses Google Geocoding API to resolve road names
- **Notification Integration:** Triggers the same notification system as real incidents
- **Database Persistence:** Stores incident data in IncidentsEvent collection

**Flow:**
1. Validates input parameters (coordinates, timing, user_id)
2. Creates incident polygon (±0.002 degrees around coordinates)
3. Resolves location name via Google Geocoding API
4. Updates incident database with formatted incident record
5. Generates and sends notifications to affected users
6. Queues notification in IncidentEventNotificationQueue

### Weather Notification Testing (`POST /fake_weather_notification`)
Simulates weather alert notifications based on user location:

**Key Features:**
- **Location Detection:** Uses user's home and current location
- **Grid-based Alerts:** Finds weather alerts based on geographic grid system
- **Alert Processing:** Matches weather events to predefined categories
- **Notification Delivery:** Sends weather notifications through standard channels

## 🚀 Usage Methods

### Create Fake Incident
```bash
curl -X POST "https://api.tsp.example.com/api/v2/fake_incident_event" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "usr_12345",
    "event_id": "TEST001",
    "notification_type": 1,
    "lat": 29.7604,
    "lon": -95.3698,
    "start_time": "2024-06-25T10:00:00Z",
    "expires_time": "2024-06-25T12:00:00Z",
    "location": "I-45 North"
  }'
```

### Generate Weather Alert
```bash
curl -X POST "https://api.tsp.example.com/api/v2/fake_weather_notification" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "usr_12345"
  }'
```

## 📊 Output Examples

### Successful Response
```json
{
  "result": "success",
  "data": "OK"
}
```

### Validation Error
```json
{
  "error": "ERROR_BAD_REQUEST_BODY",
  "message": "Invalid input parameters",
  "code": 200
}
```

## ⚠️ Important Notes

### Development Use Only
This controller is designed for development and testing environments. It should not be exposed in production systems as it can create false notifications and incidents.

### Notification Integration
The fake events trigger the same notification pathways as real events, including:
- Push notifications to mobile devices
- Database logging
- User notification history
- Alert queuing systems

### Geographic Dependencies
- Uses Google Geocoding API for location resolution
- Relies on WeatherGridRegionCode collection for weather alerts
- Coordinates must be within supported geographic regions

### Testing Scenarios
Supports testing for:
- Incident notification delivery
- Weather alert systems
- User location-based services
- Emergency response workflows

## 🔗 Related File Links

- **Models:** `IncidentsEvent`, `WeatherCriticalAlert`, `AuthUsers`, `AppDatas`
- **Services:** `@app/src/services/googleApis`
- **Helpers:** `@app/src/helpers/send-message`
- **Schemas:** `@app/src/schemas/incident-event`

---
*This controller provides essential testing capabilities for incident and weather notification systems.*