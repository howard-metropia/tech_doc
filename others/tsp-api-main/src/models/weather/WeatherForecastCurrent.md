# WeatherForecastCurrent Model

## 📋 Model Overview
- **Purpose:** Stores current weather forecast data for grid-based weather tracking
- **Table/Collection:** weather_forecast_current
- **Database Type:** MongoDB (cache)
- **Relationships:** None defined

## 🔧 Schema Definition
- **grid_id** | **Number** | **Optional** | **Weather grid identifier**
- **latitude** | **Number** | **Optional** | **Grid center latitude**
- **longitude** | **Number** | **Optional** | **Grid center longitude**
- **start_at** | **Date** | **Optional** | **Forecast start time**
- **end_at** | **Date** | **Optional** | **Forecast end time**
- **weather** | **Object** | **Optional** | **Weather data object**
- **is_impacted** | **Boolean** | **Optional** | **Weather impact flag**
- **events** | **Object** | **Optional** | **Weather events data**

## 🔑 Key Information
- **Primary Key:** MongoDB ObjectId
- **Indexes:** Not specified
- **Unique Constraints:** Not specified
- **Default Values:** is_impacted: false, events: null

## 📝 Usage Examples
```javascript
// Create weather forecast
const forecast = new WeatherForecastCurrent({
  grid_id: 123,
  latitude: 29.7604,
  longitude: -95.3698,
  start_at: new Date(),
  weather: { temperature: 75, humidity: 60 },
  is_impacted: false
});
await forecast.save();

// Find impacted weather grids
const impactedGrids = await WeatherForecastCurrent.find({ is_impacted: true });
```

## 🔗 Related Models
- WeatherGrids - Related through grid_id
- Part of weather monitoring system

## 📌 Important Notes
- Grid-based weather system for geographic regions
- Tracks weather impact on transportation
- Flexible weather and events objects for various data
- Cache database for real-time weather data

## 🏷️ Tags
**Keywords:** weather, forecast, grid, current, impact
**Category:** #model #database #weather #forecast #grid #mongodb