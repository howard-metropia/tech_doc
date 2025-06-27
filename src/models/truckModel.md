# Model Documentation: TruckModel

## 📋 Model Overview
- **Purpose:** Stores truck map data and routing information
- **Table/Collection:** truck_map
- **Database Type:** MongoDB
- **Relationships:** None defined

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| _id | ObjectId | Yes | MongoDB document ID (auto-generated) |
| truck_map | Object | Yes | Truck map/routing data |
| created_at | Date | Yes | UTC timestamp of creation |

## 🔑 Key Information
- **Primary Key:** _id (auto-generated ObjectId)
- **Indexes:** Default MongoDB _id index
- **Unique Constraints:** None specified
- **Default Values:** 
  - _id: auto-generated
  - created_at: current UTC timestamp

## 📝 Usage Examples
```javascript
const { truckMapSchema } = require('./truckModel');

// Create new truck map entry
const newTruckMap = await truckMapSchema.create({
  truck_map: {
    route: 'A to B',
    distance: 150,
    restrictions: ['height', 'weight']
  }
});

// Find truck maps by date range
const recentMaps = await truckMapSchema.find({
  created_at: { $gte: new Date('2024-01-01') }
});

// Update truck map data
await truckMapSchema.findByIdAndUpdate(id, {
  truck_map: updatedMapData
});
```

## 🔗 Related Models
- No direct model relationships defined

## 📌 Important Notes
- Uses MongoDB 'cache' connection
- Exports as object with truckMapSchema property
- Uses moment-timezone for UTC timestamp handling
- truck_map field stores flexible JSON object data

## 🏷️ Tags
**Keywords:** truck, routing, map, logistics, freight
**Category:** #model #database #transportation #mongodb

---