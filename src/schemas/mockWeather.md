# Mock Weather Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates weather alert and forecast management for testing/simulation
- **Validation Library:** Joi
- **Related Controller:** mockWeather controller

## 🔧 Schema Structure
```javascript
{
  postAlert: { data: { startAt, endAt, impactedArea } },
  getAlert: { id: string },
  putAlert: { data: { startAt, endAt, impactedArea } },
  deleteAlert: { id: string },
  getForecast: { gridId: number },
  putForecast: { id, windSpeed, windGust, rain, snow, temperatures },
  findGridByCoordinates: { lat: number, lng: number }
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| startAt | string | Yes | - | Alert start time |
| endAt | string | Yes | - | Alert end time |
| impactedArea | array | Yes | Numbers ≥ 1 | Affected grid areas |
| id | string | Yes | - | Alert/forecast identifier |
| gridId | number | Yes | - | Weather grid identifier |
| windSpeed | number | No | - | Wind speed value |
| windGust | number | No | - | Wind gust value |
| rain | number | No | - | Rainfall amount |
| snow | number | No | - | Snowfall amount |
| lowTemperature | number | No | - | Minimum temperature |
| highTemperature | number | No | - | Maximum temperature |
| lat | number | Yes | - | Latitude coordinate |
| lng | number | Yes | - | Longitude coordinate |

## 💡 Usage Example
```javascript
// Create weather alert
{
  "data": {
    "startAt": "2024-01-15T08:00:00Z",
    "endAt": "2024-01-15T18:00:00Z",
    "impactedArea": [1, 5, 12, 23]
  }
}

// Update weather forecast
{
  "id": "forecast_123",
  "windSpeed": 15.5,
  "rain": 2.3,
  "lowTemperature": 10,
  "highTemperature": 25
}

// Find grid by coordinates
{
  "lat": 37.7749,
  "lng": -122.4194
}
```

## ⚠️ Important Validations
- Alert times are required string fields (likely ISO format)
- Impacted areas must be positive integers (grid IDs)
- Weather parameters are optional for forecast updates
- Coordinates required for grid lookup operations
- ID fields are strings for alert/forecast identification
- Alert data wrapped in 'data' object for POST/PUT operations

## 🏷️ Tags
**Keywords:** weather, alerts, forecasts, simulation, testing, grids
**Category:** #schema #validation #joi #mockweather