# UBikeStations Model Documentation

## 📋 Model Overview
- **Purpose:** Stores UBike (YouBike) station information with location and availability data
- **Table/Collection:** ubike_stations
- **Database Type:** MongoDB
- **Relationships:** Self-contained station data with geospatial indexing

## 🔧 Schema Definition
- **Field Name** | **Type** | **Required** | **Description**
- _id | Number | No | Custom numeric ID
- StationUID | String | No | Unique station identifier
- StationID | Number | No | Numeric station identifier
- ServiceType | Number | No | Type of service provided
- ServiceAvailable | Number | No | Service availability status
- AvailableRentBikes | Number | No | Number of bikes available for rent
- AvailableReturnBikes | Number | No | Number of available return slots
- StationPosition.PositionLon | Number | No | Station longitude coordinate
- StationPosition.PositionLat | Number | No | Station latitude coordinate
- StationPosition.GeoHash | String | No | Geohash for location indexing
- StationLocation | Object (GeoJSON Point) | No | GeoJSON Point geometry
- StationName.Zh_tw | String | No | Station name in Traditional Chinese
- StationName.En | String | No | Station name in English

### Nested Schema: pointSchema (StationLocation)
- **type** | String | Yes | Must be "Point" for GeoJSON
- **coordinates** | Array of Numbers | Yes | [longitude, latitude] coordinate pair

## 🔑 Key Information
- **Primary Key:** _id (custom Number type)
- **Indexes:** 
  - StationLocation (2dsphere geospatial index)
  - Auto-indexing enabled
- **Unique Constraints:** None explicitly defined
- **Default Values:** None specified

## 📝 Usage Examples
```javascript
// Find stations near a location
const nearbyStations = await UBikeStations.find({
  StationLocation: {
    $near: {
      $geometry: { type: "Point", coordinates: [121.5654, 25.0330] },
      $maxDistance: 1000 // 1km radius
    }
  }
});

// Find available stations
const availableStations = await UBikeStations.find({
  AvailableRentBikes: { $gt: 0 }
});
```

## 🔗 Related Models
- **Trip models** - Referenced for bike sharing trip planning
- **User location models** - Used for proximity-based queries
- **Mobility service models** - Part of integrated transport system

## 📌 Important Notes
- Uses 2dsphere index for efficient geospatial queries
- Supports bilingual station names (Chinese Traditional and English)
- Real-time availability tracking for bikes and return slots
- Custom numeric _id instead of MongoDB ObjectId
- Connected to 'dataset' MongoDB database for operational data

## 🏷️ Tags
**Keywords:** ubike, youbike, bikeshare, station, availability, geospatial
**Category:** #model #database #mongodb #geospatial #bikeshare