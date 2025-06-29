# Preference Schema Documentation

## 📋 Schema Overview
- **Purpose:** Validates user transportation and parking preferences configuration
- **Validation Library:** Joi
- **Related Controller:** preference controller

## 🔧 Schema Structure
```javascript
{
  get: { type: 'transport'|'single'|'parking' },
  update: { 
    type: 'transport'|'single'|'parking',
    change_data: {
      // Transport preferences
      choose_setting: 'normal'|'family'|'travel'|'work',
      normal/family/travel/work: { transports, path, road_types },
      // Single preferences  
      vehicle: { road_types },
      mass_transit: { transports, path },
      // Parking preferences
      search_range, navigation_show, vehicle_height, price, operations
    }
  },
  getDefault: { type, get_default: setting_name }
}
```

## 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| type | string | Yes | 'transport'/'single'/'parking' | Preference category |
| choose_setting | string | No | 'normal'/'family'/'travel'/'work' | Active transport setting |
| transports | array | Yes | Valid transport modes | Allowed transportation types |
| path | string | Yes | 'all'/'walk_less'/'trans_less'/'best' | Route optimization preference |
| road_types | array | Yes | Valid road type enums | Allowed/avoided road types |
| search_range | number | No | Positive integer | Parking search radius |
| navigation_show | boolean | No | - | Show navigation in parking |
| vehicle_height | number | No | Positive integer | Vehicle height for parking |
| operations | array | No | Integers 1-9 | Parking operation preferences |

## 💡 Usage Example
```javascript
// Transport preference update
{
  "type": "transport",
  "change_data": {
    "choose_setting": "work",
    "work": {
      "transports": ["driving", "bus", "subway"],
      "path": "walk_less",
      "road_types": ["motorways", "toll_roads"]
    }
  }
}

// Parking preference update
{
  "type": "parking", 
  "change_data": {
    "search_range": 500,
    "navigation_show": true,
    "vehicle_height": 200,
    "operations": [1, 2, 5]
  }
}
```

## ⚠️ Important Validations
- Type parameter is required for all operations
- Transport arrays must contain valid predefined values
- Numeric values must be positive integers
- Road types restricted to specific infrastructure categories
- Operations array limited to values 1-9
- Setting names must match predefined categories

## 🏷️ Tags
**Keywords:** user preferences, transportation, parking, routing, road types
**Category:** #schema #validation #joi #preference