# Duo Group Controller API Documentation

## Overview
The Duo Group Controller manages carpool groups in the MaaS platform, enabling users to create, join, and manage community-based carpooling organizations. It supports both public and private groups, enterprise integration, and comprehensive group administration features.

**File Path:** `/allrepo/connectsmart/hybrid/applications/portal/controllers/duo_group.py`

**Controller Type:** Authenticated Portal Controller

**Authentication:** JWT token required

## Features
- Comprehensive group lifecycle management (create, update, delete)
- Public and private group support
- Enterprise group integration with email verification
- Image management for group avatars and banners
- Geofencing with radius-based location constraints
- Member management with role-based permissions
- Advanced search capabilities with location and name filtering
- Administrative profile management for group leaders

## API Endpoints

### Group Management
**Endpoint:** `/duo_group/group`
**Methods:** GET, POST, PUT, DELETE
**Authentication:** JWT token required

#### POST - Create Carpool Group
Creates a new carpool group with specified parameters.

**Required Fields:**
- `name`: Group name (must be unique)
- `types`: Array of group type IDs
- `is_private`: Boolean indicating private/public status
- `geofence`: Location object with coordinates and radius

**Optional Fields:**
- `description`: Group description
- `avatar`: Base64 encoded avatar image
- `banner`: Base64 encoded banner image
- `enterprise_id`: Enterprise association

**Request Example:**
```json
{
  "name": "Downtown Commuters",
  "types": [1, 2],
  "is_private": false,
  "geofence": {
    "latitude": 25.0330,
    "longitude": 121.5654,
    "radius": 5000,
    "address": "Taipei Main Station, Taiwan"
  },
  "description": "Group for daily downtown commuters",
  "enterprise_id": 123
}
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "id": 456
  }
}
```

**Status Codes:**
- `201`: Group created successfully
- `400`: Invalid parameters
- `403`: Duplicate group name or invalid group type

#### GET - List User Groups
Retrieves carpool groups the user has joined.

**Parameters:**
- `sortby` (optional): Sort order ('asc' or 'desc', default: 'asc')
- `offset` (optional): Pagination offset (default: 0)
- `perpage` (optional): Items per page (default: 10)

**Response Format:**
```json
{
  "success": true,
  "data": {
    "groups": [
      {
        "id": 456,
        "creator_id": 123,
        "name": "Downtown Commuters",
        "description": "Group for daily downtown commuters",
        "avatar": "https://cdn.example.com/avatar.jpg",
        "banner": "https://cdn.example.com/banner.jpg",
        "is_private": false,
        "geofence": {
          "latitude": 25.0330,
          "longitude": 121.5654,
          "radius": 5000,
          "address": "Taipei Main Station, Taiwan"
        },
        "member_status": 1,
        "types": [1, 2],
        "members": 25,
        "enterprise": false
      }
    ],
    "total_count": 5,
    "next_offset": 10
  }
}
```

#### PUT - Update Group
Updates group information (manager permissions required).

**URL Parameter:**
- `group_id`: Group ID to update

**Updatable Fields:**
- `name`: Group name
- `types`: Group type array
- `description`: Group description
- `avatar`: Avatar image
- `is_private`: Privacy setting
- `geofence`: Location and radius
- `banner`: Banner image

#### DELETE - Delete Group
Deletes a group (manager permissions required).

**URL Parameter:**
- `group_id`: Group ID to delete

### Group Search
**Endpoint:** `/duo_group/search`
**Methods:** GET
**Authentication:** JWT token required

#### GET - Search Groups
Searches for groups by name, location, or enterprise email.

**Search Parameters:**
- `q`: Group name query
- `max_lat`, `min_lat`, `max_lon`, `min_lon`: Bounding box coordinates
- `enterprise_email`: Enterprise email for enterprise groups
- `offset`, `perpage`: Pagination parameters

**Response Format:**
```json
{
  "success": true,
  "data": {
    "groups": [
      {
        "id": 456,
        "creator_id": 123,
        "name": "Downtown Commuters",
        "description": "Group for daily downtown commuters",
        "avatar": "https://cdn.example.com/avatar.jpg",
        "banner": "https://cdn.example.com/banner.jpg",
        "is_private": false,
        "geofence_latitude": 25.0330,
        "geofence_longitude": 121.5654,
        "geofence_radius": 5000,
        "address": "Taipei Main Station, Taiwan",
        "enterprise_id": null,
        "enterprise": false,
        "types": [1, 2],
        "members": 25,
        "member_status": 0
      }
    ],
    "total_count": 15,
    "next_offset": 10
  }
}
```

### Member Management
**Endpoint:** `/duo_group/members`
**Methods:** GET
**Authentication:** JWT token required

#### GET - List Group Members
Lists members of a specific group.

**Required Parameters:**
- `group_id`: Group ID

**Optional Parameters:**
- `offset`, `perpage`: Pagination parameters

**Response Format:**
```json
{
  "success": true,
  "data": {
    "members": [
      {
        "user_id": 789,
        "full_name": "John Doe",
        "avatar": "https://cdn.example.com/user789.jpg",
        "rating": 4.8,
        "gender": "male",
        "pair_blacklist": false
      }
    ],
    "total_count": 25,
    "next_offset": 20,
    "security_key": "abc123..."
  }
}
```

### Member Profile
**Endpoint:** `/duo_group/member_profile`
**Methods:** GET
**Authentication:** JWT token required

#### GET - Get Member Profile
Retrieves detailed profile information for a group member.

**Required Parameters:**
- `user_id`: User ID to get profile for

**Optional Parameters:**
- `offer_id`: Related carpool offer ID
- `reservation_id`: Related reservation ID

**Response Format:**
```json
{
  "success": true,
  "data": {
    "user_id": 789,
    "full_name": "John Doe",
    "avatar": "https://cdn.example.com/user789.jpg",
    "rating": 4.8,
    "gender": "male",
    "introduction": "Experienced carpooler...",
    "linkedin_url": "https://linkedin.com/in/johndoe",
    "facebook_url": "https://facebook.com/johndoe",
    "twitter_url": "https://twitter.com/johndoe",
    "vehicle_detail": "Honda Civic 2020",
    "match_rides": 45,
    "cancel_or_noshow": 2,
    "match_with_me": 5,
    "pair_blacklist": false,
    "price": 12.50,
    "unit_price": 0.15,
    "security_key": "abc123..."
  }
}
```

### Group Administration

#### Accept User
**Endpoint:** `/duo_group/accept_user`
**Methods:** POST
**Authentication:** JWT token required (manager permissions)

Accepts a user's request to join the group.

#### Reject User
**Endpoint:** `/duo_group/reject_user`
**Methods:** POST
**Authentication:** JWT token required (manager permissions)

Rejects a user's request to join the group with optional reason.

#### Add User
**Endpoint:** `/duo_group/add_user`
**Methods:** POST
**Authentication:** JWT token required (manager permissions)

Directly adds a user to the group without request process.

#### Remove User
**Endpoint:** `/duo_group/remove_user`
**Methods:** POST
**Authentication:** JWT token required (manager permissions)

Removes a user from the group.

#### Set Admin
**Endpoint:** `/duo_group/set_admin`
**Methods:** POST
**Authentication:** JWT token required (manager permissions)

Grants administrative privileges to a group member.

### User Actions

#### Join Group
**Endpoint:** `/duo_group/join`
**Methods:** POST
**Authentication:** JWT token required

Requests to join a group or joins directly if public.

**Request Fields:**
- `group_id`: Group ID to join
- `user_description` (optional): User's introduction message

#### Leave Group
**Endpoint:** `/duo_group/leave`
**Methods:** POST
**Authentication:** JWT token required

Leaves a group with automatic management transfer if needed.

#### Cancel Join Request
**Endpoint:** `/duo_group/cancel`
**Methods:** POST
**Authentication:** JWT token required

Cancels a pending join request.

### Administrative Profiles
**Endpoint:** `/duo_group/admin_profile`
**Methods:** GET, POST
**Authentication:** JWT token required

#### POST - Update Admin Profile
Updates the administrative profile for a group manager.

**Request Fields:**
- `group_id`: Group ID
- `introduction`: Admin introduction text
- `open_contact`: Boolean for contact visibility
- `email`: Contact email
- `linkedin_url`, `facebook_url`, `twitter_url`: Social media links
- `gender`: Gender preference

#### GET - Get Admin Profile
Retrieves the administrative profile for a group.

### Suggestion Groups
**Endpoint:** `/duo_group/suggestion_group`
**Methods:** GET
**Authentication:** JWT token required

Retrieves suggested groups for the user based on preferences and location.

## Data Models

### Group Structure
```python
{
    "id": int,                          # Group identifier
    "creator_id": int,                  # Group creator user ID
    "name": str,                        # Group name (unique)
    "description": str,                 # Group description
    "avatar": str,                      # Avatar image URL
    "banner": str,                      # Banner image URL
    "is_private": bool,                 # Privacy setting
    "geofence": str,                    # WKT geofence data
    "geofence_radius": int,             # Radius in meters
    "geofence_latitude": float,         # Center latitude
    "geofence_longitude": float,        # Center longitude
    "address": str,                     # Human-readable address
    "enterprise_id": int,               # Enterprise association
    "client_id": int,                   # Client application ID
    "disabled": bool                    # Soft delete flag
}
```

### Member Structure
```python
{
    "group_id": int,                    # Group identifier
    "user_id": int,                     # User identifier
    "member_status": int,               # Member status code
    "notification_id": int              # Related notification ID
}
```

### Member Status Codes
- `0`: None (not a member)
- `1`: Regular member
- `2`: Group management/admin
- `3`: Pending approval

## Geofencing System

### Location-Based Constraints
Groups can define geographic boundaries using:
- **Center Point**: Latitude and longitude coordinates
- **Radius**: Distance in meters from center
- **Address**: Human-readable location description

### WKT (Well-Known Text) Format
Geographic data is stored using WKT Point format:
```python
from geomet import wkt
from geojson import Point

center = Point((longitude, latitude))
wkt_geofence = wkt.dumps(center, decimals=6)
```

## Enterprise Integration

### Enterprise Groups
- **Verification**: Email-based enterprise verification
- **Privacy**: Enhanced privacy controls
- **Auto-Join**: Configurable automatic joining for verified employees
- **Management**: Centralized administration features

### Enterprise Helper Integration
```python
enterprise_helper = EnterpriseHelper(ENTERPRISE_URL)
enterprise_result = enterprise_helper.get_enterprise(enterprise_email, user_id)
```

## Image Management

### Image Upload Process
1. **Base64 Decoding**: Client uploads as base64 encoded data
2. **Image Processing**: PIL (Python Imaging Library) processing
3. **Storage**: AWS S3 or local filesystem storage
4. **URL Generation**: CDN-optimized image URLs

### Supported Features
- **Avatar Images**: Square profile images for groups
- **Banner Images**: Rectangular header images
- **Format Support**: JPEG output with quality optimization
- **Error Handling**: Graceful fallback for invalid images

## Notification System

### Group Notifications
- **Join Requests**: Notifications to group managers
- **Join Responses**: Acceptance/rejection notifications
- **Group Updates**: Member notification for changes
- **Group Dissolution**: Notifications when groups are deleted

### Template Notifications
```python
push_template_notification(
    notification_type, 
    user_ids, 
    msg_data=data,
    first_name=user_name,
    group_name=group_name
)
```

## Security and Privacy

### Access Control
- **User Isolation**: Users can only access their own data
- **Manager Permissions**: Group-specific administrative rights
- **Enterprise Verification**: Email-based enterprise validation
- **Blacklist Integration**: Automatic filtering of blocked users

### Privacy Features
- **Private Groups**: Approval-required membership
- **Enterprise Groups**: Company-restricted access
- **Member Visibility**: Configurable member information display
- **Data Protection**: Minimal personal data exposure

## Performance Optimization

### Database Optimization
- **Indexed Queries**: Optimized search and filter operations
- **Pagination**: Efficient large result set handling
- **Caching**: Strategic caching of frequently accessed data
- **Connection Pooling**: Database connection optimization

### Image Optimization
- **CDN Integration**: Content delivery network for images
- **Lazy Loading**: On-demand image processing
- **Compression**: Optimized image file sizes
- **Format Standardization**: Consistent image formats

## Error Handling

### Common Error Codes
- `ERROR_DUO_GROUP_NOT_FOUND`: Group does not exist
- `ERROR_DUPLICATE_DUO_GROUP_NAME`: Group name already taken
- `ERROR_DUO_GROUP_TYPE_INVALID`: Invalid group type
- `ERROR_NO_CREATOR_PERMISSIONS`: Insufficient permissions
- `ERROR_USER_ALREADY_IN_GROUP`: User already a member
- `ERROR_ALREADY_REQUEST_JOIN_GROUP`: Duplicate join request

### Validation and Safety
- **Input Validation**: Comprehensive parameter checking
- **Image Validation**: Safe image processing with error handling
- **Geographic Validation**: Coordinate and radius validation
- **Permission Checking**: Multi-level authorization validation

## Integration Points

### Carpool Matching System
- **Group-Based Matching**: Prioritizes same-group members
- **Trust Network**: Enhanced matching within trusted groups
- **Location Filtering**: Uses group geofence for matching
- **Preference Alignment**: Group-based preference matching

### Mobile Applications
- **Group Discovery**: Location-based group recommendations
- **Real-Time Updates**: Live group activity notifications
- **Image Management**: In-app image capture and upload
- **Social Features**: Group-based social interactions

## Analytics and Monitoring

### Key Metrics
- Group creation and dissolution rates
- Member engagement and activity levels
- Geographic distribution of groups
- Enterprise adoption patterns

### Usage Tracking
```python
# App data recording for analytics
db.app_data.insert(
    user_id=user_id,
    user_action='CreateCarpoolGroup',
    lat=location_lat,
    lon=location_lon,
    gmt_time=now,
    local_time=user_local_time
)
```

## Future Enhancements

### Planned Features
- **Advanced Matching**: ML-based group recommendations
- **Event Management**: Group-based event planning
- **Gamification**: Points and rewards for active participation
- **Multi-Language**: International group support

### Scalability Improvements
- **Microservice Architecture**: Service decomposition
- **Event-Driven Processing**: Asynchronous operation handling
- **Geographic Partitioning**: Location-based data distribution
- **Real-Time Streaming**: Live group activity feeds