# Common Service

## Overview

The Common service provides localization utilities for date formatting based on user location and language preferences, integrating geographic timezone detection with user language settings.

## Service Information

- **Service Name**: Common
- **File Path**: `/src/services/common.js`
- **Type**: Localization Utility Service
- **Dependencies**: Moment.js, Geo-TZ, MySQL

## Functions

### getUserLocaleDate(userId, dateTime)

Formats dates according to user's locale and timezone preferences.

**Purpose**: Provides localized date strings for user-facing content
**Parameters**:
- `userId` (number): User identifier for locale detection
- `dateTime` (string|Date): UTC date/time to format

**Returns**: Formatted date string in user's locale

**Example**:
```javascript
const localDate = await getUserLocaleDate(12345, "2023-12-25T10:00:00Z");
// Returns: "Dec 25, 2023" (English) or "25 dic 2023" (Spanish)
```

### getUserLocaleMoment(userId, dateTime)

Creates a Moment.js object with user's timezone and language settings.

**Purpose**: Provides timezone-aware Moment objects for date manipulation
**Parameters**:
- `userId` (number): User identifier
- `dateTime` (string|Date): UTC date/time to convert

**Returns**: Moment.js object in user's timezone with locale

**Process Flow**:
1. **Default Timezone**: America/Chicago as fallback
2. **Location Lookup**: Queries app_data for user's latest coordinates
3. **Timezone Detection**: Uses geo-tz to find timezone by coordinates
4. **Language Detection**: Retrieves device_language from auth_user
5. **Locale Application**: Sets Moment.js locale and timezone

## Data Sources

### User Location (app_data table)
- **Query**: Latest record by user_id (ORDER BY id DESC LIMIT 1)
- **Fields**: lat, lon coordinates
- **Purpose**: Geographic timezone determination

### User Language (auth_user table)
- **Query**: device_language field
- **Processing**: Converts underscore to dash, lowercase normalization
- **Default**: 'en-us' for missing language preferences

## Geographic Processing

### Timezone Detection
- **Library**: geo-tz for coordinate-based timezone lookup
- **Input**: Latitude/longitude coordinates
- **Output**: IANA timezone identifier (e.g., "America/New_York")
- **Fallback**: "America/Chicago" when coordinates unavailable

### Coordinate Validation
- Uses latest app_data record for most accurate location
- Handles missing coordinates gracefully
- Provides reasonable default timezone

## Language Processing

### Language Normalization
```javascript
lang = lang.replace('_', '-').toLowerCase();
// Converts: 'en_US' → 'en-us'
```

### Supported Locales
- Supports all Moment.js locales
- Automatic locale detection from user language
- Fallback to 'en-us' for unsupported languages

### Date Formatting
- **Format**: 'll' (localized date format)
- **Examples**: 
  - English: "Dec 25, 2023"
  - Spanish: "25 dic 2023"
  - French: "25 déc. 2023"

## Integration Points

### Used By
- Token expiration notifications
- Event date display
- User communication services
- Timezone-aware scheduling

### External Dependencies
- **Moment.js**: Date manipulation and formatting
- **Geo-TZ**: Geographic timezone detection
- **MySQL Portal**: User location and language data

## Error Handling

### Missing Data
- **No Coordinates**: Falls back to America/Chicago timezone
- **No Language**: Defaults to 'en-us' locale
- **Invalid User**: Graceful handling of non-existent users

### Database Errors
- **Connection Issues**: Handled by database connection pool
- **Query Failures**: Fallback to default values
- **Transaction Safety**: Read-only operations

## Performance Considerations

### Database Queries
- **Optimized Lookups**: Single record queries with LIMIT 1
- **Indexed Queries**: Uses user_id indexes for fast retrieval
- **Minimal Data**: Selects only required fields

### Caching Opportunities
- User timezone/language settings rarely change
- Consider caching for frequently accessed users
- Memory-efficient single-record queries

## Security Considerations

- **User Privacy**: Location data handled securely
- **Data Access**: Read-only user data access
- **No Data Storage**: Doesn't persist user preferences

## Usage Guidelines

1. **Date Consistency**: Use for all user-facing date displays
2. **Timezone Awareness**: Always consider user's local timezone
3. **Language Support**: Ensure content supports detected locale
4. **Error Handling**: Handle cases where user data is unavailable
5. **Performance**: Consider caching for high-frequency usage

## Limitations

### Current Implementation
- **Single Location**: Uses only latest location data
- **No Preference Override**: Cannot manually set timezone/language
- **Database Dependency**: Requires user data for localization

### Future Enhancements
- **User Preferences**: Allow manual timezone/language selection
- **Location History**: Use location patterns for better timezone detection
- **Caching Layer**: Implement user preference caching

## Dependencies

- **Moment.js**: Date manipulation and localization
- **Geo-TZ**: Geographic timezone determination
- **@maas/core/mysql**: Database connection management
- **@maas/core/log**: Error logging capabilities