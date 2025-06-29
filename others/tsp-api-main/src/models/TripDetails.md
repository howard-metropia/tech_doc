# TripDetails Model Documentation

## 📋 Model Overview
- **Purpose:** Stores detailed information about individual trips and their attributes
- **Table/Collection:** trip_detail
- **Database Type:** MySQL (portal database)
- **Relationships:** Related to trip management and user journey tracking

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| id | INT | Yes | Primary key, auto-increment |
| trip_id | INT | Yes | Foreign key referencing main trip record |
| user_id | INT | Yes | Foreign key referencing auth_user |
| detail_type | VARCHAR | No | Type of trip detail (e.g., waypoint, event) |
| detail_data | JSON/TEXT | No | Detailed trip information in JSON format |
| created_at | TIMESTAMP | Yes | Record creation timestamp |
| updated_at | TIMESTAMP | Yes | Last update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** trip_id, user_id, detail_type
- **Unique Constraints:** None
- **Default Values:** created_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP

## 📝 Usage Examples
```javascript
// Basic query example
const tripDetails = await TripDetails.query().where('trip_id', 123);

// Get details for specific user
const userTripDetails = await TripDetails.query()
  .where('user_id', userId)
  .where('detail_type', 'waypoint');

// Insert new trip detail
await TripDetails.query().insert({
  trip_id: 123,
  user_id: 456,
  detail_type: 'milestone',
  detail_data: JSON.stringify({ milestone: 'departure' })
});
```

## 🔗 Related Models
- `Trips` - Many-to-one relationship via trip_id
- `AuthUsers` - Many-to-one relationship via user_id
- `TripWayPoints` - Related trip waypoint data

## 📌 Important Notes
- Contains granular trip information for analytics and tracking
- detail_data field stores flexible JSON data structure
- Used for storing trip milestones, events, and metadata
- Essential for trip validation and incentive calculations

## 🏷️ Tags
**Keywords:** trips, details, tracking, analytics, journey
**Category:** #model #database #trips #mysql

---
Note: This model stores detailed trip information for analysis and validation purposes.