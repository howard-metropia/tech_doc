# BytemarkTicketsLog Model

## Overview
MongoDB logging model for tracking Bytemark ticket operations and transactions. This model provides comprehensive audit trail capabilities for monitoring ticket lifecycle events, user interactions, and system operations within the Bytemark transit ticketing integration.

## File Location
`/src/models/BytemarkTicketsLog.js`

## Model Definition
```javascript
const mongoose = require('mongoose');
const conn = require('@maas/core/mongo')('cache');

const mongoSchema = new mongoose.Schema(
  {
    user_id: { type: Number },
    timestamp: { type: Number },
    uuid: { type: String },
    status: { type: String },
  },
  { strict: false },
);
const BytemarkTicketsLog = conn.model('bytemark_tickets_log', mongoSchema);

module.exports = BytemarkTicketsLog;
```

## Database Configuration
- **Database**: MongoDB cache instance
- **Collection**: `bytemark_tickets_log`
- **Framework**: Mongoose ODM
- **Connection**: Managed by @maas/core MongoDB connection pool
- **Schema Mode**: Non-strict (allows additional fields)

## Schema Definition

### Core Fields

#### user_id
- **Type**: Number
- **Purpose**: Identifies the user associated with the ticket operation
- **Usage**: Links ticket logs to specific user accounts
- **Indexing**: Consider indexing for user-based queries

#### timestamp
- **Type**: Number
- **Purpose**: Unix timestamp of the ticket operation
- **Format**: Unix epoch time for precise timing
- **Usage**: Chronological ordering and time-based queries

#### uuid
- **Type**: String
- **Purpose**: Unique identifier for the ticket or transaction
- **Format**: UUID string format
- **Usage**: Correlation with external Bytemark systems

#### status
- **Type**: String
- **Purpose**: Current status of the ticket operation
- **Values**: "purchased", "validated", "expired", "refunded", "cancelled"
- **Usage**: Track ticket lifecycle states

### Extended Fields (Non-strict Schema)
```javascript
{
  // Core schema fields above
  ticket_type: String,        // Type of ticket (daily, weekly, monthly)
  purchase_amount: Number,    // Cost of the ticket
  validation_location: String, // Where ticket was validated
  expiration_date: Date,      // When ticket expires
  refund_amount: Number,      // Amount refunded if applicable
  payment_method: String,     // How ticket was purchased
  route_info: Object,         // Transit route information
  device_info: Object,        // Device used for purchase/validation
  error_details: Object       // Error information if operation failed
}
```

## Purpose and Functionality
- **Transaction Logging**: Records all ticket purchase and validation events
- **User Activity Tracking**: Monitors user interaction with Bytemark tickets
- **Audit Trail**: Provides comprehensive history for financial reconciliation
- **System Monitoring**: Enables tracking of ticket system performance and issues

## Key Features
- **Flexible Schema**: Non-strict mode accommodates evolving logging requirements
- **User-Ticket Correlation**: Links ticket operations to specific users
- **Timestamp Precision**: Unix timestamp for accurate time tracking
- **UUID Integration**: Compatible with external ticketing systems
- **Status Tracking**: Comprehensive ticket lifecycle monitoring

## Usage Patterns

### Ticket Purchase Logging
```javascript
const purchaseLog = {
  user_id: 12345,
  timestamp: Math.floor(Date.now() / 1000),
  uuid: 'bytemark-ticket-abc123',
  status: 'purchased',
  ticket_type: 'daily_pass',
  purchase_amount: 5.50,
  payment_method: 'credit_card'
};

await BytemarkTicketsLog.create(purchaseLog);
```

### Ticket Validation Logging
```javascript
const validationLog = {
  user_id: 12345,
  timestamp: Math.floor(Date.now() / 1000),
  uuid: 'bytemark-ticket-abc123',
  status: 'validated',
  validation_location: 'Metro Station A',
  route_info: {
    route_id: 'route_123',
    direction: 'northbound'
  }
};

await BytemarkTicketsLog.create(validationLog);
```

## Integration Points
- **Bytemark API**: Receives ticket data from external Bytemark systems
- **User Management**: Correlates with user accounts and authentication
- **Payment Processing**: Links with payment transaction systems
- **Transit Services**: Integrates with route and validation infrastructure

## Operational Workflows

### Purchase Workflow
1. **User Initiates Purchase**: User selects and purchases ticket
2. **Payment Processing**: Payment system processes transaction
3. **Ticket Generation**: Bytemark system generates ticket with UUID
4. **Log Creation**: Purchase event logged with user, timestamp, and details
5. **Confirmation**: User receives purchase confirmation

### Validation Workflow
1. **User Presents Ticket**: User shows ticket at validation point
2. **System Validation**: Ticket validity checked against Bytemark system
3. **Status Update**: Ticket status updated based on validation result
4. **Log Entry**: Validation event logged with location and result
5. **Access Grant/Deny**: User granted or denied transit access

## Query Patterns

### User Ticket History
```javascript
// Get all tickets for a specific user
const userTickets = await BytemarkTicketsLog.find({ user_id: 12345 })
  .sort({ timestamp: -1 });
```

### Status-based Queries
```javascript
// Find all validated tickets in date range
const validatedTickets = await BytemarkTicketsLog.find({
  status: 'validated',
  timestamp: { 
    $gte: startTimestamp, 
    $lte: endTimestamp 
  }
});
```

## Performance Considerations
- **Indexing Strategy**: Create indexes on user_id, timestamp, and status
- **Bulk Operations**: Support batch logging for high-volume scenarios
- **Connection Pooling**: Leverage @maas/core MongoDB connection management
- **Query Optimization**: Optimize common query patterns for user history and status tracking

## Data Analytics Applications
- **Revenue Tracking**: Monitor ticket sales and payment patterns
- **Usage Analytics**: Analyze ticket validation patterns and popular routes
- **User Behavior**: Track user purchasing and travel patterns
- **System Performance**: Monitor ticket system reliability and response times

## Monitoring and Alerting
- **Failed Transactions**: Alert on high failure rates
- **Revenue Anomalies**: Detect unusual purchase patterns
- **System Downtime**: Monitor ticket system availability
- **User Issues**: Track user-reported problems with tickets

## Data Retention and Archival
- **Financial Records**: Maintain for regulatory compliance periods
- **User Privacy**: Consider data retention policies for user data
- **Archive Strategy**: Move old logs to long-term storage
- **Cleanup Procedures**: Regular maintenance of log collections

## Security and Compliance
- **PCI Compliance**: Ensure payment data handling meets standards
- **User Privacy**: Protect user travel pattern information
- **Data Encryption**: Encrypt sensitive fields in logs
- **Access Control**: Restrict log access to authorized personnel

## Integration with Related Models
- **BytemarkTickets**: Source ticket data and current status
- **BytemarkCacheStatusCheckLog**: Cache validation operations
- **UserWallet**: Financial transactions and balance updates
- **TransitAlert**: Integration with transit system notifications

## Development Considerations
- **Schema Evolution**: Non-strict schema supports new field additions
- **Error Handling**: Comprehensive error logging for troubleshooting
- **Testing**: Include logging in ticket operation test scenarios
- **Documentation**: Maintain field definitions as schema evolves