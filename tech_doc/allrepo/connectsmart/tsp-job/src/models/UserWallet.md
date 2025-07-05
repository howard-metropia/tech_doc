# UserWallet Model

## Overview
Financial account management model for user wallet operations in the TSP Job system. Handles user financial data, balances, and transaction tracking.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class UserWallet extends Model {
  static get tableName() {
    return 'user_wallet';
  }
}
module.exports = UserWallet.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `user_wallet`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool

## Purpose
- User financial account management
- Wallet balance tracking
- Payment method storage
- Transaction history foundation

## Key Features
- Financial data security
- Real-time balance management
- Transaction audit trails
- Payment integration support

## Integration Points
- **CoinTransaction**: Coin-based transactions
- **PointsTransaction**: Loyalty points management
- **TokenTransaction**: Token-based payments
- **UberBenefitTransaction**: Rideshare benefit tracking
- **TicketTransaction**: Transit ticket purchases

## Usage Context
Used in payment processing, financial reporting, wallet balance operations, and transaction management across the TSP system.

## Database Schema
The model maps to the `user_wallet` table containing:
- User financial account information
- Current wallet balances
- Payment method references
- Account status and limits
- Financial transaction history links

## Security Considerations
- Encrypted financial data storage
- PCI compliance requirements
- Secure transaction processing
- Audit logging for all operations
- Access control restrictions

## Transaction Management
- ACID compliant operations
- Concurrent transaction handling
- Balance reconciliation
- Error recovery mechanisms
- Double-entry accounting patterns

## Performance Optimization
- Indexed balance lookups
- Efficient transaction queries
- Connection pooling
- Cached balance calculations
- Optimized for high-frequency operations

## Related Models
- AuthUsers: Wallet ownership
- CoinTransaction: Virtual currency
- PointsTransaction: Loyalty system
- TokenTransaction: Payment tokens
- UberBenefitTransaction: Benefit tracking

## API Integration
Primary endpoints:
- Wallet balance inquiries
- Payment processing
- Transaction history
- Account management
- Financial reporting

## Business Logic
- Balance validation
- Transaction limits
- Fee calculations
- Currency conversions
- Promotional credit handling

## Development Notes
- Critical financial data requires extra security
- All operations should be logged and auditable
- Supports multiple currency types
- Compatible with external payment processors
- Follows financial industry best practices