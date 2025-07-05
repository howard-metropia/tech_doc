# HNTB Habitual Trip Origin Migration Documentation

## Quick Summary

The HNTB Habitual Trip Origin migration creates a specialized table for tracking recurring trip patterns and frequently used origin locations within the HNTB transportation research platform. This migration establishes the `hntb_habitual_trip_origin` table that captures detailed origin location information for habitual trip analysis, enabling researchers to identify regular travel patterns, common departure points, and behavioral consistency in transportation choices. The table serves as a critical component for understanding user mobility patterns and supporting predictive modeling for transportation planning.

**Key Features:**
- Activity-based primary key system linking to user activity patterns
- Comprehensive location data with both coordinates and descriptive information
- User correlation through flexible identification fields for longitudinal tracking
- Geographic precision with double-precision latitude and longitude storage
- Location naming and addressing support for human-readable location identification
- Automatic timestamp management for temporal pattern analysis and data integrity

## Technical Analysis

### Database Schema Structure

The migration implements a comprehensive table schema optimized for habitual trip origin tracking and location analysis:

```javascript
const tableName = 'hntb_habitual_trip_origin';

exports.up = async function (knex) {
  try {
    await knex.schema.createTable(tableName, (table) => {
      table.integer('activity_id').unsigned().primary();
      table.string('user_id', 256).notNullable();
      table.integer('location_id').notNullable();
      table.string('name', 256).nullable();
      table.string('address', 256).nullable();
      table.double('lat').notNullable();
      table.double('lng').notNullable();
      table.dateTime('created_on').notNullable().defaultTo(knex.raw('CURRENT_TIMESTAMP'));
      table.dateTime('modified_on').notNullable().defaultTo(knex.raw('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'));
      table.unique(['activity_id'], { indexName: 'activity_id' });
    });
  } catch (e) {
    logger.error(e.message);
    await knex.schema.dropTableIfExists(tableName);
    throw new Error(e);
  }
};
```

### Field Specifications and Data Types

**Primary Identification System:**
- `activity_id`: Unsigned integer serving as the primary key for unique activity identification
- Links directly to specific user activities and behavioral patterns
- Unique constraint ensures one-to-one relationship with activity records

**User and Location Association:**
- `user_id`: 256-character string field enabling cross-study user correlation
- Non-nullable constraint ensures every origin record is associated with a research participant
- `location_id`: Integer field linking to standardized location database entries

**Geographic Coordinate System:**
- `lat`: Double precision field for accurate latitude coordinates
- `lng`: Double precision field for accurate longitude coordinates
- Both coordinates are required (notNullable) ensuring complete geographic data
- High precision supports detailed spatial analysis and clustering algorithms

**Location Description Fields:**
- `name`: Optional 256-character field for location identifiers or common names
- `address`: Optional 256-character field for structured address information
- Nullable fields provide flexibility for various data collection scenarios
- Supports both formal addresses and user-defined location names

**Audit Trail Management:**
- `created_on`: Automatic timestamp generation using MySQL CURRENT_TIMESTAMP
- Records exact moment of origin location registration
- `modified_on`: Auto-updating timestamp with ON UPDATE CURRENT_TIMESTAMP trigger
- Tracks any modifications to location data or user associations

### Error Handling and Transaction Safety

The migration implements comprehensive error handling with automatic cleanup mechanisms:

```javascript
catch (e) {
  logger.error(e.message);
  await knex.schema.dropTableIfExists(tableName);
  throw new Error(e);
}
```

**Safety Features:**
- Automatic table cleanup on migration failure prevents inconsistent schema states
- Integration with @maas/core/log system for centralized error monitoring
- Exception re-throwing maintains proper error propagation through the system
- Transaction-safe operations ensure database consistency during deployment

### Rollback Implementation

```javascript
exports.down = async function (knex) {
  await knex.schema.dropTable(tableName);
};
```

The rollback function provides complete migration reversal by removing the entire table structure, ensuring clean environment restoration for testing and development scenarios.

## Usage/Integration

### Migration Execution Context

**Database Connection:**
- Utilizes Knex.js query builder for standardized database schema management
- Operates within the TSP Job service database infrastructure
- Integrates with the comprehensive HNTB research platform ecosystem

**Migration Timing:**
- Timestamp: March 28, 2025, 02:11:24 GMT (20250328021124)
- Follows user targeting and travel time analysis migrations
- Supports advanced pattern recognition and behavioral analysis capabilities

### Integration with Habitual Trip Analysis

**Habitual Origin Tracking Workflow:**
1. User activity patterns identified through trip frequency analysis
2. Origin locations extracted from historical trip data
3. Geographic clustering applied to identify common departure points
4. Location metadata collected including names and addresses
5. Habitual origin records created with comprehensive location data
6. Pattern analysis performed for predictive modeling and planning

**Research Applications:**
- Identification of frequently used origin points for transportation planning
- Analysis of user mobility patterns and behavioral consistency
- Predictive modeling for trip destination and timing
- Location-based service optimization for transportation providers
- Urban planning insights through aggregated origin pattern analysis

### Application Integration Points

**Service Layer Integration:**
```javascript
// Example usage in habitual trip analysis services
const habitualOriginData = {
  activity_id: userActivity.id,
  user_id: authenticatedUser.id,
  location_id: identifyLocationCluster(coordinates),
  name: locationMetadata.commonName,
  address: await reverseGeocode(coordinates),
  lat: coordinates.latitude,
  lng: coordinates.longitude
};

await knex('hntb_habitual_trip_origin').insert(habitualOriginData);

// Query habitual origins for pattern analysis
const userOrigins = await knex('hntb_habitual_trip_origin')
  .where('user_id', userId)
  .select('*')
  .orderBy('created_on', 'desc');
```

**Analytics Integration:**
- Powers origin-destination flow analysis and visualization
- Enables spatial clustering analysis for transportation planning
- Supports predictive modeling for trip planning and routing
- Facilitates location-based behavioral pattern recognition

## Dependencies

### Core Framework Dependencies

**Knex.js Query Builder:**
- Version compatibility with TSP Job service Knex configuration
- Requires MySQL database connection with appropriate geographic data handling
- Utilizes Knex migration system for version control and deployment automation

**@maas/core/log System:**
```javascript
const { logger } = require('@maas/core/log');
```
- Integrates with centralized logging infrastructure for comprehensive error tracking
- Provides structured error reporting and audit trail capabilities
- Supports distributed logging across the microservice architecture

### Database Requirements

**MySQL Database System:**
- Requires MySQL 5.7+ for proper double precision handling and timestamp functionality
- Utilizes CURRENT_TIMESTAMP and ON UPDATE CURRENT_TIMESTAMP features
- Depends on proper timezone configuration for accurate temporal tracking

**Geographic Data Handling:**
- Double precision support for accurate coordinate storage
- Spatial indexing capabilities for efficient geographic queries
- Proper collation settings for address and name field handling

### Platform Integration Dependencies

**HNTB Research Platform:**
- Coordinates with activity management systems for activity_id validation
- Integrates with user management systems for participant tracking
- Connects with location clustering algorithms for origin identification
- Supports geographic information systems for spatial analysis

**TSP Job Service Architecture:**
- Operates within TSP Job microservice context for scalable processing
- Utilizes shared database connection pooling for optimal performance
- Integrates with background job processing systems for pattern analysis

## Code Examples

### Migration Execution Commands

**Running the Migration:**
```bash
# Execute migration in TSP Job service context
cd allrepo/connectsmart/tsp-job
npx knex migrate:up --env production

# Verify migration status and table structure
npx knex migrate:status
mysql -e "DESCRIBE hntb_habitual_trip_origin;"
```

**Migration Rollback:**
```bash
# Rollback specific migration
npx knex migrate:down --env production

# Rollback to previous version
npx knex migrate:rollback --to=20250328021124
```

### Database Interaction Examples

**Habitual Origin Registration:**
```javascript
const knex = require('./database/connection');

// Register new habitual trip origin
const registerHabitualOrigin = async (activityData, locationData) => {
  const originData = {
    activity_id: activityData.id,
    user_id: activityData.userId,
    location_id: await identifyOrCreateLocation(locationData),
    name: locationData.name || await generateLocationName(locationData),
    address: locationData.address || await reverseGeocode(locationData.coordinates),
    lat: locationData.coordinates.latitude,
    lng: locationData.coordinates.longitude
  };
  
  const result = await knex('hntb_habitual_trip_origin').insert(originData);
  return result;
};

// Query origins with geographic filtering
const getNearbyOrigins = async (centerPoint, radiusKm) => {
  const earthRadiusKm = 6371;
  const lat1Rad = centerPoint.lat * Math.PI / 180;
  const lng1Rad = centerPoint.lng * Math.PI / 180;
  
  return await knex('hntb_habitual_trip_origin')
    .select('*')
    .whereRaw(`
      ${earthRadiusKm} * acos(
        cos(${lat1Rad}) * cos(lat * PI() / 180) *
        cos((lng * PI() / 180) - ${lng1Rad}) +
        sin(${lat1Rad}) * sin(lat * PI() / 180)
      ) <= ${radiusKm}
    `)
    .orderBy('created_on', 'desc');
};
```

**Habitual Pattern Analysis:**
```javascript
// Identify user's most frequent origins
const getUserTopOrigins = async (userId, limit = 10) => {
  return await knex('hntb_habitual_trip_origin')
    .where('user_id', userId)
    .select('location_id', 'name', 'address', 'lat', 'lng')
    .count('* as frequency')
    .groupBy('location_id', 'name', 'address', 'lat', 'lng')
    .orderBy('frequency', 'desc')
    .limit(limit);
};

// Geographic clustering analysis
const analyzeOriginClusters = async (boundingBox) => {
  return await knex('hntb_habitual_trip_origin')
    .whereBetween('lat', [boundingBox.minLat, boundingBox.maxLat])
    .whereBetween('lng', [boundingBox.minLng, boundingBox.maxLng])
    .select('lat', 'lng', 'name')
    .count('* as origin_frequency')
    .groupBy('lat', 'lng', 'name')
    .having('origin_frequency', '>', 5)
    .orderBy('origin_frequency', 'desc');
};

// Temporal pattern analysis
const analyzeTemporalPatterns = async (userId) => {
  return await knex('hntb_habitual_trip_origin')
    .where('user_id', userId)
    .select(
      knex.raw('HOUR(created_on) as hour_of_day'),
      knex.raw('DAYOFWEEK(created_on) as day_of_week'),
      'location_id',
      'name'
    )
    .count('* as frequency')
    .groupBy('hour_of_day', 'day_of_week', 'location_id', 'name')
    .orderBy(['day_of_week', 'hour_of_day', 'frequency'], ['asc', 'asc', 'desc']);
};
```

### Geographic Analysis Functions

**Spatial Clustering Implementation:**
```javascript
// K-means clustering for origin locations
const clusterOrigins = async (userId, numClusters = 5) => {
  const origins = await knex('hntb_habitual_trip_origin')
    .where('user_id', userId)
    .select('lat', 'lng', 'activity_id', 'name');
  
  if (origins.length < numClusters) {
    return origins.map(origin => ({ ...origin, cluster_id: 0 }));
  }
  
  // Simple k-means implementation
  const clusters = initializeClusters(origins, numClusters);
  let iterations = 0;
  const maxIterations = 100;
  
  while (iterations < maxIterations) {
    const newClusters = assignToClosestCluster(origins, clusters);
    const updatedCentroids = calculateNewCentroids(newClusters);
    
    if (clustersConverged(clusters, updatedCentroids)) {
      break;
    }
    
    clusters.forEach((cluster, index) => {
      cluster.centroid = updatedCentroids[index];
    });
    
    iterations++;
  }
  
  return assignClusterIds(origins, clusters);
};

// Calculate distance between two geographic points
const calculateDistance = (point1, point2) => {
  const earthRadiusKm = 6371;
  const dLat = (point2.lat - point1.lat) * Math.PI / 180;
  const dLng = (point2.lng - point1.lng) * Math.PI / 180;
  
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(point1.lat * Math.PI / 180) * Math.cos(point2.lat * Math.PI / 180) *
    Math.sin(dLng / 2) * Math.sin(dLng / 2);
  
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return earthRadiusKm * c;
};

// Identify location clusters and representative points
const identifyOriginHotspots = async (regionBounds, minOrigins = 10) => {
  const origins = await knex('hntb_habitual_trip_origin')
    .whereBetween('lat', [regionBounds.minLat, regionBounds.maxLat])
    .whereBetween('lng', [regionBounds.minLng, regionBounds.maxLng])
    .select('lat', 'lng', 'user_id', 'name');
  
  const clusters = await performDBSCAN(origins, 0.5, minOrigins); // 500m radius
  
  return clusters.map(cluster => ({
    centroid: calculateCentroid(cluster.points),
    pointCount: cluster.points.length,
    uniqueUsers: [...new Set(cluster.points.map(p => p.user_id))].length,
    commonNames: getCommonNames(cluster.points),
    bounds: calculateBounds(cluster.points)
  }));
};
```

### Location Data Management

**Address and Name Processing:**
```javascript
// Normalize and validate location data
const normalizeLocationData = async (rawLocationData) => {
  const normalized = {
    coordinates: {
      lat: parseFloat(rawLocationData.lat),
      lng: parseFloat(rawLocationData.lng)
    },
    name: rawLocationData.name ? rawLocationData.name.trim() : null,
    address: rawLocationData.address ? rawLocationData.address.trim() : null
  };
  
  // Validate coordinates
  if (Math.abs(normalized.coordinates.lat) > 90 || Math.abs(normalized.coordinates.lng) > 180) {
    throw new Error('Invalid coordinates provided');
  }
  
  // Generate name if not provided
  if (!normalized.name && normalized.address) {
    normalized.name = extractLocationName(normalized.address);
  }
  
  // Reverse geocode for address if not provided
  if (!normalized.address) {
    normalized.address = await reverseGeocodeCoordinates(normalized.coordinates);
  }
  
  return normalized;
};

// Merge similar origin locations
const mergeNearbyOrigins = async (userId, mergeDistanceKm = 0.1) => {
  const userOrigins = await knex('hntb_habitual_trip_origin')
    .where('user_id', userId)
    .orderBy('created_on');
  
  const merged = [];
  const processed = new Set();
  
  for (const origin of userOrigins) {
    if (processed.has(origin.activity_id)) continue;
    
    const nearbyOrigins = userOrigins.filter(other => 
      !processed.has(other.activity_id) &&
      calculateDistance(origin, other) <= mergeDistanceKm
    );
    
    if (nearbyOrigins.length > 1) {
      const mergedLocation = {
        activity_ids: nearbyOrigins.map(o => o.activity_id),
        centroid: calculateCentroid(nearbyOrigins),
        names: [...new Set(nearbyOrigins.map(o => o.name).filter(Boolean))],
        addresses: [...new Set(nearbyOrigins.map(o => o.address).filter(Boolean))],
        frequency: nearbyOrigins.length
      };
      
      merged.push(mergedLocation);
      nearbyOrigins.forEach(o => processed.add(o.activity_id));
    }
  }
  
  return merged;
};
```

### Error Handling and Data Validation

**Comprehensive Data Validation:**
```javascript
// Validate habitual origin data
const validateOriginData = (data) => {
  const errors = [];
  
  if (!data.activity_id || data.activity_id <= 0) {
    errors.push('Valid activity_id required');
  }
  
  if (!data.user_id || data.user_id.length > 256) {
    errors.push('Valid user_id required (max 256 characters)');
  }
  
  if (!data.location_id) {
    errors.push('Location ID is required');
  }
  
  if (data.name && data.name.length > 256) {
    errors.push('Name must be 256 characters or less');
  }
  
  if (data.address && data.address.length > 256) {
    errors.push('Address must be 256 characters or less');
  }
  
  if (!data.lat || Math.abs(data.lat) > 90) {
    errors.push('Valid latitude required (-90 to 90)');
  }
  
  if (!data.lng || Math.abs(data.lng) > 180) {
    errors.push('Valid longitude required (-180 to 180)');
  }
  
  if (errors.length > 0) {
    throw new ValidationError(errors.join(', '));
  }
};

// Safe origin insertion with conflict handling
const insertOriginSafely = async (data) => {
  validateOriginData(data);
  
  try {
    const result = await knex('hntb_habitual_trip_origin').insert(data);
    logger.info(`Habitual origin registered for activity ${data.activity_id}`);
    return result;
  } catch (error) {
    if (error.code === 'ER_DUP_ENTRY') {
      // Handle duplicate activity_id
      const existing = await knex('hntb_habitual_trip_origin')
        .where('activity_id', data.activity_id)
        .first();
      
      logger.warn(`Duplicate origin registration for activity ${data.activity_id}`);
      return existing;
    }
    logger.error(`Failed to register habitual origin: ${error.message}`);
    throw error;
  }
};
```

This migration establishes essential infrastructure for tracking and analyzing habitual trip origins within the HNTB transportation research platform, enabling sophisticated pattern recognition and behavioral analysis for transportation planning and policy development.