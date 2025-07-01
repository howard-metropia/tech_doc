# App Version Controller API Documentation

## Overview
The App Version Controller manages mobile application version control and update notifications in the MaaS platform. It provides version checking capabilities to determine if app updates are available, required, or if the current version is supported.

**File Path:** `/allrepo/connectsmart/hybrid/applications/portal/controllers/app_version.py`

**Controller Type:** Public Portal Controller

**Authentication:** No authentication required for version checking

## Features
- App version compatibility checking
- Platform-specific version management (iOS/Android)
- Required vs optional update detection
- Support status validation
- Version comparison using semantic versioning

## API Endpoints

### Version Index
**Endpoint:** `/app_version/index`
**Methods:** GET
**Authentication:** None

#### GET - Version Index
Basic endpoint that returns 404 for v1 API calls and empty response for v2+.

**Response:**
- Returns empty string for v2+ API calls
- Returns 404 for v1 API calls

**Status Codes:**
- `200`: Success (v2+ API)
- `404`: Not found (v1 API)

### Latest Version Check
**Endpoint:** `/app_version/latest`
**Methods:** GET
**Authentication:** None

#### GET - Check Latest Version
Checks if app updates are available and determines update requirements.

**Required Parameters:**
- `app_os`: Platform identifier ('ios' or 'android')

**Optional Parameters:**
- `version`: Current app version for comparison

**Headers:**
- `newversion`: Custom header for version tracking

**Response Format:**
```json
{
  "success": true,
  "data": {
    "newest_version": "2.1.0",
    "base_version": "2.0.0",
    "required_upgrade": false,
    "can_upgrade": true,
    "supported": true,
    "headerVersion": "1.2.3"
  }
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid parameters (missing or invalid app_os)

## Version Logic

### Version Comparison Rules
The system uses LooseVersion for semantic version comparison:

1. **Newest Version**: Highest published version for the platform
2. **Base Version**: Minimum required version (marked as required)
3. **Required Upgrade**: Current version < base version
4. **Can Upgrade**: Current version < newest version
5. **Supported**: Current version ≤ newest version

### Update Decision Matrix
```
Current vs Base    | Current vs Newest | Action
-------------------|-------------------|------------------
< base version     | Any              | Required upgrade
≥ base version     | < newest         | Optional upgrade
≥ base version     | = newest         | No upgrade needed
> newest version   | N/A              | Unsupported
```

## Data Model

### App Update Structure
```python
{
    "app_os": str,              # Platform: 'ios' or 'android'
    "app_version": str,         # Version string (e.g., "2.1.0")
    "published": bool,          # Whether version is published
    "is_required": bool         # Whether this is a required update
}
```

## Database Schema

### Table: app_update
- `app_os`: Platform identifier ('ios', 'android')
- `app_version`: Semantic version string
- `published`: Publication status (boolean)
- `is_required`: Required update flag (boolean)

### Query Logic
```sql
SELECT * FROM app_update 
WHERE app_os = ? AND published = true
ORDER BY app_version DESC
```

## Version Management

### Version States
1. **Published**: Available for download
2. **Required**: Must be installed (base version)
3. **Latest**: Most recent published version
4. **Supported**: Within supported version range

### Platform Support
- **iOS**: Handles iOS app store versions
- **Android**: Manages Google Play store versions
- **Cross-platform**: Common version checking logic

## Implementation Details

### Key Dependencies
- `distutils.version.LooseVersion`: Semantic version comparison
- `json_response`: Standardized response formatting
- Database ORM for app_update table queries

### Version Processing Algorithm
```python
def process_versions(app_os, current_version=None):
    # Find all published versions for platform
    versions = query_published_versions(app_os)
    
    # Determine newest and base versions
    newest = find_highest_version(versions)
    base = find_required_version(versions)
    
    # Compare with current version if provided
    if current_version:
        required_upgrade = current_version < base
        can_upgrade = current_version < newest
        supported = current_version <= newest
    
    return version_status
```

### Header Processing
- Captures `http_newversion` header for tracking
- Logs version header for debugging
- Returns header value in response

## Error Handling

### Parameter Validation
- Validates `app_os` parameter presence
- Ensures `app_os` is either 'ios' or 'android'
- Handles missing version parameter gracefully

### Error Response Format
```json
{
  "success": false,
  "error_code": "ERROR_BAD_REQUEST_PARAMS",
  "message": "Invalid parameters"
}
```

## Usage Examples

### Check iOS Version
```bash
curl -X GET "/app_version/latest/ios?version=2.0.1" \
  -H "newversion: 2.0.1"
```

### Check Android Version
```bash
curl -X GET "/app_version/latest/android?version=1.9.5"
```

### Response Example
```json
{
  "success": true,
  "data": {
    "newest_version": "2.1.0",
    "base_version": "2.0.0", 
    "required_upgrade": false,
    "can_upgrade": true,
    "supported": true,
    "headerVersion": "2.0.1"
  }
}
```

## Integration Points

### Mobile Applications
- iOS app checks for updates on launch
- Android app validates compatibility
- In-app update prompts based on response

### App Store Integration
- Coordinates with app store release cycles
- Manages staged rollouts
- Handles version deprecation

### Analytics Integration
- Tracks version adoption rates
- Monitors update compliance
- Reports version distribution

## Configuration Management

### Version Release Process
1. **Staging**: Test new version internally
2. **Publishing**: Mark version as published
3. **Required Update**: Set base version if needed
4. **Rollout**: Monitor adoption metrics

### Database Management
```sql
-- Publish new version
INSERT INTO app_update (app_os, app_version, published, is_required) 
VALUES ('ios', '2.1.0', true, false);

-- Mark version as required
UPDATE app_update 
SET is_required = true 
WHERE app_os = 'ios' AND app_version = '2.0.0';
```

## Security Considerations

### Public Endpoint
- No authentication required for version checks
- Rate limiting recommended for abuse prevention
- Input validation prevents injection attacks

### Version Integrity
- Version strings validated against expected format
- Database constraints prevent invalid data
- Audit trails for version management changes

## Performance Optimization

### Caching Strategy
- Cache version lookup results
- Implement CDN for global distribution
- Use database indexes on app_os and published fields

### Query Optimization
```sql
-- Optimized query with index
CREATE INDEX idx_app_update_lookup 
ON app_update (app_os, published, app_version);
```

## Monitoring & Alerting

### Key Metrics
- Version check request volume
- Update adoption rates
- Unsupported version usage
- Platform distribution

### Health Checks
- Database connectivity
- Version data consistency
- Response time monitoring

## Troubleshooting Guide

### Common Issues
1. **Version Not Found**: Check published status
2. **Wrong Update Status**: Verify is_required flag
3. **Platform Issues**: Validate app_os parameter
4. **Version Comparison**: Check LooseVersion format

### Debug Logging
- Log version comparison results
- Track header values
- Monitor database query performance