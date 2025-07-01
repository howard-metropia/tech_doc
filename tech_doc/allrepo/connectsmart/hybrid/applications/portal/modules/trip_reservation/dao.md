# Trip Reservation DAO Module

## Overview

The `dao.py` module defines database table schemas for the trip reservation system within the Web2py portal application. This module provides Data Access Object (DAO) definitions for managing trip reservations, carpools, user ratings, and real-time tracking functionality.

## Purpose

- **Database Schema Definition**: Provides PyDAL table definitions for trip reservation functionality
- **Data Structure Validation**: Implements field validation and constraints for reservation data
- **Relationship Management**: Defines relationships between reservations, trips, and user data
- **Carpool Support**: Specialized tables for duo/carpool reservation management

## Dependencies

```python
from pydal.objects import Table, Field
from gluon.validators import IS_LENGTH, IS_DATETIME
```

## Module Structure

### Exported Classes

The module exports seven table classes:
- `ReservationTable` - Core reservation data
- `TripTable` - Trip execution data
- `DuoReservationTable` - Carpool reservation relationships
- `TripHistoryViewTable` - Historical trip view
- `DuoRatingTable` - User rating system
- `DuoRealtimeTable` - Real-time location tracking
- `DuoTripeTable` - Trip passenger pickup/dropoff data

## Table Definitions

### ReservationTable

Defines the core reservation structure for all travel modes.

#### Key Fields

**User Information**
- `user_id` (integer, required): User making reservation
- `name` (string, 100): User name for reservation
- `role` (integer): User role (driver/passenger)
- `gender` (string, 30): Gender preference for matching

**Trip Details**
- `travel_mode` (integer, required): Transportation mode
- `status` (integer, required): Current reservation status
- `match_type` (integer): Type of matching algorithm used

**Location Data**
- `origin` (string, 200): Origin address
- `origin_name` (string, 100): Origin display name
- `origin_latitude/longitude` (double, required): Origin coordinates
- `origin_access_latitude/longitude` (double): Access point coordinates
- `destination` (string, 200): Destination address
- `destination_name` (string, 100): Destination display name
- `destination_latitude/longitude` (double, required): Destination coordinates
- `destination_access_latitude/longitude` (double): Access point coordinates

**Timing Information**
- `started_on` (datetime, required): Trip start time
- `started_off` (datetime): Departure window end
- `estimated_arrival_on/off` (datetime): Arrival time window
- `overlap_on/off` (datetime): Schedule overlap period

**Financial Data**
- `unit_price` (double): Price per unit distance
- `price` (decimal): Total trip price
- `premium` (decimal): Premium service fee
- `with_erh` (boolean): Enhanced routing/handling flag

**Additional Attributes**
- `card_id` (string, 512): Associated suggestion card
- `route_meter` (integer): Trip distance in meters
- `threshold_time` (integer): Time threshold for matching
- `carpool_uuid` (string, 50): Carpool group identifier
- `location_latitude/longitude` (double): Current location
- `local_time` (datetime): Local timezone timestamp
- `created_on/modified_on` (datetime, required): Record timestamps

### TripTable

Extends reservation data with actual trip execution information.

#### Key Features

**Trip Execution**
- `reservation_id` (reference, unique): Links to reservation
- `started_on` (datetime, required): Actual start time
- `ended_on` (datetime): Trip completion time
- `distance` (float): Actual trip distance
- `end_status` (integer, default=0): Trip completion status
- `end_type` (string, 16): Type of trip ending

**Navigation Support**
- `navigation_app` (integer, default=1): Navigation app used
- `car_navigation_system` (string, 16): In-vehicle navigation
- `occupancy` (integer, default=1): Vehicle occupancy

**Trip Validation**
- `is_calendar_event` (integer): Calendar integration flag
- `eta_valid_result` (integer): ETA validation result
- `failed_reason` (string, 128): Failure reason if applicable

**Final Destination Support**
- `final_destination_name/address` (string, 200): Ultimate destination
- `final_destination_latitude/longitude` (double): Final coordinates

### DuoReservationTable

Manages carpool (duo) reservation relationships and pricing.

#### Key Fields

**Carpool Relationships**
- `reservation_id` (reference, required): Links to base reservation
- `offer_id` (integer, required): Carpool offer identifier
- `group_id` (integer, required): Carpool group ID
- `is_creator` (boolean, required): Creator of carpool offer flag

**Financial Management**
- `price` (decimal, default=0): Carpool share price
- `with_erh` (boolean): Enhanced routing flag
- `premium` (decimal): Premium service fee
- `notification_id` (integer): Associated notification

### TripHistoryViewTable

Provides a consolidated view for trip history queries.

#### Features

**Comprehensive Trip Data**
- Combines reservation and trip completion data
- Includes all location and timing information
- Maintains financial transaction records
- Supports carpool relationship tracking

**Query Optimization**
- Denormalized structure for efficient history queries
- Includes computed fields for reporting
- Supports filtering by multiple criteria

### DuoRatingTable

Manages user rating system for carpool participants.

#### Rating System

**Rating Structure**
- `trip_id` (reference, required): Associated trip
- `ratee_id` (integer, required): User being rated
- `rating` (double, required): Numerical rating value

**Features**
- Post-trip rating collection
- Mutual rating support for carpools
- Rating aggregation for user profiles

### DuoRealtimeTable

Tracks real-time location and status during active trips.

#### Real-time Tracking

**Location Data**
- `trip_id` (reference, required): Active trip reference
- `latitude/longitude` (double): Current coordinates
- `course` (double): Travel direction/heading
- `record_on` (datetime, required): Timestamp of record

**Status Information**
- `status` (integer): Current trip status
- `estimated_arrival_time` (integer): ETA in seconds
- `passenger_id` (integer): Associated passenger for carpools

### DuoTripeTable

Manages passenger pickup and dropoff events in carpools.

#### Pickup/Dropoff Tracking

**Event Recording**
- `trip_id` (reference, required): Associated trip
- `passenger_id` (integer): Passenger being tracked
- `pick_up_time` (datetime): Actual pickup timestamp
- `pick_up_latitude/longitude` (double): Pickup coordinates
- `drop_off_time` (datetime): Actual dropoff timestamp
- `drop_off_latitude/longitude` (double): Dropoff coordinates

## Validation Framework

### Field Validation

**String Length Validation**
- Uses `IS_LENGTH()` validator for all string fields
- Prevents data truncation and ensures database compatibility

**DateTime Validation**
- `IS_DATETIME()` validator ensures proper timestamp format
- Supports timezone-aware datetime handling

**Required Field Enforcement**
- Critical fields marked as `required=True, notnull=True`
- Ensures data integrity at database level

### Data Integrity

**Referential Integrity**
- Foreign key relationships properly defined
- Cascade behaviors for related record management

**Default Values**
- Sensible defaults for optional fields
- Prevents null-related query issues

## Usage Patterns

### Table Instantiation

```python
# Example table creation
reservation_table = ReservationTable(db, 'reservation')
trip_table = TripTable(db, 'trip')
duo_reservation_table = DuoReservationTable(db, 'duo_reservation')
```

### Field Extension

```python
# Tables support field extension
custom_fields = (Field('custom_field', 'string'),)
extended_table = ReservationTable(db, 'reservation', *custom_fields)
```

## Security Considerations

### Data Protection

**Sensitive Information**
- Location data requires careful access control
- Personal information (name, gender) needs privacy protection
- Financial data (prices, premiums) requires audit trails

**Input Validation**
- All user inputs validated through PyDAL validators
- SQL injection prevention through parameterized queries
- Length limits prevent buffer overflow attacks

## Performance Optimization

### Indexing Strategy

**Primary Keys**
- Auto-incrementing integer primary keys for performance
- Unique constraints on critical business keys

**Foreign Keys**
- Proper indexing on relationship fields
- Query optimization through join strategies

**Search Fields**
- Location-based queries benefit from spatial indexing
- Timestamp fields indexed for temporal queries

## Integration Points

### Web2py Framework

**PyDAL Integration**
- Native Web2py database abstraction layer
- Automatic SQL generation and optimization
- Built-in migration support

**Validation Framework**
- Leverages Web2py's validation system
- Form integration for user interfaces
- Error handling and user feedback

### Business Logic Integration

**Service Layer**
- Tables designed for service layer abstraction
- Clean separation of data and business logic
- Support for complex business rules

## Error Handling

### Validation Errors

**Field Validation**
- Length constraint violations
- Data type mismatches
- Required field violations

**Referential Integrity**
- Foreign key constraint violations
- Orphaned record prevention
- Cascade deletion handling

## Future Enhancements

### Scalability Improvements

**Partitioning Strategy**
- Time-based partitioning for historical data
- Geographic partitioning for location queries
- User-based sharding considerations

**Performance Optimization**
- Query result caching strategies
- Read replica support for analytics
- Archive strategies for old trip data

### Functionality Extensions

**Enhanced Tracking**
- Additional real-time metrics
- Environmental data integration
- Advanced routing information

**Analytics Support**
- Data warehouse integration
- Business intelligence views
- Performance metrics collection

This DAO module provides a robust foundation for the trip reservation system, supporting complex carpool operations while maintaining data integrity and performance.