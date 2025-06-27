# busTickets Model Documentation

## 📋 Model Overview
- **Purpose:** Manages transit fare mapping and Bytemark ticketing system integration
- **Table/Collection:** transit_fare_mapping, bytemark_fare
- **Database Type:** MongoDB
- **Relationships:** Maps routes to fare structures and ticketing systems

## 🔧 Schema Definition

### Transit Fare Mapping (mogonBusTickets)
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| _id | ObjectId | Yes | MongoDB document identifier |
| route_id | String | No | Transit route identifier |
| agency_id | String | No | Transit agency identifier |
| route_short_name | String | No | Short route name (e.g., "1", "A") |
| route_long_name | String | No | Full route name |
| route_type | String | No | Type of route (bus, rail, etc.) |

### Bytemark Fare (mogonBytemarkTickets)
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| _id | ObjectId | Yes | MongoDB document identifier |
| uu_id | String | No | Unique identifier for fare |
| short_description | String | No | Brief fare description |
| long_description | String | No | Detailed fare description |
| name | String | No | Fare product name |
| sale_price | Number | No | Price of the fare |

## 🔑 Key Information
- **Primary Key:** _id (MongoDB ObjectId)
- **Indexes:** None explicitly defined
- **Unique Constraints:** None
- **Default Values:** None specified

## 📝 Usage Examples
```javascript
// Find fare mapping for route
const fareMapping = await mogonBusTickets.find({
  route_id: 'route_123',
  agency_id: 'metro_transit'
});

// Get Bytemark fare products
const fares = await mogonBytemarkTickets.find({
  sale_price: { $gte: 0 }
}).sort({ sale_price: 1 });

// Create new fare mapping
const mapping = new mogonBusTickets({
  route_id: 'route_456',
  agency_id: 'city_bus',
  route_short_name: '15',
  route_long_name: 'Downtown Express',
  route_type: 'bus'
});
```

## 🔗 Related Models
- **GTFS Routes**: Transit fare mapping links to GTFS route data
- **UserTickets**: Bytemark fares used for user ticket purchases
- **PaymentTransactions**: Fare purchases create payment records

## 📌 Important Notes
- Two separate collections for different fare systems
- Transit fare mapping integrates with GTFS data standards
- Bytemark integration for mobile ticketing
- Fare pricing stored as numeric values
- Dataset database for reference data storage

## 🏷️ Tags
**Keywords:** transit, fares, tickets, bytemark, GTFS
**Category:** #model #database #transit #fares