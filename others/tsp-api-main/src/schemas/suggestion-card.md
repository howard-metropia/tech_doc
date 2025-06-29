# Suggestion Card Schema Documentation

### 📋 Schema Overview
- **Purpose:** Validates suggestion card management operations (get/delete)
- **Validation Library:** Joi
- **Related Controller:** suggestion-card.js

### 🔧 Schema Structure
```javascript
// Get suggestion card
get: {
  id: number (required, min 1)
}

// Delete suggestion card
delete: {
  id: number (required, min 1)
}
```

### 📝 Field Validations
| Field | Type | Required | Validation Rules | Description |
|-------|------|----------|------------------|-------------|
| id | number | Yes | min 1 | Suggestion card identifier |

### 💡 Usage Example
```javascript
// Get suggestion card
{
  "id": 123
}

// Delete suggestion card
{
  "id": 456
}

// Invalid request - ID too small
{
  "id": 0 // Error: must be >= 1
}

// Invalid request - wrong data type
{
  "id": "123" // Error: must be number
}
```

### ⚠️ Important Validations
- ID must be positive integer (minimum value 1)
- Both get and delete operations use identical validation
- All requests require header verification fields
- Simple schema focused on card identification
- No additional parameters for basic CRUD operations

### 🏷️ Tags
**Keywords:** suggestion-card, recommendations, cards, crud
**Category:** #schema #validation #joi #suggestion-card