# Prediction Agent Controller

## Overview
The Prediction Agent Controller implements intelligent location prediction services for the MaaS platform, utilizing machine learning algorithms to anticipate user travel patterns and destinations based on historical trip data and real-time context.

## Technical Stack
- **Framework**: Web2py with RESTful API design
- **Authentication**: JWT-based authentication
- **Database**: MongoDB for trip clustering, MySQL for cluster references
- **Geospatial**: GeoPy for distance calculations
- **Time Handling**: Pytz for timezone management
- **ML Integration**: Trip clustering and pattern recognition

## Architecture

### Core Components
- **Location Matching**: GPS-based location clustering and matching
- **Temporal Analysis**: Time-based pattern recognition
- **Destination Prediction**: ML-driven destination forecasting
- **Pattern Recognition**: Habitual travel behavior analysis

### Data Flow
```
User Location → Cluster Matching → Time Analysis → Pattern Recognition → Prediction Results
```

### Database Schema
```sql
-- MySQL cluster reference table
cm_cluster_id (id, cluster_id)

-- MongoDB collections
cluster_trips: {
  _id: ObjectId,
  user_id: int,
  common_start_location: { coordinates: [lon, lat] },
  common_end_location: { coordinates: [lon, lat] },
  common_destination_name: string,
  common_destination_address: string,
  departure_time_range: { earliest: time, latest: time },
  15th_percentile_time: { time: time },
  85th_percentile_time: { time: time },
  day_of_week: int
}
```

## API Endpoints

### GET /api/v1/prediction_agent/location
Predict likely destinations based on current location and context.

**Query Parameters:**
```
lat: 37.7749 (required)
lon: -122.4194 (required)
timestamp: 1640995200 (optional, defaults to current time)
```

**Response:**
```json
{
  "success": true,
  "data": {
    "prediction_locations": [
      {
        "id": 123,
        "name": "Downtown Office",
        "address": "123 Market St, San Francisco, CA",
        "latitude": 37.7849,
        "longitude": -122.4094,
        "origin_id": 123,
        "local_departure_time": "08:30",
        "default_mode": 1,
        "loc_type": 1
      }
    ]
  }
}
```

### PATCH /api/v1/prediction_agent/location/{location_id}
Update prediction location preferences.

**Request Body:**
```json
{
  "name": "Updated Location Name",
  "address": "New Address"
}
```

### DELETE /api/v1/prediction_agent/location/{location_id}
Remove a prediction location from user's profile.

## Core Algorithms

### Location Clustering
```python
def match_locations(user_id, lat, lon, eps_in_km):
    """
    Find clustered locations within epsilon distance
    Uses geospatial queries on MongoDB cluster_trips collection
    """
    # Query MongoDB for user's trip clusters
    # Calculate great circle distance for each cluster
    # Return matches within epsilon threshold (default 0.2km)
```

### Time Slot Analysis
```python
def datetimetoslot(local_datetime):
    """Convert datetime to 15-minute time slots"""
    return (local_datetime.hour * 60 + local_datetime.minute) // SLOT_MINUTE

SLOT_MINUTE = 15  # 15-minute time slots
ONEDAY_MINUTE = 1440  # Total minutes in a day
SLOT_RANGE = 96  # Total 15-minute slots per day
```

### Temporal Pattern Matching
```python
def check_time_in_range(start_time, end_time):
    """
    Check if current time falls within historical departure window
    Includes 60-minute buffer before start time
    """
    # Convert time strings to datetime objects
    # Apply timezone localization
    # Check current time against departure window
```

### Prediction Engine
```python
def predictive(user, timestamp, lat, lon):
    """
    Main prediction algorithm combining:
    1. Location clustering (0.2km radius)
    2. Day-of-week matching (weekday vs weekend)
    3. Time window analysis (15th-85th percentile)
    4. Historical pattern validation
    """
```

## Business Logic

### Day Classification
- **WEEKDAY** (1): Monday through Friday
- **WEEKEND** (2): Saturday and Sunday
- Affects prediction accuracy and pattern matching

### Time Window Analysis
- **15th Percentile**: Earliest typical departure time
- **85th Percentile**: Latest typical departure time
- **Buffer Time**: 60 minutes before earliest departure
- **Fallback**: Absolute earliest/latest if percentiles unavailable

### Distance Thresholds
- **Location Matching**: 200 meters (0.2km) radius
- **Great Circle Distance**: Accurate geospatial calculations
- **Cluster Validation**: Minimum trip count requirements

## Machine Learning Integration

### Trip Clustering Features
- Start/end location coordinates
- Departure time patterns
- Day of week preferences
- Trip frequency analysis

### Pattern Recognition
- Habitual behavior identification
- Temporal consistency scoring
- Location affinity mapping
- Prediction confidence levels

## Error Handling

### Common Errors
- `ERROR_BAD_REQUEST_PARAMS` (400): Invalid location parameters
- Location not found: Empty prediction results
- Invalid coordinates: Validation failures

### Validation
- Latitude/longitude range checking
- User ID verification
- Timestamp format validation
- Location access permissions

## Performance Optimizations

### Database Efficiency
- MongoDB geospatial indexing
- Efficient cluster queries
- Cached distance calculations
- Optimized time range queries

### Algorithm Optimization
- Pre-computed time slots
- Cached cluster references
- Efficient pattern matching
- Lazy loading of prediction data

## Integration Points

### MongoDB Integration
```python
from mongo_helper import MongoManager

mongo = MongoManager.get()
data = list(mongo.cluster_trips.find(mongofields))
```

### Geospatial Calculations
```python
from geopy.distance import great_circle

distance = great_circle((lat1, lon1), (lat2, lon2)).m
```

### Timezone Handling
```python
import pytz

tz = pytz.timezone(request.env.http_zone)
local_datetime = utc_datetime.astimezone(tz)
```

## Configuration Parameters
- `eps_in_km`: Location matching radius (default: 0.2km)
- `SLOT_MINUTE`: Time slot duration (15 minutes)
- `TRAVEL_TIME_LIMIT`: Minimum travel time threshold
- Timezone configuration from request environment

## Security Features
- JWT authentication for all prediction requests
- User-specific data isolation
- Location data privacy protection
- Access control for prediction updates

## Monitoring and Analytics
- Prediction accuracy tracking
- Location cluster analysis
- Time pattern validation
- User behavior insights

## Dependencies
- `mongo_helper`: MongoDB connection management
- `geopy`: Geospatial distance calculations
- `pytz`: Timezone handling
- `json_response`: API response formatting
- `auth`: User authentication system