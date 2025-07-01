# Preference Controller

## Overview
The Preference Controller manages user travel preferences in the MaaS platform, storing and retrieving personalized settings for transportation modes, single-trip preferences, and parking options. It provides a flexible preference system with default fallback values.

## Technical Stack
- **Framework**: Web2py with RESTful API design
- **Authentication**: JWT-based authentication
- **Database**: MySQL for preference storage
- **Configuration**: JSON-based default preferences
- **Response Format**: JSON

## Architecture

### Core Components
- **Preference Management**: CRUD operations for user preferences
- **Default System**: Fallback to system defaults when user preferences unavailable
- **Type-based Organization**: Separate preference categories (transport, single, parking)
- **Delta Updates**: Partial preference updates without full replacement

### Database Schema
```sql
preference (
  id: int,
  user_id: int,
  transport: json,
  single: json, 
  parking: json,
  created_on: datetime,
  modified_on: datetime
)
```

### Preference Categories
1. **Transport**: Multi-modal transportation preferences
2. **Single**: Single-trip specific preferences
3. **Parking**: Parking-related preferences

## API Endpoints

### PUT /api/v1/preference/setting
Update user preferences with delta changes.

**Request Body:**
```json
{
  "type": "transport",
  "change_data": {
    "preferred_mode": "transit",
    "walking_distance": 800,
    "cost_weight": 0.7
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "preferred_mode": "transit",
    "walking_distance": 800,
    "cost_weight": 0.7
  }
}
```

### GET /api/v1/preference/setting
Retrieve user preferences with default fallback.

**Query Parameters:**
```
type: transport|single|parking (required)
```

**Response:**
```json
{
  "success": true,
  "data": {
    "normal": {
      "preferred_modes": ["driving", "transit"],
      "max_walk_distance": 500,
      "cost_sensitivity": 0.5
    },
    "family": {
      "preferred_modes": ["driving"],
      "comfort_priority": true
    },
    "travel": {
      "preferred_modes": ["transit", "rideshare"],
      "flexibility": true
    },
    "work": {
      "preferred_modes": ["transit", "bike"],
      "time_priority": true
    }
  }
}
```

### GET /api/v1/preference/default
Retrieve system default preferences.

**Query Parameters:**
```
type: transport|single|parking (required)
get_default: normal|family|travel|work (optional)
```

**Response:**
```json
{
  "success": true,
  "data": {
    "preferred_modes": ["driving", "transit"],
    "max_walk_distance": 500,
    "cost_sensitivity": 0.5,
    "time_sensitivity": 0.8
  }
}
```

## Business Logic

### Preference Types

#### Transport Preferences
- **normal**: Default daily transportation preferences
- **family**: Family-oriented travel preferences
- **travel**: Tourist/leisure travel preferences  
- **work**: Work commute preferences

#### Single Trip Preferences
- **vehicle**: Private vehicle preferences
- **mass_transit**: Public transit preferences

#### Parking Preferences
- **parking**: Parking location and cost preferences

### Delta Update Logic
```python
def update_preferences(user_id, preference_type, change_data):
    """
    Merge new preferences with existing ones
    Only updates specified fields, preserves others
    """
    # Retrieve existing preferences
    existing = get_user_preferences(user_id, preference_type)
    
    # Merge with change_data
    for key, value in change_data.items():
        existing[key] = value
    
    # Save updated preferences
    save_preferences(user_id, preference_type, existing)
```

### Default Fallback System
```python
def get_preferences(user_id, preference_type):
    """
    1. Try to load user-specific preferences
    2. Fall back to system defaults if not found
    3. Special handling for transport 'normal' type (always default)
    """
    user_prefs = load_user_preferences(user_id, preference_type)
    if not user_prefs:
        return load_default_preferences(preference_type)
    
    # Transport normal type always uses default
    if preference_type == 'transport':
        defaults = load_default_preferences(preference_type)
        user_prefs['normal'] = defaults.get('normal')
    
    return user_prefs
```

### Default Configuration Loading
```python
def _load_default():
    """
    Load default preferences from JSON configuration file
    Located at: private/default_preference.json
    """
    path = os.path.join(request.folder, 'private', 'default_preference.json')
    with open(path) as f:
        return json.load(f)
```

## Configuration Structure

### Default Preference File
```json
{
  "transport": {
    "normal": {
      "preferred_modes": ["driving", "transit"],
      "max_walk_distance": 500,
      "cost_sensitivity": 0.5,
      "time_sensitivity": 0.8
    },
    "family": {
      "preferred_modes": ["driving"],
      "comfort_priority": true,
      "safety_priority": true
    },
    "travel": {
      "preferred_modes": ["transit", "rideshare"],
      "flexibility": true,
      "exploration_factor": 0.7
    },
    "work": {
      "preferred_modes": ["transit", "bike"],
      "time_priority": true,
      "reliability_factor": 0.9
    }
  },
  "single": {
    "vehicle": {
      "fuel_type": "gasoline",
      "parking_preference": "free"
    },
    "mass_transit": {
      "comfort_level": "standard",
      "accessibility_required": false
    }
  },
  "parking": {
    "parking": {
      "max_walk_distance": 300,
      "price_sensitivity": 0.6,
      "covered_preferred": true
    }
  }
}
```

## Error Handling

### Common Errors
- `ERROR_BAD_REQUEST_BODY` (400): Invalid request body format
- `ERROR_BAD_REQUEST_PARAMS` (400): Invalid query parameters

### Validation Rules
- **Type Validation**: Must be 'transport', 'single', or 'parking'
- **Data Format**: change_data must be valid JSON object
- **Sub-type Validation**: get_default must match valid sub-types

### Input Sanitization
- JSON object validation for change_data
- String validation for preference types
- Parameter existence checking

## Performance Considerations

### Caching Strategy
- Default preferences cached in memory
- User preferences cached per session
- JSON file loaded once at startup
- Database queries optimized with indexes

### Database Optimization
- Single row per user for all preferences
- JSON columns for flexible schema
- Efficient upsert operations
- Minimal database roundtrips

## Integration Points

### User Authentication
```python
@auth.allows_jwt()
@jwt_helper.check_token()
def setting():
    user_id = auth.user.id
    # Access user-specific preferences
```

### Timestamp Management
```python
data = dict(modified_on=request.utcnow)
# Automatic timestamp updates on changes
```

### Response Formatting
```python
import json_response

return json_response.success(preference_data)
```

## Security Features
- JWT authentication required for all operations
- User isolation - cannot access other users' preferences
- Input validation and sanitization
- Type-safe preference updates

## Use Cases

### Personalized Routing
- Transport mode preferences influence route planning
- Walking distance limits affect intermodal options
- Cost sensitivity impacts fare-based decisions

### Trip Planning
- Single trip preferences customize one-time journeys
- Family preferences prioritize safety and comfort
- Work preferences emphasize reliability and time

### Parking Integration
- Parking preferences guide space selection
- Price sensitivity affects parking recommendations
- Accessibility requirements considered

## Dependencies
- `json_response`: API response formatting
- `auth`: User authentication and authorization
- `os`: File system access for default configuration
- `json`: JSON parsing and serialization