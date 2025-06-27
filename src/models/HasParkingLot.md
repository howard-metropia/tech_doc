# HasParkingLot Model

## 📋 Model Overview
- **Purpose:** Stores parking lot availability and metadata information
- **Table/Collection:** has_parking_lots
- **Database Type:** MongoDB (dataset)
- **Relationships:** None defined

## 🔧 Schema Definition
- **parkinglot_uid** | **String** | **Required** | **Unique parking lot identifier**
- **[dynamic fields]** | **Mixed** | **Optional** | **Flexible schema allows additional fields**
- **createdAt** | **Date** | **Auto** | **Record creation timestamp**
- **updatedAt** | **Date** | **Auto** | **Record update timestamp**

## 🔑 Key Information
- **Primary Key:** MongoDB ObjectId
- **Indexes:** parkinglot_uid (unique index)
- **Unique Constraints:** parkinglot_uid
- **Default Values:** Automatic timestamps

## 📝 Usage Examples
```javascript
// Find parking lot by UID
const parkingLot = await InrixParkingLot.findOne({ parkinglot_uid: 'LOT_123' });

// Create new parking lot
const newLot = new InrixParkingLot({
  parkinglot_uid: 'LOT_456',
  name: 'Downtown Garage',
  capacity: 200
});
await newLot.save();

// Find all parking lots
const allLots = await InrixParkingLot.find({});
```

## 🔗 Related Models
- No explicit relationships defined
- Part of parking service integration

## 📌 Important Notes
- Uses flexible schema (strict: false) for dynamic data structure
- Unique index on parkinglot_uid ensures no duplicates
- Automatic timestamp management
- Auto-indexing enabled for performance
- Model name exported as InrixParkingLot

## 🏷️ Tags
**Keywords:** parking, lot, inrix, availability, capacity
**Category:** #model #database #parking #inrix #capacity #mongodb