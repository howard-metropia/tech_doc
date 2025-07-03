# TollGuru Configuration Documentation

## Quick Summary

This configuration module manages the integration settings for TollGuru API, a comprehensive toll calculation service that provides real-time toll costs, route optimization, and toll analytics. TollGuru helps transportation platforms calculate accurate toll charges across multiple toll systems, enabling cost-effective route planning and transparent pricing for users. The configuration establishes API authentication and endpoint settings for seamless toll calculation integration within the TSP Job system.

## Technical Analysis

### Code Structure

```javascript
module.exports = {
  apiKey: process.env.TOLLGURU_API_KEY || 'F87gRb46JBbmdbtH9tT9LJ2RnPGGJqL9',
  url: 'https://dev.TollGuru.com',
  source: 'here',
};
```

### Configuration Properties

1. **apiKey**: Authentication token for TollGuru API
   - Sources from `TOLLGURU_API_KEY` environment variable
   - Falls back to default development key
   - Used for API authentication in request headers

2. **url**: TollGuru API base endpoint
   - Points to development environment by default
   - No environment variable override (potential improvement area)
   - Base URL for all TollGuru API requests

3. **source**: Map data source identifier
   - Set to 'here' indicating HERE Maps integration
   - Determines coordinate system and route format
   - Affects toll calculation accuracy and coverage

### Integration Architecture

The configuration supports TollGuru's RESTful API architecture:
- Authentication via API key in headers
- Route-based toll calculations
- Support for multiple map providers
- Real-time toll rate updates

## Usage/Integration

### Loading Configuration

```javascript
const tollguruConfig = require('./config/vendor/tollguru');

// Access configuration
const { apiKey, url, source } = tollguruConfig;
```

### Basic API Integration

```javascript
const axios = require('axios');
const tollguruConfig = require('./config/vendor/tollguru');

async function calculateTollCost(route) {
  const endpoint = `${tollguruConfig.url}/v1/calc/route`;
  
  const response = await axios.post(endpoint, {
    source: tollguruConfig.source,
    polyline: route.encodedPolyline,
    vehicle: {
      type: '2AxlesAuto',
      weight: {
        value: 2000,
        unit: 'pound'
      },
      height: {
        value: 7,
        unit: 'feet'
      }
    },
    departure_time: new Date().toISOString()
  }, {
    headers: {
      'x-api-key': tollguruConfig.apiKey,
      'Content-Type': 'application/json'
    }
  });
  
  return response.data;
}
```

### Integration with HERE Maps

```javascript
const tollguruConfig = require('./config/vendor/tollguru');
const hereAPI = require('./services/hereAPI');

class TollCalculationService {
  constructor() {
    this.config = tollguruConfig;
    this.hereService = new hereAPI();
  }

  async getRouteWithTolls(origin, destination, vehicleType = '2AxlesAuto') {
    // Get route from HERE Maps
    const hereRoute = await this.hereService.calculateRoute(origin, destination);
    
    // Calculate tolls using TollGuru
    const tollData = await this.calculateTolls({
      polyline: hereRoute.polyline,
      vehicleType: vehicleType,
      departureTime: new Date()
    });
    
    return {
      route: hereRoute,
      tolls: tollData.tolls,
      summary: {
        distance: hereRoute.distance,
        duration: hereRoute.duration,
        tollCost: tollData.summary.tollCost,
        currency: tollData.summary.currency
      }
    };
  }

  async calculateTolls(routeData) {
    const response = await fetch(`${this.config.url}/v1/calc/route`, {
      method: 'POST',
      headers: {
        'x-api-key': this.config.apiKey,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        source: this.config.source,
        polyline: routeData.polyline,
        vehicle: {
          type: routeData.vehicleType
        },
        departure_time: routeData.departureTime.toISOString()
      })
    });

    if (!response.ok) {
      throw new Error(`TollGuru API error: ${response.status}`);
    }

    return response.json();
  }
}
```

## Dependencies

### Internal Dependencies

1. **HERE API Service** (`services/hereAPI.js`): Provides route polylines
2. **Google Maps Service** (`services/googleMap.js`): Alternative route provider
3. **Trip Processing Jobs**: Use toll calculations for cost estimation
4. **Route Planning Services**: Integrate toll costs in route optimization

### External Dependencies

1. **TollGuru API**: Third-party toll calculation service
2. **HERE Maps**: Primary source for route polylines
3. **HTTP Clients**: axios or fetch for API requests
4. **Polyline Libraries**: For encoding/decoding route data

### Vehicle Type Support

TollGuru supports various vehicle classifications:
```javascript
const VEHICLE_TYPES = {
  CAR: '2AxlesAuto',
  MOTORCYCLE: '2AxlesMotorcycle',
  PICKUP: '2AxlesPickup',
  SUV: '2AxlesSUV',
  TRUCK: '3AxlesTruck',
  BUS: '2AxlesBus',
  RV: '2AxlesRV',
  TAXI: '2AxlesTaxi'
};
```

## Code Examples

### Advanced Toll Calculation Service

```javascript
const tollguruConfig = require('./config/vendor/tollguru');

class AdvancedTollService {
  constructor() {
    this.config = tollguruConfig;
    this.cache = new Map();
    this.cacheTimeout = 3600000; // 1 hour
  }

  async calculateMultiRouteTolls(routes, vehicleProfile) {
    const results = await Promise.all(
      routes.map(route => this.calculateRouteToll(route, vehicleProfile))
    );
    
    return results.sort((a, b) => a.totalCost - b.totalCost);
  }

  async calculateRouteToll(route, vehicleProfile) {
    const cacheKey = this.getCacheKey(route, vehicleProfile);
    const cached = this.cache.get(cacheKey);
    
    if (cached && cached.timestamp > Date.now() - this.cacheTimeout) {
      return cached.data;
    }
    
    const tollData = await this.fetchTollData(route, vehicleProfile);
    
    this.cache.set(cacheKey, {
      data: tollData,
      timestamp: Date.now()
    });
    
    return tollData;
  }

  async fetchTollData(route, vehicleProfile) {
    const requestBody = {
      source: this.config.source,
      polyline: route.polyline,
      vehicle: {
        type: vehicleProfile.type,
        weight: vehicleProfile.weight,
        height: vehicleProfile.height,
        axles: vehicleProfile.axles
      },
      departure_time: route.departureTime || new Date().toISOString(),
      return_tolls_by_road: true,
      return_toll_locations: true
    };

    const response = await fetch(`${this.config.url}/v1/calc/route`, {
      method: 'POST',
      headers: {
        'x-api-key': this.config.apiKey,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    });

    const data = await response.json();
    
    return {
      route: route,
      totalCost: data.summary.tollCost,
      currency: data.summary.currency,
      tollsByRoad: data.tollsByRoad,
      tollLocations: data.tollLocations,
      breakdown: this.processTollBreakdown(data)
    };
  }

  processTollBreakdown(tollData) {
    return tollData.tollsByRoad.map(toll => ({
      name: toll.name,
      cost: toll.cost,
      location: toll.location,
      type: toll.type,
      payment_method: toll.payment_method
    }));
  }

  getCacheKey(route, vehicleProfile) {
    return `${route.polyline.substring(0, 20)}_${vehicleProfile.type}_${vehicleProfile.weight.value}`;
  }
}
```

### Error Handling and Retry Logic

```javascript
const tollguruConfig = require('./config/vendor/tollguru');

class TollGuruClient {
  constructor() {
    this.config = tollguruConfig;
    this.maxRetries = 3;
    this.retryDelay = 1000;
  }

  async makeRequest(endpoint, data, retryCount = 0) {
    try {
      const response = await fetch(`${this.config.url}${endpoint}`, {
        method: 'POST',
        headers: {
          'x-api-key': this.config.apiKey,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });

      if (response.status === 429) {
        // Rate limit exceeded
        const retryAfter = response.headers.get('Retry-After') || 60;
        await this.delay(retryAfter * 1000);
        return this.makeRequest(endpoint, data, retryCount);
      }

      if (!response.ok) {
        throw new Error(`TollGuru API error: ${response.status} ${response.statusText}`);
      }

      return response.json();
    } catch (error) {
      if (retryCount < this.maxRetries) {
        await this.delay(this.retryDelay * Math.pow(2, retryCount));
        return this.makeRequest(endpoint, data, retryCount + 1);
      }
      
      throw error;
    }
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

### Environment-Specific Configuration

```javascript
// Enhanced configuration with environment support
const getConfig = () => {
  const env = process.env.NODE_ENV || 'development';
  
  const configs = {
    development: {
      apiKey: process.env.TOLLGURU_API_KEY || 'F87gRb46JBbmdbtH9tT9LJ2RnPGGJqL9',
      url: 'https://dev.TollGuru.com',
      source: 'here'
    },
    staging: {
      apiKey: process.env.TOLLGURU_API_KEY,
      url: 'https://staging.TollGuru.com',
      source: 'here'
    },
    production: {
      apiKey: process.env.TOLLGURU_API_KEY,
      url: 'https://api.TollGuru.com',
      source: 'here'
    }
  };

  if (env === 'production' && !process.env.TOLLGURU_API_KEY) {
    throw new Error('TOLLGURU_API_KEY must be set in production');
  }

  return configs[env];
};

module.exports = getConfig();
```

### Batch Processing Implementation

```javascript
const tollguruConfig = require('./config/vendor/tollguru');

class TollBatchProcessor {
  constructor() {
    this.config = tollguruConfig;
    this.batchSize = 10;
  }

  async processBatchRoutes(routes, vehicleType) {
    const batches = this.createBatches(routes, this.batchSize);
    const results = [];

    for (const batch of batches) {
      const batchResults = await Promise.all(
        batch.map(route => this.processRoute(route, vehicleType))
      );
      results.push(...batchResults);
      
      // Rate limiting between batches
      await this.delay(1000);
    }

    return results;
  }

  createBatches(items, size) {
    const batches = [];
    for (let i = 0; i < items.length; i += size) {
      batches.push(items.slice(i, i + size));
    }
    return batches;
  }

  async processRoute(route, vehicleType) {
    try {
      const response = await fetch(`${this.config.url}/v1/calc/route`, {
        method: 'POST',
        headers: {
          'x-api-key': this.config.apiKey,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          source: this.config.source,
          polyline: route.polyline,
          vehicle: { type: vehicleType },
          departure_time: route.departureTime
        })
      });

      const data = await response.json();
      
      return {
        routeId: route.id,
        success: true,
        tollCost: data.summary.tollCost,
        currency: data.summary.currency,
        details: data
      };
    } catch (error) {
      return {
        routeId: route.id,
        success: false,
        error: error.message
      };
    }
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

## Best Practices

1. **API Key Management**:
   - Store production keys in secure environment variables
   - Rotate API keys periodically
   - Monitor key usage for anomalies

2. **Performance Optimization**:
   - Implement response caching for repeated routes
   - Batch API requests when processing multiple routes
   - Use connection pooling for HTTP clients

3. **Error Handling**:
   - Implement comprehensive error catching
   - Log API failures with context
   - Provide fallback toll estimates when API is unavailable

4. **Monitoring**:
   - Track API response times
   - Monitor rate limit usage
   - Alert on authentication failures

This configuration module provides the foundation for toll calculation features within the TSP Job system, enabling accurate cost estimation and route optimization while maintaining flexibility across different deployment environments.