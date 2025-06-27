# TripRoutes Model Documentation

## 📋 Model Overview
- **Purpose:** Stores routing information and path details for trips
- **Table/Collection:** trip_routes
- **Database Type:** MySQL (portal database)
- **Relationships:** Related to Trips, AuthUsers, and route planning services

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| id | INT | Yes | Primary key, auto-increment |
| trip_id | INT | No | Foreign key to trips table |
| user_id | INT | Yes | Foreign key to auth_user table |
| route_data | JSON | No | Complete route information and waypoints |
| distance | DECIMAL | No | Total route distance (miles/km) |
| duration | INT | No | Estimated duration (seconds) |
| travel_mode | VARCHAR | No | Transportation mode used |
| route_provider | VARCHAR | No | Routing service provider (HERE/Google/Mapbox) |
| route_hash | VARCHAR | No | Hash for route deduplication |
| polyline | TEXT | No | Encoded polyline string |
| created_at | TIMESTAMP | Yes | Route creation timestamp |
| updated_at | TIMESTAMP | Yes | Last update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** trip_id, user_id, route_hash, created_at
- **Unique Constraints:** None
- **Default Values:** created_at = CURRENT_TIMESTAMP

## 📝 Usage Examples
```javascript
// Basic query example
const routes = await TripRoutes.query()
  .where('user_id', userId)
  .orderBy('created_at', 'desc');

// Get routes for specific trip
const tripRoutes = await TripRoutes.query()
  .where('trip_id', tripId)
  .select('route_data', 'polyline', 'distance', 'duration');

// Find similar routes using hash
const similarRoutes = await TripRoutes.query()
  .where('route_hash', routeHash)
  .where('travel_mode', travelMode);
```

## 🔗 Related Models
- `AuthUsers` - Many-to-one relationship via user_id
- `Trips` - Many-to-one relationship via trip_id
- `TripDetail` - Related trip execution details
- Route optimization and planning services

## 📌 Important Notes
- Route_data stores comprehensive routing information as JSON
- Polyline field uses encoded polyline algorithm for map display
- Route_hash enables finding duplicate/similar routes
- Multiple routing providers supported for redundancy

## 🏷️ Tags
**Keywords:** routes, navigation, polyline, routing, trips
**Category:** #model #database #navigation #mysql

---
Note: Central repository for all route calculations and path planning data in the system.