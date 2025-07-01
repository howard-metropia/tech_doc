# User Profiles Helper Module Documentation

## Overview
The User Profiles Helper Module provides comprehensive user profile data aggregation and formatting for the ConnectSmart Hybrid Portal application. It handles user information retrieval, name formatting with internationalization support, and flexible metadata inclusion.

## File Location
**Source**: `/home/datavan/METROPIA/metro_combine/allrepo/connectsmart/hybrid/applications/portal/modules/profiles_helper.py`

## Dependencies
- `utils.cdn_url`: CDN URL generation utility
- `re`: Regular expression operations for Unicode handling

## Functions

### `user_profiles(db, user_ids, meta=None)`

#### Purpose
Retrieve and format user profile information with customizable metadata inclusion.

#### Parameters
- `db`: Database connection object
- `user_ids` (list): List of user IDs to retrieve profiles for
- `meta` (list, optional): List of additional metadata fields to include

#### Returns
List of user profile dictionaries with formatted information

## Profile Data Structure

### Core Profile Fields
```python
{
    'user_id': int,                    # User database ID
    'name': {                          # Name components
        'first_name': str,
        'last_name': str
    },
    'full_name': str,                  # Formatted display name
    'avatar': str,                     # CDN URL for avatar image
    'rating': float                    # User rating score
}
```

### Extended Metadata Fields

#### Vehicle Information (`meta=['vehicle']`)
```python
'vehicle': {
    'type': str,                       # Vehicle type
    'color': str,                      # Vehicle color
    'plate': str                       # License plate number
}
```

#### Detailed Vehicle Information (`meta=['vehicle_detail']`)
```python
'vehicle': {
    'type': str,                       # Vehicle type
    'color': str,                      # Vehicle color
    'plate': str,                      # License plate number
    'make': str,                       # Vehicle manufacturer
    'picture_front': str,              # CDN URL for front photo
    'picture_side': str                # CDN URL for side photo
}
```

#### Phone Information (`meta=['phone']`)
```python
'phone': {
    'country_code': str,               # Country calling code
    'phone_number': str                # Phone number
}
```

#### Device Information (`meta=['device']`)
```python
'device': {
    'model': str,                      # Device model
    'language': str,                   # Device/user language
    'token_type': str,                 # 'apns', 'fcm', or None
    'token': str                       # Push notification token
}
```

## Name Formatting Logic

### Full Name Generation
The module implements sophisticated name formatting with internationalization support:

#### Single Name Cases
- **Only First Name**: Uses first name as full name
- **Only Last Name**: Uses last name as full name

#### Complete Name Cases
The formatting logic handles different cultural naming conventions:

##### Asian Name Format Detection
```python
# Detects Chinese/Japanese/Korean characters
fl = re.findall(u'[\u4e00-\u9fff]', first_name)
ll = re.findall(u'[\u4e00-\u9fff]', last_name)

if len(fl) > 0 or len(ll) > 0:
    # Asian format: LastName + FirstName (no space)
    full_name = row.last_name + '' + row.first_name
```

##### Western Name Format
```python
else:
    # Western format: FirstName + LastInitial.
    full_name = row.first_name + ' ' + row.last_name[0] + '.'
```

## Device Token Management

### Token Type Detection
```python
type_map = {
    row.apns_device_token: 'apns',     # iOS devices
    row.device_token: 'fcm',           # Android devices
    None: None                         # No token
}
```

### Token Priority
- Prefers `device_token` (FCM) over `apns_device_token`
- Automatically determines token type based on presence

## Usage Examples

### Basic Profile Retrieval
```python
# Get basic profiles for multiple users
user_ids = [123, 456, 789]
profiles = user_profiles(db, user_ids)

for profile in profiles:
    print(f"User: {profile['full_name']}")
    print(f"Rating: {profile['rating']}")
```

### Extended Profile with Vehicle Info
```python
# Include vehicle information
profiles = user_profiles(db, user_ids, meta=['vehicle'])

for profile in profiles:
    if 'vehicle' in profile:
        vehicle = profile['vehicle']
        print(f"{profile['full_name']} drives a {vehicle['color']} {vehicle['type']}")
```

### Complete Profile Data
```python
# Include all available metadata
meta_fields = ['vehicle_detail', 'phone', 'device']
profiles = user_profiles(db, user_ids, meta=meta_fields)

for profile in profiles:
    print(f"User: {profile['full_name']}")
    if 'phone' in profile:
        phone = profile['phone']
        print(f"Phone: +{phone['country_code']}{phone['phone_number']}")
```

### Driver Profile for Rideshare
```python
# Specific metadata for driver profiles
driver_meta = ['vehicle_detail', 'phone', 'device']
driver_profiles = user_profiles(db, driver_ids, meta=driver_meta)

for driver in driver_profiles:
    print(f"Driver: {driver['full_name']} (Rating: {driver['rating']})")
    vehicle = driver.get('vehicle', {})
    print(f"Vehicle: {vehicle.get('make')} {vehicle.get('type')}")
    print(f"Plate: {vehicle.get('plate')}")
```

## Database Schema Requirements

### auth_user Table Fields
```sql
-- Core fields
id INTEGER PRIMARY KEY
first_name VARCHAR
last_name VARCHAR  
avatar VARCHAR
rating DECIMAL

-- Vehicle fields
vehicle_type VARCHAR
vehicle_color VARCHAR
vehicle_plate VARCHAR
vehicle_make VARCHAR
vehicle_picture_front VARCHAR
vehicle_picture_side VARCHAR

-- Contact fields
country_code VARCHAR
phone_number VARCHAR

-- Device fields
device_model VARCHAR
device_language VARCHAR
device_token VARCHAR        -- FCM token
apns_device_token VARCHAR   -- iOS token
```

## Internationalization Features

### Unicode Character Support
- **Chinese Characters**: `\u4e00-\u9fff` range
- **Japanese Hiragana/Katakana**: Included in CJK range
- **Korean Characters**: Hangul support

### Cultural Name Conventions
- **Asian**: Family name first, no space separation
- **Western**: Given name first, abbreviated family name
- **Flexible**: Handles missing name components gracefully

## Performance Considerations

### Query Optimization
- Single database query for all requested users
- Efficient `belongs()` operation for ID filtering
- Minimal data processing overhead

### Memory Usage
- Builds profile list incrementally
- CDN URL generation only when needed
- Metadata included conditionally

## CDN Integration

### Avatar URLs
```python
avatar = cdn_url(row.avatar)  # Converts relative path to full CDN URL
```

### Vehicle Images
```python
picture_front = cdn_url(row.vehicle_picture_front)
picture_side = cdn_url(row.vehicle_picture_side)
```

## Error Handling

### Missing Data Graceful Handling
- Empty strings handled appropriately
- None values converted to meaningful defaults
- Missing metadata fields skipped without errors

### Validation Considerations
- No explicit validation of user IDs
- Assumes valid database connection
- Unicode regex safe for all string inputs

## Integration Patterns

### API Response Formatting
```python
def get_user_profiles_api():
    user_ids = request.vars.user_ids.split(',')
    meta = request.vars.meta.split(',') if request.vars.meta else None
    
    profiles = user_profiles(db, user_ids, meta)
    return dict(users=profiles)
```

### Rideshare Driver Matching
```python
def find_nearby_drivers(location, meta=['vehicle', 'phone', 'device']):
    # Get driver IDs from location query
    driver_ids = get_drivers_near_location(location)
    
    # Get full driver profiles
    return user_profiles(db, driver_ids, meta=meta)
```

## Security Considerations
- Profile data exposure controlled by meta parameter
- Phone numbers only included when explicitly requested
- Device tokens protected by metadata filtering
- Avatar URLs through CDN prevent direct file access

## Future Enhancements
- Profile caching mechanism
- Additional metadata field support
- Bulk profile update operations
- Profile data validation
- Privacy settings integration

## Related Components
- CDN URL utility
- User authentication system
- Device notification management
- Vehicle management system