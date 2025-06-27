# CountyCodeGeometry Model Documentation

## 📋 Model Overview
- **Purpose:** Stores county geometric boundaries using GeoJSON MultiPolygon format
- **Table/Collection:** county_code_geometry
- **Database Type:** MongoDB
- **Relationships:** Geographic reference data for county boundaries

## 🔧 Schema Definition

### Main Schema
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| _id | ObjectId | Yes | MongoDB document identifier |
| object_id | Number | Yes | Unique county object identifier |
| geometry | Object | No | GeoJSON MultiPolygon geometry |
| name | String | Yes | County name |

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
// Find county by point location
const county = await CountyCodeGeometry.findOne({
  geometry: {
    $geoIntersects: {
      $geometry: {
        type: "Point",
        coordinates: [longitude, latitude]
      }
    }
  }
});

// Find county by name
const county = await CountyCodeGeometry.findOne({
  name: "San Francisco County"
});

// Find counties within state boundary
const counties = await CountyCodeGeometry.find({
  geometry: {
    $geoWithin: {
      $geometry: {
        type: "Polygon",
        coordinates: [stateBoundaryCoords]
      }
    }
  }
});
```

## 🔗 Related Models
- **CityCodeGeometry**: Related city boundaries within counties
- **ZipcodeGeometry**: Related ZIP code boundaries within counties
- **StateGeometry**: Counties belong to states/provinces

## 📌 Important Notes
- Uses GeoJSON MultiPolygon format for complex county boundaries
- 2dsphere index enables efficient geospatial queries
- Part of regionCode module for geographic reference data
- Name field for human-readable identification
- Cache database for fast geographic lookups
- Useful for administrative and political boundary queries

## 🏷️ Tags
**Keywords:** county, administrative-boundaries, geospatial, GeoJSON, government
**Category:** #model #database #geospatial #administrative