# WeatherCriticalAlert Model

## Overview
Weather critical alert management model for the TSP Job system. Handles storage, processing, and geospatial analysis of severe weather alerts that impact transportation, enabling proactive user notifications and travel safety warnings based on weather conditions and geographic impact areas.

## Model Definition
```javascript
const { Schema } = require('mongoose');
const conn = require('@maas/core/mongo')('cache');

const mongoSchema = new Schema({
  alert_id: { type: String },
  start_at: { type: Date },
  end_at: { type: Date },
  impacted_area: { type: Array },
  properties: { type: Object },
  geometry: { type: Object}
});

const WeatherCriticalAlert = conn.model('weather_critical_alert', mongoSchema);

module.exports = WeatherCriticalAlert;
```

## Database Configuration
- **Database**: Cache MongoDB instance
- **Collection**: `weather_critical_alert`
- **ORM**: Mongoose with structured schema
- **Connection**: Managed by @maas/core MongoDB connection pool
- **Indexing**: Geospatial and temporal indexing for efficient queries

## Purpose
- Critical weather alert storage and management
- Geospatial weather impact analysis
- Transportation safety notification generation
- User location-based weather alert targeting
- Real-time weather condition monitoring

## Key Features
- **Geospatial Analysis**: Geographic impact area processing
- **Temporal Management**: Time-based alert lifecycle tracking
- **Multi-hazard Support**: Various weather condition handling
- **Impact Assessment**: Transportation route and user impact analysis
- **Real-time Processing**: Immediate alert ingestion and processing

## Schema Structure
Comprehensive weather alert data model:

```javascript
{
  alert_id: String,              // Unique weather alert identifier
  start_at: Date,                // Alert effective start time
  end_at: Date,                  // Alert expiration time
  impacted_area: Array,          // Geographic coordinates of impact zone
  properties: {                  // Weather alert metadata
    severity: String,            // Alert severity level
    certainty: String,           // Confidence level
    urgency: String,             // Time sensitivity
    event_type: String,          // Weather phenomenon type
    headline: String,            // Alert headline
    description: String,         // Detailed description
    instruction: String,         // Safety instructions
    sender: String,              // Issuing authority
    web_url: String,             // Additional information URL
    contact_info: Object         // Emergency contact information
  },
  geometry: {                    // GeoJSON geometry object
    type: String,                // Geometry type (Polygon, MultiPolygon)
    coordinates: Array           // Coordinate arrays
  }
}
```

## Weather Alert Types
- **Severe Weather**: Thunderstorms, tornadoes, hail
- **Winter Weather**: Snow, ice, freezing conditions
- **Flood Warnings**: Flash floods, river flooding
- **Wind Alerts**: High winds, dust storms
- **Temperature Extremes**: Excessive heat, cold warnings
- **Visibility Issues**: Fog, smoke, dust

## Usage Context
Primary usage in weather notification processing jobs:

```javascript
const getCurrentWeatherAlerts = async () => {
  const currentTime = new Date();
  
  const activeAlerts = await WeatherCriticalAlert.find({
    start_at: { $lte: currentTime },
    end_at: { $gte: currentTime }
  })
  .select({
    alert_id: 1,
    start_at: 1,
    end_at: 1,
    impacted_area: 1,
    properties: 1,
    geometry: 1
  })
  .lean();
  
  return activeAlerts;
};
```

## Geospatial Processing
Advanced geographic analysis for user impact assessment:

```javascript
const getUsersInWeatherImpactArea = async (alertGeometry) => {
  // Find users with locations intersecting weather alert area
  const affectedUsers = await WeatherGridRegionCode.find({
    geometry: {
      $geoIntersects: {
        $geometry: alertGeometry
      }
    }
  }).select('user_id lat lon').lean();

  return affectedUsers;
};

const checkUserLocationInWeatherZone = async (userLat, userLon, alertId) => {
  const weatherAlert = await WeatherCriticalAlert.findOne({
    alert_id: alertId,
    geometry: {
      $geoIntersects: {
        $geometry: {
          type: "Point",
          coordinates: [userLon, userLat]
        }
      }
    }
  });

  return weatherAlert !== null;
};
```

## Alert Processing Workflow
Comprehensive weather alert lifecycle management:

```javascript
const processWeatherAlerts = async () => {
  const currentTime = moment.utc().format('YYYY-MM-DD HH:mm:ss');
  
  try {
    // Get active weather alerts
    const activeAlerts = await WeatherCriticalAlert.find({
      start_at: { $lte: new Date() },
      end_at: { $gte: new Date() }
    });

    for (const alert of activeAlerts) {
      // Determine alert severity and user impact
      const severity = calculateWeatherSeverity(alert.properties);
      
      // Find affected users based on location and travel patterns
      const affectedUsers = await findUsersInWeatherArea(alert);
      
      // Process user notifications
      await processWeatherNotifications(alert, affectedUsers, severity);
      
      // Log alert processing metrics
      await logWeatherAlertMetrics(alert, affectedUsers.length);
    }
  } catch (error) {
    logger.error(`Weather alert processing error: ${error.message}`);
  }
};
```

## Severity Classification
Weather alert severity assessment system:

```javascript
const calculateWeatherSeverity = (properties) => {
  const severityMatrix = {
    'Extreme': 4,
    'Severe': 3,
    'Moderate': 2,
    'Minor': 1,
    'Unknown': 0
  };

  const urgencyMatrix = {
    'Immediate': 3,
    'Expected': 2,
    'Future': 1,
    'Past': 0
  };

  const certaintyMatrix = {
    'Observed': 3,
    'Likely': 2,
    'Possible': 1,
    'Unlikely': 0
  };

  const severityScore = severityMatrix[properties.severity] || 0;
  const urgencyScore = urgencyMatrix[properties.urgency] || 0;
  const certaintyScore = certaintyMatrix[properties.certainty] || 0;

  return Math.round((severityScore + urgencyScore + certaintyScore) / 3);
};
```

## User Notification Logic
Intelligent user targeting based on weather impact and travel patterns:

```javascript
const processWeatherNotifications = async (alert, affectedUsers, severity) => {
  for (const user of affectedUsers) {
    try {
      // Check user weather notification preferences
      const userSettings = await getUserWeatherSettings(user.user_id);
      
      if (!userSettings.weather_alert_enabled) continue;
      
      // Generate localized weather message
      const message = generateWeatherMessage(alert, user.language);
      
      // Determine notification priority based on severity and user activity
      const priority = calculateNotificationPriority(severity, user);
      
      // Queue weather notification
      await queueWeatherNotification({
        user_id: user.user_id,
        alert_id: alert.alert_id,
        message: message,
        priority: priority,
        weather_type: alert.properties.event_type,
        severity: severity
      });
      
    } catch (error) {
      logger.error(`Weather notification processing error for user ${user.user_id}: ${error.message}`);
    }
  }
};
```

## Integration with Trip Planning
Weather impact on travel routes and user journeys:

```javascript
const assessWeatherImpactOnTrips = async (alert) => {
  // Find habitual trips intersecting weather area
  const affectedHabitualTrips = await findHabitualTripsInWeatherZone(alert.geometry);
  
  // Find scheduled reservations in impact area
  const affectedReservations = await findReservationsInWeatherZone(alert.geometry);
  
  // Find calendar events in weather impact area
  const affectedCalendarEvents = await findCalendarEventsInWeatherZone(alert.geometry);
  
  return {
    habitual_trips: affectedHabitualTrips,
    reservations: affectedReservations,
    calendar_events: affectedCalendarEvents,
    total_affected: affectedHabitualTrips.length + affectedReservations.length + affectedCalendarEvents.length
  };
};
```

## Multi-language Support
Localized weather alert messages:

```javascript
const generateWeatherMessage = (alert, language) => {
  const weatherMessages = {
    en: {
      flood_warning: {
        title: 'Flood Warning in Your Area',
        body: 'High risk of flooding detected. Avoid unnecessary travel and use alternative routes.'
      },
      severe_storm: {
        title: 'Severe Weather Alert',
        body: 'Severe thunderstorms expected. Exercise caution when traveling.'
      },
      winter_weather: {
        title: 'Winter Weather Advisory',
        body: 'Snow and ice conditions. Drive carefully and allow extra travel time.'
      }
    },
    es: {
      flood_warning: {
        title: 'Alerta de Inundación en su Área',
        body: 'Alto riesgo de inundación detectado. Evite viajes innecesarios y use rutas alternativas.'
      },
      severe_storm: {
        title: 'Alerta de Clima Severo',
        body: 'Se esperan tormentas severas. Tenga precaución al viajar.'
      },
      winter_weather: {
        title: 'Aviso de Clima Invernal',
        body: 'Condiciones de nieve y hielo. Conduzca con cuidado y permita tiempo extra de viaje.'
      }
    }
  };

  const eventType = mapWeatherEventType(alert.properties.event_type);
  const messageTemplate = weatherMessages[language]?.[eventType] || weatherMessages.en[eventType];
  
  return {
    title: messageTemplate.title,
    body: messageTemplate.body,
    details: alert.properties.description,
    instructions: alert.properties.instruction
  };
};
```

## Performance Features
- **MongoDB Indexing**: Geospatial and temporal indexing for fast queries
- **Efficient Queries**: Optimized for location-based filtering
- **Connection Pooling**: Managed database connections
- **Memory Optimization**: Lean queries for large datasets

## Analytics and Metrics
Weather alert effectiveness tracking:

```javascript
const logWeatherAlertMetrics = async (alert, affectedUserCount) => {
  const metrics = {
    alert_id: alert.alert_id,
    event_type: alert.properties.event_type,
    severity: alert.properties.severity,
    affected_users: affectedUserCount,
    geographic_area: calculateAlertArea(alert.geometry),
    duration_hours: moment(alert.end_at).diff(moment(alert.start_at), 'hours'),
    processing_timestamp: new Date(),
    engagement_metrics: {
      notifications_sent: 0,
      user_interactions: 0,
      route_changes: 0
    }
  };

  await WeatherAlertMetrics.create(metrics);
};
```

## Error Handling
Comprehensive error management for weather processing:

```javascript
try {
  await processWeatherAlerts();
} catch (error) {
  logger.error(`WeatherCriticalAlert processing failed: ${error.message}`);
  
  // Send alert to monitoring system
  const alert = new AlertManager(slackConfig);
  const alertMessage = {
    project: 'tsp-job',
    stage: process.env.PROJECT_STAGE,
    status: 'ERROR',
    vendor: 'weather-service',
    vendorApi: 'weather-critical-alert',
    originApi: 'tsp-job weather-notify',
    errorMsg: error.message,
    meta: 'Weather alert processing failure'
  };
  alert.sendMsg(alertMessage);
}
```

## Data Sources Integration
Multiple weather data provider support:

```javascript
const ingestWeatherAlertsFromSources = async () => {
  const weatherSources = [
    'national_weather_service',
    'local_emergency_management',
    'weather_api_providers'
  ];

  for (const source of weatherSources) {
    try {
      const alerts = await fetchAlertsFromSource(source);
      
      for (const alert of alerts) {
        await WeatherCriticalAlert.updateOne(
          { alert_id: alert.id },
          {
            alert_id: alert.id,
            start_at: new Date(alert.onset),
            end_at: new Date(alert.expires),
            impacted_area: alert.area,
            properties: {
              severity: alert.severity,
              certainty: alert.certainty,
              urgency: alert.urgency,
              event_type: alert.event,
              headline: alert.headline,
              description: alert.description,
              instruction: alert.instruction,
              sender: alert.sender,
              web_url: alert.web,
              source: source
            },
            geometry: alert.geometry
          },
          { upsert: true }
        );
      }
    } catch (error) {
      logger.error(`Weather data ingestion error from ${source}: ${error.message}`);
    }
  }
};
```

## Cleanup and Maintenance
Automated cleanup of expired weather alerts:

```javascript
const cleanupExpiredWeatherAlerts = async () => {
  const currentTime = new Date();
  
  // Remove alerts that ended more than 24 hours ago
  const cleanupThreshold = moment().subtract(24, 'hours').toDate();
  
  const result = await WeatherCriticalAlert.deleteMany({
    end_at: { $lt: cleanupThreshold }
  });
  
  logger.info(`Cleaned up ${result.deletedCount} expired weather alerts`);
  
  return result.deletedCount;
};
```

## Related Models
- WeatherGridRegionCode: Geographic weather impact zones
- InternalUserTag: User classification for targeted alerts
- NotificationRecord: Weather alert delivery tracking
- TripRecords: Travel pattern analysis for weather impact

## API Integration
- National Weather Service alerts
- Local emergency management systems
- Commercial weather API providers
- Geographic information systems
- User notification delivery services

## Development Notes
- Critical for user safety and travel planning
- Requires real-time weather data processing
- Supports multiple weather data sources
- Optimized for geospatial queries and analysis
- Integration with emergency alert systems and travel planning