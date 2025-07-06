# TSP API ReformatHere Service Documentation

## 🔍 Quick Summary (TL;DR)
The ReformatHere service specializes in transforming HERE Maps transit route data into standardized format, handling timezone conversion to UTC, bus/light rail naming normalization, transfer counting, and ticket system integration for Houston Metro transit.

**Keywords:** here-maps-integration | transit-data-transformation | utc-conversion | houston-metro | bus-tickets | light-rail-processing | transfer-counting | route-standardization

**Primary use cases:** Converting HERE Maps route responses, normalizing Houston Metro transit data, preparing bus ticket information, calculating transfers and metrics, standardizing time formats

**Compatibility:** Node.js >= 16.0.0, HERE Maps API integration, Houston Metro-specific transit data, moment-timezone for UTC conversion

## ❓ Common Questions Quick Index
- **Q: What data source does this handle?** → HERE Maps transit route planning responses
- **Q: How are times converted?** → All times converted to UTC format for consistency
- **Q: What transit systems are supported?** → Houston Metro buses and light rail (RED line)
- **Q: How are transfers counted?** → Counts transit segments excluding first/last walking segments
- **Q: What ticket information is generated?** → Bus and light rail ticket data for fare processing
- **Q: How are bus names normalized?** → Removes leading zeros and standardizes naming

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **HERE Maps translator** specifically designed for Houston's public transit. It takes the complex route data from HERE Maps and converts it into a clean, standardized format that the app can use, while also figuring out which bus tickets you'll need and how many times you'll have to transfer.

**Technical explanation:** 
A specialized data transformation service for HERE Maps transit responses, focusing on Houston Metro integration. Converts all timestamps to UTC, normalizes transit vehicle naming, calculates route metrics, and prepares ticket purchasing data for seamless transit experience.

**Business value explanation:**
Enables reliable HERE Maps integration for transit planning, ensures consistent data format across the platform, supports automated ticket purchasing, provides accurate transfer and timing information, and maintains Houston Metro compatibility.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/reformatHere.js`
- **Language:** JavaScript (ES2020) 
- **Framework:** Node.js with moment-timezone
- **Type:** HERE Maps Transit Data Transformation Service
- **File Size:** ~5.4 KB
- **Complexity Score:** ⭐⭐⭐ (Medium-High - Transit-specific transformation logic)

**Dependencies:**
- `moment-timezone`: UTC timezone conversion (**Critical**)
- `uuid`: Trip UUID generation (**High**)
- `@app/src/services/timeTransform`: Time formatting utilities (**Medium**)
- `@app/src/models/busTickets`: Bus ticket data models (**High**)

## 📝 Detailed Code Analysis

### convert Function

**Purpose:** Transforms HERE Maps route data with Houston Metro specialization

**Parameters:**
- `data`: Object - Raw HERE Maps route response
- `date`: String - Base date for calculations
- `difftimezone`: Number - Timezone offset (not used in UTC conversion)

**Returns:** Promise resolving to `{ data, BusTickets }`

### Core Transformation Logic

### 1. Route Initialization and Metrics
```javascript
for (const attributename in data.routes) {
  const lastSections = data.routes[attributename].sections.length - 1;
  let totalTravelMeters = 0;
  let talTravelTime = 0;
  let transfers = 0;
  
  data.routes[attributename].trip_detail_uuid = uuidv4();
  data.routes[attributename].travel_mode = 2; // PUBLIC_TRANSIT
}
```
- Generates unique trip identifiers
- Sets default travel mode to public transit
- Initializes metric counters

### 2. Transfer Counting Logic
```javascript
if (
  attributename2 != 0 &&
  attributename2 != lastSections &&
  data.routes[attributename].sections[attributename2].type == 'transit'
) {
  transfers++;
}
```
- Excludes first and last segments (typically walking)
- Only counts actual transit segments as transfers
- Provides accurate transfer count for user information

### 3. UTC Time Conversion
```javascript
data.routes[attributename].sections[attributename2].departure.time = tz(
  data.routes[attributename].sections[attributename2].departure.time,
)
  .utc()
  .format('YYYY-MM-DDTHH:mm:ss+00:00');

data.routes[attributename].sections[attributename2].arrival.time = tz(
  data.routes[attributename].sections[attributename2].arrival.time,
)
  .utc()
  .format('YYYY-MM-DDTHH:mm:ss+00:00');
```
- Converts all timestamps to UTC format
- Ensures consistent time representation
- Handles both departure and arrival times

### 4. Intermediate Stops Processing
```javascript
if (data.routes[attributename].sections[attributename2].type == 'transit') {
  for (const attributename3 in data.routes[attributename].sections[attributename2].intermediateStops) {
    data.routes[attributename].sections[attributename2].intermediateStops[attributename3].departure.time = tz(
      data.routes[attributename].sections[attributename2].intermediateStops[attributename3].departure.time,
    )
      .utc()
      .format('YYYY-MM-DDTHH:mm:ss+00:00');
  }
}
```
- Processes all intermediate stops along transit routes
- Maintains timestamp consistency throughout the journey
- Critical for accurate real-time transit information

### Houston Metro Bus Processing

### Bus Name Normalization
```javascript
if (data.routes[attributename].sections[attributename2].transport.mode == 'bus') {
  let tempBusName = "";
  try {
    tempBusName = data.routes[attributename].sections[attributename2].transport.shortName.substr(0, 1) === '0'
      ? data.routes[attributename].sections[attributename2].transport.shortName.replace('0', '')
      : data.routes[attributename].sections[attributename2].transport.shortName;
    
    tempBusName = tempBusName.substr(0, 1) === '0'
      ? tempBusName.replace('0', '')
      : tempBusName;
  } catch(e) {
    tempBusName = data.routes[attributename].sections[attributename2].transport.name;
  }
  
  data.routes[attributename].sections[attributename2].transport.shortName = 
  data.routes[attributename].sections[attributename2].transport.name = tempBusName;
}
```
- Removes leading zeros from bus route numbers
- Handles missing shortName gracefully
- Standardizes bus naming for Houston Metro

### Ticket System Integration
```javascript
data.routes[attributename].sections[attributename2].transport.is_ticket = 0;
data.routes[attributename].sections[attributename2].transport.fare = 0;
data.routes[attributename].sections[attributename2].transport.product_id = '';

const tmpBusName = data.routes[attributename].sections[attributename2].transport.name;
BusTickets.push(`${attributename}##${attributename2}##${tmpBusName}`);
```
- Initializes ticket system fields
- Creates ticket identifiers for fare processing
- Links routes to ticket purchasing system

### Houston Metro Light Rail Processing

### Light Rail Line Mapping
```javascript
else if (data.routes[attributename].sections[attributename2].transport.mode == 'lightRail') {
  if (data.routes[attributename].sections[attributename2].transport.name == '700') {
    data.routes[attributename].sections[attributename2].transport.name = 
    data.routes[attributename].sections[attributename2].transport.shortName = 'RED';
  } else if (data.routes[attributename].sections[attributename2].transport.name == '800') {
    data.routes[attributename].sections[attributename2].transport.name = 
    data.routes[attributename].sections[attributename2].transport.shortName = 'RED';
  } else if (data.routes[attributename].sections[attributename2].transport.name == '900') {
    data.routes[attributename].sections[attributename2].transport.name = 
    data.routes[attributename].sections[attributename2].transport.shortName = 'RED';
  }
}
```
- Maps HERE Maps light rail codes to Houston Metro line names
- Standardizes all Houston light rail services as 'RED' line
- Ensures consistent naming across the application

### Route Metrics Calculation
```javascript
totalTravelMeters += parseInt(data.routes[attributename].sections[attributename2].travelSummary.length);
talTravelTime += parseInt(data.routes[attributename].sections[attributename2].travelSummary.duration);

// Final route assignment
data.routes[attributename].total_travel_meters = totalTravelMeters;
data.routes[attributename].total_price = 0;
data.routes[attributename].started_on = data.routes[attributename].sections[0].departure.time;
data.routes[attributename].ended_on = data.routes[attributename].sections[lastSections].arrival.time;
data.routes[attributename].total_travel_time = talTravelTime;
data.routes[attributename].transfers = transfers;
```
- Aggregates distance and time across all segments
- Sets route start/end times from actual section data
- Provides comprehensive route metrics

## 🚀 Usage Methods

### Basic HERE Maps Route Processing
```javascript
const reformatHereService = require('@app/src/services/reformatHere');

async function processHereRoute(hereRouteData, requestDate, timezoneOffset) {
  try {
    const result = await reformatHereService.convert(
      hereRouteData,
      requestDate,
      timezoneOffset
    );
    
    console.log('HERE route processing completed:');
    console.log('Processed routes:', result.data.routes.length);
    console.log('Bus tickets needed:', result.BusTickets.length);
    
    // Display route summary
    result.data.routes.forEach((route, index) => {
      console.log(`Route ${index + 1}:`);
      console.log('  Travel time:', route.total_travel_time, 'seconds');
      console.log('  Distance:', route.total_travel_meters, 'meters');
      console.log('  Transfers:', route.transfers);
      console.log('  Start:', route.started_on);
      console.log('  End:', route.ended_on);
    });
    
    return result;
  } catch (error) {
    console.error('HERE route processing failed:', error);
    throw error;
  }
}

// Usage
const hereData = {
  routes: [
    {
      sections: [
        {
          type: 'pedestrian',
          departure: { time: '2024-06-25T14:00:00' },
          arrival: { time: '2024-06-25T14:05:00' },
          travelSummary: { length: 400, duration: 300 }
        },
        {
          type: 'transit',
          transport: { mode: 'bus', shortName: '082', name: '82' },
          departure: { time: '2024-06-25T14:10:00' },
          arrival: { time: '2024-06-25T14:35:00' },
          travelSummary: { length: 8000, duration: 1500 },
          intermediateStops: [
            { departure: { time: '2024-06-25T14:15:00' } }
          ]
        }
      ]
    }
  ]
};

const processed = await processHereRoute(hereData, '2024-06-25', -5);
```

### Route Analysis and Ticket Management
```javascript
class HereRouteAnalyzer {
  constructor() {
    this.reformatService = require('@app/src/services/reformatHere');
  }

  async analyzeAndProcessRoute(hereData, options = {}) {
    const { date = new Date().toISOString().split('T')[0], timezoneOffset = 0 } = options;
    
    try {
      const result = await this.reformatService.convert(hereData, date, timezoneOffset);
      
      const analysis = {
        routeCount: result.data.routes.length,
        ticketInfo: this.analyzeTickets(result.BusTickets),
        routeMetrics: this.calculateRouteMetrics(result.data.routes),
        recommendations: this.generateRecommendations(result.data.routes)
      };
      
      return {
        success: true,
        processedData: result.data,
        tickets: result.BusTickets,
        analysis
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        originalData: hereData
      };
    }
  }

  analyzeTickets(busTickets) {
    const ticketMap = new Map();
    const routeTickets = new Map();
    
    busTickets.forEach(ticket => {
      const [routeIndex, sectionIndex, busName] = ticket.split('##');
      
      if (!ticketMap.has(busName)) {
        ticketMap.set(busName, 0);
      }
      ticketMap.set(busName, ticketMap.get(busName) + 1);
      
      if (!routeTickets.has(routeIndex)) {
        routeTickets.set(routeIndex, []);
      }
      routeTickets.get(routeIndex).push(busName);
    });
    
    return {
      uniqueServices: Array.from(ticketMap.keys()),
      serviceCount: ticketMap.size,
      totalTickets: busTickets.length,
      ticketsByRoute: Object.fromEntries(routeTickets),
      serviceFrequency: Object.fromEntries(ticketMap)
    };
  }

  calculateRouteMetrics(routes) {
    if (!routes.length) return null;
    
    const metrics = {
      totalRoutes: routes.length,
      avgTravelTime: 0,
      avgDistance: 0,
      avgTransfers: 0,
      timeRange: { min: Infinity, max: -Infinity },
      distanceRange: { min: Infinity, max: -Infinity }
    };
    
    let totalTime = 0, totalDistance = 0, totalTransfers = 0;
    
    routes.forEach(route => {
      totalTime += route.total_travel_time || 0;
      totalDistance += route.total_travel_meters || 0;
      totalTransfers += route.transfers || 0;
      
      const time = route.total_travel_time || 0;
      const distance = route.total_travel_meters || 0;
      
      metrics.timeRange.min = Math.min(metrics.timeRange.min, time);
      metrics.timeRange.max = Math.max(metrics.timeRange.max, time);
      metrics.distanceRange.min = Math.min(metrics.distanceRange.min, distance);
      metrics.distanceRange.max = Math.max(metrics.distanceRange.max, distance);
    });
    
    metrics.avgTravelTime = Math.round(totalTime / routes.length);
    metrics.avgDistance = Math.round(totalDistance / routes.length);
    metrics.avgTransfers = (totalTransfers / routes.length).toFixed(1);
    
    return metrics;
  }

  generateRecommendations(routes) {
    const recommendations = [];
    
    if (routes.length === 0) {
      recommendations.push({
        type: 'warning',
        message: 'No routes found',
        priority: 'high'
      });
      return recommendations;
    }
    
    // Find fastest route
    const fastestRoute = routes.reduce((fastest, current) => 
      (current.total_travel_time || Infinity) < (fastest.total_travel_time || Infinity) ? current : fastest
    );
    
    recommendations.push({
      type: 'time',
      message: `Fastest route takes ${Math.round(fastestRoute.total_travel_time / 60)} minutes`,
      priority: 'medium'
    });
    
    // Check for routes with no transfers
    const directRoutes = routes.filter(route => route.transfers === 0);
    if (directRoutes.length > 0) {
      recommendations.push({
        type: 'convenience',
        message: `${directRoutes.length} direct route(s) available (no transfers)`,
        priority: 'high'
      });
    }
    
    // Check for routes with many transfers
    const highTransferRoutes = routes.filter(route => route.transfers >= 2);
    if (highTransferRoutes.length > 0) {
      recommendations.push({
        type: 'convenience',
        message: `${highTransferRoutes.length} route(s) require 2+ transfers`,
        priority: 'low'
      });
    }
    
    return recommendations;
  }
}
```

## 📊 Output Examples

### Processed Route Response
```json
{
  "data": {
    "routes": [
      {
        "trip_detail_uuid": "123e4567-e89b-12d3-a456-426614174000",
        "travel_mode": 2,
        "total_travel_meters": 8400,
        "total_price": 0,
        "started_on": "2024-06-25T19:00:00+00:00",
        "ended_on": "2024-06-25T19:40:00+00:00",
        "total_travel_time": 1800,
        "transfers": 1,
        "sections": [
          {
            "type": "pedestrian",
            "departure": {
              "time": "2024-06-25T19:00:00+00:00"
            },
            "arrival": {
              "time": "2024-06-25T19:05:00+00:00"
            }
          },
          {
            "type": "transit",
            "transport": {
              "mode": "bus",
              "shortName": "82",
              "name": "82",
              "is_ticket": 0,
              "fare": 0,
              "product_id": ""
            },
            "departure": {
              "time": "2024-06-25T19:10:00+00:00"
            },
            "arrival": {
              "time": "2024-06-25T19:35:00+00:00"
            }
          }
        ]
      }
    ]
  },
  "BusTickets": [
    "0##1##82"
  ]
}
```

### Route Analysis Summary
```json
{
  "success": true,
  "analysis": {
    "routeCount": 3,
    "ticketInfo": {
      "uniqueServices": ["82", "RED", "56"],
      "serviceCount": 3,
      "totalTickets": 5,
      "ticketsByRoute": {
        "0": ["82", "RED"],
        "1": ["56"],
        "2": ["82", "56"]
      },
      "serviceFrequency": {
        "82": 2,
        "RED": 1,
        "56": 2
      }
    },
    "routeMetrics": {
      "totalRoutes": 3,
      "avgTravelTime": 1620,
      "avgDistance": 7200,
      "avgTransfers": "1.3",
      "timeRange": {"min": 1200, "max": 2100},
      "distanceRange": {"min": 5000, "max": 9500}
    },
    "recommendations": [
      {
        "type": "time",
        "message": "Fastest route takes 20 minutes",
        "priority": "medium"
      },
      {
        "type": "convenience", 
        "message": "1 direct route(s) available (no transfers)",
        "priority": "high"
      }
    ]
  }
}
```

## ⚠️ Important Notes

### HERE Maps Integration
- **UTC Conversion:** All timestamps converted to UTC for consistency across time zones
- **Route Structure:** Maintains HERE Maps section-based route structure
- **Transfer Calculation:** Intelligent transfer counting excludes walking segments
- **Error Handling:** Graceful handling of missing bus name fields

### Houston Metro Specialization
- **Bus Name Normalization:** Removes leading zeros from route numbers (082 → 82)
- **Light Rail Mapping:** Maps HERE codes (700/800/900) to Houston RED line
- **Ticket Integration:** Prepares data for Houston Metro ticket purchasing system
- **Local Adaptations:** Specific handling for Houston transit naming conventions

### Data Quality and Consistency
- **Metric Aggregation:** Calculates total distance, time, and transfer counts
- **Time Standardization:** Consistent UTC timestamp format throughout
- **Field Cleanup:** Removes unnecessary ID fields from HERE responses
- **Structure Preservation:** Maintains intermediate stops and detailed route information

### Performance Considerations
- **Efficient Processing:** Single-pass transformation of route data
- **Memory Management:** Processes large route responses efficiently
- **UUID Generation:** Unique trip identifiers for tracking and analytics
- **Batch Ticket Processing:** Collects all ticket requirements for optimization

## 🔗 Related File Links

- **Time Transform Service:** `allrepo/connectsmart/tsp-api/src/services/timeTransform.js`
- **Bus Tickets Models:** `allrepo/connectsmart/tsp-api/src/models/busTickets.js`
- **General Reformat Service:** `allrepo/connectsmart/tsp-api/src/services/reformat.js`

---
*This service provides specialized HERE Maps route data transformation with Houston Metro integration for the TSP platform.*