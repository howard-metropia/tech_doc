# MongoPTX Model Documentation

## 📋 Model Overview
- **Purpose:** Manages bus intercity fares and bike station data for Taiwan PTX (Public Transport eXchange) system
- **Table/Collection:** bus_intercityfares, ubike_stations
- **Database Type:** MongoDB
- **Relationships:** Transit fare structures and bike sharing stations

## 🔧 Schema Definition

### Bus InterCity Fares (BusInterCityFares)
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| _id | ObjectId | Yes | MongoDB document identifier |
| RouteID | String | No | Bus route identifier |
| SubRouteName | String | No | Sub-route name |
| StageFares | Array | No | Fare stages array |

### Stage Fares Object
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| Direction | Number | No | Direction (0=outbound, 1=inbound) |
| OriginStage | Object | No | Origin stage info |
| DestinationStage | Object | No | Destination stage info |
| Fares | Array | No | Fare amounts array |

### Bike Stations (BikeStations)
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| _id | Number | Yes | Station ID number |
| StationUID | String | No | Unique station identifier |
| StationID | Number | No | Numeric station ID |
| AvailableRentBikes | Number | No | Available bikes for rent |
| AvailableReturnBikes | Number | No | Available docking spaces |
| StationPosition | Object | No | Geographic position |
| StationName | Object | No | Multilingual station name |
| ServiceAvailable | Number | No | Service availability status |

### Station Position Object
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| PositionLon | Number | No | Longitude coordinate |
| PositionLat | Number | No | Latitude coordinate |
| GeoHash | String | No | GeoHash for location |

### Station Name Object
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| Zh_tw | String | No | Chinese (Traditional) name |
| En | String | No | English name |

## 🔑 Key Information
- **Primary Key:** _id (ObjectId for fares, Number for stations)
- **Indexes:** None explicitly defined
- **Unique Constraints:** None
- **Default Values:** None specified

## 📝 Usage Examples
```javascript
// Get bus fare information
const fares = await BusInterCityFares.find({
  RouteID: 'route_taipei_taichung'
});

// Find nearby bike stations
const stations = await BikeStations.find({
  'StationPosition.PositionLat': { $gte: 25.0, $lte: 25.1 },
  'StationPosition.PositionLon': { $gte: 121.5, $lte: 121.6 },
  ServiceAvailable: 1
});

// Get stations with available bikes
const availableStations = await BikeStations.find({
  AvailableRentBikes: { $gt: 0 }
});
```

## 🔗 Related Models
- **Transit Routes**: Bus fare data relates to route information
- **Bike Sharing Systems**: Station data for bike availability
- **User Reservations**: Bike station availability affects reservations

## 📌 Important Notes
- Taiwan-specific public transport data integration
- Multilingual support for station names (Chinese/English)
- Real-time bike availability tracking
- Flexible fare structure with stage-based pricing
- GeoHash support for efficient location queries

## 🏷️ Tags
**Keywords:** PTX, Taiwan, bus-fares, bike-stations, multilingual
**Category:** #model #database #taiwan #transit #bikes