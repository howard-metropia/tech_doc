# TSP API HERE Routing Service Documentation

## 🔍 Quick Summary (TL;DR)
The HERE Routing service provides route calculation functionality using HERE Technologies' routing API, with comprehensive monitoring, error handling, and Slack alerting for production reliability.

**Keywords:** here-routing | route-calculation | turn-by-turn | here-api | navigation | route-planning | influx-monitoring | slack-alerts

**Primary use cases:** Calculating optimal routes between locations, generating turn-by-turn directions, multimodal trip planning, real-time route optimization

**Compatibility:** Node.js >= 16.0.0, HERE Maps API v8, InfluxDB monitoring, Slack integration

## ❓ Common Questions Quick Index
- **Q: What transport modes are supported?** → Car, pedestrian, bicycle, truck, and public transit
- **Q: How are API failures handled?** → Automatic Slack alerts and InfluxDB monitoring
- **Q: What's the API timeout?** → 10 seconds for route requests
- **Q: Are routes real-time?** → Yes, includes live traffic and road conditions
- **Q: What return formats are available?** → Polylines, turn instructions, summaries, and more
- **Q: How is performance monitored?** → InfluxDB tracks response times and success rates

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as your **personal GPS calculator** that connects to HERE Maps. When you need to get from point A to point B, it asks HERE's powerful computers to figure out the best route, considering traffic, road conditions, and your method of travel (car, walking, bike, etc.). It also keeps track of how well the service is working and alerts the team if anything goes wrong.

**Technical explanation:** 
A production-grade routing service that interfaces with HERE Technologies' v8 routing API to calculate optimal routes between geographic points. Features comprehensive monitoring via InfluxDB, automatic Slack alerting for failures, configurable timeouts, and support for multiple transport modes with real-time traffic integration.

**Business value explanation:**
Critical for navigation and trip planning applications. Provides reliable, real-time routing with enterprise-grade monitoring and alerting. Reduces development complexity while ensuring high availability and performance tracking for business-critical transportation services.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/hereRouting.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Axios HTTP client with monitoring integration
- **Type:** External API Integration Service
- **File Size:** ~2.3 KB
- **Complexity Score:** ⭐⭐⭐ (Medium - External API with comprehensive monitoring)

**Dependencies:**
- `config`: Configuration management (**Critical**)
- `@maas/core/log`: Logging infrastructure (**High**)
- `axios`: HTTP client for API requests (**Critical**)
- `@maas/services`: InfluxDB and Slack managers (**Critical**)
- `@app/src/static/error-code`: Error code definitions (**High**)

## 📝 Detailed Code Analysis

### HERE Routing Function

**Purpose:** Calculates routes using HERE Technologies API with comprehensive monitoring

**Parameters:**
- `transportMode`: String - Transport method (car, pedestrian, bicycle, truck, publicTransport)
- `originLocation`: String - Starting coordinates (lat,lng format)
- `destinationLocation`: String - Ending coordinates (lat,lng format)
- `returnMode`: String - Data to return (polyline, summary, actions, etc.)
- `originApi`: String - Calling API identifier for monitoring

**Processing Flow:**
1. **Parameter Assembly:** Constructs HERE API request parameters
2. **API Request:** Calls HERE routing API with timeout protection
3. **Success Monitoring:** Logs successful requests to InfluxDB
4. **Error Handling:** Comprehensive error capture and alerting
5. **Slack Notification:** Sends failure alerts to configured Slack channel

**Request Configuration:**
```javascript
const axiosApiInstance = axios.create({
  timeout: 10000,
  baseURL: hereConfig.router,
});

const params = {
  transportMode,
  origin: originLocation,
  destination: destinationLocation,
  return: returnMode,
  apikey: hereConfig.apiKey,
};
```

**Monitoring Integration:**
```javascript
await influx.writeIntoServiceMonitor({
  originApi,
  vendor: 'Here',
  vendorService: 'Routing',
  vendorApi: 'https://router.hereapi.com/v8/routes',
  status: 'SUCCESS',
  duration: new Date() - start,
  meta: params,
});
```

**Error Handling and Alerting:**
```javascript
const slack = new SlackManager(slackConfig.token, slackConfig.channelId);
slack.sendVendorFailedMsg({
  project: projectConfig.projectName,
  stage: projectConfig.projectStage,
  status: 'ERROR',
  vendor: 'Here',
  vendorApi: '/v8/routes',
  originApi,
  errorMsg,
  meta: JSON.stringify(requestParams)
});
```

## 🚀 Usage Methods

### Basic Route Calculation
```javascript
const { hereRouting } = require('@app/src/services/hereRouting');

async function calculateRoute() {
  try {
    const route = await hereRouting(
      'car',                           // Transport mode
      '52.5,13.4',                    // Berlin coordinates
      '52.6,13.5',                    // Destination coordinates
      'polyline,summary,actions',      // Return data types
      'GET /api/v2/routes'            // Origin API for monitoring
    );
    
    console.log('Route calculated successfully');
    console.log('Distance:', route.routes[0].sections[0].summary.length);
    console.log('Duration:', route.routes[0].sections[0].summary.duration);
    
    return route;
  } catch (error) {
    console.error('Route calculation failed:', error.message);
    throw error;
  }
}
```

### Multi-Modal Route Planning
```javascript
class RoutePlanningService {
  constructor() {
    this.hereRouting = require('@app/src/services/hereRouting').hereRouting;
  }

  async getMultiModalOptions(origin, destination, originApi) {
    const transportModes = ['car', 'pedestrian', 'bicycle', 'publicTransport'];
    const routeOptions = [];

    for (const mode of transportModes) {
      try {
        const route = await this.hereRouting(
          mode,
          origin,
          destination,
          'summary,polyline',
          originApi
        );

        if (route.routes && route.routes.length > 0) {
          const summary = route.routes[0].sections[0].summary;
          routeOptions.push({
            mode,
            distance: summary.length,
            duration: summary.duration,
            polyline: route.routes[0].sections[0].polyline
          });
        }
      } catch (error) {
        console.warn(`${mode} routing failed:`, error.message);
        // Continue with other modes
      }
    }

    return routeOptions.sort((a, b) => a.duration - b.duration);
  }

  async getOptimalRoute(origin, destination, preferences = {}) {
    const {
      preferredMode = 'car',
      avoidTolls = false,
      avoidHighways = false
    } = preferences;

    let returnMode = 'polyline,summary,actions';
    if (avoidTolls) returnMode += ',tollCost';
    
    try {
      const route = await this.hereRouting(
        preferredMode,
        origin,
        destination,
        returnMode,
        'GET /api/v2/optimal-route'
      );

      return this.formatRouteResponse(route);
    } catch (error) {
      // Fallback to basic route without preferences
      console.warn('Optimal routing failed, falling back to basic route');
      return await this.hereRouting(
        preferredMode,
        origin,
        destination,
        'polyline,summary',
        'GET /api/v2/optimal-route-fallback'
      );
    }
  }

  formatRouteResponse(hereResponse) {
    if (!hereResponse.routes || hereResponse.routes.length === 0) {
      throw new Error('No routes found');
    }

    const route = hereResponse.routes[0];
    const section = route.sections[0];

    return {
      distance: section.summary.length,
      duration: section.summary.duration,
      polyline: section.polyline,
      instructions: section.actions || [],
      tollCosts: section.tollCost || null,
      departureTime: section.departure?.time,
      arrivalTime: section.arrival?.time
    };
  }
}
```

### Real-Time Route Updates
```javascript
class RealTimeRoutingService {
  constructor() {
    this.hereRouting = require('@app/src/services/hereRouting').hereRouting;
    this.activeRoutes = new Map();
  }

  async startRouteTracking(routeId, origin, destination, transportMode) {
    try {
      const route = await this.hereRouting(
        transportMode,
        origin,
        destination,
        'polyline,summary,actions',
        `GET /api/v2/routes/${routeId}/track`
      );

      this.activeRoutes.set(routeId, {
        route,
        lastUpdate: Date.now(),
        transportMode,
        origin,
        destination
      });

      return route;
    } catch (error) {
      console.error(`Failed to start tracking route ${routeId}:`, error);
      throw error;
    }
  }

  async updateRoute(routeId, currentLocation) {
    const activeRoute = this.activeRoutes.get(routeId);
    if (!activeRoute) {
      throw new Error(`Route ${routeId} not found in active tracking`);
    }

    try {
      // Recalculate route from current position
      const updatedRoute = await this.hereRouting(
        activeRoute.transportMode,
        currentLocation,
        activeRoute.destination,
        'polyline,summary,actions',
        `GET /api/v2/routes/${routeId}/update`
      );

      activeRoute.route = updatedRoute;
      activeRoute.lastUpdate = Date.now();

      return updatedRoute;
    } catch (error) {
      console.error(`Failed to update route ${routeId}:`, error);
      // Return last known good route
      return activeRoute.route;
    }
  }

  stopRouteTracking(routeId) {
    return this.activeRoutes.delete(routeId);
  }
}
```

### Batch Route Processing
```javascript
async function processBatchRoutes(routeRequests, maxConcurrency = 5) {
  const { hereRouting } = require('@app/src/services/hereRouting');
  const results = [];
  
  // Process routes in batches to avoid overwhelming the API
  for (let i = 0; i < routeRequests.length; i += maxConcurrency) {
    const batch = routeRequests.slice(i, i + maxConcurrency);
    
    const batchPromises = batch.map(async (request, index) => {
      try {
        const route = await hereRouting(
          request.transportMode,
          request.origin,
          request.destination,
          request.returnMode || 'summary',
          `BATCH /routes/batch-${Math.floor(i/maxConcurrency)}-${index}`
        );
        
        return {
          requestId: request.id,
          success: true,
          route: route
        };
      } catch (error) {
        return {
          requestId: request.id,
          success: false,
          error: error.message
        };
      }
    });

    const batchResults = await Promise.allSettled(batchPromises);
    results.push(...batchResults.map(result => result.value));

    // Rate limiting delay between batches
    if (i + maxConcurrency < routeRequests.length) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }

  return results;
}
```

## 📊 Output Examples

### Successful Route Response
```json
{
  "routes": [
    {
      "id": "route-1",
      "sections": [
        {
          "id": "section-1",
          "type": "vehicle",
          "departure": {
            "time": "2024-06-25T14:30:00Z",
            "place": {
              "location": {
                "lat": 52.5,
                "lng": 13.4
              }
            }
          },
          "arrival": {
            "time": "2024-06-25T15:15:00Z",
            "place": {
              "location": {
                "lat": 52.6,
                "lng": 13.5
              }
            }
          },
          "summary": {
            "length": 18500,
            "duration": 2700,
            "baseDuration": 2400
          },
          "polyline": "BG8ysDlwBjE8B9F4D...",
          "actions": [
            {
              "action": "depart",
              "instruction": "Head north on Main Street"
            }
          ]
        }
      ]
    }
  ]
}
```

### Error Response
```json
{
  "error": "ERROR_THIRD_PARTY_FAILED",
  "message": "HERE API request failed",
  "code": 200
}
```

### Monitoring Data (InfluxDB)
```json
{
  "originApi": "GET /api/v2/routes",
  "vendor": "Here",
  "vendorService": "Routing",
  "vendorApi": "https://router.hereapi.com/v8/routes",
  "status": "SUCCESS",
  "duration": 1250,
  "meta": {
    "transportMode": "car",
    "origin": "52.5,13.4",
    "destination": "52.6,13.5"
  }
}
```

## ⚠️ Important Notes

### Transport Mode Options
- **car**: Standard passenger vehicle routing
- **pedestrian**: Walking routes with sidewalks and pedestrian paths
- **bicycle**: Bike-friendly routes and bike lanes
- **truck**: Commercial vehicle routing with restrictions
- **publicTransport**: Public transit with schedules and transfers
- **scooter**: Motorized scooter routing

### Return Mode Parameters
- **summary**: Basic route information (distance, duration)
- **polyline**: Encoded route geometry
- **actions**: Turn-by-turn navigation instructions
- **tollCost**: Toll road costs and payment information
- **elevation**: Route elevation profile
- **instructions**: Detailed navigation guidance

### Monitoring and Alerting
- **InfluxDB Integration**: All requests logged with performance metrics
- **Slack Alerts**: Automatic notifications for API failures
- **Performance Tracking**: Response time and success rate monitoring
- **Error Classification**: Detailed error categorization and reporting

### Configuration Requirements
```javascript
// Required configuration structure
{
  vendor: {
    here: {
      apiKey: 'YOUR_HERE_API_KEY',
      router: 'https://router.hereapi.com'
    },
    project: {
      projectName: 'TSP-API',
      projectStage: 'production'
    },
    slack: {
      token: 'SLACK_BOT_TOKEN',
      channelId: 'CHANNEL_ID'
    }
  },
  database: {
    influx: {
      url: 'INFLUX_DB_URL',
      token: 'INFLUX_TOKEN',
      serviceMonitor: {
        timeout: 5000
      }
    }
  }
}
```

### Performance Considerations
- **Timeout**: 10-second request timeout to prevent hanging
- **Rate Limiting**: Implement batch processing for high-volume requests
- **Caching**: Consider caching frequently requested routes
- **Monitoring**: Track API usage and response times

### Error Handling Best Practices
- **Graceful Degradation**: Handle API failures without breaking application
- **Retry Logic**: Consider implementing retry mechanisms for transient failures
- **Fallback Routes**: Provide alternative routing when primary service fails
- **User Communication**: Clear error messages for user-facing applications

## 🔗 Related File Links

- **HERE Geocoding:** `allrepo/connectsmart/tsp-api/src/services/hereGeocoding.js`
- **HERE Polylines:** `allrepo/connectsmart/tsp-api/src/services/hereMapPolylines.js`
- **Error Codes:** `allrepo/connectsmart/tsp-api/src/static/error-code.js`
- **Route Controllers:** Controllers that use routing functionality

---
*This service provides reliable, enterprise-grade routing functionality with comprehensive monitoring and alerting for production transportation applications.*