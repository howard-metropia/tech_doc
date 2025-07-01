# HoustonMetro Model

## 📋 Model Overview
- **Purpose:** Stores Houston Metro transit real-time data and updates
- **Table/Collection:** houston_metro
- **Database Type:** MongoDB (dataset)
- **Relationships:** None defined

## 🔧 Schema Definition
- **_id** | **String** | **Required** | **Record identifier**
- **__v** | **Number** | **Optional** | **Version key**
- **stopTimeUpdate** | **Array** | **Optional** | **Stop time update information**
- **trip** | **Object** | **Optional** | **Trip information object**
  - **tripId** | **String** | **Optional** | **Trip identifier**
  - **startTime** | **String** | **Optional** | **Trip start time**
  - **startDate** | **String** | **Optional** | **Trip start date**
  - **scheduleRelationship** | **String** | **Optional** | **Schedule relationship status**
  - **routeId** | **String** | **Optional** | **Route identifier**
  - **directionId** | **Number** | **Optional** | **Direction identifier**
- **vehicle** | **Object** | **Optional** | **Vehicle information object**

## 🔑 Key Information
- **Primary Key:** _id (String)
- **Indexes:** Not specified
- **Unique Constraints:** _id
- **Default Values:** None specified

## 📝 Usage Examples
```javascript
// Find metro data by route
const routeData = await HoustonMetro.find({ 'trip.routeId': 'ROUTE_123' });

// Find by trip ID
const tripData = await HoustonMetro.findOne({ 'trip.tripId': 'TRIP_456' });

// Create new metro record
const metroRecord = new HoustonMetro({
  _id: 'RECORD_789',
  trip: {
    tripId: 'TRIP_456',
    routeId: 'ROUTE_123',
    directionId: 1
  },
  stopTimeUpdate: []
});
await metroRecord.save();
```

## 🔗 Related Models
- No explicit relationships defined
- Part of Houston Metro transit system integration

## 📌 Important Notes
- Exported as { HoustonMetro: houstonMetro }
- Stores real-time transit data from Houston Metro
- Nested schema for trip information
- Flexible vehicle object for various vehicle data
- String-based _id for external system integration

## 🏷️ Tags
**Keywords:** houston, metro, transit, realtime, gtfs, vehicle
**Category:** #model #database #houston #metro #transit #realtime #mongodb