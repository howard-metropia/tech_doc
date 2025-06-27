# MTC (Message Results) Model Documentation

## 📋 Model Overview
- **Purpose:** Stores MTC (Metropolitan Transportation Commission) message results and location data
- **Table/Collection:** message_results
- **Database Type:** MongoDB (cache database)
- **Relationships:** Embedded Location documents within Record subdocuments

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| user_id | Number | No | User identifier |
| records | Array[Record] | No | Array of trip records |

### Record Subdocument Schema
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| origin | Location | No | Trip origin location |
| destination | Location | No | Trip destination location |
| departure_time | Date | No | Departure timestamp |
| eta_time | Number | No | Estimated time of arrival (minutes) |
| eta_distance | Number | No | Estimated distance (miles/km) |
| plan_id | String | No | Trip plan identifier |
| message_id | Number | No | Message identifier |
| user_id | Number | No | User identifier |
| created_on | Date | No | Record creation timestamp |

### Location Subdocument Schema
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| name | String | No | Location name/label |
| address | String | No | Full address string |
| latitude | Number | No | Geographic latitude |
| longitude | Number | No | Geographic longitude |

## 🔑 Key Information
- **Primary Key:** _id (MongoDB ObjectId)
- **Indexes:** user_id, records.message_id
- **Unique Constraints:** None
- **Default Values:** None specified

## 📝 Usage Examples
```javascript
// Basic query example
const messages = await MessageResults.find({ user_id: 12345 });

// Find records by plan_id
const planRecords = await MessageResults.find({
  'records.plan_id': 'PLAN123'
});

// Query by location proximity
const nearbyRecords = await MessageResults.find({
  'records.origin.latitude': { $gte: 37.7, $lte: 37.8 },
  'records.origin.longitude': { $gte: -122.5, $lte: -122.4 }
});
```

## 🔗 Related Models
- `AuthUsers` - Referenced by user_id field
- Trip planning and routing services may reference plan_id

## 📌 Important Notes
- MongoDB flexible schema allows for additional fields
- Location coordinates use decimal degrees format
- ETA fields store estimates at time of message creation
- Used for caching and quick retrieval of MTC communications

## 🏷️ Tags
**Keywords:** mtc, messages, locations, cache, mongodb
**Category:** #model #database #cache #mongodb

---
Note: This model serves as a cache for MTC message results and trip planning data.