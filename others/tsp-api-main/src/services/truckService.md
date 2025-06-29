# TSP API Truck Service Documentation

## 🔍 Quick Summary (TL;DR)
The Truck Service provides truck mapping data retrieval with timestamp-based change detection, MongoDB integration, data validation, and efficient caching through last-modified timestamp comparison to minimize unnecessary data transfers.

**Keywords:** truck-mapping | mongodb-integration | timestamp-tracking | data-validation | change-detection | caching-optimization | truck-routes | map-data

**Primary use cases:** Retrieving latest truck route mapping data, checking for updates since last fetch, providing efficient data synchronization for truck routing

**Compatibility:** Node.js >= 16.0.0, MongoDB with truck mapping collections, moment.js for timestamp handling, Joi schema validation

## ❓ Common Questions Quick Index
- **Q: What does this service track?** → Truck route mapping data with timestamps for change detection
- **Q: How does change detection work?** → Compares previous timestamp with latest data creation timestamp
- **Q: What happens if no changes exist?** → Returns empty object to indicate no updates available
- **Q: How is data validated?** → Uses Joi schema validation for MongoDB document structure
- **Q: What's the data structure?** → Returns last_modified timestamp and map_array with truck mapping data
- **Q: How are errors handled?** → Comprehensive error logging with graceful empty object fallback

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **truck route update checker** that helps apps know when new truck routing information is available. Instead of constantly downloading the same data, it only provides updates when something has actually changed, saving bandwidth and improving performance.

**Technical explanation:** 
A lightweight data synchronization service that manages truck mapping information retrieval from MongoDB with timestamp-based change detection, implements efficient caching strategies through last-modified comparison, provides data validation through Joi schemas, and ensures optimal performance by returning empty responses when no updates are available.

**Business value explanation:**
Enables efficient truck route data distribution, reduces bandwidth usage through smart caching, provides reliable truck mapping updates for logistics applications, supports real-time route optimization systems, and ensures data integrity through validation mechanisms.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/truckService.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with MongoDB and class-based architecture
- **Type:** Truck Mapping Data Retrieval Service
- **File Size:** ~1.1 KB
- **Complexity Score:** ⭐⭐ (Low-Medium - Simple data retrieval with validation)

**Dependencies:**
- `../models/truckModel`: MongoDB truck mapping schema (**Critical**)
- `moment-timezone`: Timestamp conversion and handling (**High**)
- `../schemas/truckJoiSchema`: Data validation schemas (**High**)
- `@maas/core/log`: Error logging system (**Medium**)

## 📝 Detailed Code Analysis

### TruckMapService Class Architecture

### Class Constructor and Initialization
**Purpose:** Sets up the service with data validation capabilities

```javascript
class TruckMapService {
  constructor() {
    this.validatorMangoDbData = validatorTruck.validateTruckMapMongoDBData;
  }
}
```

**Constructor Features:**
- **Validator Binding:** Links Joi schema validator for MongoDB data validation
- **Class-Based Design:** Object-oriented approach for service encapsulation
- **Simple Initialization:** Minimal setup with validator reference

### Latest Truck Map Retrieval System

### getLatestTruckMap Function
**Purpose:** Retrieves latest truck mapping data with timestamp-based change detection

```javascript
async getLatestTruckMap(previousLastModifiedTimestamp) {
  try {
    // Get latest truck map from MongoDB
    const latestTruckMap = await truckMapSchema.findOne(
      {},
      {},
      { sort: { created_at: -1 } },
    );
    
    if (latestTruckMap) {
      // Validate retrieved data
      await this.validatorMangoDbData.validateAsync(latestTruckMap.toJSON());
      
      // Extract and convert timestamp
      const createdAt = latestTruckMap.created_at;
      const createdAtUnixTime = moment(createdAt).unix();
      
      // Check if data has changed since last request
      if (previousLastModifiedTimestamp != createdAtUnixTime) {
        const truckMapInfo = {
          last_modified: createdAtUnixTime,
          map_array: latestTruckMap.truck_map,
        };
        return truckMapInfo;
      }
    }
  } catch (error) {
    logger.error(error);
  }
  
  // Return empty object if no changes or error
  return {};
}
```

**Data Retrieval Features:**
- **Latest Data Query:** MongoDB sort by created_at descending to get newest entry
- **Data Validation:** Joi schema validation ensures data integrity
- **Timestamp Comparison:** Unix timestamp comparison for change detection
- **Conditional Response:** Only returns data if changes detected
- **Error Handling:** Graceful error handling with logging and empty object fallback

### Timestamp Management and Optimization

### Change Detection Logic
```javascript
// Convert MongoDB date to Unix timestamp
const createdAt = latestTruckMap.created_at;
const createdAtUnixTime = moment(createdAt).unix();

// Compare with previous timestamp (loose equality for string/number comparison)
if (previousLastModifiedTimestamp != createdAtUnixTime) {
  const truckMapInfo = {
    last_modified: createdAtUnixTime,
    map_array: latestTruckMap.truck_map,
  };
  return truckMapInfo;
}
```

**Optimization Features:**
- **Unix Timestamp Conversion:** Consistent timestamp format for comparison
- **Loose Equality Check:** Handles string/number type differences gracefully
- **Bandwidth Optimization:** Prevents unnecessary data transfer when no changes
- **Last Modified Tracking:** Provides timestamp for client-side caching

### Data Structure and Response Format

### Response Structure
```javascript
const truckMapInfo = {
  last_modified: createdAtUnixTime,
  map_array: latestTruckMap.truck_map,
};
```

**Response Features:**
- **Standardized Format:** Consistent response structure with timestamp and data
- **Truck Map Array:** Complete truck mapping data in array format
- **Timestamp Inclusion:** Last modified timestamp for subsequent requests
- **Empty Object Fallback:** Returns {} when no changes or errors occur

## 🚀 Usage Methods

### Basic Truck Service Usage
```javascript
const { TruckMapService } = require('@app/src/services/truckService');

// Initialize service
const truckService = new TruckMapService();

// Get latest truck map (first time - no previous timestamp)
const initialData = await truckService.getLatestTruckMap(null);
console.log('Initial truck map:', initialData);
// Output: { last_modified: 1719316200, map_array: [...] }

// Check for updates using previous timestamp
const updatedData = await truckService.getLatestTruckMap(initialData.last_modified);
console.log('Updated truck map:', updatedData);
// Output: {} if no changes, or new data structure if updated
```

### Advanced Truck Map Management System
```javascript
class TruckMapManager {
  constructor() {
    this.truckService = new TruckMapService();
    this.currentMapData = null;
    this.lastModified = null;
    this.updateHistory = [];
    this.checkInterval = null;
    this.subscribers = new Set();
  }

  async initializeMap() {
    try {
      console.log('Initializing truck map data...');
      const mapData = await this.truckService.getLatestTruckMap(null);
      
      if (mapData && mapData.map_array) {
        this.currentMapData = mapData.map_array;
        this.lastModified = mapData.last_modified;
        
        this.updateHistory.push({
          timestamp: new Date().toISOString(),
          lastModified: mapData.last_modified,
          mapSize: mapData.map_array.length,
          action: 'initial_load'
        });
        
        console.log(`Truck map initialized with ${mapData.map_array.length} entries`);
        this.notifySubscribers('initialized', mapData);
        
        return {
          success: true,
          mapSize: mapData.map_array.length,
          lastModified: mapData.last_modified
        };
      } else {
        throw new Error('No truck map data available');
      }
    } catch (error) {
      console.error('Error initializing truck map:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  async checkForUpdates() {
    try {
      console.log(`Checking for truck map updates since ${this.lastModified}...`);
      const mapData = await this.truckService.getLatestTruckMap(this.lastModified);
      
      if (mapData && mapData.map_array) {
        const previousSize = this.currentMapData ? this.currentMapData.length : 0;
        
        this.currentMapData = mapData.map_array;
        this.lastModified = mapData.last_modified;
        
        this.updateHistory.push({
          timestamp: new Date().toISOString(),
          lastModified: mapData.last_modified,
          mapSize: mapData.map_array.length,
          previousSize,
          action: 'update'
        });
        
        console.log(`Truck map updated: ${previousSize} → ${mapData.map_array.length} entries`);
        this.notifySubscribers('updated', mapData);
        
        return {
          success: true,
          updated: true,
          mapSize: mapData.map_array.length,
          previousSize,
          lastModified: mapData.last_modified
        };
      } else {
        console.log('No truck map updates available');
        return {
          success: true,
          updated: false,
          message: 'No updates available'
        };
      }
    } catch (error) {
      console.error('Error checking for truck map updates:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  startAutoUpdates(intervalMinutes = 5) {
    if (this.checkInterval) {
      clearInterval(this.checkInterval);
    }

    console.log(`Starting auto-updates every ${intervalMinutes} minutes`);
    this.checkInterval = setInterval(async () => {
      await this.checkForUpdates();
    }, intervalMinutes * 60 * 1000);

    return {
      success: true,
      interval: intervalMinutes,
      message: `Auto-updates started every ${intervalMinutes} minutes`
    };
  }

  stopAutoUpdates() {
    if (this.checkInterval) {
      clearInterval(this.checkInterval);
      this.checkInterval = null;
      
      return {
        success: true,
        message: 'Auto-updates stopped'
      };
    } else {
      return {
        success: false,
        message: 'Auto-updates not running'
      };
    }
  }

  subscribe(callback) {
    if (typeof callback === 'function') {
      this.subscribers.add(callback);
      
      // Send current data to new subscriber
      if (this.currentMapData) {
        callback('current', {
          last_modified: this.lastModified,
          map_array: this.currentMapData
        });
      }
      
      return {
        success: true,
        message: 'Subscribed to truck map updates'
      };
    } else {
      return {
        success: false,
        error: 'Callback must be a function'
      };
    }
  }

  unsubscribe(callback) {
    const removed = this.subscribers.delete(callback);
    return {
      success: removed,
      message: removed ? 'Unsubscribed from updates' : 'Callback not found'
    };
  }

  notifySubscribers(eventType, data) {
    this.subscribers.forEach(callback => {
      try {
        callback(eventType, data);
      } catch (error) {
        console.error('Error notifying subscriber:', error);
      }
    });
  }

  getCurrentMap() {
    return {
      success: true,
      data: this.currentMapData,
      lastModified: this.lastModified,
      mapSize: this.currentMapData ? this.currentMapData.length : 0
    };
  }

  getUpdateHistory(limit = 10) {
    return {
      success: true,
      history: this.updateHistory.slice(-limit),
      totalUpdates: this.updateHistory.length
    };
  }

  analyzeMapChanges() {
    if (this.updateHistory.length < 2) {
      return {
        success: false,
        message: 'Insufficient update history for analysis'
      };
    }

    const history = this.updateHistory;
    const changes = [];
    
    for (let i = 1; i < history.length; i++) {
      const current = history[i];
      const previous = history[i - 1];
      
      changes.push({
        timestamp: current.timestamp,
        sizeDelta: current.mapSize - previous.mapSize,
        previousSize: previous.mapSize,
        newSize: current.mapSize,
        action: current.action
      });
    }

    const sizeTrend = changes.map(c => c.sizeDelta);
    const averageChange = sizeTrend.reduce((sum, delta) => sum + delta, 0) / sizeTrend.length;
    const maxIncrease = Math.max(...sizeTrend);
    const maxDecrease = Math.min(...sizeTrend);

    return {
      success: true,
      analysis: {
        totalChanges: changes.length,
        averageChange: Math.round(averageChange * 100) / 100,
        maxIncrease,
        maxDecrease,
        currentSize: this.currentMapData ? this.currentMapData.length : 0,
        trend: averageChange > 0 ? 'growing' : averageChange < 0 ? 'shrinking' : 'stable'
      },
      changes
    };
  }

  async forceRefresh() {
    console.log('Forcing truck map refresh...');
    const previousLastModified = this.lastModified;
    this.lastModified = null; // Force update by clearing timestamp
    
    const result = await this.checkForUpdates();
    
    if (!result.success || !result.updated) {
      // Restore previous timestamp if refresh failed
      this.lastModified = previousLastModified;
    }
    
    return {
      ...result,
      forced: true
    };
  }

  getServiceStats() {
    return {
      success: true,
      stats: {
        currentMapSize: this.currentMapData ? this.currentMapData.length : 0,
        lastModified: this.lastModified,
        totalUpdates: this.updateHistory.length,
        subscriberCount: this.subscribers.size,
        autoUpdatesRunning: !!this.checkInterval,
        serviceUptime: this.updateHistory.length > 0 
          ? new Date().getTime() - new Date(this.updateHistory[0].timestamp).getTime()
          : 0
      }
    };
  }

  async validateCurrentMap() {
    try {
      if (!this.currentMapData) {
        return {
          success: false,
          error: 'No current map data to validate'
        };
      }

      // Simulate validation of map data structure
      const validationResults = {
        totalEntries: this.currentMapData.length,
        validEntries: 0,
        invalidEntries: 0,
        errors: []
      };

      this.currentMapData.forEach((entry, index) => {
        try {
          // Basic validation - check for required fields
          if (entry && typeof entry === 'object') {
            validationResults.validEntries++;
          } else {
            validationResults.invalidEntries++;
            validationResults.errors.push(`Entry ${index}: Invalid structure`);
          }
        } catch (error) {
          validationResults.invalidEntries++;
          validationResults.errors.push(`Entry ${index}: ${error.message}`);
        }
      });

      return {
        success: true,
        validation: validationResults,
        isValid: validationResults.invalidEntries === 0
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  cleanup() {
    this.stopAutoUpdates();
    this.subscribers.clear();
    this.updateHistory = [];
    this.currentMapData = null;
    this.lastModified = null;
    
    return {
      success: true,
      message: 'Truck map manager cleaned up'
    };
  }
}

// Usage
const truckManager = new TruckMapManager();

// Initialize truck map
const initResult = await truckManager.initializeMap();
console.log('Initialization result:', initResult);

// Start auto-updates every 5 minutes
const autoUpdateResult = truckManager.startAutoUpdates(5);
console.log('Auto-update result:', autoUpdateResult);

// Subscribe to updates
const subscription = truckManager.subscribe((eventType, data) => {
  console.log(`Truck map ${eventType}:`, {
    lastModified: data.last_modified,
    mapSize: data.map_array.length
  });
});

// Get current map
const currentMap = truckManager.getCurrentMap();
console.log('Current map info:', currentMap);

// Check for updates manually
const updateCheck = await truckManager.checkForUpdates();
console.log('Update check result:', updateCheck);

// Get update history
const history = truckManager.getUpdateHistory(5);
console.log('Update history:', history);

// Analyze map changes
const analysis = truckManager.analyzeMapChanges();
console.log('Map analysis:', analysis);

// Get service statistics
const stats = truckManager.getServiceStats();
console.log('Service stats:', stats);
```

### Real-Time Truck Route Integration
```javascript
class TruckRouteOptimizer {
  constructor() {
    this.truckManager = new TruckMapManager();
    this.activeRoutes = new Map();
    this.routeCache = new Map();
    this.optimizationHistory = [];
  }

  async initialize() {
    try {
      await this.truckManager.initializeMap();
      
      // Subscribe to map updates
      this.truckManager.subscribe((eventType, data) => {
        if (eventType === 'updated') {
          this.invalidateRouteCache();
          this.reoptimizeActiveRoutes();
        }
      });

      return { success: true, message: 'Truck route optimizer initialized' };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  async optimizeRoute(origin, destination, truckSpecs = {}) {
    try {
      const routeKey = `${origin.lat},${origin.lng}_${destination.lat},${destination.lng}`;
      
      // Check cache first
      if (this.routeCache.has(routeKey)) {
        const cached = this.routeCache.get(routeKey);
        if (Date.now() - cached.timestamp < 300000) { // 5-minute cache
          return {
            success: true,
            route: cached.route,
            fromCache: true,
            cacheAge: Date.now() - cached.timestamp
          };
        }
      }

      // Get current truck map
      const mapData = this.truckManager.getCurrentMap();
      if (!mapData.success || !mapData.data) {
        throw new Error('No truck map data available');
      }

      // Simulate route optimization using truck map
      const optimizedRoute = this.calculateOptimalRoute(
        origin,
        destination,
        mapData.data,
        truckSpecs
      );

      // Cache the result
      this.routeCache.set(routeKey, {
        route: optimizedRoute,
        timestamp: Date.now()
      });

      // Track optimization
      this.optimizationHistory.push({
        timestamp: new Date().toISOString(),
        origin,
        destination,
        routeLength: optimizedRoute.distance,
        estimatedTime: optimizedRoute.duration
      });

      return {
        success: true,
        route: optimizedRoute,
        fromCache: false,
        mapVersion: mapData.lastModified
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  calculateOptimalRoute(origin, destination, truckMap, truckSpecs) {
    // Simulate route calculation logic
    const baseDistance = this.calculateDistance(origin, destination);
    const baseDuration = baseDistance / 50; // 50 km/h average speed
    
    return {
      distance: Math.round(baseDistance * 1000) / 1000, // km
      duration: Math.round(baseDuration * 60), // minutes
      waypoints: [origin, destination],
      truckRestrictions: this.identifyRestrictions(truckMap, truckSpecs),
      optimizedFor: 'time_and_fuel',
      calculatedAt: new Date().toISOString()
    };
  }

  calculateDistance(point1, point2) {
    // Haversine formula for distance calculation
    const R = 6371; // Earth's radius in km
    const dLat = (point2.lat - point1.lat) * Math.PI / 180;
    const dLng = (point2.lng - point1.lng) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(point1.lat * Math.PI / 180) * Math.cos(point2.lat * Math.PI / 180) *
              Math.sin(dLng/2) * Math.sin(dLng/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
  }

  identifyRestrictions(truckMap, truckSpecs) {
    // Simulate restriction identification
    const restrictions = [];
    
    if (truckSpecs.weight > 40000) { // 40 ton limit
      restrictions.push('weight_restricted_routes');
    }
    
    if (truckSpecs.height > 4.2) { // 4.2m height limit
      restrictions.push('height_restricted_bridges');
    }
    
    return restrictions;
  }

  invalidateRouteCache() {
    this.routeCache.clear();
    console.log('Route cache invalidated due to map update');
  }

  async reoptimizeActiveRoutes() {
    console.log(`Reoptimizing ${this.activeRoutes.size} active routes...`);
    
    for (const [routeId, routeInfo] of this.activeRoutes.entries()) {
      try {
        const newRoute = await this.optimizeRoute(
          routeInfo.origin,
          routeInfo.destination,
          routeInfo.truckSpecs
        );
        
        if (newRoute.success) {
          routeInfo.route = newRoute.route;
          routeInfo.lastOptimized = new Date().toISOString();
          console.log(`Route ${routeId} reoptimized successfully`);
        }
      } catch (error) {
        console.error(`Error reoptimizing route ${routeId}:`, error);
      }
    }
  }

  getOptimizationStats() {
    return {
      totalOptimizations: this.optimizationHistory.length,
      activeRoutes: this.activeRoutes.size,
      cacheSize: this.routeCache.size,
      averageRouteDistance: this.optimizationHistory.length > 0
        ? this.optimizationHistory.reduce((sum, opt) => sum + opt.routeLength, 0) / this.optimizationHistory.length
        : 0
    };
  }
}

// Usage
const routeOptimizer = new TruckRouteOptimizer();
await routeOptimizer.initialize();

const route = await routeOptimizer.optimizeRoute(
  { lat: 29.7604, lng: -95.3698 }, // Houston
  { lat: 32.7767, lng: -96.7970 }, // Dallas
  { weight: 35000, height: 4.0, length: 18.5 }
);

console.log('Optimized route:', route);
```

## 📊 Output Examples

### Successful Data Retrieval
```javascript
{
  last_modified: 1719316200,
  map_array: [
    {
      route_id: "TR001",
      coordinates: [[29.7604, -95.3698], [32.7767, -96.7970]],
      restrictions: ["weight_limit_40t", "height_limit_4.2m"],
      road_type: "highway"
    },
    {
      route_id: "TR002", 
      coordinates: [[30.2672, -97.7431], [31.7619, -106.4850]],
      restrictions: ["hazmat_prohibited"],
      road_type: "arterial"
    }
  ]
}
```

### No Updates Available
```javascript
{}
```

### Truck Map Manager Initialization
```javascript
{
  success: true,
  mapSize: 150,
  lastModified: 1719316200
}
```

### Update Check Result
```javascript
{
  success: true,
  updated: true,
  mapSize: 165,
  previousSize: 150,
  lastModified: 1719320400
}
```

### Map Analysis
```javascript
{
  success: true,
  analysis: {
    totalChanges: 12,
    averageChange: 3.5,
    maxIncrease: 15,
    maxDecrease: -2,
    currentSize: 165,
    trend: "growing"
  },
  changes: [
    {
      timestamp: "2024-06-25T14:30:00Z",
      sizeDelta: 15,
      previousSize: 150,
      newSize: 165,
      action: "update"
    }
  ]
}
```

### Service Statistics
```javascript
{
  success: true,
  stats: {
    currentMapSize: 165,
    lastModified: 1719320400,
    totalUpdates: 8,
    subscriberCount: 2,
    autoUpdatesRunning: true,
    serviceUptime: 3600000
  }
}
```

### Route Optimization Result
```javascript
{
  success: true,
  route: {
    distance: 362.5,
    duration: 435,
    waypoints: [
      { lat: 29.7604, lng: -95.3698 },
      { lat: 32.7767, lng: -96.7970 }
    ],
    truckRestrictions: ["weight_restricted_routes"],
    optimizedFor: "time_and_fuel",
    calculatedAt: "2024-06-25T14:30:00Z"
  },
  fromCache: false,
  mapVersion: 1719320400
}
```

## ⚠️ Important Notes

### Data Synchronization and Caching
- **Timestamp-Based Updates:** Uses Unix timestamps for efficient change detection
- **Bandwidth Optimization:** Returns empty object when no changes exist to minimize data transfer
- **MongoDB Querying:** Efficiently queries latest document using sort on created_at field
- **Client-Side Caching:** Enables effective client-side caching through last_modified timestamps

### Data Validation and Integrity
- **Joi Schema Validation:** Ensures data structure consistency before returning results
- **Error Handling:** Graceful error handling with logging and empty object fallback
- **Type Safety:** Proper handling of timestamp comparisons with loose equality
- **Document Conversion:** Converts MongoDB documents to JSON for validation

### Performance Considerations
- **Single Document Query:** Retrieves only the latest document for efficiency
- **Conditional Response:** Only processes and returns data when changes detected
- **Memory Efficiency:** Minimal memory footprint with simple class structure
- **Error Recovery:** Continues operation even when validation or retrieval fails

### MongoDB Integration
- **Schema Dependencies:** Requires properly structured truckMapSchema model
- **Index Requirements:** Should have index on created_at field for optimal performance
- **Document Structure:** Expects truck_map field containing array of mapping data
- **Connection Management:** Relies on established MongoDB connection through model

## 🔗 Related File Links

- **Truck Model:** `allrepo/connectsmart/tsp-api/src/models/truckModel.js`
- **Truck Validation:** `allrepo/connectsmart/tsp-api/src/schemas/truckJoiSchema.js`
- **Core Logging:** `@maas/core/log` logging infrastructure
- **Route Services:** Services that may integrate truck routing capabilities

---
*This service provides efficient truck mapping data retrieval with smart caching and change detection for the TSP platform.*