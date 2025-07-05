# MarketProfile Service

## Quick Summary

The MarketProfile service is a critical configuration management system that provides geographic and operational parameters for different service markets within the ConnectSmart platform. This service centralizes market-specific settings including geographic boundaries, timezone configurations, and service area definitions, enabling the platform to operate across multiple cities and regions with tailored configurations.

**Key Features:**
- Geographic service area definition using polygon boundaries
- Timezone management for multi-region operations
- Market-specific configuration centralization
- Dynamic service profile resolution
- Comprehensive logging for configuration debugging
- Fail-safe fallback mechanisms for unknown markets

## Technical Analysis

### Architecture Overview

The service is implemented as a function-based module that exports a single resolver function. It maintains a static configuration object containing detailed market profiles and provides a lookup mechanism to retrieve market-specific configurations based on application identifiers.

### Core Data Structure

The service centers around a comprehensive profiles object containing market definitions:

```javascript
const profiles = {
  "connectsmart": {
    "market": "HCS",
    "timezone": "America/Chicago", 
    "polygon": "POLYGON ((-96.03311 29.72802,-96.03337 29.72859,...))"
  }
  // Additional market profiles would be defined here
};
```

### Configuration Architecture

#### 1. Market Identification System
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

#### 2. Geographic Boundary Definition
The service uses Well-Known Text (WKT) format to define precise geographic boundaries:
- **POLYGON format**: Industry-standard geographic representation
- **Coordinate precision**: High-precision latitude/longitude pairs
- **Service area coverage**: Complete metropolitan area boundary definition

#### 3. Market-Specific Parameters
Each market profile contains essential operational parameters:
- **Market Code**: Unique identifier for database operations and analytics
- **Timezone**: Local timezone for accurate scheduling and user experience
- **Geographic Polygon**: Precise service area boundaries for trip validation

### Data Validation and Error Handling

The service implements robust validation mechanisms:

```javascript
// Case-insensitive lookup with comprehensive error handling
const k = app.toLowerCase();
if (Object.keys(profiles).indexOf(k) === -1) {
  logger.error(`Service profile not found for app: ${app}`);
  return null;
}
```

### Geographic Data Format

The service stores geographic boundaries in WKT POLYGON format, which provides:
- **Standards Compliance**: Industry-standard geographic data representation
- **High Precision**: Accurate coordinate definitions for service boundaries
- **Integration Compatibility**: Direct compatibility with GIS systems and spatial databases
- **Performance Optimization**: Efficient storage and retrieval of complex geometric data

## Usage/Integration

### Primary Integration Points

#### 1. Service Area Validation
```javascript
const getServiceProfile = require('@app/src/services/marketProfile');

// Retrieve market configuration for service validation
const serviceProfile = getServiceProfile('connectsmart');
if (serviceProfile) {
  console.log(`Operating in market: ${serviceProfile.market}`);
  console.log(`Timezone: ${serviceProfile.timezone}`);
  // Use polygon for geographic validation
}
```

#### 2. Geographic Boundary Checking
```javascript
const { parse } = require('wkt');
const turf = require('@turf/turf');

// Parse and utilize geographic boundaries
const serviceProfile = getServiceProfile('connectsmart');
if (serviceProfile && serviceProfile.polygon) {
  const geoJson = parse(serviceProfile.polygon);
  const polygon = turf.polygon(geoJson.coordinates);
  
  // Validate if point is within service area
  const userLocation = turf.point([-95.3698, 29.7604]);
  const isInServiceArea = turf.booleanPointInPolygon(userLocation, polygon);
}
```

#### 3. Timezone-Aware Operations
```javascript
const moment = require('moment-timezone');

// Market-specific timezone operations
const serviceProfile = getServiceProfile('connectsmart');
if (serviceProfile) {
  const localTime = moment().tz(serviceProfile.timezone);
  console.log(`Local time in ${serviceProfile.market}: ${localTime.format()}`);
}
```

### Configuration Management Patterns

#### 1. Multi-Market Support
```javascript
// Support for multiple market configurations
const markets = ['connectsmart', 'gomyway', 'ridemetro'];
const marketConfigs = markets.map(market => ({
  market,
  profile: getServiceProfile(market)
})).filter(config => config.profile !== null);

console.log(`Configured markets: ${marketConfigs.length}`);
```

#### 2. Service Validation Pipeline
```javascript
// Comprehensive service validation using market profiles
async function validateServiceAvailability(appName, userLatitude, userLongitude) {
  const profile = getServiceProfile(appName);
  
  if (!profile) {
    return { available: false, reason: 'Market not configured' };
  }
  
  // Parse geographic boundary
  const geoJson = parse(profile.polygon);
  const serviceArea = turf.polygon(geoJson.coordinates);
  const userPoint = turf.point([userLongitude, userLatitude]);
  
  const inServiceArea = turf.booleanPointInPolygon(userPoint, serviceArea);
  
  return {
    available: inServiceArea,
    market: profile.market,
    timezone: profile.timezone,
    reason: inServiceArea ? 'Service available' : 'Outside service area'
  };
}
```

#### 3. Configuration Debugging
```javascript
// Comprehensive configuration debugging and validation
function debugMarketConfiguration(appName) {
  const profile = getServiceProfile(appName);
  
  if (!profile) {
    console.log(`❌ Market profile not found for: ${appName}`);
    console.log(`Available profiles: ${Object.keys(profiles).join(', ')}`);
    return;
  }
  
  console.log(`✅ Market Profile for ${appName}:`);
  console.log(`   Market Code: ${profile.market}`);
  console.log(`   Timezone: ${profile.timezone}`);
  console.log(`   Polygon Length: ${profile.polygon.length} characters`);
  
  // Validate polygon format
  try {
    const geoJson = parse(profile.polygon);
    console.log(`   Polygon Coordinates: ${geoJson.coordinates[0].length} points`);
  } catch (error) {
    console.log(`   ❌ Invalid polygon format: ${error.message}`);
  }
}
```

## Dependencies

### Core Framework Dependencies
- **@maas/core/log**: Centralized logging system for configuration debugging and error tracking

### Geospatial Processing Dependencies (Integration)
- **wkt (External)**: Well-Known Text parsing for geographic polygon processing
- **@turf/turf (External)**: Geospatial analysis and geometric operations
- **GIS Libraries (External)**: Integration with geographic information systems

### Runtime Dependencies
- **Node.js Core Modules**: Standard JavaScript runtime environment
- **JSON Processing**: Native JavaScript object manipulation
- **String Processing**: Case-insensitive lookups and validation

### Configuration Dependencies
- **Static Configuration**: Embedded market profile definitions
- **Application Identifiers**: Standardized app naming conventions
- **Geographic Data Standards**: WKT format compliance for polygon definitions

## Code Examples

### Complete Market Configuration System

```javascript
// Comprehensive market profile management system
class MarketProfileManager {
  constructor() {
    this.getServiceProfile = require('@app/src/services/marketProfile');
    this.profileCache = new Map();
  }
  
  // Enhanced profile retrieval with caching
  getProfile(appName) {
    const cacheKey = appName.toLowerCase();
    
    if (this.profileCache.has(cacheKey)) {
      return this.profileCache.get(cacheKey);
    }
    
    const profile = this.getServiceProfile(appName);
    if (profile) {
      this.profileCache.set(cacheKey, profile);
    }
    
    return profile;
  }
  
  // Validate service availability for coordinates
  async validateLocation(appName, latitude, longitude) {
    const profile = this.getProfile(appName);
    
    if (!profile) {
      return { valid: false, error: 'Market not configured' };
    }
    
    try {
      const { parse } = require('wkt');
      const turf = require('@turf/turf');
      
      const geoJson = parse(profile.polygon);
      const serviceArea = turf.polygon(geoJson.coordinates);
      const userPoint = turf.point([longitude, latitude]);
      
      const isValid = turf.booleanPointInPolygon(userPoint, serviceArea);
      
      return {
        valid: isValid,
        market: profile.market,
        timezone: profile.timezone,
        coordinates: { latitude, longitude }
      };
    } catch (error) {
      return { valid: false, error: `Geographic validation failed: ${error.message}` };
    }
  }
  
  // Get all configured markets
  getAvailableMarkets() {
    const allProfiles = {};
    const profileKeys = Object.keys(require('@app/src/services/marketProfile').profiles || {});
    
    profileKeys.forEach(key => {
      const profile = this.getProfile(key);
      if (profile) {
        allProfiles[key] = {
          market: profile.market,
          timezone: profile.timezone,
          hasPolygon: !!profile.polygon
        };
      }
    });
    
    return allProfiles;
  }
}
```

### Geographic Boundary Analysis Tool

```javascript
// Advanced geographic analysis using market profiles
class GeographicAnalyzer {
  constructor() {
    this.marketProfile = require('@app/src/services/marketProfile');
  }
  
  async analyzeServiceCoverage(appName, coordinates) {
    const profile = this.marketProfile(appName);
    
    if (!profile) {
      throw new Error(`Market profile not found: ${appName}`);
    }
    
    const { parse } = require('wkt');
    const turf = require('@turf/turf');
    
    // Parse service area
    const geoJson = parse(profile.polygon);
    const serviceArea = turf.polygon(geoJson.coordinates);
    
    // Calculate area coverage
    const areaSquareMeters = turf.area(serviceArea);
    const areaSquareMiles = areaSquareMeters * 0.000000386102;
    
    // Analyze coordinate coverage
    const results = coordinates.map(coord => {
      const point = turf.point([coord.longitude, coord.latitude]);
      const isInside = turf.booleanPointInPolygon(point, serviceArea);
      const distance = isInside ? 0 : turf.pointToLineDistance(point, turf.lineString(geoJson.coordinates[0]));
      
      return {
        latitude: coord.latitude,
        longitude: coord.longitude,
        inServiceArea: isInside,
        distanceToService: distance
      };
    });
    
    const coverage = {
      market: profile.market,
      timezone: profile.timezone,
      serviceAreaSqMiles: Math.round(areaSquareMiles * 100) / 100,
      totalPoints: coordinates.length,
      pointsInService: results.filter(r => r.inServiceArea).length,
      coveragePercentage: Math.round((results.filter(r => r.inServiceArea).length / coordinates.length) * 100),
      analysis: results
    };
    
    return coverage;
  }
  
  async findNearestServiceBoundary(appName, latitude, longitude) {
    const profile = this.marketProfile(appName);
    
    if (!profile) {
      return null;
    }
    
    const { parse } = require('wkt');
    const turf = require('@turf/turf');
    
    const geoJson = parse(profile.polygon);
    const serviceArea = turf.polygon(geoJson.coordinates);
    const userPoint = turf.point([longitude, latitude]);
    
    // Find nearest point on boundary
    const boundaryLine = turf.polygonToLine(serviceArea);
    const nearestPoint = turf.nearestPointOnLine(boundaryLine, userPoint);
    
    return {
      market: profile.market,
      userLocation: { latitude, longitude },
      nearestBoundaryPoint: {
        latitude: nearestPoint.geometry.coordinates[1],
        longitude: nearestPoint.geometry.coordinates[0]
      },
      distanceToService: turf.distance(userPoint, nearestPoint, { units: 'miles' })
    };
  }
}
```

### Multi-Market Configuration Validator

```javascript
// Comprehensive validation system for market configurations
async function validateAllMarketConfigurations() {
  const validator = {
    results: [],
    
    async validate() {
      const marketProfile = require('@app/src/services/marketProfile');
      
      // Test known configurations
      const testApps = ['connectsmart', 'invalid_app', ''];
      
      for (const app of testApps) {
        const result = await this.validateSingleMarket(app, marketProfile);
        this.results.push(result);
      }
      
      return this.generateReport();
    },
    
    async validateSingleMarket(appName, marketProfile) {
      const profile = marketProfile(appName);
      
      const validation = {
        appName,
        valid: !!profile,
        errors: [],
        warnings: []
      };
      
      if (!profile) {
        validation.errors.push('Profile not found');
        return validation;
      }
      
      // Validate required fields
      if (!profile.market) validation.errors.push('Missing market code');
      if (!profile.timezone) validation.errors.push('Missing timezone');
      if (!profile.polygon) validation.errors.push('Missing polygon definition');
      
      // Validate timezone format
      try {
        const moment = require('moment-timezone');
        if (!moment.tz.zone(profile.timezone)) {
          validation.errors.push(`Invalid timezone: ${profile.timezone}`);
        }
      } catch (error) {
        validation.errors.push(`Timezone validation error: ${error.message}`);
      }
      
      // Validate polygon format
      if (profile.polygon) {
        try {
          const { parse } = require('wkt');
          const geoJson = parse(profile.polygon);
          
          if (!geoJson.coordinates || !geoJson.coordinates[0]) {
            validation.errors.push('Invalid polygon coordinates');
          } else if (geoJson.coordinates[0].length < 4) {
            validation.warnings.push('Polygon has very few coordinate points');
          }
          
          validation.polygonPoints = geoJson.coordinates[0].length;
        } catch (error) {
          validation.errors.push(`Polygon parsing error: ${error.message}`);
        }
      }
      
      return validation;
    },
    
    generateReport() {
      const validConfigs = this.results.filter(r => r.valid && r.errors.length === 0);
      const invalidConfigs = this.results.filter(r => !r.valid || r.errors.length > 0);
      
      return {
        summary: {
          total: this.results.length,
          valid: validConfigs.length,
          invalid: invalidConfigs.length
        },
        validConfigurations: validConfigs,
        invalidConfigurations: invalidConfigs,
        recommendations: this.generateRecommendations(invalidConfigs)
      };
    },
    
    generateRecommendations(invalidConfigs) {
      const recommendations = [];
      
      invalidConfigs.forEach(config => {
        if (config.errors.includes('Profile not found')) {
          recommendations.push(`Add profile configuration for app: ${config.appName}`);
        }
        if (config.errors.some(e => e.includes('timezone'))) {
          recommendations.push(`Fix timezone configuration for app: ${config.appName}`);
        }
        if (config.errors.some(e => e.includes('polygon'))) {
          recommendations.push(`Validate polygon definition for app: ${config.appName}`);
        }
      });
      
      return [...new Set(recommendations)]; // Remove duplicates
    }
  };
  
  return await validator.validate();
}
```

This market profile service provides essential geographic and operational configuration management, enabling the ConnectSmart platform to operate effectively across multiple markets with precise service boundaries and timezone-aware operations.