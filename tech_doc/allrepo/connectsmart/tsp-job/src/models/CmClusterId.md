# CmClusterId.js - TSP Job Model Documentation

## Quick Summary

The CmClusterId model manages activity location clustering data within the TSP Job scheduling system, specifically for the M3 experiment compensation program. This Objection.js ORM model provides database access to the `cm_cluster_id` table in the portal database, storing cluster identifiers that link habitual travel patterns to MongoDB-stored trip clustering data. The model is essential for validating user compensation eligibility by matching actual trips with predicted habitual travel behavior in mobility incentive programs.

## Technical Analysis

### Code Structure
```javascript
const knex = require('@maas/core/mysql')('portal');
class CmClusterId extends Model {
  static get tableName() {
    return 'cm_cluster_id';
  }
}
module.exports = CmClusterId.bindKnex(knex);
```

### Implementation Bug
Consistent with other models in the codebase, this model extends the `Model` class without the required import:
```javascript
const { Model } = require('objection');
```

### Database Architecture
- **Database**: `portal` (MySQL connection via @maas/core)
- **Table**: `cm_cluster_id`
- **Role**: Bridge between MySQL activity location data and MongoDB trip clustering collections
- **Integration**: Links M3 experiment tiles with clustered trip pattern analysis

### Clustering System Design
The model facilitates a sophisticated clustering system that:
- **Habitual Pattern Recognition**: Identifies common origin-destination pairs for users
- **Geographic Clustering**: Groups similar trips by location proximity and frequency
- **Behavioral Analysis**: Analyzes user travel patterns for predictive modeling
- **Compensation Validation**: Verifies user behavior changes for incentive eligibility
- **Cross-database Integration**: Bridges MySQL operational data with MongoDB analytics storage

## Usage/Integration

### M3 Compensation Job Integration

**Primary Usage in `src/jobs/m3_compensation.js`**:
The model is central to the M3 experiment compensation validation system that processes:
- **Behavior Change Validation**: Confirms users have modified transportation modes as incentivized
- **Geographic Validation**: Verifies trips occur within expected habitual location clusters
- **Distance Validation**: Ensures trips meet minimum distance requirements (>1 mile, within 5km of cluster)
- **Incentive Distribution**: Triggers point rewards for validated behavior changes

### Clustering Data Pipeline

**Integration with MongoDB ClusterTrips Collection**:
```javascript
// From m3_compensation.js - retrieving habitual patterns
const getHabitualLatLon = async (experimentId) => {
  const tripOID = await knex('cm_cluster_id')
    .innerJoin('m3_experiment_tile', 'cm_cluster_id.id', 'm3_experiment_tile.activity_location_id')
    .where('m3_experiment_tile.id', experimentId);
    
  const cluster = await ClusterTrips.findOne({ 
    _id: ObjectId(tripOID[0].cluster_id) 
  }).lean();
  
  return {
    origin: [cluster.common_start_location.coordinates[1], cluster.common_start_location.coordinates[0]],
    destination: [cluster.common_end_location.coordinates[1], cluster.common_end_location.coordinates[0]]
  };
};
```

### Experiment Management System

**M3 Experiment Tile Association**:
- **Experiment Tracking**: Links cluster data to specific M3 mobility experiments
- **Activity Location Mapping**: Associates clusters with user activity locations
- **Behavioral Baseline**: Establishes pre-experiment travel patterns for comparison
- **Validation Criteria**: Defines geographic and temporal boundaries for trip validation

### Geographic Validation Logic

**Distance-Based Validation**:
- **Origin Proximity**: Validates trip start points within 5km of cluster origin
- **Destination Proximity**: Confirms trip end points within 5km of cluster destination
- **Haversine Distance Calculation**: Precise geographic distance measurement
- **Clustering Tolerance**: Accounts for natural variation in habitual travel patterns

## Dependencies

### Core Framework Dependencies
- **@maas/core/mysql**: Database connection management for portal database
- **objection**: ORM framework (missing import - critical bug)
- **knex**: SQL query builder (provided through @maas/core)
- **mongodb**: MongoDB ObjectId handling for cross-database operations

### Geographic and Mathematical Dependencies
- **haversine-distance**: Precise geographic distance calculations between coordinates
- **@turf/turf**: Advanced geospatial analysis and geometric operations
- **moment-timezone**: Date/time processing for temporal analysis
- **ObjectId**: MongoDB document identifier handling

### Related Model Dependencies
- **ClusterTrips**: MongoDB collection storing clustered trip pattern data
- **M3ExperimentTile**: Experiment configuration and tile management
- **M3Compensation**: Compensation record management and validation tracking
- **Trip**: Individual trip data for validation against clusters
- **Telework**: Trip automation and logging data

### Machine Learning and Analytics Dependencies
- **Clustering Algorithms**: K-means or similar algorithms for trip pattern grouping
- **Geospatial Analysis**: Location-based clustering and proximity analysis
- **Behavioral Analytics**: Pattern recognition and change detection
- **Statistical Validation**: Confidence intervals and significance testing

## Code Examples

### Cluster Data Retrieval
```javascript
const CmClusterId = require('@app/src/models/CmClusterId');

// Get cluster information for experiment validation
const getClusterForExperiment = async (experimentId) => {
  const clusterMapping = await CmClusterId.query()
    .join('m3_experiment_tile', 'cm_cluster_id.id', 'm3_experiment_tile.activity_location_id')
    .where('m3_experiment_tile.id', experimentId)
    .select(
      'cm_cluster_id.*',
      'm3_experiment_tile.experiment_id',
      'm3_experiment_tile.tile_config'
    )
    .first();
    
  if (!clusterMapping) {
    throw new Error(`No cluster mapping found for experiment ${experimentId}`);
  }
  
  return clusterMapping;
};
```

### Cross-Database Cluster Analysis
```javascript
// Retrieve complete cluster data from MySQL and MongoDB
const getCompleteClusterData = async (clusterId) => {
  // Get cluster metadata from MySQL
  const clusterMeta = await CmClusterId.query()
    .findById(clusterId)
    .withGraphJoined('[experiment_tiles, activity_locations]');
    
  // Get detailed cluster analysis from MongoDB
  const clusterDetails = await ClusterTrips.findOne({
    _id: ObjectId(clusterMeta.cluster_id)
  }).lean();
  
  return {
    id: clusterId,
    metadata: clusterMeta,
    analysis: clusterDetails,
    habitual_origin: {
      lat: clusterDetails.common_start_location.coordinates[1],
      lng: clusterDetails.common_start_location.coordinates[0]
    },
    habitual_destination: {
      lat: clusterDetails.common_end_location.coordinates[1],
      lng: clusterDetails.common_end_location.coordinates[0]
    },
    trip_count: clusterDetails.trip_count,
    confidence_score: clusterDetails.confidence_score
  };
};
```

### Trip Validation Against Clusters
```javascript
// Validate trip against habitual cluster (from m3_compensation.js)
const validateTripAgainstCluster = async (tripData, experimentId) => {
  const habituals = await getHabitualLatLon(experimentId);
  const limitMeter = 5000; // 5km tolerance
  
  // Calculate distances using haversine formula
  const originDistance = haversine(habituals.origin, [
    tripData.origin_latitude,
    tripData.origin_longitude
  ]);
  
  const destinationDistance = haversine(habituals.destination, [
    tripData.destination_latitude,
    tripData.destination_longitude
  ]);
  
  // Validate proximity to habitual patterns
  const isValidTrip = originDistance <= limitMeter && destinationDistance <= limitMeter;
  
  return {
    valid: isValidTrip,
    origin_distance: originDistance,
    destination_distance: destinationDistance,
    habitual_origin: habituals.origin,
    habitual_destination: habituals.destination,
    validation_threshold: limitMeter
  };
};
```

### Cluster Creation and Management
```javascript
// Create new cluster mapping for experiment
const createClusterMapping = async (experimentData) => {
  // First, create the clustering analysis in MongoDB
  const clusterAnalysis = await ClusterTrips.create({
    user_id: experimentData.user_id,
    common_start_location: {
      type: 'Point',
      coordinates: [experimentData.habitual_origin.lng, experimentData.habitual_origin.lat]
    },
    common_end_location: {
      type: 'Point',
      coordinates: [experimentData.habitual_destination.lng, experimentData.habitual_destination.lat]
    },
    trip_count: experimentData.historical_trips.length,
    confidence_score: experimentData.clustering_confidence,
    created_at: new Date()
  });
  
  // Create MySQL mapping record
  const clusterMapping = await CmClusterId.query().insert({
    cluster_id: clusterAnalysis._id.toString(),
    user_id: experimentData.user_id,
    activity_type: experimentData.activity_type,
    created_at: new Date(),
    confidence_threshold: experimentData.clustering_confidence,
    geographic_tolerance: 5000 // 5km default tolerance
  });
  
  return {
    mapping_id: clusterMapping.id,
    cluster_id: clusterAnalysis._id,
    habitual_pattern: {
      origin: experimentData.habitual_origin,
      destination: experimentData.habitual_destination
    }
  };
};
```

### Compensation Validation Integration
```javascript
// Complete compensation validation workflow
const validateCompensationEligibility = async (compensationId) => {
  const compensation = await knex('m3_compensation')
    .where('id', compensationId)
    .first();
    
  if (!compensation) {
    throw new Error('Compensation record not found');
  }
  
  // Get user's habitual travel pattern
  const clusterData = await getCompleteClusterData(compensation.cluster_id);
  
  // Get user's actual trips during experiment period
  const userTrips = await knex('trip')
    .join('telework', 'trip.id', 'telework.trip_id')
    .where('trip.user_id', compensation.user_id)
    .where('telework.started_on', '>=', compensation.deliver_time)
    .where('telework.started_on', '<', compensation.validate_time)
    .where('trip.distance', '>', 1609.344) // > 1 mile
    .whereIn('trip.travel_mode', [2, 3, 4, 5]); // Valid travel modes
    
  let validationPassed = false;
  
  for (const trip of userTrips) {
    const validation = await validateTripAgainstCluster(trip, compensation.experiment_id);
    
    if (validation.valid) {
      // Update compensation record with validation details
      await knex('m3_compensation')
        .where('id', compensationId)
        .update({
          changed_mode: trip.travel_mode,
          trip_id: trip.id,
          processed: 1,
          validation_distance_origin: validation.origin_distance,
          validation_distance_destination: validation.destination_distance,
          validated_at: new Date()
        });
        
      validationPassed = true;
      break;
    }
  }
  
  if (!validationPassed) {
    await knex('m3_compensation')
      .where('id', compensationId)
      .update({
        processed: 1,
        validation_failed: true,
        validation_reason: 'No trips matched habitual cluster pattern'
      });
  }
  
  return validationPassed;
};
```

### Analytics and Monitoring
```javascript
// Generate cluster performance analytics
const getClusterAnalytics = async (dateRange) => {
  const analytics = await CmClusterId.query()
    .join('m3_experiment_tile', 'cm_cluster_id.id', 'm3_experiment_tile.activity_location_id')
    .join('m3_compensation', 'm3_experiment_tile.id', 'm3_compensation.experiment_id')
    .where('m3_compensation.created_at', '>=', dateRange.start)
    .where('m3_compensation.created_at', '<=', dateRange.end)
    .select(
      knex.raw('COUNT(DISTINCT cm_cluster_id.id) as total_clusters'),
      knex.raw('COUNT(m3_compensation.id) as total_compensations'),
      knex.raw('SUM(CASE WHEN m3_compensation.processed = 1 AND m3_compensation.trip_id IS NOT NULL THEN 1 ELSE 0 END) as successful_validations'),
      knex.raw('AVG(cm_cluster_id.confidence_threshold) as avg_confidence'),
      knex.raw('AVG(cm_cluster_id.geographic_tolerance) as avg_tolerance')
    )
    .first();
    
  return {
    ...analytics,
    validation_rate: (analytics.successful_validations / analytics.total_compensations * 100).toFixed(2),
    cluster_efficiency: (analytics.successful_validations / analytics.total_clusters).toFixed(2)
  };
};
```

This model serves as a critical component in the sophisticated mobility behavior analysis and incentive validation system, enabling precise geographic and behavioral validation of user travel pattern changes while bridging operational MySQL data with advanced MongoDB-based clustering analytics for comprehensive mobility intelligence.