# BusRouteFavorite Model

## Overview
MySQL model for storing user's favorite bus routes and transit preferences.

## File Location
`/src/models/BusRouteFavorite.js`

## Database Configuration
- **Connection**: MySQL portal database
- **Table**: `bus_route_favorite`
- **Framework**: Objection.js ORM

## Model Structure
```javascript
class BusRouteFavorite extends Model {
  static get tableName() {
    return 'bus_route_favorite';
  }
}
```

## Table Schema
The `bus_route_favorite` table typically contains:

### Primary Fields
- **id**: Primary key identifier
- **user_id**: User who favorited the route
- **route_id**: Bus route identifier
- **route_name**: Human-readable route name
- **agency_id**: Transit agency identifier

### Route Details
- **origin_stop_id**: Preferred origin stop
- **destination_stop_id**: Preferred destination stop
- **direction_id**: Route direction (0 or 1)
- **trip_headsign**: Route destination headsign

### Metadata
- **created_at**: When favorite was added
- **updated_at**: Last modification timestamp
- **is_active**: Whether favorite is active

## Usage Context
- **Transit Preferences**: Store user's preferred bus routes
- **Quick Access**: Enable fast route selection
- **Personalization**: Customize transit experience
- **Journey Planning**: Optimize route recommendations

## Common Queries
- Retrieve user's favorite routes
- Check if route is favorited
- Get popular routes by usage
- Filter routes by agency or area

## Related Components
- Transit route planning system
- User preference management
- Bus route information services
- Transit agency integrations

## Performance Considerations
- Indexed on user_id for fast user queries
- Indexed on route_id for route popularity analysis
- Composite index on user_id + route_id for uniqueness