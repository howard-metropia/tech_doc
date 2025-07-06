# Carpools Controller API Documentation

## Overview
The Carpools Controller is the core component of the MaaS platform's carpool matching system. It manages carpool reservations, intelligent matching algorithms, real-time coordination, payment processing, and user interactions for shared mobility services.

**File Path:** `/allrepo/connectsmart/hybrid/applications/portal/controllers/carpools.py`

**Controller Type:** Authenticated Portal Controller

**Authentication:** JWT token required for most endpoints

## Features
- Advanced carpool matching algorithms with multiple filtering layers
- Real-time route optimization using HERE Maps API
- Payment processing and transaction management
- User rating and feedback systems
- Geofencing and location-based matching
- Time-slot based reservation system
- Premium pricing and unit-based calculations
- Blacklist integration for user safety

## Core Matching Algorithm

### Multi-Layer Filtering System
The carpool matching uses an 8-step filtering process:

1. **Group Member Filtering**: Find users in same carpool groups
2. **Blacklist Filtering**: Remove blocked users bidirectionally
3. **Profile Filtering**: Apply gender and preference filters
4. **Role Filtering**: Match drivers with passengers and vice versa
5. **Time Filtering**: Match within acceptable time windows
6. **Location Filtering**: Filter by 50-mile radius proximity
7. **Pickup Time Filtering**: Calculate travel time to pickup location
8. **Route Optimization**: Compare carpool vs direct route times

### Geographic and Route Processing
```python
def _filter_by_route(reservation, o_lat, o_lon, d_lat, d_lon, role, threshold_time):
    # Uses HERE Maps API for route calculation
    # Compares direct route vs carpool route
    # Applies threshold_time for acceptable detour
    # Returns matched reservations with travel time data
```

## API Endpoints

### Carpool Matching
**Endpoint:** `/carpools/matching`
**Methods:** GET
**Authentication:** JWT token required

#### GET - Find Carpool Matches
Finds potential carpool matches for a reservation.

**Required Parameters:**
- `reservation_id`: ID of reservation to find matches for

**Response Format:**
```json
{
  "success": true,
  "data": {
    "match": [
      {
        "accept_time": "2024-01-15 08:00:00",
        "offers": [
          {
            "offer_id": 123,
            "role": "driver",
            "user": {
              "user_id": 456,
              "full_name": "John Doe",
              "avatar": "https://...",
              "rating": 4.8
            },
            "reservation_id": 789,
            "price": 12.50,
            "premium": 2.0
          }
        ]
      }
    ],
    "security_key": "abc123..."
  }
}
```

### Administrative Matching Statistics
**Endpoint:** `/carpools/matching_statistic`
**Methods:** POST
**Authentication:** Metropia role required

#### POST - Generate Matching Statistics
Processes matching statistics for reservations (internal API).

**Parameters:**
- `reservation_ids` (optional): Specific reservation IDs to process

**Response Format:**
```json
{
  "success": true
}
```

## Data Models

### Reservation Structure
```python
{
    "id": int,                          # Reservation ID
    "user_id": int,                     # User making reservation
    "role": str,                        # "driver" or "passenger"
    "origin_latitude": float,           # Start location lat
    "origin_longitude": float,          # Start location lon
    "destination_latitude": float,      # End location lat
    "destination_longitude": float,     # End location lon
    "started_on": datetime,             # Departure time
    "started_off": datetime,            # Arrival time
    "status": str,                      # Reservation status
    "price": decimal,                   # Base price
    "unit_price": decimal,              # Per-mile/minute price
    "route_meter": int,                 # Route distance in meters
    "threshold_time": int,              # Acceptable detour time
    "gender": str                       # Gender preference
}
```

### Match Statistics Structure
```python
{
    "reservation_id": int,              # Source reservation
    "match_reservation_id": int,        # Matched reservation
    "time_to_pickup": int,              # Travel time to pickup (seconds)
    "time_to_dropoff": int,             # Travel time to dropoff (seconds)
    "created_on": datetime,             # Record creation time
    "modified_on": datetime             # Last modification time
}
```

## Matching Algorithm Details

### Geographic Filtering
```python
def _filter_by_location(reservation, o_lat, o_lon, d_lat, d_lon):
    # Uses Vincenty formula for accurate distance calculation
    # Filters reservations within 50-mile radius
    # Returns matched and unmatched reservations
```

### Time Window Matching
```python
def _filter_by_time(reservation, accept_times, role):
    # Matches departure/arrival times with 3-hour flexibility
    # Handles driver-passenger time coordination
    # Returns reservations within acceptable time slots
```

### Route Optimization
The system uses HERE Maps API for:
- Direct route calculation between origin and destination
- Multi-waypoint carpool route calculation
- Travel time estimation with real-time traffic
- Threshold-based detour acceptance

## Payment Integration

### Price Calculation
```python
def calculate_total_price_by_unit_price(owner, target, enable_unit_price):
    # Calculates total cost based on route distance and time
    # Applies unit pricing for fair cost distribution
    # Handles transaction fees for drivers and passengers
```

### Transaction Fees
- **Passenger Fee**: Added to total cost
- **Driver Fee**: Deducted from earnings (minimum protection)
- **Premium Charges**: Enhanced route optimization fee

## Database Schema

### Core Tables
- **reservation**: Carpool reservation details
- **match_statistic**: Matching history and statistics
- **blacklist**: User blocking relationships
- **group_member**: Carpool group memberships

### Indexes and Performance
```sql
-- Optimized queries for matching
CREATE INDEX idx_reservation_search ON reservation (status, role, started_off);
CREATE INDEX idx_reservation_location ON reservation (origin_latitude, origin_longitude);
CREATE INDEX idx_match_statistic_lookup ON match_statistic (reservation_id, match_reservation_id);
```

## External Service Integration

### HERE Maps API
- Route calculation and optimization
- Real-time traffic data
- Multi-waypoint routing
- Distance and duration estimation

### MongoDB Integration
- User location state tracking
- Real-time position updates
- Historical trip data storage

### SQS Event Processing
- Asynchronous match processing
- Event-driven notifications
- System decoupling and scalability

## Carpool Group Integration

### Group-Based Matching
```python
def get_same_group_user(db, user_id):
    # Finds users in same carpool groups
    # Applies group membership status filters
    # Returns eligible matching candidates
```

### Enterprise Groups
- Corporate carpool programs
- Verified member matching
- Enhanced safety and trust features

## Real-Time Features

### Live Matching Updates
- Dynamic re-matching as conditions change
- Real-time availability updates
- Instant notification delivery

### Location Tracking
- GPS-based position updates
- ETA calculations and updates
- Route deviation detection

## Security and Privacy

### User Safety Features
- Bidirectional blacklist filtering
- Profile-based matching preferences
- Group-verified member prioritization
- Rating and feedback systems

### Data Protection
- User location data encryption
- Secure payment processing
- Privacy-compliant data handling

## Performance Optimization

### Caching Strategy
- Frequent route calculation caching
- User profile data caching
- Geographic boundary pre-calculation

### Algorithmic Efficiency
- Multi-threaded matching processing
- Efficient geometric calculations
- Database query optimization

## Error Handling

### API Error Responses
```json
{
  "success": false,
  "error_code": "ERROR_BAD_REQUEST_PARAMS",
  "message": "Invalid parameters"
}
```

### Matching Failure Recovery
- Graceful degradation for API failures
- Fallback matching algorithms
- Error logging and monitoring

## Usage Examples

### Find Carpool Matches
```bash
curl -X GET "/carpools/matching?reservation_id=123" \
  -H "Authorization: Bearer <jwt_token>"
```

### Process Matching Statistics
```bash
curl -X POST "/carpools/matching_statistic" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"reservation_ids": [123, 456, 789]}'
```

## Integration Points

### Mobile Applications
- Real-time match notifications
- Route visualization and tracking
- In-app payment processing
- User feedback and rating systems

### Analytics Platform
- Matching success rates
- Route optimization metrics
- User behavior analysis
- Platform performance monitoring

### Payment System
- Dynamic pricing calculations
- Transaction fee processing
- Refund and dispute handling
- Financial reporting integration

## Monitoring and Analytics

### Key Metrics
- Match success rates by geographic area
- Average matching time
- Route optimization savings
- User satisfaction scores

### Performance Monitoring
- API response times
- HERE Maps API quota usage
- Database query performance
- Matching algorithm efficiency

## Troubleshooting

### Common Issues
1. **No Matches Found**: Check time windows and location radius
2. **HERE API Failures**: Implement fallback routing
3. **Price Calculation Errors**: Validate unit pricing configuration
4. **Blacklist Issues**: Verify bidirectional filtering logic

### Debug Logging
- Detailed matching step logging
- API request/response tracking
- Performance timing measurements
- Error context preservation

## Future Enhancements

### Planned Features
- Machine learning-based match prediction
- Advanced route optimization algorithms
- Multi-modal transportation integration
- Enhanced enterprise features

### Scalability Considerations
- Microservice architecture migration
- Event-driven processing expansion
- Geographic partitioning strategies
- Real-time streaming data processing