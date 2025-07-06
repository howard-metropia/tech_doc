# PointsTransaction Model Documentation

## Overview
PointsTransaction is a Knex.js-based model that manages point-based reward transactions in the MaaS platform. This model handles the creation, tracking, and management of user point transactions for various transportation activities and incentive programs.

## Class Definition
```javascript
const config = require('config');
const knex = require('@maas/core/mysql')('portal');

class PointsTransaction extends Model {
  static get tableName() {
    return config.portal.pointsTransactionSchema;
  }
}
module.exports = PointsTransaction.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL (`portal`)
- **Table**: Dynamic based on `config.portal.pointsTransactionSchema`
- **ORM**: Knex.js with Model base class
- **Connection**: Managed through @maas/core/mysql
- **Configuration**: Schema name from application configuration

## Core Functionality

### Transaction Management
- Records all point-based transactions and rewards
- Tracks point earnings, spending, and balance changes
- Maintains transaction history for auditing purposes
- Supports various transaction types and categories

### Incentive Program Integration
- Links transactions to specific incentive programs
- Manages reward distribution for transportation activities
- Tracks program participation and effectiveness
- Supports gamification and engagement features

## Usage Patterns

### Point Transaction Recording
```javascript
const PointsTransaction = require('./PointsTransaction');

// Record point earning transaction
const pointTransaction = await PointsTransaction.query().insert({
  user_id: userId,
  transaction_type: 'earn',
  points_amount: 50,
  activity_type: 'public_transit_trip',
  trip_id: tripId,
  program_id: programId,
  transaction_timestamp: new Date(),
  description: 'Bus trip reward',
  expiration_date: expirationDate
});

// Calculate user point balance
const userBalance = await PointsTransaction.query()
  .where('user_id', userId)
  .sum('points_amount as total_points');
```

### Reward Distribution
- Automated point distribution for qualified activities
- Manual point adjustments for special programs
- Bulk point distribution for campaigns
- Point expiration and lifecycle management

## Transaction Types and Categories

### Earning Transactions
- **Trip Rewards**: Points for using sustainable transportation
- **Achievement Bonuses**: Milestone and goal completion rewards
- **Referral Rewards**: User referral program points
- **Survey Participation**: Research participation incentives
- **Challenge Completion**: Gamification challenge rewards

### Spending Transactions
- **Transit Fare**: Points used for transportation costs
- **Merchandise**: Reward catalog purchases
- **Discount Redemption**: Partner offer redemptions
- **Charity Donation**: Points donated to causes
- **Gift Transfer**: Points transferred to other users

### Administrative Transactions
- **Manual Adjustment**: Administrative point corrections
- **Bonus Award**: Special recognition rewards
- **Penalty Deduction**: Policy violation penalties
- **Expiration**: Point expiration processing
- **Migration**: System upgrade point transfers

## Integration Points

### Incentive Programs
- **Campaign Management**: Marketing campaign integration
- **Challenge System**: Gamification platform connection
- **Partner Programs**: Third-party reward integration
- **Analytics**: Program effectiveness measurement

### Transportation Services
- **Trip Validation**: Activity verification for rewards
- **Mode Detection**: Transportation mode identification
- **Route Analysis**: Sustainable route incentives
- **Multi-modal Integration**: Comprehensive trip rewards

### User Management
- **Account Integration**: User profile correlation
- **Balance Management**: Real-time balance updates
- **Notification System**: Transaction alerts
- **History Tracking**: User transaction history

## Business Logic Features

### Point Calculation Rules
- Dynamic point values based on activity type
- Multiplier effects for special programs
- Tier-based reward structures
- Seasonal and promotional adjustments

### Validation and Verification
- Transaction authenticity verification
- Duplicate transaction prevention
- Fraud detection and prevention
- Activity qualification validation

### Expiration Management
- Point expiration date tracking
- Automated expiration processing
- Expiration notification system
- Extension and renewal capabilities

## Performance Considerations
- Efficient balance calculation queries
- Transaction history pagination
- Bulk transaction processing
- Real-time balance updates

## Data Integrity
- Transaction atomicity guarantees
- Balance consistency validation
- Audit trail maintenance
- Reconciliation processes

## Security Features
- Transaction authorization controls
- Fraud detection algorithms
- Secure point transfer mechanisms
- Access control and permissions

## Analytics and Reporting
- User engagement metrics
- Program effectiveness analysis
- Transaction pattern analysis
- Revenue impact measurement

## Related Components
- **User Accounts**: Account balance integration
- **Incentive Jobs**: Automated reward processing
- **Campaign Management**: Marketing integration
- **Analytics Dashboard**: Performance monitoring

## Compliance and Auditing
- Financial transaction compliance
- Audit trail requirements
- Regulatory reporting support
- Data retention policies

## Future Enhancements
- Blockchain-based point systems
- Advanced fraud detection
- Real-time analytics
- Cross-platform point integration
- Enhanced gamification features