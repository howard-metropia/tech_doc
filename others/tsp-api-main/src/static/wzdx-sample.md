# Static/Constants Documentation: wzdx-sample.js

## 📋 File Overview
- **Purpose:** Provides sample work zone data following the WZDx (Work Zone Data Exchange) v4.2 specification for testing construction zone integration
- **Usage:** Used by construction zone services, road closure processing, and traffic management system testing
- **Type:** Mock data / WZDx sample / Construction zone fixture

## 🔧 Main Exports
```javascript
module.exports = {
  data: {
    type: "FeatureCollection",
    road_event_feed_info: {
      publisher: "Houston TranStar",
      version: "4.2",
      update_date: "2024-10-27T00:00:00Z",
      data_sources: [...]
    },
    features: [{
      id: "fef42",
      type: "Feature",
      properties: { core_details: {...}, extensions: {...} },
      geometry: { type: "LineString", coordinates: [...] }
    }]
  }
};
```

## 📝 Constants Reference
| Section | Key Properties | Sample Values | Purpose |
|---------|---------------|---------------|---------|
| Feed Info | publisher, version, update_date | Houston TranStar, 4.2, 2024-10-27 | Data source identification |
| Core Details | event_type, road_names, direction | work-zone, Main St, northbound | Basic event classification |
| Timing | start_date, end_date, creation_date | ISO 8601 timestamps | Event lifecycle management |
| Impact | vehicle_impact, location_method | all-lanes-closed, channel-device-method | Traffic impact assessment |
| Extensions | type, incident_type, description | Closure, Construction zone | Additional context data |
| Geometry | type, coordinates | LineString, lat/lng pairs | Geographic representation |

## 💡 Usage Examples
```javascript
// Import WZDx sample data
const wzdxSample = require('./static/wzdx-sample');

// Test work zone processing
const workZone = wzdxSample.data.features[0];
const coreDetails = workZone.properties.core_details;

// Check if work zone affects route
if (coreDetails.vehicle_impact === 'all-lanes-closed') {
  suggestAlternateRoute();
}

// Extract timing information
const startDate = new Date(workZone.properties.start_date);
const endDate = new Date(workZone.properties.end_date);
const isActive = Date.now() >= startDate && Date.now() <= endDate;

// Geographic intersection testing
const workZoneCoords = workZone.geometry.coordinates;
const userRoute = getUserRoute();
if (routeIntersectsLineString(userRoute, workZoneCoords)) {
  showConstructionWarning();
}

// Feed metadata validation
const feedInfo = wzdxSample.data.road_event_feed_info;
console.log(`Data from ${feedInfo.publisher}, version ${feedInfo.version}`);
// "Data from Houston TranStar, version 4.2"
```

## ⚠️ Important Notes
- Follows WZDx (Work Zone Data Exchange) v4.2 specification for standardized work zone data
- Sample represents overnight construction closure pattern common in urban areas
- Extensions section provides additional Houston TranStar-specific metadata
- Coordinates represent realistic Houston area construction zone location
- Schedule indicates "Excluding the Weekend(s)" for typical weekday-only construction
- Last expire time (timestamp) helps track data freshness for cache management

## 🏷️ Tags
**Keywords:** work-zones, construction-closures, wzdx-specification, traffic-management, road-events, houston-transtar  
**Category:** #static #mock-data #construction #wzdx #traffic-events #testing