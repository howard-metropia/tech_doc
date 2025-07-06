# App Data API Test Suite

## Overview
Comprehensive test suite for the App Data API endpoint, focusing on user location-based labeling functionality. Tests the `postAppData` endpoint's ability to process user actions and geographic coordinates to assign appropriate user labels.

## File Purpose
- **Primary Function**: Test app data submission and user labeling logic
- **Type**: Integration test suite
- **Role**: Validates app data processing and location-based user categorization

## Test Configuration

### Test Setup
- **Framework**: Mocha with Chai assertions
- **HTTP Testing**: Supertest for API endpoint testing
- **Authentication**: JWT token-based authentication
- **Test User**: User ID 1003
- **Database**: Direct model manipulation for test data setup

### Dependencies
- `@maas/core/bootstrap`: Application bootstrapping
- `@maas/core/api`: API application factory
- `@maas/core`: Router and core utilities
- `supertest`: HTTP assertion library
- `chai`: Assertion library
- `AuthUserLabel`: User labeling model

## Test Scenarios

### App Data Submission Tests

#### Test Case 1: Generic Location Data
**Purpose**: Test app data submission with generic coordinates
**Input Data**:
```javascript
{
  action: 'OpenApp',
  lat: 1.0,
  lon: 1.0
}
```
**Expected Behavior**:
- API returns success response
- User receives label ID 3 (default/generic location)
- Database updated with correct user label

**Validation Steps**:
1. Submit app data with generic coordinates
2. Verify API response success
3. Wait for async processing (1.5 seconds)
4. Query database for updated user label
5. Confirm label ID is 3

#### Test Case 2: Houston-Specific Location Data
**Purpose**: Test app data submission with Houston coordinates
**Input Data**:
```javascript
{
  action: 'OpenApp',
  lat: 29.761384,
  lon: -95.369040
}
```
**Expected Behavior**:
- API returns success response
- User receives label ID 2 (Houston-specific location)
- Geographic processing identifies Houston coordinates

**Validation Steps**:
1. Submit app data with Houston coordinates
2. Verify API response success
3. Wait for extended async processing (6 seconds)
4. Query database for updated user label
5. Confirm label ID is 2

## Authentication Flow

### Token Management
```javascript
beforeEach(async () => {
  const token = await authToken(userid);
  auth = { ...auth, Authorization: `Bearer ${token}` };
});
```

### Header Configuration
- **Content-Type**: `application/json`
- **Authorization**: `Bearer {JWT_token}`
- **User Context**: Embedded user ID for request processing

## Database Operations

### Test Data Cleanup
```javascript
beforeEach(async () => {
  await AuthUserLabel.query()
    .where({ user_id: userid })
    .whereIn('label_id', [2, 3])
    .delete();
  
  await AuthUserLabel.query()
    .insert({
      user_id: userid,
      label_id: 3,
    });
});
```

### Label Verification
- Queries `AuthUserLabel` model for user-specific labels
- Filters by label IDs 2 and 3 (location-based categories)
- Validates label assignment based on geographic coordinates

## Geographic Processing Logic

### Location-Based Labeling
- **Generic Coordinates (1.0, 1.0)**: Assigns label ID 3
- **Houston Coordinates (29.761384, -95.369040)**: Assigns label ID 2
- **Processing Time**: Variable delay for geographic lookup

### Label Categories
- **Label ID 2**: Houston/Regional-specific users
- **Label ID 3**: Generic/Default users
- **Purpose**: Enable targeted features and content

## API Endpoint Details

### Endpoint Information
- **Method**: POST
- **Route**: Retrieved via `router.url('postAppData')`
- **Authentication**: Required JWT token
- **Rate Limiting**: Not specified in tests

### Request Format
```javascript
{
  "action": "OpenApp",
  "lat": number,
  "lon": number
}
```

### Response Format
```javascript
{
  "result": "success"
}
```

## Asynchronous Processing

### Processing Delays
- **Generic Location**: 1.5-second delay for processing
- **Houston Location**: 6-second delay for geographic lookup
- **Purpose**: Allow background processing to complete

### Background Tasks
- Geographic coordinate processing
- User label assignment
- Database updates
- Potential third-party service calls

## Error Handling

### Expected Behaviors
- Successful API responses for valid data
- Proper error handling for invalid coordinates
- Database transaction safety
- Authentication failure handling

### Logging Integration
- Debug-level logging enabled for testing
- MaaS core logging system integration
- Error tracking and reporting

## Integration Points

### Service Dependencies
- **Geographic Services**: Coordinate processing and location identification
- **User Management**: User labeling and categorization
- **Analytics**: App usage tracking and user behavior analysis

### Database Schema
- **AuthUserLabel Table**: User-to-label relationship mapping
- **Label Categories**: Predefined label types for user segmentation
- **Geographic Data**: Location-based processing rules

## Performance Considerations

### Test Execution
- Asynchronous processing requires wait times
- Database cleanup between tests
- Token generation for each test run

### Production Implications
- Geographic lookup performance
- Database update efficiency
- User labeling accuracy

## Maintenance Notes

### Test Data Management
- Clean user labels before each test
- Consistent test user (ID 1003)
- Predictable label assignment logic

### Geographic Accuracy
- Houston coordinates should remain valid
- Generic coordinates for baseline testing
- Consider additional location test cases

### Future Enhancements
- Test additional geographic regions
- Validate error scenarios
- Test concurrent user processing
- Add performance benchmarks