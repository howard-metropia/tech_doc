# Mock Weather Events Controller

## 🔍 Quick Summary (TL;DR)
Mock weather controller provides development and testing endpoints for simulating weather alerts and forecasts in non-production environments for the TSP API system.

**Keywords:** mock weather | testing controller | weather simulation | development API | alert management | forecast testing | grid coordinates | weather events | development tools | testing utilities

**Primary Use Cases:**
- Testing weather-dependent features in development
- Simulating weather alerts for QA validation
- Creating controlled weather scenarios for feature testing
- Grid-based weather forecast simulation

**Compatibility:** Node.js 16+, Koa.js 2.x, TSP API v2

## ❓ Common Questions Quick Index
- **Q: How do I create a mock weather alert?** → [Usage Methods - Create Alert](#-usage-methods)
- **Q: Can I use this in production?** → [Technical Specifications - Environment Control](#-technical-specifications)
- **Q: How do I simulate forecasts for specific coordinates?** → [Usage Methods - Forecast Management](#-usage-methods)
- **Q: What weather alert formats are supported?** → [Output Examples - Alert Responses](#-output-examples)
- **Q: How do I find weather grid IDs?** → [Usage Methods - Grid Lookup](#-usage-methods)
- **Q: What happens if alert creation fails?** → [Output Examples - Error Responses](#-output-examples)
- **Q: How to troubleshoot 404 errors?** → [Important Notes - Troubleshooting](#-important-notes)
- **Q: What authentication is required?** → [Technical Specifications - Security](#-technical-specifications)
- **Q: How do I update existing weather data?** → [Usage Methods - Update Operations](#-usage-methods)

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a weather machine for testing - like a movie studio creating fake rain or snow for filming. Just as filmmakers need controlled weather conditions to test scenes, developers need controlled weather data to test how their transportation app behaves during storms, snow, or extreme heat. This controller acts like a weather remote control, letting developers create, modify, and remove fake weather events at will.

**Technical explanation:**
RESTful controller providing CRUD operations for mock weather alerts and forecasts. Implements environment-gated access with configuration-driven availability, using Koa.js routing patterns with validation middleware and standardized response formatting.

**Business value:** Enables comprehensive testing of weather-dependent transportation features without relying on unpredictable real weather conditions, reducing testing costs and improving feature reliability.

**System context:** Part of TSP API's testing infrastructure, supporting quality assurance for weather-sensitive mobility services like route planning, alert notifications, and service disruption management.

## 🔧 Technical Specifications

**File Information:**
- Path: `/src/controllers/mockWeatherEvents.js`
- Language: JavaScript (Node.js)
- Type: Koa.js Router Controller
- Size: ~4KB
- Complexity: Medium (conditional routing, CRUD operations)

**Dependencies:**
- `@koa/router` (^12.0.0) - HTTP routing framework
- `@maas/core/response` (custom) - Standardized API responses
- `koa-bodyparser` (^4.3.0) - Request body parsing middleware
- `config` (^3.3.8) - Configuration management

**Environment Control:**
- Disabled in production unless `weather.mockAllowed = 'true'`
- Requires `portal.projectStage !== 'production'` OR debug mode enabled
- Routes only registered when conditions met

**Security Requirements:**
- Standard TSP API authentication (JWT tokens)
- Environment-based access control
- Input validation via Joi schemas

## 📝 Detailed Code Analysis

**Main Router Configuration:**
```javascript
const router = new Router({ prefix: '/api/v2' });
// Environment check gates all route registration
if (stage !== 'production' || isDebugModeEnabled) {
  // Routes only registered if conditions met
}
```

**CRUD Operation Pattern:**
Each endpoint follows standardized pattern:
1. Input validation via schema
2. Service layer call
3. Conditional success/error response
4. Consistent error handling with MaasError

**Error Handling Mechanism:**
- Success responses: `success()` wrapper with data
- Client errors: `fail()` with 400 status
- Not found: `MaasError(404)` with descriptive messages
- Validation errors: Automatic Joi validation rejection

**Performance Characteristics:**
- Synchronous route registration (startup time)
- Async/await pattern for all operations
- No caching layer (testing data)

## 🚀 Usage Methods

**Create Weather Alert:**
```bash
POST /api/v2/mock-weather/alert
Content-Type: application/json
Authorization: Bearer <jwt-token>

{
  "title": "Severe Thunderstorm Warning",
  "description": "Heavy rain and lightning expected",
  "severity": "severe",
  "gridId": "ABC123",
  "startTime": "2024-01-15T14:00:00Z",
  "endTime": "2024-01-15T18:00:00Z"
}
```

**Get Alert by ID:**
```bash
GET /api/v2/mock-weather/alert/123
Authorization: Bearer <jwt-token>
```

**Update Existing Alert:**
```bash
PUT /api/v2/mock-weather/alert/123
Content-Type: application/json

{
  "severity": "moderate",
  "description": "Updated conditions"
}
```

**Find Weather Grid:**
```bash
GET /api/v2/mock-weather/grid?lat=40.7128&lng=-74.0060
Authorization: Bearer <jwt-token>
```

**Update Forecast:**
```bash
PUT /api/v2/mock-weather/forecast/456
Content-Type: application/json

{
  "temperature": 75,
  "conditions": "partly_cloudy",
  "precipitation": 0.1
}
```

## 📊 Output Examples

**Successful Alert Creation:**
```json
{
  "status": "success",
  "data": {
    "message": "ok",
    "id": "alert_123456"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Alert Retrieval Response:**
```json
{
  "status": "success",
  "data": {
    "id": "alert_123456",
    "title": "Severe Thunderstorm Warning",
    "severity": "severe",
    "gridId": "ABC123",
    "active": true,
    "createdAt": "2024-01-15T10:30:00Z"
  }
}
```

**Grid Lookup Response:**
```json
{
  "status": "success",
  "data": {
    "gridId": "NYC_GRID_001",
    "coordinates": [40.7128, -74.0060],
    "coverage": "manhattan_south"
  }
}
```

**Error Responses:**
```json
// 404 Not Found
{
  "status": "error",
  "code": 404,
  "message": "alert not found",
  "timestamp": "2024-01-15T10:35:00Z"
}

// 400 Bad Request
{
  "status": "error",
  "code": 400,
  "message": "failed to create mock-alert"
}
```

## ⚠️ Important Notes

**Environment Restrictions:**
- Automatically disabled in production environments
- Override with `weather.mockAllowed = 'true'` config
- Routes return 404 if not available

**Common Troubleshooting:**
- **404 on all endpoints:** Check environment stage and mockAllowed config
- **Validation errors:** Verify request body matches schema requirements
- **Alert not found:** Confirm alert ID exists and hasn't been deleted
- **Grid lookup fails:** Verify coordinates are within supported regions

**Security Considerations:**
- Only available in non-production environments by design
- Standard API authentication still required
- Input validation prevents injection attacks
- No sensitive data exposure in mock responses

**Performance Notes:**
- No rate limiting on mock endpoints
- Memory-based storage (data not persistent)
- Suitable for testing volumes only

## 🔗 Related File Links

**Service Layer:** `/src/services/mockWeather.js` - Business logic implementation
**Validation Schemas:** `/src/schemas/mockWeather.js` - Input validation rules
**Configuration:** `/config/default.js` - Environment and weather settings
**Core Response:** `@maas/core/response` - Standardized API responses
**Main Router:** `/src/app.js` - Controller registration
**Test Files:** `/test/controllers/mockWeatherEvents.test.js` (if exists)

## 📈 Use Cases

**Development Testing:**
- QA engineers simulating weather scenarios
- Developers testing alert notification systems
- Feature testing for weather-dependent routing

**Integration Testing:**
- Third-party service integration validation
- Mobile app weather feature testing
- End-to-end weather workflow testing

**Demo Scenarios:**
- Client demonstrations with controlled weather
- Training environments with predictable conditions
- Sales demos showing weather-responsive features

## 🛠️ Improvement Suggestions

**Code Optimization:**
- Add response caching for repeated grid lookups
- Implement bulk operations for multiple alerts
- Add request rate limiting for fair usage

**Feature Expansion:**
- Historical weather data simulation
- Weather pattern templates (storms, heatwaves)
- Geographic region-based alert broadcasting
- Integration with real weather data for hybrid testing

**Monitoring Improvements:**
- Usage analytics for testing patterns
- Performance metrics for response times
- Error tracking for validation failures

## 🏷️ Document Tags

**Keywords:** mock-weather, testing-controller, weather-simulation, development-api, alert-management, forecast-testing, koa-router, crud-operations, environment-gated, weather-grid, coordinates-lookup, rest-api, validation-middleware, testing-utilities

**Technical Tags:** #mock-api #weather-testing #koa-controller #development-tools #crud-endpoints #environment-control #testing-infrastructure #api-v2

**Target Roles:** QA Engineers (Intermediate), Backend Developers (Intermediate), DevOps Engineers (Beginner)

**Difficulty Level:** ⭐⭐⭐ (3/5) - Moderate complexity due to environment gating, CRUD patterns, and validation requirements

**Maintenance Level:** Low - Stable testing controller with minimal updates needed

**Business Criticality:** Medium - Essential for quality testing but not customer-facing

**Related Topics:** weather-apis, testing-frameworks, mock-services, api-development, quality-assurance, environmental-configuration