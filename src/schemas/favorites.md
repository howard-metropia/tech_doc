# Favorites Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates user favorite locations for CRUD operations
- **Validation Library:** Joi
- **Related Controller:** Favorites controller for user location management

## 🔧 Schema Structure
```javascript
// Create favorite schema
{
  ...verifyHeaderFieldsByJoi,
  name: Joi.string().required(),
  address: Joi.string().required(),
  latitude: Joi.number().required(),
  longitude: Joi.number().required(),
  category: Joi.number().integer().valid(1, 2, 3, 4).required(),
  access_latitude: Joi.number(),
  access_longitude: Joi.number(),
  icon_type: Joi.number().integer().default(1),
  place_id: Joi.string(),
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| name | string | Yes | Any string | Display name for favorite location |
| address | string | Yes | Any string | Human-readable address |
| latitude | number | Yes | Valid number | Geographic latitude coordinate |
| longitude | number | Yes | Valid number | Geographic longitude coordinate |
| category | number | Yes | Integer: 1,2,3,4 | Location category type |
| access_latitude | number | No | Valid number | Access point latitude |
| access_longitude | number | No | Valid number | Access point longitude |
| icon_type | number | No | Integer, default: 1 | Display icon type |
| place_id | string | No | Any string | Google Places ID reference |
| id | number | Yes (update/delete) | Min: 1 | Favorite location ID |

## 💡 Usage Example
```javascript
// Create favorite request
{
  "name": "Home",
  "address": "123 Main St, City, State",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "category": 1,
  "icon_type": 2,
  "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4"
}

// Update favorite request
{
  "id": 5,
  "name": "Updated Home",
  "address": "456 Oak Ave, City, State",
  "latitude": 37.7849,
  "longitude": -122.4094,
  "category": 2
}

// Request that fails validation
{
  "name": "Office",
  "address": "100 Business Blvd",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "category": 5 // Error: category must be 1, 2, 3, or 4
}
```

## ⚠️ Important Validations
- Category must be exactly 1, 2, 3, or 4 (predefined location types)
- Coordinates are required for all operations except get
- Icon type defaults to 1 if not specified
- Update and delete operations require valid ID (minimum 1)
- Access coordinates are optional for more precise location access

## 🏷️ Tags
**Keywords:** favorites, user-locations, coordinates, location-categories
**Category:** #schema #validation #joi #favorites