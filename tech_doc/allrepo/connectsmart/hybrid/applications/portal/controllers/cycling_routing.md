# Cycling Routing Controller API Documentation

## Overview
The Cycling Routing Controller provides bicycle route planning and navigation services for the MaaS platform. It integrates with external routing services to deliver optimized cycling paths, supporting eco-friendly transportation options within the mobility ecosystem.

**File Path:** `/allrepo/connectsmart/hybrid/applications/portal/controllers/cycling_routing.py`

**Controller Type:** Authenticated Portal Controller

**Authentication:** JWT token required

## Features
- Bicycle-specific route calculation
- Integration with external routing services
- Waypoint management and optimization
- Real-time route planning
- Origin and destination coordinates handling
- Error resilience and fallback mechanisms

## API Endpoints

### Cycling Route Planning
**Endpoint:** `/cycling_routing/path`
**Methods:** POST
**Authentication:** JWT token required

#### POST - Calculate Cycling Route
Calculates optimized cycling routes between origin and destination points.

**Required Fields:**
- `origin`: Object containing origin coordinates
  - `latitude`: Starting point latitude
  - `longitude`: Starting point longitude
- `destination`: Object containing destination coordinates
  - `latitude`: Ending point latitude
  - `longitude`: Ending point longitude

**Request Example:**
```json
{
  "origin": {
    "latitude": 25.0330,
    "longitude": 121.5654
  },
  "destination": {
    "latitude": 25.0478,
    "longitude": 121.5173
  }
}
```

**Response Format:**
```json
{
  "success": true,
  "data": [
    {
      "waypoints": [
        [25.0330, 121.5654],
        [25.0350, 121.5600],
        [25.0400, 121.5500],
        [25.0450, 121.5300],
        [25.0478, 121.5173]
      ],
      "distance": 5.2,
      "duration": 18.5,
      "elevation_gain": 45,
      "difficulty": "moderate"
    }
  ]
}
```

**Status Codes:**
- `200`: Success with route data
- `400`: Invalid parameters
- `500`: Routing service error

## Route Calculation Process

### Request Processing
1. **Parameter Extraction**: Extract origin and destination coordinates
2. **Service Integration**: Format request for external routing service
3. **Route Calculation**: Query routing service with bicycle parameters
4. **Waypoint Processing**: Add origin and destination to route waypoints
5. **Response Formatting**: Structure data for client consumption

### External Service Integration
```python
def calculate_route():
    params = {
        'o': "{},{}".format(origin['latitude'], origin['longitude']),
        'd': "{},{}".format(destination['latitude'], destination['longitude'])
    }
    formatted_url = routing_service_url + '/path?' + query_params
    response = requests.get(url=formatted_url, params=params)
```

## Data Model

### Request Structure
```python
{
    "origin": {
        "latitude": float,          # Starting point latitude
        "longitude": float          # Starting point longitude
    },
    "destination": {
        "latitude": float,          # Ending point latitude
        "longitude": float          # Ending point longitude
    }
}
```

### Route Response Structure
```python
{
    "waypoints": [                  # Array of coordinate pairs
        [latitude, longitude],      # Origin point
        [latitude, longitude],      # Intermediate waypoints
        [latitude, longitude]       # Destination point
    ],
    "distance": float,              # Total distance in kilometers
    "duration": float,              # Estimated time in minutes
    "elevation_gain": int,          # Total elevation gain in meters
    "difficulty": str               # Route difficulty level
}
```

## Configuration

### Routing Service Configuration
```python
routing_service_url = configuration.get("routing.url")
```

**Configuration Parameters:**
- `routing.url`: Base URL for external routing service
- Service timeout settings
- API authentication credentials
- Route calculation parameters

## Authentication & Security

### JWT Authentication
- `@auth.allows_jwt()`: Enables JWT token authentication
- `@jwt_helper.check_token()`: Validates token integrity
- User session validation for route requests

### Security Features
- Input validation for coordinate parameters
- Rate limiting for routing requests
- Secure communication with external services

## Implementation Details

### Waypoint Management
The system automatically manages route waypoints:
1. **Origin Addition**: Prepends origin coordinates to route
2. **Destination Addition**: Appends destination coordinates to route
3. **Path Optimization**: External service provides intermediate waypoints
4. **Coordinate Validation**: Ensures valid geographic coordinates

### Error Handling
```python
try:
    data = resp.json()['data']
    for path in data:
        path['waypoints'].insert(0, (origin['latitude'], origin['longitude']))
        path['waypoints'].append((destination['latitude'], destination['longitude']))
except Exception as e:
    logger.error(e)
    # Fallback to basic waypoint structure
    data = {
        'waypoints': [
            (origin['latitude'], origin['longitude']),
            (destination['latitude'], destination['longitude'])
        ]
    }
```

### Fallback Mechanism
When routing service fails:
- Returns basic direct route with origin and destination
- Logs error for debugging and monitoring
- Provides minimal viable route data
- Maintains API contract with clients

## External Service Integration

### Routing Service API
- **Method**: GET request with query parameters
- **Parameters**: Origin and destination coordinates
- **Response**: JSON with route data and waypoints
- **Timeout**: Configurable request timeout
- **Retry Logic**: Basic error handling and fallback

### Service Requirements
- Geographic coordinate support
- Bicycle-specific routing algorithms
- JSON response format
- RESTful API design
- Reliable uptime and performance

## Performance Optimization

### Request Optimization
- Efficient parameter formatting
- Minimal data transfer
- Cached routing configurations
- Connection pooling for external requests

### Response Optimization
- Streamlined waypoint processing
- Efficient coordinate array handling
- Minimal JSON payload size
- Fast response formatting

## Usage Examples

### Calculate Cycling Route
```bash
curl -X POST /cycling_routing/path \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": {
      "latitude": 25.0330,
      "longitude": 121.5654
    },
    "destination": {
      "latitude": 25.0478,
      "longitude": 121.5173
    }
  }'
```

### Response Example
```json
{
  "success": true,
  "data": [
    {
      "waypoints": [
        [25.0330, 121.5654],
        [25.0335, 121.5640],
        [25.0340, 121.5620],
        [25.0478, 121.5173]
      ]
    }
  ]
}
```

## Integration Points

### Mobile Applications
- Real-time navigation and turn-by-turn directions
- Route visualization on maps
- Offline route caching capabilities
- Integration with GPS tracking

### Multi-Modal Planning
- Combination with other transportation modes
- Transit connection points
- Park-and-ride facility integration
- Last-mile connectivity solutions

### Mapping Services
- Integration with HERE Maps, Google Maps, or OpenStreetMap
- Custom cycling lane data overlay
- Real-time traffic and construction updates
- Points of interest along routes

## Cycling-Specific Features

### Route Optimization Factors
- **Bike Lanes**: Preference for dedicated cycling infrastructure
- **Traffic Volume**: Avoidance of high-traffic roads
- **Elevation**: Consideration of hills and terrain difficulty
- **Safety**: Prioritization of safer cycling routes
- **Scenery**: Optional scenic route preferences

### Environmental Considerations
- **Weather Integration**: Route adjustments for weather conditions
- **Seasonal Factors**: Different routes for different seasons
- **Surface Types**: Preference for paved vs. unpaved paths
- **Lighting**: Consideration for day/night cycling safety

## Error Handling and Resilience

### Service Failure Recovery
```python
if routing_service_unavailable:
    # Provide direct line route as fallback
    fallback_route = create_direct_route(origin, destination)
    return fallback_route
```

### Error Logging
- Comprehensive error logging for debugging
- External service response monitoring
- Performance metrics tracking
- User experience impact assessment

## Monitoring and Analytics

### Key Metrics
- Route calculation success rates
- Average response times
- External service availability
- User route preferences and patterns

### Performance Monitoring
- API endpoint response times
- External service dependency health
- Error rate tracking
- Geographic usage patterns

## Future Enhancements

### Planned Features
- **Real-time Traffic**: Integration with cycling traffic data
- **Weather Integration**: Weather-aware route planning
- **Community Routes**: User-generated popular cycling routes
- **Safety Scoring**: Route safety assessment and scoring

### Advanced Capabilities
- **Multi-stop Routing**: Support for multiple waypoints
- **Route Variants**: Multiple route options with different characteristics
- **Accessibility Features**: Routes suitable for different cycling abilities
- **Environmental Impact**: Carbon footprint calculations for routes

## Troubleshooting

### Common Issues
1. **External Service Timeouts**: Check routing service availability
2. **Invalid Coordinates**: Validate latitude/longitude ranges
3. **Empty Route Responses**: Verify service configuration
4. **Waypoint Processing Errors**: Check coordinate format consistency

### Debug Strategies
- Log external service requests and responses
- Monitor routing service uptime and performance
- Validate coordinate input ranges and formats
- Test fallback mechanisms regularly