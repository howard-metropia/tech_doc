# Reservation Controller

## Overview
The Reservation Controller manages transportation service reservations within the MaaS platform, supporting multiple travel modes including carpool (DUO), public transit, driving, walking, biking, and intermodal trips. It provides comprehensive booking, updating, and cancellation capabilities with location tracking and campaign integration.

## Technical Stack
- **Framework**: Web2py with RESTful API design
- **Authentication**: JWT-based authentication
- **Database**: MySQL for reservations, MongoDB for location tracking
- **Messaging**: AWS SQS for notifications
- **Geospatial**: Location coordinate management
- **Time Handling**: UTC and timezone conversion

## Architecture

### Core Components
- **Reservation Management**: Create, update, cancel, and retrieve reservations
- **Multi-modal Support**: Different travel modes with specific handling
- **Location Services**: Origin/destination with access points
- **Carpool Integration**: Special handling for DUO mode carpooling
- **Campaign Integration**: Suggestion card and promotional features
- **Conflict Management**: Automatic conflict resolution for overlapping reservations

### Database Schema
```sql
-- Main reservation table
reservation (
  id: int,
  user_id: int,
  travel_mode: int,
  name: varchar,
  origin: text,
  origin_name: varchar,
  origin_latitude: decimal(10,8),
  origin_longitude: decimal(10,8),
  origin_access_latitude: decimal(10,8),
  origin_access_longitude: decimal(10,8),
  destination: text,
  destination_name: varchar,
  destination_latitude: decimal(10,8),
  destination_longitude: decimal(10,8),
  destination_access_latitude: decimal(10,8),
  destination_access_longitude: decimal(10,8),
  started_on: datetime,
  started_off: datetime,
  estimated_arrival_on: datetime,
  estimated_arrival_off: datetime,
  overlap_on: datetime,
  overlap_off: datetime,
  status: int,
  role: int,
  carpool_uuid: varchar,
  card_id: int,
  location_latitude: decimal(10,8),
  location_longitude: decimal(10,8),
  local_time: datetime,
  with_erh: boolean,
  premium: decimal(10,2),
  erh_available_time: datetime,
  created_on: datetime,
  modified_on: datetime
)

-- DUO carpool extensions
duo_reservation (
  id: int,
  reservation_id: int,
  offer_id: int,
  price: decimal(10,2)
)
```

## API Endpoints

### POST /api/v1/reservation/reservation
Create a new transportation reservation.

**Request Body:**
```json
{
  "travel_mode": 1,
  "name": "Work Commute",
  "origin": {
    "address": "123 Main St, San Francisco, CA",
    "name": "Home",
    "latitude": 37.7749,
    "longitude": -122.4194,
    "access_latitude": 37.7750,
    "access_longitude": -122.4195
  },
  "destination": {
    "address": "456 Market St, San Francisco, CA", 
    "name": "Office",
    "latitude": 37.7849,
    "longitude": -122.4094,
    "access_latitude": 37.7850,
    "access_longitude": -122.4095
  },
  "started_on": "2024-01-15T08:30:00Z",
  "estimated_arrival_on": "2024-01-15T09:00:00Z",
  "card_id": 123
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 456,
    "conflict_offer_ids": []
  }
}
```

### PUT /api/v1/reservation/reservation/{reservation_id}/update
Update an existing reservation.

**Request Body:**
```json
{
  "travel_mode": 2,
  "name": "Updated Trip",
  "origin": {
    "address": "789 Oak St, San Francisco, CA",
    "name": "New Home",
    "latitude": 37.7649,
    "longitude": -122.4294
  },
  "destination": {
    "address": "321 Pine St, San Francisco, CA",
    "name": "New Office", 
    "latitude": 37.7949,
    "longitude": -122.3994
  },
  "started_on": "2024-01-15T09:00:00Z",
  "estimated_arrival_on": "2024-01-15T09:30:00Z"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "conflict_offer_ids": [789]
  }
}
```

### PUT /api/v1/reservation/reservation/{reservation_id}/cancel
Cancel a reservation.

**Response:**
```json
{
  "success": true,
  "data": {
    "affected_offer_id": 123
  }
}
```

### GET /api/v1/reservation/reservation
Retrieve user's reservations with filtering and pagination.

**Query Parameters:**
```
travel_mode: [1,2,3] (optional)
offset: 0 (optional)
perpage: 10 (optional)
```

**Response:**
```json
{
  "success": true,
  "data": {
    "reservations": [
      {
        "id": 456,
        "travel_mode": 1,
        "name": "Work Commute",
        "role": 1,
        "origin": {
          "name": "Home",
          "address": "123 Main St, San Francisco, CA",
          "latitude": 37.7749,
          "longitude": -122.4194,
          "access_latitude": 37.7750,
          "access_longitude": -122.4195
        },
        "destination": {
          "name": "Office",
          "address": "456 Market St, San Francisco, CA",
          "latitude": 37.7849,
          "longitude": -122.4094,
          "access_latitude": 37.7850,
          "access_longitude": -122.4095
        },
        "started_on": "2024-01-15T08:30:00Z",
        "estimated_arrival_on": "2024-01-15T09:00:00Z",
        "status": 1,
        "offer_id": null,
        "riders": [],
        "card_id": 123
      }
    ],
    "total_count": 1,
    "next_offset": 1,
    "security_key": "user_security_key"
  }
}
```

### GET /api/v1/reservation/today
Retrieve today's reservations.

**Query Parameters:**
```
offset: 0 (optional)
perpage: 10 (optional)
```

**Response:** Similar to main reservation endpoint but filtered for today's trips.

### GET /api/v1/reservation/reservation_driver
Get driver information for a specific reservation (Admin only).

**Query Parameters:**
```
reservation_id: 123 (required)
```

**Response:**
```json
{
  "success": true,
  "data": {
    "offer_id": 789,
    "driver_id": 456,
    "id": 123,
    "role": 1,
    "price": 15.50
  }
}
```

## Travel Modes

### Supported Modes
- **DRIVING** (1): Private vehicle
- **PUBLIC_TRANSIT** (2): Bus, train, metro
- **WALKING** (3): Pedestrian
- **BIKING** (4): Bicycle
- **INTERMODAL** (5): Multi-mode combination
- **TRUCKING** (6): Commercial vehicle
- **DUO** (7): Carpool/rideshare

### Mode-Specific Features
- **DUO Mode**: Special carpool matching and pairing logic
- **Intermodal**: Combined transportation modes
- **Public Transit**: Integration with transit systems

## Reservation States

### Status Values
- **RESERVATION_STATUS_RESERVED** (1): Active reservation
- **RESERVATION_STATUS_MATCHED** (2): Paired with carpool partner
- **RESERVATION_STATUS_CANCELED** (3): Cancelled by user
- **RESERVATION_STATUS_SEARCHING** (4): Looking for carpool match

### Role Values
- **ROLE_DRIVER** (1): Carpool driver
- **ROLE_PASSENGER** (2): Carpool passenger

## Business Logic

### Conflict Management
```python
def cancel_unpaired_conflict(db, user_id, started_on, estimated_arrival_on):
    """
    Automatically cancel conflicting unpaired carpool offers
    Prevents overlapping reservations
    """
    return carpool_handler.cancel_unpaired_conflict(
        db, user_id, started_on, estimated_arrival_on
    )
```

### Location Tracking
```python
# MongoDB integration for user location
mongofields = {'user_id': user_id}
lastlatlon = list(mongo.app_state.find(mongofields).sort("timestamp", -1).limit(1))
```

### Campaign Integration
```python
# Suggestion card integration
if card_id:
    CampaignHandler.change_status(user_id, campaign_id, card_id, status, reply)
    CampaignHandler.action_card_record(user_id, campaign_id, step_no, reply_status)
```

### ERH (Emergency Ride Home) Support
```python
# Enhanced features for carpool passengers
if reservation.with_erh:
    data['with_erh'] = True
    data['premium'] = float(reservation.premium)
    data['erh_available_time'] = datetime_to_string(reservation.erh_available_time)
```

## Location Management

### Coordinate System
- **Primary Coordinates**: Main pickup/dropoff points
- **Access Coordinates**: Walking access points for transit

### Geospatial Features
- Precise latitude/longitude storage (8 decimal places)
- Access point management for intermodal trips
- Location tracking integration

## Carpool (DUO) Features

### Pairing Logic
```python
def paired_partners(db, reservation, include_profile=True, enable_unit_price=False):
    """
    Retrieve paired carpool partners with profiles and pricing
    """
    return carpool_handler.paired_partners(
        db, reservation, include_profile, enable_unit_price
    )
```

### Cancellation Handling
```python
def cancel_paired(db, reservation_id, send_message):
    """
    Cancel paired carpool reservations and notify partners
    """
    return carpool_handler.cancel_paired(db, reservation_id, send_message)
```

### Pricing Integration
- Unit pricing support for carpool rides
- Revenue sharing between driver and platform
- Dynamic pricing based on demand

## Error Handling

### Common Errors
- `ERROR_BAD_REQUEST_BODY` (400): Invalid request parameters
- `ERROR_RESERVATION_NOT_FOUND` (404): Reservation not found
- `ERROR_NO_PERMISSIONS` (403): User permission denied
- `ERROR_MODE_NOT_IN_OUR_SUPPORT` (403): Unsupported travel mode
- `ERROR_DUO_RESERVATION_NO_SUPPORT_UPDATE` (403): DUO reservations cannot be updated

### Validation Rules
- Required location coordinates
- Valid travel mode selection
- Future datetime validation
- User ownership verification

## Integration Points

### Trip Reservation Module
```python
import trip_reservation as trvel
from trip_reservation import carpool_handler
```

### Campaign System
```python
import campaign as CampaignHandler

# Status and record management
CampaignHandler.change_status(user_id, campaign_id, card_id, status, reply)
```

### SQS Messaging
```python
from sqs_helper import send_sqs_task

# Notification delivery
send_sqs_task('cloud_message', notification_data)
```

### MongoDB Integration
```python
from mongo_helper import MongoManager

# Location tracking
mongo = MongoManager.get()
```

### Date/Time Utilities
```python
from datetime_utils import string_to_datetime, utcnow_to_tz, datetime_to_string
```

## Performance Optimizations

### Database Queries
- Efficient joins with duo_reservation table
- Indexed queries by user_id and travel_mode
- Optimized pagination with limitby

### Caching Strategy
- Security key caching
- Configuration parameter caching
- Partner profile caching for carpool

## Security Features
- JWT authentication for all operations
- User isolation and permission checking
- Location data privacy protection
- Secure carpool partner matching

## Monitoring and Analytics
- Reservation creation/cancellation rates
- Travel mode usage patterns
- Carpool matching success rates
- Location tracking accuracy

## Dependencies
- `json_response`: API response formatting
- `trip_reservation`: Core reservation logic
- `campaign`: Campaign and suggestion integration
- `carpool_handler`: Carpool-specific operations
- `datetime_utils`: Date/time conversion utilities
- `sqs_helper`: AWS SQS messaging
- `mongo_helper`: MongoDB connection management