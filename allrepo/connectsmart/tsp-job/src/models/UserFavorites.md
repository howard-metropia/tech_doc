# UserFavorites Model

## Overview
User favorites and bookmarks management model for the TSP Job system. Handles user-saved locations, routes, preferences, and frequently accessed items.

## Model Definition
```javascript
const knex = require('@maas/core/mysql')('portal');
class UserFavorites extends Model {
  static get tableName() {
    return 'user_favorites';
  }
}
module.exports = UserFavorites.bindKnex(knex);
```

## Database Configuration
- **Database**: Portal MySQL instance
- **Table**: `user_favorites`
- **ORM**: Objection.js with Knex query builder
- **Connection**: Managed by @maas/core MySQL connection pool

## Purpose
- User favorite locations storage
- Bookmarked routes and trips
- Personalized quick access items
- User-curated content management

## Key Features
- Multi-type favorite support
- Personalized collections
- Quick access functionality
- Category-based organization

## Favorite Types
- **Locations**: Home, work, frequently visited places
- **Routes**: Preferred travel paths
- **Transit Stops**: Regular bus/train stations
- **Parking Spots**: Preferred parking locations
- **Carpool Routes**: Regular sharing paths
- **Business Places**: Restaurants, shops, services

## Integration Points
- **AuthUsers**: Favorite ownership
- **UserConfig**: Preference-driven favorites
- **BusRouteFavorite**: Transit-specific favorites
- **CmLocation**: Location-based favorites

## Usage Context
Used for personalizing user experience, providing quick access to frequently used items, and storing user-curated content for enhanced usability.

## Database Schema
Typical structure includes:
- User ID reference
- Favorite item type
- Item reference/content
- Category or tag
- Creation and update timestamps
- Usage frequency tracking

## Performance Optimization
- Indexed user lookups
- Cached frequently accessed favorites
- Efficient category filtering
- Optimized for mobile quick access

## Business Logic
- Duplicate prevention
- Category management
- Usage analytics
- Automatic suggestions based on patterns

## Related Models
- AuthUsers: Ownership relationship
- UserConfig: Preference integration
- BusRouteFavorite: Transit favorites
- UserActions: Usage tracking

## API Integration
- Favorite management endpoints
- Quick access APIs
- Suggestion services
- Category organization

## Development Notes
- Supports flexible favorite types
- Scalable for large favorite collections
- Mobile-optimized for quick access
- Analytics-friendly for recommendations