# AppData Model

## Overview
Application data and configuration model for the TSP Job system. Stores app-specific settings, configuration data, and system parameters.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class AppData extends Model {
  static get tableName() {
    return 'app_data';
  }
}
module.exports = AppData.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `app_data`
- **ORM**: Objection.js with Knex query builder

## Purpose
- Application configuration storage
- System parameter management
- Feature flag control
- Global settings coordination

## Data Categories
- **System Config**: Core application settings
- **Feature Flags**: Feature enablement control
- **UI Settings**: Interface configuration
- **API Parameters**: Service configuration
- **Business Rules**: Logic parameters

## Key Features
- Hierarchical configuration
- Environment-specific settings
- Real-time configuration updates
- Version control support

## Configuration Types
- **Global**: System-wide settings
- **Regional**: Location-specific config
- **Service**: Service-specific parameters
- **User**: User-level overrides

## Integration Points
- **UserConfig**: User-specific settings
- **Enterprises**: Enterprise configurations
- **ExperimentConfig**: A/B testing parameters

## Performance Features
- Cached configuration access
- Efficient parameter retrieval
- Real-time updates
- Minimal overhead

## Related Models
- UserConfig: User preferences
- ExperimentConfig: Testing parameters
- Enterprises: Organization settings

## Development Notes
- Critical system component
- Performance optimization essential
- Change management important
- Backward compatibility required