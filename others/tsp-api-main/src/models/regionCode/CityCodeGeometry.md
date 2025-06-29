# CityCodeGeometry Model Documentation

## 📋 Model Overview
- **Purpose:** Stores city code geometric boundaries using GeoJSON MultiPolygon format
- **Table/Collection:** city_code_geometry
- **Database Type:** MongoDB
- **Relationships:** Geographic reference data for city boundaries

## 🔧 Schema Definition

### Main Schema
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| _id | ObjectId | Yes | MongoDB document identifier |
| object_id | Number | Yes | Unique city object identifier |
| geometry | Object | No | GeoJSON MultiPolygon geometry |
| name | String | Yes | City name |

### Geometry Schema (GeoJSON MultiPolygon)
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| type | String | Yes | Must be "MultiPolygon" |
| coordinates | Array | Yes | 4D array of coordinates [[[[[Number]]]]] |

## 🔑 Key Information
- **Primary Key:** _id (MongoDB ObjectId)
- **Indexes:** 2dsphere index on geometry field for geospatial queries
- **Unique Constraints:** None
- **Default Values:** None specified

## 📝 Usage Examples
```javascript
// Find city by point location
const city = await CityCodeGeometry.findOne({
  geometry: {
    $geoIntersects: {
      $geometry: {
        type: "Point",
        coordinates: [longitude, latitude]
      }
    }
  }
});

// Find cities within bounding box
const cities = await CityCodeGeometry.find({
  geometry: {
    $geoWithin: {
      $geometry: {
        type: "Polygon",
        coordinates: [boundingBoxCoords]
      }
    }
  }
});

// Create new city geometry
const cityGeometry = new CityCodeGeometry({
  object_id: 12345,
  name: 'San Francisco',
  geometry: {
    type: 'MultiPolygon',
    coordinates: [multiPolygonCoordinates]
  }
});
```

## 🔗 Related Models
- **ZipcodeGeometry**: Related postal code boundaries
- **CountyCodeGeometry**: Related county boundaries
- **UserLocations**: User locations can be matched to cities

## 📌 Important Notes
- Uses GeoJSON MultiPolygon format for complex city boundaries
- 2dsphere index enables efficient geospatial queries
- Part of regionCode module for geographic reference data
- Supports point-in-polygon and area-based queries
- Cache database for fast geographic lookups

## 🏷️ Tags
**Keywords:** city-boundaries, geospatial, GeoJSON, MultiPolygon
**Category:** #model #database #geospatial #boundaries