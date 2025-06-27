# UberApiPayload Model Documentation

## 📋 Model Overview
- **Purpose:** Logs Uber API requests and responses for debugging and audit purposes
- **Table/Collection:** uber_api_payload
- **Database Type:** MongoDB
- **Relationships:** None (audit/logging model)

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| _id | ObjectId | Yes | MongoDB document identifier |
| method | String | No | HTTP method (GET, POST, etc.) |
| url | String | No | API endpoint URL |
| fare_id | String | No | Associated fare identifier |
| request | Object | No | Complete request payload |
| response | Object | No | Complete response payload |
| created_at | Date | No | Request timestamp (default: now) |

## 🔑 Key Information
- **Primary Key:** _id (MongoDB ObjectId)
- **Indexes:** None explicitly defined
- **Unique Constraints:** None
- **Default Values:** created_at defaults to Date.now

## 📝 Usage Examples
```javascript
// Log Uber API call
const payload = new UberApiPayload({
  method: 'POST',
  url: '/v1.2/requests/estimate',
  fare_id: 'fare_123',
  request: { 
    start_latitude: 37.7752315,
    start_longitude: -122.418075 
  },
  response: { 
    fare: { value: 1250, currency_code: 'USD' }
  }
});
await payload.save();

// Find requests by fare ID
const fareRequests = await UberApiPayload.find({
  fare_id: 'fare_123'
}).sort({ created_at: -1 });
```

## 🔗 Related Models
- **RidehailTrips**: fare_id may reference ridehail trip records
- **UserFares**: Associated with fare calculations

## 📌 Important Notes
- Used for debugging Uber API integration issues
- Stores complete request/response cycles for troubleshooting
- No version key to reduce document size
- Consider TTL index for automatic cleanup of old logs

## 🏷️ Tags
**Keywords:** uber-api, logging, debugging, ridehail
**Category:** #model #database #logging #ridehail