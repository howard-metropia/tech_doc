# App Version API Test Suite

## Overview
Comprehensive test suite for the App Version API endpoint, validating version comparison logic, upgrade requirements, and platform-specific version management. Tests the `getAppVersion` endpoint's ability to determine app compatibility and upgrade requirements.

## File Purpose
- **Primary Function**: Test app version validation and upgrade logic
- **Type**: Integration test suite
- **Role**: Validates version compatibility and upgrade requirement determination

## Test Configuration

### Test Setup
- **Framework**: Mocha with Chai assertions
- **HTTP Testing**: Supertest for API endpoint testing
- **Test User**: User ID 1003
- **Platform Focus**: Android platform testing
- **Version Comparison**: Dynamic version testing based on latest version

### Dependencies
- `@maas/core/bootstrap`: Application bootstrapping
- `@maas/core/api`: API application factory
- `@maas/core`: Router and core utilities
- `supertest`: HTTP assertion library
- `chai`: Assertion library

## Test Scenarios

### Basic Version Retrieval

#### Test Case 1: Get Current App Version
**Purpose**: Retrieve current app version information for Android platform
**Endpoint**: `GET /app-version/android`
**Expected Response Properties**:
```javascript
{
  newest_version: string,
  base_version: string,
  supported: boolean,
  can_upgrade: boolean,
  required_upgrade: boolean
}
```

**Validation Steps**:
1. Request app version for Android platform
2. Verify response contains all required properties
3. Store newest_version for subsequent tests
4. Validate response structure and data types

### Version Comparison Logic

#### Test Case 2: Older Version Upgrade Requirements
**Purpose**: Test upgrade requirements for older app versions
**Input**: Version one major version behind current
**Expected Behavior**:
- `supported`: true
- `can_upgrade`: true
- `required_upgrade`: true

**Logic**:
```javascript
const version = `${parseInt(newestVersion[0]) - 1}.0.0`;
```

**Validation**:
- App supports older versions
- Upgrade is available and recommended
- Upgrade is required for continued support

#### Test Case 3: Future Version Handling
**Purpose**: Test behavior with version newer than latest
**Input**: Version one major version ahead of current
**Expected Behavior**:
- `supported`: false
- `can_upgrade`: false
- `required_upgrade`: false

**Logic**:
```javascript
const version = `${parseInt(newestVersion[0]) + 1}.0.0`;
```

**Validation**:
- Future versions not supported
- No upgrade available for future versions
- No upgrade requirements for unsupported versions

### Error Handling

#### Test Case 4: Invalid Platform Validation
**Purpose**: Test error handling for unsupported platforms
**Input**: Windows platform (unsupported)
**Expected Error**:
```javascript
{
  result: "fail",
  error: {
    code: 10001,
    msg: '"os" must be one of [ios, android]'
  }
}
```

**Validation**:
- Platform validation enforced
- Appropriate error code and message
- Only iOS and Android platforms supported

## API Endpoint Details

### Endpoint Information
- **Method**: GET
- **Route Pattern**: `/app-version/{platform}`
- **Platforms Supported**: `ios`, `android`
- **Authentication**: User ID header required

### Request Headers
```javascript
{
  userid: 1003,
  'Content-Type': 'application/json'
}
```

### Query Parameters
- `version` (optional): Current app version for comparison

### Response Structure
```javascript
{
  "result": "success",
  "data": {
    "newest_version": "string",
    "base_version": "string",
    "supported": boolean,
    "can_upgrade": boolean,
    "required_upgrade": boolean
  }
}
```

## Version Logic Analysis

### Version Comparison Algorithm
- **Current Version**: User's installed app version
- **Newest Version**: Latest available app version
- **Base Version**: Minimum supported app version

### Support Matrix

| User Version | Supported | Can Upgrade | Required Upgrade |
|-------------|-----------|-------------|------------------|
| < Base      | false     | true        | true             |
| >= Base     | true      | varies      | varies           |
| > Newest    | false     | false       | false            |

### Platform-Specific Handling
- **iOS**: Apple App Store version management
- **Android**: Google Play Store version management
- **Unsupported Platforms**: Validation error returned

## Error Code Reference

### Code 10001: Validation Error
- **Trigger**: Invalid platform parameter
- **Message**: Platform must be 'ios' or 'android'
- **Resolution**: Use supported platform identifier

### Authentication Errors
- **Missing User ID**: Request header validation
- **Invalid User**: User context validation

## Integration Points

### Version Management System
- **Version Storage**: Database or configuration management
- **Platform Configuration**: iOS and Android version tracking
- **Update Policies**: Forced vs. optional updates

### Client Integration
- **Version Checking**: App startup version validation
- **Update Prompts**: User notification for available updates
- **Forced Updates**: Blocking app usage for required updates

## Test Data Management

### Dynamic Version Testing
- **Latest Version Discovery**: Query current newest version
- **Relative Version Testing**: Generate test versions dynamically
- **Version Format**: Semantic versioning (major.minor.patch)

### Test Isolation
- **No Database Changes**: Read-only version checking
- **Stateless Testing**: Each test independent
- **Platform Consistency**: Consistent behavior across platforms

## Performance Considerations

### Response Time
- **Version Lookup**: Fast database or cache query
- **Comparison Logic**: Minimal computational overhead
- **Platform Validation**: Immediate parameter checking

### Caching Strategy
- **Version Data**: Cache version information
- **Comparison Results**: Cache upgrade decisions
- **Platform Rules**: Cache validation rules

## Security Considerations

### Version Validation
- **Input Sanitization**: Version string validation
- **Platform Restriction**: Limited to supported platforms
- **User Context**: User ID requirement

### Information Disclosure
- **Version Information**: Public version data
- **Platform Support**: Known platform limitations
- **Update Requirements**: Transparent upgrade policies

## Maintenance Notes

### Version Updates
- **New Releases**: Update newest_version configuration
- **Support Policies**: Adjust base_version requirements
- **Platform Changes**: Add new platform support

### Test Maintenance
- **Version Dependencies**: Update test versions with releases
- **Platform Coverage**: Ensure all platforms tested
- **Error Scenarios**: Validate error handling paths

### Future Enhancements
- **iOS Platform Testing**: Add comprehensive iOS tests
- **Version History**: Test version rollback scenarios
- **Feature Flags**: Test version-specific feature availability
- **Gradual Rollouts**: Test phased update deployment