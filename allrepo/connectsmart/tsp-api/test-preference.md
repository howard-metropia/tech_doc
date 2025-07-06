# Test Documentation: Preference API

## Overview
This test suite validates the Preference functionality within the TSP system, which manages user transportation preferences, route optimization settings, and parking preferences. The system provides both default preferences and user-customizable settings for personalized transportation experiences.

## Test Configuration
- **File**: `test/test-preference.js`
- **Framework**: Mocha with Chai assertions and Supertest for HTTP testing
- **Models Used**: `AuthUsers`, `Preference`
- **Authentication**: Bearer token-based authentication (userid: 1003)
- **Static Data**: `DEFAULT_PREFERENCE` from defines

## API Endpoints Tested

### 1. GET /preference_default
**Purpose**: Retrieves default preference configurations

**Query Parameters**:
- `type`: Preference category ('transport', 'single', 'parking')
- `get_default`: Specific preference name (for 'single' type)

**Preference Types**:

#### Transport Preferences
```javascript
// Query: { type: 'transport' }
// Returns: DEFAULT_PREFERENCE.transport
{
  choose_setting: 'normal',  // Default setting mode
  normal: {
    transports: ['driving', 'walking'],
    path: 'best',
    road_types: ['motorways']
  },
  family: { /* family-specific settings */ },
  travel: { /* travel-specific settings */ },
  work: { /* work-specific settings */ }
}
```

#### Single Preferences
```javascript
// Query: { type: 'single', get_default: 'mass_transit' }
// Returns: DEFAULT_PREFERENCE.single.mass_transit
{
  transports: ['bus', 'subway', 'train'],
  path: 'trans_less'
}
```

#### Parking Preferences
```javascript
// Query: { type: 'parking' }
// Returns: DEFAULT_PREFERENCE.parking.parking
{
  search_range: 500,
  navigation_show: true,
  vehicle_height: 0,
  price: 0,
  charged_limit: false,
  operations: [1, 2, 3, 4, 5, 6, 7, 8, 9]
}
```

### 2. GET /preference
**Purpose**: Retrieves user's current preferences (defaults to system defaults if not customized)

**Same structure as default preferences but returns user-specific overrides if they exist**

### 3. PUT /preference
**Purpose**: Updates user's preference settings

**Request Structure**:
```javascript
{
  type: 'transport',  // Preference category
  change_data: {      // Updated preference data
    choose_setting: 'family',
    normal: {
      transports: ['driving', 'walking', 'cycling'],
      path: 'all',
      road_types: ['motorways', 'toll_roads']
    },
    family: {
      transports: ['bus', 'subway'],
      path: 'walk_less',
      road_types: ['ferries', 'tunnels']
    }
    // ... additional settings
  }
}
```

## Preference Categories

### Transport Preferences
**Four Setting Modes**:
1. **Normal**: Everyday transportation preferences
2. **Family**: Family-friendly transportation options
3. **Travel**: Long-distance travel preferences  
4. **Work**: Work commute preferences

**Configuration Options**:
- **Transports**: Available transportation modes
  - `driving`, `walking`, `cycling`, `bus`, `subway`, `train`, `tram`
- **Path**: Route optimization preference
  - `best`, `all`, `walk_less`, `trans_less`
- **Road Types**: Allowed road types
  - `motorways`, `toll_roads`, `ferries`, `tunnels`, `unpaved_roads`, `motorail_trains`

### Single Preferences
**Categories**:
1. **Vehicle**: Single-occupancy vehicle preferences
2. **Mass Transit**: Public transportation preferences

**Vehicle Preferences**:
```javascript
{
  road_types: [
    'motorways', 'toll_roads', 'ferries', 'tunnels',
    'unpaved_roads', 'motorail_trains'
  ]
}
```

**Mass Transit Preferences**:
```javascript
{
  transports: [
    'driving', 'walking', 'cycling', 'bus',
    'subway', 'train', 'tram'
  ],
  path: 'best'
}
```

### Parking Preferences
**Configuration Options**:
- **Search Range**: Maximum distance to search for parking (meters)
- **Navigation Show**: Display parking navigation
- **Vehicle Height**: Vehicle height limitations (for garage restrictions)
- **Price**: Maximum acceptable parking price
- **Charged Limit**: Electric vehicle charging requirements
- **Operations**: Available parking operations/features (array of IDs)

## Test Scenarios

### Default Preference Retrieval
```javascript
it('should get default transport preference', async () => {
  const resp = await request.set(auth).get(url).query({ type: 'transport' });
  expect(result).to.eq('success');
  expect(data).to.deep.includes(DEFAULT_PREFERENCE.transport);
});
```

### User Preference Updates
```javascript
it('should update transport preference', async () => {
  const transportData = {
    choose_setting: 'family',
    normal: {
      transports: ['driving', 'walking', 'cycling'],
      path: 'all',
      road_types: ['motorways', 'toll_roads']
    }
    // ... additional settings
  };
  
  const resp = await request.set(auth).put(url)
    .send({ type: 'transport', change_data: transportData });
    
  expect(result).to.eq('success');
  expect(data).to.deep.include(transportData);
});
```

### Error Scenarios
- **10003**: Missing Authorization token
- **10001**: Missing required 'type' parameter
- **10002**: Missing required 'type' in update request

## Business Logic

### Preference Hierarchy
1. **User Customizations**: Highest priority
2. **System Defaults**: Fallback when no user customization exists
3. **Dynamic Adaptation**: Preferences influence route calculation and suggestions

### Context-Aware Settings
- **Time-based**: Different preferences for work vs. personal trips
- **Purpose-based**: Family vs. travel vs. work optimization
- **Mode-specific**: Separate preferences for different transportation types

### Route Optimization
- **Path Preferences**: 
  - `best`: Optimal balance of time, cost, and convenience
  - `all`: Consider all available options
  - `walk_less`: Minimize walking distance
  - `trans_less`: Minimize transportation transfers

## Data Persistence

### Database Storage
```javascript
// Preference model structure
{
  user_id: Integer,     // User identifier
  type: String,         // Preference category
  preference_data: JSON // Preference configuration
}
```

### Test Data Management
```javascript
before('prepare testing data', async () => {
  const { access_token } = await AuthUsers.query()
    .select('access_token')
    .findById(userId);
  auth.Authorization = 'Bearer ' + accessToken;
});

after('remove testing data', async () => {
  await Preference.query().where('user_id', '=', userId).delete();
});
```

## Authentication and Security

### Bearer Token Authentication
- Retrieves access token from AuthUsers table
- Includes token in Authorization header
- Validates user ownership of preferences

### Data Validation
- Type parameter validation for all operations
- Structured data validation for updates
- Prevention of unauthorized field modifications

## Integration Points

### Route Planning
- Preferences influence route calculation algorithms
- Transportation mode filtering based on user settings
- Road type restrictions applied to routing

### Parking Services
- Parking search parameters from user preferences
- Vehicle-specific filtering (height, charging needs)
- Price and feature filtering

### Multi-Modal Transportation
- Cross-mode preference coordination
- Transfer optimization based on user tolerance
- Accessibility and comfort preferences

## Business Value

### Personalization
- Customized transportation recommendations
- User-specific route optimization
- Adaptive service delivery

### User Experience
- Reduced cognitive load through smart defaults
- Context-aware transportation suggestions
- Consistent experience across different trip purposes

### Operational Efficiency
- More accurate demand prediction
- Better resource allocation
- Improved user satisfaction and retention

## Test Coverage

### Functional Coverage
- ✅ Default preference retrieval for all types
- ✅ User preference retrieval and updates
- ✅ Authentication validation
- ✅ Parameter validation

### Data Coverage
- ✅ Transport preferences (all modes)
- ✅ Single preferences (vehicle/transit)
- ✅ Parking preferences
- ✅ Complex nested data structures

### Error Coverage
- ✅ Authentication failures
- ✅ Missing parameter validation
- ✅ Invalid request data handling

This test suite ensures the preference system provides flexible, user-customizable transportation settings that enhance the personalized experience within the TSP platform.