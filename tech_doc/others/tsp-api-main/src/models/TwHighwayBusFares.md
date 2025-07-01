# Model Documentation: TwHighwayBusFares

## 📋 Model Overview
- **Purpose:** Manages Taiwan highway bus fare information including pricing by stages/stops
- **Table/Collection:** intercity_bus_fare
- **Database Type:** MongoDB
- **Relationships:** None defined in model

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| _id | String | Yes | MongoDB document ID |
| FarePricingType | Number | No | Type of fare pricing model |
| IsForAllSubRoutes | Number | No | Flag indicating if fare applies to all sub-routes |
| IsFreeBus | Number | No | Flag for free bus service |
| OperatorID | String | No | Bus operator identifier |
| OperatorNo | String | No | Bus operator number |
| RouteID | String | No | Bus route identifier |
| RouteName | String | No | Bus route name |
| StageFares | Array | No | Array of stage-based fare information |
| StageFares.Direction | Number | No | Travel direction (0/1) |
| StageFares.OriginStage | Object | No | Origin stop information |
| StageFares.OriginStage.StopID | String | No | Origin stop identifier |
| StageFares.OriginStage.StopName | String | No | Origin stop name |
| StageFares.DestinationStage | Object | No | Destination stop information |
| StageFares.DestinationStage.StopID | String | No | Destination stop identifier |
| StageFares.DestinationStage.StopName | String | No | Destination stop name |
| StageFares.Fares | Array | No | Fare amounts array |
| SubRouteID | String | No | Sub-route identifier |
| SubRouteName | String | No | Sub-route name |

## 🔑 Key Information
- **Primary Key:** _id
- **Indexes:** Default MongoDB _id index
- **Unique Constraints:** None specified
- **Default Values:** None specified

## 📝 Usage Examples
```javascript
// Find fares for a specific route
const fares = await TwHighwayBusFares.findOne({ RouteID: 'R0001' });

// Find all free bus routes
const freeBuses = await TwHighwayBusFares.find({ IsFreeBus: 1 });

// Find fares between specific stops
const stageFare = await TwHighwayBusFares.findOne({
  'StageFares.OriginStage.StopID': 'S001',
  'StageFares.DestinationStage.StopID': 'S002'
});
```

## 🔗 Related Models
- No direct model relationships defined

## 📌 Important Notes
- Uses MongoDB 'dataset' connection
- Fare pricing can vary by direction and stage
- IsFreeBus and IsForAllSubRoutes are numeric flags (0/1)
- StageFares contains origin-destination pairs with fare information

## 🏷️ Tags
**Keywords:** highway bus, intercity, fare, pricing, Taiwan, transit
**Category:** #model #database #transportation #fare-management

---