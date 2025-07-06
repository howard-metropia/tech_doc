# DuoReservations Model Documentation

## 📋 Model Overview
- **Purpose:** Manages duo/carpool reservation requests and their lifecycle
- **Table/Collection:** duo_reservation
- **Database Type:** MySQL (portal database)
- **Relationships:** Core entity for carpooling system, linked to matches and users

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| id | INT | Yes | Primary key, auto-increment |
| user_id | INT | Yes | Foreign key to auth_user making the reservation |
| origin_lat | DECIMAL | Yes | Starting location latitude |
| origin_lng | DECIMAL | Yes | Starting location longitude |
| destination_lat | DECIMAL | Yes | Destination location latitude |
| destination_lng | DECIMAL | Yes | Destination location longitude |
| departure_time | DATETIME | Yes | Preferred departure time |
| passenger_count | INT | No | Number of passengers (default 1) |
| status | VARCHAR | No | Reservation status (active, matched, completed, cancelled) |
| created_at | TIMESTAMP | Yes | Reservation creation timestamp |
| updated_at | TIMESTAMP | Yes | Last update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** user_id, status, departure_time, origin coordinates
- **Unique Constraints:** None
- **Default Values:** passenger_count = 1, status = 'active', created_at = CURRENT_TIMESTAMP

## 📝 Usage Examples
```javascript
// Find available reservations for matching
const availableReservations = await DuoReservations.query()
  .where('status', 'active')
  .where('departure_time', '>', new Date());

// Get user's active reservations
const userReservations = await DuoReservations.query()
  .where('user_id', userId)
  .whereIn('status', ['active', 'matched']);

// Create new duo reservation
await DuoReservations.query().insert({
  user_id: userId,
  origin_lat: 37.7749,
  origin_lng: -122.4194,
  destination_lat: 37.3382,
  destination_lng: -121.8863,
  departure_time: '2023-12-01 08:00:00',
  passenger_count: 2
});
```

## 🔗 Related Models
- `AuthUsers` - Many-to-one relationship via user_id
- `DuoReservationMatches` - One-to-many relationship for matching pairs
- `BlockUsers` - Affects matching eligibility

## 📌 Important Notes
- Core entity for the carpooling/duo ride system
- Geographic coordinates used for proximity matching
- departure_time enables time-based matching algorithms
- Status field tracks reservation lifecycle from creation to completion

## 🏷️ Tags
**Keywords:** carpool, duo, reservations, ridesharing, matching
**Category:** #model #database #carpool #reservations #mysql

---
Note: This model is the foundation of the duo/carpooling reservation system.