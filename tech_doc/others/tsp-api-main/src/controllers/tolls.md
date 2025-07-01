# TSP API Tolls Controller Documentation

## 🔍 Quick Summary (TL;DR)
The tolls controller provides toll cost calculation for route planning, integrating with TollGuru API to deliver accurate toll pricing information for different vehicle types and payment methods.

**Keywords:** toll-calculation | route-tolls | tollguru | toll-pricing | route-planning | vehicle-tolls | toll-estimation | toll-roads

**Primary use cases:** Calculating toll costs for planned routes, estimating toll expenses, integrating toll data into route planning, providing cost-aware navigation

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, TollGuru API integration

## ❓ Common Questions Quick Index
- **Q: What toll services are supported?** → TollGuru API for comprehensive toll data
- **Q: Can I specify vehicle type?** → Yes, different vehicle types have different toll rates
- **Q: Are toll tags supported?** → Yes, toll tag discounts are factored into calculations
- **Q: How are routes specified?** → Via coordinates/waypoints in the request body
- **Q: Is real-time pricing available?** → Yes, when departure time is specified
- **Q: What regions are supported?** → Based on TollGuru coverage (North America primarily)

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **toll cost calculator** for your road trips. Before you drive somewhere, this service tells you exactly how much you'll pay in tolls based on your route, what kind of vehicle you're driving, and whether you have a toll tag. It's like having a smart assistant that knows all the toll prices on every highway and can estimate your total toll costs before you start driving.

**Technical explanation:** 
A Koa.js REST controller that provides toll cost estimation services by integrating with TollGuru API. It processes route data with vehicle specifications and toll tag information to return accurate toll calculations, supporting both real-time and static toll pricing based on departure time availability.

**Business value explanation:**
Essential for cost-aware route planning and transportation budgeting. Enables users to make informed decisions about route selection based on toll costs, supports expense tracking for business travel, and improves user experience by providing transparent cost information upfront.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/tolls.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** Toll Calculation Controller
- **File Size:** ~1.0 KB
- **Complexity Score:** ⭐⭐ (Low-Medium - External API integration with conditional logic)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `@app/src/middlewares/auth`: JWT authentication (**Critical**)
- `@app/src/schemas/toll-schemas`: Input validation schemas (**Critical**)
- `@app/src/services/toll`: Core toll calculation service (**Critical**)
- `@app/src/services/tollguru`: TollGuru API integration (**Critical**)
- `@app/src/helpers/fields-of-header`: Header field extraction (**High**)
- `@maas/core/response`: Standardized response formatting (**High**)

## 📝 Detailed Code Analysis

### Get Tolls by Route Endpoint (`POST /tolls/route`)

**Purpose:** Calculates toll costs for specified routes with vehicle and payment method considerations

**Processing Logic:**
The controller implements dual processing paths based on departure time availability:

**Path 1: Real-time Toll Calculation (with departureTime)**
```javascript
if (input.routes[0].departureTime) {
  const result = await service.getTollsByRoute(input);
  ctx.body = success(result);
}
```

**Path 2: Static Toll Calculation (without departureTime)**
```javascript
else {
  const { routes, vehicleType, tagInstalled } = ctx.request.body;
  const response = await tollGuruRoute({
    routes,
    vehicleType,
    tagInstalled,
  });
  ctx.body = success({ response });
}
```

### Input Validation Flow
```javascript
const input = await inputValidator.getTollsByRoute.validateAsync({
  ...fetchFieldsFromHeader(ctx.request.header),
  ...ctx.request.body,
});
```

**Header Fields Integration:**
- Extracts relevant fields from request headers
- Merges with request body for comprehensive input validation
- Ensures all required toll calculation parameters are present

## 🚀 Usage Methods

### Calculate Tolls with Departure Time
```bash
curl -X POST "https://api.tsp.example.com/api/v2/tolls/route" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "routes": [
      {
        "departureTime": "2024-06-25T08:00:00Z",
        "origin": {
          "lat": 37.7749,
          "lng": -122.4194
        },
        "destination": {
          "lat": 37.4419,
          "lng": -122.1430
        },
        "waypoints": []
      }
    ],
    "vehicleType": "car",
    "tagInstalled": true
  }'
```

### Calculate Static Tolls (No Departure Time)
```bash
curl -X POST "https://api.tsp.example.com/api/v2/tolls/route" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "routes": [
      {
        "origin": {
          "lat": 40.7128,
          "lng": -74.0060
        },
        "destination": {
          "lat": 40.6782,
          "lng": -73.9442
        }
      }
    ],
    "vehicleType": "truck",
    "tagInstalled": false
  }'
```

### Multi-Route Toll Calculation
```bash
curl -X POST "https://api.tsp.example.com/api/v2/tolls/route" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "routes": [
      {
        "departureTime": "2024-06-25T14:30:00Z",
        "origin": {"lat": 34.0522, "lng": -118.2437},
        "destination": {"lat": 32.7157, "lng": -117.1611},
        "waypoints": [
          {"lat": 33.6846, "lng": -117.8265}
        ]
      }
    ],
    "vehicleType": "motorcycle",
    "tagInstalled": true
  }'
```

## 📊 Output Examples

### Real-time Toll Calculation Response
```json
{
  "result": "success",
  "data": {
    "totalTollCost": 12.75,
    "currency": "USD",
    "routes": [
      {
        "routeIndex": 0,
        "tolls": [
          {
            "name": "Golden Gate Bridge",
            "cost": 8.20,
            "tagCost": 8.20,
            "cashCost": 8.60,
            "location": {
              "lat": 37.8199,
              "lng": -122.4783
            }
          },
          {
            "name": "Bay Bridge",
            "cost": 4.55,
            "tagCost": 4.55,
            "cashCost": 7.00,
            "location": {
              "lat": 37.7983,
              "lng": -122.3778
            }
          }
        ],
        "departureTime": "2024-06-25T08:00:00Z",
        "summary": {
          "distance": "45.2 miles",
          "duration": "52 minutes"
        }
      }
    ]
  }
}
```

### Static Toll Calculation Response
```json
{
  "result": "success",
  "data": {
    "response": {
      "tollCost": 8.75,
      "currency": "USD",
      "vehicleType": "truck",
      "tagInstalled": false,
      "tolls": [
        {
          "name": "Holland Tunnel",
          "cost": 8.75,
          "type": "tunnel",
          "discountAvailable": true
        }
      ],
      "route": {
        "distance": "8.5 miles",
        "duration": "25 minutes"
      }
    }
  }
}
```

### Validation Error Response
```json
{
  "error": "ValidationError",
  "message": "Invalid input parameters",
  "details": [
    {
      "field": "routes[0].origin.lat",
      "message": "Latitude must be between -90 and 90"
    },
    {
      "field": "vehicleType",
      "message": "Vehicle type must be one of: car, truck, motorcycle, bus"
    }
  ]
}
```

## ⚠️ Important Notes

### Vehicle Type Support
Common vehicle types and their toll implications:
- **car**: Standard passenger vehicle rates
- **truck**: Commercial vehicle rates (higher costs)
- **motorcycle**: Often reduced rates or exemptions
- **bus**: May have special commercial rates
- **rv**: Recreational vehicle rates (often similar to trucks)

### Toll Tag Benefits
- **Cost Savings**: Tag users often pay reduced rates
- **Convenience**: Automatic payment processing
- **Time Savings**: No need to stop at toll booths
- **Discounts**: Many toll authorities offer tag user discounts

### Processing Paths

**Real-time Processing (with departureTime):**
- Uses internal toll service for real-time calculations
- Factors in time-of-day pricing
- May include traffic-based toll adjustments
- Provides more accurate cost estimates

**Static Processing (without departureTime):**
- Uses TollGuru API directly
- Provides baseline toll costs
- Faster processing for general estimates
- Standard toll rates without time variations

### TollGuru Integration
- **Coverage**: Primarily North American toll roads
- **Accuracy**: High accuracy for covered regions
- **Updates**: Regular toll rate updates
- **Limitations**: May not cover all local toll roads

### Header Field Integration
The controller extracts additional context from headers:
- User location data
- Device information
- Request metadata
- Authentication context

### Error Handling
- **Validation Errors**: Input parameter validation failures
- **Service Errors**: TollGuru API or internal service failures
- **Authentication Errors**: Invalid or missing JWT tokens
- **Network Errors**: External API connectivity issues

## 🔗 Related File Links

- **Toll Service:** `allrepo/connectsmart/tsp-api/src/services/toll.js`
- **TollGuru Service:** `allrepo/connectsmart/tsp-api/src/services/tollguru.js`
- **Validation Schema:** `allrepo/connectsmart/tsp-api/src/schemas/toll-schemas.js`
- **Header Helper:** `allrepo/connectsmart/tsp-api/src/helpers/fields-of-header.js`

---
*This controller provides accurate toll cost calculation for informed route planning and transportation cost management.*