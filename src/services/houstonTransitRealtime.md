# TSP API Houston Transit Realtime Service Documentation

## 🔍 Quick Summary (TL;DR)
The Houston Transit Realtime service provides real-time bus and rail transit information for Houston METRO system, parsing route data and injecting live arrival times, delays, and service disruptions.

**Keywords:** houston-metro | realtime-transit | bus-tracking | transit-data | gtfs-realtime | arrival-predictions | transit-integration | houston-public-transport

**Primary use cases:** Real-time transit arrival predictions, service disruption notifications, route scheduling updates, transit data normalization

**Compatibility:** Node.js >= 16.0.0, MongoDB integration, moment-timezone for timestamp handling

## ❓ Common Questions Quick Index
- **Q: What transit modes are supported?** → Bus and rail (light rail/METRORail) for Houston METRO
- **Q: How are delays calculated?** → Uses GTFS-RT delay data in seconds added to scheduled arrival times
- **Q: What service disruptions are tracked?** → SKIPPED and CANCELED trip statuses
- **Q: How are route IDs normalized?** → Removes Houston METRO prefixes and standardizes format
- **Q: Is real-time data always available?** → No, fallback method provides empty realtime field when unavailable
- **Q: What timezone is used?** → UTC conversion with moment-timezone for consistent API responses

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **live transit tracker** specifically for Houston's public transportation system. When someone plans a trip using buses or trains in Houston, this service checks if those vehicles are running on time, running late, or if there are any cancellations, then updates the trip plan with the most current information.

**Technical explanation:** 
A specialized real-time transit data processor that integrates with Houston METRO's GTFS-Realtime feed. Parses route planning data to inject live arrival predictions, delay information, and service alerts. Handles route ID normalization, trip matching, and timezone conversions for consistent API responses.

**Business value explanation:**
Critical for providing accurate transit information to riders, reducing wait times and improving user experience. Enables real-time trip planning adjustments, supports transit reliability metrics, and enhances the overall value proposition of public transit integration in the mobility platform.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/houstonTransitRealtime.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js service with MongoDB integration
- **Type:** Real-time Transit Data Service
- **File Size:** ~5.2 KB
- **Complexity Score:** ⭐⭐⭐ (Medium - Complex transit data processing and matching)

**Dependencies:**
- `@app/src/models/HoustonBusRealtime`: MongoDB model for real-time data (**Critical**)
- `moment-timezone`: Timezone handling and date manipulation (**High**)

## 📝 Detailed Code Analysis

### parseRoutes Function

**Purpose:** Main function to inject real-time data into planned routes

**Parameters:**
- `data`: Object - Route planning data with sections and transport details

**Returns:** Object - Updated route data with real-time information

**Processing Flow:**
1. **Route Iteration:** Loops through all routes and sections
2. **Transit Mode Detection:** Identifies bus/rail transit sections
3. **ID Normalization:** Cleans route, stop, and trip IDs
4. **Real-time Data Lookup:** Queries MongoDB for current transit data
5. **Trip Matching:** Matches planned trips with real-time trip data
6. **Delay Calculation:** Applies delay information to scheduled times
7. **Service Alert Processing:** Handles SKIPPED/CANCELED statuses

**Implementation Detail:**
```javascript
// Route ID normalization for Houston METRO
let routeID = route2.transport.route_id.replace('-ME-1', '');
routeID = routeID.replace('-ME-2', '');
routeID = routeID.replace('-ME-3', '');
routeID = routeID.replace('-ME-4', '');
routeID = routeID.replace('ME', '');
routeID = routeID.length == 1 ? '00' + routeID : routeID;
routeID = routeID.length == 2 ? '0' + routeID : routeID;
```

**Real-time Data Query:**
```javascript
let realTimeData = await HoustonBusRealtime.findOne({
  _id: stopID,
  'routes._id': routeID,
});
```

**Delay Application:**
```javascript
route2.departure.realtime = tz(row2.arrival.time)
  .utc()
  .add(row2.arrival.delay, 'seconds')
  .format('YYYY-MM-DDTHH:mm:ss+00:00');
```

### parseRoutesAddNoRealtime Function

**Purpose:** Fallback function that normalizes route data without real-time injection

**Parameters:**
- `data`: Object - Route planning data to be normalized

**Returns:** Object - Normalized route data with empty realtime fields

**Use Case:** When real-time data is unavailable or disabled

## 🚀 Usage Methods

### Basic Real-time Integration
```javascript
const houstonRealtime = require('@app/src/services/houstonTransitRealtime');

async function enhanceRouteWithRealtime(routeData) {
  try {
    const enhancedRoute = await houstonRealtime.parseRoutes(routeData);
    
    console.log('Route enhanced with real-time data');
    return enhancedRoute;
  } catch (error) {
    console.error('Real-time enhancement failed:', error);
    
    // Fallback to non-realtime processing
    return await houstonRealtime.parseRoutesAddNoRealtime(routeData);
  }
}
```

### Route Planning Pipeline
```javascript
async function generateTripPlan(origin, destination, departureTime) {
  const houstonRealtime = require('@app/src/services/houstonTransitRealtime');
  
  try {
    // Get initial route plan from HERE or other routing service
    const routePlan = await getBasicRoute(origin, destination, departureTime);
    
    // Check if route includes Houston METRO transit
    const hasHoustonTransit = routePlan.routes.some(route => 
      route.sections.some(section => 
        section.type === 'transit' && 
        section.transport.route_id.includes('ME')
      )
    );
    
    if (hasHoustonTransit) {
      console.log('Enhancing route with Houston METRO real-time data');
      const realtimeRoute = await houstonRealtime.parseRoutes(routePlan);
      
      return {
        ...realtimeRoute,
        realtime_enabled: true,
        last_updated: new Date().toISOString()
      };
    } else {
      return {
        ...routePlan,
        realtime_enabled: false
      };
    }
  } catch (error) {
    console.error('Trip planning failed:', error);
    throw error;
  }
}
```

### Service Status Monitoring
```javascript
class TransitServiceMonitor {
  constructor() {
    this.houstonRealtime = require('@app/src/services/houstonTransitRealtime');
  }

  async checkServiceDisruptions(routeData) {
    try {
      const enhancedData = await this.houstonRealtime.parseRoutes(routeData);
      
      const disruptions = [];
      
      for (const route of enhancedData.routes) {
        for (const section of route.sections) {
          if (section.type === 'transit') {
            if (section.departure.realtime === 'SKIPPED') {
              disruptions.push({
                type: 'SKIPPED',
                route: section.transport.route_id,
                trip: section.transport.trip_id,
                message: 'This trip has been skipped'
              });
            } else if (section.departure.realtime === 'CANCELED') {
              disruptions.push({
                type: 'CANCELED',
                route: section.transport.route_id,
                trip: section.transport.trip_id,
                message: 'This trip has been canceled'
              });
            }
          }
        }
      }
      
      return {
        hasDisruptions: disruptions.length > 0,
        disruptions: disruptions,
        checkedAt: new Date().toISOString()
      };
    } catch (error) {
      console.error('Service disruption check failed:', error);
      return {
        hasDisruptions: null,
        error: error.message
      };
    }
  }

  async getDelayStatistics(routeData) {
    try {
      const enhancedData = await this.houstonRealtime.parseRoutes(routeData);
      
      const delays = [];
      
      for (const route of enhancedData.routes) {
        for (const section of route.sections) {
          if (section.type === 'transit' && section.departure.realtime) {
            if (typeof section.departure.realtime === 'string' && 
                section.departure.realtime.includes('T')) {
              const scheduledTime = new Date(section.departure.time);
              const realtimeTime = new Date(section.departure.realtime);
              const delayMinutes = (realtimeTime - scheduledTime) / (1000 * 60);
              
              delays.push({
                route: section.transport.route_id,
                scheduled: section.departure.time,
                realtime: section.departure.realtime,
                delayMinutes: Math.round(delayMinutes)
              });
            }
          }
        }
      }
      
      const totalDelay = delays.reduce((sum, delay) => sum + delay.delayMinutes, 0);
      const averageDelay = delays.length > 0 ? totalDelay / delays.length : 0;
      
      return {
        totalTrips: delays.length,
        averageDelayMinutes: Math.round(averageDelay * 100) / 100,
        onTimeTrips: delays.filter(d => d.delayMinutes <= 1).length,
        delayedTrips: delays.filter(d => d.delayMinutes > 1).length,
        delays: delays
      };
    } catch (error) {
      console.error('Delay statistics calculation failed:', error);
      return { error: error.message };
    }
  }
}
```

### Real-time Caching Strategy
```javascript
class HoustonRealtimeCache {
  constructor() {
    this.houstonRealtime = require('@app/src/services/houstonTransitRealtime');
    this.cache = new Map();
    this.cacheTimeout = 30000; // 30 seconds
  }

  async getEnhancedRoute(routeData, useCache = true) {
    const routeKey = this.generateRouteKey(routeData);
    
    if (useCache && this.cache.has(routeKey)) {
      const cached = this.cache.get(routeKey);
      
      if (Date.now() - cached.timestamp < this.cacheTimeout) {
        console.log('Returning cached real-time data');
        return cached.data;
      }
    }
    
    try {
      const enhancedRoute = await this.houstonRealtime.parseRoutes(routeData);
      
      this.cache.set(routeKey, {
        data: enhancedRoute,
        timestamp: Date.now()
      });
      
      return enhancedRoute;
    } catch (error) {
      console.error('Real-time enhancement failed, using fallback:', error);
      return await this.houstonRealtime.parseRoutesAddNoRealtime(routeData);
    }
  }

  generateRouteKey(routeData) {
    const transitSections = [];
    
    for (const route of routeData.routes) {
      for (const section of route.sections) {
        if (section.type === 'transit') {
          transitSections.push(`${section.transport.route_id}-${section.transport.trip_id}`);
        }
      }
    }
    
    return transitSections.join('|');
  }

  clearCache() {
    this.cache.clear();
    console.log('Real-time cache cleared');
  }

  getCacheStats() {
    const now = Date.now();
    let validEntries = 0;
    let expiredEntries = 0;
    
    for (const [key, value] of this.cache.entries()) {
      if (now - value.timestamp < this.cacheTimeout) {
        validEntries++;
      } else {
        expiredEntries++;
      }
    }
    
    return {
      totalEntries: this.cache.size,
      validEntries,
      expiredEntries,
      cacheTimeoutMs: this.cacheTimeout
    };
  }
}
```

### Testing and Validation
```javascript
class HoustonRealtimeValidator {
  constructor() {
    this.houstonRealtime = require('@app/src/services/houstonTransitRealtime');
  }

  async validateRealtimeData(routeData) {
    try {
      const originalData = JSON.parse(JSON.stringify(routeData));
      const enhancedData = await this.houstonRealtime.parseRoutes(routeData);
      
      const validationResults = {
        passed: true,
        issues: [],
        transitSections: 0,
        realtimeEnhanced: 0
      };
      
      for (let i = 0; i < enhancedData.routes.length; i++) {
        const route = enhancedData.routes[i];
        
        for (let j = 0; j < route.sections.length; j++) {
          const section = route.sections[j];
          
          if (section.type === 'transit') {
            validationResults.transitSections++;
            
            // Check if route IDs were normalized
            if (section.transport.route_id.includes('-ME-')) {
              validationResults.issues.push(`Route ${i}.${j}: Route ID not normalized: ${section.transport.route_id}`);
              validationResults.passed = false;
            }
            
            // Check if realtime field exists
            if (section.departure.realtime !== undefined) {
              validationResults.realtimeEnhanced++;
              
              // Validate realtime format
              if (typeof section.departure.realtime === 'string' && 
                  section.departure.realtime !== '' &&
                  section.departure.realtime !== 'SKIPPED' &&
                  section.departure.realtime !== 'CANCELED') {
                
                const realtimeDate = new Date(section.departure.realtime);
                if (isNaN(realtimeDate.getTime())) {
                  validationResults.issues.push(`Route ${i}.${j}: Invalid realtime format: ${section.departure.realtime}`);
                  validationResults.passed = false;
                }
              }
            }
          }
        }
      }
      
      return validationResults;
    } catch (error) {
      return {
        passed: false,
        error: error.message,
        issues: ['Validation failed due to processing error']
      };
    }
  }

  createTestData() {
    return {
      routes: [{
        sections: [{
          type: 'transit',
          transport: {
            mode: 'bus',
            route_id: 'ME001-ME-1',
            trip_id: 'ME12345-ME',
            direction_id: '0'
          },
          departure: {
            time: '2024-06-25T14:30:00+00:00',
            place: {
              stop_id: 'ME5001'
            }
          }
        }]
      }]
    };
  }

  async runTests() {
    console.log('Running Houston Real-time Service Tests...');
    
    const testData = this.createTestData();
    
    // Test 1: Basic real-time processing
    try {
      const result1 = await this.houstonRealtime.parseRoutes(testData);
      console.log('✓ Basic real-time processing test passed');
    } catch (error) {
      console.log('✗ Basic real-time processing test failed:', error.message);
    }
    
    // Test 2: No real-time fallback
    try {
      const result2 = await this.houstonRealtime.parseRoutesAddNoRealtime(testData);
      console.log('✓ No real-time fallback test passed');
    } catch (error) {
      console.log('✗ No real-time fallback test failed:', error.message);
    }
    
    // Test 3: Data validation
    try {
      const validation = await this.validateRealtimeData(testData);
      if (validation.passed) {
        console.log('✓ Data validation test passed');
      } else {
        console.log('✗ Data validation test failed:', validation.issues);
      }
    } catch (error) {
      console.log('✗ Data validation test failed:', error.message);
    }
  }
}
```

## 📊 Output Examples

### Enhanced Route with Real-time Data
```json
{
  "routes": [{
    "sections": [{
      "type": "transit",
      "transport": {
        "mode": "bus",
        "route_id": "001",
        "trip_id": "12345",
        "direction_id": "0"
      },
      "departure": {
        "time": "2024-06-25T14:30:00+00:00",
        "realtime": "2024-06-25T14:33:00+00:00",
        "place": {
          "stop_id": "5001"
        }
      }
    }]
  }]
}
```

### Service Disruption Response
```json
{
  "routes": [{
    "sections": [{
      "type": "transit",
      "transport": {
        "mode": "bus",
        "route_id": "002",
        "trip_id": "67890"
      },
      "departure": {
        "time": "2024-06-25T15:00:00+00:00",
        "realtime": "CANCELED",
        "place": {
          "stop_id": "5002"
        }
      }
    }]
  }]
}
```

### Delay Statistics Summary
```json
{
  "totalTrips": 5,
  "averageDelayMinutes": 2.4,
  "onTimeTrips": 2,
  "delayedTrips": 3,
  "delays": [
    {
      "route": "001",
      "scheduled": "2024-06-25T14:30:00+00:00",
      "realtime": "2024-06-25T14:33:00+00:00",
      "delayMinutes": 3
    }
  ]
}
```

## ⚠️ Important Notes

### Houston METRO Specific Implementation
- **Route ID Format:** Handles ME prefixes and numerical padding (001, 002, etc.)
- **Trip ID Processing:** Removes METRO-specific prefixes for database matching
- **Direction Handling:** Uses 0/1 direction IDs for bidirectional routes
- **Stop ID Normalization:** Removes ME prefixes from stop identifiers

### Real-time Data Limitations
- **Data Availability:** Real-time data may not be available for all routes/trips
- **Update Frequency:** Depends on Houston METRO's GTFS-Realtime feed update rate
- **Service Hours:** Real-time data only available during service hours
- **Weekend/Holiday:** May have different data availability patterns

### Error Handling Strategy
- **Database Failures:** Falls back to empty realtime fields
- **Missing Trip Data:** Sets empty realtime when trip not found
- **Invalid Timestamps:** Logs errors but continues processing
- **Service Disruptions:** Properly handles SKIPPED/CANCELED statuses

### Performance Considerations
- **Database Queries:** Individual queries per route section may be slow
- **Batch Processing:** Consider batching lookups for multiple routes
- **Caching Strategy:** Implement caching for frequently requested routes
- **Memory Usage:** Large route datasets may require memory optimization

### Timezone Handling
- **UTC Conversion:** All timestamps converted to UTC for consistency
- **Central Time:** Houston operates in Central Time Zone
- **Daylight Saving:** Automatic handling via moment-timezone
- **API Response:** Always returns ISO 8601 UTC format

### Data Quality Issues
- **ID Mismatches:** Route/trip IDs may not always match between systems
- **Stale Data:** Real-time data may be outdated during service disruptions
- **Format Variations:** Different data sources may have inconsistent formats
- **Service Changes:** Route modifications may cause temporary data issues

## 🔗 Related File Links

- **Real-time Data Model:** `allrepo/connectsmart/tsp-api/src/models/HoustonBusRealtime.js`
- **Transit Controllers:** Controllers handling Houston METRO trip planning
- **GTFS Integration:** General Transit Feed Specification processing services
- **Time Zone Services:** Timezone conversion utilities

---
*This service provides essential real-time transit information for Houston METRO system integration within the TSP platform.*