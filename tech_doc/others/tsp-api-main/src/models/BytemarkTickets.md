# Model Documentation: BytemarkTickets

## 📋 Model Overview
- **Purpose:** Caches Bytemark transit ticket and pass information for users
- **Table/Collection:** bytemark_tickets_cache
- **Database Type:** MongoDB
- **Relationships:** References users by user_id

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| user_id | Number | No | User identifier |
| timestamp | Number | No | Unix timestamp |
| passes | Array | No | Array of pass objects |
| passes.pass_uuid | String | No | Unique pass identifier |
| passes.timestamp | Number | No | Pass timestamp |
| passes.status | String | No | Pass status |
| passes.free_ticket_status | Number | No | Free ticket flag |
| passes.payload | Mixed | No | Pass payload data |
| passes.payload_hash | String | No | Hash of payload |
| passes4 | Array | No | Alternative pass array (v4) |
| passesLog | Array | No | Pass operation logs |
| passesLog.server_time | String | No | Server timestamp |
| passesLog.data | Object | No | Log data |
| passes4Log | Array | No | Pass v4 operation logs |

## 🔑 Key Information
- **Primary Key:** _id (auto-generated)
- **Indexes:** Default MongoDB _id index
- **Unique Constraints:** None specified
- **Default Values:** None specified

## 📝 Usage Examples
```javascript
// Get user's cached tickets
const tickets = await BytemarkTickets.findOne({ user_id: 12345 });

// Update user's passes
await BytemarkTickets.findOneAndUpdate(
  { user_id: 12345 },
  { 
    $push: { passes: newPass },
    timestamp: Date.now()
  },
  { upsert: true }
);

// Find active passes
const activeTickets = await BytemarkTickets.find({
  'passes.status': 'active'
});

// Clean old cache entries
await BytemarkTickets.deleteMany({
  timestamp: { $lt: thirtyDaysAgo }
});
```

## 🔗 Related Models
- AuthUsers - user_id references user records

## 📌 Important Notes
- Uses MongoDB 'cache' connection
- Schema is non-strict (allows additional fields)
- Supports two versions of passes (passes and passes4)
- Each pass version has corresponding log array
- Used for caching transit ticket data from Bytemark system

## 🏷️ Tags
**Keywords:** bytemark, transit, tickets, passes, cache, public-transport
**Category:** #model #database #transit #ticketing #mongodb

---