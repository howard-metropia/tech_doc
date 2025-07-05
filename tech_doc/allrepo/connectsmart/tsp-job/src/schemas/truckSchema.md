# TruckSchema

## Quick Summary
Validation schemas for truck routing and height restriction data in the TSP Job system. Manages validation of truck mapping data including height restrictions, segment IDs, link IDs, and presentation text for commercial vehicle routing and clearance information.

## Technical Analysis

### Code Structure
```javascript
const Joi = require('joi');

const validateTruckMapArray = Joi.array()
  .items(
    Joi.object({
      max_height: Joi.number().strict().required(),
      min_height: Joi.number().strict().required(),
      present_word: Joi.string().required().allow(null),
      segment_id: Joi.number().strict().required(),
      link_id: Joi.number().strict().required(),
    }),
  )
  .min(1)
  .required();

const TruckMapSchemas = {
  ValidateTruckMapArray: validateTruckMapArray,
  ValidateTruckMapJsonContent: Joi.object({
    last_modified: Joi.number().integer().strict().required(),
    truck_map_array: validateTruckMapArray,
  }),
  ValidateTruckMapMongoDBData: Joi.object({
    _id: Joi.alternatives().try(Joi.object(), Joi.string()).required(),
    truck_map: validateTruckMapArray,
    created_at: Joi.date().required(),
    __v: Joi.number().required(),
  }),
};
```

### Schema Components

#### Truck Map Array Schema
- **validateTruckMapArray**: Core validation for truck routing restrictions
- **max_height**: Required strict number for maximum vehicle height clearance (feet/meters)
- **min_height**: Required strict number for minimum height restriction
- **present_word**: Nullable string for display text (bridge names, restriction descriptions)
- **segment_id**: Required strict number identifying road segment
- **link_id**: Required strict number identifying road network link

#### JSON Content Schema
- **ValidateTruckMapJsonContent**: Validates external data sources and API responses
- **last_modified**: Unix timestamp for data freshness tracking
- **truck_map_array**: Array of truck routing restrictions using base schema

#### MongoDB Document Schema
- **ValidateTruckMapMongoDBData**: Database document structure validation
- **_id**: MongoDB ObjectId in object or string format
- **truck_map**: Truck routing data array (renamed from truck_map_array)
- **created_at**: Document creation timestamp
- **__v**: MongoDB version control field

### Implementation Details
The schema enforces strict numeric validation for height measurements to prevent routing errors. The present_word field accommodates various restriction descriptions like "Low Bridge", "Tunnel Clearance", or specific bridge names. Height values are typically in feet but can be configured for metric systems.

## Usage/Integration

### Primary Use Cases
- **Commercial Vehicle Routing**: Validates height restrictions for truck navigation
- **Infrastructure Data Management**: Manages bridge and tunnel clearance information
- **Route Planning Validation**: Ensures safe routing for oversized vehicles
- **Mapping Data Synchronization**: Validates truck restriction updates from external sources

### Integration Points
```javascript
// Truck routing validation
const { TruckMapSchemas } = require('../schemas/truckSchema');

// Validate height restriction data
const validation = TruckMapSchemas.ValidateTruckMapArray.validate(truckRestrictions);

// Validate complete mapping data
const contentValidation = TruckMapSchemas.ValidateTruckMapJsonContent.validate(mapData);
```

### Scheduling Context
Used in scheduled jobs that update truck routing restrictions from DOT feeds, bridge inspection data, and construction notices, typically running multiple times daily to maintain current clearance information.

## Dependencies

### Core Dependencies
- **joi**: Schema validation with strict numeric type checking
- **mongoose**: MongoDB integration for truck mapping data
- **@maas/core**: Core platform services and database connections

### External Service Dependencies
- **Department of Transportation APIs**: Source of bridge and tunnel clearance data
- **HERE Maps API**: Commercial vehicle routing integration
- **MongoDB**: Storage for validated truck restriction data
- **AWS S3**: External data source for mapping updates

### Configuration Requirements
```javascript
// Environment variables for truck routing configuration
TRUCK_ROUTING_DATA_SOURCE=https://api.dot.gov/truck-restrictions
TRUCK_HEIGHT_UNIT=feet // or meters
TRUCK_DATA_SYNC_INTERVAL=21600000 // 6 hours
TRUCK_CLEARANCE_BUFFER=0.5 // safety buffer in feet
MIN_TRUCK_HEIGHT=8.0 // minimum commercial vehicle height
MAX_TRUCK_HEIGHT=13.6 // standard maximum height limit
```

## Code Examples

### Basic Truck Restriction Validation
```javascript
const { TruckMapSchemas } = require('./schemas/truckSchema');

// Validate truck height restriction data
const truckRestrictions = [
  {
    max_height: 13.5,
    min_height: 8.0,
    present_word: "Low Bridge - Main St",
    segment_id: 12345,
    link_id: 67890
  },
  {
    max_height: 11.8,
    min_height: 8.0,
    present_word: null, // No descriptive text
    segment_id: 12346,
    link_id: 67891
  }
];

const { error, value } = TruckMapSchemas.ValidateTruckMapArray.validate(truckRestrictions);

if (error) {
  console.error('Truck restriction validation failed:', error.details);
} else {
  console.log(`Validated ${value.length} truck restrictions`);
}
```

### Route Planning Integration
```javascript
// Truck route planning with height validation
class TruckRoutingService {
  async validateRouteForVehicle(route, vehicleHeight) {
    try {
      // Get restrictions for route segments
      const restrictions = await this.getTruckRestrictionsForRoute(route);
      
      // Validate restriction data structure
      const { error, value } = TruckMapSchemas.ValidateTruckMapArray.validate(restrictions);
      
      if (error) {
        throw new ValidationError(`Invalid restriction data: ${error.message}`);
      }
      
      // Check clearances
      const clearanceIssues = [];
      
      for (const restriction of value) {
        const clearance = restriction.max_height;
        const safetyBuffer = 0.5; // 6 inches safety buffer
        
        if ((vehicleHeight + safetyBuffer) > clearance) {
          clearanceIssues.push({
            segment_id: restriction.segment_id,
            link_id: restriction.link_id,
            restriction_height: clearance,
            vehicle_height: vehicleHeight,
            clearance_deficit: (vehicleHeight + safetyBuffer) - clearance,
            description: restriction.present_word || 'Height Restriction'
          });
        }
      }
      
      return {
        routeValid: clearanceIssues.length === 0,
        clearanceIssues,
        totalRestrictions: value.length
      };
      
    } catch (error) {
      logger.error('Route validation failed', { route, vehicleHeight, error });
      throw error;
    }
  }
}
```

### Data Import and Validation
```javascript
// Import truck restriction data from external source
const importTruckRestrictions = async (dataSource) => {
  try {
    // Fetch external data
    const response = await fetch(dataSource);
    const rawData = await response.json();
    
    // Validate JSON content structure
    const { error: contentError, value: validatedContent } = 
      TruckMapSchemas.ValidateTruckMapJsonContent.validate(rawData);
    
    if (contentError) {
      throw new DataImportError(`Invalid data format: ${contentError.message}`);
    }
    
    // Process and validate individual restrictions
    const processedRestrictions = validatedContent.truck_map_array.map(restriction => ({
      ...restriction,
      // Convert heights if needed (assuming source is in feet)
      max_height: parseFloat(restriction.max_height.toFixed(1)),
      min_height: parseFloat(restriction.min_height.toFixed(1)),
      // Clean up present_word
      present_word: restriction.present_word ? 
        restriction.present_word.trim() : null
    }));
    
    // Final validation of processed data
    const { error: finalError, value: finalData } = 
      TruckMapSchemas.ValidateTruckMapArray.validate(processedRestrictions);
    
    if (finalError) {
      throw new DataProcessingError(`Data processing failed: ${finalError.message}`);
    }
    
    logger.info('Truck restrictions imported successfully', {
      source: dataSource,
      restrictionCount: finalData.length,
      lastModified: new Date(validatedContent.last_modified * 1000)
    });
    
    return {
      restrictions: finalData,
      lastModified: validatedContent.last_modified,
      importTimestamp: new Date()
    };
    
  } catch (error) {
    logger.error('Truck restriction import failed', { dataSource, error });
    throw error;
  }
};
```

### MongoDB Integration
```javascript
// MongoDB document creation and validation
const saveTruckMappingData = async (truckMapData) => {
  try {
    // Prepare MongoDB document
    const document = {
      _id: new mongoose.Types.ObjectId(),
      truck_map: truckMapData.restrictions,
      created_at: new Date(),
      __v: 0
    };
    
    // Validate document structure
    const { error, value } = TruckMapSchemas.ValidateTruckMapMongoDBData.validate(document);
    
    if (error) {
      throw new DatabaseError(`Invalid MongoDB document: ${error.message}`);
    }
    
    // Clear existing restrictions and insert new data
    await TruckModel.deleteMany({});
    const result = await TruckModel.create(value);
    
    // Update cache for fast lookups
    await redis.setex('truck:restrictions', 3600, JSON.stringify(value.truck_map));
    
    logger.info('Truck mapping data saved', {
      documentId: result._id,
      restrictionCount: result.truck_map.length
    });
    
    return result;
    
  } catch (error) {
    logger.error('Failed to save truck mapping data', error);
    throw error;
  }
};
```

### Scheduled Synchronization Job
```javascript
// Complete truck restriction synchronization job
const syncTruckRestrictions = async () => {
  const jobMetrics = {
    startTime: new Date(),
    source: process.env.TRUCK_ROUTING_DATA_SOURCE,
    status: 'running',
    errors: []
  };
  
  try {
    // Import latest restriction data
    const importResult = await importTruckRestrictions(jobMetrics.source);
    
    // Validate and save to MongoDB
    const saveResult = await saveTruckMappingData(importResult);
    
    // Update job metrics
    jobMetrics.status = 'completed';
    jobMetrics.endTime = new Date();
    jobMetrics.restrictionsProcessed = saveResult.truck_map.length;
    jobMetrics.lastDataUpdate = new Date(importResult.lastModified * 1000);
    
    // Log success metrics
    logger.info('Truck restriction sync completed successfully', jobMetrics);
    
    // Notify routing services of updated data
    await notificationService.notifyServices('truck-restrictions-updated', {
      restrictionCount: saveResult.truck_map.length,
      updateTime: jobMetrics.endTime
    });
    
  } catch (error) {
    jobMetrics.status = 'failed';
    jobMetrics.endTime = new Date();
    jobMetrics.errors.push(error.message);
    
    logger.error('Truck restriction sync failed', jobMetrics);
    
    // Alert operations team
    await notificationService.alertAdmins('Truck restriction sync failure', {
      error: error.message,
      jobMetrics
    });
  }
};
```

### Height Conversion and Validation
```javascript
// Utility functions for height validation and unit conversion
const TruckHeightUtils = {
  // Convert between feet and meters
  feetToMeters: (feet) => feet * 0.3048,
  metersToFeet: (meters) => meters / 0.3048,
  
  // Validate height restriction makes sense
  validateHeightRestriction: (restriction) => {
    const { max_height, min_height } = restriction;
    
    // Basic sanity checks
    if (max_height <= min_height) {
      throw new Error(`Max height (${max_height}) must be greater than min height (${min_height})`);
    }
    
    // Reasonable bounds checking (assuming feet)
    if (max_height < 8 || max_height > 20) {
      console.warn(`Unusual max height: ${max_height} feet`);
    }
    
    if (min_height < 6 || min_height > 15) {
      console.warn(`Unusual min height: ${min_height} feet`);
    }
    
    return true;
  },
  
  // Format height for display
  formatHeight: (height, unit = 'feet') => {
    const formattedHeight = parseFloat(height.toFixed(1));
    return `${formattedHeight} ${unit}`;
  }
};

// Usage in validation pipeline
const validateAndFormatRestrictions = (restrictions) => {
  return restrictions.map(restriction => {
    // Validate individual restriction
    TruckHeightUtils.validateHeightRestriction(restriction);
    
    // Format for consistency
    return {
      ...restriction,
      max_height: parseFloat(restriction.max_height.toFixed(1)),
      min_height: parseFloat(restriction.min_height.toFixed(1)),
      present_word: restriction.present_word ? 
        restriction.present_word.trim() : null,
      formatted_clearance: TruckHeightUtils.formatHeight(restriction.max_height)
    };
  });
};
```

## Related Components
- **TruckService**: Service class for truck routing using these schemas
- **TruckModel**: Database model utilizing MongoDB validation schema
- **HERE Maps integration**: Commercial vehicle routing with height restrictions
- **Route planning services**: Validation of truck-safe routes using restriction data