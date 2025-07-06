# CoinTransaction Model

## Overview
Virtual currency transaction management model for the TSP Job system. Handles coin-based rewards, payments, and virtual currency operations within the platform.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('dataset');
class CoinTransaction extends Model {
  static get tableName() {
    return 'coin_transaction';
  }
}
module.exports = CoinTransaction.bindKnex(knex);
```

## Database Configuration
- **Database**: Dataset MySQL instance
- **Table**: `coin_transaction`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool

## Purpose
- Virtual coin transaction tracking
- Reward system management
- Gamification currency handling
- Loyalty program operations

## Key Features
- Immutable transaction records
- Balance calculation support
- Reward distribution tracking
- Audit trail maintenance

## Transaction Types
- **Rewards**: Earned coins from activities
- **Purchases**: Coin spending transactions
- **Bonuses**: Promotional coin awards
- **Transfers**: Inter-user coin transfers
- **Adjustments**: Administrative corrections
- **Expiration**: Time-based coin removal

## Integration Points
- **UserWallet**: Coin balance management
- **PointsTransaction**: Multi-currency support
- **TokenTransaction**: Broader payment ecosystem
- **UserBadgeRelatedActivityLog**: Achievement rewards

## Usage Context
Used in gamification systems, loyalty programs, reward distribution, and virtual currency management across the transportation platform.

## Database Schema
Core transaction fields:
- User identification
- Transaction amount and type
- Transaction metadata
- Timestamp and audit information
- Reference to related activities

## Transaction Integrity
- ACID compliant operations
- Double-entry accounting principles
- Concurrent transaction handling
- Rollback capabilities for errors
- Balance reconciliation support

## Business Logic
- Reward calculation algorithms
- Spending validation rules
- Balance limit enforcement
- Expiration policy management
- Transfer authorization checks

## Performance Considerations
- Indexed transaction lookups
- Efficient balance calculations
- Batch processing for bulk operations
- Optimized for high-frequency transactions

## Related Models
- UserWallet: Balance integration
- PointsTransaction: Multi-currency system
- TokenTransaction: Payment tokens
- UserActions: Activity-based rewards

## API Integration
- Transaction processing endpoints
- Balance inquiry services
- Reward distribution APIs
- Transaction history reporting

## Security Features
- Transaction validation
- Fraud detection mechanisms
- Audit logging
- Access control restrictions

## Development Notes
- Immutable transaction design
- Supports complex reward algorithms
- Analytics-optimized for reporting
- Scalable for high transaction volumes