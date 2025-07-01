# Static/Constants Documentation: mock-data/weather/criticalAlert.js

## 📋 File Overview
- **Purpose:** Provides mock critical weather alert data following the National Weather Service GeoJSON format for testing weather notification systems
- **Usage:** Used by weather service testing, alert processing validation, and emergency notification system development
- **Type:** Mock data / Weather alert sample / GeoJSON fixture

## 🔧 Main Exports
```javascript
module.exports = {
  '@context': ['https://geojson.org/geojson-ld/geojson-context.jsonld', ...],
  type: 'FeatureCollection',
  features: [{
    id: 'https://api.weather.gov/alerts/urn:oid:...',
    type: 'Feature',
    geometry: { type: 'Polygon', coordinates: [...] },
    properties: {
      event: 'Flood Warning(mock event, only for testing)',
      severity: 'Severe',
      urgency: 'Immediate',
      // ... complete weather alert properties
    }
  }]
};
```

## 📝 Constants Reference
| Property Category | Key Fields | Sample Values | Purpose |
|-------------------|------------|---------------|---------|
| Alert Metadata | id, event, severity, urgency | Flood Warning, Severe, Immediate | Alert classification and routing |
| Geographic Data | geometry.coordinates | Polygon boundary coordinates | Geospatial filtering and targeting |
| Timing | sent, effective, onset, expires, ends | ISO 8601 timestamps | Alert lifecycle management |
| Content | headline, description, instruction | Detailed alert information | User-facing alert content |
| Classification | category, certainty, status | Met, Observed, Actual | NWS standard categorization |
| Response Actions | response | 'Avoid' | Recommended user actions |

## 💡 Usage Examples
```javascript
// Import critical alert mock
const criticalAlert = require('./static/mock-data/weather/criticalAlert');

// Test alert processing
const alertFeature = criticalAlert.features[0];
const alertProps = alertFeature.properties;

// Severity checking
if (alertProps.severity === 'Severe' && alertProps.urgency === 'Immediate') {
  triggerCriticalNotification();
}

// Geographic boundary testing
const alertPolygon = alertFeature.geometry.coordinates[0];
const userLocation = [29.7604, -95.3698]; // lat, lng
if (isPointInPolygon(userLocation, alertPolygon)) {
  sendLocationBasedAlert();
}

// Alert timing validation
const currentTime = new Date();
const alertExpires = new Date(alertProps.expires);
if (currentTime < alertExpires) {
  processActiveAlert();
}

// Content extraction for notifications
const alertMessage = {
  title: alertProps.headline,
  body: alertProps.description,
  action: alertProps.instruction,
  response: alertProps.response // 'Avoid'
};
```

## ⚠️ Important Notes
- Event clearly marked as "(mock event, only for testing)" to prevent confusion
- Geographic coordinates represent realistic South Carolina flood zone boundaries
- Follows official National Weather Service API response structure
- Includes complete alert lifecycle timestamps for timing validation tests
- SAME (Specific Area Message Encoding) and UGC codes included for emergency broadcast compatibility
- Alert description includes realistic flood stage information and impact details

## 🏷️ Tags
**Keywords:** weather-alerts, emergency-notifications, geojson, nws-api, flood-warnings, critical-weather  
**Category:** #static #mock-data #weather #emergency-alerts #geospatial #testing