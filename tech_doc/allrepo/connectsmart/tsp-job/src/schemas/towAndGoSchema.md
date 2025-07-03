# TowAndGoSchema

## Quick Summary
Comprehensive validation schemas for Tow and Go emergency roadside assistance data structures. Handles validation of tow service location data including link IDs, segment IDs, JSON content validation, and MongoDB document structure for emergency assistance service integration.

## Technical Analysis

### Code Structure
```javascript
const Joi = require('joi');

const validateTowAndGoArray = Joi.array()
  .items(
    Joi.object({
      link_id: Joi.number().strict().required(),
      segment_id: Joi.number().strict().required().allow(null),
    }),
  )
  .min(1)
  .required();

const TowAndGoSchemas = {
  ValidateTowAndGoArray: validateTowAndGoArray,
  ValidateTowAndGoJsonContent: Joi.object({
    last_modified: Joi.number().integer().strict().required(),
    tow_and_go: validateTowAndGoArray,
  }),
  ValidateTowAndGoMongoDBData: Joi.object({
    _id: Joi.alternatives().try(Joi.object(), Joi.string()).required(),
    tow_and_go: validateTowAndGoArray,
    created_at: Joi.date().required(),
    __v: Joi.number().required(),
  }),
};
```

### Schema Components

#### Array Validation Schema
- **validateTowAndGoArray**: Core array schema for tow service locations
- **link_id**: Required strict number representing road network link identifier
- **segment_id**: Required strict number (nullable) for road segment specification
- **Minimum length**: Enforces at least one tow service location

#### JSON Content Schema
- **ValidateTowAndGoJsonContent**: Validates API response and file content
- **last_modified**: Unix timestamp indicating data freshness
- **tow_and_go**: Array of service locations using base array schema

#### MongoDB Document Schema
- **ValidateTowAndGoMongoDBData**: Validates database document structure
- **_id**: Flexible MongoDB ObjectId (object or string format)
- **created_at**: Document creation timestamp
- **__v**: MongoDB version key for document versioning

### Implementation Details
The schema employs strict mode validation ensuring numeric fields are exactly numbers, not strings. The nullable segment_id accommodates road networks where segment granularity isn't available. The modular design allows reuse of the core array schema across different data contexts.

## Usage/Integration

### Primary Use Cases
- **Data Import Validation**: Validates external tow service data before database insertion
- **API Response Validation**: Ensures proper structure of tow service location data
- **Database Document Validation**: Validates MongoDB documents before persistence
- **Data Synchronization**: Validates data consistency during S3 to MongoDB sync operations

### Integration Points
```javascript
// Service location validation
const { TowAndGoSchemas } = require('../schemas/towAndGoSchema');

// Validate API response
const { error } = TowAndGoSchemas.ValidateTowAndGoJsonContent.validate(apiResponse);

// Validate before MongoDB insertion
const mongoValidation = TowAndGoSchemas.ValidateTowAndGoMongoDBData.validate(document);
```

### Scheduling Context
Used in scheduled jobs that sync tow service data from external sources to MongoDB, typically running hourly to maintain current emergency service availability information.

## Dependencies

### Core Dependencies
- **joi**: Primary validation library with strict mode support
- **mongoose**: MongoDB ODM utilizing these schemas for document validation
- **@maas/core**: Core platform utilities for database connections

### External Service Dependencies
- **AWS S3**: Source of tow service data files requiring validation
- **MongoDB**: Target database for validated tow service documents
- **External Tow APIs**: Third-party services providing location updates

### Configuration Requirements
```javascript
// Environment configuration for tow service integration
TOW_AND_GO_DATA_SOURCE=s3://bucket/tow-locations
TOW_AND_GO_SYNC_INTERVAL=3600000 // 1 hour
TOW_AND_GO_MONGODB_COLLECTION=tow_and_go
LINK_SEGMENT_VALIDATION_STRICT=true
```

## Code Examples

### Array Validation Usage
```javascript
const { TowAndGoSchemas } = require('./schemas/towAndGoSchema');

// Validate tow service locations array
const towLocations = [
  { link_id: 12345, segment_id: 67890 },
  { link_id: 12346, segment_id: null }, // null segment_id is allowed
  { link_id: 12347, segment_id: 67891 }
];

const { error, value } = TowAndGoSchemas.ValidateTowAndGoArray.validate(towLocations);

if (error) {
  console.error('Tow location validation failed:', error.details);
} else {
  console.log('Valid tow locations:', value.length);
}
```

### JSON Content Validation
```javascript
// Validate complete JSON content from external source
const validateTowServiceData = (jsonData) => {
  const validation = TowAndGoSchemas.ValidateTowAndGoJsonContent.validate(jsonData);
  
  if (validation.error) {
    throw new ValidationError(`Invalid tow service data: ${validation.error.message}`);
  }
  
  // Check data freshness
  const lastModified = new Date(validation.value.last_modified * 1000);
  const dataAge = Date.now() - lastModified.getTime();
  const maxAge = 24 * 60 * 60 * 1000; // 24 hours
  
  if (dataAge > maxAge) {
    console.warn('Tow service data is older than 24 hours');
  }
  
  return validation.value;
};

// Example usage
const externalData = {
  last_modified: Math.floor(Date.now() / 1000),
  tow_and_go: [
    { link_id: 1001, segment_id: 2001 },
    { link_id: 1002, segment_id: null }
  ]
};

try {
  const validatedData = validateTowServiceData(externalData);
  console.log(`Validated ${validatedData.tow_and_go.length} tow locations`);
} catch (error) {
  console.error('Data validation failed:', error.message);
}
```

### MongoDB Document Validation
```javascript
// Validate MongoDB document before insertion
const insertTowAndGoData = async (towData) => {
  const document = {
    _id: new mongoose.Types.ObjectId(),
    tow_and_go: towData.tow_and_go,
    created_at: new Date(),
    __v: 0
  };
  
  // Validate document structure
  const { error, value } = TowAndGoSchemas.ValidateTowAndGoMongoDBData.validate(document);
  
  if (error) {
    throw new DatabaseError(`Invalid MongoDB document: ${error.message}`);
  }
  
  // Insert validated document
  const result = await TowAndGoCollection.insertOne(value);
  
  logger.info('Tow and Go data inserted', {
    documentId: result.insertedId,
    locationCount: value.tow_and_go.length
  });
  
  return result;
};
```

### Data Synchronization Job
```javascript
// Complete synchronization job using all schema validations
const syncTowAndGoData = async () => {
  try {
    // Fetch data from S3
    const s3Data = await s3.getObject({
      Bucket: 'tow-service-data',
      Key: 'latest/tow-locations.json'
    }).promise();
    
    const jsonData = JSON.parse(s3Data.Body.toString());
    
    // Validate JSON content
    const { error: jsonError, value: validatedJson } = 
      TowAndGoSchemas.ValidateTowAndGoJsonContent.validate(jsonData);
    
    if (jsonError) {
      await notificationService.alert('Tow data validation failed', jsonError);
      return;
    }
    
    // Prepare MongoDB document
    const mongoDocument = {
      _id: new mongoose.Types.ObjectId(),
      tow_and_go: validatedJson.tow_and_go,
      created_at: new Date(),
      __v: 0
    };
    
    // Validate MongoDB document
    const { error: mongoError, value: validatedDoc } = 
      TowAndGoSchemas.ValidateTowAndGoMongoDBData.validate(mongoDocument);
    
    if (mongoError) {
      logger.error('MongoDB document validation failed', mongoError);
      return;
    }
    
    // Replace existing data with new validated data
    await TowAndGoModel.deleteMany({});
    const result = await TowAndGoModel.create(validatedDoc);
    
    logger.info('Tow and Go data synchronized successfully', {
      documentId: result._id,
      locationCount: result.tow_and_go.length,
      lastModified: new Date(validatedJson.last_modified * 1000)
    });
    
  } catch (error) {
    logger.error('Tow and Go sync job failed', error);
    await notificationService.alertAdmins('Tow service sync failure', error);
  }
};
```

### Error Handling and Logging
```javascript
// Comprehensive error handling for schema validation
const processIncomingTowData = async (data, source) => {
  const processingMetrics = {
    source,
    timestamp: new Date(),
    validationErrors: [],
    processedCount: 0
  };
  
  try {
    // First validate the array structure
    const arrayValidation = TowAndGoSchemas.ValidateTowAndGoArray.validate(data);
    
    if (arrayValidation.error) {
      processingMetrics.validationErrors.push({
        type: 'array_validation',
        error: arrayValidation.error.details
      });
      
      // Log detailed validation failure
      logger.error('Tow location array validation failed', {
        source,
        errorCount: arrayValidation.error.details.length,
        sampleError: arrayValidation.error.details[0]
      });
      
      return processingMetrics;
    }
    
    // Process each location with individual validation
    const validLocations = [];
    const invalidLocations = [];
    
    for (const [index, location] of data.entries()) {
      try {
        // Validate individual location
        if (typeof location.link_id !== 'number' || location.link_id <= 0) {
          throw new Error(`Invalid link_id: ${location.link_id}`);
        }
        
        if (location.segment_id !== null && 
            (typeof location.segment_id !== 'number' || location.segment_id <= 0)) {
          throw new Error(`Invalid segment_id: ${location.segment_id}`);
        }
        
        validLocations.push(location);
      } catch (locationError) {
        invalidLocations.push({
          index,
          location,
          error: locationError.message
        });
      }
    }
    
    processingMetrics.processedCount = validLocations.length;
    processingMetrics.invalidCount = invalidLocations.length;
    
    // Log processing results
    logger.info('Tow location processing completed', processingMetrics);
    
    return {
      ...processingMetrics,
      validLocations,
      invalidLocations
    };
    
  } catch (error) {
    logger.error('Tow data processing failed', { source, error: error.message });
    throw error;
  }
};
```

## Related Components
- **TowAndGoService**: Service class consuming these validation schemas
- **tow-and-go-sync-s3-to-mongodb job**: Scheduled sync job using these schemas
- **TowAndGoModel**: Database model utilizing MongoDB validation schema
- **HntbTowAndGo**: Specialized tow service implementation with schema validation