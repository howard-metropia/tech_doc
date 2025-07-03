# TSP Job Test: Truck Map Schemas and Models Test Documentation

## Quick Summary

**Purpose**: Unit test suite for truck map data validation schemas and MongoDB models, ensuring data integrity for commercial vehicle routing restrictions and height clearance information.

**Key Features**:
- Tests TruckMapModel MongoDB schema validation
- Validates Joi schemas for truck map JSON content
- Covers create, read, and validation operations
- Tests both valid and invalid data scenarios
- Ensures proper error handling and validation messages

**Technology Stack**: Mocha testing framework, Chai assertions, Sinon for mocking, Joi validation, Mongoose ODM

## Technical Analysis

### Code Structure

The test file implements comprehensive validation testing for truck map data structures:

```javascript
// Core testing dependencies
const assert = require('assert');
const chai = require('chai');
const expect = chai.expect;
const sinon = require('sinon');
const Joi = require('joi');

// Business logic imports
const { TruckMapModel } = require('@app/src/models/TruckModel');
const { TruckMapSchemas } = require('@app/src/schemas/truckSchema');
```

### Key Components

**TruckMapModel Testing**:
- MongoDB/Mongoose model validation
- Document creation and persistence
- Schema constraint enforcement
- Error handling for invalid data structures

**Joi Schema Validation**:
- JSON content structure validation
- Data type enforcement (numbers, strings, arrays)
- Required field validation
- Detailed error message generation

**Mock Data Structures**:
```javascript
const validTruckMapData = {
  truck_map: [{
    max_height: 18,
    min_height: 16,
    present_word: "Vertical clearance between",
    segment_id: 412633298,
    link_id: 17804935
  }]
};

const validJsonContent = {
  last_modified: 1640385302,
  truck_map_array: [{
    max_height: 3.5,
    min_height: 2.1,
    present_word: "max height is 3.5 and min height is 2.1",
    segment_id: 123,
    link_id: 456
  }]
};
```

### Implementation Details

**MongoDB Model Structure**:
- Uses Mongoose schema with embedded documents
- Validates truck_map array with height restriction objects
- Supports multiple clearance points per map
- Maintains referential integrity with segment and link IDs

**Joi Schema Architecture**:
- `ValidateTruckMapJsonContent`: Validates complete JSON structure
- Supports nested array validation for truck_map_array
- Enforces numeric constraints for height values
- Requires all mandatory fields with appropriate types

**Validation Test Patterns**:
1. **Positive Tests**: Valid data scenarios that should pass
2. **Negative Tests**: Invalid data scenarios that should fail
3. **Error Message Tests**: Verification of specific error messages
4. **Boundary Tests**: Edge cases and limit validation

**Mock Implementation Strategy**:
- Uses Sinon stubs for Mongoose save operations
- Implements callback-based validation testing
- Maintains test isolation with proper cleanup
- Simulates database interaction without actual persistence

## Usage/Integration

### Test Execution

**Running Truck Schema Tests**:
```bash
# Run truck map schema and model tests
npm test test/testTruckSchemasModels.js

# Run with coverage reporting
npm run test:coverage test/testTruckSchemasModels.js
```

**Test Categories**:
- **TruckMap Model Tests**: MongoDB/Mongoose validation
- **JSON Content Validation**: Joi schema validation
- **Error Handling Tests**: Invalid data scenarios

### Integration Points

**Model Integration**:
- Integrates with `@app/src/models/TruckModel` for data persistence
- Uses Mongoose ODM for MongoDB operations
- Supports document lifecycle management

**Schema Integration**:
- Uses `@app/src/schemas/truckSchema` for validation rules
- Integrates with Joi validation framework
- Provides structured error reporting

**Service Layer Integration**:
- Supports truck routing service requirements
- Validates data before persistence operations
- Ensures data quality for commercial vehicle navigation

### Data Flow Validation

**Input Validation Pipeline**:
1. **Joi Schema Validation**: Structure and type checking
2. **Mongoose Model Validation**: Database constraint enforcement
3. **Business Logic Validation**: Domain-specific rules
4. **Persistence Validation**: Database integrity checks

## Dependencies

### Core Dependencies

**Testing Framework**:
- `chai`: Assertion library with expect and assert interfaces
- `sinon`: Mocking framework for external dependencies
- `mocha`: Test runner framework (implicit)
- `assert`: Node.js built-in assertion module

**Validation Libraries**:
- `joi`: Schema validation and data sanitization
- `mongoose`: MongoDB ODM with schema validation

**Business Logic**:
- `@app/src/models/TruckModel`: Mongoose model definitions
- `@app/src/schemas/truckSchema`: Joi validation schemas

### Schema Dependencies

**TruckMapModel Schema Requirements**:
```javascript
// MongoDB document structure
{
  _id: ObjectId,
  truck_map: [{
    max_height: Number,      // Maximum clearance height
    min_height: Number,      // Minimum clearance height  
    present_word: String,    // Descriptive text
    segment_id: Number,      // Road segment identifier
    link_id: Number         // Link/connection identifier
  }],
  created_at: Date,
  __v: Number
}
```

**JSON Content Schema Requirements**:
```javascript
// External API/file format
{
  last_modified: Number,     // Unix timestamp
  truck_map_array: [{
    max_height: Number,      // Required numeric value
    min_height: Number,      // Required numeric value
    present_word: String,    // Required string (can be null)
    segment_id: Number,      // Required numeric ID
    link_id: Number         // Required numeric ID
  }]
}
```

## Code Examples

### TruckMapModel Validation Tests

```javascript
describe('TruckMap', () => {
  let validateStub;

  beforeEach(() => {
    validateStub = sinon.stub();
  });

  afterEach(() => {
    sinon.restore();
  });

  it('should be valid if truck map model is present', (done) => {
    const truckMap = new TruckMapModel({
      truck_map: [{
        max_height: 18,
        min_height: 16,
        present_word: "Vertical clearance between",
        segment_id: 412633298,
        link_id: 17804935
      }]
    });

    truckMap.validate((err) => {
      assert.strictEqual(err, null);
      done();
    });
  });

  it('should save truck map', async () => {
    const saveStub = sinon.stub(TruckMapModel.prototype, 'save');
    const mockTruckMap = new TruckMapModel({
      truck_map: [/* valid truck map data */]
    });
    saveStub.resolves(mockTruckMap);

    const truckMapAction = new TruckMapModel(mockTruckMap);
    const saveTruckMap = await truckMapAction.save();

    expect(saveStub.calledOnce).to.be.true;
    expect(saveTruckMap).to.deep.equal(mockTruckMap);

    saveStub.restore();
  });
});
```

### Joi Schema Validation Tests

```javascript
describe('ValidateTruckMapJsonContent', () => {
  it('should validate a valid truck map JSON content using validate', () => {
    const validTruckMap = {
      last_modified: 1640385302,
      truck_map_array: [{
        max_height: 3.5,
        min_height: 2.1,
        present_word: "max height is 3.5 and min height is 2.1",
        segment_id: 123,
        link_id: 456
      }]
    };
    
    const { error } = TruckMapSchemas.ValidateTruckMapJsonContent.validate(
      validTruckMap
    );
    expect(error).to.be.undefined;
  });

  it('should fail to validate an invalid truck map JSON content', () => {
    const invalidTruckMap = {
      last_modified: 'invalid',  // Should be number
      truck_map_array: [{
        max_height: 3.5,
        min_height: 2.1,
        present_word: null,      // Can be null
        segment_id: 123,
        link_id: 456
      }]
    };
    
    const { error } = TruckMapSchemas.ValidateTruckMapJsonContent.validate(
      invalidTruckMap
    );
    const expected_error = '"last_modified" must be a number';
    expect(error).to.be.an.instanceOf(Joi.ValidationError);
    expect(error.details[0].message).to.equal(expected_error);
  });
});
```

### Mock Callback Testing Pattern

```javascript
it('should be invalid if truck map model is empty', (done) => {
  const truckMap = new TruckMapModel();
  validateStub.callsArgWith(0, null);  // Simulate callback with no error
  sinon.replace(truckMap, 'validate', validateStub);
  
  truckMap.validate((err) => {
    expect(err).to.be.null;
    expect(validateStub.calledOnce).to.be.true;
    done();
  });
});
```

### Complex Validation Scenarios

```javascript
it('should handle multiple truck map entries', (done) => {
  const truckMap = new TruckMapModel({
    truck_map: [
      {
        max_height: 18,
        min_height: 16,
        present_word: "Vertical clearance between",
        segment_id: 412633298,
        link_id: 17804935
      },
      {
        max_height: 16,
        min_height: 14,
        present_word: "Vertical clearance between",
        segment_id: 408493889,
        link_id: 17807233
      },
      {
        max_height: 18,
        min_height: 16,
        present_word: "Vertical clearance between",
        segment_id: 468559695,
        link_id: 17808045
      }
    ]
  });

  truckMap.validate((err) => {
    assert.strictEqual(err, null);
    done();
  });
});
```

### Error Message Validation

```javascript
it('should provide specific error messages for validation failures', () => {
  const invalidData = {
    last_modified: 'invalid',
    truck_map_array: [{
      max_height: null,        // Should be number
      min_height: null,        // Should be number
      present_word: 'bridge',
      segment_id: 'invalid',   // Should be number
      link_id: 1011
    }]
  };
  
  const { error } = TruckMapSchemas.ValidateTruckMapJsonContent.validate(
    invalidData
  );
  
  expect(error).to.be.an.instanceOf(Joi.ValidationError);
  expect(error.details[0].message).to.equal('"last_modified" must be a number');
});
```

This comprehensive test suite ensures the truck map data validation system maintains data integrity for commercial vehicle routing, providing reliable height clearance information while preventing invalid data from entering the system through robust schema validation and model constraints.