# HoustonBusRealtime Model Documentation

## 📋 Model Overview
- **Purpose:** Stores real-time Houston Metro bus schedule and arrival data
- **Table/Collection:** houston_metro_stop_schedule
- **Database Type:** MongoDB (dataset database)
- **Relationships:** Contains nested route, direction, and trip data for Houston transit

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| _id | String | Yes | MongoDB document identifier |
| __v | Number | No | MongoDB version key |
| routes | Array | No | Array of route objects with directions and trips |
| routes.routeId | String | No | Houston Metro route identifier |
| routes.directions | Array | No | Array of direction objects |
| routes.directions.directionId | Number | No | Direction identifier (0=outbound, 1=inbound) |
| routes.directions.trips | Array | No | Array of trip objects with schedule data |
| routes.directions.trips.tripId | Number | No | Unique trip identifier |
| routes.directions.trips.stopSequence | Number | No | Stop sequence number in trip |
| routes.directions.trips.scheduleRelationship | String | No | GTFS schedule relationship |
| routes.directions.trips.arrival | Object | No | Arrival time and delay information |
| routes.directions.trips.departure | Object | No | Departure time and delay information |
| stopId | String | No | Houston Metro stop identifier |
| syncTime | String | No | Last synchronization timestamp |

## 🔑 Key Information
- **Primary Key:** _id
- **Indexes:** stopId, routes.routeId, syncTime
- **Unique Constraints:** None
- **Default Values:** None specified

## 📝 Usage Examples
```javascript
// Get real-time data for a specific stop
const stopData = await HoustonBusRealtime.findOne({ stopId: 'STOP_123' });

// Find all routes serving a stop
const routesAtStop = await HoustonBusRealtime.findOne(
  { stopId: 'STOP_123' },
  { 'routes.routeId': 1 }
);

// Get recent sync data
const recentData = await HoustonBusRealtime.find({
  syncTime: { $gte: oneHourAgo }
});
```

## 🔗 Related Models
- Houston Metro GTFS static data models
- Transit alert models for service disruptions
- User trip models for Houston Metro integration

## 📌 Important Notes
- Contains complex nested structure following GTFS-Realtime format
- arrival and departure objects include both scheduled time and delay
- scheduleRelationship indicates if trip is on schedule, added, or cancelled
- syncTime tracks data freshness for real-time accuracy
- Used for providing live Houston Metro bus arrival predictions
- Supports both inbound and outbound trip directions

## 🏷️ Tags
**Keywords:** transit, realtime, houston, metro, bus, gtfs
**Category:** #model #database #transit #realtime #mongodb

---
Note: This MongoDB model stores real-time Houston Metro bus data for live transit information.