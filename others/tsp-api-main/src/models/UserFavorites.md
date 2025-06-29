# UserFavorites Model Documentation

## 📋 Model Overview
- **Purpose:** Stores user's favorite locations, routes, and preferences
- **Table/Collection:** user_favorites
- **Database Type:** MySQL
- **Relationships:** Belongs to users, references various location types

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| id | Integer | Yes | Primary key (auto-increment) |
| user_id | Integer | - | Owner of the favorite |
| favorite_type | String | - | Type (location, route, poi, etc.) |
| name | String | - | User-defined name for favorite |
| address | String | - | Address if location-based |
| latitude | Decimal | - | Latitude coordinate |
| longitude | Decimal | - | Longitude coordinate |
| category | String | - | Category (home, work, restaurant, etc.) |
| data | JSON | - | Additional favorite-specific data |
| icon | String | - | Icon identifier for display |
| order_index | Integer | - | Display order preference |
| is_active | Boolean | - | Whether favorite is active |
| last_used | DateTime | - | Last time favorite was used |
| use_count | Integer | - | Number of times used |
| created_at | DateTime | - | Record creation timestamp |
| updated_at | DateTime | - | Record update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** Likely on user_id, favorite_type, category, is_active
- **Unique Constraints:** Possibly user_id+name combination
- **Default Values:** Auto-generated timestamps, is_active default true

## 📝 Usage Examples
```javascript
// Add favorite location
const favorite = await UserFavorites.query().insert({
  user_id: userId,
  favorite_type: 'location',
  name: 'Home',
  address: '123 Main Street',
  latitude: 37.7749,
  longitude: -122.4194,
  category: 'home',
  icon: 'home'
});

// Get user's favorites by category
const homeFavorites = await UserFavorites.query()
  .where('user_id', userId)
  .where('category', 'home')
  .where('is_active', true)
  .orderBy('order_index');

// Update usage statistics
await UserFavorites.query()
  .where('id', favoriteId)
  .patch({
    last_used: new Date(),
    use_count: knex.raw('use_count + 1')
  });
```

## 🔗 Related Models
- **AuthUsers**: Favorites belong to specific users
- **POIs**: May reference point of interest data
- **UserTrips**: Favorites used as trip origins/destinations

## 📌 Important Notes
- Flexible favorite system supporting multiple types
- Geographic coordinates for location-based favorites
- Usage tracking for personalization
- Custom ordering and categorization
- Icon system for visual representation

## 🏷️ Tags
**Keywords:** favorites, locations, user-preferences, bookmarks
**Category:** #model #database #user-data #preferences