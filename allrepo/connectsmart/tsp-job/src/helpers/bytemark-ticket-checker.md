# Bytemark Ticket Checker Helper

## Overview
**File**: `src/helpers/bytemark-ticket-checker.js`  
**Type**: Helper Module  
**Purpose**: Validates and manages Bytemark transit tickets and passes through pagination API

## Key Functions

### Core Validation Functions
- **hasNext()**: Validates pagination metadata and determines if more pages exist
- **extractErrorData()**: Extracts error information from token items
- **getPassUuids()**: Retrieves all pass UUIDs for a user token with pagination
- **getOrderUuids()**: Retrieves all order item UUIDs for a user token with pagination

### Dependencies
- `@maas/core/log`: Logging functionality

## Implementation Details

### Pagination Management
```javascript
const hasNext = pageInfo => {
  const { pageCount, totalCount, pagination } = pageInfo;
  const realCount = (pagination.page - 1) * pagination.per_page + pageCount;
  return !!pagination.next && realCount <= totalCount;
};
```

### Pass UUID Retrieval
- **Per Page**: 20 items
- **Error Handling**: Returns null on API errors
- **Pagination**: Continues until no more pages

### Order UUID Retrieval  
- **Per Page**: 30 items
- **Data Processing**: Flattens order items to extract UUIDs
- **Termination**: Stops when no orders found

## API Integration

### Error Detection
```javascript
const hasError = (resp) => resp.errors && resp.errors.length;
```

### Dependency Injection
```javascript
setManager: (manager) => {
  BytemarkTicketChecker.bytemarkCli = manager;
}
```

## Data Flow

### Pass Processing
1. Initialize pagination (page=1, perPage=20)
2. Fetch pass data via API
3. Extract order_item UUIDs from passes
4. Continue pagination if hasNext() returns true
5. Return consolidated UUID array

### Order Processing
1. Initialize pagination (page=1, perPage=30) 
2. Fetch order data via API
3. Flatten order_items to extract UUIDs
4. Continue pagination until no more orders
5. Return consolidated UUID array

## Error Handling

### Response Validation
- **Empty Response**: Returns null
- **API Errors**: Returns null if errors array exists
- **Empty Data**: Returns null if no passes/orders found

### Logging
- Logs invalid page info with details
- Uses structured error messages

## Usage Example

```javascript
const checker = require('./bytemark-ticket-checker');

// Set up the manager
checker.setManager(bytemarkApiManager);

// Get pass UUIDs
const passUuids = await checker.getPassUuids(userToken);

// Get order UUIDs  
const orderUuids = await checker.getOrderUuids(userToken);
```

## Configuration

### Constants
- **Pass Page Size**: 20 items per request
- **Order Page Size**: 30 items per request
- **Error Response**: Returns null on any failure

## Response Structure

### Pass Response
```javascript
{
  data: {
    pagination: { page, per_page, next },
    page_count: number,
    total_count: number,
    passes: [{ order_item: { uuid } }]
  }
}
```

### Order Response  
```javascript
{
  data: {
    pagination: { page, per_page, next },
    page_count: number,
    total_count: number,
    orders: [{ order_items: [{ uuid }] }]
  }
}
```

## Performance Considerations

### Pagination Strategy
- Uses appropriate page sizes for different endpoints
- Processes all pages in sequence
- Accumulates results before returning

### Memory Management
- Builds UUID arrays incrementally
- Uses spread operator for efficient array concatenation

## Integration Points

### External Dependencies
- **Bytemark API**: Merchant API for pass/order data
- **MaaS Core**: Logging infrastructure

### Service Integration
- Designed for dependency injection pattern
- Manager must be set before use
- Returns standardized UUID arrays

## Testing Considerations

### Mock Points
- `bytemarkCli.getPass()` method
- `bytemarkCli.getOrder()` method
- Pagination response structure

### Edge Cases
- Empty responses
- API errors
- Invalid pagination data
- Large datasets requiring multiple pages

## Security Notes

### Data Handling
- No sensitive data logging
- Token passed through securely
- UUID-only response format

### Error Information
- Sanitized error responses
- No credential exposure
- Structured error data extraction