# UISSchema

## Quick Summary
Comprehensive validation schemas for Unified Incident System (UIS) data handling traffic incidents, flood events, and road closures. Provides geographic validation, temporal validation, polygon geometry validation, and structured data validation for Texas transportation incident management systems.

## Technical Analysis

### Code Structure
```javascript
const Joi = require('joi');
const moment = require('moment-timezone');
const formatToMatch = 'YYYY-MM-DD HH:mm:ss';

// Geographic validation for Texas region
const eventType = Joi.string().valid('incident', 'Flood', 'Closure').required();
const lat = Joi.number().min(28.011111).max(31.399999).required();
const lon = Joi.number().min(-97.499999).max(-93.499999).required();
const latlon = Joi.array().ordered(lon, lat).required();

// Polygon validation with closure requirement
const polygon = Joi.array()
  .items(latlon)
  .min(5)
  .required()
  .custom((value, helpers) => {
    if (value[0][0] === value[value.length - 1][0] && 
        value[0][1] === value[value.length - 1][1]) {
      return value;
    } else {
      return helpers.message(
        `first and last position are not the same: ${value[0]}:${value[value.length - 1]}`
      );
    }
  });

// Time format validation
const timeFormat = Joi.string()
  .required()
  .custom((value, helpers) => {
    const isValidFormat = moment(value, formatToMatch).isValid();
    if (isValidFormat) {
      return value;
    } else {
      return helpers.message(`error: time format not correct: ${value}`);
    }
  });

// Custom validation for start/expires relationship
const startExpiresCheck = (value, helpers) => {
  const { expires, start } = value;
  if (expires > start) {
    return value;
  } else {
    return helpers.message(
      `error: start: ${start}, expires: ${expires} 'expires' must be later than 'start'`
    );
  }
};
```

### Schema Components

#### Geographic Validation
- **lat/lon bounds**: Restricted to Texas geographic region (28.01-31.4°N, -97.5 to -93.5°W)
- **latlon array**: Ordered longitude-first coordinate pairs for GeoJSON compatibility
- **polygon validation**: Ensures proper polygon closure and minimum 5-point requirement

#### Temporal Validation
- **timeFormat**: Strict YYYY-MM-DD HH:mm:ss format using moment.js
- **startExpiresCheck**: Custom validation ensuring logical temporal relationships
- **timezone awareness**: Integrated with moment-timezone for accurate time handling

#### Event Type Schemas
- **IncidentSchemas**: Traffic incidents with detailed metadata and lane information
- **FloodSchemas**: Flood events with simplified structure and optional descriptions
- **ClosureSchemas**: Road closures with roadway information and closure details

#### Detailed Field Validation
```javascript
const incidentRecordFormatted = Joi.object({
  ID: Joi.string().required(),
  ROADWAY_NAME: Joi.string().required(),
  DIRECTION: Joi.string().required(),
  CROSS_STREET_QUAL: Joi.string().required(),
  CROSS_STREET: Joi.string().required(),
  LATITUDE: lat,
  LONGITUDE: lon,
  STATUS: Joi.string().required(),
  // Incident type flags (all required integers)
  HAZMAT_SPILL: Joi.number().integer().required(),
  HEAVY_TRUCK: Joi.number().integer().required(),
  HIGH_WATER: Joi.number().integer().required(),
  ICE_ON_ROADWAY: Joi.number().integer().required(),
  LOST_LOAD: Joi.number().integer().required(),
  ROAD_DEBRIS: Joi.number().integer().required(),
  STALL: Joi.number().integer().required(),
  VEHICLE_FIRE: Joi.number().integer().required(),
  OTHER: Joi.number().integer().required(),
  BUS: Joi.number().integer().required(),
  ACCIDENT: Joi.number().integer().required(),
  CONSTRUCTION: Joi.number().integer().required(),
  // Impact metrics
  VEHICLES_INVOLVED: Joi.number().integer().required(),
  LANES_AFFECTED: Joi.string().required(),
  // Lane blockage information
  MAINLANES_BLOCKED: Joi.number().integer().required(),
  FRONTAGE_LANES_BLOCKED: Joi.number().integer().required(),
  RAMP_LANES_BLOCKED: Joi.number().integer().required(),
  HOV_LANES_BLOCKED: Joi.number().integer().required(),
  SHOULDER_LANES_BLOCKED: Joi.number().integer().required(),
  OPPOSING_MAINLANES_BLOCKED: Joi.number().integer().required(),
  OPPOSING_SHOULDER_LANES_BLOCKED: Joi.number().integer().required(),
  // Timeline information (nullable)
  DETECTION_TIME: Joi.string().allow(null),
  VERIFICATION_TIME: Joi.string().allow(null),
  MOVED_TIME: Joi.string().allow(null),
  CLEARED_TIME: Joi.string().allow(null),
  // Summary information
  LANE_SUMMARY: Joi.string().required(),
  LANE_CROSS_SECTION: Joi.string().required(),
}).required();
```

### Implementation Details
The schema implements Texas-specific geographic bounds to prevent invalid location data. The polygon validation ensures GeoJSON compliance and proper geometric closure. Time validation uses moment.js for robust parsing and timezone handling. The modular design allows specific event types while maintaining common geographic and temporal validation.

## Usage/Integration

### Primary Use Cases
- **Traffic Incident Management**: Validates incident reports from TxDOT and other agencies
- **Emergency Response Coordination**: Ensures accurate geographic and temporal data for first responders
- **Flood Event Tracking**: Validates flood boundary data for public safety alerts
- **Road Closure Management**: Validates planned and emergency road closure information
- **Real-time Traffic Updates**: Ensures data quality for traffic information systems

### Integration Points
```javascript
// UIS data validation
const { IncidentSchemas, FloodSchemas, ClosureSchemas } = require('../schemas/uisSchema');

// Validate incident data
const incidentValidation = IncidentSchemas.validate(incidentData);

// Validate flood event
const floodValidation = FloodSchemas.validate(floodEventData);
```

### Scheduling Context
Used in scheduled jobs that process incident feeds from TxDOT, emergency services, and weather agencies, running every 5-15 minutes to maintain real-time incident awareness.

## Dependencies

### Core Dependencies
- **joi**: Schema validation framework with custom validation support
- **moment-timezone**: Temporal validation and timezone handling
- **mongoose**: MongoDB integration for incident document storage

### External Service Dependencies
- **TxDOT Incident APIs**: Source of traffic incident data
- **National Weather Service**: Flood event data
- **Emergency Services APIs**: Real-time incident feeds
- **MongoDB**: Storage for validated incident documents

### Configuration Requirements
```javascript
// Environment configuration for UIS integration
UIS_DATA_FEED_URL=https://api.txdot.gov/incidents
UIS_TIMEZONE=America/Chicago
UIS_GEO_BOUNDS_ENABLED=true
UIS_MIN_POLYGON_POINTS=5
UIS_MAX_EVENT_DURATION_HOURS=168 // 7 days
INCIDENT_PROCESSING_INTERVAL=300000 // 5 minutes
FLOOD_ALERT_THRESHOLD=6 // hours
```

## Code Examples

### Geographic Validation Usage
```javascript
const { IncidentSchemas } = require('./schemas/uisSchema');

// Validate incident with geographic bounds
const incidentData = {
  event_id: "TXI-2024-001234",
  lat: 30.2672, // Austin, TX
  lon: -97.7431,
  polygon: [
    [-97.7431, 30.2672],
    [-97.7421, 30.2672],
    [-97.7421, 30.2682],
    [-97.7431, 30.2682],
    [-97.7431, 30.2672] // Properly closed polygon
  ],
  type: "incident",
  description: "Multi-vehicle accident on I-35",
  reroute: 1,
  location: "I-35 NB at 15th St",
  start: "2024-01-15 14:30:00",
  expires: "2024-01-15 16:30:00",
  version: {
    update_time: "2024-01-15 14:35:00",
    area_change: false,
    time_change: true
  },
  record_formatted: {
    ID: "TXI-2024-001234",
    ROADWAY_NAME: "Interstate 35",
    DIRECTION: "Northbound",
    CROSS_STREET_QUAL: "at",
    CROSS_STREET: "15th Street",
    LATITUDE: 30.2672,
    LONGITUDE: -97.7431,
    STATUS: "Active",
    HAZMAT_SPILL: 0,
    HEAVY_TRUCK: 1,
    HIGH_WATER: 0,
    ICE_ON_ROADWAY: 0,
    LOST_LOAD: 0,
    ROAD_DEBRIS: 1,
    STALL: 0,
    VEHICLE_FIRE: 0,
    OTHER: 0,
    BUS: 0,
    ACCIDENT: 1,
    CONSTRUCTION: 0,
    VEHICLES_INVOLVED: 3,
    LANES_AFFECTED: "2 left lanes",
    MAINLANES_BLOCKED: 2,
    FRONTAGE_LANES_BLOCKED: 0,
    RAMP_LANES_BLOCKED: 0,
    HOV_LANES_BLOCKED: 0,
    SHOULDER_LANES_BLOCKED: 0,
    OPPOSING_MAINLANES_BLOCKED: 0,
    OPPOSING_SHOULDER_LANES_BLOCKED: 0,
    DETECTION_TIME: "2024-01-15 14:28:00",
    VERIFICATION_TIME: "2024-01-15 14:30:00",
    MOVED_TIME: null,
    CLEARED_TIME: null,
    LANE_SUMMARY: "2 of 4 mainlanes blocked",
    LANE_CROSS_SECTION: "4 lane divided highway"
  }
};

const { error, value } = IncidentSchemas.validate(incidentData);

if (error) {
  console.error('Incident validation failed:', error.details);
} else {
  console.log('Incident validated successfully:', value.event_id);
}
```

### Flood Event Processing
```javascript
// Flood event validation and processing
const processFloodEvent = async (floodData) => {
  try {
    // Validate flood event structure
    const { error, value } = FloodSchemas.validate(floodData);
    
    if (error) {
      throw new ValidationError(`Flood event validation failed: ${error.message}`);
    }
    
    // Check if flood is in high-risk area
    const isHighRiskArea = await checkHighRiskFloodZone(value.lat, value.lon);
    
    // Validate polygon covers reasonable area
    const polygonArea = calculatePolygonArea(value.polygon);
    const maxFloodArea = 1000; // square kilometers
    
    if (polygonArea > maxFloodArea) {
      console.warn(`Large flood area detected: ${polygonArea} km²`);
    }
    
    // Calculate duration
    const startTime = moment(value.start, 'YYYY-MM-DD HH:mm:ss');
    const endTime = moment(value.expires, 'YYYY-MM-DD HH:mm:ss');
    const durationHours = endTime.diff(startTime, 'hours');
    
    // Extended flood events require special handling
    if (durationHours > 24) {
      await notificationService.alertEmergencyServices('Extended flood event', {
        eventId: value.event_id,
        duration: durationHours,
        location: value.location,
        area: polygonArea
      });
    }
    
    return {
      validatedEvent: value,
      isHighRisk: isHighRiskArea,
      polygonArea,
      durationHours
    };
    
  } catch (error) {
    logger.error('Flood event processing failed', { floodData, error });
    throw error;
  }
};
```

### Incident Feed Processing
```javascript
// Process incident feed from external source
const processIncidentFeed = async () => {
  try {
    // Fetch latest incident data
    const response = await fetch(process.env.UIS_DATA_FEED_URL);
    const incidents = await response.json();
    
    const processingResults = {
      total: incidents.length,
      valid: 0,
      invalid: 0,
      errors: []
    };
    
    for (const incident of incidents) {
      try {
        // Validate incident structure
        const { error, value } = IncidentSchemas.validate(incident);
        
        if (error) {
          processingResults.invalid++;
          processingResults.errors.push({
            incidentId: incident.event_id || 'unknown',
            error: error.message
          });
          continue;
        }
        
        // Additional business logic validation
        const validationResult = await validateIncidentBusinessRules(value);
        
        if (!validationResult.isValid) {
          processingResults.invalid++;
          processingResults.errors.push({
            incidentId: value.event_id,
            error: validationResult.reason
          });
          continue;
        }
        
        // Store valid incident
        await saveIncidentToDatabase(value);
        
        // Trigger alerts if needed
        if (shouldTriggerAlert(value)) {
          await triggerIncidentAlert(value);
        }
        
        processingResults.valid++;
        
      } catch (processingError) {
        logger.error('Individual incident processing failed', {
          incident: incident.event_id,
          error: processingError
        });
        processingResults.invalid++;
      }
    }
    
    logger.info('Incident feed processing completed', processingResults);
    
    return processingResults;
    
  } catch (error) {
    logger.error('Incident feed processing failed', error);
    throw error;
  }
};
```

### Time Validation and Timezone Handling
```javascript
// Comprehensive time validation utilities
const TimeValidationUtils = {
  // Validate time format and range
  validateEventTime: (timeString, context = 'general') => {
    const timeFormat = 'YYYY-MM-DD HH:mm:ss';
    const parsedTime = moment(timeString, timeFormat);
    
    if (!parsedTime.isValid()) {
      throw new Error(`Invalid time format: ${timeString}`);
    }
    
    // Check if time is reasonable (not too far in past or future)
    const now = moment();
    const maxPastHours = 168; // 7 days
    const maxFutureHours = 168; // 7 days
    
    const hoursDiff = now.diff(parsedTime, 'hours');
    
    if (hoursDiff > maxPastHours) {
      console.warn(`Event time is ${hoursDiff} hours in the past: ${timeString}`);
    }
    
    if (hoursDiff < -maxFutureHours) {
      console.warn(`Event time is ${Math.abs(hoursDiff)} hours in the future: ${timeString}`);
    }
    
    return parsedTime;
  },
  
  // Validate start/expires relationship with business rules
  validateTimeRange: (startTime, expiresTime, eventType) => {
    const start = moment(startTime, 'YYYY-MM-DD HH:mm:ss');
    const expires = moment(expiresTime, 'YYYY-MM-DD HH:mm:ss');
    
    if (!start.isValid() || !expires.isValid()) {
      throw new Error('Invalid time format in time range');
    }
    
    if (expires.isSameOrBefore(start)) {
      throw new Error(`Expires time must be after start time: ${startTime} -> ${expiresTime}`);
    }
    
    const durationHours = expires.diff(start, 'hours');
    
    // Event type specific duration limits
    const maxDurations = {
      incident: 48, // 2 days max
      Flood: 168, // 7 days max
      Closure: 720 // 30 days max for planned closures
    };
    
    const maxDuration = maxDurations[eventType] || 168;
    
    if (durationHours > maxDuration) {
      console.warn(`Event duration (${durationHours}h) exceeds maximum for ${eventType} (${maxDuration}h)`);
    }
    
    return {
      durationHours,
      isValid: true,
      start: start.toDate(),
      expires: expires.toDate()
    };
  }
};
```

### Polygon Geometry Validation
```javascript
// Advanced polygon validation utilities
const PolygonValidationUtils = {
  // Validate polygon geometry and closure
  validatePolygon: (polygon) => {
    // Check minimum points
    if (polygon.length < 5) {
      throw new Error(`Polygon must have at least 5 points, got ${polygon.length}`);
    }
    
    // Check closure
    const firstPoint = polygon[0];
    const lastPoint = polygon[polygon.length - 1];
    
    if (firstPoint[0] !== lastPoint[0] || firstPoint[1] !== lastPoint[1]) {
      throw new Error('Polygon is not closed - first and last points must be identical');
    }
    
    // Check for self-intersection (basic check)
    const hasIntersection = checkPolygonSelfIntersection(polygon);
    if (hasIntersection) {
      console.warn('Polygon may have self-intersections');
    }
    
    // Calculate area
    const area = calculatePolygonArea(polygon);
    
    // Validate reasonable area (not too small or too large)
    const minArea = 0.0001; // ~100m²
    const maxArea = 10000; // 10,000 km²
    
    if (area < minArea) {
      console.warn(`Very small polygon area: ${area} km²`);
    }
    
    if (area > maxArea) {
      console.warn(`Very large polygon area: ${area} km²`);
    }
    
    return {
      isValid: true,
      pointCount: polygon.length,
      area,
      perimeter: calculatePolygonPerimeter(polygon)
    };
  },
  
  // Check if point is within Texas bounds
  isWithinTexasBounds: (lat, lon) => {
    return lat >= 28.011111 && lat <= 31.399999 && 
           lon >= -97.499999 && lon <= -93.499999;
  },
  
  // Validate all polygon points are within bounds
  validatePolygonBounds: (polygon) => {
    const outOfBoundsPoints = [];
    
    for (let i = 0; i < polygon.length; i++) {
      const [lon, lat] = polygon[i];
      
      if (!PolygonValidationUtils.isWithinTexasBounds(lat, lon)) {
        outOfBoundsPoints.push({
          index: i,
          coordinates: [lon, lat],
          reason: 'Outside Texas geographic bounds'
        });
      }
    }
    
    if (outOfBoundsPoints.length > 0) {
      throw new Error(`Polygon has ${outOfBoundsPoints.length} points outside Texas bounds`);
    }
    
    return true;
  }
};
```

## Related Components
- **IncidentsEvent model**: Database model for storing validated incident data
- **update-incident-events job**: Scheduled job processing UIS feeds using these schemas
- **TransitAlert service**: Integration with incident data for transit disruption alerts
- **Emergency notification services**: Real-time alerting based on validated incident data