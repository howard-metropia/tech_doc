# UserConfig Model

## Overview
User preference and configuration management model for the TSP Job system. Stores personalized settings, preferences, and user-specific configuration data.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class UserConfig extends Model {
  static get tableName() {
    return 'user_config';
  }
}
module.exports = UserConfig.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `user_config`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool

## Purpose
- User preference storage
- Application configuration per user
- Personalization settings
- Feature flag management per user

## Key Features
- Flexible configuration storage
- User-specific customization
- Feature enablement control
- Preference persistence

## Configuration Types
- **UI Preferences**: Theme, language, layout
- **Notification Settings**: Push, email, SMS preferences
- **Privacy Settings**: Data sharing, tracking options
- **Feature Flags**: Beta feature access
- **Travel Preferences**: Default modes, routes
- **Account Settings**: Profile visibility, sharing

## Integration Points
- **AuthUsers**: User ownership
- **Notifications**: Preference-based messaging
- **UserFavorites**: Personalized content
- **AppData**: Application-specific settings

## Usage Context
Used for personalizing user experience, managing feature access, storing user preferences, and configuring application behavior per user.

## Database Schema
Typical fields include:
- User ID reference
- Configuration key-value pairs
- Setting categories
- Timestamps for updates
- Version tracking

## Performance Considerations
- Cached frequently accessed settings
- Efficient key-value lookups
- Minimal database queries for settings
- Optimized for read-heavy operations

## Data Management
- JSON configuration storage
- Hierarchical setting organization
- Default value fallbacks
- Setting validation and constraints

## Related Models
- AuthUsers: Configuration ownership
- UserFavorites: Preference-based favorites
- Notifications: Setting-driven messaging
- UserActions: Behavior-based configuration

## API Integration
- User preference endpoints
- Configuration management APIs
- Setting synchronization services
- Personalization features

## Development Notes
- Supports flexible schema-less configuration
- Backward compatibility for setting changes
- Efficient caching strategies
- Validation for critical settings