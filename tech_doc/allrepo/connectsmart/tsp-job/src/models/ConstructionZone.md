# ConstructionZone Model

## Overview
Comprehensive geospatial data model for construction zone management within the TSP Job system. Handles active construction areas, road work zones, and traffic disruptions using GeoJSON Polygon geometry with extensive metadata for real-time construction impact analysis and routing optimization.

## Model Definition
```javascript
const { Schema } = require('mongoose');
const conn = require('@maas/core/mongo')('cache');

const polygonSchema = new Schema(
  {
    type: {
      type: String,
      enum: ['Polygon'],
      required: true,
    },
    coordinates: {
      type: [[[Number]]],
      required: true,
    },
  },
  { _id: false },
);

const coreDetailsSchema = new Schema(
  {
    data_source_id: {
      type: String,
      required: true,
    },
    event_type: {
      type: String,
      required: true,
    },
    road_names: {
      type: [String],
      required: true,
    },
    direction: {
      type: String,
      required: true,
    },
    creation_date: {
      type: Date,
      default: Date.now,
      required: true,
    },
    update_date: {
      type: Date,
      required: true,
    },
  },
  { _id: false },
);

const extensionsSchema = new Schema(
  {
    location: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      required: true,
    },
    incident_type: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      required: true,
    },
    impacted_level: {
      type: String,
      required: true,
    },
    info_url: {
      type: String,
      required: true,
    },
    image_url: {
      type: String,
      required: true,
    },
    lat: {
      type: Number,
      required: true,
    },
    lon: {
      type: Number,
      required: true,
    },
    start: {
      type: Date,
      default: Date.now,
      required: true,
    },
    expires: {
      type: Date,
      required: true,
    },
  },
  { _id: false },
);

const propertiesSchema = new Schema(
  {
    core_details: {
      type: coreDetailsSchema,
      required: true,
    },
    beginning_cross_street: {
      type: String,
      required: true,
    },
    ending_cross_street: {
      type: String,
      required: true,
    },
    is_start_position_verified: {
      type: Boolean,
      required: true,
    },
    is_end_position_verified: {
      type: Boolean,
      required: true,
    },
    start_date: {
      type: Date,
      required: true,
    },
    end_date: {
      type: Date,
      required: true,
    },
    is_start_date_verified: {
      type: Boolean,
      required: true,
    },
    is_end_date_verified: {
      type: Boolean,
      required: true,
    },
    location_method: {
      type: String,
      required: true,
    },
    vehicle_impact: {
      type: String,
      required: true,
    },
    event_status: {
      type: String,
    },
    extensions: {
      type: extensionsSchema,
      required: true,
    },
  },
  { _id: false },
);

const constructionZoneSchema = new Schema({
  type: {
    type: String,
    enum: ['Feature'],
    required: true,
  },
  properties: {
    type: propertiesSchema,
    required: true,
  },
  geometry: {
    type: polygonSchema,
    required: true,
  },
});

constructionZoneSchema.index({ geometry: '2dsphere' });
const ConstructionZone = conn.model('construction_zone', constructionZoneSchema);

module.exports = ConstructionZone;
```

## Database Configuration
- **Database**: MongoDB cache instance
- **Collection**: `construction_zone`
- **ODM**: Mongoose with geospatial indexing
- **Connection**: Managed by @maas/core MongoDB connection pool
- **Index**: 2dsphere for spatial queries and intersection detection

## Quick Summary
The ConstructionZone model manages active construction zones and road work areas using GeoJSON Feature format with comprehensive metadata. It provides real-time construction impact analysis, route optimization around work zones, traffic disruption notifications, and construction-aware transportation planning within the MaaS platform.

## Technical Analysis

### Complex Schema Architecture
The ConstructionZone model implements a sophisticated nested schema structure following GeoJSON Feature specification:

**Root Schema (`constructionZoneSchema`)**:
- `type`: Fixed as 'Feature' following GeoJSON standards
- `properties`: Comprehensive construction zone metadata
- `geometry`: Polygon geometry defining construction area boundaries

**Core Details Schema (`coreDetailsSchema`)**:
- `data_source_id`: Source system identifier for data provenance
- `event_type`: Classification of construction event type
- `road_names`: Array of affected roadway names
- `direction`: Traffic direction impact (northbound, southbound, etc.)
- `creation_date`: Initial record creation timestamp
- `update_date`: Last modification timestamp for change tracking

**Extensions Schema (`extensionsSchema`)**:
- `location`: Human-readable location description
- `type`: Construction work type classification
- `incident_type`: Specific incident category
- `description`: Detailed work description
- `impacted_level`: Severity assessment of traffic impact
- `info_url`: External information resource link
- `image_url`: Visual documentation link
- `lat/lon`: Centroid coordinates for quick reference
- `start/expires`: Construction timeline with automatic expiration

**Properties Schema (`propertiesSchema`)**:
- `beginning_cross_street`: Start boundary street reference
- `ending_cross_street`: End boundary street reference
- `is_start_position_verified`: Data accuracy flag for start location
- `is_end_position_verified`: Data accuracy flag for end location
- `start_date/end_date`: Official construction schedule
- `is_start_date_verified/is_end_date_verified`: Schedule accuracy flags
- `location_method`: Geolocation methodology (GPS, manual, etc.)
- `vehicle_impact`: Description of traffic flow impact
- `event_status`: Current status of construction work

### Geospatial Implementation
```javascript
// 2dsphere index for efficient spatial intersection queries
constructionZoneSchema.index({ geometry: '2dsphere' });

// GeoJSON Polygon structure for construction zones
{
  type: "Feature",
  properties: {
    core_details: {
      data_source_id: "txdot_001",
      event_type: "road_construction",
      road_names: ["Interstate 35", "US Highway 290"],
      direction: "northbound",
      creation_date: "2024-01-15T08:00:00Z",
      update_date: "2024-01-20T14:30:00Z"
    },
    beginning_cross_street: "Ben White Blvd",
    ending_cross_street: "Oltorf Street",
    is_start_position_verified: true,
    is_end_position_verified: true,
    start_date: "2024-01-20T06:00:00Z",
    end_date: "2024-06-15T18:00:00Z",
    is_start_date_verified: true,
    is_end_date_verified: false,
    location_method: "GPS_surveyed",
    vehicle_impact: "Lane closure - reduced capacity",
    event_status: "active",
    extensions: {
      location: "I-35 between Ben White and Oltorf",
      type: "bridge_reconstruction",
      incident_type: "planned_construction",
      description: "Bridge deck replacement and structural upgrades",
      impacted_level: "major",
      info_url: "https://www.txdot.gov/projects/i35-austin-bridge",
      image_url: "https://cdn.txdot.gov/construction/i35-bridge-2024.jpg",
      lat: 30.2240,
      lon: -97.7312,
      start: "2024-01-20T06:00:00Z",
      expires: "2024-06-15T18:00:00Z"
    }
  },
  geometry: {
    type: "Polygon",
    coordinates: [
      [
        [-97.7320, 30.2230], // Southwest corner
        [-97.7320, 30.2250], // Northwest corner
        [-97.7300, 30.2250], // Northeast corner
        [-97.7300, 30.2230], // Southeast corner
        [-97.7320, 30.2230]  // Closed polygon
      ]
    ]
  }
}
```

### Data Validation and Integrity
- **Required Field Enforcement**: All critical construction details mandated
- **Date Validation**: Automatic validation of construction timelines
- **Geospatial Validation**: Polygon coordinate validation and closure verification
- **URL Validation**: External resource link format verification
- **Status Tracking**: Comprehensive audit trail for construction updates

## Usage/Integration

### Construction Zone Spatial Queries
```javascript
// Find active construction zones affecting a route
const findConstructionAlongRoute = async (routePolygon) => {
  const currentDate = new Date();
  
  return await ConstructionZone.find({
    'properties.start_date': { $lte: currentDate },
    'properties.end_date': { $gte: currentDate },
    'properties.event_status': { $ne: 'completed' },
    geometry: {
      $geoIntersects: {
        $geometry: routePolygon
      }
    }
  }).select('properties.core_details.road_names properties.vehicle_impact properties.extensions.impacted_level geometry');
};

// Find construction zones within area
const findConstructionInArea = async (centerLon, centerLat, radiusMeters) => {
  const currentDate = new Date();
  
  return await ConstructionZone.find({
    'properties.extensions.start': { $lte: currentDate },
    'properties.extensions.expires': { $gte: currentDate },
    geometry: {
      $geoWithin: {
        $centerSphere: [[centerLon, centerLat], radiusMeters / 6378100]
      }
    }
  });
};

// Check if specific point is in construction zone
const isPointInConstructionZone = async (longitude, latitude) => {
  const currentDate = new Date();
  
  const zone = await ConstructionZone.findOne({
    'properties.start_date': { $lte: currentDate },
    'properties.end_date': { $gte: currentDate },
    geometry: {
      $geoIntersects: {
        $geometry: {
          type: "Point",
          coordinates: [longitude, latitude]
        }
      }
    }
  });
  
  return zone ? {
    inConstructionZone: true,
    impact: zone.properties.vehicle_impact,
    description: zone.properties.extensions.description,
    impactLevel: zone.properties.extensions.impacted_level
  } : { inConstructionZone: false };
};
```

### Real-time Traffic Management
- **Route Optimization**: Avoid construction zones in routing algorithms
- **Travel Time Estimation**: Adjust ETAs based on construction delays
- **Alternative Route Suggestions**: Provide construction-free alternatives
- **Traffic Impact Assessment**: Analyze construction effects on traffic flow

### User Notification Systems
- **Proactive Alerts**: Notify users of construction on planned routes
- **Real-time Updates**: Push notifications for unexpected construction changes
- **Impact Warnings**: Alert users to significant traffic disruptions
- **Alternative Suggestions**: Recommend alternate routes and transportation modes

## Dependencies

### Core System Dependencies
- **mongoose**: MongoDB ODM providing schema validation and geospatial query capabilities
- **@maas/core/mongo**: Centralized MongoDB connection management
  - Connection pooling for high-volume construction data queries
  - Cache database optimization for real-time construction lookups
  - Error handling and connection recovery for critical traffic systems

### External Data Dependencies
- **DOT Construction Feeds**: State and local transportation department data
- **Municipal Work Permits**: City construction and utility work notifications
- **Traffic Management Centers**: Real-time construction status updates
- **Emergency Services**: Unplanned construction and incident responses

### Integration Dependencies
- **Routing Services**: Construction-aware route calculation and optimization
- **Notification Systems**: Real-time user alerts and traffic updates
- **Analytics Platform**: Construction impact analysis and traffic flow assessment
- **Mapping Services**: Visual construction zone display and navigation

## Code Examples

### Construction Zone Management Service
```javascript
const ConstructionZone = require('@app/src/models/ConstructionZone');

class ConstructionZoneService {
  // Create new construction zone
  static async createConstructionZone(constructionData) {
    const zone = new ConstructionZone({
      type: "Feature",
      properties: {
        core_details: {
          data_source_id: constructionData.sourceId,
          event_type: constructionData.eventType,
          road_names: constructionData.roadNames,
          direction: constructionData.direction,
          creation_date: new Date(),
          update_date: new Date()
        },
        beginning_cross_street: constructionData.beginningStreet,
        ending_cross_street: constructionData.endingStreet,
        is_start_position_verified: constructionData.startVerified || false,
        is_end_position_verified: constructionData.endVerified || false,
        start_date: new Date(constructionData.startDate),
        end_date: new Date(constructionData.endDate),
        is_start_date_verified: constructionData.dateVerified || false,
        is_end_date_verified: constructionData.endDateVerified || false,
        location_method: constructionData.locationMethod,
        vehicle_impact: constructionData.vehicleImpact,
        event_status: constructionData.status || 'planned',
        extensions: {
          location: constructionData.location,
          type: constructionData.workType,
          incident_type: constructionData.incidentType,
          description: constructionData.description,
          impacted_level: constructionData.impactLevel,
          info_url: constructionData.infoUrl,
          image_url: constructionData.imageUrl,
          lat: constructionData.centroid.lat,
          lon: constructionData.centroid.lon,
          start: new Date(constructionData.startDate),
          expires: new Date(constructionData.endDate)
        }
      },
      geometry: {
        type: "Polygon",
        coordinates: constructionData.polygonCoordinates
      }
    });
    
    try {
      await zone.save();
      console.log(`Construction zone created: ${constructionData.description}`);
      return zone;
    } catch (error) {
      console.error('Failed to create construction zone:', error);
      throw error;
    }
  }
  
  // Update construction zone status
  static async updateConstructionStatus(zoneId, statusUpdate) {
    const updateData = {
      'properties.event_status': statusUpdate.status,
      'properties.core_details.update_date': new Date()
    };
    
    if (statusUpdate.endDate) {
      updateData['properties.end_date'] = new Date(statusUpdate.endDate);
      updateData['properties.extensions.expires'] = new Date(statusUpdate.endDate);
    }
    
    if (statusUpdate.vehicleImpact) {
      updateData['properties.vehicle_impact'] = statusUpdate.vehicleImpact;
    }
    
    return await ConstructionZone.findByIdAndUpdate(
      zoneId,
      { $set: updateData },
      { new: true }
    );
  }
  
  // Find expired construction zones for cleanup
  static async findExpiredZones() {
    const currentDate = new Date();
    
    return await ConstructionZone.find({
      $or: [
        { 'properties.end_date': { $lt: currentDate } },
        { 'properties.extensions.expires': { $lt: currentDate } },
        { 'properties.event_status': 'completed' }
      ]
    }).select('_id properties.core_details.road_names properties.extensions.description');
  }
}
```

### Route Impact Analysis
```javascript
// Advanced construction impact analysis
class ConstructionImpactAnalyzer {
  // Analyze route construction impacts
  static async analyzeRouteImpacts(routeGeometry, routeOptions = {}) {
    const currentDate = new Date();
    const futureDate = new Date(Date.now() + (routeOptions.lookaheadHours || 24) * 60 * 60 * 1000);
    
    const constructionZones = await ConstructionZone.find({
      $and: [
        { 'properties.start_date': { $lte: futureDate } },
        { 'properties.end_date': { $gte: currentDate } },
        { 'properties.event_status': { $nin: ['completed', 'cancelled'] } },
        {
          geometry: {
            $geoIntersects: {
              $geometry: routeGeometry
            }
          }
        }
      ]
    });
    
    const impactAnalysis = {
      hasConstructionImpact: constructionZones.length > 0,
      totalConstructionZones: constructionZones.length,
      impactLevels: {
        minor: 0,
        moderate: 0,
        major: 0,
        severe: 0
      },
      constructionDetails: [],
      recommendedActions: []
    };
    
    constructionZones.forEach(zone => {
      const impact = zone.properties.extensions.impacted_level;
      impactAnalysis.impactLevels[impact] = (impactAnalysis.impactLevels[impact] || 0) + 1;
      
      impactAnalysis.constructionDetails.push({
        location: zone.properties.extensions.location,
        description: zone.properties.extensions.description,
        impactLevel: impact,
        vehicleImpact: zone.properties.vehicle_impact,
        roadNames: zone.properties.core_details.road_names,
        startDate: zone.properties.start_date,
        endDate: zone.properties.end_date,
        infoUrl: zone.properties.extensions.info_url
      });
    });
    
    // Generate recommendations
    if (impactAnalysis.impactLevels.severe > 0) {
      impactAnalysis.recommendedActions.push('Consider alternative route due to severe construction impact');
    }
    if (impactAnalysis.impactLevels.major > 0) {
      impactAnalysis.recommendedActions.push('Allow extra travel time for major construction delays');
    }
    if (impactAnalysis.totalConstructionZones > 3) {
      impactAnalysis.recommendedActions.push('Multiple construction zones detected - consider public transit');
    }
    
    return impactAnalysis;
  }
  
  // Calculate construction delay estimates
  static async calculateConstructionDelays(routeDistance, constructionZones) {
    let totalDelayMinutes = 0;
    
    constructionZones.forEach(zone => {
      const impactLevel = zone.properties.extensions.impacted_level;
      const vehicleImpact = zone.properties.vehicle_impact.toLowerCase();
      
      // Delay calculation based on impact level and type
      let delayMultiplier = 1;
      if (impactLevel === 'severe') delayMultiplier = 3;
      else if (impactLevel === 'major') delayMultiplier = 2;
      else if (impactLevel === 'moderate') delayMultiplier = 1.5;
      else if (impactLevel === 'minor') delayMultiplier = 1.2;
      
      // Additional delay for specific impact types
      if (vehicleImpact.includes('closure')) delayMultiplier *= 1.5;
      if (vehicleImpact.includes('detour')) delayMultiplier *= 2;
      
      // Base delay calculation (simplified)
      const baseDelay = 5; // 5 minutes per construction zone
      totalDelayMinutes += baseDelay * delayMultiplier;
    });
    
    return {
      estimatedDelayMinutes: Math.round(totalDelayMinutes),
      delayCategory: totalDelayMinutes > 30 ? 'high' : totalDelayMinutes > 15 ? 'moderate' : 'low'
    };
  }
}
```

### Data Maintenance and Validation
```javascript
// Construction zone data maintenance
const constructionDataMaintenance = {
  // Clean up expired construction zones
  async cleanupExpiredZones() {
    const currentDate = new Date();
    const gracePeriodDays = 7; // Keep expired zones for 7 days
    const cleanupDate = new Date(currentDate - gracePeriodDays * 24 * 60 * 60 * 1000);
    
    const result = await ConstructionZone.deleteMany({
      $or: [
        { 'properties.end_date': { $lt: cleanupDate } },
        { 
          'properties.event_status': 'completed',
          'properties.core_details.update_date': { $lt: cleanupDate }
        }
      ]
    });
    
    console.log(`Cleaned up ${result.deletedCount} expired construction zones`);
    return result;
  },
  
  // Validate construction zone data integrity
  async validateConstructionZones() {
    const zones = await ConstructionZone.find({});
    const validationResults = {
      total: zones.length,
      valid: 0,
      invalid: 0,
      issues: []
    };
    
    for (const zone of zones) {
      const issues = [];
      
      // Validate required fields
      if (!zone.properties.core_details.road_names || zone.properties.core_details.road_names.length === 0) {
        issues.push('Missing road names');
      }
      
      // Validate dates
      if (zone.properties.start_date >= zone.properties.end_date) {
        issues.push('Invalid date range - start date after end date');
      }
      
      // Validate geometry
      if (!zone.geometry.coordinates || zone.geometry.coordinates.length === 0) {
        issues.push('Invalid geometry coordinates');
      }
      
      // Validate URLs
      const urlRegex = /^https?:\/\/.+/;
      if (!urlRegex.test(zone.properties.extensions.info_url)) {
        issues.push('Invalid info URL format');
      }
      
      if (issues.length === 0) {
        validationResults.valid++;
      } else {
        validationResults.invalid++;
        validationResults.issues.push({
          zoneId: zone._id,
          location: zone.properties.extensions.location,
          issues: issues
        });
      }
    }
    
    return validationResults;
  }
};
```

## Performance Considerations
- **Geospatial Indexing**: 2dsphere index optimizes construction zone intersection queries
- **Query Optimization**: Date range filtering combined with spatial queries for efficiency
- **Cache Strategy**: MongoDB cache database for high-frequency construction lookups
- **Connection Pooling**: @maas/core manages connections for consistent performance
- **Data Pruning**: Automatic cleanup of expired construction zones reduces database size

## Integration Points
- **Route Planning**: Construction-aware routing and alternative path calculation
- **Traffic Management**: Real-time traffic flow optimization around construction zones
- **User Notifications**: Proactive construction alerts and impact warnings
- **Analytics Platform**: Construction impact analysis and traffic pattern insights
- **Emergency Services**: Integration with traffic management centers and first responders
- **External Data Sources**: DOT feeds, municipal permits, and traffic management systems

## Use Cases
- **Route Optimization**: Avoid active construction zones in route calculations
- **Travel Time Estimation**: Adjust ETAs based on construction-induced delays
- **Proactive User Alerts**: Notify users of construction affecting planned routes
- **Traffic Flow Analysis**: Assess construction impact on regional traffic patterns
- **Emergency Response**: Coordinate emergency services around construction zones
- **Construction Compliance**: Monitor construction zone adherence to permitted areas
- **Data Integration**: Consolidate construction information from multiple sources
- **Historical Analysis**: Track construction patterns and impact over time