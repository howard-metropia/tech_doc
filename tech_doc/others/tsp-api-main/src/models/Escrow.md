# Escrow Model Documentation

## 📋 Model Overview
- **Purpose:** Manages escrow transactions for secure payment processing
- **Table/Collection:** escrow
- **Database Type:** MySQL (portal database)
- **Relationships:** Links to payment transactions and user accounts for secure fund handling

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| id | INT | Yes | Primary key, auto-increment |
| user_id | INT | Yes | Foreign key to auth_user |
| transaction_id | VARCHAR | Yes | Unique transaction identifier |
| amount | DECIMAL | Yes | Escrow amount in dollars |
| currency | VARCHAR | No | Currency code (default USD) |
| escrow_type | VARCHAR | No | Type of escrow (payment, refund, deposit) |
| status | VARCHAR | No | Escrow status (pending, held, released, cancelled) |
| reference_id | VARCHAR | No | Reference to related transaction/booking |
| hold_until | TIMESTAMP | No | Automatic release timestamp |
| released_at | TIMESTAMP | No | Actual release timestamp |
| created_at | TIMESTAMP | Yes | Escrow creation timestamp |
| updated_at | TIMESTAMP | Yes | Last update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** user_id, transaction_id, status, reference_id, hold_until
- **Unique Constraints:** transaction_id
- **Default Values:** currency = 'USD', status = 'pending', created_at = CURRENT_TIMESTAMP

## 📝 Usage Examples
```javascript
// Create escrow for payment
await Escrow.query().insert({
  user_id: userId,
  transaction_id: 'escrow_12345',
  amount: 25.50,
  escrow_type: 'payment',
  reference_id: 'trip_456',
  hold_until: futureDate
});

// Get pending escrows for user
const pendingEscrows = await Escrow.query()
  .where('user_id', userId)
  .where('status', 'pending');

// Release escrow funds
await Escrow.query()
  .where('id', escrowId)
  .update({ 
    status: 'released', 
    released_at: new Date() 
  });
```

## 🔗 Related Models
- `AuthUsers` - Many-to-one relationship via user_id
- `EscrowDetail` - One-to-many relationship for detailed transactions
- Payment gateway models for fund processing
- Trip/booking models via reference_id

## 📌 Important Notes
- Provides secure fund holding for disputed or pending transactions
- hold_until enables automatic fund release after specified time
- reference_id links escrow to specific services (trips, bookings, etc.)
- Essential for payment security and dispute resolution
- Supports multiple escrow types for different business scenarios

## 🏷️ Tags
**Keywords:** escrow, payments, security, transactions, funds
**Category:** #model #database #payments #escrow #mysql

---
Note: This model provides secure escrow functionality for payment processing and dispute management.