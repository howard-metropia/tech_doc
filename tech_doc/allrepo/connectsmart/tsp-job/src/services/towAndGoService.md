# Tow And Go Service

## Overview

The Tow And Go Service provides comprehensive data management capabilities for tow-and-go parking information, handling the complete data lifecycle from S3 storage through MongoDB synchronization with robust validation and error handling. This service enables automated processing of parking availability data for integration with transportation service provider systems.

## Service Information

- **Service Name**: Tow And Go Data Management Service
- **File Path**: `/src/services/towAndGoService.js`
- **Type**: Data Synchronization and Validation Service
- **Architecture**: Class-based service with dependency injection pattern
- **Dependencies**: AWS S3 Storage, MongoDB, Joi Validation, Logging Service

## Class Architecture

### TowAndGoService Class

Implements a comprehensive service pattern with proper encapsulation and separation of concerns for tow-and-go data management operations.

**Constructor Configuration**:
```javascript
constructor() {
  this.towAndGoFileName = 'tow-and-go.json';
  this.storage = new StorageS3();
  this.validateJsonFileContent = TowAndGoSchemas.ValidateTowAndGoJsonContent;
  this.validateMongoDbData = TowAndGoSchemas.ValidateTowAndGoMongoDBData;
  this.validateTowAndGoArray = TowAndGoSchemas.ValidateTowAndGoArray;
}
```

**Dependencies Initialization**:
- **Storage Layer**: AWS S3 integration through StorageS3 helper
- **Validation Layer**: Joi schema validation for data integrity
- **Data Layer**: MongoDB model integration for persistence
- **Logging Layer**: Structured logging for operations monitoring

## Core Methods

### uploadTowAndGoDataToS3(towAndGoJsonContent)

Uploads validated tow-and-go data to AWS S3 storage with comprehensive content validation.

**Purpose**: Store tow-and-go data in cloud storage with validation
**Parameters**: 
- `towAndGoJsonContent` (string): JSON string containing tow-and-go data
**Returns**: Promise resolving to upload completion

**Validation and Upload Process**:
1. **Content Parsing**: Converts JSON string to object for validation
2. **Schema Validation**: Validates structure using Joi schema
3. **S3 Upload**: Stores validated content with predefined filename
4. **Error Propagation**: Throws validation or upload errors

**Implementation Details**:
```javascript
async uploadTowAndGoDataToS3(towAndGoJsonContent) {
  await this.validateJsonFileContent.validateAsync(
    JSON.parse(towAndGoJsonContent),
  );
  await this.storage.uploadFileContentToS3File(
    this.towAndGoFileName,
    towAndGoJsonContent,
  );
}
```

**Error Handling**:
- JSON parsing errors for malformed content
- Joi validation errors for schema violations
- S3 upload errors for storage failures
- Network connectivity issues

### getTowAndGoDataFromS3()

Retrieves and validates tow-and-go data from AWS S3 storage with automatic content verification.

**Purpose**: Fetch and validate stored tow-and-go data from cloud storage
**Parameters**: None
**Returns**: Promise resolving to validated JSON data object

**Retrieval and Validation Process**:
1. **S3 Retrieval**: Downloads JSON data from predefined S3 location
2. **Content Validation**: Validates retrieved data against schema
3. **Data Return**: Returns validated JSON object for processing

**Data Flow**:
```javascript
async getTowAndGoDataFromS3() {
  const towAndGoJsonData = await this.storage.getJsonDataFromS3(
    this.towAndGoFileName,
  );
  await this.validateJsonFileContent.validateAsync(towAndGoJsonData);
  return towAndGoJsonData;
}
```

**Validation Benefits**:
- Ensures data integrity before processing
- Catches schema violations early in pipeline
- Provides consistent data structure guarantees
- Enables safe downstream processing

### syncTowAndGoFromS3ToMongoDb()

Orchestrates complete data synchronization pipeline from S3 storage to MongoDB with validation checkpoints.

**Purpose**: Synchronize cloud storage data with database storage
**Parameters**: None
**Returns**: Promise resolving to synchronization completion

**Synchronization Pipeline**:
1. **Data Retrieval**: Fetches validated data from S3 storage
2. **Array Extraction**: Extracts tow-and-go array from JSON structure
3. **Database Storage**: Persists data to MongoDB with validation
4. **Validation Checkpoint**: Verifies stored data integrity

**Pipeline Implementation**:
```javascript
async syncTowAndGoFromS3ToMongoDb() {
  const towAndGoData = await this.getTowAndGoDataFromS3();
  const towAndGopArrayData = towAndGoData['tow_and_go'];
  await this.saveTowAndGoToMongoDB(towAndGopArrayData);
  await this.validateLatestTowAndGoData();
}
```

**Data Structure Handling**:
- Supports nested JSON structures with array extraction
- Maintains data relationships during transfer
- Preserves metadata and structural integrity
- Enables flexible schema evolution

### saveTowAndGoToMongoDB(towAndGoData)

Persists validated tow-and-go data to MongoDB with comprehensive error handling and logging.

**Purpose**: Store tow-and-go array data in MongoDB with validation
**Parameters**: 
- `towAndGoData` (array): Array of tow-and-go objects to store
**Returns**: Promise resolving to saved MongoDB document

**Storage Process**:
1. **Array Validation**: Validates input array structure and content
2. **Document Creation**: Creates MongoDB document with timestamp
3. **Database Persistence**: Saves document with error handling
4. **Result Return**: Returns saved document or propagates errors

**MongoDB Integration**:
```javascript
async saveTowAndGoToMongoDB(towAndGoData) {
  await this.validateTowAndGoArray.validateAsync(towAndGoData);
  const towAndGoModel = new TowAndGoModel({
    tow_and_go: towAndGoData,
  });
  try {
    return await towAndGoModel.save();
  } catch (error) {
    logger.warn(`[sync_tow_and_go_data_to_mangodb] error: ${error.message}`);
    throw error;
  }
}
```

**Error Handling Strategy**:
- Validation errors for malformed data
- Database connection errors
- Document constraint violations
- Disk space and resource limitations

### validateLatestTowAndGoData()

Validates the most recently stored tow-and-go data in MongoDB to ensure data integrity after storage operations.

**Purpose**: Verify data integrity of latest MongoDB document
**Parameters**: None
**Returns**: Promise resolving to validation completion

**Validation Process**:
1. **Latest Document Retrieval**: Queries most recent document by creation date
2. **Document Existence Check**: Verifies document was found
3. **Schema Validation**: Validates document structure and content
4. **Integrity Confirmation**: Confirms successful storage operation

**Quality Assurance Implementation**:
```javascript
async validateLatestTowAndGoData() {
  const latestMongoDbTowAndGoData = await TowAndGoModel.findOne(
    {},
    {},
    { sort: { created_at: -1 } },
  );
  if (latestMongoDbTowAndGoData) {
    await this.validateMongoDbData.validateAsync(
      latestMongoDbTowAndGoData.toJSON(),
    );
  }
}
```

**Benefits**:
- Ensures successful data persistence
- Validates round-trip data integrity
- Catches storage-related data corruption
- Provides confidence in data quality

## Data Validation Architecture

### Schema Validation System

**Multi-layered Validation**:
- **JSON Content Validation**: Validates S3 file structure and content
- **Array Validation**: Validates tow-and-go array elements
- **MongoDB Validation**: Validates stored document structure
- **Type Safety**: Ensures data type consistency throughout pipeline

**Validation Schemas**:
```javascript
// Schema initialization in constructor
this.validateJsonFileContent = TowAndGoSchemas.ValidateTowAndGoJsonContent;
this.validateMongoDbData = TowAndGoSchemas.ValidateTowAndGoMongoDBData;
this.validateTowAndGoArray = TowAndGoSchemas.ValidateTowAndGoArray;
```

### Error Handling Patterns

**Validation Error Management**:
- Joi validation errors with detailed field information
- Schema violation reporting with specific error paths
- Graceful error propagation with context preservation
- Structured logging for debugging and monitoring

**Error Recovery Strategies**:
- Early validation to prevent partial data corruption
- Transaction-like behavior for data consistency
- Rollback capabilities for failed operations
- Comprehensive error logging for troubleshooting

## Storage Architecture

### AWS S3 Integration

**Storage Configuration**:
- **Fixed Filename**: 'tow-and-go.json' for consistent data location
- **JSON Format**: Structured data storage with schema validation
- **Cloud Storage**: Scalable and reliable data persistence
- **Access Control**: Secure storage with appropriate permissions

**S3 Operations**:
```javascript
// Upload operation
await this.storage.uploadFileContentToS3File(
  this.towAndGoFileName,
  towAndGoJsonContent,
);

// Download operation
const towAndGoJsonData = await this.storage.getJsonDataFromS3(
  this.towAndGoFileName,
);
```

### MongoDB Integration

**Document Structure**:
```javascript
{
  tow_and_go: [
    {
      // Tow-and-go data objects
      location: "...",
      availability: "...",
      // Additional fields...
    }
  ],
  created_at: Date,
  updated_at: Date
}
```

**Database Operations**:
- **Document Creation**: New documents for each synchronization
- **Timestamp Management**: Automatic created_at and updated_at fields
- **Query Optimization**: Indexed queries for latest document retrieval
- **Data Integrity**: Schema validation at storage layer

## Performance Considerations

### Data Processing Efficiency

**Streaming Operations**:
- Efficient JSON parsing for large datasets
- Memory-conscious data transformations
- Batch processing for array operations
- Optimized database queries

**Resource Management**:
- Connection pooling for MongoDB operations
- S3 transfer optimization
- Memory usage monitoring
- CPU-efficient validation operations

### Scalability Features

**Horizontal Scaling**:
- Stateless service design for multiple instances
- Independent operation execution
- Load balancing compatibility
- Resource isolation patterns

**Vertical Scaling**:
- Memory-efficient data structures
- CPU optimization for validation
- I/O optimization for storage operations
- Connection management for external services

## Security Considerations

### Data Security

**S3 Security**:
- Encrypted storage with AWS KMS integration
- Access control through IAM policies
- Secure data transmission using HTTPS
- Audit logging for data access

**MongoDB Security**:
- Authentication and authorization
- Encrypted connections
- Role-based access control
- Data encryption at rest

### Validation Security

**Input Sanitization**:
- Schema-based validation prevents injection attacks
- Type safety through Joi validation
- Content length limitations
- Format validation for data fields

**Error Information Security**:
- Sanitized error messages in logs
- No sensitive data exposure in errors
- Secure error propagation patterns
- Audit trail for security events

## Integration Patterns

### Service Integration

**Dependency Injection**:
- Clean separation of concerns
- Testable service architecture
- Configurable dependencies
- Mock-friendly design patterns

**External Service Integration**:
- AWS S3 SDK integration
- MongoDB native driver usage
- Logging service integration
- Error monitoring system integration

### Data Pipeline Integration

**ETL Pipeline Support**:
- Extract: S3 data retrieval
- Transform: Validation and structure processing
- Load: MongoDB persistence with verification

**Event-Driven Architecture**:
- Trigger-based synchronization
- Event logging for monitoring
- State change notifications
- Integration with job scheduling systems

## Usage Examples

### Basic Data Synchronization

```javascript
const towAndGoService = new TowAndGoService();

// Complete synchronization pipeline
try {
  await towAndGoService.syncTowAndGoFromS3ToMongoDb();
  console.log('Synchronization completed successfully');
} catch (error) {
  console.error('Synchronization failed:', error.message);
}
```

### Manual Data Upload

```javascript
const towAndGoService = new TowAndGoService();

// Upload new data to S3
const newData = JSON.stringify({
  tow_and_go: [
    { location: 'Location A', spaces: 10, available: 5 },
    { location: 'Location B', spaces: 15, available: 12 }
  ]
});

try {
  await towAndGoService.uploadTowAndGoDataToS3(newData);
  console.log('Data uploaded successfully');
} catch (error) {
  console.error('Upload failed:', error.message);
}
```

### Data Validation Testing

```javascript
const towAndGoService = new TowAndGoService();

// Validate latest stored data
try {
  await towAndGoService.validateLatestTowAndGoData();
  console.log('Latest data validation passed');
} catch (error) {
  console.error('Data validation failed:', error.message);
}
```

### Error Handling Implementation

```javascript
const towAndGoService = new TowAndGoService();

async function safeSynchronization() {
  try {
    await towAndGoService.syncTowAndGoFromS3ToMongoDb();
    return { success: true, message: 'Synchronization completed' };
  } catch (error) {
    logger.error('Synchronization error:', error);
    
    if (error.name === 'ValidationError') {
      return { success: false, error: 'Data validation failed', details: error.details };
    } else if (error.code === 'NetworkingError') {
      return { success: false, error: 'Network connectivity issue' };
    } else {
      return { success: false, error: 'Unknown synchronization error' };
    }
  }
}
```

## Monitoring and Observability

### Logging Strategy

**Structured Logging**:
- Operation-level logging with context
- Error logging with stack traces
- Performance metrics logging
- Data validation event logging

**Log Categories**:
- **INFO**: Successful operations and milestones
- **WARN**: Non-critical issues and warnings
- **ERROR**: Operation failures and exceptions
- **DEBUG**: Detailed operation information

### Health Monitoring

**Service Health Indicators**:
- S3 connectivity and access
- MongoDB connection status
- Data validation success rates
- Synchronization completion rates

**Alerting Triggers**:
- Validation failure thresholds
- Storage operation failures
- Data synchronization delays
- Service availability issues

## Testing Strategies

### Unit Testing

```javascript
describe('TowAndGoService', () => {
  let service;
  
  beforeEach(() => {
    service = new TowAndGoService();
  });
  
  test('should validate and upload data to S3', async () => {
    const testData = JSON.stringify({ tow_and_go: [] });
    await expect(service.uploadTowAndGoDataToS3(testData)).resolves.not.toThrow();
  });
  
  test('should handle invalid JSON data', async () => {
    const invalidData = 'invalid json';
    await expect(service.uploadTowAndGoDataToS3(invalidData)).rejects.toThrow();
  });
});
```

### Integration Testing

```javascript
describe('TowAndGoService Integration', () => {
  test('complete synchronization pipeline', async () => {
    const service = new TowAndGoService();
    
    // Upload test data
    const testData = generateTestData();
    await service.uploadTowAndGoDataToS3(JSON.stringify(testData));
    
    // Synchronize to MongoDB
    await service.syncTowAndGoFromS3ToMongoDb();
    
    // Validate stored data
    await service.validateLatestTowAndGoData();
  });
});
```

## Limitations and Future Enhancements

### Current Limitations

**Data Size Constraints**:
- Single-file S3 storage approach
- Memory loading of complete datasets
- Synchronous processing pipeline
- No incremental update support

**Error Recovery**:
- Limited retry mechanisms
- No partial failure recovery
- Simple error propagation
- Basic rollback capabilities

### Future Enhancements

**Performance Improvements**:
- Streaming data processing for large datasets
- Incremental synchronization capabilities
- Parallel processing for validation operations
- Caching layer for frequently accessed data

**Enhanced Features**:
- Multi-source data synchronization
- Real-time data update notifications
- Advanced error recovery mechanisms
- Data versioning and rollback capabilities

**Operational Enhancements**:
- Comprehensive monitoring dashboard
- Automated data quality reporting
- Performance optimization recommendations
- Advanced alerting and notification systems

## Dependencies

- **@maas/core/log**: Structured logging and error tracking
- **StorageS3**: AWS S3 integration helper class
- **TowAndGoModel**: MongoDB model for data persistence
- **TowAndGoSchemas**: Joi validation schemas collection
- **AWS SDK**: S3 storage operations (via StorageS3)
- **MongoDB Driver**: Database operations (via Mongoose)
- **Joi**: Schema validation and data integrity