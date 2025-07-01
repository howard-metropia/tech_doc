# BusRoutes Model Documentation

## 📋 Model Overview
- **Purpose:** Caches bus route information from GTFS feeds for transit planning and routing
- **Table/Collection:** bus_routes
- **Database Type:** MongoDB
- **Relationships:** Standalone collection for cached transit route data

## 🔧 Schema Definition
| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| routes | [Object] | No | Array of route objects |
| routes[].type | String | No | Route type identifier |
| routes[].route_id | String | No | GTFS route ID |
| routes[].agency_id | String | No | Transit agency ID |
| routes[].route_short_name | String | No | Short route name (e.g., "M1") |
| routes[].route_long_name | String | No | Full route name |
| routes[].route_color | String | No | Route color (hex code) |
| routes[].first_headsign | String | No | First direction headsign |
| routes[].first_headsign2 | String | No | Alternative first headsign |
| routes[].end_headsign | String | No | End direction headsign |
| routes[].services | String | No | Service information |
| mrkTime | Date | No | Mark/cache timestamp |
| addedAt | Date | Auto | Document creation timestamp |
| modifiedAt | Date | Auto | Last modification timestamp |

## 🔑 Key Information
- **Primary Key:** _id (MongoDB ObjectId)
- **Indexes:** Default _id index
- **Unique Constraints:** None
- **Default Values:** None
- **Schema Options:** versionKey: false, custom timestamps

## 📝 Usage Examples
```javascript
// Create bus routes cache entry
const routesData = await BusRoutes.create({
  routes: [
    {
      type: 'bus',
      route_id: 'route_1',
      agency_id: 'agency_001',
      route_short_name: 'M1',
      route_long_name: 'Main Street Line',
      route_color: '#FF0000',
      first_headsign: 'Downtown',
      end_headsign: 'Uptown',
      services: 'weekday'
    }
  ],
  mrkTime: new Date()
});

// Find routes by agency
const agencyRoutes = await BusRoutes.find({
  'routes.agency_id': 'agency_001'
});

// Update route cache
await BusRoutes.updateOne(
  { _id: routeId },
  { $set: { mrkTime: new Date() } }
);
```

## 🔗 Related Models
- Used for transit trip planning and routing
- Integrates with GTFS data processing
- Supports real-time transit information

## 📌 Important Notes
- Cache layer for GTFS route data
- Supports multiple routes per document
- Custom timestamp fields (addedAt, modifiedAt)
- Headsign fields store route direction information
- Route colors support visual representation in apps
- Mark time tracks cache freshness

## 🏷️ Tags
**Keywords:** bus-routes, transit, gtfs, cache, mongodb, transportation, routing
**Category:** #model #database #transit #cache #mongodb #transportation