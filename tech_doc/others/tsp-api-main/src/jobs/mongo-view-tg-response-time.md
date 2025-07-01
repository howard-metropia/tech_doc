# Mongo View: Tow and Go Response Time

## 📋 Job Overview
- **Purpose:** Creates MongoDB view to track tow and go service response times
- **Type:** One-time migration / Manual trigger
- **Schedule:** On-demand execution
- **Impact:** MongoDB cache database - creates admin_platform_tow_and_go_response_time view

## 🔧 Technical Details
- **Dependencies:** @maas/core/mongo, cloud_message collection
- **Database Operations:** Creates/recreates MongoDB view on cache database
- **Key Operations:** Aggregates tow requests with status transitions and calculates response time

## 📝 Code Summary
```javascript
const pipeline = [
  { $match: { notification_type: 81 } },
  { $project: { tow_id: "$meta.tow_id", status: "$meta.call_third_status", create_on: "$sent_on" } },
  { $group: { _id: "$tow_id", status_two_response: {...}, status_four_response: {...} } },
  { $project: { response_time: { $divide: [{ $subtract: [...] }, 1000] } } },
  { $lookup: { from: 'tow_and_go_region_code', localField: "tow_id", as: "regionCode" } }
];
```

## ⚠️ Important Notes
- Drops and recreates view if it already exists
- Calculates response time by subtracting status 2 timestamp from status 4 timestamp
- Includes region code lookup for geographic analysis
- Response time calculated in seconds (divided by 1000)

## 📊 Example Output
```
View created: admin_platform_tow_and_go_response_time
Fields: tow_id, status, create_on, response_time, city_tag, county_tag, zipcode_tag
```

## 🏷️ Tags
**Keywords:** tow-and-go, response-time, mongodb-view, analytics, notification
**Category:** #job #mongodb-view #analytics #tow-service