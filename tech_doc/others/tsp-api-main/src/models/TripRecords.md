# TripRecords Model Documentation

## 📋 Model Overview
- **Purpose:** Stores trip record data with origin, destination, and mode information
- **Table/Collection:** trip_record
- **Database Type:** MongoDB
- **Relationships:** References users and trip data

## 🔧 Schema Definition

### Main Schema
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| _id | ObjectId | Yes | MongoDB document identifier |
| user_id | Number | No | User who made the trip |
| origin | Object | No | Trip starting position |
| destination | Object | No | Trip ending position |
| timestamp | Number | No | API execution timestamp |
| mode | String | No | Transportation mode used |
| trip_id | Number | No | Associated trip identifier |

### Position Schema (Origin/Destination)
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| timestamp | Number | No | Position timestamp |
| latitude | Number | No | Latitude coordinate |
| longitude | Number | No | Longitude coordinate |

## 🔑 Key Information
- **Primary Key:** _id (MongoDB ObjectId)
- **Indexes:** None explicitly defined
- **Unique Constraints:** None
- **Default Values:** None specified

## 📝 Usage Examples
```javascript
// Record a new trip
const tripRecord = new TripRecords({
  user_id: 12345,
  origin: {
    timestamp: Date.now(),
    latitude: 37.7749,
    longitude: -122.4194
  },
  destination: {
    timestamp: Date.now() + 1800000, // 30 minutes later
    latitude: 37.7849,
    longitude: -122.4094
  },
  timestamp: Date.now(),
  mode: 'driving',
  trip_id: 987
});
await tripRecord.save();

// Find user's recent trips
const recentTrips = await TripRecords.find({
  user_id: userId,
  timestamp: { $gte: Date.now() - 7*24*60*60*1000 } // Last 7 days
}).sort({ timestamp: -1 });
```

## 🔗 Related Models
- **AuthUsers**: Trip records belong to specific users
- **Trips**: May reference detailed trip information
- **TransportModes**: Mode field references available transport options

## 📌 Important Notes
- Uses timestamp format for all time data
- Separate position objects for origin and destination
- No version key to reduce document size
- Cache database for fast trip data access
- Flexible mode field for various transportation types

## 🏷️ Tags
**Keywords:** trips, records, origin-destination, transportation
**Category:** #model #database #trips #tracking