# TSP Job Test: Truck Service Operations Test Documentation

## Quick Summary

**Purpose**: Comprehensive test suite for TruckMapService operations including MongoDB persistence, AWS S3 integration, and data validation across the complete truck mapping workflow.

**Key Features**:
- Tests MongoDB storage operations with Mongoose schemas
- Validates AWS S3 upload/download operations for truck map data
- Comprehensive Joi schema validation testing
- Error handling for invalid data scenarios
- Integration testing with real AWS services (mocked)
- Data integrity validation across storage layers

**Technology Stack**: Mocha testing framework, Chai assertions, Sinon for mocking, AWS SDK, Mongoose ODM, Joi validation

## Technical Analysis

### Code Structure

The test file implements a comprehensive testing framework for truck mapping services:

```javascript
// Core dependencies
const { expect } = require('chai');
const assert = require('assert');
const sinon = require('sinon');
const awsMock = require('aws-sdk-mock');

// Business logic imports
const { TruckMapService } = require('@app/src/services/TruckService');
const { StorageS3 } = require('@app/src/helpers/Storage');
const { TruckMapSchemas } = require('@app/src/schemas/truckSchema');
const { TruckMapModel } = require('@app/src/models/TruckModel');
```

### Key Components

**Service Class Architecture**:
- `TruckMapService`: Core service orchestrating truck map operations
- `StorageS3`: AWS S3 integration helper for file operations
- Data validation pipeline with Joi schemas
- MongoDB persistence with Mongoose models

**Test Coverage Areas**:
1. **MongoDB Operations**: Data persistence and validation
2. **S3 Upload Operations**: File storage and validation
3. **S3 Download Operations**: Data retrieval and validation
4. **Schema Validation**: Comprehensive data validation testing

**Mock Data Structures**:
```javascript
const validTruckMapArray = [
  {
    max_height: 15.5,
    min_height: 10.5,
    present_word: "max height is 15.5 and min height: 10.5",
    segment_id: 1,
    link_id: 2,
  },
  {
    max_height: 13.5,
    min_height: 8.5,
    present_word: "max height is 13.5 and min height: 8.5",
    segment_id: 2,
    link_id: 3,
  }
];

const validS3JsonContent = {
  last_modified: 1647043987,
  truck_map_array: validTruckMapArray
};
```

### Implementation Details

**Service Method Testing**:
- `saveTruckMapToMongoDB()`: Validates and persists truck map data
- `uploadTruckMapDataToS3()`: Uploads validated JSON to S3 bucket
- `getTruckMapJsonDataFromS3()`: Retrieves and validates S3 data
- `validateLatestTruckMap()`: Validates existing database records

**Error Handling Patterns**:
- Joi validation errors with specific field messages
- MongoDB constraint violations
- AWS S3 service errors
- Data type and format validation failures

**AWS Integration**:
- Uses `aws-sdk-mock` for S3 operation testing
- Validates JSON content before S3 upload
- Retrieves and validates data from S3 bucket
- Handles AWS service configuration and credentials

**Validation Pipeline Architecture**:
```javascript
// Input validation flow
JSON String → Joi Schema Validation → MongoDB Model Validation → Persistence
```

## Usage/Integration

### Test Execution

**Running Truck Service Tests**:
```bash
# Run complete truck service test suite
npm test test/testTruckService.js

# Run specific test categories
npm test test/testTruckService.js --grep "saveTruckMapToMongoDB"
npm test test/testTruckService.js --grep "uploadTruckMapDataToS3"
```

**Test Environment Requirements**:
- MongoDB connection for model testing
- AWS credentials configuration (mocked)
- S3 bucket configuration
- Joi schema definitions

### Service Integration Patterns

**MongoDB Integration**:
```javascript
const truckMapService = new TruckMapService();
await truckMapService.saveTruckMapToMongoDB(truckMapArray);
```

**S3 Integration**:
```javascript
const jsonContent = JSON.stringify(truckMapData);
await truckMapService.uploadTruckMapDataToS3(jsonContent);

const retrievedData = await truckMapService.getTruckMapJsonDataFromS3();
```

**Validation Integration**:
```javascript
await truckMapService.validateLatestTruckMap();
```

### AWS Configuration

**S3 Service Setup**:
```javascript
const config = require('config');
const awsConfig = config.get('vendor.aws');

// S3 bucket configuration
const bucketName = awsConfig.s3.bucket;
const region = awsConfig.region;
```

## Dependencies

### Core Dependencies

**Testing Framework**:
- `chai`: Assertion library with expect interface
- `sinon`: Mocking framework for external dependencies
- `assert`: Node.js assertion module
- `mocha`: Test runner framework (implicit)

**AWS Integration**:
- `aws-sdk-mock`: Mock AWS services for testing
- AWS S3 SDK for storage operations
- Configuration management for AWS credentials

**Database Layer**:
- `mongoose`: MongoDB ODM for schema validation
- `@app/src/models/TruckModel`: Mongoose model definitions

**Validation**:
- `joi`: Schema validation framework
- `@app/src/schemas/truckSchema`: Joi validation schemas

### Service Dependencies

**Core Services**:
- `@app/src/services/TruckService`: Main truck mapping service
- `@app/src/helpers/Storage`: S3 storage helper utilities

**Configuration**:
- `config`: Application configuration management
- AWS credentials and S3 bucket configuration
- MongoDB connection settings

### External Service Integration

**AWS S3**:
- Bucket permissions for read/write operations
- JSON file storage and retrieval
- Data validation before/after S3 operations

**MongoDB**:
- Truck map collection schema
- Document validation constraints
- Index optimization for queries

## Code Examples

### MongoDB Persistence Testing

```javascript
describe('saveTruckMapToMongoDB', () => {
  beforeEach(() => {
    truckMapService = new TruckMapService();
  });

  it('should save valid truck map data to MongoDB', async () => {
    const mockTruckMapArray = [
      {
        max_height: 15.5,
        min_height: 10.5,
        present_word: "max height is 15.5 and min height: 10.5",
        segment_id: 1,
        link_id: 2,
      }
    ];
    
    const mockTruckMapData = new TruckMapModel({
      truck_map: mockTruckMapArray,
    });
    
    const saveStub = sinon.stub(TruckMapModel.prototype, 'save');
    saveStub.resolves(mockTruckMapData);
    
    await assert.doesNotThrow(async () => {
      await truckMapService.saveTruckMapToMongoDB(mockTruckMapArray);
    });
  });

  it('should reject invalid truck map data', async () => {
    const invalidData = [
      {
        max_height: "15.5",  // Should be number
        min_height: 10.5,
        present_word: "test",
        segment_id: 1,
        link_id: 2,
      }
    ];
    
    await assert.rejects(async () => {
      await truckMapService.saveTruckMapToMongoDB(invalidData);
    });
    
    try {
      await truckMapService.saveTruckMapToMongoDB(invalidData);
    } catch (error) {
      expect(error).to.be.an.instanceOf(Joi.ValidationError);
      expect(error.details[0].message).to.equal('"[0].max_height" must be a number');
    }
  });
});
```

### S3 Upload Validation Testing

```javascript
describe('uploadTruckMapDataToS3', () => {
  beforeEach(() => {
    truckMapService = new TruckMapService();
  });

  after(() => {
    awsMock.restore('S3');
    sinon.restore();
  });

  it('should validate data before S3 upload', async () => {
    const validTruckMapData = JSON.stringify({
      last_modified: 12123231312,
      truck_map_array: [
        {
          max_height: 15.5,
          min_height: 10.5,
          present_word: "max height is 15.5 and min height: 10.5",
          segment_id: 2,
          link_id: 2,
        }
      ],
    });
    
    await assert.doesNotReject(async () => {
      await truckMapService.uploadTruckMapDataToS3(validTruckMapData);
    });
  });

  it('should reject invalid JSON structure', async () => {
    const invalidData = JSON.stringify({
      last_modified: '12123231312',  // Should be number
      truck_map_array: [
        {
          max_height: 5.3,
          min_height: 10.5,
          present_word: "test",
          segment_id: 1,
          link_id: 2,
        }
      ],
    });
    
    await assert.rejects(async () => {
      await truckMapService.uploadTruckMapDataToS3(invalidData);
    });
    
    try {
      await truckMapService.uploadTruckMapDataToS3(invalidData);
    } catch (error) {
      expect(error).to.be.an.instanceOf(Joi.ValidationError);
      expect(error.details[0].message).to.equal('"last_modified" must be a number');
    }
  });
});
```

### S3 Data Retrieval Testing

```javascript
describe('getTruckMapJsonDataFromS3', () => {
  beforeEach(() => {
    storage = new StorageS3();
    validator = TruckMapSchemas.ValidateTruckMapJsonContent;
    truckMapService = new TruckMapService();
    truckMapService.storage = storage;
    truckMapService.validatorJsonFileContent = validator;
  });

  it('should retrieve and validate S3 data successfully', async () => {
    const mockValidData = {
      last_modified: 1234567890,
      truck_map_array: [
        {
          max_height: 15.5,
          min_height: 10.5,
          present_word: "max height is 15.5 and min height: 10.5",
          segment_id: 2,
        }
      ],
    };
    
    const getJsonDataStub = sinon.stub(storage, 'getJsonDataFromS3')
      .resolves(mockValidData);
    const validateStub = sinon.stub(validator, 'validateAsync')
      .resolves();
    
    const result = await truckMapService.getTruckMapJsonDataFromS3();
    
    expect(result).to.deep.equal(mockValidData);
    expect(getJsonDataStub.calledOnceWithExactly('truck_map.json')).to.be.true;
    expect(validateStub.calledOnceWithExactly(mockValidData)).to.be.true;
  });

  it('should handle invalid S3 data', async () => {
    const mockInvalidData = {
      last_modified: "1234567890",  // Should be number
      truck_map_array: [/* valid array */],
    };
    
    const getJsonDataStub = sinon.stub(storage, 'getJsonDataFromS3')
      .resolves(mockInvalidData);
    
    try {
      await truckMapService.getTruckMapJsonDataFromS3();
    } catch (error) {
      expect(error).to.be.an.instanceOf(Joi.ValidationError);
      expect(error.details[0].message).to.equal('"last_modified" must be a number');
    }
  });
});
```

### Database Validation Testing

```javascript
describe('validateLatestTruckMap', () => {
  let truckMapService;
  let validatorStub;

  beforeEach(() => {
    truckMapService = new TruckMapService();
    validatorStub = sinon.stub(
      truckMapService.validatorMongoDbData, 'validateAsync'
    );
  });

  it('should validate latest truck map in database', async () => {
    const mockTruckMapData = {
      _id: mongoose.Types.ObjectId(),
      truck_map: [
        {
          max_height: 15.5,
          min_height: 10.5,
          present_word: "max height is 15.5 and min height: 10.5",
          segment_id: 2,
          link_id: 1
        }
      ],
      created_at: new Date(),
      __v: 0
    };
    
    const mockTruckMap = new TruckMapModel(mockTruckMapData);
    sinon.stub(TruckMapModel, 'findOne').returns(mockTruckMap);
    
    assert.doesNotThrow(async () => {
      await truckMapService.validateLatestTruckMap();
    });
  });
});
```

### Comprehensive Error Testing Pattern

```javascript
// Test all required fields
const requiredFields = ['max_height', 'min_height', 'present_word', 'segment_id', 'link_id'];

requiredFields.forEach(field => {
  it(`should require ${field} field`, async () => {
    const invalidData = { /* complete object */ };
    delete invalidData.truck_map_array[0][field];
    
    const jsonString = JSON.stringify(invalidData);
    
    await assert.rejects(async () => {
      await truckMapService.uploadTruckMapDataToS3(jsonString);
    });
    
    try {
      await truckMapService.uploadTruckMapDataToS3(jsonString);
    } catch (error) {
      expect(error).to.be.an.instanceOf(Joi.ValidationError);
      expect(error.details[0].message).to.equal(`"truck_map_array[0].${field}" is required`);
    }
  });
});
```

This comprehensive test suite ensures the truck mapping service maintains data integrity across the complete pipeline from initial validation through MongoDB persistence and S3 storage, providing reliable commercial vehicle routing data while preventing invalid information from corrupting the system.