# Truck Joi Schema Documentation

### 📋 Schema Overview
- **Purpose:** Validates truck routing and height restriction data
- **Validation Library:** Joi
- **Related Controller:** truck.js

### 🔧 Schema Structure
```javascript
// Query string parameters
validateQueryStringParams: {
  last_modified: number (required, integer, min 0)
}

// Truck map MongoDB document
validateTruckMapMongoDBData: {
  _id: object or string (required),
  truck_map: array of restriction objects (required),
  created_at: date (required),
  __v: number (required)
}

// Truck restriction object
truckRestriction: {
  max_height: number (required),
  min_height: number (required),
  present_word: string (required),
  segment_id: number (required),
  link_id: number (required)
}
```

### 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| last_modified | number | Yes | integer, min 0 | Timestamp for data freshness |
| _id | object/string | Yes | - | MongoDB document ID |
| truck_map | array | Yes | array of restrictions | Height restriction data |
| max_height | number | Yes | - | Maximum allowed height |
| min_height | number | Yes | - | Minimum height restriction |
| present_word | string | Yes | - | Restriction description |
| segment_id | number | Yes | - | Road segment identifier |
| link_id | number | Yes | - | Road link identifier |
| created_at | date | Yes | - | Document creation timestamp |
| __v | number | Yes | - | MongoDB version key |

### 💡 Usage Example
```javascript
// Query for truck data updates
{
  "last_modified": 1640995200
}

// Truck map MongoDB document
{
  "_id": "507f1f77bcf86cd799439011",
  "truck_map": [
    {
      "max_height": 4.2,
      "min_height": 0.0,
      "present_word": "Low Bridge",
      "segment_id": 12345,
      "link_id": 67890
    },
    {
      "max_height": 3.8,
      "min_height": 0.0,
      "present_word": "Height Restriction",
      "segment_id": 12346,
      "link_id": 67891
    }
  ],
  "created_at": "2024-01-15T08:00:00Z",
  "__v": 0
}

// Invalid request - negative last_modified
{
  "last_modified": -1 // Error: must be >= 0
}
```

### ⚠️ Important Validations
- Last modified timestamp must be non-negative integer
- MongoDB document ID can be object or string format
- All truck restriction fields are required
- Height values are numbers (likely in meters)
- Segment and link IDs reference road network data
- Present word describes restriction type/reason
- Created date must be valid date format

### 🏷️ Tags
**Keywords:** truck, routing, height-restrictions, mongodb, transportation
**Category:** #schema #validation #joi #truck