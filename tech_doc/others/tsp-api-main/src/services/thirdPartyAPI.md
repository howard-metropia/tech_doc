# TSP API ThirdPartyAPI Service Documentation

## 🔍 Quick Summary (TL;DR)
The ThirdPartyAPI service manages parallel batch processing of HERE Maps API calls for route data enrichment, including walking instructions, polylines encoding/decoding, distance/duration calculations, and data corrections with comprehensive error handling and performance monitoring.

**Keywords:** here-maps-api | batch-processing | parallel-requests | polyline-encoding | route-enrichment | walking-instructions | error-handling | performance-monitoring

**Primary use cases:** Enriching route data with HERE Maps APIs, processing multiple route segments simultaneously, encoding/decoding polylines, calculating route distances and durations

**Compatibility:** Node.js >= 16.0.0, axios for HTTP requests, HERE Maps API integration, polyline encoding/decoding utilities, moment.js for time calculations

## ❓ Common Questions Quick Index
- **Q: What HERE APIs are supported?** → Router v8, Transit Router v8, Legacy Routing v7.2 for different route types
- **Q: How are requests processed?** → Parallel batch processing with promise-based coordination
- **Q: What data is enriched?** → Walking instructions, polylines, distances, durations, and corrections
- **Q: How are errors handled?** → Individual request failures don't stop batch, failed requests tracked separately
- **Q: What's the polyline processing?** → Decoding/encoding with precision 7 for route visualization
- **Q: How is performance monitored?** → InfluxDB integration (commented) for API call tracking

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **route data enhancer** that takes basic route information and makes multiple parallel calls to HERE Maps to fill in missing details like turn-by-turn directions, visual map lines, accurate distances, and timing corrections. It's like having multiple assistants working simultaneously to complete different parts of a route plan.

**Technical explanation:** 
A sophisticated batch processing service for HERE Maps API integration that handles parallel HTTP requests, polyline encoding/decoding with coordinate transformations, route data enrichment with multiple data types, and comprehensive error handling with performance monitoring capabilities.

**Business value explanation:**
Enables rich route visualization with detailed mapping data, improves user experience through accurate route information, supports multi-modal route planning with transit integration, provides scalable API processing for high-volume route requests, and maintains service reliability through robust error handling.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/thirdPartyAPI.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with axios HTTP client and moment.js
- **Type:** Third-Party API Integration and Batch Processing Service
- **File Size:** ~22.4 KB
- **Complexity Score:** ⭐⭐⭐⭐⭐ (Very High - Complex parallel processing and data transformation)

**Dependencies:**
- `axios`: HTTP client for API requests (**Critical**)
- `@app/src/services/hereMapPolylines`: Polyline encoding/decoding (**Critical**)
- `moment`: Date/time calculations and formatting (**High**)
- HERE Maps API access and authentication (**Critical**)

## 📝 Detailed Code Analysis

### Parallel Request Processing Architecture

### Base Request Pattern
```javascript
class thirdPartyAPI {
  async [MethodName]API(ApiURLAry) {
    return new Promise((resolve, reject) => {
      const TempAry = [];
      const ApiURLAryTemp = [];
      const LoseAPITemp = [];
      let j = 0;
      const k = ApiURLAry.length;
      const APIstartTime = Date.now();
      
      for (let i = 0; i < k; i++) {
        ApiURLAryTemp[i] = ApiURLAry[i].split('##');
        const start = new Date();
        
        axios.get(ApiURLAryTemp[i][2])
          .then(async (response) => {
            // Process successful response
            j++;
            // ... specific processing logic
            if (j == k) {
              resolve({ TempAry, LoseAPITemp });
            }
          })
          .catch(async (err) => {
            // Handle individual failures
            j++;
            LoseAPITemp.push(ApiURLAry[i]);
            if (j == k) {
              resolve({ TempAry, LoseAPITemp });
            }
          });
      }
    });
  }
}
```

**Architecture Features:**
- **Parallel Processing:** All requests fired simultaneously for maximum throughput
- **Progress Tracking:** Counter-based completion detection
- **Error Isolation:** Individual failures don't affect batch processing
- **Performance Monitoring:** Start time tracking for batch duration measurement

### Walking Instructions Processing

### HereWalkingAPI Function
**Purpose:** Extracts and processes turn-by-turn walking instructions from HERE routing responses

```javascript
async HereWalkingAPI(ApiURLAry) {
  // ... parallel processing setup
  
  .then(async (response) => {
    let m = 0;
    let WalkDeparture = '';
    let WalkArrival = '';
    j++;
    
    // Extract maneuver instructions
    for (const attributename3 in response.data.response.route[0].leg[0].maneuver) {
      if (m < response.data.response.route[0].leg[0].maneuver.length - 1) {
        // Concatenate departure instructions
        WalkDeparture += response.data.response.route[0].leg[0].maneuver[m].instruction;
      } else if (m == response.data.response.route[0].leg[0].maneuver.length - 1) {
        // Final arrival instruction
        WalkArrival = response.data.response.route[0].leg[0].maneuver[m].instruction;
      }
      m++;
    }
    
    // Clean HTML tags from instructions
    let str = WalkDeparture.toString();
    let str2 = WalkArrival.toString();
    str = str.replace(/(<([^>]+)>)/gi, '');
    str2 = str2.replace(/(<([^>]+)>)/gi, '');
    
    // Format result
    TempAry[i] = `${ApiURLAryTemp[i][0]}##${ApiURLAryTemp[i][1]}##${str}##${str2}`;
  })
}
```

**Processing Features:**
- **Instruction Extraction:** Separates departure and arrival instructions
- **HTML Cleaning:** Removes HTML tags from instruction text
- **Concatenation Logic:** Combines multiple departure steps into single instruction
- **Result Formatting:** Structured output with route and section indices

### Polyline Processing System

### HerePolylinesAPI Function
**Purpose:** Processes and encodes route polylines for map visualization

```javascript
async HerePolylinesAPI(ApiURLAry) {
  // ... setup and axios request
  
  .then(async (response) => {
    if (ApiURLAryTemp[i][2].indexOf('https://transit.router.hereapi.com/v8/routes') >= 0) {
      // Transit API Processing
      let m = 0;
      const TempPolyline = [];
      const TempPolyline2 = [];
      let FinalPolylinesAry = [];
      let FinalPolylines;
      
      try {
        // Extract polylines from transit and pedestrian sections
        for (const attributename in response.data.routes[0].sections) {
          console.log(response.data.routes[0].sections[attributename].type);
          if (response.data.routes[0].sections[attributename].type === 'transit' ||
              response.data.routes[0].sections[attributename].type === 'pedestrian') {
            TempPolyline[m] = response.data.routes[0].sections[attributename].polyline;
            m++;
          }
        }
        
        // Multi-section polyline combination
        if (TempPolyline.length >= 2) {
          let n = 0;
          TempPolyline.forEach((element) => {
            const TempDecode = poly.decode(element);
            TempPolyline2[n] = TempDecode.polyline;
            n++;
          });
          
          // Concatenate all decoded polylines
          TempPolyline2.forEach((element) => {
            FinalPolylinesAry = FinalPolylinesAry.concat(element);
          });
          
          // Re-encode combined polyline
          const encodedInput = {
            precision: 7,
            thirdDim: 0,
            thirdDimPrecision: 0,
            polyline: FinalPolylinesAry,
          };
          FinalPolylines = poly.encode(encodedInput);
        }
        
        // Handle single or empty polylines
        if (TempPolyline.length === 1) {
          FinalPolylines = TempPolyline[0] === undefined ? '' : TempPolyline;
        }
        if (TempPolyline.length === 0) {
          FinalPolylines = '';
        }
      } catch (e) {
        console.log(e);
        FinalPolylines = '';
      }
      
      TempAry[i] = `${ApiURLAryTemp[i][0]}##${ApiURLAryTemp[i][1]}##${FinalPolylines}`;
    }
  })
}
```

**Polyline Features:**
- **Section Filtering:** Processes only transit and pedestrian sections
- **Decode/Encode Pipeline:** Converts encoded polylines to coordinates and back
- **Multi-Section Combination:** Merges multiple route segments into single polyline
- **Precision Handling:** Uses precision 7 for coordinate accuracy
- **Error Recovery:** Graceful handling of malformed polyline data

### Distance and Duration Calculation

### HereLengthAPI Function
**Purpose:** Calculates total route distance and duration across all sections

```javascript
async HereLengthAPI(ApiURLAry) {
  // ... setup and request
  
  .then(async (response) => {
    try {
      let TempLength = 0; 
      let TempDuration = 0;
      const sectionsLength = response.data.routes[0].sections.length;
      const tmpSections = response.data.routes[0].sections;
      
      if (sectionsLength === 1) {
        // Single section route
        TempLength = tmpSections[0].summary.length;
        TempDuration = tmpSections[0].summary.duration;  
      } else if (sectionsLength >= 2) {
        // Multi-section route - sum all sections
        for (let x = 0; x < sectionsLength; x++) {
          TempLength += tmpSections[x].summary.length;
          TempDuration += tmpSections[x].summary.duration;
        }
      }
      
      TempAry[i] = `${ApiURLAryTemp[i][0]}##${ApiURLAryTemp[i][1]}##${TempLength}##${TempDuration}`;
    } catch (err) {
      console.log(err);
    }
  })
}
```

**Calculation Features:**
- **Section Aggregation:** Sums length and duration across all route sections
- **Single/Multi Handling:** Different logic for single vs multi-section routes
- **Error Handling:** Try-catch for malformed response data
- **Precise Summation:** Maintains accuracy across multiple sections

### Route Corrections System

### CorrectionsAPI Function
**Purpose:** Corrects route data using HERE or Google APIs with best-match selection

```javascript
async CorrectionsAPI(ApiURLAry) {
  // ... setup and request
  
  .then(async (response) => {
    if (ApiURLAryTemp[i][3] === 'here') {
      // HERE API correction
      const TempLength = response.data.routes[0].sections[0].summary.length;
      const TempDuration = response.data.routes[0].sections[0].summary.duration;
      TempAry[i] = `${ApiURLAryTemp[i][0]}##${ApiURLAryTemp[i][1]}##${TempLength}##${TempDuration}`;
      
    } else if (ApiURLAryTemp[i][3] === 'google') {
      // Google API correction with best-match selection
      const TempTwoLength = [];
      
      for (const attributename in response.data.routes) {
        // Calculate distance differences for route matching
        TempTwoLength.push(
          Math.abs(
            parseInt(ApiURLAryTemp[i][4]) -
            response.data.routes[attributename].legs[0].distance.value,
          ),
        );
      }
      
      // Find route with minimum distance difference
      let value = TempTwoLength[0];
      let index = 0;
      for (let im = 0; im < TempTwoLength.length; im++) {
        if (TempTwoLength[im] < value) {
          value = TempTwoLength[im];
          index = im;
        }
      }
      
      // Use best-match route data
      const TempLength = response.data.routes[index].legs[0].distance.value;
      const TempDuration = response.data.routes[index].legs[0].duration.value;
      TempAry[i] = `${ApiURLAryTemp[i][0]}##${ApiURLAryTemp[i][1]}##${TempLength}##${TempDuration}`;
    }
  })
}
```

**Correction Features:**
- **Multi-Provider Support:** Handles both HERE and Google API responses
- **Best-Match Algorithm:** Selects most accurate route from multiple options
- **Distance Comparison:** Uses original distance for route matching
- **Provider-Specific Logic:** Different processing for each API provider

### Data Integration System

### InsertData Function
**Purpose:** Integrates API results back into route data structure with time adjustments

```javascript
async InsertData(data, ary, type) {
  if (type === 'length') {
    for (let i = 0; i < ary.length; i++) {
      if (ary[i] !== undefined) {
        const AryTemp = [];
        AryTemp[i] = ary[i].split('##');
        
        // Update length data
        data.routes[AryTemp[i][0]].sections[AryTemp[i][1]].travelSummary.length = AryTemp[i][2];
        
        // First section timing adjustment
        if (AryTemp[i][1] == '0') {
          let tmpSeconds = data.routes[AryTemp[i][0]].sections[AryTemp[i][1]].travelSummary.duration - parseFloat(AryTemp[i][3]);
          data.routes[AryTemp[i][0]].sections[AryTemp[i][1]].travelSummary.duration = parseFloat(AryTemp[i][3]);
          
          // Adjust departure time based on duration change
          if (tmpSeconds < 0) {
            data.routes[AryTemp[i][0]].sections[AryTemp[i][1]].departure.time = 
              moment(data.routes[AryTemp[i][0]].sections[AryTemp[i][1]].departure.time).add(tmpSeconds, 'seconds').format('YYYY-MM-DDTHH:mm:ss');
          } else {
            data.routes[AryTemp[i][0]].sections[AryTemp[i][1]].departure.time = 
              moment(data.routes[AryTemp[i][0]].sections[AryTemp[i][1]].arrival.time).add(-tmpSeconds, 'seconds').format('YYYY-MM-DDTHH:mm:ss');
          }
        }
        
        // Last section timing adjustment
        if (parseFloat(AryTemp[i][1]) == (data.routes[AryTemp[i][0]].sections.length-1)) {
          let tmpSeconds2 = parseFloat(AryTemp[i][3]) - data.routes[AryTemp[i][0]].sections[AryTemp[i][1]].travelSummary.duration;
          data.routes[AryTemp[i][0]].sections[AryTemp[i][1]].travelSummary.duration = parseFloat(AryTemp[i][3]);
          
          // Adjust arrival time
          data.routes[AryTemp[i][0]].sections[AryTemp[i][1]].arrival.time = 
            moment(data.routes[AryTemp[i][0]].sections[AryTemp[i][1]].arrival.time).add(tmpSeconds2, 'seconds').format('YYYY-MM-DDTHH:mm:ss');
        }
      }
    }
    
    // Recalculate total route metrics
    for (const attributename in data.routes) {
      let tempTotalmeters = 0;
      let tempTotaltime = 0;
      
      for (const attributename2 in data.routes[attributename].sections) {
        tempTotalmeters += parseFloat(data.routes[attributename].sections[attributename2].travelSummary.length);
        tempTotaltime += parseFloat(data.routes[attributename].sections[attributename2].travelSummary.duration);
      }
      
      data.routes[attributename].total_travel_meters = tempTotalmeters;
      data.routes[attributename].total_travel_time = tempTotaltime;
    }
    
  } else if (type === 'polyline') {
    // Polyline data integration
    for (let i = 0; i < ary.length; i++) {
      if (ary[i] !== undefined) {
        const AryTemp = [];
        AryTemp[i] = ary[i].split('##');
        data.routes[AryTemp[i][0]].sections[AryTemp[i][1]].polyline = AryTemp[i][2];
      }
    }
  }
  
  return data;
}
```

**Integration Features:**
- **Time Synchronization:** Adjusts departure/arrival times based on duration changes
- **Total Recalculation:** Updates route-level totals after section updates
- **First/Last Section Logic:** Special handling for route boundary sections
- **Data Type Handling:** Different logic for length vs polyline data

## 🚀 Usage Methods

### Basic API Enrichment
```javascript
const thirdPartyAPI = require('@app/src/services/thirdPartyAPI');

// Walking instructions enrichment
const walkingUrls = [
  '0##1##https://router.hereapi.com/v8/routes?origin=29.7604,-95.3698&destination=29.7500,-95.3600&transportMode=pedestrian&apikey=YOUR_KEY',
  '0##2##https://router.hereapi.com/v8/routes?origin=29.7500,-95.3600&destination=29.7400,-95.3500&transportMode=pedestrian&apikey=YOUR_KEY'
];

const walkingResult = await thirdPartyAPI.HereWalkingAPI(walkingUrls);
console.log('Walking instructions:', walkingResult.TempAry);
console.log('Failed requests:', walkingResult.LoseAPITemp);

// Polyline enrichment
const polylineUrls = [
  '0##1##https://transit.router.hereapi.com/v8/routes?origin=29.7604,-95.3698&destination=29.7500,-95.3600&apikey=YOUR_KEY',
  '0##2##https://router.hereapi.com/v8/routes?origin=29.7500,-95.3600&destination=29.7400,-95.3500&transportMode=car&apikey=YOUR_KEY'
];

const polylineResult = await thirdPartyAPI.HerePolylinesAPI(polylineUrls);
```

### Advanced Route Enhancement Pipeline
```javascript
class RouteEnhancementService {
  constructor() {
    this.thirdPartyAPI = require('@app/src/services/thirdPartyAPI');
    this.apiRetryLimit = 3;
    this.retryDelay = 2000;
  }

  async enhanceRouteData(routeData, enhancementTypes = ['polylines', 'lengths', 'instructions']) {
    try {
      const startTime = Date.now();
      let enhancedData = { ...routeData };
      const errors = [];
      
      // Generate API URLs for each enhancement type
      const apiRequests = this.generateAPIRequests(routeData, enhancementTypes);
      
      // Process each enhancement type
      for (const enhancementType of enhancementTypes) {
        try {
          const urls = apiRequests[enhancementType];
          if (urls && urls.length > 0) {
            const result = await this.processEnhancement(enhancementType, urls);
            enhancedData = await this.integrateResults(enhancedData, result, enhancementType);
          }
        } catch (error) {
          console.error(`Error processing ${enhancementType}:`, error);
          errors.push({
            type: enhancementType,
            error: error.message
          });
        }
      }
      
      const processingTime = Date.now() - startTime;
      
      return {
        success: true,
        data: enhancedData,
        processingTime,
        errors: errors.length > 0 ? errors : null,
        enhancementTypes: enhancementTypes
      };
    } catch (error) {
      console.error('Route enhancement failed:', error);
      return {
        success: false,
        data: routeData,
        error: error.message
      };
    }
  }

  generateAPIRequests(routeData, enhancementTypes) {
    const requests = {
      polylines: [],
      lengths: [],
      instructions: [],
      corrections: []
    };

    routeData.routes.forEach((route, routeIndex) => {
      route.sections.forEach((section, sectionIndex) => {
        const baseUrl = this.buildHereURL(section);
        const requestId = `${routeIndex}##${sectionIndex}##${baseUrl}`;

        if (enhancementTypes.includes('polylines')) {
          requests.polylines.push(requestId);
        }
        if (enhancementTypes.includes('lengths')) {
          requests.lengths.push(requestId);
        }
        if (enhancementTypes.includes('instructions') && section.type === 'pedestrian') {
          requests.instructions.push(requestId);
        }
      });
    });

    return requests;
  }

  buildHereURL(section) {
    const origin = `${section.departure.place.location.lat},${section.departure.place.location.lng}`;
    const destination = `${section.arrival.place.location.lat},${section.arrival.place.location.lng}`;
    
    let baseUrl = '';
    if (section.type === 'pedestrian') {
      baseUrl = `https://router.hereapi.com/v8/routes?origin=${origin}&destination=${destination}&transportMode=pedestrian`;
    } else if (section.type === 'transit') {
      baseUrl = `https://transit.router.hereapi.com/v8/routes?origin=${origin}&destination=${destination}`;
    } else if (section.type === 'car') {
      baseUrl = `https://router.hereapi.com/v8/routes?origin=${origin}&destination=${destination}&transportMode=car`;
    }
    
    return `${baseUrl}&apikey=${process.env.HERE_API_KEY}`;
  }

  async processEnhancement(enhancementType, urls) {
    let retries = 0;
    
    while (retries < this.apiRetryLimit) {
      try {
        switch (enhancementType) {
          case 'polylines':
            return await this.thirdPartyAPI.HerePolylinesAPI(urls);
          case 'lengths':
            return await this.thirdPartyAPI.HereLengthAPI(urls);
          case 'instructions':
            return await this.thirdPartyAPI.HereWalkingAPI(urls);
          case 'corrections':
            return await this.thirdPartyAPI.CorrectionsAPI(urls);
          default:
            throw new Error(`Unknown enhancement type: ${enhancementType}`);
        }
      } catch (error) {
        retries++;
        if (retries >= this.apiRetryLimit) {
          throw error;
        }
        console.log(`Retrying ${enhancementType} (attempt ${retries + 1})`);
        await this.delay(this.retryDelay);
      }
    }
  }

  async integrateResults(routeData, result, enhancementType) {
    if (enhancementType === 'polylines') {
      return await this.thirdPartyAPI.InsertData(routeData, result.TempAry, 'polyline');
    } else if (enhancementType === 'lengths' || enhancementType === 'corrections') {
      return await this.thirdPartyAPI.InsertData(routeData, result.TempAry, 'length');
    } else if (enhancementType === 'instructions') {
      return this.integrateWalkingInstructions(routeData, result.TempAry);
    }
    return routeData;
  }

  integrateWalkingInstructions(routeData, instructionsArray) {
    for (let i = 0; i < instructionsArray.length; i++) {
      if (instructionsArray[i] !== undefined) {
        const parts = instructionsArray[i].split('##');
        const routeIndex = parseInt(parts[0]);
        const sectionIndex = parseInt(parts[1]);
        const departureInstructions = parts[2];
        const arrivalInstructions = parts[3];

        if (routeData.routes[routeIndex] && routeData.routes[routeIndex].sections[sectionIndex]) {
          routeData.routes[routeIndex].sections[sectionIndex].walkingInstructions = {
            departure: departureInstructions,
            arrival: arrivalInstructions
          };
        }
      }
    }
    return routeData;
  }

  async delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async batchEnhanceMultipleRoutes(routesArray, enhancementTypes = ['polylines', 'lengths']) {
    const results = [];
    
    // Process routes in parallel
    const promises = routesArray.map(async (routeData, index) => {
      try {
        const result = await this.enhanceRouteData(routeData, enhancementTypes);
        return {
          index,
          success: true,
          result
        };
      } catch (error) {
        return {
          index,
          success: false,
          error: error.message,
          originalData: routeData
        };
      }
    });

    const processedResults = await Promise.all(promises);
    
    return {
      totalRoutes: routesArray.length,
      successful: processedResults.filter(r => r.success).length,
      failed: processedResults.filter(r => !r.success).length,
      results: processedResults
    };
  }

  getEnhancementStats() {
    return {
      supportedEnhancements: ['polylines', 'lengths', 'instructions', 'corrections'],
      supportedAPIs: ['HERE Router v8', 'HERE Transit v8', 'HERE Legacy v7.2'],
      retryLimit: this.apiRetryLimit,
      retryDelay: this.retryDelay
    };
  }
}

// Usage
const enhancementService = new RouteEnhancementService();

// Enhance single route
const sampleRoute = {
  routes: [
    {
      sections: [
        {
          type: 'pedestrian',
          departure: { place: { location: { lat: 29.7604, lng: -95.3698 } } },
          arrival: { place: { location: { lat: 29.7500, lng: -95.3600 } } }
        }
      ]
    }
  ]
};

const enhanced = await enhancementService.enhanceRouteData(sampleRoute, ['polylines', 'instructions']);
console.log('Enhanced route:', enhanced);

// Batch enhance multiple routes
const multipleRoutes = [sampleRoute, sampleRoute, sampleRoute];
const batchResult = await enhancementService.batchEnhanceMultipleRoutes(multipleRoutes);
console.log('Batch enhancement result:', batchResult);
```

### Performance Monitoring Integration
```javascript
class APIPerformanceMonitor {
  constructor() {
    this.thirdPartyAPI = require('@app/src/services/thirdPartyAPI');
    this.metrics = {
      totalRequests: 0,
      successfulRequests: 0,
      failedRequests: 0,
      averageResponseTime: 0,
      apiEndpoints: new Map()
    };
  }

  async monitoredAPICall(apiMethod, urls) {
    const startTime = Date.now();
    const endpointCounts = new Map();
    
    // Count endpoint usage
    urls.forEach(url => {
      const endpoint = this.extractEndpoint(url);
      endpointCounts.set(endpoint, (endpointCounts.get(endpoint) || 0) + 1);
    });

    try {
      const result = await this.thirdPartyAPI[apiMethod](urls);
      const duration = Date.now() - startTime;
      
      // Update metrics
      this.updateMetrics(urls.length, result.LoseAPITemp.length, duration, endpointCounts, 'success');
      
      return {
        ...result,
        performance: {
          duration,
          totalRequests: urls.length,
          successfulRequests: urls.length - result.LoseAPITemp.length,
          failedRequests: result.LoseAPITemp.length,
          successRate: ((urls.length - result.LoseAPITemp.length) / urls.length * 100).toFixed(2)
        }
      };
    } catch (error) {
      const duration = Date.now() - startTime;
      this.updateMetrics(urls.length, urls.length, duration, endpointCounts, 'error');
      
      return {
        TempAry: [],
        LoseAPITemp: urls,
        performance: {
          duration,
          totalRequests: urls.length,
          successfulRequests: 0,
          failedRequests: urls.length,
          successRate: '0.00',
          error: error.message
        }
      };
    }
  }

  extractEndpoint(urlString) {
    if (typeof urlString === 'string') {
      const parts = urlString.split('##');
      const url = parts.length > 2 ? parts[2] : urlString;
      
      if (url.includes('router.hereapi.com')) return 'HERE_ROUTER';
      if (url.includes('transit.router.hereapi.com')) return 'HERE_TRANSIT';
      if (url.includes('route.ls.hereapi.com')) return 'HERE_LEGACY';
    }
    return 'UNKNOWN';
  }

  updateMetrics(totalRequests, failedRequests, duration, endpointCounts, status) {
    this.metrics.totalRequests += totalRequests;
    this.metrics.successfulRequests += (totalRequests - failedRequests);
    this.metrics.failedRequests += failedRequests;
    
    // Update average response time
    const previousAvg = this.metrics.averageResponseTime;
    const previousTotal = this.metrics.totalRequests - totalRequests;
    this.metrics.averageResponseTime = 
      (previousAvg * previousTotal + duration) / this.metrics.totalRequests;

    // Update endpoint counts
    endpointCounts.forEach((count, endpoint) => {
      const current = this.metrics.apiEndpoints.get(endpoint) || { total: 0, successful: 0, failed: 0 };
      current.total += count;
      if (status === 'success') {
        current.successful += count;
      } else {
        current.failed += count;
      }
      this.metrics.apiEndpoints.set(endpoint, current);
    });
  }

  getPerformanceReport() {
    const endpointStats = {};
    this.metrics.apiEndpoints.forEach((stats, endpoint) => {
      endpointStats[endpoint] = {
        ...stats,
        successRate: stats.total > 0 ? (stats.successful / stats.total * 100).toFixed(2) : '0.00'
      };
    });

    return {
      summary: {
        totalRequests: this.metrics.totalRequests,
        successfulRequests: this.metrics.successfulRequests,
        failedRequests: this.metrics.failedRequests,
        overallSuccessRate: this.metrics.totalRequests > 0 ? 
          (this.metrics.successfulRequests / this.metrics.totalRequests * 100).toFixed(2) : '0.00',
        averageResponseTime: Math.round(this.metrics.averageResponseTime)
      },
      endpoints: endpointStats,
      timestamp: new Date().toISOString()
    };
  }

  resetMetrics() {
    this.metrics = {
      totalRequests: 0,
      successfulRequests: 0,
      failedRequests: 0,
      averageResponseTime: 0,
      apiEndpoints: new Map()
    };
  }
}

// Usage
const monitor = new APIPerformanceMonitor();

// Monitored API calls
const walkingUrls = ['0##1##https://router.hereapi.com/v8/routes?...'];
const result = await monitor.monitoredAPICall('HereWalkingAPI', walkingUrls);

console.log('API Result:', result);
console.log('Performance Report:', monitor.getPerformanceReport());
```

## 📊 Output Examples

### Successful API Processing
```javascript
{
  TempAry: [
    "0##1##Head north on Main St##Arrive at destination",
    "0##2##Head west on Commerce St##Turn right to destination"
  ],
  LoseAPITemp: []
}
```

### Polyline Processing Result
```javascript
{
  TempAry: [
    "0##1##BFoz5xJ67P1B1B7P7P-F-F6QoM4R8t@-A2DgF7C0B",
    "0##2##"
  ],
  LoseAPITemp: [
    "0##2##https://failed-url..."
  ]
}
```

### Route Enhancement Result
```javascript
{
  success: true,
  data: {
    routes: [
      {
        sections: [
          {
            type: "pedestrian",
            polyline: "BFoz5xJ67P1B1B7P7P-F-F6QoM4R8t@-A2DgF7C0B",
            travelSummary: {
              length: 1250,
              duration: 900
            },
            walkingInstructions: {
              departure: "Head north on Main St",
              arrival: "Arrive at destination"
            }
          }
        ],
        total_travel_meters: 1250,
        total_travel_time: 900
      }
    ]
  },
  processingTime: 2340,
  errors: null,
  enhancementTypes: ["polylines", "lengths", "instructions"]
}
```

### Performance Monitoring Report
```javascript
{
  summary: {
    totalRequests: 150,
    successfulRequests: 142,
    failedRequests: 8,
    overallSuccessRate: "94.67",
    averageResponseTime: 1250
  },
  endpoints: {
    "HERE_ROUTER": {
      total: 85,
      successful: 82,
      failed: 3,
      successRate: "96.47"
    },
    "HERE_TRANSIT": {
      total: 65,
      successful: 60,
      failed: 5,
      successRate: "92.31"
    }
  },
  timestamp: "2024-06-25T14:30:00.000Z"
}
```

## ⚠️ Important Notes

### API Integration and Rate Limiting
- **Parallel Processing:** All requests fired simultaneously for maximum throughput
- **Rate Limiting:** No built-in rate limiting - may need external throttling
- **API Keys:** Requires valid HERE Maps API keys in URLs
- **Service Monitoring:** InfluxDB integration available (commented) for production monitoring

### Error Handling and Resilience
- **Individual Failures:** Single request failures don't stop batch processing
- **Error Tracking:** Failed requests collected in LoseAPITemp array
- **Graceful Degradation:** Service continues with partial results
- **Retry Logic:** No built-in retries - implement externally if needed

### Data Transformation and Accuracy
- **Polyline Precision:** Uses precision 7 for coordinate accuracy
- **Multi-Section Handling:** Complex logic for combining route segments
- **Time Synchronization:** Adjusts departure/arrival times based on duration updates
- **Total Recalculation:** Updates route-level metrics after section changes

### Performance and Scalability
- **Memory Usage:** Large batches may consume significant memory
- **Processing Time:** Linear with batch size and API response times
- **Concurrent Limits:** Limited by axios defaults and HERE API limits
- **Response Size:** Large polylines and instructions may impact performance

## 🔗 Related File Links

- **Polyline Utilities:** `allrepo/connectsmart/tsp-api/src/services/hereMapPolylines.js`
- **HERE Integration:** Other HERE Maps service integrations
- **Route Processing:** Route planning and optimization services

---
*This service provides comprehensive HERE Maps API integration with parallel batch processing for route data enrichment in the TSP platform.*