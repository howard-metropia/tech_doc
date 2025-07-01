# TwTraFares Model

## 📋 Model Overview
- **Purpose:** Stores Taiwan Railway (TRA) fare information between stations
- **Table/Collection:** tra_fare
- **Database Type:** MongoDB (dataset)
- **Relationships:** None defined

## 🔧 Schema Definition
- **_id** | **String** | **Required** | **Fare record identifier**
- **OriginStationID** | **String** | **Optional** | **Origin station identifier**
- **DestinationStationID** | **String** | **Optional** | **Destination station identifier**
- **Direction** | **Number** | **Optional** | **Travel direction indicator**
- **Fares** | **Array** | **Optional** | **Fare information array**

## 🔑 Key Information
- **Primary Key:** _id (String)
- **Indexes:** Not specified
- **Unique Constraints:** _id
- **Default Values:** None specified

## 📝 Usage Examples
```javascript
// Find fare between stations
const fare = await TwTraFares.findOne({
  OriginStationID: 'STATION_A',
  DestinationStationID: 'STATION_B'
});

// Find all fares from origin
const originFares = await TwTraFares.find({ OriginStationID: 'STATION_A' });
```

## 🔗 Related Models
- No explicit relationships defined
- Part of Taiwan transit system integration

## 📌 Important Notes
- Taiwan Railway (TRA) fare data storage
- String-based _id for external system integration
- Flexible Fares array for different fare types
- Dataset database for reference data

## 🏷️ Tags
**Keywords:** taiwan, tra, railway, fare, transit
**Category:** #model #database #taiwan #railway #transit #fare #mongodb