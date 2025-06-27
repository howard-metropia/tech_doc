# TollModels Documentation

## 📋 Model Overview
- **Purpose:** Manages toll road zones, rates, and verification data for dynamic pricing
- **Table/Collection:** toll_zone_verify, toll_zones, toll_rate, toll_zone_pairs
- **Database Type:** MongoDB (cache and dataset connections)
- **Relationships:** Zone pairs reference toll zones, rates reference zone pairs

## 🔧 Schema Definition

### TollZoneVerify (Cache)
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| route_id | String | No | Route identifier |
| user_id | Number | No | User requesting toll info |
| departure_time | Date | No | Planned departure time |
| here_polyline | String | No | HERE Maps encoded polyline |
| google_polyline | String | No | Google Maps encoded polyline |
| staticTollCost | Object | No | Static toll calculation |
| dynamicTollCost | Object | No | Dynamic toll calculation |
| drivingCost | Object | No | Total driving cost |

### TollZones (Dataset)
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| source | String | No | Data source identifier |
| order | Number | No | Zone ordering on highway |
| highway | String | No | Highway identifier |
| direction | String | No | Traffic direction |
| type | String | No | Zone type (entry/exit) |
| name | String | No | Zone name |
| lat | Number | No | Latitude coordinate |
| lon | Number | No | Longitude coordinate |
| geoPolygon | GeoJSON | No | Geographic boundary polygon |
| googlePolygon | String | No | Google-encoded polygon |

## 🔑 Key Information
- **Primary Key:** _id (MongoDB ObjectId)
- **Indexes:** 
  - TollZoneVerify: TTL index on updatedAt (1 hour expiry)
  - TollZones: Compound unique index on order+highway+direction+type, 2dsphere on geoPolygon
  - TollRate: Compound index on zone_pair_id+time
  - TollZonePairs: Unique index on zone_pair_id
- **Unique Constraints:** Zone combinations, zone pair IDs
- **Default Values:** Timestamps auto-generated

## 📝 Usage Examples
```javascript
// Find toll zones for a highway
const zones = await TollZones.find({
  highway: 'I-405',
  direction: 'NB'
}).sort({ order: 1 });

// Get current toll rates
const rates = await TollRate.find({
  zone_pair_id: 'zone1_zone2',
  time: currentHour
});

// Cache toll verification (expires in 1 hour)
const verification = new TollZoneVerify({
  route_id: routeId,
  staticTollCost: { amount: 5.50 }
});
```

## 🔗 Related Models
- **TollZones** ↔ **TollZonePairs**: Zones define pairs for rate calculation
- **TollZonePairs** ↔ **TollRate**: Pairs have time-based rate schedules
- **TollZoneVerify**: Temporary cache for route calculations

## 📌 Important Notes
- Uses both cache and dataset MongoDB connections
- TollZoneVerify has TTL (1 hour) for automatic cleanup
- Geographic queries supported via 2dsphere indexes
- Rate data includes statistical distributions (mean, standard deviation)
- Strict mode disabled for flexible schema evolution

## 🏷️ Tags
**Keywords:** toll-roads, dynamic-pricing, geospatial, rates
**Category:** #model #database #transportation #pricing