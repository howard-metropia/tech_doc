# CityCodeGeometry Model

## Overview
Geospatial data model for city boundary management within the TSP Job system. Handles city administrative boundaries using MongoDB with GeoJSON MultiPolygon geometry for precise geographical operations and city-based trip analysis.

## Model Definition
```javascript
const { Schema } = require('mongoose');
const conn = require('@maas/core/mongo')('cache');

const tripLineSchema = new Schema(
  {
    type: {
      type: String,
      enum: ['MultiPolygon'],
      required: true,
    },
    coordinates: {
      type: [[[[Number]]]],
      required: true,
    },
  },
  { _id: false },
);

const newTripTrajectory = new Schema({
  object_id: {
    type: Number,
    required: true,
  },
  geometry: {
    type: tripLineSchema,
  },
  name: {
    type: String,
    required: true,
  },
});

newTripTrajectory.index({ geometry: '2dsphere' });
const CityCodeGeometry = conn.model('city_code_geometry', newTripTrajectory);

module.exports = CityCodeGeometry;
```

## Database Configuration
- **Database**: MongoDB cache instance
- **Collection**: `city_code_geometry`
- **ODM**: Mongoose with geospatial indexing
- **Connection**: Managed by @maas/core MongoDB connection pool
- **Index**: 2dsphere for geospatial queries

## Quick Summary
The CityCodeGeometry model provides geospatial representation of city administrative boundaries using GeoJSON MultiPolygon format. It enables precise city-based geographic operations including trip origin/destination analysis, service area validation, and location-based filtering within the transportation service platform.

## Technical Analysis

### Schema Structure
The model implements a nested schema architecture with specialized geospatial components:

**Main Schema (`newTripTrajectory`)**:
- `object_id`: Unique numerical identifier for city boundary records
- `geometry`: Embedded GeoJSON geometry schema for spatial data
- `name`: Human-readable city name for identification

**Geometry Schema (`tripLineSchema`)**:
- `type`: Enforced as 'MultiPolygon' for complex city boundaries
- `coordinates`: Four-dimensional array structure `[[[[Number]]]]` representing polygon coordinate sets

### Geospatial Implementation
```javascript
// 2dsphere index enables MongoDB geospatial operations
newTripTrajectory.index({ geometry: '2dsphere' });

// MultiPolygon coordinate structure
coordinates: [
  [ // Polygon 1
    [ // Exterior ring
      [longitude, latitude],
      [longitude, latitude],
      // ... more coordinates
    ],
    [ // Optional interior ring (holes)
      [longitude, latitude],
      // ... hole coordinates
    ]
  ],
  [ // Polygon 2 (for complex city boundaries)
    // ... additional polygon coordinates
  ]
]
```

### Database Architecture
- **MongoDB Cache Database**: Optimized for fast geospatial queries
- **2dsphere Index**: Enables complex spatial operations including intersections, containment, and proximity searches
- **Schema Validation**: Strict type enforcement for geospatial data integrity
- **No Sub-document IDs**: `{ _id: false }` for geometry schema reduces document size

## Usage/Integration

### Geographic Operations
```javascript
// Find cities containing a specific point
const citiesContainingPoint = await CityCodeGeometry.find({
  geometry: {
    $geoIntersects: {
      $geometry: {
        type: "Point",
        coordinates: [longitude, latitude]
      }
    }
  }
});

// Find cities within a bounding box
const citiesInBounds = await CityCodeGeometry.find({
  geometry: {
    $geoWithin: {
      $geometry: {
        type: "Polygon",
        coordinates: [[boundingBoxCoordinates]]
      }
    }
  }
});

// Find cities near a location
const nearbyCities = await CityCodeGeometry.find({
  geometry: {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [longitude, latitude]
      },
      $maxDistance: 1000 // meters
    }
  }
});
```

### Trip Analysis Integration
- **Origin/Destination Validation**: Verify trip endpoints fall within valid city boundaries
- **Service Area Management**: Define operational zones for transportation services
- **Jurisdictional Routing**: Route optimization based on municipal boundaries
- **Billing Zone Determination**: Calculate fees based on city-specific rates

### Data Processing Workflows
- **Boundary Import**: Bulk import of city boundary data from GIS sources
- **Geometric Validation**: Ensure polygon closure and coordinate validity
- **Spatial Indexing**: Automatic 2dsphere index maintenance for query performance
- **Cache Optimization**: MongoDB cache layer for frequently accessed boundaries

## Dependencies

### Core Dependencies
- **mongoose**: MongoDB ODM for schema definition and validation
- **@maas/core/mongo**: Centralized MongoDB connection manager
  - Provides connection pooling and configuration management
  - Handles database instance routing ('cache' database)
  - Manages connection lifecycle and error handling

### System Dependencies
- **MongoDB Server**: Version 4.0+ with geospatial features
- **Node.js**: Compatible with MongoDB driver requirements
- **GeoJSON Specification**: Adherence to RFC 7946 standards

### Integration Dependencies
- **Trip Processing Services**: For origin/destination validation
- **Routing Services**: For boundary-aware route calculation
- **Billing Services**: For jurisdiction-based pricing
- **Analytics Services**: For city-based trip analysis

## Code Examples

### Model Instantiation
```javascript
const CityCodeGeometry = require('@app/src/models/CityCodeGeometry');

// Create new city boundary
const newCity = new CityCodeGeometry({
  object_id: 12345,
  name: "Austin",
  geometry: {
    type: "MultiPolygon",
    coordinates: [
      [
        [
          [-97.7431, 30.2672],
          [-97.7431, 30.2972],
          [-97.7131, 30.2972],
          [-97.7131, 30.2672],
          [-97.7431, 30.2672]
        ]
      ]
    ]
  }
});

await newCity.save();
```

### Spatial Query Operations
```javascript
// Check if trip origin is within city limits
async function validateTripOrigin(latitude, longitude) {
  const containingCity = await CityCodeGeometry.findOne({
    geometry: {
      $geoIntersects: {
        $geometry: {
          type: "Point",
          coordinates: [longitude, latitude]
        }
      }
    }
  });
  
  return containingCity ? containingCity.name : null;
}

// Find all cities within service radius
async function findServiceArea(centerLat, centerLng, radiusKm) {
  const serviceArea = await CityCodeGeometry.find({
    geometry: {
      $geoWithin: {
        $centerSphere: [[centerLng, centerLat], radiusKm / 6371]
      }
    }
  }).select('name object_id');
  
  return serviceArea.map(city => ({
    id: city.object_id,
    name: city.name
  }));
}
```

### Boundary Analysis Functions
```javascript
// Calculate city boundary centroid
async function getCityCentroid(cityObjectId) {
  const city = await CityCodeGeometry.findOne({ object_id: cityObjectId });
  if (!city) return null;
  
  // MongoDB aggregation for centroid calculation
  const result = await CityCodeGeometry.aggregate([
    { $match: { object_id: cityObjectId } },
    {
      $project: {
        centroid: { $geoNear: { $geometry: "$geometry" } }
      }
    }
  ]);
  
  return result[0]?.centroid;
}

// Validate MultiPolygon structure
function validateCityGeometry(geometry) {
  if (geometry.type !== 'MultiPolygon') {
    throw new Error('City geometry must be MultiPolygon type');
  }
  
  // Validate coordinate structure
  if (!Array.isArray(geometry.coordinates) || 
      !geometry.coordinates.every(polygon => 
        Array.isArray(polygon) && 
        polygon.every(ring => 
          Array.isArray(ring) && 
          ring.every(coord => 
            Array.isArray(coord) && coord.length === 2
          )
        )
      )) {
    throw new Error('Invalid MultiPolygon coordinate structure');
  }
  
  return true;
}
```

## Performance Considerations
- **2dsphere Indexing**: Optimizes geospatial queries for city boundary operations
- **Cache Database**: Utilizes MongoDB cache instance for high-frequency spatial lookups
- **Schema Optimization**: Minimal schema design reduces document size and query overhead
- **Connection Pooling**: Managed by @maas/core for efficient database connection reuse

## Integration Points
- **Trip Validation Services**: Origin/destination boundary validation
- **Routing Engine**: Municipal boundary-aware route optimization
- **Service Management**: City-based service area definition
- **Analytics Platform**: Geographic trip analysis and reporting
- **Billing System**: Jurisdiction-based fare calculation

## Use Cases
- **Trip Origin Validation**: Verify trip starts within serviceable city limits
- **Destination Analysis**: Analyze trip patterns by destination city
- **Service Coverage**: Define and manage transportation service areas
- **Geographic Reporting**: Generate city-based usage statistics
- **Boundary Enforcement**: Ensure operations comply with municipal boundaries
- **Route Optimization**: City-aware routing for efficiency and compliance