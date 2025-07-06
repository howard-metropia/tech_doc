# test-WeatherService.js

## Overview
Comprehensive test suite for the weather service in the TSP API. Tests weather data integration, route-based weather analysis, AI-powered weather messaging, and geographic weather grid processing.

## File Location
`/test/test-WeatherService.js`

## Dependencies
- **chai**: BDD/TDD assertion library
- **sinon**: Test spies, stubs, and mocks
- **moment-timezone**: Date/time manipulation with timezone support
- **axios**: HTTP client for external API calls
- **Models**: AppDatas, WeatherGridRegionCode
- **Service**: weather service

## Service Under Test
```javascript
const weatherService = require('@app/src/services/weather');
```

## Test Suites

### 1. Time Zone Management

#### getCurrentTimeZone
**Function**: `weatherService.getCurrentTimeZone(userId)`

**Test Cases**:
1. **Successful Time Zone Calculation**:
   ```javascript
   const mockResult = {
     local_time: '2023-04-15T12:00:00Z',
     gmt_time: '2023-04-15T10:00:00Z'
   };
   // Returns time zone offset: 2 hours
   ```
   - Calculates timezone offset between local and GMT time
   - Uses AppDatas model for user-specific time data

2. **Error Handling**:
   - Returns 0 when database error occurs
   - Graceful fallback for missing user data

### 2. Travel Mode Translation

#### getTravelMode
**Function**: `weatherService.getTravelMode(modeId)`

**Test Case**:
```javascript
const result = weatherService.getTravelMode(1);
expect(result).to.equal('driving');
```

**Mode Mapping**:
- Mode 1: 'driving'
- Other modes: walking, transit, cycling, etc.

### 3. Route Weather Grid Processing

#### getGridsofRoutes
**Function**: `weatherService.getGridsofRoutes(routes)`

**Input Structure**:
```javascript
const mockRoutes = [
  {
    departure_time: 1618483200,
    arrival_time: 1618486800,
    decodeRoutes: [[[0, 0], [1, 1]]],
    travel_mode: 1
  }
];
```

**Weather Grid Response**:
```javascript
const mockGrids = [
  {
    grid_id: 'grid1',
    city_tag: 'City1',
    county_tag: 'County1',
    weather: {
      is_impacted: true,
      start_at: new Date(1618483200000),
      end_at: new Date(1618486800000),
      updated_at: new Date(),
      update_frequency_in_minute: 60,
      events: { 
        indicators: {}, 
        categories: [] 
      }
    }
  }
];
```

**Test Functionality**:
- Processes route coordinates to find weather grids
- Associates weather data with route segments
- Returns routes enhanced with grid weather information

### 4. Weather Data Expiration

#### getLastExpireTime
**Function**: `weatherService.getLastExpireTime(route)`

**Test Scenario**:
```javascript
const mockRoute = {
  grids: [
    {
      updated_at: '2023-04-15T10:00:00Z',
      update_frequency_in_minute: 60
    },
    {
      updated_at: '2023-04-15T11:00:00Z',
      update_frequency_in_minute: 30
    }
  ]
};
```

**Logic**:
- Calculates expiration time for each weather grid
- Returns earliest expiration time across all grids
- Format: Unix timestamp (updated_at + frequency)

### 5. Weather Information Processing

#### getWeatherInfo
**Function**: `weatherService.getWeatherInfo(route, timezoneOffset)`

**Input Route with Weather Grids**:
```javascript
const mockRoute = {
  grids: [
    {
      start_at: '2023-04-15T10:00:00Z',
      end_at: '2023-04-15T12:00:00Z',
      city_tag: 'City1',
      events: {
        indicators: { windSpeed: 30 },
        categories: [2]
      }
    },
    {
      start_at: '2023-04-15T11:00:00Z',
      end_at: '2023-04-15T13:00:00Z',
      county_tag: 'County2',
      events: {
        indicators: { rain: 15 },
        categories: []
      }
    }
  ],
  travel_mode: 1
};
```

**Weather Event Translation**:
- **Wind Speed 30**: Translates to 'strong wind'
- **Rain 15**: Translates to 'heavy shower'
- **Categories**: Numeric codes for weather event types

**Output Structure**:
```javascript
[
  {
    eventTypeSet: ['strong wind'],
    // Additional weather info...
  },
  {
    eventTypeSet: ['heavy shower'],
    // Additional weather info...
  }
]
```

### 6. AI Weather Messaging

#### getAIMessage
**Function**: `weatherService.getAIMessage(eventInfos, language, tripInfo, context)`

**Test Parameters**:
```javascript
const mockEventInfos = [{ msg: 'Weather event info' }];
const mockTripInfo = {
  currentLocalTime: '2023-04-15 10:00',
  destination: 'New York',
  departureTime: '2023-04-15 11:00',
  travelMode: 'driving'
};
```

**AI Integration**:
- Uses axios to call external AI service
- Processes weather events into natural language messages
- Context-aware messaging (trip_planning, alerts, etc.)

**Response Processing**:
```javascript
const response = {
  data: {
    choices: [{ 
      message: { 
        content: 'AI-generated weather warning' 
      } 
    }]
  }
};
```

## Weather Event Classification

### Indicators
- **windSpeed**: Wind speed in mph/kmh
- **rain**: Rainfall amount
- **temperature**: Temperature readings
- **visibility**: Visibility distance

### Categories
- **Numeric Codes**: Weather event type identifiers
- **Event Types**: Strong wind, heavy shower, fog, etc.
- **Severity Levels**: Different thresholds for impact

## Geographic Integration

### Weather Grids
- **Grid System**: Geographic areas with weather coverage
- **Coordinate Mapping**: Routes mapped to weather grid coverage
- **Regional Data**: City and county-level weather information

### Route Processing
- **Coordinate Decoding**: Route polylines decoded to coordinates
- **Grid Intersection**: Determines which grids affect route
- **Time-based Filtering**: Weather events during travel time

## Time-based Weather Logic

### Travel Time Windows
- **Departure Time**: When journey begins
- **Arrival Time**: When journey ends
- **Weather Windows**: Weather events during travel period

### Update Frequency
- **Grid-specific**: Each grid has its own update frequency
- **Expiration Tracking**: Determines when weather data becomes stale
- **Real-time Updates**: Fresh weather data for accurate predictions

## AI Integration Features

### Natural Language Generation
- **Context Awareness**: Trip planning vs. emergency alerts
- **Language Support**: Multiple language weather messages
- **Personalization**: User-specific travel information

### Message Types
- **trip_planning**: Route planning weather advice
- **alerts**: Critical weather warnings
- **updates**: Current condition updates

## Error Handling Patterns

### Database Errors
```javascript
// Graceful fallback
const result = await weatherService.getCurrentTimeZone('user123');
expect(result).to.equal(0); // Default when error occurs
```

### External API Failures
- **AI Service**: Handles axios request failures
- **Weather APIs**: Graceful degradation when weather unavailable
- **Default Responses**: Fallback behavior for service interruptions

## Testing Patterns

### Mock Data Structure
- **Realistic Data**: Uses actual data structures from production
- **Time Handling**: Proper Unix timestamps and ISO dates
- **Geographic Data**: Real coordinate ranges and grid structures

### Stubbing Strategy
```javascript
// Database query stubbing
const queryStub = sinon.stub(AppDatas, 'query').returns({
  findOne: sinon.stub().returns({
    orderBy: sinon.stub().resolves(mockResult)
  })
});

// HTTP request stubbing
const axiosPostStub = sinon.stub(axios, 'post').resolves(response);
```

## Business Logic

### Weather-Aware Transportation
- **Route Safety**: Weather conditions affect route recommendations
- **Travel Mode Impact**: Different weather effects for driving vs. walking
- **Time-sensitive**: Weather changes throughout travel duration

### User Experience
- **Proactive Warnings**: AI-generated weather messages
- **Real-time Updates**: Current weather conditions
- **Personalized Advice**: User-specific travel recommendations

This test suite ensures the weather service accurately processes weather data, integrates with route planning, generates intelligent weather messages, and maintains reliable weather-aware transportation features in the TSP API.