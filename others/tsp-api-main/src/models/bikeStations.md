# bikeStations Model Documentation

## 📋 Model Overview
- **Purpose:** Stores bike sharing station data with real-time availability information
- **Table/Collection:** connectsmart_bike_station
- **Database Type:** MongoDB
- **Relationships:** None (cached station data)

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| _id | String | Yes | MongoDB document ID |
| uid | String | No | Unique station identifier |
| city | String | No | City where station is located |
| operator_url | String | No | Bike sharing operator website |
| operator_name | String | No | Name of bike sharing operator |
| name | String | No | Station name/label |
| address | String | No | Physical address of station |
| location | GeoJSON | No | Geographic coordinates (Point) |
| empty_slots | Number | No | Number of available docking slots |
| free_bikes | Number | No | Number of available bikes |

## 🔑 Key Information
- **Primary Key:** _id (MongoDB ObjectId)
- **Indexes:** 2dsphere index on location field
- **Unique Constraints:** None
- **Default Values:** None specified

## 📝 Usage Examples
```javascript
// Find nearby bike stations
const stations = await bikeStations.find({
  location: {
    $near: {
      $geometry: { type: "Point", coordinates: [lng, lat] },
      $maxDistance: 1000
    }
  }
});

// Get stations with available bikes
const availableStations = await bikeStations.find({
  free_bikes: { $gt: 0 }
});
```

## 🔗 Related Models
- None - cached data from external bike sharing APIs

## 📌 Important Notes
- Uses MongoDB cache database for fast lookups
- Location field uses GeoJSON Point format for geospatial queries
- Real-time data updated from external bike sharing services
- Commented out timestamp fields suggest manual update strategy

## 🏷️ Tags
**Keywords:** bike-sharing, stations, geospatial, real-time
**Category:** #model #database #mobility #cache