# TripWayPoints Model Documentation

## 📋 Model Overview
- **Purpose:** Stores waypoint data for trip routes and navigation points
- **Table/Collection:** trip_waypoint
- **Database Type:** MongoDB (cache database)
- **Relationships:** Links waypoints to specific trips for route tracking

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| _id | ObjectId | Yes | MongoDB document identifier |
| place_uuid | String | No | Unique identifier for the place/location |
| waypoint_no | Number | No | Sequential number of waypoint in trip |
| category | String | No | Waypoint category (origin, destination, intermediate) |
| name | String | No | Human-readable name of the waypoint |
| address | String | No | Full address of the waypoint location |
| trip_id | Number | No | Reference to associated trip |
| position | Mixed | No | Geographic coordinates and position data |
| created_on | Date | No | Waypoint creation timestamp |

## 🔑 Key Information
- **Primary Key:** _id (MongoDB ObjectId)
- **Indexes:** trip_id, waypoint_no, category, place_uuid
- **Unique Constraints:** None
- **Default Values:** created_on = Date.now

## 📝 Usage Examples
```javascript
// Get waypoints for a trip
const waypoints = await TripWayPoints.find({ trip_id: 123 })
  .sort({ waypoint_no: 1 });

// Find waypoints by category
const destinations = await TripWayPoints.find({ 
  trip_id: 123, 
  category: 'destination' 
});

// Create new waypoint
const waypoint = new TripWayPoints({
  place_uuid: 'uuid-123',
  waypoint_no: 1,
  category: 'origin',
  name: 'Downtown Station',
  address: '123 Main St, City, State',
  trip_id: 123,
  position: { lat: 37.7749, lng: -122.4194 }
});
await waypoint.save();
```

## 🔗 Related Models
- `TripDetails` - Related trip information (MySQL)
- `Trips` - Associated trip records (MySQL)
- Places/POI models - Referenced via place_uuid

## 📌 Important Notes
- Stored in MongoDB cache database for fast retrieval
- position field contains flexible geographic data structure
- waypoint_no provides ordering for route navigation
- Used for trip planning and navigation services
- Supports both structured addresses and coordinate data

## 🏷️ Tags
**Keywords:** waypoints, navigation, routes, trips, geography
**Category:** #model #database #navigation #mongodb

---
Note: This MongoDB model provides waypoint storage for trip navigation and route planning.