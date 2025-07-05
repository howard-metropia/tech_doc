# Construction Alert Notification Job

## Overview
Advanced geospatial job that processes construction zone events and road closures to send targeted push notifications to affected users. The job uses sophisticated time-based categorization and geospatial analysis to deliver relevant alerts based on user activity areas and impact severity levels.

## File Location
`/src/jobs/construction-alert-notification.js`

## Dependencies
- `@app/src/models/ActivityArea` - User activity area geographic data model
- `@app/src/models/ConstructionZone` - Construction zone event data model  
- `@app/src/models/IncidentsEvent` - Traffic incident and closure event model
- `@app/src/models/AIResponseLog` - AI message generation logging model
- `@app/src/models/AuthUsers` - User authentication and profile model
- `@maas/core/log` - Centralized logging framework
- `@app/src/static/defines` - System constants and configuration
- `@turf/turf` - Geospatial analysis and GIS operations
- `@app/src/services/sendNotification` - Push notification delivery service
- `@app/src/services/constructionZone` - Construction zone business logic
- `moment-timezone` - Advanced date/time handling with timezone support

## Job Configuration

### Inputs
```javascript
inputs: {}  // No input parameters required
```

### Notification Type
```javascript
const notificationType = 105  // Construction alert notification type
```

## Core Data Models

### Event Processing Structure
```javascript
const eventList = []
constructionZoneEvents.forEach(e => {
  let eObj = {
    event_id: e.properties.core_details.data_source_id,
    location: e.properties.extensions.location,
    polygon: e.geometry.coordinates,
    start: moment(e.properties.start_date).format('YYYY-MM-DD HH:mm:ss'),
    expire: moment(e.properties.end_date).format('YYYY-MM-DD HH:mm:ss'),
    level: e.properties.extensions.impacted_level,
    info_url: e.properties.extensions.info_url || '',
    image_url: e.properties.extensions.image_url || '',
    category: category
  }
  eventList.push(eObj)
})
```

## Time-Based Categorization System

### Category Mapping Logic
```javascript
const getTimeCategory = (date, nowTime) => {
  const daysDifference = getDayDifference(date, nowTime);
  if (daysDifference === 90) return 5      // 90 days advance notice
  else if (daysDifference === 30) return 4  // 30 days advance notice
  else if (daysDifference === 14) return 3  // 2 weeks advance notice
  else if (daysDifference === 7) return 2   // 1 week advance notice
  else if (daysDifference == 1) return 1    // 1 day advance notice
  else return 6                             // Default/other timeframe
}
```

### Create Date vs Start Date Logic
```javascript
const getTimeCategoryByCreateDate = (date, nowTime) => {
  const daysDifference = getDayDifference(date, nowTime);
  if (90 >= daysDifference && daysDifference > 30) return 5
  else if (30 >= daysDifference && daysDifference > 14) return 4
  else if (14 >= daysDifference && daysDifference > 7) return 3
  else if (7 >= daysDifference && daysDifference > 1) return 2
  else if (daysDifference == 1) return 1
  else return 6
}
```

**Dual Category System**:
- **Creation Date = Today**: Uses `getTimeCategoryByCreateDate()` for start date
- **Creation Date ≠ Today**: Uses `getTimeCategory()` for start date

## Impact Level Filtering

### Severity-Based Notification Rules
```javascript
// Far impact level: Categories 5,4,3,2,1 (all advance notices)
if (e.level=='far' && [5,4,3,2,1].includes(e.category))

// Medium impact level: Categories 4,3,2,1 (30 days to 1 day)  
else if (e.level=='medium' && [4,3,2,1].includes(e.category))

// Near impact level: Categories 2,1 (1 week to 1 day only)
else if (e.level=='near' && [2,1].includes(e.category))
```

**Impact Level Definitions**:
- **Far**: Distant from user areas, requires early notification
- **Medium**: Moderate impact, needs reasonable advance notice
- **Near**: High impact, only immediate notifications to avoid alert fatigue

## Geospatial User Matching

### Geographic Intersection Query
```javascript
const userList = await ActivityArea.find({
  geometry: {
    $geoIntersects: {
      $geometry: {
        type: 'Polygon',
        coordinates: e.polygon,
      },
    },
  },
  updated_at: {
    $gte: validActivityAreaDatetime  // Only recent activity areas (7 days)
  }
}).select({
  user_id: 1
})
```

**Spatial Analysis**:
- **GeoIntersection**: MongoDB geospatial query for polygon overlap
- **Activity Recency**: Only considers activity areas updated within 7 days
- **User Deduplication**: Collects unique user IDs affected by each event

## User Information Processing

### User Data Retrieval
```javascript
const getUserInfo = async(userIDs) => {
  const result = await AuthUsers.query()
    .whereIn('id', userIDs)
    .select('id', 'device_language', 'registration_zone')
  const fResult = []
  result.forEach(u => {
    fResult.push({ 
      id: u.id, 
      language: u.device_language, 
      time_zone: u.registration_zone
    }) 
  })
  return fResult
}
```

## Timezone and Scheduling Logic

### Houston Timezone Hardcoding
```javascript
// Hardcore timezone to Houston
const userTimeZone = current.clone().tz('America/Chicago');

// Special handling for test user
if (u.id === 29434) {
  filteredUserByTimeZone.push(u)
} else {
  const localHour = userTimeZone !== undefined ? userTimeZone.hour() : current.hour();
  if (localHour === DEFINES.constructionAlert.notificationSendingHour) {
    filteredUserByTimeZone.push(u)
  }
}
```

**Timezone Strategy**:
- **Fixed Timezone**: All users processed in America/Chicago timezone
- **Hour Filtering**: Only sends notifications at configured hour
- **Test User Exception**: User ID 29434 bypasses time restrictions

## AI Message Generation

### Multilingual Message Processing
```javascript
const message = formMessage(e, nowTime, filteredUserByTimeZone[fUser].language)
const translatedMessageObj = await getAIMessage(message, filteredUserByTimeZone[fUser].language)

// Log AI interaction
AIResponseLog.create({
  task: 'construction-alert-notification',
  message: translatedMessageObj.body,
  datetime: current.toDate()
})
```

**AI Integration**:
- **Message Formation**: Creates structured message from event data
- **Translation**: AI-powered translation to user's preferred language
- **Response Logging**: Tracks all AI-generated messages for audit

## Notification Delivery

### Push Notification Structure
```javascript
const userIds = [filteredUserByTimeZone[fUser].id]
const notificationType = 105
const title = translatedMessageObj.title
const body = translatedMessageObj.body
const meta = {
  title,
  body,
  info_url: e.info_url ? e.info_url : '',
  image_url: e.image_url ? e.image_url : ''
}
const lang = translatedMessageObj.language

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

## Event Data Sources

### Construction Zone Events
```javascript
const constructionZoneEvents = await ConstructionZone.find({
  "properties.end_date": { $gte: current.toDate() }
})
```

### Closure Events
```javascript
const closureEvents = await IncidentsEvent.find({
  type: 'Closure',
  close: false
})
```

**Data Integration**:
- **Construction Zones**: Planned construction with detailed metadata
- **Closure Events**: Unplanned road closures and incidents
- **Active Filtering**: Only processes events that haven't expired

## Error Handling and Logging

### Comprehensive Error Management
```javascript
try {
  // Main processing logic
  logger.info(`[construction-alert-notification] executed event number: ${filteredEventList.length}`);
  logger.info(`[construction-alert-notification] event ${e.event_id} impact user number: ${e.user_ids.length}`);
  logger.info(`[construction-alert-notification] end`);
} catch (e) {
  logger.error(`[construction-alert-notification] error: ${e.message}`);
  logger.info(`[construction-alert-notification] stack: ${e.stack}`);
}
```

**Logging Strategy**:
- **Progress Tracking**: Event counts and user impact statistics
- **Error Details**: Full error messages and stack traces
- **Performance Metrics**: Event processing and user notification counts

## Performance Optimizations

### Batch Processing
```javascript
await Promise.all(
  eventList.map(async(e) => {
    // Geospatial filtering and user matching
  })
)

await Promise.all(
  filteredEventList.map(async(e) => {
    // Notification processing and delivery
  })
)
```

**Optimization Strategies**:
- **Parallel Processing**: Multiple events processed concurrently
- **Efficient Queries**: Targeted database queries with proper indexing
- **Memory Management**: Streaming data processing for large datasets

## Integration Points
- Construction zone management system
- Traffic incident reporting services
- User activity tracking system
- Geospatial analysis engine
- AI translation services
- Push notification infrastructure
- Activity area monitoring system

## Operational Monitoring
The job provides detailed operational insights through comprehensive logging of event processing, user targeting, and notification delivery metrics.