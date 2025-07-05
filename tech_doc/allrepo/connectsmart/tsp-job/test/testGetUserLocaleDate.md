# User Locale Date Service Test Suite

## Overview
Test suite for the user locale date service that validates the functionality of retrieving and formatting dates according to user's locale preferences and timezone settings, ensuring proper localization of date display in the application.

## File Location
`/test/testGetUserLocaleDate.js`

## Dependencies
- `chai` - Assertion library with assert interface
- `@app/src/services/common` - Common services including getUserLocaleDate function
- `@maas/core/mysql` - MySQL database connection for portal database

## Test Architecture

### Service Function Under Test
```javascript
const { getUserLocaleDate } = require('@app/src/services/common');
```

### Database Integration
- Uses real MySQL connection via `@maas/core/mysql`
- Creates temporary test user and app data records
- Performs complete cleanup after test execution

## Test Data Setup

### User Record Creation
```javascript
before(async () => {
  [userId] = await knex('auth_user').insert({
    first_name: 'test_first',
    last_name: 'test_last',
    device_language: 'en',
    common_email: 'cp_driver_001@metropia.com',
    cs_password: '$2b$10$bT6Za1oB9kbHZCeldC.d8OAlnZUgNEyjVKMvnRN92MyYw9izuu/kS',
    is_active: 'T',
    created_on: new Date()
      .toISOString()
      .replace('T', ' ')
      .replace('Z', '')
      .split('.')[0],
    security_key: 'MppvpyYfP6RPomyeF3zVruDr+fnKjcBYCWpTQqyaYVJJGpjlLW8lFDADy6qo8Tq9dQ0k3L3cEDIeMKt8aPUl2nSrEkQ7NEnIX75ubOh6yU4BoZEtjbZRNBj4lrUaNWJzMFBNrC7nzPi66X+Y6iBaat84YsprAZ1TJOleqo88J0embpzLLM4WyFuIztX1FYysqU+NNw/j3tCY+DUr9q4zKxeqq8Fn41lQxDm3STjCB51xYyKNxD+Hmfpj3kkl55elftHJoOaUEOPnhPZeJh9dmr6/5tmuvijfTcianibzAY49nQEjBGbj9jLFaEQ56mQZZ/PRXkYJXsMjL9TvJtkswg==',
  });
});
```

#### User Record Structure
- **first_name**: 'test_first' - User's first name
- **last_name**: 'test_last' - User's last name  
- **device_language**: 'en' - Language preference for localization
- **common_email**: Test email address for identification
- **cs_password**: Bcrypt hashed password for authentication
- **is_active**: 'T' - Active user status flag
- **created_on**: Formatted current timestamp
- **security_key**: Encrypted security key for session management

### App Data Record Creation
```javascript
[appDataId] = await knex('app_data').insert({
  user_id: userId,
  user_action: 'CreateCarpoolGroup',
  gmt_time: new Date()
    .toISOString()
    .replace('T', ' ')
    .replace('Z', '')
    .split('.')[0],
  local_time: new Date()
    .toISOString()
    .replace('T', ' ')
    .replace('Z', '')
    .split('.')[0],
  lat: 25.0498276,  // Taipei, Taiwan coordinates
  lon: 121.5270229,
});
```

#### App Data Structure
- **user_id**: Links to auth_user table
- **user_action**: 'CreateCarpoolGroup' - Action type for context
- **gmt_time**: GMT timestamp of the action
- **local_time**: Local timestamp of the action
- **lat**: Latitude coordinate (25.0498276 - Taipei)
- **lon**: Longitude coordinate (121.5270229 - Taipei)

## Geographic Context

### Test Location Coordinates
```javascript
lat: 25.0498276,  // Taipei, Taiwan
lon: 121.5270229,
```
- **Location**: Taipei, Taiwan
- **Timezone**: UTC+8 (Asia/Taipei)
- **Purpose**: Tests timezone-based date localization
- **Significance**: Non-US timezone for international localization testing

## Date Format Testing

### Locale Date Validation
```javascript
it('check local date', async () => {
  const t = await getUserLocaleDate(userId, new Date());
  assert(t.match(/[a-zA-Z]{3} [0-9]{1,2}, [0-9]{4}/));
});
```

#### Expected Format Pattern
- **Pattern**: `/[a-zA-Z]{3} [0-9]{1,2}, [0-9]{4}/`
- **Format**: "MMM DD, YYYY" (e.g., "Jan 15, 2023")
- **Components**:
  - **Month**: Three-letter month abbreviation (Jan, Feb, Mar, etc.)
  - **Day**: 1-2 digit day of month (1-31)
  - **Year**: Four-digit year

### Localization Features
The service handles:
1. **User Language**: Uses 'en' (English) from device_language field
2. **Timezone Adjustment**: Converts UTC time to user's local timezone
3. **Cultural Formatting**: Applies locale-specific date format conventions
4. **Coordinate-Based Timezone**: Determines timezone from lat/lon coordinates

## Database Operations

### Table Dependencies
- **auth_user**: User profile and preference data
- **app_data**: User activity data with location information

### Data Cleanup
```javascript
after(async () => {
  await knex('auth_user').where({ id: userId }).delete();
  await knex('app_data').where({ id: appDataId }).delete();
});
```

### Transaction Safety
- Uses array destructuring to capture auto-generated IDs
- Ensures complete cleanup of test data
- Maintains referential integrity during cleanup

## Service Integration

### Common Services Module
```javascript
const { getUserLocaleDate } = require('@app/src/services/common');
```

### Function Signature
```javascript
getUserLocaleDate(userId, dateObject)
```
- **userId**: Database ID of the user
- **dateObject**: JavaScript Date object to format
- **Returns**: Localized date string

## Timezone Processing Logic

### Location-Based Timezone Detection
1. **Coordinate Lookup**: Uses lat/lon from app_data table
2. **Timezone Mapping**: Maps coordinates to timezone identifier
3. **Offset Calculation**: Determines UTC offset for the location
4. **Local Conversion**: Converts input date to local time

### Language Localization
1. **Language Preference**: Retrieves device_language from auth_user
2. **Locale Mapping**: Maps language code to locale settings
3. **Format Application**: Applies locale-specific date formatting
4. **Cultural Adaptation**: Adjusts format for cultural preferences

## Error Handling

### Missing User Data
- Handles cases where user ID doesn't exist
- Manages missing app_data records gracefully
- Provides fallback behavior for incomplete data

### Invalid Coordinates
- Validates latitude/longitude ranges
- Handles coordinate-to-timezone lookup failures
- Uses default timezone when location data is unavailable

## Performance Considerations

### Database Queries
- Single query to retrieve user preferences
- Joined query for user and location data
- Indexed lookups on user_id for performance

### Caching Potential
- Timezone lookup results could be cached
- User language preferences are relatively static
- Geographic timezone mappings change infrequently

## Testing Best Practices

### Realistic Test Data
- Uses actual geographic coordinates
- Includes proper password hashing
- Maintains referential integrity between tables

### Assertion Strategy
- **Pattern Matching**: Validates date format structure
- **Regex Testing**: Ensures consistent output format
- **Functional Testing**: Tests actual service integration

## Integration Points

### User Management System
- **Authentication**: Integrates with user authentication system
- **Preferences**: Respects user language and locale settings
- **Privacy**: Handles user location data appropriately

### Localization Framework
- **i18n Support**: Enables internationalization
- **Culture-Specific Formatting**: Adapts to regional preferences
- **Multi-Language Support**: Foundation for multiple languages

## Business Applications

### Use Cases
1. **Trip Notifications**: Display trip times in user's local format
2. **Report Generation**: Format dates consistently for user reports
3. **UI Localization**: Ensure date displays match user expectations
4. **Audit Logging**: Record actions with properly formatted timestamps

### User Experience
- **Familiar Formats**: Displays dates in user's expected format
- **Timezone Accuracy**: Shows times in user's actual timezone
- **Language Consistency**: Matches user's language preferences
- **Cultural Sensitivity**: Respects regional date format conventions

## Quality Assurance

### Test Coverage
1. **Format Validation**: Ensures correct date string format
2. **Database Integration**: Tests real database operations
3. **Service Function**: Validates actual service behavior
4. **Cleanup Verification**: Ensures no test data pollution

### Edge Case Considerations
- **Timezone Boundaries**: Date changes across timezone lines
- **Daylight Saving**: Handles DST transitions correctly
- **Leap Years**: Proper handling of February 29th
- **International Dates**: Non-US date format requirements

## Maintenance Considerations

### Database Schema Changes
- Updates to auth_user table structure
- Changes to app_data location fields
- New timezone or localization requirements

### Localization Updates
- Additional language support
- New date format requirements
- Cultural format preferences
- Timezone database updates

## Security Considerations

### Data Privacy
- **Location Data**: Sensitive geographic information
- **User Preferences**: Personal configuration data
- **Test Data**: Proper cleanup prevents data leakage
- **Authentication**: Secure password handling in tests

### Access Control
- **User Data Access**: Validates user ownership of data
- **Location Privacy**: Respects location data sensitivity
- **Test Isolation**: Prevents cross-test data contamination