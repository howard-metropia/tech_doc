# Construction Zone Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates construction zone alerts, events, and notifications for traffic management
- **Validation Library:** Joi with custom GeoJSON validation
- **Related Controller:** Construction Zone controller for traffic alerts and road closures

## 🔧 Schema Structure
```javascript
// Construction alerts schema
{
  routes: Joi.array().items({
    id: Joi.string().required(),
    polyline: Joi.array().items(Joi.string()),
    travel_mode: Joi.number().integer().min(0).max(6).required(),
    arrival_time: Joi.number().integer(),
    departure_time: Joi.number().integer(),
    destination_name: Joi.string().required()
  }).min(1).required(),
}

// Construction events schema
{
  events: Joi.array().items({
    id: Joi.string(),
    location: Joi.string().required(),
    roadway_names: Joi.array().items(Joi.string()).required(),
    status: Joi.string().valid("planned", "pending", "active", "completed", "cancelled"),
    impacted_level: Joi.string().valid("far", "medium", "near").required(),
    direction: Joi.string().valid("northbound", "eastbound", "southbound", "westbound", "undefined", "unknown", "inner-loop", "outer-loop").required(),
    lanes: Joi.string().valid("all-lanes-closed", "some-lanes-closed", "all-lanes-open", "alternating-one-way", "some-lanes-closed-merge-left", "some-lanes-closed-merge-right", "all-lanes-open-shift-left", "all-lanes-open-shift-right", "some-lanes-closed-split", "flagging", "temporary-traffic-signal", "unknown").required(),
    lat: Joi.number().required(),
    lng: Joi.number().required(),
    geometry: geoJson,
  }).min(1).required(),
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| routes | array | Yes | Min 1 item | Route information for alerts |
| travel_mode | number | Yes | Integer: 0-6 | Transportation mode |
| destination_name | string | Yes | Any string | Route destination |
| events | array | Yes | Min 1 item | Construction event details |
| location | string | Yes | Any string | Construction site location |
| roadway_names | array | Yes | String array | Affected road names |
| impacted_level | string | Yes | far/medium/near | Traffic impact severity |
| direction | string | Yes | Predefined values | Traffic direction affected |
| lanes | string | Yes | Predefined values | Lane closure status |
| lat/lng | number | Yes | Valid coordinates | Geographic location |
| geometry | object | No | Valid GeoJSON | Construction zone geometry |

## 💡 Usage Example
```javascript
// Construction alerts request
{
  "routes": [
    {
      "id": "route_001",
      "polyline": ["encoded_polyline_string"],
      "travel_mode": 0,
      "arrival_time": 1640995200,
      "departure_time": 1640991600,
      "destination_name": "Downtown Office"
    }
  ]
}

// Construction events request
{
  "events": [
    {
      "id": "event_001",
      "location": "I-95 North between Exit 12 and Exit 15",
      "roadway_names": ["I-95", "Interstate 95"],
      "status": "active",
      "impacted_level": "medium",
      "direction": "northbound",
      "lanes": "some-lanes-closed",
      "lat": 39.7392,
      "lng": -104.9903,
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[-104.9903, 39.7392], [-104.9900, 39.7395], [-104.9897, 39.7392], [-104.9903, 39.7392]]]
      }
    }
  ]
}

// Request that fails validation
{
  "events": [
    {
      "location": "Main Street",
      "roadway_names": ["Main St"],
      "impacted_level": "high", // Error: must be far/medium/near
      "direction": "northbound",
      "lanes": "some-lanes-closed",
      "lat": 39.7392,
      "lng": -104.9903
    }
  ]
}
```

## ⚠️ Important Validations
- Travel mode must be integer between 0-6 (different transportation types)
- Impact level restricted to 'far', 'medium', 'near' for consistent classification
- Direction must be one of 8 predefined compass/loop directions
- Lane status must be one of 13 predefined traffic management scenarios
- Custom GeoJSON validation ensures valid geographic data format
- Arrays must contain at least one item for routes and events

## 🏷️ Tags
**Keywords:** construction-zone, traffic-alerts, road-closures, geojson, lane-management
**Category:** #schema #validation #joi #construction-zone