# UberBenefitTransaction Model

## Overview
Uber benefit and subsidy transaction model for the TSP Job system. Manages corporate benefits, subsidies, and employer-sponsored transportation credits.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class UberBenefitTransaction extends Model {
  static get tableName() {
    return 'uber_benefit_transaction';
  }
}
module.exports = UberBenefitTransaction.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `uber_benefit_transaction`
- **ORM**: Objection.js with Knex query builder

## Purpose
- Corporate benefit management
- Employer transportation subsidies
- Employee mobility credits
- Business expense tracking

## Benefit Types
- **Corporate Credits**: Company-sponsored rides
- **Commuter Benefits**: Work-related transportation
- **Healthcare Transport**: Medical appointment rides
- **Business Travel**: Work-related mobility
- **Emergency Transport**: Company emergency rides

## Key Features
- Benefit allocation tracking
- Usage monitoring
- Expense categorization
- Compliance reporting

## Integration Points
- **RidehailTrips**: Benefit-funded trips
- **UserWallet**: Credit management
- **Enterprises**: Corporate accounts
- **AuthUsers**: Employee identification

## Business Logic
- Benefit eligibility verification
- Usage limit enforcement
- Expense categorization
- Approval workflows

## Compliance Features
- Expense reporting
- Tax compliance
- Audit trail maintenance
- Policy enforcement

## Related Models
- RidehailTrips: Subsidized rides
- UserWallet: Credit tracking
- Enterprises: Corporate benefits
- CoinTransaction: Credit systems

## Development Notes
- Corporate compliance critical
- Complex benefit rules
- Multi-tenant support
- Audit requirements essential