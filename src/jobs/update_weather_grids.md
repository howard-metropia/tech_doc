# Job Documentation: update_weather_grids.js

## 📋 Job Overview
- **Purpose:** Updates weather grid data from CSV file into MongoDB WeatherGrids collection
- **Type:** One-time migration / Data refresh task
- **Schedule:** Manual trigger when grid data needs updating
- **Impact:** Replaces all weather grid data for geospatial weather queries

## 🔧 Technical Details
- **Dependencies:** fs, csv-parser, @maas/core/log, WeatherGrids model
- **Database Operations:** Deletes all existing grids, inserts new grid data from CSV
- **Key Operations:** CSV parsing, polygon coordinate transformation, MongoDB document creation

## 📝 Code Summary
```javascript
// Delete existing grids
await WeatherGrids.deleteMany({});

// Process CSV file
const data = await processCSV('src/static/houston_grids.csv');

// Transform and save each grid
for (const row of data) {
  const grid = new WeatherGrids({
    grid_id: parseInt(row.id),
    latitude: parseFloat(row.latitude),
    longitude: parseFloat(row.longitude),
    geometry: { type: 'Polygon', coordinates }
  });
  await grid.save();
}
```

## ⚠️ Important Notes
- Destructive operation - deletes ALL existing weather grid data first
- Requires houston_grids.csv file in src/static/ directory
- Processes polygon geometry from WKT format to GeoJSON
- Individual grid save errors are logged but don't stop processing
- No rollback mechanism - backup recommended before execution

## 📊 Example Output
```
CSV file successfully processed
Saved grid 1001
Saved grid 1002
Error saving grid 1003: Validation error
...
Weather grids updated
```

## 🏷️ Tags
**Keywords:** weather, grids, geospatial, csv-import, houston, mongodb
**Category:** #job #migration #weather #geospatial #data-refresh

---
Note: This job completely replaces weather grid data - ensure CSV file is validated before execution.