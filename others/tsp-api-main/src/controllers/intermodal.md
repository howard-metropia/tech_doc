# TSP API Intermodal Transportation Controller Documentation

## 🔍 Quick Summary (TL;DR)
The intermodal controller is a comprehensive multimodal trip planning engine that integrates public transit, walking, cycling, driving, and shared mobility options to provide optimal route suggestions across Houston and Taiwan regions.

**Keywords:** intermodal | multimodal-planning | trip-planner | public-transit | route-optimization | transportation-integration | mobility-as-a-service | here-api | gtfs | shared-mobility

**Primary use cases:** Cross-modal trip planning, public transit routing, shared bike integration, park-and-ride coordination

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, HERE Technologies API, Google Maps API

## ❓ Common Questions Quick Index
- **Q: How do I plan a multimodal trip?** → [Intermodal Planning](#intermodal-planning-get-intermodal)
- **Q: What regions are supported?** → Houston and Taiwan with fallback to HERE API
- **Q: How does shared bike integration work?** → Bcycle (Houston) and YouBike (Taiwan) integration
- **Q: What transit modes are available?** → Bus, light rail, subway, ferry, high-speed rail
- **Q: How are real-time updates handled?** → Houston Metro real-time integration
- **Q: What mapping services are used?** → HERE Technologies and Google Maps APIs
- **Q: How does park-and-ride work?** → Automated parking lot finding and route integration

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **super-smart travel assistant** that knows every way to get around a city. When you say "get me from point A to point B," it considers buses, trains, walking, biking, driving, ride-sharing, and even combinations like "drive to a park-and-ride lot, then take the train." It's like having a local transportation expert who knows real-time conditions, bike-share locations, and optimal connections.

**Technical explanation:** 
A sophisticated intermodal transportation planning controller that integrates multiple routing engines, real-time data sources, and mobility services. It orchestrates calls to internal routing engines for Houston/Taiwan and falls back to HERE API for other regions, while incorporating shared mobility options, real-time transit data, fare information, and geospatial processing.

**Business value explanation:**
Core functionality for comprehensive mobility-as-a-service platforms, enabling seamless multimodal transportation that reduces car dependency, optimizes travel efficiency, and integrates various transportation options into unified user experiences.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/intermodal.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** Complex Integration Controller
- **File Size:** ~63 KB
- **Complexity Score:** ⭐⭐⭐⭐⭐ (Very High - Multi-service integration, real-time processing, geospatial operations)

**Key Dependencies:**
- **Routing Engines:** Internal Houston/Taiwan engines + HERE Transit API
- **Mapping Services:** HERE Technologies, Google Maps
- **Real-time Data:** Houston Metro, Taiwan transit feeds
- **Shared Mobility:** Bcycle, YouBike services
- **Geospatial:** Turf.js, geo-tz for timezone calculations
- **Monitoring:** InfluxDB, Slack notifications

**Supported Regions:**
- **Houston:** Full engine integration with real-time bus data
- **Taiwan:** Complete transit system with shared bike integration  
- **Global:** HERE API fallback for other locations

## 📝 Detailed Code Analysis

### Main Endpoint (`GET /intermodal`)

**Core Processing Flow:**
1. **Geographic Detection:** Determines if origin/destination are in Houston or Taiwan
2. **Parameter Processing:** Configures transit modes, speeds, and regional settings
3. **Engine Routing:** Calls appropriate routing engine or HERE API
4. **Enhancement Pipeline:** Adds shared bikes, parking, real-time data, fare information
5. **Response Formatting:** Converts to standardized mobile app format

**Regional Configurations:**
```javascript
// Houston Configuration
area = 'houston';
param_cost = 0.5; param_time = 0.5;
transit = 'citybus,lightrail';
vot = '15.0,30.0,20.0,5.0,50.0';

// Taiwan Configuration  
area = 'tw';
param_cost = 0; param_time = 1.0;
transit = 'bus,subway,rail,ferry,highspeedrail';
vot = '160.0,200.0,200.0,100.0,400.0';
```

**Shared Mobility Integration:**
- **Houston Bcycle:** Automated bike-share station integration with route optimization
- **Taiwan YouBike:** Real-time bike availability with first/last mile integration
- **Park & Ride:** Automatic parking lot detection and route enhancement

**Real-time Features:**
- **Houston Metro:** Live bus positions and arrival predictions
- **Traffic Conditions:** Real-time traffic integration via HERE API
- **Service Alerts:** Transit disruption notifications

## 🚀 Usage Methods

### Basic Multimodal Trip Planning
```bash
curl -X GET "https://api.tsp.example.com/api/v2/intermodal" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "zone: America/Chicago" \
  -G \
  -d "origin=29.7604,-95.3698" \
  -d "destination=29.7749,-95.3628" \
  -d "departure=2024-06-25T15:30:00+00:00" \
  -d "private=walking,bicycling,driving" \
  -d "transit=citybus,lightrail" \
  -d "transfer=2,10" \
  -d "originName=Downtown" \
  -d "destinationName=Medical Center"
```

### Advanced Options with Shared Mobility
```bash
curl -X GET "https://api.tsp.example.com/api/v2/intermodal" \
  -G \
  -d "origin=25.0330,121.5654" \
  -d "destination=25.0478,121.5318" \
  -d "departure=2024-06-25T08:00:00+00:00" \
  -d "private=walking,bicycling,bikeshare" \
  -d "transit=subway,bus" \
  -d "walkingSpeed=3" \
  -d "cyclingSpeed=16"
```

## 📊 Output Examples

### Successful Multimodal Route
```json
{
  "result": "success",
  "data": {
    "routes": [
      {
        "total_travel_time": 1800,
        "total_travel_meters": 12500,
        "total_price": 3.50,
        "sections": [
          {
            "type": "pedestrian",
            "departure": {
              "time": "2024-06-25T15:30:00",
              "place": {"name": "Downtown"}
            },
            "arrival": {
              "time": "2024-06-25T15:35:00", 
              "place": {"name": "Metro Station"}
            },
            "travelSummary": {"duration": 300, "length": 400}
          },
          {
            "type": "transit",
            "transport": {
              "mode": "Bus",
              "name": "82",
              "fare": 1.25,
              "is_ticket": 1
            },
            "departure": {
              "time": "2024-06-25T15:38:00",
              "place": {"name": "Downtown Transit Center"}
            },
            "arrival": {
              "time": "2024-06-25T15:55:00",
              "place": {"name": "Medical Center"}
            }
          }
        ]
      }
    ]
  }
}
```

### Regional Fallback Response
```json
{
  "result": "success", 
  "data": {
    "routes": [],
    "message": "No routes found for this region, HERE API used as fallback"
  }
}
```

## ⚠️ Important Notes

### Performance Optimization
- **Caching Strategy:** Route caching for frequently requested origin-destination pairs
- **Parallel Processing:** Concurrent API calls to multiple services
- **Fallback Handling:** Graceful degradation when primary engines fail
- **Rate Limiting:** Built-in API call limiting to prevent quota exhaustion

### Geographic Boundaries
```javascript
// Houston Area (Lat/Lng boundaries)
houston: {
  lat: [28.937417, 30.626585],
  lng: [-96.336375, -94.221907]
}

// Taiwan Area  
taiwan: {
  lat: [21.88, 25.32],
  lng: [118, 122]
}
```

### Error Handling & Monitoring
- **Slack Integration:** Real-time error notifications to operations teams
- **InfluxDB Metrics:** Performance monitoring and API usage tracking
- **Graceful Degradation:** Fallback to alternative routing when primary services fail

### Real-time Considerations
- **5-minute Window:** Real-time bus data used for departures within ±5 minutes
- **Timezone Handling:** Automatic timezone detection and conversion
- **Service Alerts:** Integration with transit agency alert systems

### Integration Complexity
This controller manages one of the most complex integration scenarios in the platform:
- 15+ external API integrations
- Real-time data processing from multiple sources
- Geospatial calculations and route optimization
- Multi-language support (English, Chinese)
- Currency and fare handling across regions

## 🔗 Related File Links

- **Services:** Multiple service files for routing, formatting, real-time data
- **Configuration:** Regional engine configurations and API keys
- **Models:** Transit data models and shared mobility schemas
- **Middleware:** Authentication and API key validation

---
*This controller represents the core multimodal transportation planning capability of the TSP platform.*