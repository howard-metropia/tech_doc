# Bytemark Service

## Overview

The Bytemark service provides comprehensive ticket cache management for the Bytemark transit payment system, handling OAuth token validation, ticket synchronization, and cache lifecycle management. This service serves as the primary interface between the TSP job system and Bytemark's transit ticketing infrastructure.

## Service Information

- **Service Name**: Bytemark Ticket Cache Management
- **File Path**: `/src/services/Bytemark.js`
- **Type**: Transit Payment Integration Service
- **Dependencies**: BytemarkManager, BytemarkTicketsCache, BytemarkTicketsLog, MySQL, Redis

## Core Functions

### buildTicketCache(userId)

Creates a comprehensive ticket cache for a specific user by fetching passes from both v1 and v4 Bytemark APIs.

**Purpose**: Initialize complete ticket cache from Bytemark API endpoints
**Parameters**: 
- `userId` (string): User identifier for ticket retrieval
**Returns**: BytemarkTicketsCache object or empty object

**Implementation Details**:
- Initializes BytemarkManager with environment-specific configuration
- Retrieves user OAuth token from `bytemark_tokens` table
- Fetches passes from `/passes` endpoint (v1 API) with limit 9999
- Fetches expired passes from `/v4.0/passes` endpoint with status 'EXPIRED'
- Sorts passes by creation time (oldest first)
- Generates MD5 hash for payload integrity verification
- Creates MongoDB document with structured ticket data

**Data Processing**:
```javascript
data.passes = passes
  .sort((a, b) => new Date(a.time_created).getTime() - new Date(b.time_created).getTime())
  .reduce((pre, cur) => {
    const data = {
      pass_uuid: cur.uuid,
      timestamp: Math.floor(new Date().getTime() / 1000),
      status: cur.status,
      free_ticket_status: 0,
      payload: cur,
      payload_hash: crypto.createHash('md5').update(JSON.stringify(cur)).digest('hex'),
    };
    pre.push(data);
    return pre;
  }, []);
```

**Error Handling**:
- Returns empty object if user has no valid OAuth token
- Graceful handling of API failures
- Comprehensive logging for debugging

### checkTicketCache(userId)

Orchestrates ticket cache validation and maintenance for a specific user.

**Purpose**: Ensure user has current and valid ticket cache
**Parameters**: 
- `userId` (string): User identifier for cache validation
**Returns**: Promise resolving to cache operation result

**Logic Flow**:
1. Check if cache exists for user in MongoDB
2. If exists: Update existing cache via `updateTicketCache()`
3. If not exists: Build new cache via `buildTicketCache()`

### updateTicketCache(userId, cache)

Synchronizes existing ticket cache with current Bytemark API data, handling incremental updates and expired ticket cleanup.

**Purpose**: Maintain cache accuracy with minimal API calls
**Parameters**: 
- `userId` (string): User identifier
- `cache` (object): Existing cache object (optional)
**Returns**: Updated cache object

**Complex Update Logic**:
- Filters expired passes from local cache
- Fetches current passes from both v1 and v4 APIs
- Cross-references local cache with API data to identify new tickets
- Detects free ticket additions (specific product UUIDs)
- Updates pass status and payload based on MD5 hash comparison
- Maintains separate logs for passes and passes4

**Free Ticket Detection**:
```javascript
if (
  p.product_uuid === '2417edb7-856c-43ee-b3df-c508b8be259b' ||
  p.product_uuid === '654b9f9d-5972-445b-8c6b-5c29a35c7751'
) free = true;
```

**Cache Synchronization**:
- Rebuilds passes array from API data
- Updates passes4 incrementally based on hash comparison
- Logs refresh events to bytemark_ticket_refresh_log table
- Manages free_ticket_status flags

### checkTicketCacheTimeout(userId)

Implements timeout-based cache refresh policy to ensure data freshness.

**Purpose**: Refresh cache when timeout threshold exceeded
**Parameters**: 
- `userId` (string): User identifier for timeout check
**Returns**: Promise resolving to update result

**Timeout Logic**:
- Retrieves cache timestamp from MongoDB
- Compares with current time using 60-minute timeout
- Triggers `updateTicketCache()` if threshold exceeded

### buildCacheIfEmpty()

System initialization function that builds caches for all users when system starts empty.

**Purpose**: Bootstrap ticket caches for all registered users
**Parameters**: None
**Returns**: Promise resolving to completion status

**Bootstrap Process**:
1. Counts existing cache documents in MongoDB
2. Retrieves all users with valid OAuth tokens from MySQL
3. Builds cache for each user if system cache is empty
4. Comprehensive error handling for batch operations

**Error Recovery**:
```javascript
for (const user of users) {
  try {
    await buildTicketCache(user.user_id);
  } catch (e) {
    logger.warn(`[buildCacheIfEmpty] error: ${e.message}`);
    logger.warn(`[buildCacheIfEmpty] stack: ${e.stack}`);
  }
}
```

## Technical Architecture

### BytemarkManager Configuration

The service initializes BytemarkManager with comprehensive configuration:

```javascript
const bytemark = new BytemarkManager({
  project: process.env.PROJECT_NAME || 'connectsmart',
  stage: process.env.PROJECT_STAGE || 'production',
  customerApi: config.vendor.bytemark.url.customerApi,
  accountApi: config.vendor.bytemark.url.accountApi,
  logger,
  slackToken: process.env.SLACK_BOT_TOKEN || '[REDACTED]',
  slackChannelId: process.env.SLACK_CHANNEL_ID || 'C0500872XUY',
  originApi: 'tsp-job/buildTicketCache',
  clientId: config.vendor.bytemark.clientId,
  clientSecret: config.vendor.bytemark.clientSecret,
});
```

### Data Models Integration

**MySQL Integration** (`bytemark_tokens`):
- Stores OAuth tokens for Bytemark API access
- Validates token existence before API calls
- User-specific token retrieval

**MongoDB Integration** (`BytemarkTicketsCache`):
- Primary cache storage for ticket data
- Document-based storage with complex nested structures
- Timestamp-based cache invalidation

**Logging System** (`BytemarkTicketsLog`):
- Comprehensive audit trail for ticket operations
- Individual ticket logging with full payload
- Error tracking and debugging support

### Cache Data Structure

```javascript
{
  user_id: 12345,
  timestamp: 1640995200,
  passes: [
    {
      pass_uuid: "abc-123-def",
      timestamp: 1640995200,
      status: "USABLE",
      free_ticket_status: 0,
      payload: { /* full API response */ },
      payload_hash: "md5hash"
    }
  ],
  passes4: [
    {
      pass_uuid: "xyz-789-ghi",
      timestamp: 1640995200,
      status: "EXPIRED",
      free_ticket_status: 0,
      payload: { /* full API response */ },
      payload_hash: "md5hash"
    }
  ]
}
```

## API Integration

### Bytemark API Endpoints

**Primary Passes Endpoint**:
- `GET /passes`: Retrieves active user passes
- Limit: 9999 passes per request
- Page: 1 (first page)
- Returns: Array of pass objects with full metadata

**Version 4 Passes Endpoint**:
- `GET /v4.0/passes`: Retrieves passes with specific status
- Status filter: 'EXPIRED'
- Enhanced metadata and status tracking
- Backwards compatibility with v1 format

### Error Handling Strategy

**API Failure Management**:
- Graceful degradation on API timeouts
- Slack notification integration for monitoring
- Comprehensive error logging with stack traces
- User-specific error isolation

**Data Integrity Protection**:
- MD5 hash verification for payload changes
- Transaction-like cache updates
- Rollback capability for failed operations

## Performance Optimization

### Caching Strategy

**Time-based Invalidation**:
- 60-minute timeout for cache refresh
- On-demand updates for user requests
- Batch processing for system initialization

**Incremental Updates**:
- Hash-based change detection
- Minimal API calls for unchanged data
- Efficient memory usage with selective updates

### Database Optimization

**Query Patterns**:
- Indexed user_id lookups
- Timestamp-based filtering
- Bulk insert operations for logs

**Memory Management**:
- Lazy loading of cache objects
- Garbage collection friendly operations
- Minimal object retention

## Security Considerations

### OAuth Token Management

**Token Security**:
- Secure storage in MySQL with encryption
- Token validation before API calls
- Automatic token refresh handling

**Access Control**:
- User-specific token isolation
- API key management through configuration
- Environment-specific credentials

### Data Privacy

**Sensitive Data Handling**:
- Ticket payload encryption consideration
- User data isolation in cache
- Audit trail for compliance

## Integration Points

### Internal Services

**Job Scheduler Integration**:
- Scheduled cache refresh jobs
- User-specific cache validation
- System-wide cache maintenance

**Notification System**:
- Free ticket detection notifications
- Cache refresh event logging
- Error notification via Slack

### External APIs

**Bytemark Transit API**:
- OAuth 2.0 authentication flow
- RESTful API consumption
- Rate limiting compliance

**Third-party Monitoring**:
- Slack integration for alerting
- Performance metrics collection
- Error tracking and reporting

## Deployment Considerations

### Environment Configuration

**Stage-specific Settings**:
- Development vs Production API endpoints
- Different OAuth credentials per environment
- Configurable timeout values

**Resource Requirements**:
- MongoDB storage for cache data
- MySQL for token management
- Redis for session management (implied)

### Monitoring and Alerting

**Health Checks**:
- Cache freshness validation
- API connectivity monitoring
- Token expiration tracking

**Performance Metrics**:
- Cache hit/miss ratios
- API response times
- Error rates and patterns

## Usage Examples

### Basic Cache Operations

```javascript
// Initialize cache for new user
await buildTicketCache(userId);

// Validate and refresh existing cache
await checkTicketCache(userId);

// Force refresh if timeout exceeded
await checkTicketCacheTimeout(userId);

// System bootstrap
await buildCacheIfEmpty();
```

### Error Handling Pattern

```javascript
try {
  const cache = await buildTicketCache(userId);
  if (!cache || Object.keys(cache).length === 0) {
    logger.warn(`Failed to build cache for user: ${userId}`);
    return null;
  }
  return cache;
} catch (error) {
  logger.error(`Cache operation failed: ${error.message}`);
  throw error;
}
```

## Limitations and Future Enhancements

### Current Limitations

**API Constraints**:
- Fixed page size limit (9999)
- Single page retrieval only
- Limited error recovery options

**Cache Management**:
- Memory usage for large user bases
- No automatic cleanup of orphaned caches
- Limited cache warming strategies

### Future Improvements

**Enhanced Features**:
- Paginated API consumption
- Real-time webhook integration
- Advanced caching strategies
- Multi-region cache distribution

**Performance Enhancements**:
- Parallel cache operations
- Intelligent prefetching
- Database connection pooling
- Memory optimization techniques

## Dependencies

- **@maas/core/mysql**: Database connectivity for token storage
- **@maas/services**: BytemarkManager for API integration
- **@maas/core/log**: Comprehensive logging system
- **config**: Environment-specific configuration management
- **crypto**: MD5 hashing for data integrity
- **moment**: Timezone-aware date/time handling
- **BytemarkTicketsCache**: MongoDB model for cache storage
- **BytemarkTicketsLog**: MongoDB model for audit logging