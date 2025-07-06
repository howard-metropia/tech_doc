# CountyCodeGeometry Model

## Overview
Geospatial data model for county administrative boundary management within the TSP Job system. Provides county-level geographic operations using MongoDB with GeoJSON MultiPolygon geometry for regional transportation analysis and jurisdiction-based service management.

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
const CountyCodeGeometry = conn.model('county_code_geometry', newTripTrajectory);

module.exports = CountyCodeGeometry;
```

## Database Configuration
- **Database**: MongoDB cache instance
- **Collection**: `county_code_geometry`
- **ODM**: Mongoose with geospatial indexing
- **Connection**: Managed by @maas/core MongoDB connection pool
- **Index**: 2dsphere for optimized spatial operations

## Quick Summary
The CountyCodeGeometry model manages county administrative boundaries using GeoJSON MultiPolygon format for precise regional geographic operations. It enables county-level trip analysis, inter-county routing, regional service planning, and jurisdiction-based transportation management within the MaaS platform.

## Technical Analysis

### Schema Architecture
The model employs a sophisticated nested schema design optimized for geospatial operations:

**Primary Schema (`newTripTrajectory`)**:
- `object_id`: Unique numerical identifier for county boundary records
- `geometry`: Embedded GeoJSON MultiPolygon schema for complex boundaries
- `name`: County name for human-readable identification and filtering

**Geospatial Schema (`tripLineSchema`)**:
- `type`: Strictly enforced as 'MultiPolygon' for complex county shapes
- `coordinates`: Four-dimensional coordinate array `[[[[Number]]]]` supporting multiple polygons with holes

### Geospatial Implementation Details
```javascript
// 2dsphere index enables advanced MongoDB geospatial operations
newTripTrajectory.index({ geometry: '2dsphere' });

// MultiPolygon structure for complex county boundaries
{
  type: "MultiPolygon",
  coordinates: [
    [ // Primary county polygon
      [ // Exterior boundary ring
        [-101.5234, 35.2971], // [longitude, latitude] format
        [-101.5234, 35.3971],
        [-101.4234, 35.3971],
        [-101.4234, 35.2971],
        [-101.5234, 35.2971]  // Closed ring
      ],
      [ // Interior hole (if any, e.g., enclaves)
        [-101.5000, 35.3200],
        [-101.4800, 35.3400],
        [-101.4600, 35.3200],
        [-101.5000, 35.3200]
      ]
    ],
    [ // Additional disconnected county areas
      [ // Secondary polygon exterior ring
        [-101.3000, 35.4000],
        [-101.2800, 35.4200],
        [-101.2600, 35.4000],
        [-101.3000, 35.4000]
      ]
    ]
  ]
}
```

### Database Optimization
- **Cache Database Strategy**: Utilizes MongoDB cache instance for high-performance spatial queries
- **Spatial Indexing**: 2dsphere index supports spherical geometry calculations
- **Document Structure**: Optimized schema design minimizes storage overhead
- **Connection Management**: Leverages @maas/core connection pooling for scalability

## Usage/Integration

### County-Based Spatial Operations
```javascript
// Find county containing specific coordinates
const findCountyByPoint = async (longitude, latitude) => {
  return await CountyCodeGeometry.findOne({
    geometry: {
      $geoIntersects: {
        $geometry: {
          type: "Point", 
          coordinates: [longitude, latitude]
        }
      }
    }
  });
};

// Find all counties within a circular area
const findCountiesInRadius = async (centerLon, centerLat, radiusMeters) => {
  return await CountyCodeGeometry.find({
    geometry: {
      $geoWithin: {
        $centerSphere: [[centerLon, centerLat], radiusMeters / 6378100]
      }
    }
  });
};

// Find counties intersecting a route polygon
const findCountiesAlongRoute = async (routePolygon) => {
  return await CountyCodeGeometry.find({
    geometry: {
      $geoIntersects: {
        $geometry: routePolygon
      }
    }
  });
};
```

### Regional Transportation Analysis
- **Inter-County Trip Detection**: Identify trips crossing county boundaries
- **Regional Service Planning**: Analyze service coverage across multiple counties
- **Jurisdiction Compliance**: Ensure operations comply with county regulations
- **Cross-County Billing**: Calculate fees for multi-jurisdiction trips

### Administrative Boundary Operations
- **Service Area Definition**: Define transportation service regions by county
- **Regulatory Compliance**: Enforce county-specific transportation regulations
- **Resource Allocation**: Distribute services based on county demographics
- **Partnership Management**: Manage county-level transportation partnerships

## Dependencies

### Core System Dependencies
- **mongoose**: MongoDB ODM providing schema validation and query interface
- **@maas/core/mongo**: Centralized MongoDB connection management
  - Database connection pooling and lifecycle management
  - Configuration-driven database instance routing
  - Error handling and retry logic for database operations

### External Dependencies
- **MongoDB Server**: Version 4.0+ with geospatial indexing support
- **Node.js Runtime**: Compatible with MongoDB driver and Mongoose requirements
- **GeoJSON Standards**: RFC 7946 compliance for geometry data

### Integration Dependencies
- **Regional Planning Services**: County-level service coordination
- **Trip Processing Engine**: Inter-county trip validation and routing
- **Billing Management**: Multi-jurisdiction fare calculation
- **Analytics Platform**: Regional transportation pattern analysis

## Code Examples

### Model Usage Patterns
```javascript
const CountyCodeGeometry = require('@app/src/models/CountyCodeGeometry');

// Create new county boundary record
const createCountyBoundary = async (countyData) => {
  const county = new CountyCodeGeometry({
    object_id: countyData.fipsCode,
    name: countyData.countyName,
    geometry: {
      type: "MultiPolygon",
      coordinates: countyData.boundaryCoordinates
    }
  });
  
  try {
    await county.save();
    console.log(`County ${countyData.countyName} boundary saved successfully`);
    return county;
  } catch (error) {
    console.error('Error saving county boundary:', error);
    throw error;
  }
};

// Validate trip crosses county boundaries
const validateInterCountyTrip = async (origin, destination) => {
  const [originCounty, destinationCounty] = await Promise.all([
    CountyCodeGeometry.findOne({
      geometry: {
        $geoIntersects: {
          $geometry: { type: "Point", coordinates: origin }
        }
      }
    }),
    CountyCodeGeometry.findOne({
      geometry: {
        $geoIntersects: {
          $geometry: { type: "Point", coordinates: destination }
        }
      }
    })
  ]);
  
  return {
    isInterCounty: originCounty?.object_id !== destinationCounty?.object_id,
    originCounty: originCounty?.name,
    destinationCounty: destinationCounty?.name,
    originCountyId: originCounty?.object_id,
    destinationCountyId: destinationCounty?.object_id
  };
};
```

### Advanced Spatial Queries
```javascript
// Regional analysis functions
class CountyAnalysisService {
  // Find counties within metropolitan area
  static async findMetropolitanCounties(centerPoint, radiusKm) {
    const radiusRadians = radiusKm / 6371; // Earth radius in km
    
    return await CountyCodeGeometry.find({
      geometry: {
        $geoWithin: {
          $centerSphere: [centerPoint, radiusRadians]
        }
      }
    }).select('name object_id');
  }
  
  // Calculate county coverage for service area
  static async calculateServiceCoverage(servicePolygon) {
    const coveredCounties = await CountyCodeGeometry.find({
      geometry: {
        $geoIntersects: {
          $geometry: servicePolygon
        }
      }
    });
    
    return {
      totalCounties: coveredCounties.length,
      counties: coveredCounties.map(county => ({
        id: county.object_id,
        name: county.name
      }))
    };
  }
  
  // Find neighboring counties
  static async findNeighboringCounties(countyId, maxDistance = 1000) {
    const targetCounty = await CountyCodeGeometry.findOne({ 
      object_id: countyId 
    });
    
    if (!targetCounty) return [];
    
    return await CountyCodeGeometry.find({
      object_id: { $ne: countyId },
      geometry: {
        $near: {
          $geometry: targetCounty.geometry,
          $maxDistance: maxDistance
        }
      }
    }).limit(10);
  }
}
```

### Bulk Operations and Data Management
```javascript
// Bulk import county boundaries from GIS data
const importCountyBoundaries = async (gisDataArray) => {
  const operations = gisDataArray.map(countyData => ({
    updateOne: {
      filter: { object_id: countyData.fipsCode },
      update: {
        $set: {
          name: countyData.name,
          geometry: {
            type: "MultiPolygon",
            coordinates: countyData.coordinates
          }
        }
      },
      upsert: true
    }
  }));
  
  try {
    const result = await CountyCodeGeometry.bulkWrite(operations);
    console.log(`Processed ${result.modifiedCount} counties, inserted ${result.insertedCount} new counties`);
    return result;
  } catch (error) {
    console.error('Bulk import failed:', error);
    throw error;
  }
};

// Validate and repair county geometry data
const validateCountyGeometries = async () => {
  const counties = await CountyCodeGeometry.find({});
  const validationResults = [];
  
  for (const county of counties) {
    try {
      // Validate MultiPolygon structure
      const isValid = validateMultiPolygonGeometry(county.geometry);
      validationResults.push({
        countyId: county.object_id,
        countyName: county.name,
        isValid,
        errors: isValid ? [] : ['Invalid geometry structure']
      });
    } catch (error) {
      validationResults.push({
        countyId: county.object_id,
        countyName: county.name,
        isValid: false,
        errors: [error.message]
      });
    }
  }
  
  return validationResults;
};
```

## Performance Considerations
- **2dsphere Indexing**: Enables efficient spatial queries with spherical geometry calculations
- **Cache Database Strategy**: MongoDB cache instance optimized for frequent boundary lookups  
- **Query Optimization**: Selective field projection reduces network overhead for large polygons
- **Connection Pooling**: @maas/core manages database connections for optimal resource usage
- **Bulk Operations**: Batch processing for data imports and updates minimizes database round trips

## Integration Points
- **Regional Trip Analysis**: Multi-county trip pattern analysis and reporting
- **Service Planning**: County-level transportation service coordination
- **Regulatory Compliance**: Jurisdiction-specific rule enforcement
- **Partnership Management**: County government and agency coordination
- **Billing Systems**: Multi-jurisdiction fare calculation and revenue sharing
- **Analytics Platform**: Regional mobility pattern analysis and insights

## Use Cases
- **Inter-County Trip Validation**: Verify and track trips crossing county boundaries
- **Regional Service Coverage**: Define and manage multi-county service areas
- **Jurisdiction Compliance**: Ensure operations comply with county transportation regulations
- **Cross-County Routing**: Optimize routes considering county-specific constraints
- **Regional Analytics**: Generate county-level transportation usage reports
- **Partnership Coordination**: Manage relationships with multiple county transportation authorities
- **Resource Allocation**: Distribute transportation resources based on county demographics and needs