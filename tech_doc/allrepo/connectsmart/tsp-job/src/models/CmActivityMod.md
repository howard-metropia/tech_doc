# CmActivityMod Model

## Overview
Campaign management activity modification model for the TSP Job system. Handles activity modifications, campaign adjustments, and dynamic activity management.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class CmActivityMod extends Model {
  static get tableName() {
    return 'cm_activity_mod';
  }
}
module.exports = CmActivityMod.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `cm_activity_mod`
- **ORM**: Objection.js with Knex query builder

## Purpose
- Activity modification tracking
- Campaign adjustment management
- Dynamic activity updates
- Change history maintenance

## Modification Types
- **Schedule Changes**: Timing adjustments
- **Location Updates**: Venue modifications
- **Capacity Changes**: Availability adjustments
- **Feature Updates**: Service modifications
- **Status Changes**: Activity state updates

## Key Features
- Comprehensive change tracking
- Version control support
- Audit trail maintenance
- Rollback capabilities

## Change Categories
- **Operational**: Service-related modifications
- **Marketing**: Campaign-driven changes
- **Seasonal**: Time-based adjustments
- **Emergency**: Crisis-response modifications

## Integration Points
- **CmActivityLocation**: Location relationships
- **CmLocation**: Location data
- **ActivityArea**: Geographic boundaries
- **UserActions**: Activity impact tracking

## Audit Features
- Complete change history
- User attribution tracking
- Timestamp recording
- Reason documentation

## Business Logic
- Change validation rules
- Impact assessment
- Notification triggers
- Approval workflows

## Performance Features
- Efficient modification queries
- Fast change retrieval
- Optimized audit trails
- Scalable change tracking

## Related Models
- CmActivityLocation: Activity locations
- CmLocation: Location data
- ActivityArea: Geographic regions
- UserActions: User impact

## Development Notes
- Change management focus
- Audit trail critical
- Performance optimization important
- Workflow integration needed