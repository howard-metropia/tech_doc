# Toll Schemas Documentation

### 📋 Schema Overview
- **Purpose:** Validates toll calculation and route pricing API endpoints
- **Validation Library:** Joi
- **Related Controller:** tolls.js

### 🔧 Schema Structure
```javascript
// Toll cost object
toll: {
  tagCost: number (required, nullable),
  cashCost: number (required, nullable),
  licensePlateCost: number (optional, nullable)
}

// Route with toll zones
route: {
  id: string (required, max 40 chars),
  polyline: string (required),
  staticZones: array of time objects,
  dynamicZones: array of time objects,
  departureTime: date (optional),
  arrivalTime: date (optional),
  distance: number (optional),
  occupancy: number (default 1)
}

// Main toll calculation request
getTollsByRoute: {
  routes: array of routes (min 1),
  vehicleType: number (2,3,4,5,6),
  tagInstalled: boolean,
  debug: boolean (default false)
}
```

### 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| routes | array | Yes | min 1 route | Routes for toll calculation |
| vehicleType | number | Yes | 2,3,4,5,6 | Vehicle classification |
| tagInstalled | boolean | Yes | - | Electronic toll tag presence |
| id | string | Yes | max 40 chars | Route identifier |
| polyline | string | Yes | - | Encoded route polyline |
| tagCost | number | Yes | nullable | Electronic toll cost |
| cashCost | number | Yes | nullable | Cash toll cost |
| occupancy | number | No | default 1 | Vehicle occupancy |
| debug | boolean | No | default false | Debug mode flag |

### 💡 Usage Example
```javascript
// Toll calculation request
{
  "routes": [
    {
      "id": "route_123",
      "polyline": "encoded_polyline_string",
      "staticZones": [
        {"index": 0, "time": "08:00:00"}
      ],
      "dynamicZones": [
        {"index": 1, "time": "08:15:00"}
      ],
      "distance": 25.5,
      "occupancy": 2
    }
  ],
  "vehicleType": 2,
  "tagInstalled": true,
  "debug": false
}

// TollGuru API response validation
{
  "hasTolls": true,
  "tolls": [
    {
      "tagCost": 3.25,
      "cashCost": 4.50,
      "licensePlateCost": 3.75
    }
  ]
}

// Invalid request - wrong vehicle type
{
  "routes": [...],
  "vehicleType": 1, // Error: must be 2,3,4,5,6
  "tagInstalled": true
}
```

### ⚠️ Important Validations
- Vehicle type restricted to specific classifications (2-6)
- Route ID limited to 40 characters maximum
- Toll costs are nullable but required fields
- Zone arrays contain index and time objects
- Debug and noCache flags default to false
- Routes parameter supports both full and simplified schemas
- Unknown fields allowed in toll objects for API flexibility

### 🏷️ Tags
**Keywords:** tolls, pricing, routes, vehicle-type, zones
**Category:** #schema #validation #joi #toll-schemas