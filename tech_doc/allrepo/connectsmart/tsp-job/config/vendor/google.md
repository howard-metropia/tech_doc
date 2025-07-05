# TSP Job Service - Google Maps Configuration

## Overview

The `config/vendor/google.js` file manages Google Maps Platform configuration for the TSP Job service's mapping and geospatial services integration. This configuration provides access to Google Maps APIs for route planning, geocoding, and location-based services essential for the MaaS platform.

## File Information

- **File Path**: `/config/vendor/google.js`
- **File Type**: JavaScript Configuration Module
- **Primary Purpose**: Google Maps Platform API configuration
- **Dependencies**: Environment variables for Google Maps API credentials

## Configuration Structure

```javascript
module.exports = {
  maps: {
    apiKey: process.env.GOOGLE_MAPS_API_KEY,
  },
};
```

## Configuration Components

### Google Maps API Configuration
```javascript
maps: {
  apiKey: process.env.GOOGLE_MAPS_API_KEY,
}
```

**Purpose**: Core Google Maps Platform API access configuration
- **API Key**: Authentication credential for Google Maps services
- **Service Access**: Enables multiple Google Maps APIs through single key
- **Rate Limiting**: Subject to Google's API quotas and billing

## Google Maps Integration

### Maps Client Implementation
```javascript
const { Client } = require('@googlemaps/google-maps-services-js');
const config = require('../config/vendor/google');

const googleMapsClient = new Client({
  timeout: 10000,
  retryOptions: {
    retries: 3
  }
});

class GoogleMapsService {
  static async geocode(address) {
    try {
      const response = await googleMapsClient.geocode({
        params: {
          address: address,
          key: config.maps.apiKey
        }
      });
      
      return {
        success: true,
        results: response.data.results,
        status: response.data.status
      };
    } catch (error) {
      console.error('Geocoding error:', error);
      throw error;
    }
  }
  
  static async reverseGeocode(lat, lng) {
    try {
      const response = await googleMapsClient.reverseGeocode({
        params: {
          latlng: `${lat},${lng}`,
          key: config.maps.apiKey
        }
      });
      
      return {
        success: true,
        results: response.data.results,
        status: response.data.status
      };
    } catch (error) {
      console.error('Reverse geocoding error:', error);
      throw error;
    }
  }
  
  static async getDirections(origin, destination, options = {}) {
    try {
      const response = await googleMapsClient.directions({
        params: {
          origin: origin,
          destination: destination,
          mode: options.mode || 'driving',
          departure_time: options.departureTime || 'now',
          traffic_model: options.trafficModel || 'best_guess',
          alternatives: options.alternatives || true,
          key: config.maps.apiKey
        }
      });
      
      return {
        success: true,
        routes: response.data.routes,
        status: response.data.status,
        geocoded_waypoints: response.data.geocoded_waypoints
      };
    } catch (error) {
      console.error('Directions error:', error);
      throw error;
    }
  }
  
  static async getDistanceMatrix(origins, destinations, options = {}) {
    try {
      const response = await googleMapsClient.distancematrix({
        params: {
          origins: origins,
          destinations: destinations,
          mode: options.mode || 'driving',
          units: options.units || 'metric',
          traffic_model: options.trafficModel || 'best_guess',
          departure_time: options.departureTime || 'now',
          key: config.maps.apiKey
        }
      });
      
      return {
        success: true,
        rows: response.data.rows,
        status: response.data.status,
        origin_addresses: response.data.origin_addresses,
        destination_addresses: response.data.destination_addresses
      };
    } catch (error) {
      console.error('Distance matrix error:', error);
      throw error;
    }
  }
  
  static async findNearbyPlaces(lat, lng, type, radius = 1000) {
    try {
      const response = await googleMapsClient.placesNearby({
        params: {
          location: `${lat},${lng}`,
          radius: radius,
          type: type,
          key: config.maps.apiKey
        }
      });
      
      return {
        success: true,
        results: response.data.results,
        status: response.data.status
      };
    } catch (error) {
      console.error('Places nearby error:', error);
      throw error;
    }
  }
}
```

## Trip Planning Integration

### Route Optimization
```javascript
class RouteOptimizer {
  static async optimizeMultiStopRoute(waypoints, options = {}) {
    const origin = waypoints[0];
    const destination = waypoints[waypoints.length - 1];
    const intermediateWaypoints = waypoints.slice(1, -1);
    
    try {
      const response = await GoogleMapsService.getDirections(origin, destination, {
        waypoints: intermediateWaypoints,
        optimizeWaypoints: true,
        mode: options.mode || 'driving',
        trafficModel: options.trafficModel || 'best_guess'
      });
      
      if (response.routes.length > 0) {
        const route = response.routes[0];
        return {
          optimizedRoute: route,
          waypointOrder: route.waypoint_order,
          totalDistance: route.legs.reduce((sum, leg) => sum + leg.distance.value, 0),
          totalDuration: route.legs.reduce((sum, leg) => sum + leg.duration.value, 0),
          durationInTraffic: route.legs.reduce((sum, leg) => 
            sum + (leg.duration_in_traffic ? leg.duration_in_traffic.value : leg.duration.value), 0
          )
        };
      }
      
      throw new Error('No routes found');
    } catch (error) {
      console.error('Route optimization error:', error);
      throw error;
    }
  }
  
  static async calculateRouteAlternatives(origin, destination, options = {}) {
    try {
      const [drivingRoute, transitRoute, walkingRoute] = await Promise.allSettled([
        GoogleMapsService.getDirections(origin, destination, { mode: 'driving', ...options }),
        GoogleMapsService.getDirections(origin, destination, { mode: 'transit', ...options }),
        GoogleMapsService.getDirections(origin, destination, { mode: 'walking', ...options })
      ]);
      
      const alternatives = {};
      
      if (drivingRoute.status === 'fulfilled' && drivingRoute.value.routes.length > 0) {
        alternatives.driving = this.extractRouteInfo(drivingRoute.value.routes[0]);
      }
      
      if (transitRoute.status === 'fulfilled' && transitRoute.value.routes.length > 0) {
        alternatives.transit = this.extractRouteInfo(transitRoute.value.routes[0]);
      }
      
      if (walkingRoute.status === 'fulfilled' && walkingRoute.value.routes.length > 0) {
        alternatives.walking = this.extractRouteInfo(walkingRoute.value.routes[0]);
      }
      
      return alternatives;
    } catch (error) {
      console.error('Route alternatives error:', error);
      throw error;
    }
  }
  
  static extractRouteInfo(route) {
    return {
      distance: route.legs.reduce((sum, leg) => sum + leg.distance.value, 0),
      duration: route.legs.reduce((sum, leg) => sum + leg.duration.value, 0),
      durationInTraffic: route.legs.reduce((sum, leg) => 
        sum + (leg.duration_in_traffic ? leg.duration_in_traffic.value : leg.duration.value), 0
      ),
      polyline: route.overview_polyline.points,
      bounds: route.bounds,
      summary: route.summary
    };
  }
}
```

### Location Services
```javascript
class LocationServices {
  static async enrichLocationData(lat, lng) {
    try {
      const [reverseGeocode, nearbyPlaces] = await Promise.allSettled([
        GoogleMapsService.reverseGeocode(lat, lng),
        GoogleMapsService.findNearbyPlaces(lat, lng, 'point_of_interest', 500)
      ]);
      
      const locationData = {
        coordinates: { lat, lng },
        address: null,
        pointsOfInterest: [],
        addressComponents: {}
      };
      
      if (reverseGeocode.status === 'fulfilled' && reverseGeocode.value.results.length > 0) {
        const result = reverseGeocode.value.results[0];
        locationData.address = result.formatted_address;
        
        // Extract address components
        result.address_components.forEach(component => {
          component.types.forEach(type => {
            locationData.addressComponents[type] = component.long_name;
          });
        });
      }
      
      if (nearbyPlaces.status === 'fulfilled' && nearbyPlaces.value.results.length > 0) {
        locationData.pointsOfInterest = nearbyPlaces.value.results.map(place => ({
          name: place.name,
          placeId: place.place_id,
          types: place.types,
          rating: place.rating,
          userRatingsTotal: place.user_ratings_total,
          vicinity: place.vicinity
        }));
      }
      
      return locationData;
    } catch (error) {
      console.error('Location enrichment error:', error);
      throw error;
    }
  }
  
  static async validateAddress(address) {
    try {
      const geocodeResult = await GoogleMapsService.geocode(address);
      
      if (geocodeResult.results.length === 0) {
        return {
          valid: false,
          message: 'Address not found'
        };
      }
      
      const result = geocodeResult.results[0];
      return {
        valid: true,
        formattedAddress: result.formatted_address,
        coordinates: result.geometry.location,
        confidence: this.calculateAddressConfidence(result),
        components: result.address_components
      };
    } catch (error) {
      console.error('Address validation error:', error);
      return {
        valid: false,
        message: 'Address validation failed',
        error: error.message
      };
    }
  }
  
  static calculateAddressConfidence(geocodeResult) {
    const locationType = geocodeResult.geometry.location_type;
    const confidence = {
      'ROOFTOP': 0.9,
      'RANGE_INTERPOLATED': 0.8,
      'GEOMETRIC_CENTER': 0.6,
      'APPROXIMATE': 0.4
    };
    
    return confidence[locationType] || 0.3;
  }
}
```

## Performance Optimization

### Caching Strategy
```javascript
const NodeCache = require('node-cache');
const googleMapsCache = new NodeCache({ stdTTL: 3600 }); // 1 hour cache

class CachedGoogleMapsService extends GoogleMapsService {
  static async geocode(address) {
    const cacheKey = `geocode:${address}`;
    const cached = googleMapsCache.get(cacheKey);
    
    if (cached) {
      return cached;
    }
    
    const result = await super.geocode(address);
    googleMapsCache.set(cacheKey, result);
    return result;
  }
  
  static async getDirections(origin, destination, options = {}) {
    const cacheKey = `directions:${origin}:${destination}:${JSON.stringify(options)}`;
    const cached = googleMapsCache.get(cacheKey);
    
    if (cached) {
      return cached;
    }
    
    const result = await super.getDirections(origin, destination, options);
    
    // Cache for shorter time if traffic-dependent
    const ttl = options.departureTime === 'now' ? 300 : 3600; // 5 min vs 1 hour
    googleMapsCache.set(cacheKey, result, ttl);
    
    return result;
  }
  
  static async findNearbyPlaces(lat, lng, type, radius = 1000) {
    const cacheKey = `places:${lat}:${lng}:${type}:${radius}`;
    const cached = googleMapsCache.get(cacheKey);
    
    if (cached) {
      return cached;
    }
    
    const result = await super.findNearbyPlaces(lat, lng, type, radius);
    googleMapsCache.set(cacheKey, result, 1800); // 30 minutes
    return result;
  }
}
```

### Rate Limiting
```javascript
const RateLimiter = require('limiter').RateLimiter;

class RateLimitedGoogleMapsService {
  constructor() {
    // Google Maps free tier: 40,000 requests per month
    // Premium: up to 100,000 requests per day
    this.limiter = new RateLimiter(100, 'minute'); // 100 requests per minute
  }
  
  async makeRequest(requestFunction, ...args) {
    return new Promise((resolve, reject) => {
      this.limiter.removeTokens(1, (err, remainingRequests) => {
        if (err) {
          reject(err);
        } else {
          requestFunction(...args)
            .then(resolve)
            .catch(reject);
        }
      });
    });
  }
  
  async geocode(address) {
    return this.makeRequest(CachedGoogleMapsService.geocode.bind(CachedGoogleMapsService), address);
  }
  
  async getDirections(origin, destination, options = {}) {
    return this.makeRequest(
      CachedGoogleMapsService.getDirections.bind(CachedGoogleMapsService),
      origin,
      destination,
      options
    );
  }
}
```

## Monitoring and Analytics

### Usage Tracking
```javascript
class GoogleMapsMonitor {
  static async trackAPIUsage(apiName, success, latency, quotaUsed = 1) {
    const metrics = {
      api: apiName,
      success: success,
      latency: latency,
      quotaUsed: quotaUsed,
      timestamp: new Date().toISOString()
    };
    
    // Store metrics for analysis
    await this.storeMetrics(metrics);
    
    // Check quota limits
    await this.checkQuotaLimits(apiName, quotaUsed);
  }
  
  static async getUsageStatistics(timeRange = '24h') {
    // Retrieve usage statistics from metrics storage
    const stats = await this.retrieveMetrics(timeRange);
    
    return {
      totalRequests: stats.length,
      successRate: stats.filter(s => s.success).length / stats.length,
      averageLatency: stats.reduce((sum, s) => sum + s.latency, 0) / stats.length,
      quotaUsage: stats.reduce((sum, s) => sum + s.quotaUsed, 0),
      apiBreakdown: this.groupByAPI(stats)
    };
  }
  
  static async checkQuotaLimits(apiName, quotaUsed) {
    const dailyLimit = this.getQuotaLimit(apiName);
    const currentUsage = await this.getCurrentUsage(apiName);
    
    if (currentUsage + quotaUsed > dailyLimit * 0.9) {
      // Send alert when approaching 90% of quota
      await this.sendQuotaAlert(apiName, currentUsage, dailyLimit);
    }
  }
  
  static getQuotaLimit(apiName) {
    const quotas = {
      'geocoding': 40000,
      'directions': 40000,
      'distance_matrix': 100000,
      'places': 40000
    };
    
    return quotas[apiName] || 40000;
  }
}
```

### Error Handling and Retry Logic
```javascript
class RobustGoogleMapsService extends RateLimitedGoogleMapsService {
  static async makeRequestWithRetry(requestFunction, maxRetries = 3, ...args) {
    let lastError;
    
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        const startTime = Date.now();
        const result = await requestFunction(...args);
        const latency = Date.now() - startTime;
        
        await GoogleMapsMonitor.trackAPIUsage(
          requestFunction.name,
          true,
          latency
        );
        
        return result;
      } catch (error) {
        lastError = error;
        
        await GoogleMapsMonitor.trackAPIUsage(
          requestFunction.name,
          false,
          0
        );
        
        if (this.isRetryableError(error) && attempt < maxRetries) {
          const delay = Math.pow(2, attempt) * 1000; // Exponential backoff
          await new Promise(resolve => setTimeout(resolve, delay));
          continue;
        }
        
        break;
      }
    }
    
    throw lastError;
  }
  
  static isRetryableError(error) {
    const retryableStatuses = [
      'OVER_QUERY_LIMIT',
      'REQUEST_DENIED',
      'UNKNOWN_ERROR'
    ];
    
    return retryableStatuses.includes(error.response?.data?.status) ||
           error.code === 'ECONNRESET' ||
           error.code === 'ETIMEDOUT';
  }
}
```

## Security and Compliance

### API Key Management
```javascript
class SecureGoogleMapsConfig {
  static validateAPIKey(apiKey) {
    if (!apiKey || apiKey.length < 30) {
      throw new Error('Invalid Google Maps API key');
    }
    
    if (!apiKey.startsWith('AIza')) {
      throw new Error('Google Maps API key format is invalid');
    }
    
    return true;
  }
  
  static getRestrictedConfig() {
    // For client-side usage with restrictions
    return {
      apiKey: config.maps.apiKey,
      restrictions: {
        allowedDomains: process.env.ALLOWED_DOMAINS?.split(',') || [],
        allowedIPs: process.env.ALLOWED_IPS?.split(',') || [],
        allowedAPIs: [
          'maps_javascript_api',
          'geocoding_api',
          'directions_api'
        ]
      }
    };
  }
}
```

This Google Maps configuration provides comprehensive mapping and geospatial services integration for the TSP Job service, enabling route planning, geocoding, and location-based services with proper caching, rate limiting, monitoring, and error handling capabilities.