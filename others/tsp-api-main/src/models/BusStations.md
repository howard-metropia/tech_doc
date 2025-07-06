# BusStations Model Documentation

## 📋 Model Overview
- **Purpose:** Stores bus station and route information with directional data
- **Table/Collection:** bus_stations
- **Database Type:** MongoDB
- **Relationships:** References GTFS transit data and route information

## 🔧 Schema Definition

### Main Schema
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| _id | ObjectId | Yes | MongoDB document identifier |
| agency_id | String | No | Transit agency identifier |
| route_id | String | No | Route identifier |
| service_id | String | No | Service schedule identifier |
| route_short_name | String | No | Short route name (e.g., "1", "A") |
| route_long_name | String | No | Full route name |
| positive_direction | Object | No | Positive direction stops |
| opposite_direction | Object | No | Opposite direction stops |
| mrkTime | Date | No | Mark/update timestamp |
| addedAt | Date | No | Record creation timestamp |
| modifiedAt | Date | No | Record modification timestamp |

### History Object Schema (unused in main schema)
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| trip_id | String | No | Trip identifier |
| stop_id | String | No | Stop identifier |
| stop_sequence | String | No | Stop sequence number |
| stop_name | String | No | Stop name |

## 🔑 Key Information
- **Primary Key:** _id (MongoDB ObjectId)
- **Indexes:** None explicitly defined
- **Unique Constraints:** None
- **Default Values:** Auto-generated timestamps (addedAt, modifiedAt)

## 📝 Usage Examples
```javascript
// Find bus stations by route
const stations = await BusStations.find({
  route_id: 'route_123',
  agency_id: 'metro_transit'
});

// Get stations by route name
const routeStations = await BusStations.find({
  route_short_name: '15'
});

// Update station data
await BusStations.updateOne(
  { route_id: 'route_456' },
  { 
    $set: { 
      mrkTime: new Date(),
      positive_direction: updatedStops
    }
  }
);
```

## 🔗 Related Models
- **GTFS Routes**: Station data based on GTFS transit feeds
- **BusSchedules**: Station stops relate to schedule data
- **TripPlanning**: Stations used for route planning

## 📌 Important Notes
- Follows GTFS (General Transit Feed Specification) standards
- Directional route data for inbound/outbound services
- Custom timestamp tracking with mrkTime field
- Cache database for fast transit data access
- Flexible schema allows for varying route structures

## 🏷️ Tags
**Keywords:** bus-stations, transit, GTFS, routes, directions
**Category:** #model #database #transit #public-transport