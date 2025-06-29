# TSP API Parking Service Documentation

## 🔍 Quick Summary (TL;DR)
The Parking service provides a unified interface to multiple parking data providers (INRIX, Smarking, ParkingLotApp) for discovering off-street parking lots, real-time availability, and parking information aggregation across different data sources.

**Keywords:** parking-aggregation | multi-provider | inrix-integration | smarking-integration | parking-discovery | off-street-parking | parking-lots | vendor-abstraction

**Primary use cases:** Finding nearby parking lots, aggregating parking data from multiple sources, providing unified parking information API, managing different parking data providers

**Compatibility:** Node.js >= 16.0.0, Multiple parking data provider APIs, Axios for HTTP requests, Slack integration for error monitoring

## ❓ Common Questions Quick Index
- **Q: What parking providers are supported?** → INRIX, Smarking, and ParkingLotApp
- **Q: How are multiple providers managed?** → Unified interface with provider-specific modules
- **Q: What types of parking data?** → Off-street parking lots, availability, location information
- **Q: How is authentication handled?** → Each provider has its own auth mechanism (tokens, API keys)
- **Q: Are errors monitored?** → Yes, comprehensive error tracking with Slack notifications
- **Q: Can providers be used independently?** → Yes, each provider service can be used separately

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **parking information hub** that connects to different parking companies' systems. Just like how a travel app might check multiple airlines for flights, this service checks multiple parking companies (INRIX, Smarking, etc.) to find available parking spots and give users a complete picture of parking options in an area.

**Technical explanation:** 
A parking data aggregation service that provides unified access to multiple parking information providers through a modular architecture. Each provider module handles authentication, API communication, and data formatting independently while exposing consistent interfaces for parking lot discovery and availability queries.

**Business value explanation:**
Maximizes parking data coverage by leveraging multiple providers, reduces dependency on single data sources, provides comprehensive parking information for better user experience, enables competitive pricing analysis, and supports scalable parking marketplace development.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/parking.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with modular provider architecture
- **Type:** Multi-Provider Parking Data Aggregation Service
- **File Size:** ~0.2 KB (main file), ~3.1 KB (INRIX module)
- **Complexity Score:** ⭐⭐⭐ (Medium - Multi-provider integration with authentication)

**Dependencies:**
- `axios`: HTTP client for API requests (**Critical**)
- `@maas/core/log`: Logging infrastructure (**High**)
- `@maas/services`: Slack error notification service (**Medium**)
- Provider-specific configurations (**High**)

## 📝 Detailed Code Analysis

### Main Service Architecture

**Modular Design:**
```javascript
module.exports = {
  inrix: InrixServices,
  smarking: SmarkingServices,
  parkingLotApp: ParkingLotAppServices,
};
```

**Provider Independence:** Each provider is implemented as a separate module with its own:
- Authentication mechanisms
- API endpoint configurations
- Data transformation logic
- Error handling strategies

### INRIX Provider Implementation

**Authentication System:**
- **Token-Based:** Uses app token authentication
- **Auto-Refresh:** Automatic token renewal on 400/401 errors
- **Interceptor Pattern:** Axios interceptors handle auth seamlessly

**Key Functions:**

### getAuthorization Function

**Purpose:** Obtains access token from INRIX authentication service

**Returns:** Promise resolving to access token string

**Implementation:**
```javascript
const getAuthorization = async () => {
  const url = `${settings.auth_url}/v1/appToken`;
  const response = await axios.get(url, { params: settings.auth });
  return response.data.result.token;
};
```

**Error Handling:** Logs authentication failures and returns null on error

### getOffStreetParkingLot Function

**Purpose:** Searches for off-street parking lots using location or bounding box

**Parameters:**
- `input.boundingBox`: String - Comma-separated coordinates (lng_min,lat_min,lng_max,lat_max)
- `input.lat`: Number - Center latitude for radius search
- `input.lng`: Number - Center longitude for radius search  
- `input.radius`: Number - Search radius for point-based queries

**Returns:** Promise resolving to array of parking lot objects

**Search Modes:**
1. **Bounding Box Search:** Rectangular area defined by coordinates
2. **Radius Search:** Circular area around center point

**Coordinate Transformation:**
```javascript
// Input format: southwestern, northwestern (lng min, lat min, lng max, lat max)
// INRIX format: northwestern, southeastern (lat1|long1,lat2|long2)
const point = input.boundingBox.split(',');
queryParams = {
  box: `${point[1]}|${point[0]},${point[3]}|${point[2]}`,
};
```

**Error Monitoring:**
- Slack notifications for API failures
- Comprehensive error logging with request metadata
- Graceful fallback returning empty array

### Axios Interceptors

**Request Interceptor:**
```javascript
axiosApiInstance.interceptors.request.use(
  async (config) => {
    config.params.accesstoken = accessToken;
    return config;
  }
);
```

**Response Interceptor:**
```javascript
axiosApiInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    if ((error.response.status === 400 || error.response.status === 401) && 
        !error.config.__isRetryRequest) {
      accessToken = await getAuthorization();
      error.config.__isRetryRequest = true;
      return axiosApiInstance(error.config);
    }
    return Promise.reject(error);
  }
);
```

## 🚀 Usage Methods

### Basic Multi-Provider Parking Search
```javascript
const parkingService = require('@app/src/services/parking');

async function findParkingOptions(location, searchRadius = 1000) {
  const searchParams = {
    lat: location.latitude,
    lng: location.longitude,
    radius: searchRadius
  };
  
  try {
    // Search across all providers
    const providers = ['inrix', 'smarking', 'parkingLotApp'];
    const results = {};
    
    for (const provider of providers) {
      try {
        if (provider === 'inrix' && parkingService.inrix.getOffStreetParkingLot) {
          results[provider] = await parkingService.inrix.getOffStreetParkingLot(searchParams);
        } else if (provider === 'smarking' && parkingService.smarking.findParkingLots) {
          results[provider] = await parkingService.smarking.findParkingLots(searchParams);
        } else if (provider === 'parkingLotApp' && parkingService.parkingLotApp.searchLots) {
          results[provider] = await parkingService.parkingLotApp.searchLots(searchParams);
        }
      } catch (error) {
        console.error(`Error with ${provider}:`, error.message);
        results[provider] = [];
      }
    }
    
    return {
      location: searchParams,
      providers: results,
      totalResults: Object.values(results).reduce((sum, lots) => sum + lots.length, 0)
    };
  } catch (error) {
    console.error('Error in parking search:', error);
    throw error;
  }
}

// Usage
const location = { latitude: 29.7604, longitude: -95.3698 };
const parkingOptions = await findParkingOptions(location, 500);
```

### INRIX-Specific Parking Discovery
```javascript
class InrixParkingManager {
  constructor() {
    this.inrixService = require('@app/src/services/parking').inrix;
  }

  async searchByBoundingBox(southWest, northEast) {
    try {
      // Format: lng_min,lat_min,lng_max,lat_max
      const boundingBox = `${southWest.lng},${southWest.lat},${northEast.lng},${northEast.lat}`;
      
      const lots = await this.inrixService.getOffStreetParkingLot({
        boundingBox
      });
      
      return {
        searchMethod: 'boundingBox',
        bounds: { southWest, northEast },
        results: lots.map(lot => this.formatParkingLot(lot)),
        resultCount: lots.length
      };
    } catch (error) {
      console.error('INRIX bounding box search failed:', error);
      throw error;
    }
  }

  async searchByRadius(centerPoint, radiusMeters) {
    try {
      const lots = await this.inrixService.getOffStreetParkingLot({
        lat: centerPoint.latitude,
        lng: centerPoint.longitude,
        radius: radiusMeters
      });
      
      return {
        searchMethod: 'radius',
        center: centerPoint,
        radius: radiusMeters,
        results: lots.map(lot => this.formatParkingLot(lot)),
        resultCount: lots.length
      };
    } catch (error) {
      console.error('INRIX radius search failed:', error);
      throw error;
    }
  }

  formatParkingLot(rawLot) {
    return {
      id: rawLot.id,
      name: rawLot.name,
      location: {
        latitude: rawLot.geometry?.coordinates?.[1],
        longitude: rawLot.geometry?.coordinates?.[0],
        address: rawLot.address
      },
      capacity: {
        total: rawLot.totalSpaces,
        available: rawLot.availableSpaces
      },
      pricing: {
        hourlyRate: rawLot.rates?.hourly,
        dailyRate: rawLot.rates?.daily,
        currency: 'USD'
      },
      features: {
        covered: rawLot.covered,
        valet: rawLot.valet,
        reservation: rawLot.reservable
      },
      provider: 'inrix'
    };
  }

  async getAuthStatus() {
    try {
      const token = await this.inrixService.getAuthorization();
      return {
        authenticated: !!token,
        tokenLength: token ? token.length : 0,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      return {
        authenticated: false,
        error: error.message,
        timestamp: new Date().toISOString()
      };
    }
  }
}
```

### Multi-Provider Aggregation Service
```javascript
class ParkingAggregationService {
  constructor() {
    this.parkingService = require('@app/src/services/parking');
    this.providers = ['inrix', 'smarking', 'parkingLotApp'];
  }

  async aggregatedSearch(searchParams) {
    const results = {
      searchParams,
      providers: {},
      aggregated: {
        totalLots: 0,
        averageDistance: 0,
        priceRange: { min: Infinity, max: 0 },
        features: {
          covered: 0,
          valet: 0,
          reservation: 0
        }
      }
    };
    
    // Search all providers in parallel
    const providerPromises = this.providers.map(async (provider) => {
      try {
        let lots = [];
        
        switch (provider) {
          case 'inrix':
            lots = await this.parkingService.inrix.getOffStreetParkingLot(searchParams);
            break;
          case 'smarking':
            // Assuming similar interface
            if (this.parkingService.smarking?.findLots) {
              lots = await this.parkingService.smarking.findLots(searchParams);
            }
            break;
          case 'parkingLotApp':
            // Assuming similar interface
            if (this.parkingService.parkingLotApp?.searchLots) {
              lots = await this.parkingService.parkingLotApp.searchLots(searchParams);
            }
            break;
        }
        
        return {
          provider,
          lots: lots.map(lot => this.standardizeLotData(lot, provider)),
          success: true,
          count: lots.length
        };
      } catch (error) {
        console.error(`Provider ${provider} failed:`, error.message);
        return {
          provider,
          lots: [],
          success: false,
          error: error.message,
          count: 0
        };
      }
    });
    
    const providerResults = await Promise.all(providerPromises);
    
    // Process results
    for (const result of providerResults) {
      results.providers[result.provider] = result;
      
      if (result.success) {
        results.aggregated.totalLots += result.count;
        
        // Aggregate pricing and features
        for (const lot of result.lots) {
          if (lot.pricing?.hourlyRate) {
            results.aggregated.priceRange.min = Math.min(
              results.aggregated.priceRange.min, 
              lot.pricing.hourlyRate
            );
            results.aggregated.priceRange.max = Math.max(
              results.aggregated.priceRange.max, 
              lot.pricing.hourlyRate
            );
          }
          
          if (lot.features?.covered) results.aggregated.features.covered++;
          if (lot.features?.valet) results.aggregated.features.valet++;
          if (lot.features?.reservation) results.aggregated.features.reservation++;
        }
      }
    }
    
    // Calculate success rate
    const successfulProviders = providerResults.filter(r => r.success).length;
    results.aggregated.providerSuccessRate = (successfulProviders / this.providers.length * 100).toFixed(1) + '%';
    
    // Fix price range if no valid prices found
    if (results.aggregated.priceRange.min === Infinity) {
      results.aggregated.priceRange = { min: 0, max: 0 };
    }
    
    return results;
  }

  standardizeLotData(rawLot, provider) {
    // Standardize data format across providers
    const standardLot = {
      id: rawLot.id || rawLot.lotId || rawLot.identifier,
      name: rawLot.name || rawLot.title || rawLot.lotName,
      provider,
      location: {},
      capacity: {},
      pricing: {},
      features: {},
      lastUpdated: new Date().toISOString()
    };
    
    // Provider-specific field mapping
    switch (provider) {
      case 'inrix':
        standardLot.location = {
          latitude: rawLot.geometry?.coordinates?.[1],
          longitude: rawLot.geometry?.coordinates?.[0],
          address: rawLot.address
        };
        standardLot.capacity = {
          total: rawLot.totalSpaces,
          available: rawLot.availableSpaces
        };
        standardLot.pricing = {
          hourlyRate: rawLot.rates?.hourly,
          dailyRate: rawLot.rates?.daily
        };
        break;
        
      case 'smarking':
        // Add Smarking-specific mapping
        standardLot.location = {
          latitude: rawLot.lat || rawLot.latitude,
          longitude: rawLot.lng || rawLot.longitude,
          address: rawLot.address
        };
        break;
        
      case 'parkingLotApp':
        // Add ParkingLotApp-specific mapping
        break;
    }
    
    return standardLot;
  }

  async getProviderHealth() {
    const healthChecks = {};
    
    for (const provider of this.providers) {
      try {
        const startTime = Date.now();
        
        switch (provider) {
          case 'inrix':
            await this.parkingService.inrix.getAuthorization();
            break;
          case 'smarking':
            // Health check for Smarking
            break;
          case 'parkingLotApp':
            // Health check for ParkingLotApp
            break;
        }
        
        const responseTime = Date.now() - startTime;
        healthChecks[provider] = {
          status: 'healthy',
          responseTime,
          timestamp: new Date().toISOString()
        };
      } catch (error) {
        healthChecks[provider] = {
          status: 'unhealthy',
          error: error.message,
          timestamp: new Date().toISOString()
        };
      }
    }
    
    const healthyProviders = Object.values(healthChecks).filter(h => h.status === 'healthy').length;
    
    return {
      overall: {
        status: healthyProviders > 0 ? 'operational' : 'degraded',
        healthyProviders,
        totalProviders: this.providers.length,
        healthPercentage: (healthyProviders / this.providers.length * 100).toFixed(1) + '%'
      },
      providers: healthChecks
    };
  }
}
```

### Parking Analytics and Comparison
```javascript
class ParkingAnalyticsService {
  constructor() {
    this.aggregationService = new ParkingAggregationService();
  }

  async analyzeParkingAvailability(area) {
    try {
      const searchParams = {
        boundingBox: area.boundingBox || undefined,
        lat: area.center?.latitude,
        lng: area.center?.longitude,
        radius: area.radius || 1000
      };
      
      const results = await this.aggregationService.aggregatedSearch(searchParams);
      
      const analytics = {
        area: area.name || 'Unknown Area',
        searchParams,
        summary: {
          totalParkingLots: results.aggregated.totalLots,
          dataProviders: Object.keys(results.providers).length,
          successfulProviders: Object.values(results.providers).filter(p => p.success).length
        },
        availability: this.calculateAvailabilityMetrics(results),
        pricing: this.calculatePricingMetrics(results),
        features: this.calculateFeatureMetrics(results),
        providerComparison: this.compareProviders(results.providers)
      };
      
      return analytics;
    } catch (error) {
      console.error('Error in parking analytics:', error);
      throw error;
    }
  }

  calculateAvailabilityMetrics(results) {
    let totalSpaces = 0;
    let availableSpaces = 0;
    let lotsWithAvailability = 0;
    
    for (const provider of Object.values(results.providers)) {
      if (provider.success) {
        for (const lot of provider.lots) {
          if (lot.capacity?.total) {
            totalSpaces += lot.capacity.total;
            lotsWithAvailability++;
          }
          if (lot.capacity?.available) {
            availableSpaces += lot.capacity.available;
          }
        }
      }
    }
    
    return {
      totalSpaces,
      availableSpaces,
      occupancyRate: totalSpaces > 0 ? ((totalSpaces - availableSpaces) / totalSpaces * 100).toFixed(1) + '%' : 'N/A',
      lotsWithAvailabilityData: lotsWithAvailability,
      availabilityDataCoverage: results.aggregated.totalLots > 0 ? 
        (lotsWithAvailability / results.aggregated.totalLots * 100).toFixed(1) + '%' : '0%'
    };
  }

  calculatePricingMetrics(results) {
    const prices = [];
    
    for (const provider of Object.values(results.providers)) {
      if (provider.success) {
        for (const lot of provider.lots) {
          if (lot.pricing?.hourlyRate && lot.pricing.hourlyRate > 0) {
            prices.push(lot.pricing.hourlyRate);
          }
        }
      }
    }
    
    if (prices.length === 0) {
      return {
        averageHourlyRate: 'N/A',
        priceRange: 'N/A',
        lotsWithPricing: 0,
        pricingDataCoverage: '0%'
      };
    }
    
    prices.sort((a, b) => a - b);
    
    return {
      averageHourlyRate: '$' + (prices.reduce((sum, price) => sum + price, 0) / prices.length).toFixed(2),
      priceRange: `$${prices[0].toFixed(2)} - $${prices[prices.length - 1].toFixed(2)}`,
      medianPrice: '$' + prices[Math.floor(prices.length / 2)].toFixed(2),
      lotsWithPricing: prices.length,
      pricingDataCoverage: results.aggregated.totalLots > 0 ? 
        (prices.length / results.aggregated.totalLots * 100).toFixed(1) + '%' : '0%'
    };
  }

  calculateFeatureMetrics(results) {
    const features = {
      covered: 0,
      valet: 0,
      reservation: 0,
      electric: 0,
      handicap: 0
    };
    
    let totalLots = 0;
    
    for (const provider of Object.values(results.providers)) {
      if (provider.success) {
        totalLots += provider.lots.length;
        for (const lot of provider.lots) {
          if (lot.features?.covered) features.covered++;
          if (lot.features?.valet) features.valet++;
          if (lot.features?.reservation) features.reservation++;
          if (lot.features?.electric) features.electric++;
          if (lot.features?.handicap) features.handicap++;
        }
      }
    }
    
    const featurePercentages = {};
    for (const [feature, count] of Object.entries(features)) {
      featurePercentages[feature] = totalLots > 0 ? 
        (count / totalLots * 100).toFixed(1) + '%' : '0%';
    }
    
    return {
      counts: features,
      percentages: featurePercentages,
      totalLots
    };
  }

  compareProviders(providers) {
    const comparison = {};
    
    for (const [providerName, providerData] of Object.entries(providers)) {
      comparison[providerName] = {
        status: providerData.success ? 'operational' : 'failed',
        lotCount: providerData.count,
        dataQuality: this.assessDataQuality(providerData.lots),
        errorMessage: providerData.error || null
      };
    }
    
    return comparison;
  }

  assessDataQuality(lots) {
    if (lots.length === 0) {
      return { score: 0, details: 'No data' };
    }
    
    let score = 0;
    const maxScore = 5;
    
    // Check for basic location data
    const hasLocation = lots.filter(lot => lot.location?.latitude && lot.location?.longitude).length;
    if (hasLocation / lots.length > 0.9) score += 1;
    
    // Check for pricing data
    const hasPricing = lots.filter(lot => lot.pricing?.hourlyRate).length;
    if (hasPricing / lots.length > 0.5) score += 1;
    
    // Check for availability data
    const hasAvailability = lots.filter(lot => lot.capacity?.total).length;
    if (hasAvailability / lots.length > 0.5) score += 1;
    
    // Check for feature data
    const hasFeatures = lots.filter(lot => Object.keys(lot.features || {}).length > 0).length;
    if (hasFeatures / lots.length > 0.3) score += 1;
    
    // Check for complete records
    const completeRecords = lots.filter(lot => 
      lot.location?.latitude && lot.pricing?.hourlyRate && lot.capacity?.total
    ).length;
    if (completeRecords / lots.length > 0.3) score += 1;
    
    return {
      score,
      maxScore,
      percentage: (score / maxScore * 100).toFixed(1) + '%',
      details: {
        locationCoverage: (hasLocation / lots.length * 100).toFixed(1) + '%',
        pricingCoverage: (hasPricing / lots.length * 100).toFixed(1) + '%',
        availabilityCoverage: (hasAvailability / lots.length * 100).toFixed(1) + '%',
        featureCoverage: (hasFeatures / lots.length * 100).toFixed(1) + '%',
        completeRecords: (completeRecords / lots.length * 100).toFixed(1) + '%'
      }
    };
  }
}
```

## 📊 Output Examples

### Multi-Provider Search Results
```json
{
  "location": {
    "lat": 29.7604,
    "lng": -95.3698,
    "radius": 500
  },
  "providers": {
    "inrix": [
      {
        "id": "inrix_lot_123",
        "name": "Downtown Parking Garage",
        "location": {
          "latitude": 29.7610,
          "longitude": -95.3705,
          "address": "123 Main St, Houston, TX"
        },
        "capacity": {
          "total": 300,
          "available": 45
        },
        "pricing": {
          "hourlyRate": 3.50,
          "dailyRate": 25.00
        }
      }
    ],
    "smarking": [],
    "parkingLotApp": []
  },
  "totalResults": 1
}
```

### INRIX Bounding Box Search
```json
{
  "searchMethod": "boundingBox",
  "bounds": {
    "southWest": { "lat": 29.750, "lng": -95.380 },
    "northEast": { "lat": 29.770, "lng": -95.360 }
  },
  "results": [
    {
      "id": "lot_456",
      "name": "City Center Parking",
      "location": {
        "latitude": 29.7604,
        "longitude": -95.3698,
        "address": "456 Commerce St"
      },
      "capacity": {
        "total": 150,
        "available": 23
      },
      "features": {
        "covered": true,
        "valet": false,
        "reservation": true
      },
      "provider": "inrix"
    }
  ],
  "resultCount": 1
}
```

### Provider Health Status
```json
{
  "overall": {
    "status": "operational",
    "healthyProviders": 2,
    "totalProviders": 3,
    "healthPercentage": "66.7%"
  },
  "providers": {
    "inrix": {
      "status": "healthy",
      "responseTime": 245,
      "timestamp": "2024-06-25T14:30:00Z"
    },
    "smarking": {
      "status": "healthy",
      "responseTime": 180,
      "timestamp": "2024-06-25T14:30:00Z"
    },
    "parkingLotApp": {
      "status": "unhealthy",
      "error": "Connection timeout",
      "timestamp": "2024-06-25T14:30:00Z"
    }
  }
}
```

### Parking Analytics Summary
```json
{
  "area": "Downtown Houston",
  "summary": {
    "totalParkingLots": 15,
    "dataProviders": 3,
    "successfulProviders": 2
  },
  "availability": {
    "totalSpaces": 2250,
    "availableSpaces": 340,
    "occupancyRate": "84.9%",
    "lotsWithAvailabilityData": 12,
    "availabilityDataCoverage": "80.0%"
  },
  "pricing": {
    "averageHourlyRate": "$4.25",
    "priceRange": "$2.00 - $8.50",
    "medianPrice": "$4.00",
    "lotsWithPricing": 10,
    "pricingDataCoverage": "66.7%"
  },
  "features": {
    "percentages": {
      "covered": "40.0%",
      "valet": "13.3%",
      "reservation": "60.0%"
    }
  }
}
```

### Authentication Status
```json
{
  "authenticated": true,
  "tokenLength": 32,
  "timestamp": "2024-06-25T14:30:00Z"
}
```

## ⚠️ Important Notes

### Provider-Specific Considerations
- **INRIX:** Requires app token authentication with automatic refresh
- **Smarking:** Different API structure and authentication method
- **ParkingLotApp:** Separate authentication and data format
- **Rate Limits:** Each provider has different rate limiting policies

### Authentication Management
- **Token Persistence:** Tokens stored in memory, renewed on expiration
- **Auto-Retry:** Automatic authentication retry on 400/401 errors
- **Provider Independence:** Each provider manages its own auth state
- **Error Handling:** Graceful fallback when authentication fails

### Data Standardization Challenges
- **Format Differences:** Each provider returns different data structures
- **Field Mapping:** Requires careful mapping of provider-specific fields
- **Quality Variations:** Data completeness varies significantly between providers
- **Update Frequencies:** Providers update availability data at different intervals

### Error Monitoring and Reliability
- **Slack Integration:** Real-time error notifications for API failures
- **Comprehensive Logging:** Detailed error logs with request/response data
- **Graceful Degradation:** Service continues with available providers when others fail
- **Health Monitoring:** Regular health checks for all providers

### Performance Considerations
- **Parallel Requests:** Multiple providers queried simultaneously
- **Timeout Handling:** Reasonable timeouts prevent hanging requests
- **Caching Opportunities:** Static parking lot data could be cached
- **Rate Limiting:** Respect provider rate limits to avoid blocking

### Geographic Considerations
- **Coordinate Systems:** Different providers may use different coordinate formats
- **Search Areas:** Bounding box vs radius search capabilities vary
- **Coverage Areas:** Providers have different geographic coverage
- **Accuracy Levels:** Location accuracy varies between data sources

### Business Intelligence
- **Coverage Analysis:** Track which providers have best coverage in different areas
- **Price Comparison:** Identify pricing trends across providers
- **Availability Patterns:** Analyze availability patterns by time and location
- **Quality Metrics:** Monitor data quality and completeness by provider

## 🔗 Related File Links

- **INRIX Service:** `allrepo/connectsmart/tsp-api/src/services/parking/inrix.js`
- **Smarking Service:** `allrepo/connectsmart/tsp-api/src/services/parking/smarking.js`
- **ParkingLotApp Service:** `allrepo/connectsmart/tsp-api/src/services/parking/parkinglotapp.js`
- **Configuration:** Provider-specific config files for authentication and endpoints

---
*This service provides essential multi-provider parking data aggregation capabilities with comprehensive error handling and monitoring for the TSP platform.*