# test-mock-weather.js

## Overview
Comprehensive test suite for the mock weather service in the TSP API. Tests weather alert management, forecast updates, grid-based geographic lookups, and weather impact assessment functionality.

## File Location
`/test/test-mock-weather.js`

## Dependencies
- **chai**: BDD/TDD assertion library with promise support
- **chai-as-promised**: Promise-based assertions
- **sinon**: Test spies, stubs, and mocks
- **moment**: Date/time manipulation
- **Models**: WeatherCriticalAlert, WeatherGrids, WeatherForecastCurrent
- **Service**: mockWeather service

## Service Under Test
```javascript
const mockWeather = require('@app/src/services/mockWeather');
```

## Database Models

### WeatherCriticalAlert
```javascript
{
  alert_id: string,
  startAt: ISO_DATE_STRING,
  endAt: ISO_DATE_STRING,
  impactedArea: string,
  event_type: string,
  event_description: string,
  event_status: string
}
```

### WeatherForecastCurrent
```javascript
{
  _id: string,
  grid_id: string,
  start_at: moment,
  end_at: moment,
  windSpeed: number,
  rain: number,
  is_impacted: boolean,
  events: object || null
}
```

### WeatherGrids
```javascript
{
  grid_id: string,
  latitude: number,
  longitude: number,
  geometry: {
    type: 'Polygon',
    coordinates: array
  }
}
```

## Test Suites

### 1. Alert Management (mockAlert)

#### Create Alert
**Function**: `mockWeather.createAlert(mockData)`

**Test Cases**:
1. **Successful Creation**:
   ```javascript
   const mockData = {
     data: {
       startAt: '2023-04-01T00:00:00Z',
       endAt: '2023-04-02T00:00:00Z',
       impactedArea: 'Test Area'
     }
   };
   ```
   - Returns alert ID with prefix 'mock.alert.'
   - Stubs WeatherCriticalAlert.prototype.save()

2. **Save Failure Handling**:
   - Database save operation fails
   - Returns proper error: "Error saving mock alert: Save failed"

#### Get Alert
**Function**: `mockWeather.getAlert(alertId)`

**Test Cases**:
1. **Successful Retrieval**:
   - Returns alert object for valid ID
   - Uses WeatherCriticalAlert.findOne()

2. **Alert Not Found**:
   - Returns null for non-existent alert
   - Handles missing data gracefully

3. **Database Error**:
   - Throws formatted error with alert ID
   - Error format: "Failed to get alert:{id} due to {error}"

#### Update Alert
**Function**: `mockWeather.updateAlert(alertId, mockData)`

**Test Cases**:
1. **Successful Update**:
   ```javascript
   const mockData = {
     data: {
       startAt: '2023-04-03T00:00:00Z',
       endAt: '2023-04-04T00:00:00Z',
       impactedArea: 'Updated Area'
     }
   };
   ```
   - Uses WeatherCriticalAlert.findOneAndUpdate()
   - Returns updated alert object

2. **Alert Not Found**:
   - Returns null for non-existent alert
   - No error thrown for missing data

#### Delete Alert
**Function**: `mockWeather.deleteAlert(alertId)`

**Test Cases**:
1. **Successful Deletion**:
   - Returns true when deletedCount = 1
   - Uses WeatherCriticalAlert.deleteOne()

2. **Alert Not Found**:
   - Returns false when deletedCount = 0
   - Indicates unsuccessful deletion

### 2. Forecast Management (mockForecast)

#### Update Forecast
**Function**: `mockWeather.updateForecast(mockData)`

**Weather Impact Logic**:
```javascript
// High impact conditions
windSpeed: 30, rain: 10 → is_impacted: true

// Low impact conditions  
windSpeed: 5, rain: 0 → is_impacted: false, events: null
```

**Test Cases**:
1. **High Impact Weather**:
   - Updates forecast with impact flag
   - Maintains existing events data

2. **Low Impact Weather**:
   - Sets is_impacted to false
   - Clears events array (sets to null)
   - Removes previous impact status

#### Get Forecast
**Function**: `mockWeather.getForecast(gridId)`

**Response Structure**:
```javascript
[
  {
    _id: 'forecast1',
    grid_id: 'grid123',
    start_at: moment,
    end_at: moment,
    is_impacted: true,
    events: {
      event_id: 'event1',
      event_type: 'event_type1',
      event_start_at: moment,
      event_end_at: moment,
      event_impacted_area: 'impacted_area1',
      event_description: 'event_description1',
      event_status: 'event_status1'
    }
  }
]
```

**Test Cases**:
1. **Successful Retrieval**:
   - Returns array of forecast objects
   - Includes both impacted and non-impacted forecasts
   - Uses specific field selection

2. **No Forecasts Found**:
   - Returns empty array
   - No error for missing data

3. **Database Error**:
   - Throws formatted error with grid ID
   - Error format: "Failed to get forecast:{gridId} due to {error}"

### 3. Geographic Grid System

#### Find Grid by Coordinates
**Function**: `mockWeather.findGridByCoordinates(latitude, longitude)`

**Geographic Lookup**:
```javascript
// Example coordinates (New York City)
latitude: 40.7128
longitude: -74.006
```

**Grid Response**:
```javascript
{
  grid_id: 'grid123',
  latitude: 40.7128,
  longitude: -74.006,
  geometry: {
    type: 'Polygon',
    coordinates: [[[longitude, latitude], ...]]
  }
}
```

**Test Cases**:
1. **Successful Grid Lookup**:
   - Returns grid object for valid coordinates
   - Includes geometry polygon data
   - Uses WeatherGrids.findOne()

2. **Grid Not Found**:
   - Returns null for coordinates outside coverage
   - No error for missing grid

3. **Database Error**:
   - Throws formatted error with coordinates
   - Error format: "Failed to search grid: (lat, lng) {error}"

## Testing Patterns

### Stubbing Strategy
```javascript
// Model method stubbing
const saveStub = sinon.stub(WeatherCriticalAlert.prototype, 'save').resolves();

// Query chain stubbing
const execStub = sinon.stub().resolves(result);
sinon.stub(Model, 'findOneAndUpdate').returns({ exec: execStub });

// Field selection stubbing
const selectStub = sinon.stub().returns(data);
sinon.stub(Model, 'find').returns({ select: selectStub });
```

### Error Handling
- **Database Failures**: All methods handle database errors gracefully
- **Missing Data**: Returns null/empty arrays instead of errors
- **Formatted Errors**: Consistent error message formatting with context

### Cleanup
```javascript
afterEach(() => {
  Model.method.restore();
});
```

## Weather Impact Assessment

### Impact Criteria
- **Wind Speed**: High wind affects transportation safety
- **Rainfall**: Heavy rain impacts visibility and road conditions
- **Combined Factors**: Multiple weather conditions increase impact

### Impact Flags
- **is_impacted**: Boolean flag for weather impact
- **events**: Associated weather events (null when no impact)

## Geographic Coverage

### Grid System
- **Coordinate-Based**: Latitude/longitude coordinate system
- **Polygon Areas**: Each grid covers specific geographic polygon
- **Forecast Association**: Each grid has associated weather forecasts

### Use Cases
- **Location-Based Alerts**: Weather alerts for specific areas
- **Route Planning**: Weather-aware transportation routing
- **Real-Time Updates**: Current weather impact on transportation

## Business Logic

### Weather Service Integration
- **Mock Service**: Testing environment weather simulation
- **Alert System**: Critical weather alert management
- **Forecast Updates**: Real-time weather condition updates
- **Geographic Targeting**: Location-specific weather data

### Transportation Impact
- **Route Optimization**: Weather-aware route planning
- **Safety Alerts**: Critical weather condition notifications
- **Service Adjustments**: Transportation service modifications

## Integration Points

### External Weather APIs
- **Mock Implementation**: Simulates real weather service integration
- **Alert Processing**: Handles weather alert lifecycle
- **Data Transformation**: Converts weather data to internal format

### Internal Systems
- **User Notifications**: Weather alerts sent to affected users
- **Route Planning**: Weather data integrated into routing decisions
- **Service Management**: Weather impacts on transportation services

## Error Resilience

### Graceful Degradation
- **Service Continuation**: System continues when weather data unavailable
- **Default Behavior**: Falls back to non-weather-aware operations
- **User Communication**: Clear error messages for weather service issues

This test suite ensures the mock weather service accurately simulates weather alert management, forecast processing, and geographic weather data integration for the TSP API's weather-aware transportation features.