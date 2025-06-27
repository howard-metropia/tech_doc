# TripIncentiveLogs Model

## 📋 Model Overview
- **Purpose:** Logs trip-related incentives and rewards earned by users
- **Table/Collection:** trip_incentive_log
- **Database Type:** MySQL (portal)
- **Relationships:** None defined

## 🔧 Schema Definition
*Schema fields are not explicitly defined in the model. Database table structure would need to be verified.*

## 🔑 Key Information
- **Primary Key:** Not explicitly defined (likely `id`)
- **Indexes:** Not specified
- **Unique Constraints:** Not specified
- **Default Values:** Not specified

## 📝 Usage Examples
```javascript
// Basic query example
const incentiveLogs = await TripIncentiveLogs.query().where('user_id', 123);

// Get logs by trip
const tripLogs = await TripIncentiveLogs.query().where('trip_id', 456);
```

## 🔗 Related Models
- No explicit relationships defined
- Related to trip and incentive models

## 📌 Important Notes
- Minimal model with only table name definition
- Part of incentive tracking system
- Uses Objection.js ORM with MySQL portal database
- Logs incentive distribution for trips

## 🏷️ Tags
**Keywords:** trip, incentive, log, rewards, tracking
**Category:** #model #database #trip #incentive #log