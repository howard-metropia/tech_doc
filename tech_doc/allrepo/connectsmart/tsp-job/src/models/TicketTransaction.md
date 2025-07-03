# TicketTransaction Model

## Overview
Transit ticket transaction model for the TSP Job system. Handles public transportation ticket purchases, validations, and fare collection.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class TicketTransaction extends Model {
  static get tableName() {
    return 'ticket_transaction';
  }
}
module.exports = TicketTransaction.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `ticket_transaction`
- **ORM**: Objection.js with Knex query builder

## Purpose
- Transit ticket purchase tracking
- Fare collection management
- Ticket validation recording
- Revenue accounting

## Ticket Types
- **Single Ride**: One-time trip tickets
- **Day Pass**: 24-hour unlimited access
- **Weekly Pass**: 7-day travel passes
- **Monthly Pass**: 30-day subscriptions
- **Zone Tickets**: Geographic fare zones
- **Transfer Tickets**: Multi-modal connections

## Key Features
- Multi-fare type support
- Real-time validation
- Digital ticket management
- Revenue tracking

## Transaction Lifecycle
1. **Purchase**: Ticket acquisition
2. **Validation**: Entry verification
3. **Usage**: Trip consumption
4. **Expiration**: Time-based expiry
5. **Refund**: Return processing

## Integration Points
- **UserWallet**: Payment processing
- **Trips**: Ticket usage tracking
- **TransitAlert**: Service disruptions
- **BytemarkTickets**: Transit system integration

## Fare Rules
- Zone-based pricing
- Time-based validity
- Transfer allowances
- Discount applications
- Peak/off-peak rates

## Related Models
- UserWallet: Payment integration
- Trips: Usage tracking
- BytemarkTickets: System tickets
- CoinTransaction: Alternative payments

## Development Notes
- Real-time validation critical
- Multi-transit system support
- Revenue accounting accurate
- Mobile ticket optimization