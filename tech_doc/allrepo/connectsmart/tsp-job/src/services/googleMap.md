# Google Maps Service

## Overview

The Google Maps service provides integrated access to Google Maps APIs with built-in monitoring, error handling, and performance tracking through InfluxDB metrics collection.

## Service Information

- **Service Name**: Google Maps
- **File Path**: `/src/services/googleMap.js`
- **Type**: External API Integration Service
- **Dependencies**: Google Maps Services JS Client, InfluxDB

## Configuration

### API Setup
- **Client**: Google Maps Services JavaScript Client
- **Timeout**: 3000ms for API requests
- **Authentication**: API key from vendor.google.maps config

### Monitoring Integration
- **InfluxDB**: Service performance monitoring
- **Metrics**: Request duration, success/failure rates
- **Timeout**: Configurable monitoring timeout

## Functions

### directions(inputs)

Provides Google Maps Directions API integration with monitoring.

**Purpose**: Calculates routes between locations with comprehensive monitoring
**Parameters**:
- `inputs` (object): Direction request parameters (origin, destination, mode, etc.)

**Returns**: Google Maps Directions API response data

**API Parameters**:
- Merges input parameters with API key
- Supports all standard Google Directions API options
- 3-second timeout for requests

**Example**:
```javascript
const inputs = {
  origin: "Seattle, WA",
  destination: "Portland, OR",
  mode: "driving",
  departure_time: "now"
};
const result = await directions(inputs);
// Returns: Google Directions API response with routes
```

## Monitoring Integration

### InfluxDB Metrics
- **Measurement**: Service performance tracking
- **Origin API**: "tsp-job googleMap service"
- **Vendor**: "Google"
- **Service**: "Directions"
- **Endpoint**: "maps/api/directions/json"

### Success Metrics
- **Status**: "SUCCESS"
- **Duration**: Request processing time
- **Metadata**: Stringified input parameters
- **Timestamp**: Automatic metric timestamp

### Error Metrics
- **Status**: "ERROR"
- **Duration**: Time until error occurrence
- **Error Message**: Exception details
- **Metadata**: Original request parameters

## Error Handling

### API Failures
- Comprehensive error logging
- InfluxDB error metric recording
- Graceful error propagation
- Request metadata preservation

### Timeout Management
- 3-second request timeout
- Automatic timeout error handling
- Duration tracking until timeout
- Monitoring of timeout frequency

### Exception Handling
- Catches and logs all API exceptions
- Preserves original error messages
- Maintains service availability
- Error context preservation

## Technical Details

### Google Maps Integration
- Uses official Google Maps Services JS client
- Supports full Directions API feature set
- Automatic API key injection
- Standard REST API communication

### Performance Monitoring
- Request start time tracking
- End-to-end duration measurement
- Success/failure rate calculation
- API response time analysis

### Configuration Management
- Environment-based API key loading
- Configurable timeout settings
- InfluxDB connection management
- Vendor-specific configuration

## Integration Points

### Used By
- Route planning services
- Trip optimization algorithms
- Navigation assistance features
- Travel time estimation

### External Dependencies
- **Google Maps Directions API**: Route calculation
- **InfluxDB**: Performance monitoring
- **@googlemaps/google-maps-services-js**: Official client library
- **@maas/services**: InfluxDB manager

## API Features

### Directions API Support
- **Route Calculation**: Optimal path finding
- **Travel Modes**: Driving, walking, transit, cycling
- **Traffic Conditions**: Real-time traffic integration
- **Alternative Routes**: Multiple route options
- **Waypoints**: Multi-stop route planning

### Request Flexibility
- Dynamic parameter passing
- All Google Directions API parameters supported
- Custom request configuration
- Flexible input handling

## Performance Considerations

- **Timeout Control**: 3-second maximum request time
- **Connection Pooling**: Efficient HTTP client usage
- **Monitoring Overhead**: Minimal performance impact
- **Error Recovery**: Fast failure detection

## Security Considerations

- **API Key Management**: Secure configuration loading
- **Request Validation**: Input parameter validation
- **Error Information**: Filtered sensitive data logging
- **Rate Limiting**: Handled by Google's API limits

## Usage Guidelines

1. **Input Validation**: Ensure valid origin/destination formats
2. **Error Handling**: Always handle potential API failures
3. **Monitoring**: Check InfluxDB metrics for API health
4. **Rate Limits**: Respect Google Maps API quotas
5. **Timeout Handling**: Plan for 3-second maximum response time

## Dependencies

- **@googlemaps/google-maps-services-js**: Official Google Maps client
- **@maas/services**: InfluxDB manager for monitoring
- **Config**: Application configuration management
- **@maas/core/log**: Centralized logging system