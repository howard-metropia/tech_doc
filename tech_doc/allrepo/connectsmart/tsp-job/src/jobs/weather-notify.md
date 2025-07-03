# Weather Notification Job

## Overview
Sophisticated weather alert system that analyzes critical weather events and delivers personalized notifications to users based on their travel patterns, location history, and geographic activity areas. The job integrates multiple data sources including habitual trips, app usage data, and home locations to provide comprehensive weather awareness across all user travel contexts.

## File Location
`/src/jobs/weather-notify.js`

## Dependencies
- `@maas/core/log` - Centralized logging framework
- `moment-timezone` - Advanced date/time manipulation with timezone support
- `@app/src/models/WeatherCriticalAlert` - Critical weather alert data model
- `@app/src/models/WeatherGridRegionCode` - Weather grid and region mapping model
- `@app/src/helpers/ai-log` - AI interaction logging utilities
- `@app/src/models/InternalUserTag` - Internal user classification model
- `@maas/core/mysql` - MySQL database connection for portal data
- `@app/src/static/defines` - System constants and configuration
- `@app/src/services/sendNotification` - Push notification delivery service
- `@app/src/services/weather` - Weather data processing and AI services
- `@app/src/services/rcs` - Rich Communication Services messaging
- `config` - Weather and project configuration management

## Job Configuration

### Inputs
```javascript
inputs: {}  // No input parameters required
```

### Notification Configuration
```javascript
const notificationType = 104  // Weather alert notification type
```

### Time Window Configuration
```javascript
const d1Time = d1TimeH.clone().tz('UTC').format('YYYY-MM-DD HH:mm:ss');     // Tomorrow start
const d1TimeEnd = d1TimeEndH.clone().tz('UTC').format('YYYY-MM-DD HH:mm:ss'); // Tomorrow end  
const d3Time = d3TimeH.clone().tz('UTC').format('YYYY-MM-DD HH:mm:ss');       // 3 days ahead
```

**Alert Time Windows**:
- **D1**: Tomorrow (next 24 hours)
- **D3**: Next 3 days for event filtering
- **Houston Timezone**: All processing based on America/Chicago timezone

## Multi-Source Location Data Collection

### 1. Habitual Trip Data (H-Trip)
```javascript
const getHTrip = async () => {
  const SQL = `
    Select f.*, u.device_language as language, 
           concat(u.country_code, u.phone_number) as phone_number, 
           u.registration_zone as time_zone 
    from (
      SELECT l.*, concat(TRUNCATE(l.o_lat,6),',', TRUNCATE(l.o_lon,6), ',', 
                         TRUNCATE(l.d_lat,6),',', TRUNCATE(l.d_lon,6),',', 
                         l.user_id) as identity 
      from (
        select user_id, 
               (select latitude from cm_location as origin where origin.id = cm_activity_location.o_id) as o_lat, 
               (select longitude from cm_location as origin where origin.id = cm_activity_location.o_id) as o_lon, 
               (select latitude from cm_location as destination where destination.id = cm_activity_location.d_id) as d_lat, 
               (select longitude from cm_location as destination where destination.id = cm_activity_location.d_id) as d_lon 
        from cm_activity_location 
        where trip_count > 2 and top_lt1_ceff_prob > 0.5 and trip_count_quarterly > 0
      ) as l 
      group by identity
    ) as f 
    left join auth_user as u on f.user_id = u.id 
    left join user_config as c on f.user_id = c.user_id 
    WHERE c.uis_setting->> '$.weather_alert'='true' OR c.uis_setting->> '$.weather_alert' is null;`;
}
```

**H-Trip Logic**:
- **High Confidence Trips**: Only includes trips with `top_lt1_ceff_prob > 0.5`
- **Regular Patterns**: Requires `trip_count > 2` for established patterns
- **Recent Activity**: Must have `trip_count_quarterly > 0`
- **Location Pairs**: Captures both origin and destination coordinates
- **Deduplication**: Groups by geographic identity to avoid duplicate locations

### 2. App Data Collection
```javascript
const getAppDataList = async (currentDatetime) => {
  const lastWeekDatetime = moment(currentDatetime).subtract(7, 'days').format('YYYY-MM-DD HH:mm:ss');
  const SQL = `
    SELECT l.user_id, l.lat, l.lon, l.language, l.uis_setting, l.phone_number, l.time_zone 
    from (
      SELECT m.*, concat(TRUNCATE(m.lat,6),',', TRUNCATE(m.lon,6), ',', m.user_id) as identity, 
             u.device_language as language, u.registration_zone as time_zone, 
             c.uis_setting, concat(u.country_code, u.phone_number) as phone_number 
      FROM hybrid.app_data as m 
      left join auth_user as u on m.user_id = u.id 
      left join user_config as c on m.user_id = c.user_id 
      where m.created_on > '${lastWeekDatetime}' and m.lon < 0 
        and (c.uis_setting->>'$.weather_alert' is null or c.uis_setting->>'$.weather_alert'='true') 
    ) as l 
    group by l.identity 
    order by l.user_id desc;`;
}
```

**App Data Features**:
- **Recent Activity**: Only includes data from last 7 days
- **Geographic Filtering**: `m.lon < 0` filters for Western Hemisphere (Americas)
- **User Preferences**: Respects weather alert opt-in/opt-out settings
- **Location Deduplication**: Groups by truncated coordinates to reduce noise

### 3. Home Location Data
```javascript
const getHomeList = async () => {
  const SQL = `
    WITH selected_group AS (
      SELECT m.*, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_on DESC) AS rn 
      FROM hybrid.user_favorites AS m 
      where m.category = 1 
    )
    SELECT s.user_id, s.latitude as lat, s.longitude as lon, 
           u.device_language as language, 
           concat(u.country_code, u.phone_number) as phone_number, 
           u.registration_zone as time_zone 
    FROM selected_group as s 
    left join auth_user as u on s.user_id = u.id 
    left join user_config as c on s.user_id = c.user_id 
    WHERE (c.uis_setting->> '$.weather_alert'='true' OR c.uis_setting->> '$.weather_alert' is null) 
      and s.rn = 1 and s.longitude < 0;`;
}
```

**Home Location Logic**:
- **Category 1**: Home/residential locations in user favorites
- **Most Recent**: Uses `ROW_NUMBER()` to get latest home location per user
- **Geographic Scope**: Western Hemisphere filtering with `longitude < 0`
- **User Consent**: Honors weather alert notification preferences

## User Location Aggregation

### Data Structure Consolidation
```javascript
const userSet = new Set();
const userList = {};

// Process H-Trip locations
htripList.forEach((trip) => {
  if (userSet.has(Number(trip.user_id))) {
    userList[trip.user_id].locList.push(
      [trip.o_lon, trip.o_lat],
      [trip.d_lon, trip.d_lat],
    );
  } else {
    const locList = [
      [trip.o_lon, trip.o_lat],
      [trip.d_lon, trip.d_lat],
    ];
    userList[trip.user_id] = {
      language: trip.language ? trip.language : 'en',
      phone_number: trip.phone_number,
      time_zone: trip.time_zone,
      locList,
    };
    userSet.add(Number(trip.user_id));
  }
});
```

**Aggregation Strategy**:
- **User Deduplication**: Single user entry with multiple locations
- **Location Accumulation**: Combines locations from all data sources
- **Timezone Consistency**: Uses hardcoded America/Chicago timezone
- **Default Language**: Falls back to English if language not specified

## Debug Mode and Testing

### Debug Mode Configuration
```javascript
const isDebugModeEnabledForUser = async (userId) => {
  const mockConfig = weatherConfig.mockAllowed;
  const allowedMock = mockConfig === 'true';
  if (!allowedMock) return false;
  
  const internalUser = await InternalUserTag.query()
    .where('user_id', userId)
    .andWhere('tag', 'internal_user')
    .first();
    
  if (internalUser) {
    logger.info(`[mock-weather] target user: ${internalUser.user_id}/${internalUser.tag}`);
    return false;
  } else {
    logger.info(`[mock-weather] not target user: ${userId}`);
    return true;
  }
}
```

### Sandbox Testing Configuration
```javascript
// For SB testing
if (stage === 'develop' || stage === 'sandbox') {
  const testUserIDs = [13697, 10288, 29495, 29464, 29597];
  if (testUserIDs.includes(Number(data.user_id))) {
    const locList = [[data.lon, data.lat]];
    userList[data.user_id] = {
      language: data.language ? data.language : 'en',
      phone_number: data.phone_number,
      time_zone: data.time_zone,
      locList,
    };
    userSet.add(Number(data.user_id));
  }
}
```

**Testing Features**:
- **Environment-Specific**: Different behavior for develop/sandbox stages
- **Test User IDs**: Specific users for testing weather notifications
- **Mock Prevention**: Filters out internal users from mock data
- **Configuration-Driven**: Uses config flags to control debug behavior

## Weather Grid Processing

### Batch Processing Architecture
```javascript
const userChunkedArray = splitIntoChunks(userList, 50);

const splitIntoChunks = (userList, chunkSize) => {
  const result = [];
  let tempSubArray = [];
  let count = 0;
  const keys = Object.keys(userList);
  
  for (const userID in userList) {
    if (count < chunkSize) {
      tempSubArray.push({
        user_id: userID,
        language: userList[userID].language,
        phone_number: userList[userID].phone_number,
        time_zone: userList[userID].time_zone,
        locList: userList[userID].locList,
      });
      count++;
    } else {
      result.push(Array.from(tempSubArray));
      tempSubArray = [];
      count = 0;
    }
  }
  return result;
};
```

**Batch Processing Benefits**:
- **Memory Management**: Processes users in chunks of 50
- **Performance Optimization**: Prevents memory overflow with large user sets
- **Parallel Processing**: Each chunk processed concurrently
- **Resource Control**: Manages database connection pooling

## Geospatial Weather Analysis

### Grid Intersection Query
```javascript
const grids = await WeatherGridRegionCode.find({
  geometry: {
    $geoIntersects: {
      $geometry: {
        type: 'MultiPoint',
        coordinates: user.locList,
      },
    },
  },
}).select({
  grid_id: 1,
  city_tag: 1,
  county_tag: 1,
});
```

**Geospatial Logic**:
- **MultiPoint Query**: Efficiently queries multiple user locations simultaneously
- **Grid Mapping**: Maps user locations to weather grid regions
- **Location Hierarchy**: Captures city and county information for alerts
- **Efficient Selection**: Only retrieves necessary grid identification data

### Critical Alert Filtering
```javascript
const alerts = await WeatherCriticalAlert.find({
  $and: [
    { impacted_area: { $in: gridIDList } },
    { start_at: { $gte: d1Datetime } },     // Events starting tomorrow or later
    { start_at: { $lte: d3Datetime } },     // Events within 3-day window
    { end_at: { $gte: d1DatetimeEnd } },    // Events lasting past tomorrow
  ],
}).select({
  properties: 1,
  impacted_area: 1,
  alert_id: 1,
  start_at: 1,
  end_at: 1,
  geometry: 1,
});
```

**Alert Filtering Rules**:
- **Geographic Matching**: Only alerts affecting user's grid regions
- **Time Window**: Events occurring within next 1-3 days
- **Duration Filter**: Events lasting beyond tomorrow end
- **Data Efficiency**: Selective field retrieval for performance

## Weather Event Processing

### Alert Deduplication
```javascript
const removeDuplicatedCriticalAlerts = (alerts) => {
  const categorizedAlerts = {};
  alerts.forEach((a) => {
    let type = a.properties.event.split(' ').slice(0, -1).join(' ');
    if (categorizedAlerts[type]) {
      if (moment(a.properties.sent) > moment(categorizedAlerts[type].properties.sent)) {
        categorizedAlerts[type] = a;
      }
    } else {
      categorizedAlerts[type] = a;
    }
  });
  return Object.entries(categorizedAlerts).map(([key, value]) => value);
};
```

### Event Title Cleanup
```javascript
const removeWordsFromEventTitle = (alerts) => {
  const wordsToRemove = ['Warning', 'Advisory', 'Watch', 'Local Statement', 'Statement'];
  alerts.forEach((a) => {
    const regex = new RegExp(`\\b(${wordsToRemove.join('|')})\\b`, 'gi');
    const modifiedStr = a.properties.event.replace(regex, '').replace(/\s+/g, ' ').trim();
    a.properties.event = modifiedStr;
  });
  return alerts;
};
```

**Event Processing Features**:
- **Duplicate Removal**: Uses most recent alert for each event type
- **Title Normalization**: Removes common weather service terminology
- **Text Cleanup**: Standardizes spacing and formatting
- **Event Categorization**: Groups related alerts by type

## AI Message Generation

### Intelligent Message Creation
```javascript
const aiMessage = await weather.getAIMessage(userAlerts, user.language, nowTime);

await aiLogModule.logAIToDB(
  'weather',
  'tsp-job /weather-notify',
  DEFINES.weather.openAIModel,
  aiMessage.origin_message,
  aiMessage.prompt,
  { critical: userAlerts },
  current.toDate(),
);
```

**AI Integration Features**:
- **Multi-Language Support**: Generates messages in user's preferred language
- **Context Awareness**: Considers user's specific weather alerts
- **Time Sensitivity**: Incorporates current time for relevant messaging
- **Audit Logging**: Comprehensive logging of AI interactions

### User Alert Structure
```javascript
userAlerts.push({
  alert_id: a.alert_id,
  loc_name: locName,                    // City/county names
  event: a.properties.event,            // Cleaned event title
  description: a.properties.description, // Detailed description
  instruction: a.properties.instruction, // Safety instructions
  polygon: a.geometry ? a.geometry.coordinates[0] : [], // Geographic boundary
  start: a.start_at,                    // Event start time
  end: a.end_at,                        // Event end time
});
```

## Multi-Channel Notification Delivery

### Push Notification Delivery
```javascript
await sendNotification(
  userIds,
  notificationType,
  title,
  body,
  meta,
  lang,
  false,
);
```

### RCS Message Delivery
```javascript
sendRCSMessage({
  user_id: user.user_id,
  title,
  body,
  polygon: user.polygon,
  phone_number: user.phone_number,
});
```

**Delivery Features**:
- **Dual Channel**: Both push notifications and RCS messages
- **Rich Content**: Includes polygon data for map visualization
- **Metadata**: Additional context including info URLs
- **Language Support**: Localized message delivery

## Dynamic Content Generation

### Info URL Mapping
```javascript
let type = Object.keys(DEFINES.weather.infoUrlList).find((key) =>
  user.alerts[0].event.toLowerCase().includes(key),
);
const info_url = DEFINES.weather.infoUrlList[type] ? DEFINES.weather.infoUrlList[type] : '';
```

**Content Features**:
- **Event-Specific URLs**: Maps weather events to relevant information sources
- **Dynamic Linking**: Provides contextual links based on event type
- **Fallback Handling**: Graceful degradation when specific info unavailable
- **User Education**: Links to weather safety and preparation resources

## Performance and Scalability

### Processing Optimization
- **Batch Processing**: 50-user chunks for memory management
- **Parallel Operations**: Concurrent processing of user chunks
- **Efficient Queries**: Optimized database queries with proper indexing
- **Resource Management**: Controlled database connection usage

### Monitoring and Logging
```javascript
logger.error(`[weather-notify] htrip loc count: ${htripList.length}`);
logger.error(`[weather-notify] appData loc count: ${appDataList.length}`);
logger.error(`[weather-notify] home loc count: ${homeList.length}`);
```

**Operational Insights**:
- **Data Source Metrics**: Tracks location counts from each data source
- **Processing Statistics**: User chunk counts and processing progress
- **Error Tracking**: Comprehensive error logging with stack traces
- **Performance Monitoring**: Processing time and resource utilization

## Integration Points
- Weather data services and APIs
- User location tracking systems
- Geographic information systems (GIS)
- AI/ML message generation services
- Multi-channel notification infrastructure
- User preference management system
- Geographic grid and region databases

## Timezone and Scheduling
All processing uses America/Chicago timezone with configurable notification sending hours defined in `DEFINES.weather.notificationSendingHour` for consistent user experience across the service area.