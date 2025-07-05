# TeleworkLogs Model

## Overview
Telework tracking and logging model for the TSP Job system. Records remote work activities, commute patterns, and telework analytics for enterprise clients.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class TeleworkLogs extends Model {
  static get tableName() {
    return 'telework_logs';
  }
}
module.exports = TeleworkLogs.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `telework_logs`
- **ORM**: Objection.js with Knex query builder

## Purpose
- Remote work activity tracking
- Commute pattern analysis
- Telework policy compliance
- Environmental impact measurement

## Log Categories
- **Work Location**: Office vs remote
- **Commute Avoidance**: Saved trips
- **Transportation Impact**: Reduced travel
- **Schedule Tracking**: Work-from-home days
- **Policy Compliance**: Company requirements

## Key Features
- Daily activity logging
- Commute impact calculation
- Environmental metrics
- Compliance reporting

## Telework Types
- **Full Remote**: Complete home-based work
- **Hybrid**: Mixed office/remote schedule
- **Flexible**: As-needed remote work
- **Emergency**: Pandemic/weather-related

## Integration Points
- **Enterprises**: Corporate telework programs
- **AuthUsers**: Employee identification
- **Trips**: Commute pattern changes
- **UserActions**: Work-related activities

## Analytics Applications
- Carbon footprint reduction
- Traffic congestion impact
- Employee productivity correlation
- Cost savings analysis

## Compliance Features
- Policy adherence tracking
- Reporting for employers
- Tax implication support
- Audit trail maintenance

## Environmental Impact
- Reduced vehicle emissions
- Traffic congestion reduction
- Energy consumption savings
- Sustainability metrics

## Related Models
- Enterprises: Corporate programs
- AuthUsers: Employee tracking
- Trips: Commute analysis
- UserActions: Work activities

## Development Notes
- Enterprise-focused feature
- Privacy-conscious design
- Environmental impact focus
- Compliance reporting critical