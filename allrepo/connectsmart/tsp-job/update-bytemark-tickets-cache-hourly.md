# Update Bytemark Tickets Cache Hourly Job

## Quick Summary
**Purpose**: Performs hourly maintenance of Bytemark ticket caches for all authenticated users to ensure ticket data freshness and prevent cache timeout issues.

**Key Features**:
- Processes all users with valid Bytemark tokens
- Checks and refreshes ticket caches proactively
- Prevents cache staleness through hourly updates
- Handles errors gracefully per user

**Functionality**: Iterates through all users with Bytemark authentication tokens and validates their ticket cache status, refreshing expired caches to maintain real-time ticket availability.

## Technical Analysis

### Code Structure
The job implements a user-by-user cache validation system:

```javascript
module.exports = {
  inputs: {},
  fn: async () => {
    logger.info(`[update-bytemark-tickets-cache-hourly] enter`);
    
    // Get all users with tokens
    const users = await knex('bytemark_tokens')
      .whereNotNull('token')
      .select('user_id');
    
    const userIds = users.map((u) => u.user_id);
    
    // Process each user
    for (const userId of userIds) {
      try {
        await service.checkTicketCacheTimeout(userId);
      } catch (e) {
        logger.warn(`[update-bytemark-tickets-cache-hourly] error: ${e.message}`);
        logger.warn(`[update-bytemark-tickets-cache-hourly] stack: ${e.stack}`);
      }
    }
  },
};
```

### Implementation Details

1. **User Selection Strategy**:
   - Queries `bytemark_tokens` table for active users
   - Filters only users with non-null tokens
   - Processes all authenticated users regardless of activity

2. **Cache Timeout Logic**:
   - Delegates to `checkTicketCacheTimeout` service method
   - Timeout threshold is 60 minutes (defined in service)
   - Refreshes cache if timestamp exceeds threshold

3. **Error Isolation**:
   - Try-catch block per user prevents cascade failures
   - Continues processing even if individual users fail
   - Logs errors with full stack traces for debugging

### Database Operations

1. **User Token Query**:
   ```sql
   SELECT user_id 
   FROM bytemark_tokens 
   WHERE token IS NOT NULL
   ```

2. **Cache Validation**:
   - Checks cache timestamp in MongoDB
   - Compares against current time minus timeout
   - Triggers refresh if expired

## Usage/Integration

### Scheduling Configuration
- **Frequency**: Every hour on the hour
- **Timing**: Aligned to hour boundaries
- **Priority**: Medium - maintains data freshness

### Cron Expression
```
0 * * * * // Every hour at :00
```

### Integration Points
1. **MySQL Database**: User token storage
2. **MongoDB**: Ticket cache storage
3. **Bytemark Service**: Cache validation and refresh
4. **Bytemark API**: Ticket data retrieval

## Dependencies

### Required Modules
```javascript
const knex = require('@maas/core/mysql')('portal');
const service = require('@app/src/services/Bytemark');
const { logger } = require('@maas/core/log');
```

### Service Dependencies
The Bytemark service provides:
- `checkTicketCacheTimeout(userId)`: Validates and refreshes cache
- Cache timeout threshold (60 minutes)
- API integration for ticket retrieval

### External Services
1. **MySQL (Portal DB)**:
   - Table: `bytemark_tokens`
   - Fields: `user_id`, `token`

2. **MongoDB (Cache DB)**:
   - Collection: `BytemarkTicketsCache`
   - Timeout tracking per user

3. **Bytemark API**:
   - Pass retrieval endpoints
   - OAuth2 token validation

### Configuration Requirements
- MySQL connection for 'portal' database
- MongoDB connection for cache storage
- Bytemark API credentials
- Logging configuration

## Code Examples

### Manual Execution
```javascript
// Run the hourly cache check manually
const job = require('./update-bytemark-tickets-cache-hourly');
await job.fn();
```

### Check Specific User Cache
```javascript
// Check cache for a specific user
const service = require('@app/src/services/Bytemark');
await service.checkTicketCacheTimeout('user123');
```

### Cache Timeout Implementation
```javascript
// From Bytemark service (simplified)
async function checkTicketCacheTimeout(userId) {
  const timeout = 60 * 60; // 60 minutes in seconds
  const cache = await BytemarkTicketsCache.findOne({ user_id: userId });
  
  if (!cache || cache.timestamp < Math.floor(Date.now() / 1000) - timeout) {
    await buildTicketCache(userId);
  }
}
```

### Error Handling Pattern
```javascript
for (const userId of userIds) {
  try {
    await service.checkTicketCacheTimeout(userId);
  } catch (e) {
    // Log error but continue processing
    logger.warn(`[update-bytemark-tickets-cache-hourly] error: ${e.message}`);
    logger.warn(`[update-bytemark-tickets-cache-hourly] stack: ${e.stack}`);
    // Next user will still be processed
  }
}
```

### Performance Considerations

1. **Sequential Processing**:
   - Processes users one at a time
   - Prevents API rate limit issues
   - Allows for connection pooling

2. **Selective Updates**:
   - Only refreshes expired caches
   - Skips users with fresh data
   - Reduces unnecessary API calls

3. **Resource Usage**:
   - Low memory footprint
   - Controlled database connections
   - Predictable execution time

### Monitoring Metrics

```javascript
// Enhanced logging for monitoring
logger.info(`[update-bytemark-tickets-cache-hourly] enter`);
logger.info(`[update-bytemark-tickets-cache-hourly] userIds: ${userIds}`);

// Could be enhanced with:
// - Count of users processed
// - Count of caches refreshed
// - Average processing time per user
// - Error rate tracking
```

### Cache Lifecycle

1. **Initial Creation**:
   - User authenticates with Bytemark
   - Cache created on first ticket request

2. **Hourly Validation**:
   - This job checks all caches
   - Refreshes if older than 60 minutes

3. **On-Demand Refresh**:
   - Triggered by user activity (separate job)
   - Immediate updates for active users

4. **Cache Expiration**:
   - Prevents serving stale ticket data
   - Ensures accurate availability info

### Best Practices
- Run during off-peak hours if possible
- Monitor for users with persistent errors
- Consider parallel processing for large user bases
- Implement circuit breakers for API failures
- Track cache hit/miss ratios