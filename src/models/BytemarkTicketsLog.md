# BytemarkTicketsLog Model Documentation

### 📋 Model Overview
- **Purpose:** Logs Bytemark ticket operations and transactions for audit and debugging
- **Table/Collection:** bytemark_tickets_log
- **Database Type:** MongoDB
- **Relationships:** References users through user_id field

### 🔧 Schema Definition

| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| user_id | Number | No | ID of the user associated with the ticket operation |
| timestamp | Number | No | Unix timestamp of the operation |
| uuid | String | No | Unique identifier for the operation |
| status | String | No | Status or result of the ticket operation |
| *Additional fields* | Various | No | Flexible schema allows other fields |

### 🔑 Key Information
- **Primary Key:** _id (MongoDB default)
- **Indexes:** Not specified in schema
- **Unique Constraints:** Not specified
- **Default Values:** None specified
- **Schema Mode:** Flexible (strict: false)

### 📝 Usage Examples
```javascript
// Log a new ticket operation
const ticketLog = new BytemarkTicketsLog({
  user_id: 12345,
  timestamp: Date.now(),
  uuid: 'ticket-op-abc123',
  status: 'success',
  operation_type: 'purchase',
  ticket_details: { route: 'A-B', fare: 2.50 }
});
await ticketLog.save();

// Find logs for a specific user
const userLogs = await BytemarkTicketsLog.find({ user_id: 12345 })
  .sort({ timestamp: -1 })
  .limit(50);

// Find failed operations
const failedOps = await BytemarkTicketsLog.find({ status: 'failed' });

// Get recent logs
const recentLogs = await BytemarkTicketsLog.find({
  timestamp: { $gte: Date.now() - 24 * 60 * 60 * 1000 }
});
```

### 🔗 Related Models
- BytemarkTicketRefreshLog - Related logging for refresh operations
- User authentication models (referenced by user_id)
- Ticket and payment models in the Bytemark system

### 📌 Important Notes
- Uses MongoDB with 'cache' connection for fast logging operations
- Flexible schema allows storing various ticket operation details
- Timestamp stored as Unix timestamp (Number type)
- UUID field helps track specific operations across systems
- Status field tracks operation success/failure
- Important for debugging payment issues and audit trails
- Cache database suggests frequent read/write operations for monitoring

### 🏷️ Tags
**Keywords:** bytemark, tickets, logging, audit, transactions, payments
**Category:** #model #database #mongodb #logging #bytemark #tickets #payments