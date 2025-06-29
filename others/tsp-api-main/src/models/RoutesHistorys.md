# Model Documentation: RoutesHistorys

## 📋 Model Overview
- **Purpose:** Stores user route history including trip details, costs, and travel information
- **Table/Collection:** routes_history
- **Database Type:** MongoDB
- **Relationships:** References users by user_id

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| id | String | No | Document ID (maps to _id) |
| user_id | String | No | User identifier |
| history | Array | No | Array of route history entries |
| history.transfers | Number | No | Number of transfers (轉乘次數) |
| history.generalized_cost | Number | No | Cost for routing algorithm (引擎演算法使用) |
| history.sections | Array | No | Route sections |
| history.total_travel_meters | Number | No | Total distance in meters |
| history.total_price | Number | No | Total fare price (總票價) |
| history.travel_mode | String | No | Mode of transportation |
| history.trip_detail_uuid | String | No | Unique trip identifier |
| history.started_on | String | No | Trip start time (UTC format) |
| history.ended_on | String | No | Trip end time (UTC format) |
| history.total_travel_time | Number | No | Total time in seconds (單位是秒) |
| addedAt | Date | Auto | Creation timestamp |
| modifiedAt | Date | Auto | Last modification timestamp |

## 🔑 Key Information
- **Primary Key:** id (mapped to _id)
- **Indexes:** Default MongoDB _id index
- **Unique Constraints:** None specified
- **Default Values:** Timestamps auto-generated

## 📝 Usage Examples
```javascript
const { RoutesHistorys } = require('./RoutesHistorys');

// Add route history for user
await RoutesHistorys.create({
  user_id: '12345',
  history: [{
    transfers: 2,
    total_travel_meters: 5000,
    total_price: 25,
    travel_mode: 'transit',
    started_on: '2024-01-01T10:00:00+00:00',
    ended_on: '2024-01-01T10:45:00+00:00',
    total_travel_time: 2700
  }]
});

// Get user's route history
const userHistory = await RoutesHistorys.findOne({ user_id: '12345' });

// Add new history entry
await RoutesHistorys.findOneAndUpdate(
  { user_id: '12345' },
  { $push: { history: newRouteEntry } }
);
```

## 🔗 Related Models
- AuthUsers - user_id references user records
- TripDetails - trip_detail_uuid may reference trip details

## 📌 Important Notes
- Uses MongoDB 'cache' connection
- Chinese comments preserved in schema
- Time format for started_on/ended_on: "2022-04-28T12:11:59+00:00"
- No version key tracking
- Custom timestamp field names (addedAt, modifiedAt)

## 🏷️ Tags
**Keywords:** routes, history, trips, travel, navigation
**Category:** #model #database #routing #history #mongodb

---