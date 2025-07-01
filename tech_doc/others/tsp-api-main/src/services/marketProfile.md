# TSP API Market Profile Service Documentation

## 🔍 Quick Summary (TL;DR)
The Market Profile service provides geographic market configuration data including service area polygons, timezone settings, and market identifiers for the ConnectSmart transportation platform, primarily focused on the Houston Community Services (HCS) market.

**Keywords:** market-configuration | service-area | geographic-boundaries | timezone-config | polygon-data | market-settings | geo-service-area | region-config

**Primary use cases:** Defining service area boundaries, timezone configuration, market identification, geographic service validation, location-based feature enablement

**Compatibility:** Node.js >= 16.0.0, WKT polygon format support, geographic coordinate systems

## ❓ Common Questions Quick Index
- **Q: What markets are supported?** → Currently configured for ConnectSmart (HCS - Houston Community Services)
- **Q: What's the polygon format?** → WKT (Well-Known Text) POLYGON format with coordinate pairs
- **Q: What coordinate system is used?** → Standard WGS84 (longitude, latitude) decimal degrees
- **Q: How large is the service area?** → Covers greater Houston metropolitan area with detailed boundary polygon
- **Q: Can new markets be added?** → Yes, by adding new profile objects to the profiles configuration
- **Q: What timezone is configured?** → America/Chicago (Central Time) for the HCS market

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **geographic rulebook** for the transportation service. It defines exactly where the service operates (like city limits), what time zone to use for scheduling, and what to call that service area. When the app needs to know "are we allowed to provide service here?" or "what time is it in this market?", it checks this configuration.

**Technical explanation:** 
A geographic configuration service that provides market-specific settings including detailed service area polygons in WKT format, timezone configurations, and market identifiers. Acts as a centralized repository for geographic business rules and service boundaries, enabling location-aware features and market-specific behavior.

**Business value explanation:**
Essential for geographic market expansion, service area management, and location-based business rules. Enables precise service boundary enforcement, supports multi-market operations, facilitates geographic analytics, and provides foundation for location-based pricing and feature availability.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/marketProfile.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js configuration service
- **Type:** Geographic Configuration Service
- **File Size:** ~1.1 MB (due to detailed polygon coordinates)
- **Complexity Score:** ⭐⭐ (Low-Medium - Large data structure with simple access pattern)

**Dependencies:**
- `@maas/core/log`: Logging infrastructure (**High**)

## 📝 Detailed Code Analysis

### Market Profile Structure

**ConnectSmart Profile:**
```javascript
{
  "market": "HCS",
  "timezone": "America/Chicago", 
  "polygon": "POLYGON ((-96.03311 29.72802, ...))"
}
```

**Profile Fields:**
- `market`: String - Market identifier ("HCS" for Houston Community Services)
- `timezone`: String - IANA timezone identifier for the market
- `polygon`: String - WKT POLYGON defining service area boundaries

### Service Area Coverage

**Geographic Scope:** Greater Houston Metropolitan Area
- **Primary Coverage:** Houston, TX and surrounding suburbs
- **Coordinate Range:** Approximately -96.19 to -95.36 longitude, 29.72 to 30.63 latitude
- **Area Coverage:** Extensive polygon with thousands of coordinate points for precise boundary definition

### Module Export Function

**Purpose:** Returns market profile configuration for specified application

**Parameters:**
- `app`: String - Application identifier (case-insensitive)

**Returns:** Object - Market profile configuration or null if not found

**Implementation:**
```javascript
module.exports = function (app) {
  const k = app.toLowerCase();
  if (Object.keys(profiles).indexOf(k) === -1) {
    logger.error(`Service profile not found for app: ${app}`);
    return null;
  }
  return profiles[k];
};
```

**Error Handling:** Logs error and returns null for unknown applications

## 🚀 Usage Methods

### Basic Profile Retrieval
```javascript
const getMarketProfile = require('@app/src/services/marketProfile');

function getServiceConfiguration(appName) {
  try {
    const profile = getMarketProfile(appName);
    
    if (!profile) {
      console.log(`No profile found for application: ${appName}`);
      return null;
    }
    
    console.log(`Market: ${profile.market}`);
    console.log(`Timezone: ${profile.timezone}`);
    console.log(`Service area defined: ${profile.polygon ? 'Yes' : 'No'}`);
    
    return profile;
  } catch (error) {
    console.error('Error retrieving market profile:', error);
    throw error;
  }
}

// Usage
const connectSmartProfile = getServiceConfiguration('connectsmart');
```

### Geographic Boundary Validation
```javascript
const turf = require('@turf/turf');
const { parse } = require('wkt');

class MarketBoundaryValidator {
  constructor() {
    this.getMarketProfile = require('@app/src/services/marketProfile');
  }

  getServiceArea(appName) {
    const profile = this.getMarketProfile(appName);
    
    if (!profile || !profile.polygon) {
      throw new Error(`No service area defined for ${appName}`);
    }
    
    try {
      const geoJson = parse(profile.polygon);
      return turf.polygon(geoJson.coordinates);
    } catch (error) {
      throw new Error(`Invalid polygon format: ${error.message}`);
    }
  }

  isLocationInServiceArea(appName, latitude, longitude) {
    try {
      const serviceArea = this.getServiceArea(appName);
      const point = turf.point([longitude, latitude]);
      
      return turf.booleanPointInPolygon(point, serviceArea);
    } catch (error) {
      console.error('Location validation failed:', error);
      return false;
    }
  }

  getServiceAreaStats(appName) {
    try {
      const serviceArea = this.getServiceArea(appName);
      const bbox = turf.bbox(serviceArea);
      const area = turf.area(serviceArea);
      
      return {
        boundingBox: {
          west: bbox[0],
          south: bbox[1], 
          east: bbox[2],
          north: bbox[3]
        },
        areaSquareMeters: area,
        areaSquareKilometers: area / 1000000,
        coordinateCount: this.getCoordinateCount(appName)
      };
    } catch (error) {
      console.error('Failed to calculate service area stats:', error);
      throw error;
    }
  }

  getCoordinateCount(appName) {
    const profile = this.getMarketProfile(appName);
    if (!profile || !profile.polygon) return 0;
    
    // Count coordinate pairs in WKT polygon
    const matches = profile.polygon.match(/-?\d+\.?\d*\s+-?\d+\.?\d*/g);
    return matches ? matches.length : 0;
  }
}
```

### Timezone Management Service
```javascript
const moment = require('moment-timezone');

class MarketTimezoneService {
  constructor() {
    this.getMarketProfile = require('@app/src/services/marketProfile');
  }

  getMarketTimezone(appName) {
    const profile = this.getMarketProfile(appName);
    
    if (!profile || !profile.timezone) {
      throw new Error(`No timezone configured for ${appName}`);
    }
    
    return profile.timezone;
  }

  getCurrentTimeInMarket(appName) {
    const timezone = this.getMarketTimezone(appName);
    return moment().tz(timezone);
  }

  convertToMarketTime(dateTime, appName) {
    const timezone = this.getMarketTimezone(appName);
    return moment(dateTime).tz(timezone);
  }

  getMarketBusinessHours(appName) {
    const timezone = this.getMarketTimezone(appName);
    const now = moment().tz(timezone);
    
    return {
      timezone: timezone,
      currentTime: now.format('YYYY-MM-DD HH:mm:ss z'),
      businessDay: now.format('dddd'),
      isWeekend: now.day() === 0 || now.day() === 6,
      businessHours: {
        start: '09:00',
        end: '17:00'
      }
    };
  }

  formatTimeForMarket(dateTime, appName, format = 'YYYY-MM-DD HH:mm:ss z') {
    const timezone = this.getMarketTimezone(appName);
    return moment(dateTime).tz(timezone).format(format);
  }
}
```

### Multi-Market Configuration Manager
```javascript
class MultiMarketConfigManager {
  constructor() {
    this.getMarketProfile = require('@app/src/services/marketProfile');
    this.boundaryValidator = new MarketBoundaryValidator();
    this.timezoneService = new MarketTimezoneService();
  }

  getAllConfiguredMarkets() {
    // This would need to be updated to dynamically read profiles
    // Currently only 'connectsmart' is configured
    return ['connectsmart'];
  }

  getMarketForLocation(latitude, longitude) {
    const markets = this.getAllConfiguredMarkets();
    
    for (const market of markets) {
      try {
        if (this.boundaryValidator.isLocationInServiceArea(market, latitude, longitude)) {
          return {
            app: market,
            profile: this.getMarketProfile(market)
          };
        }
      } catch (error) {
        console.error(`Error checking ${market} boundaries:`, error);
      }
    }
    
    return null;
  }

  getMarketCapabilities(appName) {
    const profile = this.getMarketProfile(appName);
    
    if (!profile) {
      return { available: false };
    }
    
    try {
      const stats = this.boundaryValidator.getServiceAreaStats(appName);
      const timeInfo = this.timezoneService.getMarketBusinessHours(appName);
      
      return {
        available: true,
        market: profile.market,
        timezone: profile.timezone,
        serviceArea: {
          defined: true,
          areaKm2: stats.areaSquareKilometers,
          boundingBox: stats.boundingBox
        },
        localTime: timeInfo.currentTime,
        businessHours: timeInfo.businessHours
      };
    } catch (error) {
      return {
        available: true,
        market: profile.market,
        timezone: profile.timezone,
        error: error.message
      };
    }
  }

  compareMarkets() {
    const markets = this.getAllConfiguredMarkets();
    const comparison = [];
    
    for (const market of markets) {
      const capabilities = this.getMarketCapabilities(market);
      comparison.push({
        app: market,
        ...capabilities
      });
    }
    
    return comparison;
  }
}
```

### Service Area Analytics
```javascript
class ServiceAreaAnalytics {
  constructor() {
    this.getMarketProfile = require('@app/src/services/marketProfile');
    this.boundaryValidator = new MarketBoundaryValidator();
  }

  generateServiceAreaReport(appName) {
    try {
      const profile = this.getMarketProfile(appName);
      const stats = this.boundaryValidator.getServiceAreaStats(appName);
      
      const report = {
        market: profile.market,
        timezone: profile.timezone,
        polygon: {
          format: 'WKT',
          coordinateCount: stats.coordinateCount,
          area: {
            squareMeters: stats.areaSquareMeters,
            squareKilometers: Math.round(stats.areaSquareKilometers * 100) / 100,
            squareMiles: Math.round((stats.areaSquareKilometers * 0.386102) * 100) / 100
          },
          boundingBox: {
            ...stats.boundingBox,
            width: Math.round((stats.boundingBox.east - stats.boundingBox.west) * 111.32 * 100) / 100, // km
            height: Math.round((stats.boundingBox.north - stats.boundingBox.south) * 110.54 * 100) / 100 // km
          }
        },
        coverage: this.analyzeGeographicCoverage(stats.boundingBox)
      };
      
      return report;
    } catch (error) {
      console.error('Failed to generate service area report:', error);
      throw error;
    }
  }

  analyzeGeographicCoverage(boundingBox) {
    // Analyze based on Houston area knowledge
    const analysis = {
      region: 'Greater Houston Metropolitan Area',
      majorCities: ['Houston', 'Sugar Land', 'The Woodlands', 'Pearland'],
      coverage: {
        north: boundingBox.north > 30.2 ? 'Extends to northern suburbs' : 'Central Houston focus',
        south: boundingBox.south < 29.5 ? 'Includes southern suburbs' : 'Inner city coverage',
        east: boundingBox.east > -95.0 ? 'Extends to east Houston' : 'West/Central focus',
        west: boundingBox.west < -96.0 ? 'Includes western suburbs' : 'Central area only'
      }
    };
    
    return analysis;
  }

  validatePolygonIntegrity(appName) {
    const profile = this.getMarketProfile(appName);
    
    if (!profile || !profile.polygon) {
      return { valid: false, error: 'No polygon defined' };
    }
    
    try {
      const geoJson = parse(profile.polygon);
      const polygon = turf.polygon(geoJson.coordinates);
      
      // Basic validation checks
      const area = turf.area(polygon);
      const bbox = turf.bbox(polygon);
      
      const validation = {
        valid: true,
        checks: {
          wktFormat: true,
          geometryValid: true,
          hasArea: area > 0,
          reasonable: area > 1000000 && area < 50000000000, // 1km² to 50,000km²
          boundingBox: {
            width: bbox[2] - bbox[0],
            height: bbox[3] - bbox[1]
          }
        },
        area: area,
        perimeter: this.calculatePolygonPerimeter(polygon)
      };
      
      validation.issues = [];
      
      if (!validation.checks.hasArea) {
        validation.issues.push('Polygon has no area');
      }
      
      if (!validation.checks.reasonable) {
        validation.issues.push('Polygon area seems unreasonable for a market');
      }
      
      validation.valid = validation.issues.length === 0;
      
      return validation;
    } catch (error) {
      return {
        valid: false,
        error: error.message
      };
    }
  }

  calculatePolygonPerimeter(polygon) {
    try {
      return turf.length(polygon, { units: 'kilometers' });
    } catch (error) {
      return null;
    }
  }
}
```

### Configuration Testing
```javascript
class MarketProfileTester {
  constructor() {
    this.getMarketProfile = require('@app/src/services/marketProfile');
    this.analytics = new ServiceAreaAnalytics();
  }

  runBasicTests() {
    const tests = [];
    
    // Test 1: Valid app returns profile
    try {
      const profile = this.getMarketProfile('connectsmart');
      tests.push({
        test: 'Valid app returns profile',
        passed: profile !== null,
        result: profile ? 'Profile found' : 'No profile returned'
      });
    } catch (error) {
      tests.push({
        test: 'Valid app returns profile',
        passed: false,
        error: error.message
      });
    }
    
    // Test 2: Invalid app returns null
    try {
      const profile = this.getMarketProfile('invalid');
      tests.push({
        test: 'Invalid app returns null',
        passed: profile === null,
        result: profile === null ? 'Correctly returned null' : 'Unexpected result'
      });
    } catch (error) {
      tests.push({
        test: 'Invalid app returns null',
        passed: false,
        error: error.message
      });
    }
    
    // Test 3: Case insensitive
    try {
      const profile1 = this.getMarketProfile('connectsmart');
      const profile2 = this.getMarketProfile('CONNECTSMART');
      tests.push({
        test: 'Case insensitive lookup',
        passed: JSON.stringify(profile1) === JSON.stringify(profile2),
        result: 'Both cases return same profile'
      });
    } catch (error) {
      tests.push({
        test: 'Case insensitive lookup',
        passed: false,
        error: error.message
      });
    }
    
    // Test 4: Polygon integrity
    try {
      const validation = this.analytics.validatePolygonIntegrity('connectsmart');
      tests.push({
        test: 'Polygon integrity',
        passed: validation.valid,
        result: validation.valid ? 'Polygon is valid' : validation.error || validation.issues.join(', ')
      });
    } catch (error) {
      tests.push({
        test: 'Polygon integrity',
        passed: false,
        error: error.message
      });
    }
    
    return {
      totalTests: tests.length,
      passed: tests.filter(t => t.passed).length,
      failed: tests.filter(t => !t.passed).length,
      tests
    };
  }

  generateTestReport() {
    const basicTests = this.runBasicTests();
    let serviceAreaReport = null;
    
    try {
      serviceAreaReport = this.analytics.generateServiceAreaReport('connectsmart');
    } catch (error) {
      serviceAreaReport = { error: error.message };
    }
    
    return {
      timestamp: new Date().toISOString(),
      basicTests,
      serviceArea: serviceAreaReport
    };
  }
}
```

## 📊 Output Examples

### Basic Profile Response
```json
{
  "market": "HCS",
  "timezone": "America/Chicago",
  "polygon": "POLYGON ((-96.03311 29.72802,-96.03337 29.72859,...))"
}
```

### Service Area Statistics
```json
{
  "boundingBox": {
    "west": -96.19281,
    "south": 29.72802,
    "east": -95.35379,
    "north": 30.63019
  },
  "areaSquareMeters": 15420000000,
  "areaSquareKilometers": 15420,
  "coordinateCount": 2847
}
```

### Market Capabilities Response
```json
{
  "available": true,
  "market": "HCS",
  "timezone": "America/Chicago",
  "serviceArea": {
    "defined": true,
    "areaKm2": 15420,
    "boundingBox": {
      "west": -96.19281,
      "south": 29.72802,
      "east": -95.35379,
      "north": 30.63019
    }
  },
  "localTime": "2024-06-25 14:30:00 CDT",
  "businessHours": {
    "start": "09:00",
    "end": "17:00"
  }
}
```

### Service Area Report
```json
{
  "market": "HCS",
  "timezone": "America/Chicago",
  "polygon": {
    "format": "WKT",
    "coordinateCount": 2847,
    "area": {
      "squareMeters": 15420000000,
      "squareKilometers": 15420,
      "squareMiles": 5954.88
    },
    "boundingBox": {
      "west": -96.19281,
      "south": 29.72802,
      "east": -95.35379,
      "north": 30.63019,
      "width": 93.4,
      "height": 99.7
    }
  },
  "coverage": {
    "region": "Greater Houston Metropolitan Area",
    "majorCities": ["Houston", "Sugar Land", "The Woodlands", "Pearland"]
  }
}
```

## ⚠️ Important Notes

### Geographic Data Characteristics
- **High Precision:** Polygon contains 2,800+ coordinate points for detailed boundary definition
- **File Size:** Large file due to comprehensive polygon data (~1.1MB)
- **Coverage Area:** Approximately 15,420 square kilometers (5,955 square miles)
- **Coordinate System:** WGS84 decimal degrees (longitude, latitude)

### Performance Considerations
- **Memory Usage:** Large polygon data impacts memory usage
- **Parse Time:** WKT parsing can be CPU intensive for complex polygons
- **Caching Recommended:** Consider caching parsed geometry objects
- **Lazy Loading:** Load profile data only when needed

### Configuration Management
- **Single Market:** Currently configured only for ConnectSmart/HCS
- **Case Insensitive:** Application name lookup is case-insensitive
- **Error Handling:** Returns null for unknown applications with error logging
- **Immutable Data:** Configuration is static and requires code changes to modify

### WKT Polygon Format
- **Standard Format:** Follows OGC Well-Known Text specification
- **Coordinate Order:** Longitude first, then latitude (X, Y)
- **Closed Ring:** First and last coordinates are identical
- **Counter-Clockwise:** Exterior ring follows counter-clockwise order

### Market Expansion
- **Scalable Design:** Can support multiple markets by adding profile objects
- **Consistent Structure:** New markets should follow same schema pattern
- **Timezone Support:** Each market can have different timezone configuration
- **Polygon Flexibility:** Supports any valid WKT polygon geometry

### Integration Dependencies
- **Local User Label:** Used by location-based user categorization
- **Geospatial Services:** Required for point-in-polygon operations
- **Timezone Libraries:** moment-timezone or similar for time handling
- **WKT Parsers:** External libraries needed for polygon processing

### Business Logic Applications
- **Service Boundaries:** Determines where transportation services are available
- **Pricing Zones:** Can support location-based pricing strategies
- **Feature Availability:** Controls geographic feature rollouts
- **Analytics Segmentation:** Enables market-based data analysis

## 🔗 Related File Links

- **Local User Label:** `allrepo/connectsmart/tsp-api/src/services/localUserLabel.js`
- **Geospatial Utilities:** Services that use polygon data for validation
- **User Location:** Services that determine user market membership
- **Configuration:** Market-specific settings and business rules

---
*This service provides essential geographic market configuration for location-aware features and service boundary management in the TSP platform.*