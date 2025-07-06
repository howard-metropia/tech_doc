# test-passuse.js Technical Documentation

## Purpose

Unit test suite for transit pass usage system, testing the integration with Bytemark ticketing service and database record management for transit pass validation.

## Core Functionality

### Pass Usage System

#### Service: `passUse`
- **Purpose**: Validate and record transit pass usage
- **Integration**: Bytemark ticketing system
- **Parameters**: Context object, user data (user ID, pass UUID, event UUID)
- **Returns**: Pass usage validation result

#### Bytemark Integration
- **Service**: `BytemarkManager`
- **Method**: `usePass`
- **Purpose**: External validation of transit pass usage
- **Response**: Success/error status with validation details

## Test Architecture

### Test Setup
```javascript
describe('unit test for passUse', () => {
  const ctx = {
    request: {
      method: 'POST',
      path: '/api/v2/transit_payment/pass_use',
    }
  };
  
  let stub1;
  const userId = 1003;
  const pass_uuid = 'pass_uuid';
});
```

### Mock Strategy
```javascript
// Successful pass usage mock
stub1 = sinon.stub(BytemarkManager.prototype, 'usePass').resolves({
  errors: [],  // Empty errors array indicates success
});

// Failed pass usage mock
stub1 = sinon.stub(BytemarkManager.prototype, 'usePass').resolves({
  errors: [{
    code: 50020,
    message: "Unfortunately, your session has expired. Please log back in."
  }],
});
```

## Test Scenarios

### Successful Pass Usage
```javascript
describe('successful passUse should add bytemark_pass records', () => {
  beforeEach(async () => {
    stub1 = sinon.stub(BytemarkManager.prototype, 'usePass').resolves({
      errors: [],
    });
  });

  afterEach(async () => {
    stub1.restore();
    await knex('bytemark_pass').where({ pass_uuid }).del();
  });

  it('should add bytemark_pass records', async () => {
    const passUse = require('@app/src/services/transit-payment').passUse;
    const data = {
      userId,
      pass_uuid,
      event_uuid: 'event_uuid',
    };
    
    const result = await passUse(ctx, data);
    expect(result).to.be.an('object');
    
    // Verify database record created
    const row = await knex('bytemark_pass').where({ pass_uuid });
    expect(row.length).to.equal(1);
  });
});
```

### Failed Pass Usage
```javascript
describe('failed passUse should not add bytemark_pass records', () => {
  beforeEach(async () => {
    stub1 = sinon.stub(BytemarkManager.prototype, 'usePass').resolves({
      errors: [{
        code: 50020,
        message: "Unfortunately, your session has expired. Please log back in."
      }],
    });
  });

  it('should not add bytemark_pass records', async () => {
    const passUse = require('@app/src/services/transit-payment').passUse;
    const data = {
      userId,
      pass_uuid: 'pass_uuid',
      event_uuid: 'event_uuid',
    };
    
    try {
      const result = await passUse(ctx, data);
      expect(true).to.equal(false, 'should not reach here');
    } catch (e) {
      expect(e).to.be.an('ERROR_PASS_DATA');
      expect(e.message).to.equal('ERROR_PASS_DATA');
      
      // Verify no database record created
      const row = await knex('bytemark_pass').where({pass_uuid: data.pass_uuid});
      expect(row.length).to.equal(0);
    }
  });
});
```

## Data Models

### Pass Usage Data Structure
```javascript
const passUseData = {
  userId: 'integer',        // User making the pass usage
  pass_uuid: 'string',      // Unique pass identifier
  event_uuid: 'string',     // Event/trip identifier
};
```

### Bytemark Response Structure
```javascript
// Successful response
const successResponse = {
  errors: []  // Empty array indicates success
};

// Error response
const errorResponse = {
  errors: [{
    code: 50020,
    message: "Unfortunately, your session has expired. Please log back in."
  }]
};
```

### Database Record Structure
```javascript
const bytemarkPassRecord = {
  id: 'integer',
  user_id: 'integer',
  pass_uuid: 'string',
  event_uuid: 'string',
  created_at: 'timestamp',
  updated_at: 'timestamp'
};
```

## Error Handling

### Bytemark Service Errors
- **Code 50020**: Session expired
- **Authentication**: Invalid credentials
- **Validation**: Pass usage validation failures
- **Network**: Service connectivity issues

### Application Error Types
- **ERROR_PASS_DATA**: Generic pass data validation error
- **Database Errors**: Record insertion failures
- **Service Unavailable**: Bytemark service down

## Business Logic

### Pass Validation Flow
1. **Input Validation**: Verify required fields (user ID, pass UUID, event UUID)
2. **External Validation**: Call Bytemark service for pass verification
3. **Response Processing**: Check for errors in Bytemark response
4. **Database Recording**: Create record only on successful validation
5. **Error Handling**: Prevent database changes on validation failure

### Transaction Integrity
- **Atomic Operations**: Database record created only on success
- **Rollback Strategy**: No database changes on external service failure
- **Consistency**: Maintain data consistency between systems

## Integration Points

### Bytemark Ticketing System
- **Service**: External transit ticketing provider
- **Protocol**: API-based integration
- **Authentication**: Service-to-service authentication
- **Validation**: Real-time pass validation

### Database Systems
- **Table**: `bytemark_pass`
- **Purpose**: Local record of pass usage events
- **Indexing**: Optimized for pass UUID lookups
- **Relationships**: Links to user and event data

## Performance Considerations

### External Service Integration
- **Timeout Handling**: Graceful timeout management
- **Retry Logic**: Handle temporary service failures
- **Circuit Breaker**: Prevent cascade failures
- **Response Caching**: Cache validation results when appropriate

### Database Performance
- **Index Strategy**: Optimize frequent lookup patterns
- **Connection Pooling**: Efficient database connections
- **Bulk Operations**: Handle high-volume pass usage

## Security Features

### Data Protection
- **Pass UUID Security**: Secure handling of pass identifiers
- **User Validation**: Verify user authorization for pass usage
- **Audit Trail**: Complete usage history maintained

### Service Security
- **Authentication**: Secure Bytemark service communication
- **Rate Limiting**: Prevent abuse of validation service
- **Input Sanitization**: Validate all input parameters

## Monitoring and Analytics

### Key Metrics
- **Success Rate**: Percentage of successful pass validations
- **Response Time**: Bytemark service response times
- **Error Frequency**: Rate of validation failures
- **Usage Patterns**: Pass usage frequency and timing

### Alert Conditions
- **High Error Rate**: Unusual validation failure rate
- **Service Unavailable**: Bytemark service downtime
- **Database Issues**: Record insertion failures

## Testing Strategy

### Mock Management
```javascript
beforeEach(async () => {
  stub1 = sinon.stub(BytemarkManager.prototype, 'usePass')
    .resolves(mockResponse);
});

afterEach(async () => {
  stub1.restore();
  await knex('bytemark_pass').where({ pass_uuid }).del();
});
```

### Data Cleanup
- **Test Isolation**: Clean database state between tests
- **Mock Restoration**: Restore original service methods
- **State Reset**: Reset all test dependencies

## Usage Examples

### Successful Pass Usage
```javascript
const passUseService = require('@app/src/services/transit-payment').passUse;

const ctx = {
  request: {
    method: 'POST',
    path: '/api/v2/transit_payment/pass_use'
  }
};

const data = {
  userId: 1003,
  pass_uuid: 'abc123-def456-ghi789',
  event_uuid: 'event-xyz789'
};

try {
  const result = await passUseService(ctx, data);
  console.log('Pass usage recorded successfully');
} catch (error) {
  console.log(`Pass usage failed: ${error.message}`);
}
```

### Error Handling
```javascript
try {
  const result = await passUse(ctx, data);
  
  // Check if Bytemark validation succeeded
  if (!result.errors || result.errors.length === 0) {
    console.log('Pass validated successfully');
  } else {
    console.log('Validation failed:', result.errors[0].message);
  }
} catch (error) {
  switch (error.message) {
    case 'ERROR_PASS_DATA':
      console.log('Pass data validation failed');
      break;
    default:
      console.log('Unexpected error:', error.message);
  }
}
```

### Database Verification
```javascript
// Check if pass usage was recorded
const passRecord = await knex('bytemark_pass')
  .where({ 
    user_id: userId,
    pass_uuid: passUuid 
  })
  .first();

if (passRecord) {
  console.log('Pass usage recorded in database');
} else {
  console.log('No database record found');
}
```

This test suite ensures reliable transit pass usage functionality, validating the integration between the application and Bytemark ticketing system while maintaining proper database record management and error handling.