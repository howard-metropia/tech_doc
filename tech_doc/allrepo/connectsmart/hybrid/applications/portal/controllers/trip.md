# Portal Trip Controller

## Overview
Comprehensive trip management controller for the ConnectSmart Portal, handling trip lifecycle operations, carpooling coordination, telework logging, incentive calculations, and real-time trip tracking. This controller serves as the central hub for all trip-related functionality within the mobility platform.

## File Details
- **Location**: `/applications/portal/controllers/trip.py`
- **Type**: web2py Controller (Large File: ~29,485 tokens)
- **Authentication**: JWT-based authentication required
- **Dependencies**: MongoDB, trip reservation system, carpool handlers, campaign management

## Core Imports & Dependencies
```python
import logging
import json
import math
from random import random
from decimal import Decimal
from datetime_utils import string_to_datetime, datetime_to_string, datetime_to_timestamp
from mongo_helper import MongoManager
from trip_reservation import carpool_handler
import campaign as CampaignHandler
import carpool as duo
from sqs_helper import send_sqs_task, send_sqs_event
```

## Incentive System Constants
```python
INCENTIVE_NOTIFICATION_TYPE = 98
INCENTIVE_POINTS_LIMIT_PER_WEEK = 5
INCENTIVE_FIRST_TRIP = 1
INCENTIVE_NON_FIRST_TRIP = 2
INCENTIVE_TRIP_LESS_THAN_1_MILE = 3
INCENTIVE_TRIP_INVALID_TRIP = 4
INCENTIVE_REACH_THE_WEEKLY_CAP = 5

# App mapping for navigation systems
app_mapping = {
    'here': 1,
    'google': 2,
    'apple': 3,
    'waze': 4,
}
```

## Key Controller Functions

### Trip Lifecycle Management

#### `start_trip()` - POST Start Trip
Initiates trip tracking and real-time coordination.

**Endpoint**: `POST /api/v1/trip/start`

**Request Structure**:
```python
{
    "trip_id": int,
    "started_on": "ISO_datetime",
    "origin_latitude": float,
    "origin_longitude": float,
    "origin": "string",
    "car_navigation_system": int  # App mapping ID
}
```

#### `end_trip()` - POST End Trip
Completes trip tracking with incentive calculations and telework logging.

**Endpoint**: `POST /api/v1/trip/end`

**Request Structure**:
```python
{
    "trip_id": int,
    "ended_on": "ISO_datetime",
    "destination_latitude": float,
    "destination_longitude": float,
    "destination": "string",
    "distance": float,
    "valid_incentive": bool,
    "end_type": int,
    "valid_path": bool,
    "car_navigation_system": int
}
```

#### `update_trip_eta()` - POST Update ETA
Updates trip estimated time of arrival for real-time tracking.

**Endpoint**: `POST /api/v1/trip/eta`

**Request Structure**:
```python
{
    "trip_id": int,
    "estimated_arrival_on": "ISO_datetime"
}
```

### Carpooling Coordination

#### `duo_realtime()` - POST Carpooling Real-time Updates
Manages real-time carpooling status updates and coordination.

**Status Types**:
- `DUO_REALTIME_STATUS_STARTED`: Trip started
- `DUO_REALTIME_STATUS_ARRIVE_PICKUP_POINT`: Arrived at pickup
- `DUO_REALTIME_STATUS_PICKUP_MANUALLY`: Manual pickup confirmation
- `DUO_REALTIME_STATUS_DROPOFF_MANUALLY`: Manual dropoff confirmation

#### Carpooling Partner Finding
```python
def _find_paired_reservation_by_trip(trip_id):
    """Find carpooling partners for a given trip"""
    reservation_id = db(db.trip.id==int(trip_id)).select(db.trip.reservation_id).first()
    partners = db(
        (viewer.reservation_id == reservation_id) &
        (db.duo_reservation.reservation_id != viewer.reservation_id) &
        db.reservation.status.belongs([RESERVATION_STATUS_MATCHED, RESERVATION_STATUS_STARTED])
    ).select(...)
    return partners
```

### Telework Integration

#### Automatic Telework Logging
```python
def _create_duo_autolog(trip_id, now, enterprise_id, distance=None):
    """Creates automatic telework logs for enterprise users"""
    trip = db(db.trip.id == trip_id).select(db.trip.ALL).first()
    
    # Determine travel mode based on role
    if trip.role == 1:
        telework_travel_modes = "carpool_driver"
    elif trip.role == 2:
        telework_travel_modes = "carpool_rider"
    
    # Insert telework record
    db.telework.cascade_insert(
        user_id=trip.user_id,
        enterprise_id=enterprise_id,
        trip_date=trip_date,
        travel_mode=telework_travel_modes,
        # ... location and timing data
    )
```

#### Enterprise Integration
```python
def _fetch_common_enterprise_id(driver_trip_id, rider_trip_id):
    """Finds common enterprise between driver and rider"""
    common_enterprise = db(
        (db.duo_group.disabled == False) &
        (db.duo_group.enterprise_id > 0) &
        db.group_member.user_id.belongs([driver.user_id, rider.user_id])
    ).select(
        db.duo_group.enterprise_id,
        having=db.group_member.group_id.count() > 1
    ).first()
    return common_enterprise.enterprise_id if common_enterprise else 0
```

### Incentive System

#### Incentive Calculation Logic
```python
# Incentive notification titles and bodies
incentive_notification_title = {
    1: "Want more Coins?",
    2: "You've earned {}!",
    3: "Thanks for using ConnectSmart!",
    4: "Thanks for using ConnectSmart!",
    5: "Thanks for using ConnectSmart!",
}

incentive_notification_body = {
    1: "Way to go! You've earned {} for contributing to a more connected, less congested Houston...",
    2: "Keep taking trips and keep earning rewards...",
    3: "To earn rewards, trips must be longer than {}.",
    4: "We hope you enjoyed the trip.",
    5: "We hope you enjoyed the trip.",
}
```

#### Weekly Points Limit
- **INCENTIVE_POINTS_LIMIT_PER_WEEK**: 5 points maximum per week
- **Distance Requirements**: Trips must be longer than 1 mile
- **First Trip Bonus**: Special incentives for first-time users

### Financial Integration

#### Escrow Management
```python
def _normal_escrow():
    """Normal escrow process for carpooling payments"""
    # Add escrow for rider
    _id = carpool_handler.add_escrow(db, rider_id, reservation_id)
    carpool_handler.add_escrow_detail(db, rider_id, _id, ESCROW_ACTIVITY_INC_RIDER_INVITE, price)
    
    # Transfer payment to driver
    carpool_handler.transfer_carpool_fee_driver(
        db, driver_id, rider_id, trip_id, 
        api_key=configuration.get('stripe.api_key'),
        driver_transaction_fee=float(configuration.get('escrow.driver_transaction_fee', 0)),
        passenger_transaction_fee=float(configuration.get('escrow.passenger_transaction_fee', 0))
    )
```

#### Cancellation Handling
```python
def _cancel_escrow():
    """Handle escrow refund for cancelled trips"""
    carpool_handler.cancel_carpool_return_passenger(
        db, rider_id, trip_id, ESCROW_ACTIVITY_DEC_CARPOOL_CANCEL_RIDER
    )
```

## Geographic & Distance Calculations

### Distance Calculation
```python
def _calc_geodistance(lng1, lat1, lng2, lat2):
    """Calculate geodistance using Haversine formula"""
    EARTH_RADIUS = 6378.137
    radLat1 = _calc_rad(lat1)
    radLat2 = _calc_rad(lat2)
    a = radLat1 - radLat2
    b = _calc_rad(lng1) - _calc_rad(lng2)
    s = 2 * math.asin(
        math.sqrt(
            math.pow(math.sin(a / 2), 2)
            + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b / 2), 2)
        )
    )
    return s * EARTH_RADIUS * 1000  # Return in meters
```

### Workplace Verification
```python
def _verify_o_d_is_work_place(user_id, od_geo):
    """Verify if origin/destination is user's workplace"""
    work_place_info = db(
        (db.user_favorites.user_id == user_id) &
        (db.user_favorites.category == 2)  # Work category
    ).select(db.user_favorites.latitude, db.user_favorites.longitude).first()
    
    if work_place_info:
        distance_origin = _calc_geodistance(...)
        distance_destination = _calc_geodistance(...)
        return distance_origin < 100 or distance_destination < 100  # 100m threshold
```

## Real-time Tracking

### DUO Realtime Status Validation
```python
def _check_duo_realtime(driver_trip_id):
    """Validates all required carpooling statuses are completed"""
    keys = [
        DUO_REALTIME_STATUS_STARTED,
        DUO_REALTIME_STATUS_ARRIVE_PICKUP_POINT,
        DUO_REALTIME_STATUS_PICKUP_MANUALLY,
        DUO_REALTIME_STATUS_DROPOFF_MANUALLY
    ]
    
    duo_realtime = db(db.duo_realtime.trip_id == driver_trip_id).select()
    check = {key: False for key in keys}
    
    for dr in duo_realtime:
        if dr.status in keys:
            check[dr.status] = True
    
    return all(check.values())  # All statuses must be completed
```

## Data Storage Integration

### MongoDB Integration
```python
mongo = MongoManager.get()

# Telework temporary logs
def _get_telework_log_tmp(trip_id):
    """Retrieves temporary telework log data"""
    return mongo.telework_log_tmp.find_one({"id": trip_id})

# Cleanup after processing
mongo.telework_log_tmp.delete_one({'id': trip_id})
```

### Event System Integration
```python
# Send completion events
send_sqs_event([
    {
        'userIds': [trip.user_id],
        'eventName': 'carpooling',
        'eventMeta': {
            'action': 'complete_trip',
            'trip_id': trip_id,
            'role': 'driver' if trip.role == ROLE_DRIVER else 'passenger',
        },
    }
])
```

## Security & Validation

### Authentication Requirements
- **JWT Authentication**: All endpoints require valid JWT tokens
- **User Context**: Operations scoped to authenticated user
- **Role Validation**: Driver/passenger role verification

### Data Validation
- **Coordinate Validation**: GPS coordinate format and range checking
- **Timestamp Validation**: Date/time format verification
- **Distance Validation**: Reasonable distance calculations
- **Status Validation**: Valid trip status transitions

## Performance Considerations

### Database Optimization
- **Indexed Queries**: User ID and trip ID indexes
- **Join Optimization**: Efficient carpooling partner queries
- **Batch Operations**: Bulk telework log processing

### External Service Integration
- **MongoDB Connections**: Persistent connection management
- **SQS Queue Management**: Efficient event dispatching
- **Campaign System**: Optimized notification generation

## Error Handling

### Trip State Errors
- **Duplicate Operations**: Prevent duplicate start/end operations
- **Invalid Status**: Validate trip status transitions
- **Missing Data**: Handle incomplete trip information

### Financial Errors
- **Escrow Failures**: Handle payment processing errors
- **Refund Processing**: Manage cancellation refunds
- **Balance Validation**: Verify sufficient funds

## Dependencies
- **trip_reservation**: Core reservation system
- **carpool_handler**: Financial transaction management
- **CampaignHandler**: Incentive and notification system
- **MongoManager**: MongoDB connection management
- **SQS Integration**: Event and notification queuing

## Usage Examples

### Start Trip
```python
# Request
POST /api/v1/trip/start
{
    "trip_id": 12345,
    "started_on": "2023-12-01T08:00:00Z",
    "origin_latitude": 32.7767,
    "origin_longitude": -96.7970,
    "origin": "Downtown Dallas",
    "car_navigation_system": 1
}

# Response: 200 OK with trip status
```

### End Trip with Incentives
```python
# Request
POST /api/v1/trip/end
{
    "trip_id": 12345,
    "ended_on": "2023-12-01T09:00:00Z",
    "destination_latitude": 32.8998,
    "destination_longitude": -96.7578,
    "destination": "Richardson, TX",
    "distance": 15.2,
    "valid_incentive": true,
    "end_type": 1,
    "valid_path": true
}

# Response: Includes incentive calculations and telework logging
```

This controller serves as the comprehensive trip management system for the ConnectSmart mobility platform, handling everything from basic trip tracking to complex carpooling coordination, financial transactions, and enterprise telework integration.