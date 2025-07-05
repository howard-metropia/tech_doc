# BytemarkTickets Model Documentation

## Overview
BytemarkTickets is a Mongoose-based model that manages cached transit ticket data in MongoDB. This model provides high-performance caching for Bytemark transit tickets, including pass information, status tracking, and error logging.

## Schema Definition
```javascript
const passObj = {
  pass_uuid: { type: String },
  timestamp: { type: Number },
  status: { type: String },
  free_ticket_status: { type: Number },
  payload: { type: Object },
  payload_hash: { type: String },
};

const passLogObj = {
  errors: {type: Array },
  server_time: { type: String },
  data: { type: Object },
};

const mongoSchema = new mongoose.Schema({
  user_id: { type: Number },
  timestamp: { type: Number },
  passes: [passObj],
  passes4: [passObj],
  passesLog: [passLogObj],
  passes4Log: [passLogObj],
}, { strict: false, supressReservedKeysWarning: true });
```

## Database Configuration
- **Database**: Cache MongoDB (`cache`)
- **Collection**: `bytemark_tickets_cache`
- **ORM**: Mongoose ODM
- **Connection**: Managed through @maas/core/mongo

## Data Structure

### Pass Object Schema
- **pass_uuid**: Unique identifier for transit pass
- **timestamp**: Creation/update timestamp
- **status**: Current pass status (active, expired, etc.)
- **free_ticket_status**: Free ticket availability status
- **payload**: Complete pass data from Bytemark API
- **payload_hash**: Data integrity verification hash

### Pass Log Object Schema
- **errors**: Array of error records
- **server_time**: Server timestamp for logging
- **data**: Associated data for log entry

### Document Structure
- **user_id**: User identifier for pass ownership
- **timestamp**: Document creation/update time
- **passes**: Array of standard pass objects
- **passes4**: Array of alternative pass format objects
- **passesLog**: Logging for standard passes
- **passes4Log**: Logging for alternative passes

## Core Functionality

### Caching Operations
- High-speed storage for frequently accessed ticket data
- Reduces API calls to external Bytemark service
- Maintains data consistency across application

### Error Tracking
- Comprehensive error logging for debugging
- Server-side error correlation
- API integration failure tracking

### Data Versioning
- Support for multiple pass formats (passes/passes4)
- Backward compatibility with legacy data
- Migration support for schema changes

## Usage Patterns

### Basic Operations
```javascript
const BytemarkTickets = require('./BytemarkTickets');

// Find user tickets
const userTickets = await BytemarkTickets.findOne({ user_id: userId });

// Update ticket cache
await BytemarkTickets.updateOne(
  { user_id: userId },
  { $set: { passes: newPasses, timestamp: Date.now() } }
);

// Add error log
await BytemarkTickets.updateOne(
  { user_id: userId },
  { $push: { passesLog: errorLogEntry } }
);
```

### Common Query Patterns
- Retrieve cached tickets for specific users
- Filter tickets by status or validity
- Aggregate error logs for monitoring
- Clean up expired cache entries

## Performance Optimization

### Indexing Strategy
- User ID indexing for fast user lookups
- Timestamp indexing for cache expiration
- Compound indexes for complex queries

### Cache Management
- TTL (Time To Live) for automatic expiration
- Memory-efficient storage patterns
- Batch updates for bulk operations

## Integration Points

### External APIs
- **Bytemark Service**: Primary data source
- **Transit Systems**: Real-time status updates
- **Payment Processors**: Transaction correlation

### Internal Components
- **Job Processors**: Background cache updates
- **API Endpoints**: Real-time data serving
- **Analytics**: Usage pattern analysis

## Error Handling
- Comprehensive error logging in passesLog arrays
- Graceful degradation on cache misses
- Retry mechanisms for failed operations
- Data validation before cache storage

## Data Integrity
- Payload hash verification for tamper detection
- Timestamp validation for freshness
- Schema validation with Mongoose
- Backup strategies for critical data

## Monitoring and Maintenance
- Cache hit/miss ratio tracking
- Performance metrics collection
- Regular cache cleanup operations
- Data consistency validation

## Security Considerations
- User data isolation
- Secure MongoDB connection handling
- Access control through application layer
- Data encryption for sensitive information

## Related Components
- **BytemarkPass**: Persistent storage counterpart
- **BytemarkOrderPayments**: Payment correlation
- **Cache Jobs**: Background maintenance processes
- **API Controllers**: Data serving endpoints

## Future Enhancements
- Redis integration for faster access
- Real-time push notifications
- Advanced analytics capabilities
- Multi-region caching support