# Bus Schedule Schema Documentation

### 📋 Schema Overview
- **Purpose:** Validates bus route and schedule lookup API endpoints
- **Validation Library:** Joi
- **Related Controller:** busSchedule.js

### 🔧 Schema Structure
```javascript
// Path parameters for route lookup
pathParamsRouteID: {
  routeID: string (required)
}

// Path parameters for stop schedule
pathParamsStopID: {
  routeID: string (required),
  tripID: string (required),
  stopID: string (required),
  direction: number (0-1, required)
}

// Add route to favorites
postBusRouteFavorite: {
  agencyID: string (required),
  routeID: string (required)
}

// Remove route from favorites
deleteBusRouteFavorite: {
  agencyID: string (required),
  routeID: string (required)
}
```

### 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| routeID | string | Yes | - | Bus route identifier |
| tripID | string | Yes | - | Specific trip identifier |
| stopID | string | Yes | - | Bus stop identifier |
| direction | number | Yes | integer, 0-1 | Route direction (0=inbound, 1=outbound) |
| agencyID | string | Yes | - | Transit agency identifier |

### 💡 Usage Example
```javascript
// Route lookup path parameters
{
  "routeID": "ROUTE_101"
}

// Stop schedule path parameters
{
  "routeID": "ROUTE_101",
  "tripID": "TRIP_456",
  "stopID": "STOP_789",
  "direction": 0
}

// Add route to favorites
{
  "agencyID": "METRO_TRANSIT",
  "routeID": "ROUTE_101"
}

// Remove route from favorites
{
  "agencyID": "METRO_TRANSIT",
  "routeID": "ROUTE_101"
}

// Invalid request - direction out of range
{
  "routeID": "ROUTE_101",
  "tripID": "TRIP_456",
  "stopID": "STOP_789",
  "direction": 2 // Error: must be 0 or 1
}
```

### ⚠️ Important Validations
- All route and trip identifiers are strings (not numbers)
- Direction must be exactly 0 (inbound) or 1 (outbound)
- Favorite operations require both agencyID and routeID
- Path parameters use specific validation schemas for different endpoints
- Trip ID was changed from number to string (see commented line)

### 🏷️ Tags
**Keywords:** bus, transit, schedule, gtfs, favorites, routes
**Category:** #schema #validation #joi #bus-schedule