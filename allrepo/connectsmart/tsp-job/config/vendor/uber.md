# TSP Job Service - Uber Integration Configuration

## Overview

The `config/vendor/uber.js` file manages Uber API integration configuration for the TSP Job service's rideshare services. This configuration provides access to Uber's Guest Ride API for trip estimation, booking, and management within the MaaS platform.

## File Information

- **File Path**: `/config/vendor/uber.js`
- **File Type**: JavaScript Configuration Module
- **Primary Purpose**: Uber API configuration for rideshare integration
- **Dependencies**: Environment variables for Uber API credentials and endpoints

## Configuration Structure

```javascript
module.exports = {
  loginUrl: 'https://login.uber.com/oauth/v2/token',
  etaUrl: process.env.UBER_ETA_URL || 'https://sandbox-api.uber.com/v1/guests/trips/estimates',
  baseUrl: process.env.UBER_GUEST_RIDE_URL || 'https://sandbox-api.uber.com/v1/guests',
  clientId: process.env.UBER_CLIENT_ID,
  clientSecret: process.env.UBER_CLIENT_SECRET,
};
```

## Configuration Components

### OAuth Authentication URL
```javascript
loginUrl: 'https://login.uber.com/oauth/v2/token'
```

**Purpose**: OAuth 2.0 token endpoint for Uber API authentication
- **Protocol**: OAuth 2.0 client credentials flow
- **Usage**: Obtain access tokens for API requests
- **Security**: Server-to-server authentication

### ETA Service URL
```javascript
etaUrl: process.env.UBER_ETA_URL || 'https://sandbox-api.uber.com/v1/guests/trips/estimates'
```

**Purpose**: Endpoint for trip time and cost estimates
- **Default**: Sandbox environment for testing
- **Production**: Environment variable override for production URL
- **Functionality**: Provides ride estimates without user authentication

### Base API URL
```javascript
baseUrl: process.env.UBER_GUEST_RIDE_URL || 'https://sandbox-api.uber.com/v1/guests'
```

**Purpose**: Base URL for Uber Guest Ride API
- **Default**: Sandbox environment for development
- **Production**: Environment variable override for production API
- **Scope**: Guest API access for ride booking and management

### Client Credentials
```javascript
clientId: process.env.UBER_CLIENT_ID,
clientSecret: process.env.UBER_CLIENT_SECRET
```

**Purpose**: OAuth 2.0 client credentials for API authentication
- **Client ID**: Public identifier for the application
- **Client Secret**: Private secret for secure authentication
- **Security**: Environment-based credential management

## Uber API Integration Implementation

### Authentication Service
```javascript
const axios = require('axios');
const config = require('../config/vendor/uber');

class UberAuthService {
  constructor() {
    this.accessToken = null;
    this.tokenExpiry = null;
  }
  
  async getAccessToken() {
    if (this.accessToken && this.tokenExpiry && new Date() < this.tokenExpiry) {
      return this.accessToken;
    }
    
    try {
      const response = await axios.post(config.loginUrl, 
        new URLSearchParams({
          grant_type: 'client_credentials',
          client_id: config.clientId,
          client_secret: config.clientSecret,
          scope: 'guest.trips'
        }),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          timeout: 10000
        }
      );
      
      this.accessToken = response.data.access_token;
      this.tokenExpiry = new Date(Date.now() + (response.data.expires_in * 1000));
      
      return this.accessToken;
    } catch (error) {
      console.error('Uber authentication error:', error);
      throw error;
    }
  }
  
  async makeAuthenticatedRequest(method, url, data = null) {
    const token = await this.getAccessToken();
    
    const requestConfig = {
      method: method,
      url: url,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      timeout: 15000
    };
    
    if (data) {
      requestConfig.data = data;
    }
    
    try {
      const response = await axios(requestConfig);
      return response.data;
    } catch (error) {
      console.error('Uber API request error:', error);
      throw error;
    }
  }
}

const uberAuth = new UberAuthService();
```

### Trip Estimation Service
```javascript
class UberEstimationService {
  static async getTripEstimate(pickup, destination, options = {}) {
    try {
      const estimateData = {
        pickup: {
          latitude: pickup.lat,
          longitude: pickup.lng,
          address: pickup.address
        },
        destination: {
          latitude: destination.lat,
          longitude: destination.lng,
          address: destination.address
        },
        seat_count: options.seatCount || 1
      };
      
      const response = await uberAuth.makeAuthenticatedRequest(
        'POST',
        config.etaUrl,
        estimateData
      );
      
      return {
        success: true,
        estimates: response.estimates || [],
        pickup_estimate: response.pickup_estimate,
        destination: response.destination
      };
    } catch (error) {
      console.error('Uber estimation error:', error);
      throw error;
    }
  }
  
  static async getProductTypes(latitude, longitude) {
    try {
      const url = `${config.baseUrl}/products?latitude=${latitude}&longitude=${longitude}`;
      const response = await uberAuth.makeAuthenticatedRequest('GET', url);
      
      return {
        success: true,
        products: response.products || []
      };
    } catch (error) {
      console.error('Uber products error:', error);
      throw error;
    }
  }
  
  static async getPriceEstimates(startLat, startLng, endLat, endLng) {
    try {
      const url = `${config.baseUrl}/price_estimates` +
        `?start_latitude=${startLat}&start_longitude=${startLng}` +
        `&end_latitude=${endLat}&end_longitude=${endLng}`;
      
      const response = await uberAuth.makeAuthenticatedRequest('GET', url);
      
      return {
        success: true,
        prices: response.prices || []
      };
    } catch (error) {
      console.error('Uber price estimates error:', error);
      throw error;
    }
  }
}
```

### Trip Booking Service
```javascript
class UberBookingService {
  static async createTrip(tripData, guestInfo) {
    try {
      const bookingData = {
        pickup: {
          latitude: tripData.pickup.lat,
          longitude: tripData.pickup.lng,
          address: tripData.pickup.address,
          nickname: tripData.pickup.nickname || 'Pickup Location'
        },
        destination: {
          latitude: tripData.destination.lat,
          longitude: tripData.destination.lng,
          address: tripData.destination.address,
          nickname: tripData.destination.nickname || 'Destination'
        },
        guest: {
          given_name: guestInfo.firstName,
          family_name: guestInfo.lastName,
          phone_number: guestInfo.phoneNumber,
          email: guestInfo.email
        },
        product_id: tripData.productId,
        seat_count: tripData.seatCount || 1
      };
      
      if (tripData.paymentMethodId) {
        bookingData.payment_method_id = tripData.paymentMethodId;
      }
      
      const response = await uberAuth.makeAuthenticatedRequest(
        'POST',
        `${config.baseUrl}/trips`,
        bookingData
      );
      
      return {
        success: true,
        trip: response,
        tripId: response.trip_id
      };
    } catch (error) {
      console.error('Uber trip creation error:', error);
      throw error;
    }
  }
  
  static async getTripStatus(tripId) {
    try {
      const response = await uberAuth.makeAuthenticatedRequest(
        'GET',
        `${config.baseUrl}/trips/${tripId}`
      );
      
      return {
        success: true,
        trip: response,
        status: response.status
      };
    } catch (error) {
      console.error('Uber trip status error:', error);
      throw error;
    }
  }
  
  static async cancelTrip(tripId, reason = 'user_requested') {
    try {
      const response = await uberAuth.makeAuthenticatedRequest(
        'PUT',
        `${config.baseUrl}/trips/${tripId}`,
        {
          status: 'cancelled',
          cancel_reason: reason
        }
      );
      
      return {
        success: true,
        trip: response,
        cancellation: response.cancellation
      };
    } catch (error) {
      console.error('Uber trip cancellation error:', error);
      throw error;
    }
  }
  
  static async updateTrip(tripId, updates) {
    try {
      const response = await uberAuth.makeAuthenticatedRequest(
        'PUT',
        `${config.baseUrl}/trips/${tripId}`,
        updates
      );
      
      return {
        success: true,
        trip: response
      };
    } catch (error) {
      console.error('Uber trip update error:', error);
      throw error;
    }
  }
}
```

### Real-time Trip Tracking
```javascript
class UberTrackingService {
  static async trackTrip(tripId) {
    try {
      const response = await uberAuth.makeAuthenticatedRequest(
        'GET',
        `${config.baseUrl}/trips/${tripId}/tracking`
      );
      
      return {
        success: true,
        tracking: response,
        driver: response.driver,
        vehicle: response.vehicle,
        location: response.location,
        eta: response.eta
      };
    } catch (error) {
      console.error('Uber tracking error:', error);
      throw error;
    }
  }
  
  static async getDriverLocation(tripId) {
    try {
      const trackingData = await this.trackTrip(tripId);
      
      if (trackingData.success && trackingData.location) {
        return {
          success: true,
          latitude: trackingData.location.latitude,
          longitude: trackingData.location.longitude,
          bearing: trackingData.location.bearing,
          speed: trackingData.location.speed,
          timestamp: trackingData.location.timestamp
        };
      }
      
      return {
        success: false,
        error: 'Location not available'
      };
    } catch (error) {
      console.error('Driver location error:', error);
      throw error;
    }
  }
  
  static async getArrivalTime(tripId) {
    try {
      const trackingData = await this.trackTrip(tripId);
      
      return {
        success: true,
        eta: trackingData.eta,
        estimatedArrival: new Date(Date.now() + (trackingData.eta * 1000))
      };
    } catch (error) {
      console.error('Arrival time error:', error);
      throw error;
    }
  }
}
```

## Integration with MaaS Platform

### Multi-Modal Trip Planning
```javascript
class UberMaaSIntegration {
  static async integrateWithTripPlan(tripPlan, userPreferences = {}) {
    try {
      const uberOptions = [];
      
      for (const segment of tripPlan.segments) {
        if (segment.mode === 'rideshare' || segment.mode === 'any') {
          const estimate = await UberEstimationService.getTripEstimate(
            segment.origin,
            segment.destination,
            {
              seatCount: userPreferences.passengerCount || 1
            }
          );
          
          if (estimate.success && estimate.estimates.length > 0) {
            uberOptions.push({
              segmentId: segment.id,
              provider: 'uber',
              estimates: estimate.estimates.map(est => ({
                productId: est.product_id,
                productName: est.product_name,
                priceEstimate: est.price_estimate,
                pickupTime: est.pickup_time_estimate,
                tripDuration: est.trip_duration_estimate,
                distanceEstimate: est.distance_estimate
              })),
              pickupEstimate: estimate.pickup_estimate
            });
          }
        }
      }
      
      return {
        success: true,
        uberOptions: uberOptions,
        integrationTimestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('Uber MaaS integration error:', error);
      throw error;
    }
  }
  
  static async bookIntegratedTrip(tripPlan, selectedOptions, guestInfo) {
    try {
      const bookings = [];
      
      for (const option of selectedOptions) {
        if (option.provider === 'uber') {
          const segment = tripPlan.segments.find(s => s.id === option.segmentId);
          
          const booking = await UberBookingService.createTrip(
            {
              pickup: segment.origin,
              destination: segment.destination,
              productId: option.productId,
              seatCount: option.seatCount || 1
            },
            guestInfo
          );
          
          bookings.push({
            segmentId: option.segmentId,
            provider: 'uber',
            tripId: booking.tripId,
            booking: booking.trip
          });
        }
      }
      
      return {
        success: true,
        bookings: bookings
      };
    } catch (error) {
      console.error('Integrated trip booking error:', error);
      throw error;
    }
  }
}
```

## Error Handling and Monitoring

### Error Classification
```javascript
class UberErrorHandler {
  static classifyError(error) {
    if (error.response) {
      const status = error.response.status;
      const data = error.response.data;
      
      switch (status) {
        case 400:
          return {
            type: 'validation_error',
            message: data.message || 'Invalid request parameters',
            code: data.code
          };
        case 401:
          return {
            type: 'authentication_error',
            message: 'Authentication failed',
            code: 'UNAUTHORIZED'
          };
        case 403:
          return {
            type: 'permission_error',
            message: 'Insufficient permissions',
            code: 'FORBIDDEN'
          };
        case 404:
          return {
            type: 'not_found',
            message: 'Resource not found',
            code: 'NOT_FOUND'
          };
        case 429:
          return {
            type: 'rate_limit',
            message: 'Rate limit exceeded',
            code: 'RATE_LIMITED',
            retryAfter: error.response.headers['retry-after']
          };
        case 500:
        case 502:
        case 503:
        case 504:
          return {
            type: 'server_error',
            message: 'Uber service temporarily unavailable',
            code: 'SERVICE_UNAVAILABLE',
            retryable: true
          };
        default:
          return {
            type: 'unknown_error',
            message: data.message || 'Unknown error occurred',
            code: data.code || 'UNKNOWN'
          };
      }
    }
    
    return {
      type: 'network_error',
      message: 'Network connection failed',
      code: 'NETWORK_ERROR',
      retryable: true
    };
  }
  
  static async handleRetryableError(error, retryCount = 0, maxRetries = 3) {
    const errorInfo = this.classifyError(error);
    
    if (errorInfo.retryable && retryCount < maxRetries) {
      const delay = Math.pow(2, retryCount) * 1000; // Exponential backoff
      
      console.log(`Retrying Uber request in ${delay}ms (attempt ${retryCount + 1}/${maxRetries})`);
      
      await new Promise(resolve => setTimeout(resolve, delay));
      return true; // Indicate that retry should be attempted
    }
    
    return false; // No retry should be attempted
  }
}
```

### Performance Monitoring
```javascript
class UberPerformanceMonitor {
  static async trackAPICall(operation, startTime, success, error = null) {
    const duration = Date.now() - startTime;
    
    const metrics = {
      service: 'uber',
      operation: operation,
      duration: duration,
      success: success,
      timestamp: new Date().toISOString(),
      error: error ? UberErrorHandler.classifyError(error) : null
    };
    
    // Store metrics for analysis
    await this.storeMetrics(metrics);
    
    // Alert on slow responses
    if (duration > 10000) { // 10 seconds
      await this.alertSlowResponse(operation, duration);
    }
  }
  
  static async getPerformanceStats(timeRange = '24h') {
    const metrics = await this.retrieveMetrics('uber', timeRange);
    
    return {
      totalRequests: metrics.length,
      successRate: metrics.filter(m => m.success).length / metrics.length,
      averageLatency: metrics.reduce((sum, m) => sum + m.duration, 0) / metrics.length,
      operationBreakdown: this.groupByOperation(metrics)
    };
  }
}
```

This Uber integration configuration provides comprehensive rideshare services for the TSP Job service, enabling trip estimation, booking, tracking, and management with proper authentication, error handling, and performance monitoring for seamless integration with the MaaS platform.