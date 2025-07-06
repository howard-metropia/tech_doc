# ConstructionZone Model Documentation

## 📋 Model Overview
- **Purpose:** Stores construction zone data with geographic boundaries and traffic impact details
- **Table/Collection:** construction_zone
- **Database Type:** MongoDB
- **Relationships:** None (geospatial data model)

## 🔧 Schema Definition

### Main Schema
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| type | String | Yes | GeoJSON type ('Feature') |
| properties | Object | Yes | Construction zone properties |
| geometry | GeoJSON | Yes | Geographic boundary polygon |

### Properties Schema
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| core_details | Object | Yes | Basic event information |
| beginning_cross_street | String | Yes | Starting cross street |
| ending_cross_street | String | Yes | Ending cross street |
| start_date | Date | Yes | Construction start date |
| end_date | Date | Yes | Construction end date |
| location_method | String | Yes | How location was determined |
| vehicle_impact | String | Yes | Impact on vehicle traffic |
| event_status | String | No | Current status of construction |

### Core Details Schema
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| data_source_id | String | Yes | Source system identifier |
| event_type | String | Yes | Type of construction event |
| road_names | Array | Yes | Affected road names |
| direction | String | Yes | Traffic direction affected |
| creation_date | Date | Yes | When record was created |
| update_date | Date | Yes | Last update timestamp |

## 🔑 Key Information
- **Primary Key:** _id (MongoDB ObjectId)
- **Indexes:** 2dsphere index on geometry for geospatial queries
- **Unique Constraints:** None
- **Default Values:** Date.now for creation_date and start fields

## 📝 Usage Examples
```javascript
// Find construction zones in area
const zones = await ConstructionZone.find({
  geometry: {
    $geoIntersects: {
      $geometry: {
        type: "Polygon",
        coordinates: [boundary_coords]
      }
    }
  }
});

// Get active construction zones
const activeZones = await ConstructionZone.find({
  'properties.start_date': { $lte: new Date() },
  'properties.end_date': { $gte: new Date() }
});
```

## 🔗 Related Models
- None - standalone geospatial model for construction data

## 📌 Important Notes
- Follows GeoJSON Feature format for geographic data
- Uses 2dsphere index for efficient spatial queries
- Nested schema structure for detailed construction information
- Includes verification flags for data quality assurance
- Extensions schema provides additional incident details

## 🏷️ Tags
**Keywords:** construction, geospatial, traffic-impact, GeoJSON
**Category:** #model #database #geospatial #transportation