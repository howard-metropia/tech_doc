# TwHsrFares Model Documentation

### 📋 Model Overview
- **Purpose:** Stores Taiwan High Speed Rail (HSR) fare information between stations
- **Table/Collection:** thsrc_fare
- **Database Type:** MongoDB
- **Relationships:** References station data through Origin/Destination Station IDs

### 🔧 Schema Definition

| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| _id | String | Yes | Document identifier |
| OriginStationID | String | No | ID of the origin station |
| DestinationStationID | String | No | ID of the destination station |
| OriginStationName.Zh_tw | String | No | Origin station name in Traditional Chinese |
| OriginStationName.En | String | No | Origin station name in English |
| DestinationStationName.Zh_tw | String | No | Destination station name in Traditional Chinese |
| DestinationStationName.En | String | No | Destination station name in English |
| Direction | Number | No | Travel direction indicator |
| Fares | Array | No | Array of fare information for different ticket types |

### 🔑 Key Information
- **Primary Key:** _id (String)
- **Indexes:** Not specified in schema
- **Unique Constraints:** Not specified
- **Default Values:** None specified

### 📝 Usage Examples
```javascript
// Find fares between two stations
const fares = await TwHsrFares.findOne({
  OriginStationID: 'station1',
  DestinationStationID: 'station2'
});

// Get all fares for a specific origin station
const originFares = await TwHsrFares.find({
  OriginStationID: 'TPE'
});

// Search by station name
const stationFares = await TwHsrFares.find({
  'OriginStationName.En': 'Taipei'
});
```

### 🔗 Related Models
- Station management models (referenced by OriginStationID/DestinationStationID)
- Transit routing models that use fare data

### 📌 Important Notes
- Uses MongoDB with 'dataset' connection
- Stores bilingual station names (Traditional Chinese and English)
- Fares array structure not specified - likely contains different fare types
- Direction field helps distinguish between northbound/southbound routes
- Used for Taiwan HSR fare calculation and display in transit routing

### 🏷️ Tags
**Keywords:** taiwan, hsr, high-speed-rail, fares, transit, stations
**Category:** #model #database #mongodb #taiwan #transit #fares