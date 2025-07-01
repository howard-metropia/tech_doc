# TSP API Test Suite - Routes and Basic API Tests

## Overview
The `test-routes.js` file contains fundamental API route tests, focusing on basic connectivity, version endpoints, and echo functionality to ensure core API infrastructure is working correctly.

## File Location
`/allrepo/connectsmart/tsp-api/test/test-routes.js`

## Dependencies
- **supertest**: HTTP assertion library for API testing
- **chai**: Testing assertions and expectations
- **@maas/core/api**: Core API application framework
- **@maas/core**: Router and routing utilities

## Test Architecture

### API Setup
```javascript
const createApp = require('@maas/core/api');
const { getRouter } = require('@maas/core');

const app = createApp();
const router = getRouter();
const request = supertest.agent(app.listen());
```

### Core Dependencies
```javascript
require('@maas/core/bootstrap');
const supertest = require('supertest');
const chai = require('chai');
const expect = chai.expect;
```

## Basic Route Testing

### 1. Version Endpoint Test

**Purpose**: Verify API version endpoint accessibility and response

**Endpoint**: `GET /version`

```javascript
describe('test routes', () => {
  describe('GET version', () => {
    it('should 200', (done) => {
      request
        .get(router.url('version'))
        .expect(200)
        .end((err, res) => {
          if (err) return done(err);
          done();
        });
    });
  });
});
```

**Test Validation**:
- **HTTP Status**: Confirms 200 OK response
- **Endpoint Accessibility**: Verifies routing is configured correctly
- **Basic Connectivity**: Ensures API server is responsive

### 2. Echo Service Tests

**Purpose**: Test request/response handling and data validation

**Endpoint**: `POST /echo`

#### Valid Echo Request Test
```javascript
describe('test echo', () => {
  const url = router.url('echo');
  const echoRequestBody = {
    service: 'TSP API',
    version: 1.0
  };
  
  it('Valid echo request', async function () {
    const resp = await request.post(url).send(echoRequestBody);
    const { result, data } = resp.body;
    
    expect(resp.statusCode).to.eq(200);
    expect(result).to.eq('success');
    expect(data).to.include(echoRequestBody);
  });
});
```

#### Empty Echo Request Test
```javascript
const emptyRequestBody = {};

it('Empty echo request', async function () {
  const resp = await request.post(url).send(emptyRequestBody);
  const { result, data } = resp.body;
  
  expect(resp.statusCode).to.eq(200);
  expect(result).to.eq('success');
  expect(data).to.include(emptyRequestBody);
});
```

#### No Body Echo Request Test
```javascript
it('No echo request', async function () {
  const resp = await request.post(url);
  const { result, data } = resp.body;
  
  expect(resp.statusCode).to.eq(200);
  expect(result).to.eq('success');
  expect(data).to.include(emptyRequestBody);
});
```

## API Response Structure

### Standard Response Format
```javascript
{
  result: 'success' | 'fail',
  data?: any,
  error?: {
    code: number,
    message: string,
    details?: object
  }
}
```

### Success Response Example
```javascript
{
  result: 'success',
  data: {
    service: 'TSP API',
    version: 1.0,
    timestamp: '2024-01-01T12:00:00Z'
  }
}
```

## Echo Service Functionality

### Request Mirroring
The echo service reflects the incoming request data back to the client, providing:

1. **Data Validation**: Confirms request data is properly received
2. **Serialization Testing**: Verifies JSON serialization/deserialization
3. **Connection Verification**: Validates end-to-end communication

### Echo Service Implementation
```javascript
const echoService = {
  processEcho: (requestData) => {
    return {
      result: 'success',
      data: {
        ...requestData,
        echoed_at: new Date().toISOString(),
        server_info: {
          service: 'TSP API',
          environment: process.env.NODE_ENV || 'development'
        }
      }
    };
  }
};
```

## Routing Infrastructure Testing

### Router URL Generation
```javascript
// Test router URL generation functionality
const versionUrl = router.url('version');
const echoUrl = router.url('echo');

expect(versionUrl).to.be.a('string');
expect(echoUrl).to.be.a('string');
expect(versionUrl).to.include('/version');
expect(echoUrl).to.include('/echo');
```

### Route Registration Validation
```javascript
describe('Route Registration', () => {
  it('should have registered core routes', () => {
    const registeredRoutes = router.stack.map(layer => layer.path);
    
    expect(registeredRoutes).to.include('/version');
    expect(registeredRoutes).to.include('/echo');
  });
});
```

## Health Check Patterns

### API Health Validation
```javascript
const validateAPIHealth = async () => {
  const healthChecks = {
    version: false,
    echo: false,
    database: false,
    cache: false
  };
  
  try {
    // Test version endpoint
    const versionResp = await request.get(router.url('version'));
    healthChecks.version = versionResp.statusCode === 200;
    
    // Test echo endpoint
    const echoResp = await request.post(router.url('echo')).send({ test: true });
    healthChecks.echo = echoResp.statusCode === 200 && echoResp.body.result === 'success';
    
    return healthChecks;
  } catch (error) {
    return { ...healthChecks, error: error.message };
  }
};
```

## Error Handling Testing

### Network Error Simulation
```javascript
describe('Error Handling', () => {
  it('should handle network timeouts gracefully', async function () {
    this.timeout(10000);
    
    // Simulate slow network
    const slowRequest = new Promise((resolve) => {
      setTimeout(() => {
        request.post(router.url('echo'))
          .send({ test: 'timeout' })
          .then(resolve);
      }, 5000);
    });
    
    const result = await slowRequest;
    expect(result.statusCode).to.be.oneOf([200, 408, 504]);
  });
});
```

### Malformed Request Handling
```javascript
describe('Request Validation', () => {
  it('should handle malformed JSON gracefully', async () => {
    const response = await request
      .post(router.url('echo'))
      .set('Content-Type', 'application/json')
      .send('{ invalid json }');
    
    // Depending on middleware configuration
    expect(response.statusCode).to.be.oneOf([200, 400]);
  });
});
```

## Performance Testing

### Response Time Validation
```javascript
describe('Performance Tests', () => {
  it('should respond to version request quickly', async () => {
    const startTime = Date.now();
    
    const response = await request.get(router.url('version'));
    
    const endTime = Date.now();
    const responseTime = endTime - startTime;
    
    expect(response.statusCode).to.equal(200);
    expect(responseTime).to.be.lessThan(1000); // Under 1 second
  });
  
  it('should handle echo requests efficiently', async () => {
    const testData = {
      service: 'TSP API',
      timestamp: new Date().toISOString(),
      data: Array(100).fill('test') // Larger payload
    };
    
    const startTime = Date.now();
    
    const response = await request.post(router.url('echo')).send(testData);
    
    const endTime = Date.now();
    const responseTime = endTime - startTime;
    
    expect(response.statusCode).to.equal(200);
    expect(responseTime).to.be.lessThan(2000); // Under 2 seconds
    expect(response.body.data).to.deep.include(testData);
  });
});
```

## Integration Validation

### Cross-Service Communication
```javascript
describe('Integration Tests', () => {
  it('should maintain session across requests', async () => {
    // First request
    const firstResp = await request
      .post(router.url('echo'))
      .send({ sequence: 1 });
    
    // Second request (should maintain agent session)
    const secondResp = await request
      .post(router.url('echo'))
      .send({ sequence: 2 });
    
    expect(firstResp.statusCode).to.equal(200);
    expect(secondResp.statusCode).to.equal(200);
    expect(firstResp.body.data.sequence).to.equal(1);
    expect(secondResp.body.data.sequence).to.equal(2);
  });
});
```

## Quality Assurance

### Test Coverage
- **Basic Connectivity**: Core API accessibility
- **Request Handling**: Various request types and sizes
- **Response Consistency**: Standard response format adherence
- **Error Scenarios**: Graceful error handling
- **Performance**: Response time validation

### API Contract Validation
- **Status Codes**: Correct HTTP status code usage
- **Response Format**: Consistent JSON response structure
- **Content Types**: Proper content-type handling
- **Request Methods**: Appropriate HTTP method support

## Debugging and Monitoring

### Request Logging
```javascript
const logAPIRequest = (req, res, next) => {
  console.log(`${req.method} ${req.path}`, {
    body: req.body,
    query: req.query,
    headers: req.headers,
    timestamp: new Date().toISOString()
  });
  next();
};
```

### Response Monitoring
```javascript
const monitorAPIResponse = (req, res, next) => {
  const originalSend = res.send;
  
  res.send = function(data) {
    console.log(`Response for ${req.method} ${req.path}:`, {
      statusCode: res.statusCode,
      data: data,
      responseTime: Date.now() - req.startTime
    });
    
    originalSend.call(this, data);
  };
  
  next();
};
```

This fundamental test suite ensures the basic API infrastructure is functioning correctly, providing a foundation for more complex service testing while validating core connectivity, request handling, and response consistency.