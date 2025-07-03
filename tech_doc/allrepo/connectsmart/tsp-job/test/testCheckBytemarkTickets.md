# Bytemark Ticket Checker Test Suite

## Overview
Comprehensive test suite for the Bytemark ticket validation system that verifies pass and order retrieval functionality, pagination handling, and integration with the Bytemark transit API.

## File Location
`/test/testCheckBytemarkTickets.js`

## Dependencies
- `chai` - Assertion library with expect interface
- `@maas/core/bootstrap` - Application initialization
- `config` - Configuration management
- `@app/src/helpers/bytemark-ticket-checker` - Ticket validation helper functions
- `@maas/services/src/bytemark` - Bytemark service manager

## Test Architecture

### Helper Functions Under Test
```javascript
const { 
  getPassUuids, 
  setManager, 
  getOrderUuids, 
  hasNext 
} = require('@app/src/helpers/bytemark-ticket-checker');
```

### Test Categories
1. **Unit Testing**: Pagination logic validation
2. **Component Testing**: Mock API response handling  
3. **Integration Testing**: Real Bytemark API interaction

## Utility Functions

### Mock UUID Generation
```javascript
const createMockUUIDs = (perPage, total, createFn) => {
  const pageCount = Math.ceil(total / perPage);
  const uuids = {};
  for (let i = 1; i <= pageCount; i++) {
    const start = (i - 1) * perPage + 1;
    const end = i === pageCount ? total : i * perPage;
    const pageUuids = Array.from(
      { length: end - start + 1 },
      (_, j) => createFn(`${start + j}`)
    );
    uuids[i] = pageUuids;
  }
  return uuids;
};
```
- **Purpose**: Generates paginated UUID sets for testing
- **Parameters**: Items per page, total items, UUID creation function
- **Returns**: Object with page numbers as keys and UUID arrays as values

## Unit Testing: Pagination Logic

### hasNext Function Testing
```javascript
describe('hasNext testing', function() {
  it('should throw an error if page info is invalid', () => {
    const pageInfo = {};
    const expected = false;
    const actual = hasNext(pageInfo);
    expect(actual).to.equal(expected);
  });
});
```

#### Test Scenarios
1. **Invalid Page Info**: Empty object returns false
2. **Has Next Page**: Pagination object with next=true returns true
3. **No Next Page**: Pagination object with next=false returns false

#### Page Info Structure
```javascript
const pageInfo = {
  pageCount: 10,
  totalCount: 20,
  pagination: {
    page: 1,
    per_page: 10,
    next: true // or false
  }
};
```

## Component Testing: Mock API Responses

### Mock Bytemark Manager
```javascript
const mockBytemarkManager = {
  getPass: (token, perPage, page) => { /* Mock implementation */ },
  getOrder: (token, perPage, page) => { /* Mock implementation */ }
};
```

### Pass Retrieval Testing

#### Single Page Response
```javascript
const singlePageResponse = (token, perPage, page) => {
  return {
    errors: [],
    data: {
      passes: [{
        order_item: { uuid: '123' }
      }],
      page_count: 1,
      total_count: 1,
      pagination: {
        page: 1,
        per_page: 10
      }
    }
  };
};
```

#### Multiple Page Response
```javascript
const multiplePageResponse = (token, perPage, page) => {
  const currentPage = page;
  const create = id => ({
    order_item: { uuid: id }
  });
  
  const mockUUIDs = createMockUUIDs(perPage, mockLength, create);
  const respUUIDs = mockUUIDs[currentPage];
  
  return {
    error: null,
    data: {
      passes: respUUIDs,
      page_count: respUUIDs.length,
      total_count: mockLength,
      pagination: {
        page: currentPage,
        per_page: perPage,
        next: currentPage === Object.keys(mockUUIDs).length ? null : '/next/page/'
      }
    }
  };
};
```

### Order Retrieval Testing

#### Order Response Structure
```javascript
{
  error: null,
  data: {
    orders: [{
      order_items: [{
        uuid: '123'
      }]
    }],
    page_count: 1,
    total_count: 1,
    pagination: {
      page: 1,
      per_page: 10
    }
  }
}
```

#### Test Validation
```javascript
it('should return multiple orders', async function() {
  mockBytemarkManager.getOrder = multiplePageResponse;
  setManager(mockBytemarkManager);
  const res = await getOrderUuids('fakeToken');
  expect(res).to.have.length(mockLength);
});
```

## Integration Testing: Real API Interaction

### Configuration Setup
```javascript
const BytemarkManager = require('@maas/services/src/bytemark');
const validUatToken = 'lQdwetnj4eximOQuWyJpRADEIe4xfxSq';

const bytemarkConfig = {
  project: config.get('app.project') ?? 'ConnectSmart',
  stage: process.env.PROJECT_STAGE ?? 'local',
  customerApi: config.vendor.bytemark.url.customerApi ?? 'https://overture-uat.bytemark.co',
  slackToken: process.env.SLACK_BOT_TOKEN,
  slackChannelId: process.env.SLACK_CHANNEL_ID,
  originApi: 'tsp-job/check-bytemark-tickets'
};
```

### Real API Testing
```javascript
describe('integration testing', function() {
  this.timeout(20 * 1000); // 20 second timeout
  
  it('should not be empty passed', async () => {
    const uuids = await getPassUuids(validUatToken);
    expect(uuids).length.gt(0);
  });
  
  it('should not be empty orders', async () => {
    const uuids = await getOrderUuids(validUatToken);
    expect(uuids.length).gt(0);
  });
});
```

## Data Structures

### Pass Data Structure
```javascript
{
  order_item: {
    uuid: 'unique-identifier-string'
  }
}
```

### Order Data Structure
```javascript
{
  order_items: [{
    uuid: 'unique-identifier-string'
  }]
}
```

### Pagination Structure
```javascript
{
  page: 1,                    // Current page number
  per_page: 10,              // Items per page
  next: true|false|'/path/'  // Next page indicator
}
```

## Business Logic Validation

### UUID Extraction Logic
- **Pass UUIDs**: Extracted from `order_item.uuid` field
- **Order UUIDs**: Extracted from `order_items[].uuid` field
- **Flattening**: Order items arrays are flattened into single UUID list

### Pagination Handling
- **Automatic Pagination**: Functions handle multi-page responses automatically
- **Token Management**: Uses provided authentication tokens for API access
- **Error Resilience**: Continues processing despite individual page failures

## Error Handling

### API Error Management
```javascript
{
  errors: [], // Error array for API issues
  error: null // Single error field alternative
}
```

### Network Timeout Handling
- **Integration Tests**: 20-second timeout for real API calls
- **Component Tests**: Immediate response from mocks
- **Retry Logic**: Built into underlying Bytemark manager

## Performance Considerations

### Mock Performance
- **Synchronous Operations**: Fast execution through mocked responses
- **Memory Efficiency**: Minimal data structures for testing
- **Scalability Testing**: Validates handling of large UUID sets

### Real API Performance
- **Timeout Management**: Appropriate timeouts for network calls
- **Rate Limiting**: Respects Bytemark API rate limits
- **Caching**: Leverages any caching in the Bytemark manager

## Configuration Dependencies

### Environment Variables
- `PROJECT_STAGE`: Environment stage (local, dev, prod)
- `SLACK_BOT_TOKEN`: Slack integration token
- `SLACK_CHANNEL_ID`: Slack notification channel

### Config Objects
- `config.get('app.project')`: Project identifier
- `config.vendor.bytemark.url.customerApi`: Bytemark API endpoint
- `config.vendor.bytemark.clientId`: OAuth client ID
- `config.vendor.bytemark.clientSecret`: OAuth client secret

## Quality Assurance

### Test Coverage Areas
1. **Pagination Logic**: Validates proper page navigation
2. **Data Extraction**: Confirms correct UUID extraction
3. **API Integration**: Tests real Bytemark API interaction
4. **Error Scenarios**: Handles various failure conditions

### Assertion Strategies
- **Length Validation**: Confirms expected number of results
- **Structure Validation**: Verifies correct data structures
- **Integration Validation**: Ensures real API connectivity
- **Boolean Logic**: Tests pagination decision logic

## Maintenance Considerations

### API Evolution
- **Schema Changes**: May require updates if Bytemark API changes
- **Authentication**: Token management may need updates
- **Endpoint Changes**: URL configurations may require updates

### Test Data Management
- **Mock Length**: Configurable mock data sizes for different scenarios
- **UUID Patterns**: Realistic UUID generation for testing
- **Page Size Testing**: Various pagination configurations

## Security Considerations

### Token Management
- **Test Tokens**: Uses UAT environment tokens for testing
- **Token Rotation**: Tests should handle token expiration gracefully
- **API Security**: Respects Bytemark API security requirements

### Data Privacy
- **UUID Handling**: Treats UUIDs as sensitive identifiers
- **Logging**: Careful logging of sensitive data during testing
- **Test Isolation**: Prevents test data from affecting production systems