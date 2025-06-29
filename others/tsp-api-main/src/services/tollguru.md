# TSP API TollGuru Service Documentation

## 🔍 Quick Summary (TL;DR)
The TollGuru service integrates with TollGuru API to calculate toll costs for route polylines, handles HERE to Google polyline conversion, filters specific road types, supports tag/no-tag pricing, and provides comprehensive monitoring with InfluxDB metrics and Slack alerts.

**Keywords:** toll-calculation | tollguru-api | polyline-conversion | road-filtering | tag-pricing | service-monitoring | route-costs | third-party-integration

**Primary use cases:** Calculating toll costs for driving routes, converting HERE polylines to Google format, filtering HOT lanes and express roads, providing tag vs non-tag pricing

**Compatibility:** Node.js >= 16.0.0, TollGuru API integration, HERE Maps polyline format, Google polyline encoding, InfluxDB monitoring, Slack notifications

## ❓ Common Questions Quick Index
- **Q: What polyline formats are supported?** → HERE Maps polylines converted to Google polyline format for TollGuru API
- **Q: How are toll costs calculated?** → Tag vs non-tag pricing with road filtering for HOT lanes and express roads
- **Q: What roads are filtered out?** → Roads containing "HOT", "Express", or "Katy Freeway Managed Lanes"
- **Q: What vehicle types are supported?** → Vehicle types with "AxlesAuto" suffix for TollGuru API compatibility
- **Q: How is monitoring handled?** → InfluxDB metrics collection and Slack alerts for API failures
- **Q: What error handling exists?** → Comprehensive error handling with custom error codes and fallback responses

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **toll calculator** that takes a driving route and figures out how much you'll pay in tolls. It converts route data into the format needed by TollGuru's service, calculates costs based on whether you have a toll tag, and filters out certain expensive express lanes to provide more reasonable estimates.

**Technical explanation:** 
A comprehensive toll calculation service that integrates with TollGuru API for polyline-based toll cost estimation, performs polyline format conversion between HERE and Google standards, implements business logic for road filtering and pricing options, and provides robust monitoring through InfluxDB metrics and Slack alerting.

**Business value explanation:**
Enables accurate toll cost estimation for route planning, supports cost-conscious travel decisions, provides transparent pricing for different payment methods (tag vs cash), helps users avoid expensive express lanes, and ensures reliable service through comprehensive monitoring and alerting.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/tollguru.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with axios HTTP client and polyline conversion utilities
- **Type:** Third-Party Toll Calculation Integration Service
- **File Size:** ~6.8 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High - Complex polyline conversion and API integration)

**Dependencies:**
- `axios`: HTTP client for TollGuru API calls (**Critical**)
- `@maas/services`: InfluxDB and Slack monitoring services (**High**)
- `@app/src/services/hereMapPolylines`: HERE polyline decoding (**Critical**)
- `google-polyline`: Google polyline encoding (**Critical**)
- `@app/src/schemas/toll-schemas`: Input validation schemas (**High**)

## 📝 Detailed Code Analysis

### Main Route Processing Function

### tollGuruRoute Function
**Purpose:** Processes multiple routes for toll calculation with parallel processing

```javascript
async function tollGuruRoute(bean) {
  const params = await checkInputParams(bean);
  const polylinePromises = [];
  
  params.routes.forEach((p) => {
    polylinePromises.push(
      getPolylineTollInfo(
        p.id,
        p.polyline,
        params.vehicleType,
        params.tagInstalled,
      ),
    );
  });

  const result = await Promise.all(polylinePromises);
  return result;
}
```

**Processing Features:**
- **Input Validation:** Validates parameters using Joi schemas
- **Parallel Processing:** Processes multiple routes simultaneously for performance
- **Parameter Passing:** Forwards vehicle type and tag installation status
- **Promise Coordination:** Uses Promise.all for efficient batch processing

### Polyline Conversion System

### hereToGooglePolyline Function
**Purpose:** Converts HERE Maps polylines to Google polyline format for TollGuru API

```javascript
function hereToGooglePolyline(polyline, id) {
  try {
    const polylineInfo = poly.decode(polyline);
    const gPolyline = GooglePolyline.encode(polylineInfo.polyline);
    return gPolyline;
  } catch (e) {
    throw new MaasError(
      ERROR_CODE.ERROR_TOLLS_ROUTE_INVALID_HERE_POLYLINE,
      'warn',
      'ERROR_TOLLS_ROUTE_INVALID_HERE_POLYLINE',
      200,
    );
  }
}
```

**Conversion Features:**
- **HERE Decoding:** Uses HERE polyline decoder to extract coordinate data
- **Google Encoding:** Converts coordinates to Google polyline format
- **Error Handling:** Throws specific error for invalid HERE polylines
- **Format Compatibility:** Ensures TollGuru API compatibility

### TollGuru API Integration

### tollGuruApiPostPolyline Function
**Purpose:** Makes API call to TollGuru for toll calculation with comprehensive monitoring

```javascript
async function tollGuruApiPostPolyline(polyline, vehicleType, originApi) {
  const vendorApi = tollguruConfig.url + '/toll/v2/complete-polyline-from-mapping-service';
  const inputBody = {
    serviceProvider: tollguruConfig.source,
    polyline,
    vehicle: {
      type: vehicleType + 'AxlesAuto',
    },
  };

  const metaData = {
    ...inputBody,
    key: tollguruConfig.apiKey,
  };
  
  // Service monitoring setup
  const start = new Date();
  const meta = JSON.stringify(metaData);
  const vendorService = 'Polyline';
  
  try {
    const response = await axiosApiInstance.post(vendorApi, inputBody);
    const results = response.data;
    
    // Log success metrics
    await influx.writeIntoServiceMonitor(
      formatTollguruMetrics(
        originApi,
        vendorApi,
        vendorService,
        'SUCCESS',
        new Date() - start,
        meta,
      ),
    );
    return results;
  } catch (e) {
    // Log error metrics
    await influx.writeIntoServiceMonitor(
      formatTollguruMetrics(
        originApi,
        vendorApi,
        vendorService,
        'ERROR',
        new Date() - start,
        meta,
      ),
    );
    
    // Send Slack alert
    const slack = new SlackManager(slackConfig.token, slackConfig.channelId);
    slack.sendVendorFailedMsg({
      project: projectConfig.projectName,
      stage: projectConfig.projectStage,
      status: 'ERROR',
      vendor: 'Tollguru',
      vendorApi,
      originApi,
      errorMsg: e,
      meta4Slack: e,
    });
    
    logger.error(`tollGuruApiPostPolyline failed polyline: ${polyline}`);
    throw new MaasError(
      ERROR_CODE.ERROR_THIRD_PARTY_FAILED,
      'warn',
      'ERROR_THIRD_PARTY_FAILED',
      200,
    );
  }
}
```

**API Integration Features:**
- **Configuration-Driven:** Uses config for API endpoints and keys
- **Vehicle Type Formatting:** Appends "AxlesAuto" suffix for API compatibility
- **Performance Monitoring:** Tracks response times and success/failure rates
- **Error Alerting:** Immediate Slack notifications for API failures
- **Comprehensive Logging:** InfluxDB metrics for operational monitoring

### Toll Cost Calculation and Filtering

### produceResult Function
**Purpose:** Calculates total toll costs with road filtering and tag/no-tag pricing

```javascript
async function produceResult(index, tollRespond, tagInstalled) {
  const tollInfo = await checkAPIResponse(tollRespond.route);
  let totalCost = 0;

  tollInfo.tolls.forEach((ele) => {
    const road = ele?.start?.road || ele?.road || '';
    const tagCost = ele.tagCost ?? 0;
    const noTagCost = ele.licensePlateCost
      ? ele.licensePlateCost
      : ele.cashCost
      ? ele.cashCost
      : 0;
      
    // Filter out expensive express lanes and HOT lanes
    if (!/HOT|Express|Katy Freeway Managed Lanes/.test(road)) {
      if (tagInstalled) {
        totalCost = totalCost + tagCost;
      } else {
        totalCost = totalCost + noTagCost;
      }
    } else {
      logger.info(
        `filter out [${road}] cost: ${tagInstalled ? tagCost : noTagCost}`,
      );
    }
  });

  const result = {
    id: index,
    totalCost: tollInfo.hasTolls ? parseFloat(totalCost) : 0,
  };
  return result;
}
```

**Cost Calculation Features:**
- **Road Filtering:** Excludes HOT lanes, Express lanes, and Katy Freeway Managed Lanes
- **Tag vs No-Tag Pricing:** Different pricing based on toll tag availability
- **Fallback Logic:** Uses licensePlateCost or cashCost if available
- **Zero Cost Handling:** Returns 0 if no tolls exist on route
- **Logging:** Records filtered roads for transparency

### Input Validation and Error Handling

#### Parameter Validation
```javascript
async function checkInputParams(params) {
  const value = await inputValidator.routesParams.validateAsync(params);
  return value;
}

async function checkAPIResponse(schema) {
  try {
    const value = await inputValidator.tollGuruApiPostPolyline.validateAsync(schema);
    return value;
  } catch (e) {
    logger.warn(`tollGuru response verify failed: ${e.message}`);
    throw new MaasError(
      ERROR_CODE.ERROR_TOLLGURU_RESPONSE_SCHEMA,
      'warn',
      'ERROR_TOLLGURU_RESPONSE_SCHEMA',
      200,
    );
  }
}
```

**Validation Features:**
- **Joi Schema Validation:** Comprehensive input parameter validation
- **Response Validation:** Ensures TollGuru API response matches expected schema
- **Error Propagation:** Specific error codes for different validation failures
- **Logging:** Warning logs for schema validation failures

### Monitoring and Metrics

#### Metrics Formatting
```javascript
const formatTollguruMetrics = (
  originApi,
  vendorApi,
  vendorService,
  status,
  duration,
  meta,
  errorMsg = null,
) => {
  return {
    vendor: 'Tollguru',
    originApi,
    vendorService,
    vendorApi,
    status,
    duration,
    meta,
    errorMsg,
  };
};
```

**Monitoring Features:**
- **Standardized Metrics:** Consistent format for InfluxDB storage
- **Performance Tracking:** Duration measurement for response time analysis
- **Error Context:** Comprehensive error information for debugging
- **Vendor Attribution:** Clear vendor identification for multi-vendor monitoring

## 🚀 Usage Methods

### Basic Toll Calculation
```javascript
const tollguruService = require('@app/src/services/tollguru');

// Calculate tolls for multiple routes
const tollRequest = {
  vehicleType: '2',
  tagInstalled: true,
  routes: [
    {
      id: 0,
      polyline: 'BFoz5xJ67P1B1B7P7P-F-F6QoM4R8t@-A2DgF7C0B'
    },
    {
      id: 1,
      polyline: 'BGoz5xJ67P1B1B7P7P-F-F6QoM4R8t@-A2DgF7C0C'
    }
  ]
};

const tollResults = await tollguruService.tollGuruRoute(tollRequest);
console.log('Toll results:', tollResults);
// Output: [{ id: 0, totalCost: 2.50 }, { id: 1, totalCost: 1.75 }]
```

### Advanced Toll Management System
```javascript
class TollCalculationManager {
  constructor() {
    this.tollguruService = require('@app/src/services/tollguru');
    this.calculationCache = new Map();
    this.cacheTimeout = 3600000; // 1 hour
    this.retryAttempts = 3;
    this.retryDelay = 2000;
  }

  async calculateTollsWithCache(routes, vehicleType, tagInstalled, options = {}) {
    try {
      const { forceRefresh = false, includeDetails = false } = options;
      
      // Generate cache key
      const cacheKey = this.generateCacheKey(routes, vehicleType, tagInstalled);
      
      // Check cache first
      if (!forceRefresh && this.calculationCache.has(cacheKey)) {
        const cached = this.calculationCache.get(cacheKey);
        if (Date.now() - cached.timestamp < this.cacheTimeout) {
          console.log('Using cached toll calculation');
          return {
            ...cached.data,
            fromCache: true
          };
        }
      }

      // Calculate tolls with retry logic
      const tollData = await this.calculateWithRetry({
        routes,
        vehicleType,
        tagInstalled
      });

      // Process results
      const processedResults = await this.processTollResults(tollData, includeDetails);

      // Cache the results
      this.calculationCache.set(cacheKey, {
        data: processedResults,
        timestamp: Date.now()
      });

      return {
        ...processedResults,
        fromCache: false
      };
    } catch (error) {
      console.error('Toll calculation failed:', error);
      
      // Return cached data if available
      const cacheKey = this.generateCacheKey(routes, vehicleType, tagInstalled);
      if (this.calculationCache.has(cacheKey)) {
        const cached = this.calculationCache.get(cacheKey);
        return {
          ...cached.data,
          fromCache: true,
          error: 'Using cached data due to calculation error'
        };
      }
      
      throw error;
    }
  }

  async calculateWithRetry(tollRequest) {
    let lastError;
    
    for (let attempt = 1; attempt <= this.retryAttempts; attempt++) {
      try {
        console.log(`Toll calculation attempt ${attempt}/${this.retryAttempts}`);
        return await this.tollguruService.tollGuruRoute(tollRequest);
      } catch (error) {
        lastError = error;
        
        if (attempt < this.retryAttempts) {
          console.log(`Attempt ${attempt} failed, retrying in ${this.retryDelay}ms...`);
          await this.delay(this.retryDelay);
          this.retryDelay *= 1.5; // Exponential backoff
        }
      }
    }
    
    throw lastError;
  }

  async processTollResults(tollResults, includeDetails = false) {
    try {
      const totalCost = tollResults.reduce((sum, route) => sum + route.totalCost, 0);
      const routeCount = tollResults.length;
      const tollRoutes = tollResults.filter(route => route.totalCost > 0).length;
      
      const processed = {
        routes: tollResults,
        summary: {
          totalCost: Math.round(totalCost * 100) / 100,
          routeCount,
          tollRoutes,
          freRoutes: routeCount - tollRoutes,
          averageCost: routeCount > 0 ? Math.round((totalCost / routeCount) * 100) / 100 : 0
        }
      };

      if (includeDetails) {
        processed.details = {
          costDistribution: this.analyzeCostDistribution(tollResults),
          recommendations: this.generateRecommendations(tollResults)
        };
      }

      return processed;
    } catch (error) {
      console.error('Error processing toll results:', error);
      return {
        routes: tollResults,
        summary: { totalCost: 0, routeCount: 0, tollRoutes: 0, freRoutes: 0, averageCost: 0 },
        error: error.message
      };
    }
  }

  analyzeCostDistribution(tollResults) {
    const costs = tollResults.map(r => r.totalCost).filter(cost => cost > 0);
    
    if (costs.length === 0) {
      return { min: 0, max: 0, median: 0, standardDeviation: 0 };
    }
    
    costs.sort((a, b) => a - b);
    const min = costs[0];
    const max = costs[costs.length - 1];
    const median = costs.length % 2 === 0 
      ? (costs[costs.length / 2 - 1] + costs[costs.length / 2]) / 2
      : costs[Math.floor(costs.length / 2)];
    
    // Calculate standard deviation
    const mean = costs.reduce((sum, cost) => sum + cost, 0) / costs.length;
    const variance = costs.reduce((sum, cost) => sum + Math.pow(cost - mean, 2), 0) / costs.length;
    const standardDeviation = Math.sqrt(variance);
    
    return {
      min: Math.round(min * 100) / 100,
      max: Math.round(max * 100) / 100,
      median: Math.round(median * 100) / 100,
      standardDeviation: Math.round(standardDeviation * 100) / 100
    };
  }

  generateRecommendations(tollResults) {
    const recommendations = [];
    
    // Find cheapest route
    const cheapestRoute = tollResults.reduce((min, route) => 
      route.totalCost < min.totalCost ? route : min
    );
    
    if (cheapestRoute.totalCost === 0) {
      recommendations.push({
        type: 'free_route',
        message: `Route ${cheapestRoute.id} has no tolls`,
        savings: 0
      });
    } else {
      const mostExpensive = tollResults.reduce((max, route) => 
        route.totalCost > max.totalCost ? route : max
      );
      
      const savings = mostExpensive.totalCost - cheapestRoute.totalCost;
      if (savings > 0) {
        recommendations.push({
          type: 'cost_saving',
          message: `Choose route ${cheapestRoute.id} to save $${savings.toFixed(2)}`,
          savings: Math.round(savings * 100) / 100
        });
      }
    }
    
    // Check for high-cost routes
    const averageCost = tollResults.reduce((sum, route) => sum + route.totalCost, 0) / tollResults.length;
    const highCostRoutes = tollResults.filter(route => route.totalCost > averageCost * 1.5);
    
    if (highCostRoutes.length > 0) {
      recommendations.push({
        type: 'high_cost_warning',
        message: `Routes ${highCostRoutes.map(r => r.id).join(', ')} have above-average toll costs`,
        routes: highCostRoutes.map(r => r.id)
      });
    }
    
    return recommendations;
  }

  generateCacheKey(routes, vehicleType, tagInstalled) {
    const routeHashes = routes.map(r => `${r.id}_${r.polyline.substring(0, 10)}`).join('|');
    return `${routeHashes}_${vehicleType}_${tagInstalled}`;
  }

  async comparePricingOptions(routes, vehicleType) {
    try {
      // Calculate costs for both tag and no-tag scenarios
      const [tagResults, noTagResults] = await Promise.all([
        this.calculateTollsWithCache(routes, vehicleType, true),
        this.calculateTollsWithCache(routes, vehicleType, false)
      ]);

      const comparison = routes.map((route, index) => {
        const tagCost = tagResults.routes[index]?.totalCost || 0;
        const noTagCost = noTagResults.routes[index]?.totalCost || 0;
        const savings = noTagCost - tagCost;
        
        return {
          routeId: route.id,
          tagCost: Math.round(tagCost * 100) / 100,
          noTagCost: Math.round(noTagCost * 100) / 100,
          savings: Math.round(savings * 100) / 100,
          percentSavings: noTagCost > 0 ? Math.round((savings / noTagCost) * 100) : 0
        };
      });

      const totalTagCost = tagResults.summary.totalCost;
      const totalNoTagCost = noTagResults.summary.totalCost;
      const totalSavings = totalNoTagCost - totalTagCost;

      return {
        routes: comparison,
        summary: {
          totalTagCost,
          totalNoTagCost,
          totalSavings: Math.round(totalSavings * 100) / 100,
          percentSavings: totalNoTagCost > 0 ? Math.round((totalSavings / totalNoTagCost) * 100) : 0,
          recommendation: totalSavings > 0 ? 'Get a toll tag to save money' : 'Tag savings minimal'
        }
      };
    } catch (error) {
      console.error('Error comparing pricing options:', error);
      return {
        routes: [],
        summary: { totalTagCost: 0, totalNoTagCost: 0, totalSavings: 0, percentSavings: 0 },
        error: error.message
      };
    }
  }

  async delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  clearCache() {
    this.calculationCache.clear();
    return { message: 'Toll calculation cache cleared' };
  }

  getCacheStatistics() {
    return {
      cacheSize: this.calculationCache.size,
      cacheTimeout: this.cacheTimeout / 1000, // in seconds
      retryAttempts: this.retryAttempts
    };
  }
}

// Usage
const tollManager = new TollCalculationManager();

// Calculate tolls with caching and retry logic
const routes = [
  { id: 0, polyline: 'BFoz5xJ67P1B1B7P7P-F-F6QoM4R8t@-A2DgF7C0B' },
  { id: 1, polyline: 'BGoz5xJ67P1B1B7P7P-F-F6QoM4R8t@-A2DgF7C0C' }
];

const tollResults = await tollManager.calculateTollsWithCache(routes, '2', true, { includeDetails: true });
console.log('Toll calculation results:', tollResults);

// Compare pricing options
const pricingComparison = await tollManager.comparePricingOptions(routes, '2');
console.log('Pricing comparison:', pricingComparison);
```

### Polyline Conversion Utility
```javascript
class PolylineConverter {
  constructor() {
    this.tollguruService = require('@app/src/services/tollguru');
    this.conversionCache = new Map();
  }

  convertHereToGoogle(herePolyline, cacheResult = true) {
    try {
      // Check cache first
      if (cacheResult && this.conversionCache.has(herePolyline)) {
        return this.conversionCache.get(herePolyline);
      }

      const googlePolyline = this.tollguruService.hereToGooglePolyline(herePolyline, 0);
      
      // Cache the result
      if (cacheResult) {
        this.conversionCache.set(herePolyline, googlePolyline);
      }
      
      return googlePolyline;
    } catch (error) {
      console.error('Polyline conversion failed:', error);
      throw new Error(`Failed to convert HERE polyline: ${error.message}`);
    }
  }

  batchConvertPolylines(herePolylines) {
    const results = [];
    const errors = [];
    
    herePolylines.forEach((polyline, index) => {
      try {
        const googlePolyline = this.convertHereToGoogle(polyline);
        results.push({
          index,
          herePolyline: polyline,
          googlePolyline,
          success: true
        });
      } catch (error) {
        results.push({
          index,
          herePolyline: polyline,
          googlePolyline: null,
          success: false,
          error: error.message
        });
        errors.push({ index, error: error.message });
      }
    });
    
    return {
      results,
      errors,
      successCount: results.filter(r => r.success).length,
      errorCount: errors.length
    };
  }

  validatePolylineFormat(polyline, format = 'here') {
    try {
      if (format === 'here') {
        // Try to decode HERE polyline
        this.tollguruService.hereToGooglePolyline(polyline, 0);
        return { valid: true, format: 'here' };
      } else if (format === 'google') {
        // Basic Google polyline validation
        const GooglePolyline = require('google-polyline');
        GooglePolyline.decode(polyline);
        return { valid: true, format: 'google' };
      }
      
      return { valid: false, error: 'Unknown polyline format' };
    } catch (error) {
      return { valid: false, error: error.message };
    }
  }

  clearCache() {
    this.conversionCache.clear();
    return { message: 'Polyline conversion cache cleared' };
  }
}

// Usage
const polylineConverter = new PolylineConverter();

const herePolyline = 'BFoz5xJ67P1B1B7P7P-F-F6QoM4R8t@-A2DgF7C0B';
const googlePolyline = polylineConverter.convertHereToGoogle(herePolyline);
console.log('Converted polyline:', googlePolyline);

// Validate polyline format
const validation = polylineConverter.validatePolylineFormat(herePolyline, 'here');
console.log('Polyline validation:', validation);
```

## 📊 Output Examples

### Toll Calculation Results
```javascript
[
  { id: 0, totalCost: 2.50 },
  { id: 1, totalCost: 0 },
  { id: 2, totalCost: 1.75 }
]
```

### Comprehensive Toll Analysis
```javascript
{
  routes: [
    { id: 0, totalCost: 2.50 },
    { id: 1, totalCost: 0 },
    { id: 2, totalCost: 1.75 }
  ],
  summary: {
    totalCost: 4.25,
    routeCount: 3,
    tollRoutes: 2,
    freRoutes: 1,
    averageCost: 1.42
  },
  details: {
    costDistribution: {
      min: 1.75,
      max: 2.50,
      median: 2.13,
      standardDeviation: 0.38
    },
    recommendations: [
      {
        type: "free_route",
        message: "Route 1 has no tolls",
        savings: 0
      }
    ]
  },
  fromCache: false
}
```

### Pricing Comparison Results
```javascript
{
  routes: [
    {
      routeId: 0,
      tagCost: 2.50,
      noTagCost: 3.00,
      savings: 0.50,
      percentSavings: 17
    }
  ],
  summary: {
    totalTagCost: 2.50,
    totalNoTagCost: 3.00,
    totalSavings: 0.50,
    percentSavings: 17,
    recommendation: "Get a toll tag to save money"
  }
}
```

### Polyline Conversion Results
```javascript
{
  results: [
    {
      index: 0,
      herePolyline: "BFoz5xJ67P1B1B7P7P-F-F6QoM4R8t@-A2DgF7C0B",
      googlePolyline: "u{~vFvyys@fS]",
      success: true
    }
  ],
  errors: [],
  successCount: 1,
  errorCount: 0
}
```

## ⚠️ Important Notes

### TollGuru API Integration
- **API Key Management:** Secure handling of TollGuru API keys through configuration
- **Rate Limiting:** Consider implementing rate limiting for API calls
- **Response Validation:** Comprehensive schema validation for API responses
- **Error Handling:** Robust error handling with retry logic and fallback strategies

### Polyline Format Conversion
- **HERE to Google:** Accurate conversion between different polyline encoding standards
- **Error Handling:** Specific error codes for polyline conversion failures
- **Performance:** Consider caching converted polylines for repeated requests
- **Validation:** Input validation for both HERE and Google polyline formats

### Road Filtering and Business Logic
- **Express Lane Filtering:** Excludes HOT lanes, Express lanes, and specific managed lanes
- **Tag vs No-Tag Pricing:** Different pricing calculations based on toll tag availability
- **Cost Aggregation:** Proper summation of individual toll segments
- **Logging:** Comprehensive logging for filtered roads and pricing decisions

### Monitoring and Observability
- **InfluxDB Metrics:** Performance monitoring and success/failure tracking
- **Slack Alerts:** Immediate notifications for API failures
- **Response Time Tracking:** Duration measurement for performance analysis
- **Error Classification:** Detailed error categorization for operational insights

## 🔗 Related File Links

- **HERE Polylines:** `allrepo/connectsmart/tsp-api/src/services/hereMapPolylines.js`
- **Toll Schemas:** `allrepo/connectsmart/tsp-api/src/schemas/toll-schemas.js`
- **Route Services:** Services that use toll calculation for route planning
- **Payment Services:** Services that integrate toll costs into payment calculations

---
*This service provides comprehensive toll calculation with TollGuru API integration, polyline conversion, and business logic for road filtering in the TSP platform.*