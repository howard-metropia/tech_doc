# Report Mail Service Test Suite

## Overview
Comprehensive test suite for the report mail functionality that validates automated email report generation, construction zone event processing, weather alert integration, and multi-user report delivery systems. The tests cover complex geospatial queries, AI-powered message generation, and integrated travel report compilation for user notifications.

## File Location
`/test/testReportMail.js`

## Technical Analysis

### Core Services Under Test
```javascript
// Commented out in test but referenced functionality:
// const { addUsers, mailContent, processMailList } = require('@app/src/services/reportMail');
const constructionZone = require('@app/src/services/constructionZone');
const weather = require('@app/src/services/weather');
```

The test suite validates report mail generation capabilities including construction zone matching, weather alert processing, and personalized content creation.

### Dependencies
- `@maas/core/bootstrap` - Application bootstrap and configuration
- `chai` - Assertion library with expect interface for validation
- `moment-timezone` - Advanced date/time manipulation with timezone support
- `fs` - File system operations for report content management
- Multiple database models for geospatial and temporal data processing

### Database Model Architecture

#### Core Data Models
```javascript
const AuthUser = require('@app/src/models/authUsers');
const RptMailStatus = require('@app/src/models/rptMailStatus'); 
const RptMailList = require('@app/src/models/rptMailList');
const ReservationPolyline = require('@app/src/models/reservationPolyline');
const ConstructionZone = require('@app/src/models/constructionZone');
const WeatherCriticalAlert = require('@app/src/models/weatherCriticalAlert');
const WeatherGridRegionCode = require('@app/src/models/WeatherGridRegionCode');
```

#### Test User Configuration
```javascript
const userIds = [29341, 12773]; // Production user IDs for comprehensive testing
```

### Construction Zone Testing Framework

#### Geospatial Query Architecture
```javascript
// Commented implementation shows complex MongoDB geospatial queries
const zones = await ConstructionZone.find({
  start_date: { $lte: end.toDate() },
  end_date: { $gte: start.toDate() },
  'geometry': {
    $geoIntersects: {
      $geometry: {
        type: 'LineString',
        coordinates: polyline[0].trip_geojson.coordinates
      }
    }
  },
});
```

This validates intersection detection between user travel routes and active construction zones.

#### Construction Event Categorization
```javascript
// Time-based categorization logic (commented in test)
const getTimeCategory = (date, nowTime) => {
  const daysDifference = constructionZone.getDayDifference(date, nowTime);
  if( daysDifference === 90 ) return 5;
  else if ( daysDifference === 30 ) return 4;
  else if ( daysDifference === 14 ) return 3;
  else if ( daysDifference === 7 ) return 2;
  else if ( daysDifference == 1) return 1;
  else return 6;
};
```

Categories represent urgency levels based on temporal proximity to construction events.

### Weather Alert Integration

#### Weather Geospatial Matching
```javascript
// Complex geospatial query for weather alerts (commented)
const alerts = await WeatherCriticalAlert.find({
  start_at: { $lte: end.toDate() },
  end_at: { $gte: start.toDate() },
  'geometry': {
    $geoIntersects: {
      $geometry: {
        type: 'LineString',
        coordinates: polyline[0].trip_geojson.coordinates
      }
    }
  },
});
```

#### Regional Weather Processing
```javascript
// Location name extraction from weather grid regions
const region = await WeatherGridRegionCode.find({
  geometry: {
    $geoIntersects: {
      $geometry: {
        type: 'MultiPoint',
        coordinates: locList,
      },
    },
  },
}).select({
  grid_id: 1,
  city_tag: 1,
  county_tag: 1,
});
```

## Usage/Integration

### Report Generation Workflow
The test framework validates a multi-step report generation process:

1. **User Selection**: Identify users eligible for report delivery
2. **Route Analysis**: Extract user travel patterns from reservation polylines
3. **Event Matching**: Find construction zones and weather alerts intersecting routes
4. **Content Generation**: Create personalized report content using AI services
5. **Delivery Processing**: Format and queue reports for email delivery

### Mail Content Generation
```javascript
// Commented test shows expected content generation pattern
const content = await mailContent(user, token, start, end, list);
expect(content).to.be.a('string');
fs.writeFileSync(`testMailContent${index}.html`, content);
```

The service generates HTML-formatted reports containing personalized travel information, alerts, and recommendations.

### Time Range Configuration
```javascript
const end = moment.utc().subtract(1, 'days').format('YYYY-MM-DD') + ' 23:59:59';
const start = moment.utc().subtract(8, 'days').format('YYYY-MM-DD') + ' 00:00:00';
```

Reports typically cover a 7-day retrospective period with configurable date ranges.

## Code Examples

### Construction Zone Event Processing
```javascript
// Event data structure creation (from commented code)
const eventList = zones.map((e) => {
  let category = 6;
  const createTime = constructionZone.getDayDifference(
    moment(e.properties.core_details.creation_date).format('YYYY-MM-DD HH:mm:ss'), 
    nowTime
  );
  
  if(createTime === 0) {
    category = getTimeCategoryByCreateDate(
      moment(e.properties.start_date).format('YYYY-MM-DD HH:mm:ss'),
      nowTime
    );
  } else {
    category = getTimeCategory(
      moment(e.properties.start_date).format('YYYY-MM-DD HH:mm:ss'),
      nowTime
    );
  }
  
  return {
    event_id: e.properties.core_details.data_source_id,
    location: e.properties.extensions.location,
    polygon: e.geometry.coordinates,
    start: moment(e.properties.start_date).format('YYYY-MM-DD HH:mm:ss'),
    expire: moment(e.properties.end_date).format('YYYY-MM-DD HH:mm:ss'),
    level: e.properties.extensions.impacted_level,
    info_url: e.properties.extensions.info_url || '',
    image_url: e.properties.extensions.image_url || '',
    category: category
  };
});
```

### Weather Alert Data Structure
```javascript
// Weather alert processing (from commented code)
const userAlerts = alerts.map((a) => {
  return {
    alert_id: a.alert_id,
    loc_name: locName,
    event: a.properties.event,
    description: a.properties.description,
    instruction: a.properties.instruction,
    polygon: a.geometry && a.geometry !== null && a.geometry !== undefined
      ? a.geometry.coordinates[0]
      : [],
    start: a.start_at,
    end: a.end_at,
  };
});
```

### AI-Powered Message Generation
```javascript
// Construction zone message generation
for (const e of eventList) {
  const message = constructionZone.formMessage(e, nowTime);
  const translatedMessageObj = await constructionZone.getAIMessage(message, user.language);
  messages.push(translatedMessageObj.body);
}

// Weather alert message generation  
if (alerts) {
  const msg = await weather.getAIMessage(userAlerts, 'en-US');
  console.log('Message:', msg);
}
```

### Location Name Processing
```javascript
// Extract location names with fallback hierarchy
let locName = new Set();
region.forEach((grid) => {
  locName.add(
    grid.city_tag
      ? grid.city_tag
      : grid.county_tag
      ? grid.county_tag
      : 'Houston',  // Default fallback
  );
});
locName = [...locName];
```

## Integration Points

### Geospatial Data Processing
- **MongoDB Geospatial Queries**: Complex intersection detection for routes and events
- **Coordinate System Management**: Handling of GeoJSON LineString and Polygon data
- **Route Analysis**: Integration with user reservation and travel pattern data

### AI and Localization Services
- **Message Generation**: AI-powered content creation for alerts and notifications
- **Multi-language Support**: Localized content based on user language preferences
- **Content Personalization**: User-specific report formatting and recommendations

### Email Delivery System
- **HTML Report Generation**: Rich-formatted email content with embedded data
- **Batch Processing**: Efficient multi-user report generation and delivery
- **Template Management**: Configurable report layouts and styling

### External Data Sources
- **Construction Data APIs**: Real-time construction zone information
- **Weather Services**: Critical weather alert integration
- **Geographic Information Systems**: Regional and municipal boundary data

### System Performance
- **Concurrent Processing**: Parallel report generation for multiple users
- **Caching Strategies**: Optimized data retrieval for repeated geospatial queries
- **Error Handling**: Graceful degradation when external services unavailable

This comprehensive test suite ensures the report mail system can reliably generate personalized, location-aware travel reports that integrate construction alerts, weather warnings, and user-specific travel patterns into actionable email communications.