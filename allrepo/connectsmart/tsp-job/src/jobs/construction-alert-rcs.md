# Construction Alert RCS Job

## Overview
Rich Communication Services (RCS) messaging job that delivers construction zone and road closure alerts via advanced SMS messaging. This job mirrors the functionality of the push notification system but delivers alerts through RCS channels with enhanced message formatting and polygon data for map visualization.

## File Location
`/src/jobs/construction-alert-rcs.js`

## Dependencies
- `@app/src/models/ActivityArea` - User geographic activity area data model
- `@app/src/models/ConstructionZone` - Construction zone event data model
- `@app/src/models/IncidentsEvent` - Traffic incident and closure event model
- `@app/src/models/AuthUsers` - User authentication and profile model
- `@maas/core/log` - Centralized logging framework
- `@app/src/static/defines` - System constants and configuration
- `@turf/turf` - Geospatial analysis library
- `@app/src/services/rcs` - RCS messaging service layer
- `@app/src/services/constructionZone` - Construction zone business logic
- `moment-timezone` - Date/time manipulation with timezone support

## Job Configuration

### Inputs
```javascript
inputs: {}  // No input parameters required
```

### RCS Message Structure
The job sends RCS messages with enhanced formatting and geographic data for rich user experience.

## Core Data Processing

### User Information Enhancement
```javascript
const getUserInfo = async(userIDs) => {
  const result = await AuthUsers.query()
    .whereIn('id', userIDs)
    .select('id', 'device_language', 'registration_zone', 'country_code', 'phone_number')
  const fResult = []
  result.forEach(u => {
    fResult.push({ 
      id: u.id, 
      language: u.device_language, 
      time_zone: u.registration_zone, 
      phone_number: `${u.country_code}${u.phone_number}`
    }) 
  })
  return fResult
}
```

**Enhanced User Data**:
- **Phone Number**: Full international format for RCS delivery
- **Language Preference**: For AI message translation
- **Timezone**: For delivery time optimization
- **User ID**: For tracking and personalization

## Time-Based Event Categorization

### Identical Category Logic to Push Notifications
```javascript
const getTimeCategory = (date, nowTime) => {
  const daysDifference = getDayDifference(date, nowTime);
  if (daysDifference === 90) return 5      // 90 days advance
  else if (daysDifference === 30) return 4  // 30 days advance
  else if (daysDifference === 14) return 3  // 14 days advance
  else if (daysDifference === 7) return 2   // 7 days advance
  else if (daysDifference == 1) return 1    // 1 day advance
  else return 6                             // Default category
}
```

### Create Date Processing
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

**Categorization Strategy**:
- **Same Day Creation**: Uses creation date-based categorization
- **Prior Day Creation**: Uses standard time-based categorization
- **Consistent Logic**: Matches push notification timing rules

## Event Data Collection

### Construction Zone Processing
```javascript
const constructionZoneEvents = await ConstructionZone.find({
  "properties.end_date": { $gte: current.toDate() }
})

constructionZoneEvents.forEach(e => {
  let category = 6
  const createTime = getDayDifference(
    moment(e.properties.core_details.creation_date).format('YYYY-MM-DD HH:mm:ss'), 
    nowTime
  )
  
  if (createTime === 0) {
    category = getTimeCategoryByCreateDate(
      moment(e.properties.start_date).format('YYYY-MM-DD HH:mm:ss'),
      nowTime
    )
  } else {
    category = getTimeCategory(
      moment(e.properties.start_date).format('YYYY-MM-DD HH:mm:ss'),
      nowTime
    )
  }
  
  let eObj = {
    event_id: e.properties.core_details.data_source_id,
    location: e.properties.extensions.location,
    polygon: e.geometry.coordinates,
    start: moment(e.properties.start_date).format('YYYY-MM-DD HH:mm:ss'),
    expire: moment(e.properties.end_date).format('YYYY-MM-DD HH:mm:ss'),
    level: e.properties.extensions.impacted_level,
    info_url: e.properties.extensions.info_url || '',
    category: category
  }
  eventList.push(eObj)
})
```

### Closure Event Processing
```javascript
const closureEvents = await IncidentsEvent.find({
  type: 'Closure',
  close: false
})

closureEvents.forEach(e => {
  let eObj = {
    event_id: e.event_id,
    location: e.location,
    polygon: [e.polygon],
    start: e.start,
    expire: e.expires,
    level: "near",          // All closures treated as near impact
    info_url: "",           // No info URL for closures
    category: category
  }
  eventList.push(eObj)
})
```

## Impact Level Filtering

### Severity-Based RCS Delivery Rules
```javascript
// Far impact: All categories except default (6)
if (e.level=='far' && [5,4,3,2,1].includes(e.category)) {
  // Process geospatial user matching
}
// Medium impact: 30 days to 1 day advance notice
else if (e.level=='medium' && [4,3,2,1].includes(e.category)) {
  // Process geospatial user matching  
}
// Near impact: Only immediate notifications (1-2 weeks max)
else if (e.level=='near' && [2,1].includes(e.category)) {
  // Process geospatial user matching
}
```

**RCS Delivery Strategy**:
- **Selective Delivery**: Only sends RCS for relevant timing/impact combinations
- **Reduced Frequency**: Avoids RCS spam by filtering categories
- **Geographic Targeting**: Uses same geospatial intersection logic

## Geospatial User Matching

### Activity Area Intersection
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
})
.select({
  user_id: 1
})
```

**Key Difference from Push Notifications**:
- **No Time Filtering**: RCS job doesn't filter by `updated_at` date
- **Broader Reach**: Includes all historical activity areas
- **Comprehensive Coverage**: Ensures no users miss critical RCS alerts

## Timezone Processing

### Houston-Centric Delivery
```javascript
// Hardcode timezone to Houston
const userTimeZone = current.clone().tz('America/Chicago');

const localHour = userTimeZone !== undefined ? userTimeZone.hour() : current.hour();
if (localHour === DEFINES.constructionAlert.notificationSendingHour) {
  filteredUserByTimeZone.push(u)
}
```

**Simplified Logic**:
- **No Test User Exception**: Unlike push notifications, no special user handling
- **Consistent Timing**: All users follow same delivery hour restrictions
- **Fixed Timezone**: America/Chicago timezone for all processing

## AI Message Generation

### RCS-Specific Message Formatting
```javascript
const message = formMessage(e, nowTime)  // No language parameter
const translatedMessageObj = await getAIMessage(message, filteredUserByTimeZone[fUser].language)

const userId = filteredUserByTimeZone[fUser].id
const phoneNumber = filteredUserByTimeZone[fUser].phone_number
const title = translatedMessageObj.title
const body = translatedMessageObj.body
```

**RCS Message Processing**:
- **Language-Agnostic Formation**: Initial message formation without language
- **AI Translation**: Subsequent translation to user's preferred language
- **Phone Number Integration**: Direct phone number for RCS delivery

## RCS Message Delivery

### Enhanced RCS Structure
```javascript
await sendRCSMessage({
  user_id: userId,
  title,
  body,
  polygon: e.polygon[0],      // First polygon coordinate array
  phone_number: phoneNumber,
});
```

**RCS Enhancement Features**:
- **Polygon Data**: Includes geographic polygon for map visualization
- **Rich Formatting**: Enhanced message presentation
- **Direct Delivery**: Phone number-based delivery system
- **User Tracking**: User ID for engagement analytics

## Key Differences from Push Notifications

### Feature Comparison
| Feature | Push Notifications | RCS Messages |
|---------|-------------------|--------------|
| **Phone Numbers** | Not required | Essential for delivery |
| **Activity Area Filtering** | 7-day recency filter | No time filtering |
| **Test User Handling** | Special exception for user 29434 | Standard processing |
| **Message Structure** | Includes info_url and image_url | Includes polygon data |
| **AI Logging** | Full AI response logging | No explicit AI logging |

### Technical Differences
- **Delivery Channel**: Push vs RCS messaging infrastructure
- **Geographic Data**: RCS includes polygon coordinates for maps
- **User Data**: RCS requires phone numbers for delivery
- **Reach Strategy**: RCS has broader historical activity area coverage

## Error Handling

### Comprehensive Error Management
```javascript
try {
  logger.info(`[construction-alert-rcs] executed event number: ${filteredEventList.length}`);
  // Processing logic
  logger.info(`[construction-alert-rcs] event ${e.event_id} impact user number: ${e.user_ids.length}`);
  logger.info(`[construction-alert-rcs] end`);
} catch (e) {
  logger.error(`[construction-alert-rcs] error: ${e.message}`);
  logger.info(`[construction-alert-rcs] stack: ${e.stack}`);
}
```

## Performance Considerations

### Parallel Processing
```javascript
await Promise.all(
  eventList.map(async(e) => {
    // Event filtering and user matching
  })
)

await Promise.all(
  filteredEventList.map(async(e) => {
    // RCS message delivery
  })
)
```

**Optimization Features**:
- **Concurrent Processing**: Multiple events processed simultaneously
- **Efficient Queries**: Targeted database operations
- **Streamlined Delivery**: Direct RCS service integration

## Integration Points
- RCS messaging infrastructure
- Construction zone management system
- Traffic incident reporting services
- User activity tracking system
- Geospatial analysis engine
- AI translation services
- Phone number management system

## Operational Monitoring
Provides detailed logging for RCS delivery tracking, user engagement metrics, and system performance analysis.