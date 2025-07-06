# Test Documentation: Favorites API

## Overview
This test suite validates the Favorites functionality, which allows users to save and manage frequently used locations within the TSP system. The test covers creating, retrieving, updating, and deleting favorite locations with category-based organization and count limitations.

## Test Configuration
- **File**: `test/test-favorites.js`
- **Framework**: Mocha with Chai assertions and Supertest for HTTP testing
- **Test Timeout**: 20 seconds for creation, 10 seconds for retrieval
- **Models Used**: `Favorites`
- **Authentication**: User ID-based authentication (userid: 1003)

## Test Data Structure

### Favorite Location Data
```javascript
const postData = {
  name: 'unit test',
  address: 'No.7, Sec. 5, Xinyi Rd., Xinyi Dist., Taipei City 110, Taiwan (R.O.C.)',
  latitude: 25.033969,
  longitude: 121.564461,
  category: 1,
};

const updateData = {
  name: 'unit test 2',
  address: 'test from unit test',
  latitude: 25.1234,
  longitude: 121.5678,
  category: 1,
};
```

### Response Structure Keys
```javascript
const responseKeys = [
  'id',
  'category',
  'name',
  'icon_type',
  'place_id',
  'access_latitude',
  'access_longitude',
  'longitude',
  'latitude',
  'created_on',
  'address',
  'modified_on',
];
```

## API Endpoints Tested

### 1. Create Favorite - `POST /favorites`
**Purpose**: Creates a new favorite location for the authenticated user

**Success Scenario**:
- Creates favorite with complete location data
- Returns created favorite with all response keys
- Assigns unique ID to the favorite
- Creates additional favorite with category 2 for testing
- Validates deep inclusion of posted data

**Error Scenarios**:
- `10004`: Missing authentication header (userid)
- `10002`: Required field validation (name is required)
- `20019`: Exceed count of favorite (business rule limitation)

**Business Rules**:
- Users have a limit on the number of favorites per category
- Each category appears to have a maximum of 1 favorite based on error testing
- Location data includes both coordinates and address information

### 2. Get Favorites - `GET /favorites`
**Purpose**: Retrieves all favorite locations for the authenticated user

**Success Scenario**:
- Returns array of user's favorites
- Each favorite includes all required response keys
- Validates data integrity against original creation data
- Confirms at least one favorite exists after creation

**Response Structure**:
```javascript
{
  result: 'success',
  data: {
    favorites: [
      {
        id: 123,
        category: 1,
        name: 'unit test',
        icon_type: null,
        place_id: null,
        access_latitude: 25.033969,
        access_longitude: 121.564461,
        longitude: 121.564461,
        latitude: 25.033969,
        created_on: '2023-01-01T00:00:00.000Z',
        address: 'No.7, Sec. 5, Xinyi Rd., Xinyi Dist., Taipei City 110, Taiwan (R.O.C.)',
        modified_on: '2023-01-01T00:00:00.000Z'
      }
    ]
  }
}
```

**Error Scenarios**:
- `10004`: Missing authentication header

### 3. Update Favorite - `PUT /favorites/:id`
**Purpose**: Updates an existing favorite location

**Success Scenario**:
- Updates favorite with new location data
- Returns updated favorite with all response keys
- Validates deep inclusion of updated data
- Maintains favorite ID consistency

**Error Scenarios**:
- `10004`: Missing authentication header
- `10002`: Required field validation (name is required)
- `20019`: Exceed count of favorite (when changing to existing category)
- `20014`: Favorite not found (invalid ID)

**Category Validation**:
- Test demonstrates category conflict when updating to category 2
- System enforces category limits across all operations
- Users cannot exceed favorite limits per category

### 4. Delete Favorite - `DELETE /favorites/:id`
**Purpose**: Removes a favorite location from the user's list

**Success Scenario**:
- Deletes favorite by ID
- Returns empty success response
- Removes favorite from user's collection

**Error Scenarios**:
- `10004`: Missing authentication header
- `20014`: Favorite not found (invalid ID or already deleted)

## Category System
The favorites system implements a category-based organization:
- **Category 1**: General favorites (home, work, etc.)
- **Category 2**: Secondary favorites or specific location types
- **Count Limitations**: Each category has a maximum number of allowed favorites
- **Category Conflicts**: Users cannot exceed limits when creating or updating

## Location Data Structure
Favorites store comprehensive location information:
- **Coordinates**: Latitude and longitude for precise positioning
- **Address**: Human-readable address string
- **Access Points**: Separate access coordinates for complex locations
- **Place Integration**: Support for external place ID references
- **Icon Types**: Customizable icons for different location types

## Data Validation Rules

### Required Fields
- `name`: User-defined name for the location
- `address`: Complete address information
- `latitude`: Geographic latitude coordinate
- `longitude`: Geographic longitude coordinate
- `category`: Category classification (1 or 2)

### Optional Fields
- `icon_type`: Custom icon selection
- `place_id`: External place service integration
- `access_latitude`: Alternative access point latitude
- `access_longitude`: Alternative access point longitude

## Business Logic

### Favorite Limits
- System enforces maximum favorites per category
- Error code 20019 indicates limit exceeded
- Limits apply to both creation and category changes
- Users must delete existing favorites to add new ones in full categories

### User Ownership
- Favorites are user-specific and private
- Authentication required for all operations
- Users can only manage their own favorites
- No sharing or public favorite functionality

### Location Accuracy
- Supports high-precision coordinates (6 decimal places)
- Includes both primary and access coordinates
- Address validation for human-readable information
- Integration potential with mapping services

## Test Coverage Analysis

### Positive Test Cases
- ✅ Create favorite with valid data
- ✅ Retrieve all user favorites
- ✅ Update existing favorite
- ✅ Delete favorite by ID
- ✅ Create multiple favorites with different categories

### Negative Test Cases
- ✅ Authentication validation (missing userid)
- ✅ Required field validation
- ✅ Business rule enforcement (favorite limits)
- ✅ Resource existence validation
- ✅ Category limit conflicts

### Edge Cases
- ✅ Category limit enforcement
- ✅ Duplicate category handling
- ✅ Invalid ID handling
- ✅ Data integrity validation

## Error Code Reference
- **10004**: Request header has something wrong (missing userid)
- **10002**: Required field validation errors
- **20019**: Exceed count of favorite (business rule)
- **20014**: Favorite not found (resource not found)

## Key Features Tested

### CRUD Operations
- Complete Create, Read, Update, Delete functionality
- Data integrity across operations
- Response consistency and validation

### Category Management
- Multiple category support
- Category-based limitations
- Category conflict resolution

### Location Services
- Geographic coordinate handling
- Address management
- Access point coordination
- Place ID integration potential

### User Experience
- Personal favorite management
- Quick location access
- Custom naming and organization
- Icon customization support

## Test Data Cleanup
The test suite includes proper cleanup in the `after` hook:
```javascript
after('Delete testing data', async () => {
  await Favorites.query().where('user_id', userId).delete();
});
```
This ensures test isolation and prevents data pollution between test runs.

This test suite ensures the favorites system provides reliable location management functionality for users within the TSP platform.