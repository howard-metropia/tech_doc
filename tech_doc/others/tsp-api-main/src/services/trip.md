# TSP API Trip Service Documentation

## 🔍 Quick Summary (TL;DR)
The Trip service provides comprehensive trip management functionality including trip lifecycle operations, validation systems, auto-logging, status tracking, and reward calculations with support for carpool, ridehail, transit, and multimodal travel modes across multiple enterprise integrations.

**Keywords:** trip-management | lifecycle-operations | validation-system | auto-logging | status-tracking | reward-calculations | multimodal-travel | enterprise-integration

**Primary use cases:** Managing trip start/end operations, validating trip completion, calculating trip rewards, tracking trip status across multiple travel modes, handling carpool coordination

**Compatibility:** Node.js >= 16.0.0, MySQL database with complex joins, MongoDB for route storage, moment.js for timezone handling, enterprise system integration

## ❓ Common Questions Quick Index
- **Q: What travel modes are supported?** → Carpool, ridehail, transit, instant carpool, biking, walking, driving, multimodal combinations
- **Q: How is trip validation handled?** → Automated validation system with timer-based checking, geographic verification, and manual override capabilities
- **Q: What rewards are calculated?** → Trip completion rewards, suggestion card rewards, green statistics (CO2 saved, money saved, distance not driven)
- **Q: How are carpool trips coordinated?** → Dual validation for driver/passenger pairs, real-time status tracking, automatic payment processing
- **Q: What enterprise features exist?** → Enterprise-specific logging, group membership validation, workplace detection, organization-based rewards
- **Q: How are trip statuses managed?** → Complex status logic covering completed, canceled (driver/rider/system), validated, payment processing states

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **comprehensive trip coordinator** that manages every aspect of a user's journey from start to finish. It tracks when you begin a trip, monitors your progress, verifies you actually completed it, calculates rewards for sustainable travel choices, handles payments for shared rides, and maintains detailed records for personal and business use.

**Technical explanation:** 
A sophisticated trip management system that orchestrates the complete trip lifecycle through status management, validation algorithms, reward calculation engines, enterprise integration capabilities, multi-modal travel support, and real-time coordination systems with database transaction management and timer-based automation.

**Business value explanation:**
Enables comprehensive mobility tracking for individuals and organizations, supports sustainable transportation incentives through reward systems, facilitates carpool coordination and payment processing, provides detailed analytics for transportation behavior, and integrates with enterprise systems for business travel management.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/trip.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with complex ORM relationships and timer management
- **Type:** Comprehensive Trip Lifecycle Management Service
- **File Size:** ~33+ KB (Very Large)
- **Complexity Score:** ⭐⭐⭐⭐⭐ (Very High - Complex state management and multi-system integration)

**Dependencies:**
- Multiple Models: Trips, Reservations, TeleworkLogs, UserFavorites, DuoGroups, etc. (**Critical**)
- `moment-timezone`: Complex timezone and date calculations (**Critical**)
- `@app/src/services/carpoolHandler`: Carpool coordination and payments (**High**)
- `@app/src/services/wallet`: Points and wallet transaction management (**High**)
- `@app/src/services/incentive`: Reward calculation system (**High**)

## 📝 Detailed Code Analysis

### Trip Status Management System

### getTripStatus Function
**Purpose:** Retrieves current validation status for trip based on role (driver/passenger)

```javascript
async function getTripStatus(tripId) {
  logger.info(`[getTripStatus] enter, tripId: ${tripId}`);
  try {
    const trip = await Trips.query().findOne({ id: tripId });
    if (trip) {
      let whereCond = {};
      switch (trip.role) {
        case 1: // Driver
          whereCond = {
            driver_trip_id: tripId,
          };
          break;
        case 2: // Passenger
          whereCond = {
            passenger_trip_id: tripId,
          };
          break;
      }
      const status = await DuoValidatedResult.query().findOne(whereCond);
      return status;
    } else {
      return null;
    }
  } catch (e) {
    logger.warn(`[getTripStatus] error: ${e.message}`);
    throw e;
  }
}
```

**Status Management Features:**
- **Role-Based Queries:** Different query logic for drivers vs passengers
- **Validation Integration:** Links to DuoValidatedResult for validation status
- **Error Handling:** Comprehensive error logging and propagation
- **Null Safety:** Graceful handling of non-existent trips

### Trip Status Setting and Payment Processing

### setTripStatus Function
**Purpose:** Updates trip payment status and triggers carpool fee transfers when approved

```javascript
async function setTripStatus(tripId, status, reason = '') {
  logger.info(
    `[setTripStatus] enter, tripId: ${tripId}, status: ${status}, reason: ${reason}`,
  );
  
  const trip = await Trips.query().findOne({ id: tripId });
  if (trip) {
    let whereCond = {};
    switch (trip.role) {
      case 1:
        whereCond = { driver_trip_id: tripId };
        break;
      case 2:
        whereCond = { passenger_trip_id: tripId };
        break;
    }
    
    const dvr = await DuoValidatedResult.query().where(whereCond).first();
    
    if (dvr) {
      // Update existing validation result
      await DuoValidatedResult.query().where(whereCond).patch({
        payment_status: status,
        reason,
      });
    } else {
      // Create new validation result for duo trip
      const duoTrip = await knex('trip as owner_trip')
        .join('duo_reservation as owner_duo', function () {
          this.on('owner_duo.reservation_id', '=', 'owner_trip.reservation_id');
        })
        .join('duo_reservation as partner_duo', function () {
          this.on('partner_duo.offer_id', '=', 'owner_duo.offer_id')
              .on('partner_duo.reservation_id', '<>', 'owner_duo.reservation_id');
        })
        .join('trip as partner_trip', function () {
          this.on('partner_trip.reservation_id', '=', 'partner_duo.reservation_id');
        })
        .where('owner_trip.id', '=', tripId)
        .select(
          'partner_trip.id as partner_trip_id',
          'partner_trip.role as partner_role',
          'owner_trip.id as owner_trip_id',
          'owner_trip.role as owner_role',
        )
        .first();

      if (duoTrip) {
        let driverTripId = 0;
        let passengerTripId = 0;
        if (Number(duoTrip.owner_role) === 1) {
          driverTripId = tripId;
          passengerTripId = Number(duoTrip.partner_trip_id);
        } else {
          driverTripId = Number(duoTrip.partner_trip_id);
          passengerTripId = tripId;
        }
        
        await knex('duo_validated_result').insert({
          score: 0,
          passed: 0,
          validation_status: 0,
          payment_status: status,
          reason,
          driver_trip_id: driverTripId,
          passenger_trip_id: passengerTripId,
        });
      }
    }

    // Process payment when status is approved
    if (status === 1) {
      // Extract driver and passenger IDs
      // Trigger carpool fee transfer
      const pay = await carpoolHandler.transferCarpoolFeeDriver(
        driverId,
        passengerId,
        tripId,
      );
    }
  }
}
```

**Payment Processing Features:**
- **Complex Join Queries:** Multi-table joins to identify carpool partnerships
- **Role Determination:** Automatic driver/passenger role identification
- **Payment Triggering:** Automatic fee transfer on approval (status = 1)
- **Validation Record Management:** Creates or updates validation results

### Trip Lifecycle Management

### startTrip Function
**Purpose:** Initiates trip with validation timer setup and real-time coordination

```javascript
const startTrip = async (userId, input, tripLogs, zone) => {
  try {
    const startedOn = new Date();
    // Create trip record
    const [_id] = await knex('trip').insert({
      user_id: userId,
      travel_mode: input.travel_mode,
      origin: input.origin,
      destination: input.destination,
      distance: input.distance,
      started_on: startedOn,
      estimated_arrival_on: input.estimated_arrival_on,
      // ... other fields
    });

    // Handle different travel modes
    let replyStatus = TRIP_STATUS.started;
    
    switch (input.travel_mode) {
      case TRAVEL_MODE.carpool:
        // Handle carpool-specific logic
        break;
      case TRAVEL_MODE.ridehail:
        // Handle ridehail-specific logic
        break;
      case TRAVEL_MODE.transit:
        // Handle transit-specific logic
        break;
    }

    // Set up validation timer (non-blocking)
    if (input.estimated_arrival_on && input.route) {
      setImmediate(async () => {
        try {
          // Store route information
          const route = input.route
            ? typeof input.route === 'string'
              ? input.route
              : JSON.stringify(input.route)
            : '';
          await TripRoutes.query().insert({
            trip_id: _id,
            route,
            estimated_arrival_on: input.estimated_arrival_on,
          });

          // Set validation timer
          const estimatedArrivalTime = moment
            .utc(input.estimated_arrival_on)
            .unix();
          const now = Date.now();
          const timeout = (estimatedArrivalTime - Math.floor(now / 1000)) * 1000;
          
          const timerId = setTimeout(async () => {
            await validateTrip(_id);
          }, timeout);

          // Store timer reference
          await TripValidationQueue.query().insert({
            trip_id: _id,
            run_at: estimatedArrivalTime * 1000,
            timer_id: timerId[Symbol.toPrimitive](),
          });
          
          logger.info(
            `[startTrip] trip validation timer set for trip: ${_id}, ETA: ${input.estimated_arrival_on}`,
          );
        } catch (error) {
          logger.error(
            `[startTrip] error setting validation timer: ${error.message}`,
          );
        }
      });
    }

    return { id: _id };
  } catch (e) {
    logger.error(`[startTrip] error: ${e.message}`);
    throw e;
  }
};
```

**Trip Startup Features:**
- **Multi-Modal Support:** Different logic paths for various travel modes
- **Timer-Based Validation:** Automatic validation scheduling based on ETA
- **Route Storage:** Comprehensive route data storage for validation
- **Non-Blocking Operations:** Performance optimization with setImmediate
- **Error Recovery:** Comprehensive error handling and logging

### Trip Validation System

### Auto-Logging and Duo Trip Creation
```javascript
const createDuoAutolog = async (
  trip_id,
  now,
  enterprise_id,
  distance = null,
  zone = 'America/Chicago',
) => {
  const trip = await Trips.query().findById(trip_id);
  logger.info(
    `[create_duo_autolog] trip ${trip.id} role ${trip.role} user id: ${trip.user_id}`,
  );
  
  // Check if telework log already exists
  const telework = await Teleworks.query().where('trip_id', trip.id).first();
  if (telework) {
    logger.info(
      `[create_duo_autolog] skip, when trip log id: ${telework.id}, trip id: ${telework.trip_id} is already exist.`,
    );
    return;
  }
  
  // Get temporary trip data
  const telework_log_tmp = await TeleworkLogTmps.findOne({ id: trip_id });
  if (telework_log_tmp) {
    const origin_name = telework_log_tmp.origin_name;
    const origin_address = telework_log_tmp.origin_address;
    const started_on = telework_log_tmp.started_on;
    const destination_name = telework_log_tmp.destination_name ?? trip.destination;
    const destination_address = telework_log_tmp.destination_address ?? trip.destination;
    const trip_date = moment(trip.started_on).tz(zone).format('YYYY-MM-DD');
    const telework_travel_modes = trip.role === ROLE.DRIVER ? 'carpool_driver' : 'carpool_rider';
    
    // Verify workplace detection
    const is_work_place = await _verify_o_d_is_work_place(trip.user_id, {
      origin_longitude: telework_log_tmp.origin_lng,
      origin_latitude: telework_log_tmp.origin_lat,
      destination_longitude: telework_log_tmp.destination_lng,
      destination_latitude: telework_log_tmp.destination_lat,
    });

    // Create telework log entry
    const data = {
      user_id: trip.user_id,
      is_autolog: 1,
      enterprise_id,
      trip_date,
      trip_id: trip.id,
      started_on,
      ended_on: now,
      is_round_trip: 'F',
      is_recurring_trip: 'F',
      origin_telework_id: 0,
      is_work_place: is_work_place ? 'T' : 'F',
    };
    
    const [telework_id] = await knex('telework').insert(data);
    
    // Create detailed telework log
    await knex('telework_log').insert({
      telework_id,
      travel_mode: telework_travel_modes,
      origin_name,
      origin_address,
      origin_lat: telework_log_tmp.origin_lat,
      origin_lng: telework_log_tmp.origin_lng,
      destination_name,
      destination_address,
      destination_lat: telework_log_tmp.destination_lat,
      destination_lng: telework_log_tmp.destination_lng,
      distance: distance ?? trip.distance,
    });
  }
};
```

**Auto-Logging Features:**
- **Duplicate Prevention:** Checks for existing telework logs before creation
- **Workplace Detection:** Geographic verification of work-related trips
- **Enterprise Integration:** Links trips to enterprise organizations
- **Role-Based Travel Modes:** Different logging for drivers vs riders
- **Timezone Handling:** Proper timezone conversion for trip dates

### Geographic Distance Calculations

### Distance Calculation Utilities
```javascript
const _calc_rad = (d) => {
  return (d * Math.PI) / 180.0;
};

const _calc_geodistance = (lng1, lat1, lng2, lat2) => {
  const EARTH_REDIUS = 6378.137;
  const radLat1 = _calc_rad(lat1);
  const radLat2 = _calc_rad(lat2);
  const a = radLat1 - radLat2;
  const b = _calc_rad(lng1) - _calc_rad(lng2);
  const s =
    2 *
    Math.asin(
      Math.sqrt(
        Math.pow(Math.sin(a / 2), 2) +
          Math.cos(radLat1) * Math.cos(radLat2) * Math.pow(Math.sin(b / 2), 2),
      ),
    ) *
    EARTH_REDIUS *
    1000;
  return s;
};

const _verify_o_d_is_work_place = async (user_id, od_geo) => {
  let is_work_place = false;
  // Fetch user work place information
  const work_place_info = await UserFavorites.query()
    .where('user_id', user_id)
    .where('category', 2) // Work place category
    .select('latitude', 'longitude')
    .first();
    
  if (work_place_info) {
    const distance_with_origin = _calc_geodistance(
      work_place_info.longitude,
      work_place_info.latitude,
      od_geo.origin_longitude,
      od_geo.origin_latitude,
    );
    const distance_with_destination = _calc_geodistance(
      work_place_info.longitude,
      work_place_info.latitude,
      od_geo.destination_longitude,
      od_geo.destination_latitude,
    );
    // 100 meter tolerance for workplace detection
    if (distance_with_origin < 100 || distance_with_destination < 100) {
      is_work_place = true;
    }
  }
  return is_work_place;
};
```

**Geographic Calculation Features:**
- **Haversine Formula:** Accurate earth-surface distance calculations
- **Workplace Detection:** 100-meter tolerance for work location matching
- **User Favorites Integration:** Links to user-defined favorite locations
- **Precision Handling:** Proper radian conversion and earth radius constants

### Real-Time Status Validation

### checkDuoRealtime Function
**Purpose:** Validates that all required carpool coordination steps have been completed

```javascript
const checkDuoRealtime = async (driver_trip_id) => {
  logger.info(`[_check_duo_realtime] enter, driver_trip_id: ${driver_trip_id}`);
  const duo_realtime = await DuoRealtime.query().where('trip_id', driver_trip_id);
  
  const check = {};
  const keys = [
    DUO_REALTIME_STATUS.STARTED,
    DUO_REALTIME_STATUS.ARRIVE_PICKUP_POINT,
    DUO_REALTIME_STATUS.PICKUP_MANUALLY,
    DUO_REALTIME_STATUS.DROPOFF_MANUALLY,
  ];
  
  // Initialize all checks as false
  for (const key of keys) {
    check[key] = false;
  }
  
  // Mark completed steps as true
  for (const dr of duo_realtime) {
    if (keys.includes(dr.status)) {
      check[dr.status] = true;
    }
  }
  
  // All steps must be completed for validation
  let result = true;
  for (const key of keys) {
    if (!check[key]) {
      result = false;
    }
  }
  
  logger.info(`[_check_duo_realtime] result: ${result}`);
  return result;
};
```

**Real-Time Validation Features:**
- **Step-by-Step Verification:** Ensures all carpool coordination steps completed
- **Status Tracking:** Monitors trip start, pickup arrival, manual pickup/dropoff
- **Boolean Logic:** All required steps must be true for validation
- **Driver-Centric:** Validation based on driver's trip coordination

## 🚀 Usage Methods

### Basic Trip Management
```javascript
const tripService = require('@app/src/services/trip');

// Start a new trip
const tripData = {
  travel_mode: 'carpool',
  origin: 'Home',
  destination: 'Office',
  distance: 15000,
  estimated_arrival_on: '2024-06-25T16:30:00Z',
  route: {
    polyline: 'encoded_polyline_data',
    waypoints: []
  }
};

const newTrip = await tripService.startTrip(12345, tripData, [], 'America/Chicago');
console.log('Trip started:', newTrip);

// Check trip status
const status = await tripService.getTripStatus(newTrip.id);
console.log('Trip status:', status);

// Update trip payment status
await tripService.setTripStatus(newTrip.id, 1, 'Approved by admin');
```

### Advanced Trip Management System
```javascript
class ComprehensiveTripManager {
  constructor() {
    this.tripService = require('@app/src/services/trip');
    this.activeTrips = new Map();
    this.validationQueue = new Map();
    this.metrics = {
      totalTrips: 0,
      completedTrips: 0,
      canceledTrips: 0,
      validatedTrips: 0
    };
  }

  async startManagedTrip(userId, tripData, options = {}) {
    try {
      const {
        autoValidation = true,
        enableRealTimeTracking = true,
        enterpriseId = null,
        zone = 'America/Chicago'
      } = options;

      const startTime = Date.now();
      
      // Start the trip
      const trip = await this.tripService.startTrip(userId, tripData, [], zone);
      
      // Track the trip
      this.activeTrips.set(trip.id, {
        userId,
        tripId: trip.id,
        startTime,
        travelMode: tripData.travel_mode,
        estimatedArrival: tripData.estimated_arrival_on,
        status: 'started',
        enterpriseId,
        validationEnabled: autoValidation
      });

      // Set up validation if enabled
      if (autoValidation && tripData.estimated_arrival_on) {
        await this.scheduleValidation(trip.id, tripData.estimated_arrival_on);
      }

      // Update metrics
      this.metrics.totalTrips++;

      return {
        success: true,
        tripId: trip.id,
        message: 'Trip started successfully',
        validationScheduled: autoValidation,
        estimatedProcessingTime: Date.now() - startTime
      };
    } catch (error) {
      console.error('Error starting managed trip:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  async scheduleValidation(tripId, estimatedArrival) {
    try {
      const arrivalTime = new Date(estimatedArrival).getTime();
      const currentTime = Date.now();
      const delay = arrivalTime - currentTime;

      if (delay > 0) {
        const timeoutId = setTimeout(async () => {
          await this.validateTrip(tripId);
        }, delay);

        this.validationQueue.set(tripId, {
          timeoutId,
          scheduledTime: arrivalTime,
          status: 'scheduled'
        });

        console.log(`Validation scheduled for trip ${tripId} in ${delay}ms`);
      } else {
        // If estimated arrival is in the past, validate immediately
        setImmediate(() => this.validateTrip(tripId));
      }
    } catch (error) {
      console.error('Error scheduling validation:', error);
    }
  }

  async validateTrip(tripId) {
    try {
      console.log(`Starting validation for trip ${tripId}`);
      
      const tripInfo = this.activeTrips.get(tripId);
      if (!tripInfo) {
        console.warn(`No active trip found for validation: ${tripId}`);
        return;
      }

      // Simulate validation logic
      const validationResult = await this.performTripValidation(tripId, tripInfo);
      
      // Update trip status
      if (validationResult.passed) {
        await this.completeTripValidation(tripId, validationResult);
      } else {
        await this.handleValidationFailure(tripId, validationResult);
      }

      // Clean up validation queue
      if (this.validationQueue.has(tripId)) {
        clearTimeout(this.validationQueue.get(tripId).timeoutId);
        this.validationQueue.delete(tripId);
      }

    } catch (error) {
      console.error(`Error validating trip ${tripId}:`, error);
    }
  }

  async performTripValidation(tripId, tripInfo) {
    // Simulate complex validation logic
    const validationChecks = {
      distanceCheck: Math.random() > 0.1, // 90% pass rate
      timeCheck: Math.random() > 0.05, // 95% pass rate
      routeCheck: Math.random() > 0.15, // 85% pass rate
      workplaceCheck: tripInfo.enterpriseId ? Math.random() > 0.2 : true // 80% pass for enterprise
    };

    const passed = Object.values(validationChecks).every(check => check);
    const score = Object.values(validationChecks).filter(check => check).length / Object.keys(validationChecks).length;

    return {
      tripId,
      passed,
      score: Math.round(score * 100),
      checks: validationChecks,
      validatedAt: new Date().toISOString(),
      reasons: this.generateValidationReasons(validationChecks)
    };
  }

  generateValidationReasons(checks) {
    const reasons = [];
    if (!checks.distanceCheck) reasons.push('Distance discrepancy detected');
    if (!checks.timeCheck) reasons.push('Trip duration outside expected range');
    if (!checks.routeCheck) reasons.push('Route validation failed');
    if (!checks.workplaceCheck) reasons.push('Workplace verification failed');
    return reasons;
  }

  async completeTripValidation(tripId, validationResult) {
    try {
      const tripInfo = this.activeTrips.get(tripId);
      
      // Update trip status in service
      await this.tripService.setTripStatus(tripId, 1, 'Validation passed');
      
      // Update local tracking
      tripInfo.status = 'validated';
      tripInfo.validationResult = validationResult;
      tripInfo.completedAt = new Date().toISOString();
      
      // Update metrics
      this.metrics.completedTrips++;
      this.metrics.validatedTrips++;
      
      console.log(`Trip ${tripId} validated successfully with score ${validationResult.score}`);
      
      // Trigger reward calculation
      await this.calculateTripRewards(tripId, tripInfo);
      
    } catch (error) {
      console.error(`Error completing validation for trip ${tripId}:`, error);
    }
  }

  async handleValidationFailure(tripId, validationResult) {
    try {
      const tripInfo = this.activeTrips.get(tripId);
      
      // Update trip status
      await this.tripService.setTripStatus(tripId, 2, `Validation failed: ${validationResult.reasons.join(', ')}`);
      
      // Update local tracking
      tripInfo.status = 'validation_failed';
      tripInfo.validationResult = validationResult;
      tripInfo.failedAt = new Date().toISOString();
      
      console.log(`Trip ${tripId} validation failed: ${validationResult.reasons.join(', ')}`);
      
    } catch (error) {
      console.error(`Error handling validation failure for trip ${tripId}:`, error);
    }
  }

  async calculateTripRewards(tripId, tripInfo) {
    try {
      // Simulate reward calculation
      const baseReward = 10;
      const modeMultiplier = this.getTravelModeMultiplier(tripInfo.travelMode);
      const enterpriseBonus = tripInfo.enterpriseId ? 5 : 0;
      
      const totalReward = baseReward * modeMultiplier + enterpriseBonus;
      
      tripInfo.rewards = {
        baseReward,
        modeMultiplier,
        enterpriseBonus,
        totalReward
      };
      
      console.log(`Trip ${tripId} earned ${totalReward} points`);
      
    } catch (error) {
      console.error(`Error calculating rewards for trip ${tripId}:`, error);
    }
  }

  getTravelModeMultiplier(travelMode) {
    const multipliers = {
      'carpool': 2.0,
      'transit': 1.8,
      'biking': 1.5,
      'walking': 1.2,
      'driving': 1.0,
      'ridehail': 1.1
    };
    return multipliers[travelMode] || 1.0;
  }

  async cancelTrip(tripId, reason = 'User canceled') {
    try {
      const tripInfo = this.activeTrips.get(tripId);
      if (!tripInfo) {
        throw new Error(`Trip ${tripId} not found`);
      }

      // Update trip status
      await this.tripService.setTripStatus(tripId, 3, reason);
      
      // Update local tracking
      tripInfo.status = 'canceled';
      tripInfo.cancelReason = reason;
      tripInfo.canceledAt = new Date().toISOString();
      
      // Clean up validation if scheduled
      if (this.validationQueue.has(tripId)) {
        clearTimeout(this.validationQueue.get(tripId).timeoutId);
        this.validationQueue.delete(tripId);
      }
      
      // Update metrics
      this.metrics.canceledTrips++;
      
      return {
        success: true,
        message: `Trip ${tripId} canceled: ${reason}`
      };
    } catch (error) {
      console.error(`Error canceling trip ${tripId}:`, error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  async getTripDetails(tripId) {
    try {
      const tripInfo = this.activeTrips.get(tripId);
      if (!tripInfo) {
        return {
          found: false,
          message: 'Trip not found in active trips'
        };
      }

      // Get database status
      const dbStatus = await this.tripService.getTripStatus(tripId);
      
      return {
        found: true,
        tripInfo,
        dbStatus,
        validationStatus: this.validationQueue.get(tripId),
        duration: tripInfo.completedAt 
          ? new Date(tripInfo.completedAt).getTime() - tripInfo.startTime
          : Date.now() - tripInfo.startTime
      };
    } catch (error) {
      console.error(`Error getting trip details for ${tripId}:`, error);
      return {
        found: false,
        error: error.message
      };
    }
  }

  async getActiveTrips(userId = null) {
    const activeTrips = Array.from(this.activeTrips.values());
    
    if (userId) {
      return activeTrips.filter(trip => trip.userId === userId);
    }
    
    return activeTrips;
  }

  async generateTripReport(userId = null, dateRange = null) {
    try {
      const trips = await this.getActiveTrips(userId);
      
      let filteredTrips = trips;
      if (dateRange) {
        const startDate = new Date(dateRange.start).getTime();
        const endDate = new Date(dateRange.end).getTime();
        filteredTrips = trips.filter(trip => 
          trip.startTime >= startDate && trip.startTime <= endDate
        );
      }

      const report = {
        summary: {
          totalTrips: filteredTrips.length,
          completedTrips: filteredTrips.filter(t => t.status === 'validated').length,
          canceledTrips: filteredTrips.filter(t => t.status === 'canceled').length,
          pendingTrips: filteredTrips.filter(t => t.status === 'started').length
        },
        travelModes: {},
        rewards: {
          totalPoints: 0,
          averagePoints: 0
        },
        validationStats: {
          passed: 0,
          failed: 0,
          pending: 0
        }
      };

      // Calculate travel mode distribution
      filteredTrips.forEach(trip => {
        const mode = trip.travelMode;
        report.travelModes[mode] = (report.travelModes[mode] || 0) + 1;
        
        if (trip.rewards) {
          report.rewards.totalPoints += trip.rewards.totalReward;
        }
        
        if (trip.validationResult) {
          if (trip.validationResult.passed) {
            report.validationStats.passed++;
          } else {
            report.validationStats.failed++;
          }
        } else if (trip.status === 'started') {
          report.validationStats.pending++;
        }
      });

      if (filteredTrips.length > 0) {
        report.rewards.averagePoints = Math.round(report.rewards.totalPoints / filteredTrips.length * 100) / 100;
      }

      return {
        success: true,
        report,
        generatedAt: new Date().toISOString(),
        criteria: { userId, dateRange }
      };
    } catch (error) {
      console.error('Error generating trip report:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  getSystemMetrics() {
    return {
      ...this.metrics,
      activeTripsCount: this.activeTrips.size,
      pendingValidations: this.validationQueue.size,
      successRate: this.metrics.totalTrips > 0 
        ? (this.metrics.completedTrips / this.metrics.totalTrips * 100).toFixed(2) + '%'
        : '0%',
      validationRate: this.metrics.completedTrips > 0
        ? (this.metrics.validatedTrips / this.metrics.completedTrips * 100).toFixed(2) + '%'
        : '0%'
    };
  }

  async cleanupExpiredTrips(maxAge = 86400000) { // 24 hours default
    const now = Date.now();
    const expiredTrips = [];

    for (const [tripId, tripInfo] of this.activeTrips.entries()) {
      if (now - tripInfo.startTime > maxAge) {
        expiredTrips.push(tripId);
      }
    }

    for (const tripId of expiredTrips) {
      if (this.validationQueue.has(tripId)) {
        clearTimeout(this.validationQueue.get(tripId).timeoutId);
        this.validationQueue.delete(tripId);
      }
      this.activeTrips.delete(tripId);
    }

    return {
      cleanedTrips: expiredTrips.length,
      remainingTrips: this.activeTrips.size
    };
  }
}

// Usage
const tripManager = new ComprehensiveTripManager();

// Start a managed trip
const tripResult = await tripManager.startManagedTrip(12345, {
  travel_mode: 'carpool',
  origin: 'Home',
  destination: 'Office',
  distance: 15000,
  estimated_arrival_on: '2024-06-25T16:30:00Z',
  route: { polyline: 'encoded_data' }
}, {
  autoValidation: true,
  enterpriseId: 100,
  zone: 'America/Chicago'
});

console.log('Trip started:', tripResult);

// Get trip details
const tripDetails = await tripManager.getTripDetails(tripResult.tripId);
console.log('Trip details:', tripDetails);

// Generate trip report
const report = await tripManager.generateTripReport(12345, {
  start: '2024-06-01',
  end: '2024-06-30'
});
console.log('Trip report:', report);

// Get system metrics
const metrics = tripManager.getSystemMetrics();
console.log('System metrics:', metrics);
```

## 📊 Output Examples

### Trip Start Response
```javascript
{
  id: 12345
}
```

### Trip Status Response
```javascript
{
  id: 1,
  score: 85,
  passed: 1,
  validation_status: 1,
  payment_status: 1,
  reason: "Validation passed",
  driver_trip_id: 12345,
  passenger_trip_id: 12346,
  created_at: "2024-06-25T14:30:00Z",
  updated_at: "2024-06-25T16:30:00Z"
}
```

### Trip Validation Result
```javascript
{
  tripId: 12345,
  passed: true,
  score: 95,
  checks: {
    distanceCheck: true,
    timeCheck: true,
    routeCheck: true,
    workplaceCheck: true
  },
  validatedAt: "2024-06-25T16:30:00Z",
  reasons: []
}
```

### Comprehensive Trip Report
```javascript
{
  success: true,
  report: {
    summary: {
      totalTrips: 25,
      completedTrips: 22,
      canceledTrips: 2,
      pendingTrips: 1
    },
    travelModes: {
      "carpool": 15,
      "transit": 6,
      "biking": 3,
      "driving": 1
    },
    rewards: {
      totalPoints: 850,
      averagePoints: 34.0
    },
    validationStats: {
      passed: 20,
      failed: 2,
      pending: 1
    }
  },
  generatedAt: "2024-06-25T17:00:00Z",
  criteria: {
    userId: 12345,
    dateRange: {
      start: "2024-06-01",
      end: "2024-06-30"
    }
  }
}
```

### System Metrics
```javascript
{
  totalTrips: 150,
  completedTrips: 142,
  canceledTrips: 8,
  validatedTrips: 135,
  activeTripsCount: 5,
  pendingValidations: 2,
  successRate: "94.67%",
  validationRate: "95.07%"
}
```

## ⚠️ Important Notes

### Complex State Management
- **Multi-Modal Support:** Different logic paths for carpool, ridehail, transit, biking, walking
- **Role-Based Operations:** Distinct behavior for drivers vs passengers/riders
- **Status Transitions:** Complex state machine with multiple status types and transitions
- **Timer-Based Operations:** Automatic validation scheduling based on estimated arrival times

### Database Transaction Management
- **ACID Compliance:** Critical operations wrapped in database transactions
- **Complex Joins:** Multi-table joins for carpool partnership identification
- **Performance Optimization:** Efficient queries with proper indexing requirements
- **Data Integrity:** Referential integrity across multiple related tables

### Validation System Architecture
- **Automated Validation:** Timer-based validation triggering at estimated arrival
- **Manual Override:** Administrative capability to override validation results
- **Geographic Verification:** Distance-based workplace and route validation
- **Multi-Round Validation:** Support for validation retries with buffer time

### Enterprise Integration Features
- **Organization Tracking:** Enterprise-specific trip logging and reporting
- **Workplace Detection:** Geographic verification of work-related trips
- **Group Membership:** Duo group validation for carpool partnerships
- **Reward Calculation:** Enterprise-specific bonus point calculations

## 🔗 Related File Links

- **Carpool Handler:** `allrepo/connectsmart/tsp-api/src/services/carpoolHandler.js`
- **Wallet Service:** `allrepo/connectsmart/tsp-api/src/services/wallet.js`
- **Incentive Service:** `allrepo/connectsmart/tsp-api/src/services/incentive.js`
- **Trip Models:** `allrepo/connectsmart/tsp-api/src/models/Trips.js`, `TripRoutes.js`, `TripValidationQueue.js`
- **Enterprise Service:** `allrepo/connectsmart/tsp-api/src/services/enterprise.js`

---
*This service provides comprehensive trip lifecycle management with validation systems, reward calculations, and enterprise integration for the TSP platform.*