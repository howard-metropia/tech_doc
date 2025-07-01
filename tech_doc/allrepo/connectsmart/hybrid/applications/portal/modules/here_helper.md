# HERE Maps Helper Module - ConnectSmart Portal

🔍 **Quick Summary (TL;DR)**
- HERE Maps Routing API integration for calculating travel distances with support for multiple transport modes as primary routing service
- here-maps | routing-api | distance-calculation | transport-modes | route-optimization | api-integration
- Used as primary routing service for trip distance calculations, carpool route planning, and travel optimization in ConnectSmart platform
- Compatible with HERE Routing API v8, requires HERE API key, supports car/bicycle/pedestrian modes with custom return parameters

❓ **Common Questions Quick Index**
- Q: How do I calculate routes with HERE Maps? → See [Usage Methods](#usage-methods)
- Q: What transport modes are available? → See [Technical Specifications](#technical-specifications)
- Q: How does this differ from Google Maps integration? → See [Important Notes](#important-notes)
- Q: What happens when HERE API fails? → See [Output Examples](#output-examples)
- Q: How do I configure return parameters? → See [Usage Methods](#usage-methods)
- Q: What's the API timeout setting? → See [Technical Specifications](#technical-specifications)
- Q: How do I troubleshoot route calculation errors? → See [Output Examples](#output-examples)
- Q: Can I get route polylines and waypoints? → See [Improvement Suggestions](#improvement-suggestions)

📋 **Functionality Overview**
- **Non-technical explanation:** Like having a professional route planner that calculates exact travel distances using HERE's mapping data - it's similar to asking a local taxi dispatcher "what's the best route from A to B" and getting precise distance measurements. Works like a GPS navigation system that focuses on providing accurate distance calculations for different types of transportation.
- **Technical explanation:** HERE Routing API v8 client providing real-world distance calculations with configurable transport modes and return parameters, featuring structured error handling and logging integration.
- **Business value:** Provides primary routing data for accurate trip pricing, enables reliable carpool distance calculations, and supports precise incentive calculations based on actual road network distances.
- **System context:** Serves as the primary routing service in ConnectSmart's distance calculation hierarchy, with Google Maps as fallback, supporting incentive engine and trip validation workflows.

🔧 **Technical Specifications**
- **File info:** `here_helper.py`, 43 lines, Python HERE Maps API client, medium complexity
- **Dependencies:**
  - `requests` (external): HTTP client for API communication (critical dependency)
  - `logging` (built-in): Debug and error logging capabilities
  - `json` (built-in): JSON response parsing and error handling
  - `gluon.current` (Web2py): Framework context for configuration access
- **API configuration:**
  - `base_url`: 'https://router.hereapi.com' (HERE Routing API v8 endpoint)
  - `here.app_key`: HERE API key from application configuration (required)
  - `timeout_duration`: 3 seconds request timeout with custom session handling
- **Transport modes:** car, bicycle, pedestrian, truck, scooter (HERE API standard modes)
- **Return parameters:** configurable via return_mode parameter (summary, polyline, actions, etc.)
- **Output format:** Distance in meters (integer) extracted from route summary
- **Error handling:** HTTP status codes, API-specific error responses, network timeout handling

📝 **Detailed Code Analysis**
```python
def here_routing(origin, destination, transport_mode, return_mode):
    """Calculate route distance using HERE Routing API v8"""
    
    # Configure custom timeout and session for reliability
    timeout = requests.Timeout(timeout_duration)  # 3-second timeout
    session = requests.Session()
    session.timeout = timeout
    
    # HERE Routing API v8 endpoint
    url = base_url + '/v8/routes'
    
    try:
        # API request with HERE-specific parameters
        response = session.get(url, params={
            'apiKey': api_key,              # HERE API authentication
            'origin': origin,               # Start point (lat,lng format)
            'destination': destination,     # End point (lat,lng format)  
            'return': return_mode,          # Response detail level
            'transportMode': transport_mode # Travel method (car, bicycle, etc.)
        })
        
        # Parse JSON response with error detection
        data = json.loads(response.text)
        
        if response.status_code == 200 and data.get('routes'):
            # Extract distance from first route, first section
            distance = data['routes'][0]['sections'][0]['summary']['length']
            logger.debug(
                'distance between {} and {} from here API: {}'.format(
                    origin, destination, distance
                )
            )
            return distance  # Distance in meters
        else:
            # Log API-specific error responses
            logger.warning("failed to get route info from here API")
            logger.warning(json.dumps(data))
            return None
            
    except Exception as e:
        # Handle network errors, timeouts, JSON parsing failures
        logger.warning("failed to fetch here API: {}".format(e))
        return None
```

🚀 **Usage Methods**
```python
from applications.portal.modules.here_helper import here_routing

# Basic route distance calculation
origin = "52.5,13.4"  # Berlin coordinates (lat,lng format)
destination = "48.1,11.6"  # Munich coordinates
distance = here_routing(origin, destination, 'car', 'summary')
print(f"Driving distance: {distance} meters")

# Different transport modes
car_distance = here_routing(origin, destination, 'car', 'summary')
bike_distance = here_routing(origin, destination, 'bicycle', 'summary') 
walk_distance = here_routing(origin, destination, 'pedestrian', 'summary')

# Detailed route information
detailed_route = here_routing(origin, destination, 'car', 'polyline,summary')

# Integration with trip validation system
def calculate_trip_distance(origin_lat, origin_lng, dest_lat, dest_lng, mode='car'):
    origin_coords = f"{origin_lat},{origin_lng}"
    dest_coords = f"{dest_lat},{dest_lng}"
    
    distance = here_routing(origin_coords, dest_coords, mode, 'summary')
    return distance if distance else 0

# Carpool route optimization
def optimize_carpool_route(pickup_points, destination, transport_mode='car'):
    total_distance = 0
    current_location = pickup_points[0]
    
    for next_point in pickup_points[1:] + [destination]:
        segment_distance = here_routing(current_location, next_point, transport_mode, 'summary')
        if segment_distance:
            total_distance += segment_distance
            current_location = next_point
        else:
            return None  # Route calculation failed
    
    return total_distance

# Error handling with fallback
def robust_distance_calculation(origin, dest, mode='car'):
    distance = here_routing(origin, dest, mode, 'summary')
    if distance is None:
        # Could fallback to Google Maps or linear calculation
        logger.warning(f"HERE routing failed for {origin} to {dest}")
        return None
    return distance

# Batch route calculations
def calculate_multiple_routes(route_list):
    results = []
    for origin, destination, mode in route_list:
        distance = here_routing(origin, destination, mode, 'summary')
        results.append({
            'origin': origin,
            'destination': destination, 
            'mode': mode,
            'distance': distance,
            'success': distance is not None
        })
    return results
```

📊 **Output Examples**
```python
# Successful route calculation
>>> here_routing("52.5,13.4", "48.1,11.6", "car", "summary")
584234  # Distance in meters (584.2 km Berlin to Munich)

# Different transport modes comparison
>>> origin, dest = "52.5200,13.4050", "52.5100,13.3900"  # Short Berlin route
>>> here_routing(origin, dest, "car", "summary")
3420  # Car route: 3.42 km
>>> here_routing(origin, dest, "bicycle", "summary") 
2890  # Bicycle route: 2.89 km (more direct)
>>> here_routing(origin, dest, "pedestrian", "summary")
2650  # Walking route: 2.65 km (most direct)

# API success response structure
{
    "routes": [{
        "sections": [{
            "summary": {
                "length": 584234,           # Distance in meters
                "duration": 20125,          # Duration in seconds  
                "baseDuration": 19580       # Duration without traffic
            }
        }]
    }]
}

# Error scenarios
>>> here_routing("invalid", "coordinates", "car", "summary")
[WARNING] failed to get route info from here API
[WARNING] {"error": {"type": "InvalidInputError", "title": "Invalid Input"}}
None

# Network timeout
>>> here_routing(origin, dest, "car", "summary")  # With network issues
[WARNING] failed to fetch here API: ReadTimeout("Request timed out")
None

# API quota exceeded
>>> here_routing(origin, dest, "car", "summary")  # When quota exceeded
[WARNING] failed to get route info from here API
[WARNING] {"error": {"type": "QuotaExceededError", "title": "Usage quota exceeded"}}
None

# Debug logging output
[DEBUG] distance between 52.5,13.4 and 48.1,11.6 from here API: 584234

# No route found scenario
>>> here_routing("0,0", "90,180", "car", "summary")  # Impossible route
[WARNING] failed to get route info from here API
[WARNING] {"error": {"type": "NoRouteFoundError", "title": "No route found"}}
None
```

⚠️ **Important Notes**
- **API key management:** HERE API key should be restricted to specific domains/IPs in HERE Developer Portal
- **Coordinate format:** HERE API expects "lat,lng" string format, differs from Google Maps tuple format
- **Transport mode availability:** Not all transport modes available in all regions (e.g., scooter mode limited)
- **API versioning:** Uses HERE Routing API v8 - future versions may require code updates
- **Rate limiting:** HERE API has request rate limits - implement throttling for high-volume usage
- **Route quality:** HERE Maps particularly strong in Europe and urban areas, coverage varies globally
- **Timeout considerations:** 3-second timeout may be insufficient for complex long-distance routes
- **Primary service:** Used as first choice in distance calculation hierarchy before Google Maps fallback

🔗 **Related File Links**
- **Fallback service:** `google_helper.py` - Google Maps integration used when HERE API fails
- **Primary consumer:** `incentive_helper.py` calls HERE routing for trip distance calculations
- **Configuration source:** Web2py application configuration contains HERE API credentials
- **Distance calculation flow:** HERE → Google Maps → linear distance fallback hierarchy
- **API documentation:** HERE Developer Portal for API key management and documentation
- **Monitoring:** Consider implementing API usage monitoring and error rate tracking

📈 **Use Cases**
- **Primary trip distance calculation:** First choice for calculating actual travel distances in ConnectSmart platform
- **Carpool route optimization:** Calculate efficient multi-stop routes for shared rides
- **Incentive system support:** Provide accurate distance data for environmental impact calculations
- **Trip validation:** Verify user-reported distances against HERE's route calculations
- **Cost calculation:** Enable fair pricing based on actual route distances rather than straight-line distances
- **Route planning features:** Support advanced trip planning with detailed route information
- **Analytics and reporting:** Generate precise travel statistics for mobility program analysis

🛠️ **Improvement Suggestions**
- **Response caching:** Implement caching layer to reduce API costs for frequently requested routes
- **Parallel processing:** Add async support for batch route calculations to improve performance
- **Enhanced return modes:** Support polyline, actions, and turn-by-turn directions for advanced features
- **Traffic integration:** Enable real-time traffic data for more accurate travel time estimates
- **Route alternatives:** Return multiple route options with different distance/time characteristics
- **Waypoint support:** Add support for complex multi-stop routing scenarios
- **Error categorization:** Implement specific error handling for different HERE API error types
- **API monitoring:** Add structured logging and metrics for API performance and reliability tracking

🏷️ **Document Tags**
- **Keywords:** here-maps-api, routing-api, distance-calculation, transport-modes, route-optimization, primary-routing-service, api-integration, travel-distance, carpool-routing, trip-validation
- **Technical tags:** `#here-maps` `#routing-api` `#distance-calculation` `#transport-modes` `#api-client` `#route-optimization` `#portal` `#primary-service`
- **Target roles:** Backend developers (intermediate), GIS specialists, routing system developers, API integrators
- **Difficulty level:** ⭐⭐ (intermediate) - Requires HERE API setup, understanding of routing concepts, and error handling
- **Maintenance level:** Medium - API key management, service monitoring, version compatibility tracking
- **Business criticality:** High - primary routing service affecting all distance-based calculations and pricing
- **Related topics:** routing optimization, geolocation services, distance calculation, API integration, mobility analytics, transport planning