# TripDetail Model Documentation

## 📋 Model Overview
- **Purpose:** Stores detailed information about individual trips taken by users
- **Table/Collection:** trip_detail
- **Database Type:** MySQL (portal database)
- **Relationships:** Belongs to Trip, AuthUsers, and potentially TripRoutes

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| id | INT | Yes | Primary key, auto-increment |
| trip_id | INT | Yes | Foreign key to trips table |
| user_id | INT | Yes | Foreign key to auth_user table |
| mode | VARCHAR | No | Transportation mode used |
| distance | DECIMAL | No | Distance traveled in miles/km |
| duration | INT | No | Trip duration in seconds |
| start_time | TIMESTAMP | No | Trip start timestamp |
| end_time | TIMESTAMP | No | Trip end timestamp |
| origin_lat | DECIMAL | No | Origin latitude |
| origin_lng | DECIMAL | No | Origin longitude |
| destination_lat | DECIMAL | No | Destination latitude |
| destination_lng | DECIMAL | No | Destination longitude |
| created_at | TIMESTAMP | Yes | Record creation timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** trip_id, user_id, start_time, end_time
- **Unique Constraints:** None
- **Default Values:** created_at = CURRENT_TIMESTAMP

## 📝 Usage Examples
```javascript
// Basic query example
const tripDetails = await TripDetail.query().where('user_id', userId);

// Get trips within date range
const recentTrips = await TripDetail.query()
  .where('start_time', '>=', startDate)
  .where('end_time', '<=', endDate);

// Get trip details with specific mode
const transitTrips = await TripDetail.query()
  .where('mode', 'public_transit')
  .orderBy('start_time', 'desc');
```

## 🔗 Related Models
- `AuthUsers` - Many-to-one relationship via user_id
- `Trips` - Many-to-one relationship via trip_id
- `TripRoutes` - Related trip routing information

## 📌 Important Notes
- Coordinates are stored in decimal degrees format
- Duration is calculated as difference between start_time and end_time
- Mode field aligns with reservation travel modes
- Distance calculation may vary based on routing algorithm

## 🏷️ Tags
**Keywords:** trips, travel, journey, route, transportation
**Category:** #model #database #trips #mysql

---
Note: This model captures granular trip data for analytics and user history.