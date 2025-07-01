# Portal Trace Controller

## Overview
Handles location tracking, trip trajectory collection, app state monitoring, and user Origin-Destination-Time-Mode (UODTM) data processing for the ConnectSmart mobility platform. This controller manages comprehensive movement analytics and campaign management integration.

## File Details
- **Location**: `/applications/portal/controllers/trace.py`
- **Type**: web2py Controller
- **Authentication**: JWT-based authentication required
- **Dependencies**: MongoDB, S3, SQS, Campaign Manager, Geo-services

## Core Functions

### `trip_trajectory()` - POST Trip Trajectory Data
Collects detailed trip trajectory data including GPS coordinates, speed, and travel mode information.

#### Endpoint
```
POST /api/v1/trace/trip_trajectory
```

#### Content Types Supported
- `application/json` - Standard JSON payload
- `application/zip` - Compressed trajectory data
- `application/gzip` - GZIP compressed data

#### Request Structure
```python
{
    "mode": "driving|public_transit|walking|biking|duo|intermodal|trucking",
    "trip_id": int,
    "trajectory": [
        {
            "latitude": float,     # GPS latitude (-90 to 90)
            "longitude": float,    # GPS longitude (-180 to 180)
            "altitude": float,     # Elevation in meters
            "course": float,       # Direction in degrees
            "speed": float,        # Speed in units/second
            "accuracy": float,     # GPS accuracy in meters
            "timestamp": int       # Unix timestamp
        }
    ],
    "mode_detail": "string"   # Required for intermodal trips
}
```

#### Data Validation
```python
# Mode validation
mode_options = ['driving', 'public_transit', 'walking', 'biking', 'duo', 'intermodal', 'trucking']

# Intermodal mode detail validation
if fields['mode'] == 'intermodal':
    mode_detail_options = ['driving', 'public']
    if fields['mode_detail'] not in mode_detail_options:
        return error_response
```

#### Storage Process
1. **User Attribution**: Adds user_id to trajectory data
2. **Timestamp Addition**: Records submission timestamp
3. **MongoDB Storage**: Stores complete trajectory in MongoDB
4. **S3 Backup**: Optional S3 storage for large datasets

### `app_state()` - POST Application State Tracking
Monitors application UI state changes and user location context.

#### Endpoint
```
POST /api/v1/trace/app_state
```

#### Request Structure
```python
{
    "previous_state": int,  # Previous UI state ID
    "current_state": int,   # Current UI state ID
    "latitude": float,      # Current location latitude
    "longitude": float      # Current location longitude
}
```

#### Business Logic
1. **Location Processing**: Reverse geocoding for city identification
2. **Distance Calculation**: Vincenty distance for location changes
3. **City Update**: Updates user's current city if moved >30km
4. **Campaign Triggers**: Triggers card resend for specific states

```python
# Distance-based city update
if distance is None or distance > 30000:
    geodata = revgeocode(fields['latitude'], fields['longitude'])
    city = geodata['address']['county']

# Campaign card resend trigger
if fields['current_state'] == 4:
    resend = CampaignHandler.resend_card(auth.user.id, resend_duration)
```

### `user_visit()` - POST User Visit Tracking
Records user visit patterns and location dwell times.

#### Endpoint
```
POST /api/v1/trace/user_visit
```

#### Request Structure
```python
{
    "latitude": float,        # Visit location latitude
    "longitude": float,       # Visit location longitude
    "arrival_date": int,      # Unix timestamp of arrival
    "departure_date": int,    # Unix timestamp of departure
    "os_type": "string"      # Operating system type
}
```

### `uodtm()` - POST Origin-Destination-Time-Mode Analysis
Processes UODTM data for campaign management and predictive analytics.

#### Endpoint
```
POST /api/v1/trace/uodtm
```

#### Request Structure
```python
{
    "o_id": int,           # Origin location ID
    "d_id": int,           # Destination location ID
    "departure_time": int, # Planned departure timestamp
    "mode": int           # Transportation mode ID
}
```

#### Campaign Integration Logic
1. **Time Range Generation**: Creates departure time windows
2. **Campaign Matching**: Finds active campaigns for UODTM pattern
3. **Card Generation**: Creates notification cards for matched campaigns
4. **Point Calculation**: Calculates reward points for actions

```python
# Time window generation
timeRange = CampaignHandler.uodtsGenerator(depTime)
fromTime = timeRange[0]
toTime = timeRange[1]

# Campaign matching query
sql = (db.cm_campaign_user.user_id == userId) & \
      (db.cm_campaign_user.o_id == fields['o_id']) & \
      (db.cm_campaign_user.d_id == fields['d_id']) & \
      (db.cm_campaign_user.travel_mode == fields['mode'])
```

#### Campaign Card Types
- **Type 3**: GO_LATER - Suggests departure time delay
- **Type 4**: CHANGE_MODE - Suggests alternative transportation
- **Type 7**: WTA_GO_LATER - WTA-specific departure delay
- **Type 9**: WTA_CHANGE_MODE - WTA-specific mode change

### `log_here()` - POST HERE Maps Log Upload
Handles HERE Maps SDK log uploads for debugging and analytics.

#### Endpoint
```
POST /api/v1/trace/log_here/{filename}
```

#### Features
- **Compressed Upload**: Supports ZIP compression
- **S3 Storage**: Direct upload to S3 bucket
- **Debugging Support**: Maintains HERE Maps integration logs

## Utility Functions

### Geographic Processing
```python
def revgeocode(lat, lng):
    """Reverse geocoding using HERE Maps API"""
    params = {
        'at': str(lat)+','+str(lng),
        'lang': 'en-US',
        'apiKey': configuration.get('here.app_key'),
    }
    # Returns location details with county/city information
```

### Coordinate Validation
```python
def _check_lat(lat):
    """Validates latitude format (6 decimal places max)"""
    return re.search(r'^(\-|\+)?([0-8]?\d{1}\.\d{0,6}|90\.0{0,6}|[0-8]?\d{1}|90)$', str(lat))

def _check_lon(lon):
    """Validates longitude format (6 decimal places max)"""
    return re.search(r'^(\-|\+)?(((\d|[1-9]\d|1[0-7]\d|0{1,3})\.\d{0,6})|(\d|[1-9]\d|1[0-7]\d|0{1,3})|180\.0{0,6}|180)$', str(lon))
```

### Cluster Data Integration
```python
def cluster_trip_id(tid):
    """Maps trip ID to cluster ID"""
    toid = db(db.cm_cluster_id.id == tid).select(db.cm_cluster_id.cluster_id).first()
    return toid.cluster_id if toid.cluster_id else None

def get_cluster(toid):
    """Retrieves cluster trip data from MongoDB"""
    mongo = MongoManager.get()
    obj_id = ObjectId(toid)
    return mongo.cluster_trips.find_one({'_id': obj_id})
```

## Data Storage Architecture

### MongoDB Collections
- **trip_trajectory**: GPS trajectory data with metadata
- **app_state**: Application state transitions
- **user_visit**: Location visit patterns
- **cluster_trips**: Clustered trip pattern data

### S3 Storage Structure
```python
# Trip trajectory files
'trip_trajectory/trip_{trip_id}_{mode}_{mode_detail}.json'

# HERE Maps logs
'log/here/{filename}'
```

### Database Tables
- **user_visit**: Current user location cache
- **cm_campaign_user**: Campaign participation tracking
- **verify_predicted_location**: UODTM prediction verification

## Campaign Integration

### Card Generation Process
1. **Campaign Matching**: Find active campaigns for UODTM pattern
2. **Card Type Determination**: Select appropriate intervention type
3. **Point Calculation**: Calculate reward points
4. **Notification Creation**: Generate push notification payload
5. **SQS Dispatch**: Queue notification for delivery

### Notification Structure
```python
nextCardData = {
    "silent": False,
    "user_list": [userId],
    "notification_type": typeId,
    "ended_on": end_time,
    "title": title,
    "body": body,
    "meta": {
        "action": {
            "current_mode": int,
            "o_id": int,
            "d_id": int,
            "departure_time": int
        },
        "points": float,
        "card_id": string
    }
}
```

## Security & Validation

### Input Validation
- **Coordinate Bounds**: Latitude/longitude range validation
- **Mode Verification**: Transportation mode whitelist
- **Timestamp Validation**: Unix timestamp format verification
- **Required Fields**: Comprehensive field presence checking

### Authentication
- **JWT Tokens**: All endpoints require valid JWT authentication
- **User Context**: All data attributed to authenticated user
- **Rate Limiting**: Protection against trajectory data flooding

## Performance Considerations

### Data Compression
- **GZIP Support**: Compressed trajectory upload support
- **ZIP Processing**: Batch trajectory data handling
- **S3 Optimization**: Direct cloud storage for large datasets

### Query Optimization
- **MongoDB Indexing**: User ID and timestamp indexes
- **Campaign Caching**: Active campaign data caching
- **Location Caching**: Recent location data caching

## Dependencies
- **MongoDB**: Trajectory and app state storage
- **AWS S3**: Large file and log storage
- **AWS SQS**: Notification queue management
- **HERE Maps API**: Reverse geocoding services
- **Campaign Handler**: Notification card generation
- **Geopy**: Distance calculations

## Usage Examples

### Upload Trip Trajectory
```python
# Request
POST /api/v1/trace/trip_trajectory
{
    "mode": "driving",
    "trip_id": 12345,
    "trajectory": [
        {
            "latitude": 32.32961,
            "longitude": -111.04619,
            "altitude": 2113,
            "course": 178,
            "speed": 30.3,
            "accuracy": 54,
            "timestamp": 1539711000
        }
    ]
}

# Response: 200 OK
```

### Submit UODTM Data
```python
# Request
POST /api/v1/trace/uodtm
{
    "o_id": 23,
    "d_id": 45,
    "departure_time": 1539711000,
    "mode": 2
}

# Response: Campaign card if matched
{
    "status": "success",
    "data": {
        "notification_type": 4,
        "title": "Consider Transit",
        "body": "Save time and money!",
        "meta": {
            "action": {
                "suggested_mode": 3,
                "points": 5.0
            }
        }
    }
}
```

This controller provides comprehensive location tracking and analytics capabilities, enabling intelligent transportation recommendations and campaign management within the ConnectSmart mobility platform.