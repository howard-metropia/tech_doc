# pmPriceObjects Model Documentation

## 📋 Model Overview
- **Purpose:** Stores parking meter price objects with detailed pricing and time information
- **Table/Collection:** pm_price_objects
- **Database Type:** MongoDB
- **Relationships:** Related to parking zones and pricing structures

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| _id | String | Yes | Unique price object identifier |
| area | String | No | Parking area identifier |
| zone | String | No | Parking zone identifier |
| paid | Boolean | No | Whether parking requires payment |
| timeBlockUnit | String | No | Time unit (minutes, hours) |
| timeBlockQuantity | String | No | Quantity of time blocks |
| timeBlockId | String | No | Time block identifier |
| price | Object | No | Pricing breakdown object |
| parkingStartTimeLocal | Date | No | Local start time |
| parkingStopTimeLocal | Date | No | Local stop time |
| isParkingAllowed | Boolean | No | Whether parking is permitted |
| parkingNotAllowedReason | String | No | Reason if parking not allowed |
| maxParkingTime | Object | No | Maximum parking duration |
| parkingStartTimeUtc | Date | No | UTC start time |
| parkingStopTimeUtc | Date | No | UTC stop time |
| timeZoneStandardName | String | No | Time zone name |
| cultureCode | String | No | Culture/locale code |
| currency | String | No | Currency code (USD, EUR, etc.) |
| currencySymbol | String | No | Currency symbol |

### Price Object Schema
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| parkingPrice | Number | No | Base parking price |
| transactionFee | Number | No | Additional transaction fee |
| totalPrice | Number | No | Total cost including fees |

### MaxParkingTime Object Schema
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| hours | Number | No | Maximum hours allowed |
| days | Number | No | Maximum days allowed |
| minutes | Number | No | Maximum minutes allowed |
| totalMinutes | Number | No | Total minutes (calculated) |

## 🔑 Key Information
- **Primary Key:** _id (string)
- **Indexes:** None explicitly defined
- **Unique Constraints:** None
- **Default Values:** Auto-generated timestamps

## 📝 Usage Examples
```javascript
// Find pricing for specific zone
const priceObjects = await PmPriceObjects.find({
  area: 'downtown',
  zone: 'zone_A',
  paid: true
});

// Get current parking prices
const currentPrices = await PmPriceObjects.find({
  parkingStartTimeUtc: { $lte: new Date() },
  parkingStopTimeUtc: { $gte: new Date() }
});
```

## 🔗 Related Models
- **ParkingZones**: Price objects belong to specific zones
- **ParkingReservations**: Pricing applied to reservations
- **ParkingTransactions**: Actual payments based on these prices

## 📌 Important Notes
- Supports complex time-based pricing structures
- Handles multiple currencies and locales
- Includes maximum parking duration enforcement
- UTC and local time tracking for accuracy
- Detailed price breakdown with fees

## 🏷️ Tags
**Keywords:** parking, pricing, meters, time-based, zones
**Category:** #model #database #parking #pricing