# Mongo View: School Zone Events

## 📋 Job Overview
- **Purpose:** Creates MongoDB view to track school zone entry events and speeding violations
- **Type:** One-time migration / Manual trigger
- **Schedule:** On-demand execution
- **Impact:** MongoDB cache database - creates admin_platform_school_zone view

## 🔧 Technical Details
- **Dependencies:** @maas/core/mongo, user_actions collection, userActionList defines
- **Database Operations:** Drops and recreates MongoDB view on cache database
- **Key Operations:** Filters school zone events, formats data with region information

## 📝 Code Summary
```javascript
const pipeline = [
  { $match: { $or: [
    { action: userActionList.enterSchoolZone },
    { action: userActionList.enterSchoolZoneSpeeding }
  ]}},
  { $addFields: { event_time: { $dateFromString: { dateString: '$attributes.event_time' }}}},
  { $project: { action: 1, event_time: 1, school_zone_id: 1, trip_id: 1, region_info: 1 }}
];
```

## ⚠️ Important Notes
- Tracks both regular school zone entries and speeding violations
- Converts event_time string to proper Date object
- Includes geographic region tagging (city, county, zipcode)
- Drops existing view before creating new one to ensure clean state

## 📊 Example Output
```
View created: admin_platform_school_zone
Fields: event_name, event_time, school_zone_id, trip_id, city_tag, county_tag, zipcode_tag
Action types: enterSchoolZone, enterSchoolZoneSpeeding
```

## 🏷️ Tags
**Keywords:** school-zone, safety, speeding, user-actions, mongodb-view
**Category:** #job #mongodb-view #safety #school-zone #user-tracking