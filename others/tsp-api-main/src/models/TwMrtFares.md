# TwMrtFares Model

## 📋 Model Overview
- **Purpose:** Stores Taiwan Metro (MRT) fare information between stations
- **Table/Collection:** metro_fare
- **Database Type:** MongoDB (dataset)
- **Relationships:** None defined

## 🔧 Schema Definition
- **_id** | **String** | **Required** | **Fare record identifier**
- **OriginStationID** | **String** | **Optional** | **Origin station identifier**
- **DestinationStationID** | **String** | **Optional** | **Destination station identifier**
- **OriginStationName** | **Object** | **Optional** | **Origin station names in multiple languages**
  - **Zh_tw** | **String** | **Optional** | **Traditional Chinese name**
  - **En** | **String** | **Optional** | **English name**
- **DestinationStationName** | **Object** | **Optional** | **Destination station names in multiple languages**
  - **Zh_tw** | **String** | **Optional** | **Traditional Chinese name**
  - **En** | **String** | **Optional** | **English name**
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
const fare = await TwMrtFares.findOne({
  OriginStationID: 'STATION_A',
  DestinationStationID: 'STATION_B'
});

// Find all fares from origin station
const originFares = await TwMrtFares.find({ OriginStationID: 'STATION_A' });

// Find fares with English station names
const faresWithEn = await TwMrtFares.find({ 'OriginStationName.En': { $exists: true } });
```

## 🔗 Related Models
- No explicit relationships defined
- Part of Taiwan transit system integration

## 📌 Important Notes
- Supports bilingual station names (Traditional Chinese and English)
- Stores fare data for Taiwan Metro (MRT) system
- String-based _id for external system integration
- Flexible Fares array for different fare types

## 🏷️ Tags
**Keywords:** taiwan, mrt, metro, fare, transit, multilingual
**Category:** #model #database #taiwan #metro #transit #fare #mongodb