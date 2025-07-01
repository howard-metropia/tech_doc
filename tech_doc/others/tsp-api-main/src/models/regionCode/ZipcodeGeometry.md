# ZipcodeGeometry Model Documentation

## 📋 Model Overview
- **Purpose:** Stores ZIP code geometric boundaries using GeoJSON MultiPolygon format
- **Table/Collection:** zip_code_geometry
- **Database Type:** MongoDB
- **Relationships:** Geographic reference data for postal code boundaries

## 🔧 Schema Definition

### Main Schema
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| _id | ObjectId | Yes | MongoDB document identifier |
| object_id | Number | Yes | Unique ZIP code object identifier |
| geometry | Object | No | GeoJSON MultiPolygon geometry |
| zip_code | Number | Yes | ZIP code number |

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
// Find ZIP code by point location
const zipcode = await ZipcodeGeometry.findOne({
  geometry: {
    $geoIntersects: {
      $geometry: {
        type: "Point",
        coordinates: [longitude, latitude]
      }
    }
  }
});

// Find ZIP codes by numeric code
const zipArea = await ZipcodeGeometry.findOne({
  zip_code: 94102
});

// Find nearby ZIP codes
const nearbyZips = await ZipcodeGeometry.find({
  geometry: {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [longitude, latitude]
      },
      $maxDistance: 5000 // 5km radius
    }
  }
});
```

## 🔗 Related Models
- **CityCodeGeometry**: Related city boundaries
- **CountyCodeGeometry**: Related county boundaries
- **UserAddresses**: User addresses can be matched to ZIP codes

## 📌 Important Notes
- Uses GeoJSON MultiPolygon format for complex ZIP code boundaries
- 2dsphere index enables efficient geospatial queries
- Part of regionCode module for geographic reference data
- Numeric ZIP code field for easy lookup and matching
- Cache database for fast geographic lookups

## 🏷️ Tags
**Keywords:** zipcode, postal-code, geospatial, GeoJSON, boundaries
**Category:** #model #database #geospatial #postal-codes