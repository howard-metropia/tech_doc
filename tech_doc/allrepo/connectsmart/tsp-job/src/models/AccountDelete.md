# AccountDelete Model

## Overview
Account deletion and data removal model for the TSP Job system. Manages user account deletion requests, data cleanup, and privacy compliance.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class AccountDelete extends Model {
  static get tableName() {
    return 'account_delete';
  }
}
module.exports = AccountDelete.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `account_delete`
- **ORM**: Objection.js with Knex query builder

## Purpose
- Account deletion request tracking
- Data removal coordination
- Privacy compliance management
- GDPR right to deletion

## Deletion Types
- **User Initiated**: Self-service deletion
- **Administrative**: Admin-triggered removal
- **Compliance**: Legal requirement deletions
- **Automated**: Policy-based cleanup

## Key Features
- Multi-stage deletion process
- Data retention compliance
- Audit trail maintenance
- Recovery period support

## Deletion Process
1. **Request**: Deletion initiation
2. **Validation**: Identity verification
3. **Grace Period**: Recovery window
4. **Data Removal**: Systematic cleanup
5. **Completion**: Final confirmation

## Data Categories
- **Personal Data**: User information
- **Transaction Data**: Financial records
- **Location Data**: GPS and tracking
- **Communication**: Messages and alerts

## Compliance Features
- GDPR compliance
- Data retention policies
- Privacy regulation adherence
- Audit documentation

## Integration Points
- **AuthUsers**: Account identification
- **UserWallet**: Financial data cleanup
- **Trips**: Trip data removal
- **Notifications**: Communication cleanup

## Related Models
- AuthUsers: Account management
- UserWallet: Financial cleanup
- Trips: Travel data removal
- UserActions: Activity cleanup

## Development Notes
- Privacy compliance critical
- Multi-system coordination
- Audit trail essential
- Recovery mechanism important