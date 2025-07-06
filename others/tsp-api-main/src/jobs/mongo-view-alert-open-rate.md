# Mongo View: Alert Open Rate Analytics

## 📋 Job Overview
- **Purpose:** Creates MongoDB view to track alert notification open rates and click analytics
- **Type:** One-time migration / Manual trigger
- **Schedule:** On-demand execution
- **Impact:** MongoDB cache database - creates admin_platform_alert_open_rate view

## 🔧 Technical Details
- **Dependencies:** @maas/core/mongo, notification_record and user_actions collections
- **Database Operations:** Creates/recreates MongoDB view with lookup join
- **Key Operations:** Joins notification records with user action clicks to calculate engagement metrics

## 📝 Code Summary
```javascript
const pipeline = [
  { $lookup: { from: 'user_actions', localField: "event_id", foreignField: "attributes.event_id", as: "userActionsDocs" }},
  { $group: { _id: "$event_id", user_ids: { $addToSet: "$user_id" }, action_records: {$addToSet: "$userActionsDocs._id"} }},
  { $project: { total_click_counts: { $size: {$arrayElemAt: ["$action_records", 0]}}, impact_user_count: { $size: "$user_ids" } }}
];
```

## ⚠️ Important Notes
- Calculates both total click counts and unique user impact
- Includes geographic data (lat, lng, region tags) for location-based analysis
- Drops and recreates view if it already exists
- Provides engagement metrics for alert effectiveness measurement

## 📊 Example Output
```
View created: admin_platform_alert_open_rate
Fields: event_id, lat, lng, event_type, send_time, total_click_counts, impact_user_count, geographic_tags
```

## 🏷️ Tags
**Keywords:** alert-analytics, open-rate, engagement, notifications, user-actions
**Category:** #job #mongodb-view #analytics #notifications #engagement