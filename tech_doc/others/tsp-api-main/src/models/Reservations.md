# Reservations Model Documentation

## 📋 Model Overview
- **Purpose:** Manages trip reservations across all transportation modes including carpooling
- **Table/Collection:** reservation
- **Database Type:** MySQL (portal database)
- **Relationships:** Related to AuthUsers, DuoReservations, and trip planning

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| id | INT | Yes | Primary key, auto-increment |
| user_id | INT | Yes | Foreign key to auth_user table |
| travel_mode | INT | Yes | Transportation mode (see static constants) |
| status | INT | Yes | Reservation status (see static constants) |
| role | INT | No | User role for shared trips (driver/passenger) |
| origin_lat | DECIMAL | No | Starting point latitude |
| origin_lng | DECIMAL | No | Starting point longitude |
| destination_lat | DECIMAL | No | Ending point latitude |
| destination_lng | DECIMAL | No | Ending point longitude |
| departure_time | TIMESTAMP | No | Preferred departure time |
| arrival_time | TIMESTAMP | No | Preferred arrival time |
| created_at | TIMESTAMP | Yes | Reservation creation timestamp |
| updated_at | TIMESTAMP | Yes | Last update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** user_id, status, travel_mode, departure_time
- **Unique Constraints:** None
- **Default Values:** created_at = CURRENT_TIMESTAMP

### Travel Mode Constants
```javascript
{
  DRIVING: 1,
  PUBLIC_TRANSIT: 2,
  WALKING: 3,
  BIKING: 4,
  INTERMODAL: 5,
  TRUCKING: 6,
  PARK_AND_RIDE: 7,
  DUO: 100  // Carpooling
}
```

### Status Constants
```javascript
{
  NONE: 0,               // Draft or no request
  SEARCHING: 1,          // Looking for matches
  CHOOSING: 2,           // Selecting from options
  PENDING: 3,            // Awaiting confirmation
  SUGGESTION: 4,         // System suggestion
  ACCEPTED: 5,           // User accepted
  REPEALED: 6,           // Cancelled by user
  REPEALED_CONFLICT: 7,  // Cancelled due to conflict
  MATCHED: 11,           // Successfully matched
  RESERVED: 50,          // Confirmed reservation
  CANCELED: 51,          // Cancelled reservation
  CANCELED_INACTION: 52, // Auto-cancelled
  CANCELED_PASSIVE: 53,  // Passively cancelled
  STARTED: 60            // Trip started
}
```

### Role Constants
```javascript
{
  DRIVER: 1,
  PASSENGER: 2
}
```

## 📝 Usage Examples
```javascript
// Basic query example
const reservations = await Reservations.query()
  .where('user_id', userId)
  .where('status', Reservations.status.RESERVED);

// Get active DUO reservations with relationship
const duoReservations = await Reservations.query()
  .where('travel_mode', Reservations.travelMode.DUO)
  .whereIn('status', [Reservations.status.MATCHED, Reservations.status.RESERVED])
  .withGraphFetched('duoReservation');

// Find reservations by location proximity
const nearbyReservations = await Reservations.query()
  .whereBetween('origin_lat', [lat - 0.01, lat + 0.01])
  .whereBetween('origin_lng', [lng - 0.01, lng + 0.01]);
```

## 🔗 Related Models
- `AuthUsers` - Many-to-one relationship via user_id
- `DuoReservations` - One-to-one relationship for carpooling details
- Trip tracking and validation models

## 📌 Important Notes
- Status workflow manages reservation lifecycle
- DUO mode (100) specifically for carpooling functionality
- Role field only relevant for shared transportation modes
- Coordinates stored in decimal degrees format

## 🏷️ Tags
**Keywords:** reservations, trips, carpooling, transportation, duo
**Category:** #model #database #transportation #mysql

---
Note: Central model for managing all transportation reservations in the MaaS platform.