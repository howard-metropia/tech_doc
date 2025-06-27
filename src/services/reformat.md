# TSP API Reformat Service Documentation

## 🔍 Quick Summary (TL;DR)
The Reformat service transforms and standardizes route planning data from multiple transportation providers (HERE, Smartrek) into a unified format, handling timezone conversion, transport mode normalization, fare calculation, parking lot integration, and data quality filtering.

**Keywords:** route-data-transformation | transport-mode-standardization | timezone-conversion | fare-calculation | parking-integration | data-formatting | travel-mode-classification | multi-provider-support

**Primary use cases:** Converting external route data to standard format, normalizing transport modes across providers, calculating total fares, integrating parking data, filtering unreasonable routes, handling shared bike systems

**Compatibility:** Node.js >= 16.0.0, supports HERE Maps and Smartrek route data, timezone handling with moment-timezone, UUID generation for trip tracking

## ❓ Common Questions Quick Index
- **Q: What data sources are supported?** → HERE Maps, Smartrek (Taiwan), shared bike systems, parking lot data
- **Q: How are timezones handled?** → Converts local times to UTC format with timezone offset adjustment
- **Q: What transport modes are supported?** → Bus, rail, subway, cycling, walking, driving, shared bikes, gondola
- **Q: How are fares calculated?** → Per-segment fare parsing with total route fare calculation
- **Q: What quality filtering exists?** → Removes unreasonable route combinations and validates data integrity
- **Q: How are parking lots integrated?** → Injects walking segments and modifies place types for park-and-ride

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **universal translator** for route planning data. Different mapping services (like Google Maps vs Apple Maps) return route information in different formats. This service takes those different formats and converts them all into one standard format that the app can understand, while also cleaning up inconsistencies and adding useful information like total costs.

**Technical explanation:** 
A comprehensive data transformation service that normalizes route planning responses from multiple providers into a standardized format. Handles complex transformations including timezone conversion, transport mode mapping, fare aggregation, parking lot integration, and data quality validation with support for multi-modal transportation scenarios.

**Business value explanation:**
Enables integration with multiple route planning providers, ensures consistent user experience across different data sources, supports complex multi-modal transportation scenarios, reduces integration complexity, and maintains data quality standards for reliable route recommendations.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/reformat.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with moment-timezone
- **Type:** Data Transformation and Normalization Service
- **File Size:** ~12.8 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High - Complex data transformation logic)

**Dependencies:**
- `moment-timezone`: Timezone conversion and formatting (**Critical**)
- `uuid`: Unique identifier generation (**High**)
- `@app/src/services/timeTransform`: Time formatting utilities (**Medium**)
- `@app/src/models/busTickets`: Bus ticket data models (**Medium**)

## 📝 Detailed Code Analysis

### Core Transformation Methods

### convert Function

**Purpose:** Main data transformation for route planning responses

**Parameters:**
- `data`: Object - Raw route data from external provider
- `date`: String - Base date for time calculations
- `difftimezone`: Number - Timezone offset in hours

**Returns:** Promise resolving to transformed route data

**Complex Transformation Pipeline:**

### 1. Route Structure Initialization
```javascript
for (const attributename in data.routes) {
  for (const attributename2 in data.routes[attributename].sections) {
    data.routes[attributename].trip_detail_uuid = uuidv4();
    data.routes[attributename].started_on = data.routes[attributename].start_time;
    data.routes[attributename].ended_on = data.routes[attributename].end_time;
  }
}
```
- Adds unique trip identifiers for tracking
- Standardizes time field naming
- Prepares structure for section processing

### 2. Timezone Conversion
```javascript
data.routes[attributename].sections[attributename2].departure.time = tz(
  data.routes[attributename].sections[attributename2].departure.time,
)
  .add(difftimezone, 'hour')
  .format('YYYY-MM-DDTHH:mm:ss+00:00');

data.routes[attributename].sections[attributename2].arrival.time = tz(
  data.routes[attributename].sections[attributename2].arrival.time,
)
  .add(difftimezone, 'hour')
  .format('YYYY-MM-DDTHH:mm:ss+00:00');
```
- Converts all timestamps to UTC format
- Applies timezone offset correction
- Handles intermediate stops recursively

### 3. Intermediate Stops Processing
```javascript
if (data.routes[attributename].sections[attributename2].intermediateStops != undefined) {
  for (const attributename3 in data.routes[attributename].sections[attributename2].intermediateStops) {
    data.routes[attributename].sections[attributename2].intermediateStops[attributename3].departure.time = tz(
      data.routes[attributename].sections[attributename2].intermediateStops[attributename3].departure.time,
    )
      .add(difftimezone, 'hour')
      .format('YYYY-MM-DDTHH:mm:ss+00:00');
  }
}
```
- Processes intermediate stops along route segments
- Ensures all timestamps are consistently formatted
- Maintains stop sequence integrity

### Transport Mode Transformation

### Cycling Mode Processing
```javascript
case 'cycle':
  if (data.routes[attributename].sections[attributename2].transport.agency != undefined) {
    // Shared bike(Bcycle): $3/30分鐘
    if (data.routes[attributename].sections[attributename2].travelSummary.duration <= 1800) {
      data.routes[attributename].sections[attributename2].transport.fare = 3;
    } else if (duration >= 1801 && duration <= 3600) {
      data.routes[attributename].sections[attributename2].transport.fare = 6;
    } else if (duration >= 3601 && duration <= 5400) {
      data.routes[attributename].sections[attributename2].transport.fare = 9;
    } else {
      data.routes[attributename].sections[attributename2].transport.fare = 12;
    }
  }
  data.routes[attributename].sections[attributename2].type = 'cycling';
  data.routes[attributename].sections[attributename2].transport.mode = 'cycling';
  break;
```
- Calculates shared bike fares based on duration
- Tiered pricing: $3 for ≤30min, $6 for 31-60min, $9 for 61-90min, $12 for >90min
- Standardizes cycling mode naming

### Transit Mode Processing
```javascript
case 'transit':
  let tempColor = data.routes[attributename].sections[attributename2].transport.route_color == '' ? '' : '#';
  data.routes[attributename].sections[attributename2].transport.mode = 
    data.routes[attributename].sections[attributename2].transport.mode.toLowerCase();
  data.routes[attributename].sections[attributename2].transport.color = 
    tempColor + data.routes[attributename].sections[attributename2].transport.route_color;
  delete data.routes[attributename].sections[attributename2].transport.route_color;
```
- Formats route colors with hex prefix
- Normalizes mode names to lowercase
- Cleans up temporary fields

### Smartrek-Specific Transformations
```javascript
if (data.routes[attributename].sections[attributename2].transport.mode === 'tra') {
  data.routes[attributename].sections[attributename2].transport.mode = 'train';
  switch (data.routes[attributename].sections[attributename2].transport.name) {
    case 'R 淡水信義線':
      data.routes[attributename].sections[attributename2].transport.color = '#d90023';
      break;
    case 'G 松山新店線':
      data.routes[attributename].sections[attributename2].transport.color = '#107547';
      break;
    case 'BR 文湖線':
      data.routes[attributename].sections[attributename2].transport.color = '#b57a25';
      break;
    // ... more Taiwan MRT lines
  }
}
```
- Maps Taiwan-specific transport modes
- Assigns correct colors for Taipei MRT lines
- Handles multiple transit systems (MRT, HSR, gondola)

### Mode Mapping Rules
```javascript
else if (data.routes[attributename].sections[attributename2].transport.mode === 'highwaybus') {
  data.routes[attributename].sections[attributename2].transport.mode = 'bus';
} else if (data.routes[attributename].sections[attributename2].transport.mode === 'mrt') {
  data.routes[attributename].sections[attributename2].transport.mode = 'subway';
} else if (data.routes[attributename].sections[attributename2].transport.mode === 'hsr') {
  data.routes[attributename].sections[attributename2].transport.mode = 'rail';
} else if (data.routes[attributename].sections[attributename2].transport.mode === 'gondola') {
  data.routes[attributename].sections[attributename2].transport.mode = 'gondola_lift';
}
```
- Standardizes transport mode naming across providers
- Maps regional transport types to universal categories

### Fare Calculation and Route Finalization
```javascript
// Total fare calculation
data.routes[attributename].total_price += 
  data.routes[attributename].sections[attributename2].transport.fare === undefined
    ? 0
    : data.routes[attributename].sections[attributename2].transport.fare;

data.routes[attributename].total_price = parseFloat(data.routes[attributename].total_price);

// Set route start/end times from first/last sections
data.routes[attributename].started_on = data.routes[attributename].sections[0].departure.time;
data.routes[attributename].ended_on = 
  data.routes[attributename].sections[data.routes[attributename].sections.length-1].arrival.time;
```
- Aggregates fares across all route segments
- Sets actual start/end times from section data
- Cleans up temporary fields

### Parking Lot Integration

### addParkingLot Function

**Purpose:** Integrates parking lots into multi-modal routes for park-and-ride scenarios

**Parameters:**
- `data`: Object - Route data to modify
- `ary`: Array - Parking lot insertion points

**Complex Insertion Logic:**
```javascript
async addParkingLot(data, ary) {
  for (const attributename in ary) {
    const tempAry = ary[attributename].split('##');
    const temJson = [];
    
    for (const attributename2 in data.routes[tempAry[0]].sections) {
      if (parseInt(attributename2) === 0) {
        // Change first segment arrival type to parkingLot
        data.routes[tempAry[0]].sections[attributename2].arrival.place.type = 'parkingLot';
        temJson.push(data.routes[tempAry[0]].sections[attributename2]);
        
        // Insert walking segment from parking to transit
        const tempLeg = JSON.parse(`{
          "type":"pedestrian",
          "actions":[...],
          "arrival":{"time":"${data.routes[tempAry[0]].sections[attributename2].arrival.time}",
          "place":{"name":"${data.routes[tempAry[0]].sections[parseInt(attributename2) + 1].departure.place.name}",
          ...}},
          "transport":{"mode":"pedestrian"},
          "travelSummary":{"length":0,"duration":0}
        }`);
        temJson.push(tempLeg);
      }
    }
  }
}
```
- Modifies existing route structure to include parking
- Inserts walking segments between parking and transit
- Maintains temporal consistency across segments

### Travel Mode Classification
```javascript
const lastSections = data.routes[attributename].sections.length - 1;
let travelMode = 2; // Default: public transit

if (
  data.routes[attributename].sections[0].type == 'pedestrian' &&
  data.routes[attributename].sections[1].type == 'transit' &&
  data.routes[attributename].sections[lastSections - 1].type == 'transit' &&
  data.routes[attributename].sections[lastSections].type == 'pedestrian'
) {
  travelMode = 2; // PUBLIC_TRANSIT
} else if (
  data.routes[attributename].sections[0].type == 'drive' ||
  data.routes[attributename].sections[lastSections].type == 'drive'
) {
  travelMode = 7; // PARK_AND_RIDE
} else {
  travelMode = 5; // INTERMODAL
}
```

**Travel Mode Categories:**
- 1: DRIVING
- 2: PUBLIC_TRANSIT  
- 3: WALKING
- 4: BIKING
- 5: INTERMODAL
- 6: TRUCKING
- 7: PARK_AND_RIDE
- 100: DUO

### Data Quality and Filtering

### fixSharedBike Function
```javascript
async fixSharedBike(data) {
  for (const attr in data.routes) {
    const tmpRoutes = data.routes[attr].sections;
    for (const attr2 in tmpRoutes) {
      const tmpArrivalPlaceType = tmpRoutes[attr2].arrival.place.type;
      if (tmpArrivalPlaceType === undefined) {
        tmpRoutes[attr2].arrival.place.type = 'station';
      }
    }
  }
  return data;
}
```
- Fixes missing place types in shared bike data
- Ensures consistent JSON structure
- Prevents undefined properties in output

### filterUnreasonable Function
```javascript
async filterUnreasonable(data) {
  for (const attributename in data.routes) {
    const firstSections = data.routes[attributename].sections[0];
    const secondSections = data.routes[attributename].sections[1];
    const lastSections = data.routes[attributename].sections[data.routes[attributename].sections.length - 1];
    
    // Remove unreasonable combinations
    if ((firstSections.type == 'cycle' && lastSections.type == 'pedestrian') ||
        (firstSections.type == 'pedestrian' && lastSections.type == 'cycle') ||
        (firstSections.type == 'drive' && secondSections.type !== 'pedestrian')) {
      delete data.routes[attributename];
    }
  }
  
  const tempData = data.routes.filter(el => el);
  data.routes = tempData;
  return data;
}
```
- Removes logically inconsistent route combinations
- Filters out incomplete or invalid route data
- Compacts array after deletions

## 🚀 Usage Methods

### Basic Route Data Transformation
```javascript
const reformatService = require('@app/src/services/reformat');

async function transformRouteData(rawRouteData, baseDate, timezoneOffset) {
  try {
    // Transform basic route data
    const transformedData = await reformatService.convert(
      rawRouteData,
      baseDate,
      timezoneOffset
    );
    
    console.log('Route transformation completed:');
    console.log('Routes:', transformedData.routes.length);
    
    // Print route summary
    transformedData.routes.forEach((route, index) => {
      console.log(`Route ${index + 1}:`);
      console.log('  Travel Mode:', route.travel_mode);
      console.log('  Total Price:', route.total_price);
      console.log('  Start:', route.started_on);
      console.log('  End:', route.ended_on);
      console.log('  Sections:', route.sections.length);
    });
    
    return transformedData;
  } catch (error) {
    console.error('Route transformation failed:', error);
    throw error;
  }
}

// Usage
const rawData = {
  routes: [
    {
      start_time: "09:00:00",
      end_time: "10:30:00",
      total_price: 0,
      sections: [
        {
          type: "pedestrian",
          departure: { time: "09:00:00" },
          arrival: { time: "09:10:00" },
          transport: { mode: "pedestrian" },
          travelSummary: { length: 500, duration: 600 }
        }
      ]
    }
  ]
};

const transformed = await transformRouteData(rawData, "2024-06-25", -5);
```

### Comprehensive Route Processing Pipeline
```javascript
class RouteProcessor {
  constructor() {
    this.reformatService = require('@app/src/services/reformat');
  }

  async processMultiProviderRoutes(routeData, options = {}) {
    try {
      const {
        date = new Date().toISOString().split('T')[0],
        timezoneOffset = 0,
        parkingLots = [],
        provider = 'HERE',
        includeParkAndRide = false,
        filterQuality = true
      } = options;

      let processedData = { ...routeData };

      // Step 1: Basic transformation
      console.log('Step 1: Converting basic route structure...');
      processedData = await this.reformatService.convert(
        processedData,
        date,
        timezoneOffset
      );

      // Step 2: Provider-specific processing
      if (provider === 'Smartrek') {
        console.log('Step 2: Applying Smartrek-specific transformations...');
        processedData = await this.reformatService.convertSmartrek(processedData);
      }

      // Step 3: Shared bike fixes
      console.log('Step 3: Fixing shared bike data...');
      processedData = await this.reformatService.fixSharedBike(processedData);

      // Step 4: Parking lot integration
      if (includeParkAndRide && parkingLots.length > 0) {
        console.log('Step 4: Integrating parking lots...');
        processedData = await this.reformatService.addParkingLot(
          processedData,
          parkingLots
        );
      }

      // Step 5: Quality filtering
      if (filterQuality) {
        console.log('Step 5: Filtering unreasonable routes...');
        processedData = await this.reformatService.filterUnreasonable(processedData);
      }

      // Step 6: Generate processing summary
      const summary = this.generateProcessingSummary(routeData, processedData);

      return {
        success: true,
        data: processedData,
        summary,
        processedAt: new Date().toISOString()
      };
    } catch (error) {
      console.error('Route processing failed:', error);
      return {
        success: false,
        error: error.message,
        originalData: routeData
      };
    }
  }

  generateProcessingSummary(originalData, processedData) {
    const originalRoutes = originalData.routes?.length || 0;
    const processedRoutes = processedData.routes?.length || 0;
    const routesFiltered = originalRoutes - processedRoutes;

    const transportModes = new Set();
    const totalFare = processedData.routes?.reduce((sum, route) => {
      if (route.travel_mode) {
        transportModes.add(this.getTravelModeString(route.travel_mode));
      }
      return sum + (route.total_price || 0);
    }, 0) || 0;

    return {
      originalRoutes,
      processedRoutes,
      routesFiltered,
      transportModes: Array.from(transportModes),
      totalFareRange: {
        min: Math.min(...processedData.routes?.map(r => r.total_price || 0) || [0]),
        max: Math.max(...processedData.routes?.map(r => r.total_price || 0) || [0]),
        average: processedRoutes > 0 ? (totalFare / processedRoutes).toFixed(2) : 0
      }
    };
  }

  getTravelModeString(modeCode) {
    const modes = {
      1: 'DRIVING',
      2: 'PUBLIC_TRANSIT',
      3: 'WALKING',
      4: 'BIKING',
      5: 'INTERMODAL',
      6: 'TRUCKING',
      7: 'PARK_AND_RIDE',
      100: 'DUO'
    };
    return modes[modeCode] || 'UNKNOWN';
  }

  async validateTransformedData(data) {
    const validationResults = {
      valid: true,
      warnings: [],
      errors: []
    };

    if (!data.routes || !Array.isArray(data.routes)) {
      validationResults.errors.push('Routes array is missing or invalid');
      validationResults.valid = false;
      return validationResults;
    }

    data.routes.forEach((route, routeIndex) => {
      // Check required fields
      if (!route.trip_detail_uuid) {
        validationResults.warnings.push(`Route ${routeIndex}: Missing trip_detail_uuid`);
      }
      
      if (!route.started_on || !route.ended_on) {
        validationResults.errors.push(`Route ${routeIndex}: Missing start/end times`);
        validationResults.valid = false;
      }

      if (typeof route.total_price !== 'number') {
        validationResults.warnings.push(`Route ${routeIndex}: Invalid total_price`);
      }

      // Validate sections
      if (!route.sections || !Array.isArray(route.sections)) {
        validationResults.errors.push(`Route ${routeIndex}: Missing or invalid sections`);
        validationResults.valid = false;
        return;
      }

      route.sections.forEach((section, sectionIndex) => {
        if (!section.departure?.time || !section.arrival?.time) {
          validationResults.errors.push(
            `Route ${routeIndex}, Section ${sectionIndex}: Missing departure/arrival times`
          );
          validationResults.valid = false;
        }

        if (!section.transport?.mode) {
          validationResults.warnings.push(
            `Route ${routeIndex}, Section ${sectionIndex}: Missing transport mode`
          );
        }
      });
    });

    return validationResults;
  }
}
```

### Fare Analysis and Transport Mode Statistics
```javascript
class RouteAnalyzer {
  constructor() {
    this.reformatService = require('@app/src/services/reformat');
  }

  analyzeTransformedRoutes(transformedData) {
    const analysis = {
      routeCount: transformedData.routes.length,
      transportModes: {},
      fareAnalysis: {
        routes: [],
        summary: {
          minFare: Infinity,
          maxFare: -Infinity,
          averageFare: 0,
          totalFare: 0,
          freeRoutes: 0
        }
      },
      travelModes: {},
      timeAnalysis: {
        shortest: null,
        longest: null,
        averageDuration: 0
      }
    };

    transformedData.routes.forEach((route, index) => {
      // Transport mode analysis
      route.sections.forEach(section => {
        const mode = section.transport?.mode || 'unknown';
        analysis.transportModes[mode] = (analysis.transportModes[mode] || 0) + 1;
      });

      // Travel mode analysis
      const travelModeStr = this.getTravelModeString(route.travel_mode);
      analysis.travelModes[travelModeStr] = (analysis.travelModes[travelModeStr] || 0) + 1;

      // Fare analysis
      const fare = route.total_price || 0;
      analysis.fareAnalysis.routes.push({
        routeIndex: index,
        fare,
        sections: route.sections.length,
        travelMode: travelModeStr
      });

      if (fare === 0) {
        analysis.fareAnalysis.summary.freeRoutes++;
      }
      
      analysis.fareAnalysis.summary.minFare = Math.min(analysis.fareAnalysis.summary.minFare, fare);
      analysis.fareAnalysis.summary.maxFare = Math.max(analysis.fareAnalysis.summary.maxFare, fare);
      analysis.fareAnalysis.summary.totalFare += fare;

      // Time analysis
      const startTime = new Date(route.started_on);
      const endTime = new Date(route.ended_on);
      const duration = endTime - startTime;

      if (!analysis.timeAnalysis.shortest || duration < analysis.timeAnalysis.shortest.duration) {
        analysis.timeAnalysis.shortest = { routeIndex: index, duration, durationMinutes: duration / 60000 };
      }

      if (!analysis.timeAnalysis.longest || duration > analysis.timeAnalysis.longest.duration) {
        analysis.timeAnalysis.longest = { routeIndex: index, duration, durationMinutes: duration / 60000 };
      }
    });

    // Calculate averages
    if (analysis.routeCount > 0) {
      analysis.fareAnalysis.summary.averageFare = (
        analysis.fareAnalysis.summary.totalFare / analysis.routeCount
      ).toFixed(2);
    }

    // Fix infinity values
    if (analysis.fareAnalysis.summary.minFare === Infinity) {
      analysis.fareAnalysis.summary.minFare = 0;
    }

    return analysis;
  }

  getTravelModeString(modeCode) {
    const modes = {
      1: 'DRIVING',
      2: 'PUBLIC_TRANSIT',
      3: 'WALKING',
      4: 'BIKING',
      5: 'INTERMODAL',
      6: 'TRUCKING',
      7: 'PARK_AND_RIDE',
      100: 'DUO'
    };
    return modes[modeCode] || 'UNKNOWN';
  }

  generateRecommendations(analysis) {
    const recommendations = [];

    // Fare recommendations
    if (analysis.fareAnalysis.summary.freeRoutes > 0) {
      recommendations.push({
        type: 'cost',
        message: `${analysis.fareAnalysis.summary.freeRoutes} free route(s) available`,
        priority: 'high'
      });
    }

    if (analysis.fareAnalysis.summary.minFare > 0 && analysis.fareAnalysis.summary.maxFare > analysis.fareAnalysis.summary.minFare * 2) {
      recommendations.push({
        type: 'cost',
        message: `Consider cheaper alternatives - fare range $${analysis.fareAnalysis.summary.minFare} to $${analysis.fareAnalysis.summary.maxFare}`,
        priority: 'medium'
      });
    }

    // Transport mode recommendations
    if (analysis.transportModes.pedestrian) {
      recommendations.push({
        type: 'health',
        message: `Route includes walking - good for fitness`,
        priority: 'low'
      });
    }

    if (analysis.transportModes.cycling) {
      recommendations.push({
        type: 'environment',
        message: `Eco-friendly cycling option available`,
        priority: 'medium'
      });
    }

    // Time recommendations
    if (analysis.timeAnalysis.shortest && analysis.timeAnalysis.longest) {
      const timeDiff = analysis.timeAnalysis.longest.durationMinutes - analysis.timeAnalysis.shortest.durationMinutes;
      if (timeDiff > 30) {
        recommendations.push({
          type: 'time',
          message: `Route times vary significantly - consider fastest option for time-sensitive trips`,
          priority: 'medium'
        });
      }
    }

    return recommendations;
  }
}
```

## 📊 Output Examples

### Transformed Route Response
```json
{
  "routes": [
    {
      "trip_detail_uuid": "123e4567-e89b-12d3-a456-426614174000",
      "started_on": "2024-06-25T09:00:00+00:00",
      "ended_on": "2024-06-25T10:30:00+00:00",
      "total_price": 4.50,
      "travel_mode": 2,
      "sections": [
        {
          "type": "pedestrian",
          "departure": {
            "time": "2024-06-25T09:00:00+00:00",
            "place": {
              "name": "Origin",
              "type": "address",
              "location": {"lat": 29.7604, "lng": -95.3698}
            }
          },
          "arrival": {
            "time": "2024-06-25T09:10:00+00:00",
            "place": {
              "name": "Bus Stop",
              "type": "station",
              "location": {"lat": 29.7614, "lng": -95.3688}
            }
          },
          "transport": {"mode": "pedestrian"},
          "travelSummary": {"length": 800, "duration": 600}
        },
        {
          "type": "transit",
          "departure": {
            "time": "2024-06-25T09:15:00+00:00"
          },
          "arrival": {
            "time": "2024-06-25T10:20:00+00:00"
          },
          "transport": {
            "mode": "bus",
            "shortName": "82",
            "name": "82",
            "color": "#0066CC",
            "fare": 1.25
          },
          "travelSummary": {"length": 15000, "duration": 3900}
        }
      ]
    }
  ]
}
```

### Route Analysis Summary
```json
{
  "routeCount": 3,
  "transportModes": {
    "pedestrian": 6,
    "bus": 2,
    "subway": 1
  },
  "fareAnalysis": {
    "summary": {
      "minFare": 0,
      "maxFare": 8.50,
      "averageFare": "4.17",
      "totalFare": 12.50,
      "freeRoutes": 1
    }
  },
  "travelModes": {
    "PUBLIC_TRANSIT": 2,
    "WALKING": 1
  },
  "timeAnalysis": {
    "shortest": {
      "routeIndex": 0,
      "durationMinutes": 25
    },
    "longest": {
      "routeIndex": 2,
      "durationMinutes": 90
    }
  }
}
```

### Processing Summary
```json
{
  "success": true,
  "summary": {
    "originalRoutes": 5,
    "processedRoutes": 3,
    "routesFiltered": 2,
    "transportModes": ["PUBLIC_TRANSIT", "INTERMODAL"],
    "totalFareRange": {
      "min": 0,
      "max": 8.50,
      "average": "4.17"
    }
  },
  "processedAt": "2024-06-25T14:30:00.000Z"
}
```

## ⚠️ Important Notes

### Data Transformation Complexity
- **Multi-Provider Support:** Handles different data formats from HERE, Smartrek, and other providers
- **Timezone Handling:** Critical for international route planning and time display
- **Mode Standardization:** Normalizes transport modes across different naming conventions
- **Fare Aggregation:** Calculates total route costs from individual segment fares

### Provider-Specific Features
- **Smartrek Integration:** Special handling for Taiwan transit systems with MRT line colors
- **HERE Maps Support:** Standard route planning data transformation
- **Shared Bike Systems:** Custom fare calculation for BCycle and similar services
- **Regional Adaptations:** Supports different transit systems and pricing models

### Data Quality and Validation
- **Unreasonable Route Filtering:** Removes logically inconsistent route combinations
- **Missing Data Handling:** Fixes undefined properties and missing place types
- **Structure Validation:** Ensures consistent JSON structure across all routes
- **Integrity Checks:** Validates temporal and spatial consistency

### Park-and-Ride Integration
- **Parking Lot Injection:** Seamlessly integrates parking lots into multi-modal routes
- **Walking Segment Creation:** Automatically adds walking connections
- **Place Type Modification:** Updates location types for proper route visualization
- **Temporal Consistency:** Maintains correct timing across all segments

### Performance Considerations
- **Large Dataset Handling:** Efficiently processes multiple routes with many segments
- **Memory Management:** Cleans up temporary fields and unused data
- **UUID Generation:** Creates unique identifiers for trip tracking
- **Array Compaction:** Removes filtered routes to maintain array integrity

### International Support
- **Multi-Language Names:** Preserves original transit system names
- **Currency Handling:** Supports different fare currencies and formats
- **Regional Transport Types:** Maps local transport modes to universal categories
- **Cultural Adaptations:** Handles region-specific transportation patterns

## 🔗 Related File Links

- **Time Transform Service:** `allrepo/connectsmart/tsp-api/src/services/timeTransform.js`
- **Bus Tickets Models:** `allrepo/connectsmart/tsp-api/src/models/busTickets.js`
- **Route Planning Controllers:** Route planning API endpoints that use this service

---
*This service provides essential data transformation capabilities for multi-provider route planning integration with comprehensive support for complex transportation scenarios in the TSP platform.*