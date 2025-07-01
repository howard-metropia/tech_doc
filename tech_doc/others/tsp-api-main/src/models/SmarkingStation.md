# SmarkingStation Model

## 📋 Model Overview
- **Purpose:** Stores detailed parking station information from Smarking provider
- **Table/Collection:** smarking_station
- **Database Type:** MongoDB (dataset)
- **Relationships:** None defined

## 🔧 Schema Definition
- **station_id** | **Number** | **Optional** | **Station identifier**
- **address** | **String** | **Optional** | **Station address**
- **city** | **String** | **Optional** | **City location**
- **latitude** | **Number** | **Optional** | **Station latitude**
- **longitude** | **Number** | **Optional** | **Station longitude**
- **[additional fields]** | **Mixed** | **Optional** | **Other station attributes omitted in code**

## 🔑 Key Information
- **Primary Key:** MongoDB ObjectId
- **Indexes:** Not specified
- **Unique Constraints:** Not specified
- **Default Values:** None specified

## 📝 Usage Examples
```javascript
// Find station by ID
const station = await SmarkingStation.findOne({ station_id: 123 });

// Find stations in city
const cityStations = await SmarkingStation.find({ city: 'Houston' });

// Find nearby stations
const nearbyStations = await SmarkingStation.find({
  latitude: { $gte: 29.7, $lte: 29.8 },
  longitude: { $gte: -95.4, $lte: -95.3 }
});
```

## 🔗 Related Models
- No explicit relationships defined
- Part of parking service integration

## 📌 Important Notes
- More detailed schema than the base smarking model
- Exported as { SmarkingStation } object
- Collection name explicitly set to 'smarking_station'
- Schema includes location and address information

## 🏷️ Tags
**Keywords:** smarking, parking, station, location, provider
**Category:** #model #database #parking #smarking #station #mongodb