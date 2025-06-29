# GbfsStation Model Documentation

## 📋 Model Overview
- **Purpose:** Stores General Bikeshare Feed Specification (GBFS) station data with geospatial indexing
- **Table/Collection:** gbfs_stations
- **Database Type:** MongoDB
- **Relationships:** Standalone collection for bike-sharing station data

## 🔧 Schema Definition
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| _id | String | Yes | Primary document identifier |
| StationLocation | Object | Yes | GeoJSON Point geometry |
| StationLocation.type | String | Yes | Geometry type ('Point') |
| StationLocation.coordinates | [Number] | Yes | [longitude, latitude] array |
| * | Mixed | No | Additional GBFS fields (flexible schema) |

## 🔑 Key Information
- **Primary Key:** _id (String)
- **Indexes:** 
  - StationLocation: 2dsphere (geospatial index)
  - Default _id index
- **Unique Constraints:** _id field
- **Default Values:** None
- **Schema Options:** strict: false, autoIndex: true

## 📝 Usage Examples
```javascript
// Create a new GBFS station
const station = await GbfsStation.create({
  _id: 'station_001',
  StationLocation: {
    type: 'Point',
    coordinates: [-74.0060, 40.7128] // [longitude, latitude] - NYC
  },
  station_id: 'station_001',
  name: 'Central Park Station',
  capacity: 20,
  num_bikes_available: 15,
  num_docks_available: 5
});

// Find stations near a location (within 1000 meters)
const nearbyStations = await GbfsStation.find({
  StationLocation: {
    $near: {
      $geometry: {
        type: 'Point',
        coordinates: [-74.0060, 40.7128]
      },
      $maxDistance: 1000
    }
  }
});

// Find stations within a polygon area
const stationsInArea = await GbfsStation.find({
  StationLocation: {
    $geoWithin: {
      $geometry: {
        type: 'Polygon',
        coordinates: [[/* polygon coordinates */]]
      }
    }
  }
});
```

## 🔗 Related Models
- Independent collection for bike-sharing station data
- May integrate with trip planning and routing systems
- Used for real-time bike availability tracking

## 📌 Important Notes
- Follows GBFS (General Bikeshare Feed Specification) standard
- Geospatial 2dsphere index enables location-based queries
- Flexible schema allows storing all GBFS station fields
- Coordinates stored in GeoJSON format [longitude, latitude]
- Supports real-time station status updates
- Essential for bike-sharing integration in MaaS platform

## 🏷️ Tags
**Keywords:** gbfs, bikeshare, stations, geospatial, mongodb, location, cycling
**Category:** #model #database #geospatial #bikeshare #mongodb #transportation