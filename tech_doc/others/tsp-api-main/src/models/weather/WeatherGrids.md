# WeatherGrids Model

## 📋 Model Overview
- **Purpose:** Defines geographic grid system for weather data organization
- **Table/Collection:** weather_grids
- **Database Type:** MongoDB (dataset)
- **Relationships:** None defined

## 🔧 Schema Definition
- **grid_id** | **Number** | **Optional** | **Unique grid identifier**
- **latitude** | **Number** | **Optional** | **Grid center latitude**
- **longitude** | **Number** | **Optional** | **Grid center longitude**
- **geometry** | **Object** | **Optional** | **Geographic polygon boundary**
  - **type** | **String** | **Required** | **Geometry type (Polygon)**
  - **coordinates** | **Array** | **Required** | **Polygon coordinate array**

## 🔑 Key Information
- **Primary Key:** MongoDB ObjectId
- **Indexes:** geometry (2dsphere geospatial index)
- **Unique Constraints:** Not specified
- **Default Values:** None specified

## 📝 Usage Examples
```javascript
// Create weather grid
const grid = new WeatherGrids({
  grid_id: 123,
  latitude: 29.7604,
  longitude: -95.3698,
  geometry: {
    type: 'Polygon',
    coordinates: [[[-95.4, 29.7], [-95.3, 29.7], [-95.3, 29.8], [-95.4, 29.8], [-95.4, 29.7]]]
  }
});
await grid.save();

// Find grids near location
const nearbyGrids = await WeatherGrids.find({
  geometry: {
    $near: {
      $geometry: { type: 'Point', coordinates: [-95.3698, 29.7604] },
      $maxDistance: 1000
    }
  }
});
```

## 🔗 Related Models
- WeatherForecastCurrent - Related through grid_id
- Part of geographic weather system

## 📌 Important Notes
- Uses GeoJSON Polygon geometry for precise boundaries
- 2dsphere index enables efficient geospatial queries
- Grid-based system for organized weather data coverage
- Dataset database for geographic reference data

## 🏷️ Tags
**Keywords:** weather, grid, geometry, geospatial, polygon
**Category:** #model #database #weather #grid #geospatial #mongodb