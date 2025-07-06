# TSP API Weather Controller Documentation

## 🔍 Quick Summary (TL;DR)
The weather controller provides AI-powered weather alerts and navigation warnings for trip planning, integrating real-time weather data, critical alerts, and construction information with OpenAI for intelligent, contextual notifications.

**Keywords:** weather-alerts | ai-weather | navigation-warnings | critical-weather | trip-planning | openai-integration | weather-ai | route-weather

**Primary use cases:** Generating intelligent weather alerts for trips, providing voice navigation warnings, testing weather messaging systems, integrating construction and weather data

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, OpenAI API, weather data services, MongoDB

## ❓ Common Questions Quick Index
- **Q: How are weather alerts generated?** → AI processes weather data with route context for intelligent messages
- **Q: What triggers critical alerts?** → Severe weather events from official weather services
- **Q: How is AI used?** → OpenAI generates contextual weather messages for trip planning and navigation
- **Q: Are construction alerts included?** → Yes, construction data is merged with weather information
- **Q: What languages are supported?** → Multi-language support via locale-based AI messaging
- **Q: How far ahead are alerts provided?** → Up to 72 hours (3 days) in advance

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as an **intelligent weather advisor** for your trips. Instead of just telling you "it's going to rain," it uses AI to understand your specific journey and tells you things like "expect heavy rain during your drive to downtown around 3 PM - consider leaving 15 minutes early." It combines official weather warnings, construction updates, and your route details to give you personalized, actionable advice.

**Technical explanation:** 
A sophisticated Koa.js controller that leverages OpenAI to generate contextual weather alerts by processing multiple data sources including weather grids, critical weather events, and construction zones. It decodes route polylines, performs spatiotemporal analysis, and generates intelligent notifications optimized for different timing contexts (trip planning vs. pre-navigation).

**Business value explanation:**
Critical for transportation safety and user experience optimization. Reduces weather-related accidents and delays through proactive AI-powered warnings, improves trip planning accuracy, and enhances user engagement through personalized, contextual alerts that help users make informed transportation decisions.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/weather.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** AI-Powered Weather Intelligence Controller
- **File Size:** ~26 KB
- **Complexity Score:** ⭐⭐⭐⭐⭐ (Very High - Multi-source data integration, AI processing, complex logic)

**Dependencies:**
- `@maas/core/log`: Logging infrastructure (**Critical**)
- `@koa/router`: HTTP routing framework (**Critical**)
- `@maas/core/response`: Standardized response formatting (**High**)
- `@app/src/services/weather`: Core weather data processing (**Critical**)
- `@app/src/services/constructionZone`: Construction data integration (**High**)
- `@app/src/helpers/ai-log`: AI interaction logging (**High**)
- `@app/src/helpers/pd-debug-module`: Debug mode functionality (**High**)
- `moment-timezone`: Advanced date/time handling (**Critical**)
- `@app/src/services/hereMapPolylines`: Route polyline decoding (**Critical**)

## 📝 Detailed Code Analysis

### Weather Alerts Endpoint (`POST /weather_alerts`)

**Purpose:** Generates AI-powered weather alerts for trip planning with contextual intelligence

**Processing Flow:**
1. **Input Validation:** Validates timing and route parameters
2. **Debug Mode Check:** Returns empty results for debug users
3. **Route Processing:** Decodes polylines and filters routes within 72-hour window
4. **Data Aggregation:** Fetches weather grids and critical events
5. **AI Processing:** Generates contextual messages based on alert types
6. **Response Assembly:** Returns structured alerts with expiration times

**Route Polyline Decoding:**
```javascript
routes.forEach((route) => {
  const differenceInHours = moment(route.departure_time * 1000).diff(nowTime, 'hours');
  if (differenceInHours < 72) {
    const decodeRoutes = [];
    route.polyline.forEach((line) => {
      try {
        coordinates = poly.decode(line).polyline;
        decodeRoutes.push(transToGEOJson(coordinates));
      } catch (err) {
        logger.warn(`decode here polyline error of route id: ${route.id}`);
      }
    });
    route.decodeRoutes = decodeRoutes;
  }
});
```

**AI Message Generation:**
```javascript
const message = await weather.getAIMessage(
  weatherInfos,
  language,
  tripInfo,
  timing
);

aiLogModule.logAIToDB(feature, api, model, message.msg, message.prompt, parameters, 
  nowTime.format('YYYY-MM-DD HH:mm:ss'));
```

### Navigation Alerts Endpoint (`POST /navigation_alerts`)

**Purpose:** Provides real-time voice navigation warnings with construction integration

**Enhanced Features:**
- Construction zone integration
- Voice-optimized messaging
- Real-time weather updates
- Multi-modal alert handling

**Construction Integration:**
```javascript
const constructionResult = await mergeAllConstructionEvents(allRoutes, 'other');

result.forEach(r1 => {
  constructionResult.forEach(r3 => {
    if (r3.id === r1.id) {
      r1.constructionEvents = Object.values(r3.construction_list);
    }
  });
});
```

### Testing Endpoints

**Trip-Based Testing (`POST /weather_testing_message/trip-based`):**
- Simulates weather events for specific routes
- Supports different timing modes
- Processes custom event scenarios

**Location-Based Testing (`POST /weather_testing_message/location-based`):**
- Tests location-specific weather alerts
- Supports push notification testing
- Validates AI message generation

## 🚀 Usage Methods

### Get Weather Alerts for Trip Planning
```bash
curl -X POST "https://api.tsp.example.com/api/v2/weather_alerts" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "timing": "trip_planning",
    "routes": [
      {
        "id": "route_001",
        "departure_time": 1719331200,
        "destination_name": "Downtown Office",
        "travel_mode": 1,
        "polyline": ["encoded_polyline_string"]
      }
    ]
  }'
```

### Get Navigation Alerts
```bash
curl -X POST "https://api.tsp.example.com/api/v2/navigation_alerts" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "routes": [
      {
        "id": "route_001",
        "departure_time": 1719331200,
        "destination_name": "Airport",
        "travel_mode": 1,
        "polyline": ["encoded_polyline_string"]
      }
    ]
  }'
```

### Test Weather Messaging (Trip-Based)
```bash
curl -X POST "https://api.tsp.example.com/api/v2/weather_testing_message/trip-based" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "api_mode": "trip_planning",
    "current_time": "2024-06-25T10:00:00Z",
    "routes": [
      {
        "id": "test_001",
        "language": "en",
        "departure_time": "2024-06-25T14:00:00Z",
        "destination_name": "Test Destination",
        "travel_mode": 1,
        "events": [
          {
            "event_type": "critical",
            "event_title": "Severe Thunderstorm",
            "event_description": "Heavy rain and strong winds expected",
            "event_instruction": "Avoid unnecessary travel",
            "event_location": "Downtown Area",
            "event_time": "2024-06-25T13:30:00Z"
          }
        ]
      }
    ]
  }'
```

### JavaScript Client Example
```javascript
class WeatherAlertManager {
  constructor(authToken, userId) {
    this.authToken = authToken;
    this.userId = userId;
    this.baseHeaders = {
      'Authorization': `Bearer ${authToken}`,
      'userid': userId,
      'Content-Type': 'application/json'
    };
  }

  async getWeatherAlerts(routes, timing = 'trip_planning') {
    try {
      const response = await fetch('/api/v2/weather_alerts', {
        method: 'POST',
        headers: this.baseHeaders,
        body: JSON.stringify({
          timing: timing,
          routes: routes
        })
      });
      
      const result = await response.json();
      
      if (result.result === 'success') {
        console.log(`Generated ${result.data.list.length} weather alerts`);
        return result.data.list;
      } else {
        console.error('Weather alerts failed:', result.error);
        throw new Error(result.error);
      }
    } catch (error) {
      console.error('Weather alerts error:', error);
      throw error;
    }
  }

  async getNavigationAlerts(routes) {
    try {
      const response = await fetch('/api/v2/navigation_alerts', {
        method: 'POST',
        headers: this.baseHeaders,
        body: JSON.stringify({
          routes: routes
        })
      });
      
      const result = await response.json();
      
      if (result.result === 'success') {
        const alertsWithSound = result.data.list.filter(alert => 
          alert.sound_description && alert.sound_description.length > 0
        );
        console.log(`Generated ${alertsWithSound.length} voice navigation alerts`);
        return result.data.list;
      } else {
        console.error('Navigation alerts failed:', result.error);
        throw new Error(result.error);
      }
    } catch (error) {
      console.error('Navigation alerts error:', error);
      throw error;
    }
  }
}

// Usage examples
const weatherManager = new WeatherAlertManager(authToken, userId);

const routes = [
  {
    id: 'route_001',
    departure_time: Math.floor(Date.now() / 1000) + 3600, // 1 hour from now
    destination_name: 'Office',
    travel_mode: 1,
    polyline: ['encoded_polyline_here']
  }
];

// Get trip planning alerts
weatherManager.getWeatherAlerts(routes, 'trip_planning');

// Get navigation alerts
weatherManager.getNavigationAlerts(routes);
```

## 📊 Output Examples

### Weather Alert Response (Trip Planning)
```json
{
  "result": "success",
  "data": {
    "list": [
      {
        "id": "route_001",
        "title": "Weather Alert",
        "info_url": "https://weather.gov/rain",
        "description": "Heavy rain is expected during your trip to Downtown Office at 2:00 PM. The rainfall may cause reduced visibility and slippery roads. Consider departing 15 minutes earlier to allow extra travel time, and ensure your vehicle's windshield wipers are functioning properly.",
        "sound_description": [],
        "last_expire_time": 1719342000
      }
    ]
  }
}
```

### Navigation Alert Response
```json
{
  "result": "success",
  "data": {
    "list": [
      {
        "id": "route_001",
        "sound_description": [
          "Weather alert: Heavy rain ahead on your route to the airport.",
          "Reduce speed and increase following distance.",
          "Construction zone in 2 miles - expect delays."
        ],
        "last_expire_time": 1719342000
      }
    ]
  }
}
```

### Critical Weather Alert
```json
{
  "result": "success",
  "data": {
    "list": [
      {
        "id": "route_001",
        "title": "Severe Thunderstorm",
        "info_url": "https://weather.gov/thunderstorm",
        "description": "A severe thunderstorm warning is in effect for your route to Downtown Office. The storm includes damaging winds up to 60 mph and quarter-size hail. Consider postponing your trip until conditions improve, expected around 4:00 PM.",
        "sound_description": [],
        "last_expire_time": 1719342000
      }
    ]
  }
}
```

### Test Messaging Response
```json
{
  "result": "success",
  "data": {
    "list": [
      {
        "id": "test_001",
        "alert_message": {
          "msg": "A severe thunderstorm is forecasted for your route through Downtown Area. Heavy rain and strong winds are expected to impact travel conditions. Please avoid unnecessary travel during this time.",
          "prompt": "Generate a weather alert message for a trip...",
          "output": ["Severe weather alert", "Heavy thunderstorm conditions ahead"]
        }
      }
    ]
  }
}
```

## ⚠️ Important Notes

### AI Integration
- **OpenAI Model:** Uses configured AI model for message generation
- **Context Awareness:** AI considers trip details, timing, and weather severity
- **Language Support:** Multi-language message generation
- **Performance Tracking:** Logs AI execution time and parameters
- **Cost Optimization:** Intelligent caching and request batching

### Weather Data Sources
- **Grid-Based Weather:** Spatial weather data for route coverage
- **Critical Alerts:** Official weather service warnings
- **Construction Integration:** Real-time construction zone data
- **Time Boundaries:** 72-hour forecast window
- **Geographic Coverage:** Route-specific weather analysis

### Message Types and Context

**Trip Planning (`timing: "trip_planning"`):**
- Detailed descriptive messages
- Actionable recommendations
- Time-sensitive advice
- Visual information URLs

**Pre-Navigation (`timing: "pre_navigation"`):**
- Voice-optimized messages
- Concise safety warnings
- Real-time conditions
- Construction alerts

### Debug Mode Features
- **Debug Users:** Returns empty alerts for testing users
- **Development Testing:** Controlled testing environments
- **Data Validation:** Prevents pollution of production analytics
- **Feature Flags:** Configurable debug behaviors

### Performance Considerations
- **Route Filtering:** Only processes routes within 72 hours
- **Polyline Decoding:** Efficient HERE Maps polyline processing
- **Parallel Processing:** Concurrent route analysis
- **AI Optimization:** Batched AI requests where possible
- **Caching Strategy:** Weather data caching for performance

### Data Quality and Monitoring
- **AI Logging:** All AI interactions logged for analysis
- **Performance Metrics:** Execution time tracking
- **Error Handling:** Graceful degradation for missing data
- **Accuracy Validation:** Weather data quality checks

### Alert Categories
- **Weather Events:** Rain, snow, ice, wind, temperature
- **Critical Alerts:** Severe weather warnings
- **Construction Zones:** Road work and closures
- **Mixed Scenarios:** Combined weather and construction
- **Severity Levels:** Category-based severity classification

### Expiration Management
- **Dynamic Expiration:** 3-hour alert lifespans
- **Update Cycles:** Regular refresh intervals
- **Time Zone Handling:** Proper timezone conversions
- **Stale Data Prevention:** Automatic alert expiration

## 🔗 Related File Links

- **Weather Service:** `allrepo/connectsmart/tsp-api/src/services/weather.js`
- **Construction Service:** `allrepo/connectsmart/tsp-api/src/services/constructionZone.js`
- **AI Logging:** `allrepo/connectsmart/tsp-api/src/helpers/ai-log.js`
- **Polyline Decoder:** `allrepo/connectsmart/tsp-api/src/services/hereMapPolylines.js`
- **Input Validation:** `allrepo/connectsmart/tsp-api/src/schemas/weather.js`
- **Notification Helper:** `allrepo/connectsmart/tsp-api/src/helpers/send-notification.js`
- **Defines:** `allrepo/connectsmart/tsp-api/src/static/defines.js`

---
*This controller provides intelligent, AI-powered weather alerting essential for safe and informed transportation decisions.*