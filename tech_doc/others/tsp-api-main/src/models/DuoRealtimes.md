# DuoRealtimes Model

## 📋 Model Overview
- **Purpose:** Manages real-time data for Duo carpool/rideshare system
- **Table/Collection:** duo_realtime
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
const realtimeData = await DuoRealtimes.query().where('status', 'active');

// Get real-time data by trip
const tripData = await DuoRealtimes.query().where('trip_id', 123);
```

## 🔗 Related Models
- No explicit relationships defined
- Part of Duo real-time tracking system

## 📌 Important Notes
- Minimal model with only table name definition
- Part of real-time carpool/rideshare tracking
- Uses Objection.js ORM with MySQL portal database

## 🏷️ Tags
**Keywords:** duo, realtime, carpool, tracking, live
**Category:** #model #database #duo #realtime #tracking