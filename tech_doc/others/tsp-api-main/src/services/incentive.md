# TSP API Incentive Service Documentation

## 🔍 Quick Summary (TL;DR)
The incentive service manages trip-based reward systems, processing user travel behavior to award coins/points based on configurable rules, distance thresholds, and service area validation.

**Keywords:** trip-incentives | reward-system | coins-points | travel-rewards | geofencing | carpool-rewards | sqs-notifications | trip-validation

**Primary use cases:** Awarding travel incentives, validating trip eligibility, managing weekly reward limits, processing carpool rewards, sending reward notifications

**Compatibility:** Node.js >= 16.0.0, MySQL, MongoDB, AWS SQS, Turf.js geospatial analysis

## ❓ Common Questions Quick Index
- **Q: How are trip rewards calculated?** → Based on travel mode, distance, and user status (first-time vs. returning)
- **Q: What trips qualify for rewards?** → Trips >1 mile in service area with valid start/end points
- **Q: Are there weekly limits?** → Yes, configurable weekly point caps prevent abuse
- **Q: How are carpools handled?** → Special validation for driver/passenger completion status
- **Q: What notifications are sent?** → SQS-based push notifications with reward details
- **Q: Are internal users excluded?** → Yes, internal users are filtered out from rewards

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **digital rewards program** for using transportation apps. When you complete a qualifying trip (like driving, walking, or taking transit), the system checks if your trip meets certain criteria (distance, location, etc.) and then awards you coins or points. It's like a loyalty program that encourages people to use smarter transportation options by giving them rewards.

**Technical explanation:** 
A comprehensive incentive management system that validates trip data against configurable business rules, performs geospatial analysis to ensure trips occur within service areas, calculates reward points based on travel modes and user history, and manages notification delivery via AWS SQS. Includes fraud prevention, weekly limits, and detailed audit logging.

**Business value explanation:**
Critical for user engagement and behavior modification in transportation platforms. Incentivizes desired travel behaviors, increases app usage, supports sustainability goals through smart transportation choices, and provides measurable ROI through configurable reward structures and detailed analytics.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/incentive.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Multiple integrations (MySQL, MongoDB, AWS SQS, Turf.js)
- **Type:** Rewards Processing Service
- **File Size:** ~20 KB
- **Complexity Score:** ⭐⭐⭐⭐⭐ (Very High - Complex business logic with multiple validations)

**Dependencies:**
- `@maas/core/log`: Logging infrastructure (**Critical**)
- `@maas/core/mysql`: Database connection (**Critical**)
- `@aws-sdk/client-sqs`: AWS SQS for notifications (**Critical**)
- `@turf/turf`: Geospatial analysis (**Critical**)
- `wkt`: Well-Known Text parsing (**High**)
- `moment-timezone`: Date/time handling (**High**)
- Multiple models for data access (**Critical**)

## 📝 Detailed Code Analysis

### makeTripProcess Function

**Purpose:** Main incentive processing pipeline for completed trips

**Parameters:**
- `userId`: User identifier
- `tripId`: Trip identifier  
- `travelMode`: Transportation method
- `mti`: Make trip incentive data object
- `distance`: Trip distance in meters

**Processing Pipeline:**
1. **User Validation:** Check internal user status and service profile
2. **Geospatial Validation:** Verify trip occurs within service area
3. **Trip Data Validation:** Validate origin/destination coordinates and timing
4. **Distance Validation:** Ensure trip meets minimum distance requirements
5. **Carpool Validation:** Special handling for carpool completion status
6. **Reward Calculation:** Calculate points based on rules and user history
7. **Weekly Limit Check:** Ensure user hasn't exceeded weekly point cap
8. **Point Transaction:** Issue reward points to user account
9. **Notification:** Send reward notification via SQS

### Service Area Validation
```javascript
async function checkTripInServiceArea(tripId, mti, polygon) {
  // Check start point
  let startPoint = turf.point([Number(mti.real_destination_longitude), Number(mti.real_destination_latitude)]);
  let startPointInServiceArea = turf.booleanPointInPolygon(startPoint, polygon);
  if (startPointInServiceArea) return true;
  
  // Check end point
  let endPoint = turf.point([Number(mti.real_destination_longitude), Number(mti.real_destination_latitude)]);
  let endPointInServiceArea = turf.booleanPointInPolygon(endPoint, polygon);
  if (endPointInServiceArea) return true;
  
  // Check trajectory points
  const trace = await getTrace(tripId);
  let traceInServiceArea = select(trace, 100).some((point) => {
    return turf.booleanPointInPolygon(turf.point(point), polygon);
  });
  
  return traceInServiceArea;
}
```

### Carpool Validation Logic
```javascript
if (travelMode === 100) { // Carpool mode
  if (currentTrip.role === 1) {
    // Driver: Check completion status
    const duoStatus = await DuoRealtime.query()
      .whereIn('status', [1, 3, 4, 8])
      .where('trip_id', tripId)
      .selectRaw('count (distinct status) as count')
      .first();
    statusCount = duoStatus.count;
  } else {
    // Passenger: Check driver's completion status
    const driver = await DuoReservation.query()
      .join('duo_reservation as driver', function(builder) {
        builder.on('duo_reservation.offer_id', '=', 'driver.offer_id')
          .andOn('duo_reservation.reservation_id', '!=', 'driver.reservation_id')
      })
      .where('duo_reservation.reservation_id', currentTrip.reservation_id)
      .select('driver.reservation_id');
      
    if (statusCount !== 4) {
      await customDebugLog('Carpool trip incomplete');
      return;
    }
  }
}
```

### Reward Point Calculation
```javascript
isFirstTime = (await IncentiveNotifyQueue.query()
  .where({
    user_id: userId,
    msg_key: 'Incentive1_2_make_trip',
  })
  .select('id')).length === 0;

point = await incentiveHelper.getIncentiveRewardPoint(
  isFirstTime,
  rule,
  modeRule,
);

// Check weekly limits
pointsCurrentWeek = parseFloat(await userTripsWeekBonus(userId));
const weeklyLimit = rule.L ?? INCENTIVE_POINTS_LIMIT_PER_WEEK;

if (utils.pointSum(point, pointsCurrentWeek) > weeklyLimit) {
  await sendZeroPointsNotification(userId, incentiveEventType.INCENTIVE_REACH_THE_WEEKLY_CAP, now);
  return;
}
```

### userTripsWeekBonus Function

**Purpose:** Calculates user's reward points earned in current week

**Processing:**
1. **Week Boundaries:** Calculate start/end of current week
2. **Transaction Lookup:** Find all incentive notifications for the week
3. **Point Aggregation:** Sum all points from qualifying transactions
4. **Return Total:** Provide current week's point total

## 🚀 Usage Methods

### Basic Trip Incentive Processing
```javascript
const incentiveService = require('@app/src/services/incentive');

async function processTripReward(userId, tripId, travelMode, tripData, distance) {
  try {
    // Prepare make trip incentive data
    const mti = await incentiveService.incentiveTripData(
      tripData,
      tripData.destination_latitude,
      tripData.destination_longitude
    );

    // Process the incentive
    await incentiveService.makeTripProcess({
      userId,
      tripId,
      travelMode,
      mti,
      distance
    });

    console.log(`Incentive processed for trip ${tripId}`);
  } catch (error) {
    console.error('Incentive processing failed:', error);
  }
}
```

### Weekly Bonus Tracking
```javascript
async function checkUserWeeklyProgress(userId) {
  try {
    const weeklyBonus = await incentiveService.userTripsWeekBonus(userId);
    
    console.log(`User ${userId} has earned ${weeklyBonus} points this week`);
    
    // Check against weekly limit
    const weeklyLimit = 5; // Default limit
    const remainingPoints = Math.max(0, weeklyLimit - weeklyBonus);
    
    return {
      currentPoints: weeklyBonus,
      weeklyLimit,
      remainingPoints,
      canEarnMore: remainingPoints > 0
    };
  } catch (error) {
    console.error('Weekly bonus check failed:', error);
    return null;
  }
}
```

### Incentive Rule Management
```javascript
class IncentiveManager {
  constructor() {
    this.incentiveService = require('@app/src/services/incentive');
  }

  async validateTripEligibility(tripData) {
    const validations = {
      hasValidCoordinates: this.validateCoordinates(tripData),
      meetsDistanceRequirement: tripData.distance >= 1609, // 1 mile
      withinTimeWindow: this.validateTiming(tripData),
      inServiceArea: await this.validateServiceArea(tripData),
      notDuplicate: await this.checkDuplicateReward(tripData.tripId, tripData.userId)
    };

    const isEligible = Object.values(validations).every(Boolean);
    
    return {
      eligible: isEligible,
      validations,
      reason: isEligible ? 'Trip qualifies for incentive' : 'Trip does not meet requirements'
    };
  }

  validateCoordinates(tripData) {
    return !!(
      tripData.origin_latitude &&
      tripData.origin_longitude &&
      tripData.destination_latitude &&
      tripData.destination_longitude
    );
  }

  validateTiming(tripData) {
    const startTime = new Date(tripData.started_on);
    const now = new Date();
    const timeDiff = Math.abs(now.getTime() - startTime.getTime());
    const hoursDiff = timeDiff / (1000 * 60 * 60);
    
    return hoursDiff <= 2; // Within 2 hours
  }

  async checkDuplicateReward(tripId, userId) {
    try {
      const existing = await IncentiveNotifyQueue.query()
        .where('user_id', userId)
        .where('trip_ids', tripId)
        .where('incentive_type', 'incentive make trip')
        .count('id as count');
        
      return existing[0].count === 0;
    } catch (error) {
      console.error('Duplicate check failed:', error);
      return false;
    }
  }
}
```

### Batch Incentive Processing
```javascript
async function processBatchIncentives(tripCompletions) {
  const results = [];
  
  for (const completion of tripCompletions) {
    try {
      const mti = await incentiveService.incentiveTripData(
        completion.tripData,
        completion.destinationLat,
        completion.destinationLng
      );

      await incentiveService.makeTripProcess({
        userId: completion.userId,
        tripId: completion.tripId,
        travelMode: completion.travelMode,
        mti,
        distance: completion.distance
      });

      results.push({
        tripId: completion.tripId,
        userId: completion.userId,
        success: true
      });
    } catch (error) {
      results.push({
        tripId: completion.tripId,
        userId: completion.userId,
        success: false,
        error: error.message
      });
    }
  }

  return results;
}
```

## 📊 Output Examples

### Successful Incentive Processing
```javascript
// Logs indicate successful processing
{
  userId: 12345,
  tripId: 67890,
  pointsAwarded: 2,
  isFirstTime: false,
  weeklyTotal: 4,
  notificationSent: true,
  message: "Incentive-make-trip successes"
}
```

### Weekly Progress Response
```javascript
{
  currentPoints: 3.5,
  weeklyLimit: 5,
  remainingPoints: 1.5,
  canEarnMore: true,
  weekStart: "2024-06-24T00:00:00Z",
  weekEnd: "2024-06-30T23:59:59Z"
}
```

### Incentive Notification Structure
```javascript
{
  user_list: [12345],
  notification_type: 98,
  title: "You've earned 2 reward Coins!",
  body: "Keep taking trips and keep earning rewards for contributing to a more connected, less congested Houston.",
  meta: {
    event_type: 2 // INCENTIVE_NON_FIRST_TRIP
  },
  silent: false,
  ended_on: "2024-07-02T14:30:00Z"
}
```

### Error Cases
```javascript
// Distance too short
{
  error: "INCENTIVE_TRIP_LESS_THAN_1_MILE",
  message: "Trip distance 800m below minimum 1609m requirement"
}

// Weekly limit exceeded
{
  error: "INCENTIVE_REACH_THE_WEEKLY_CAP", 
  message: "User has reached weekly point limit of 5"
}

// Outside service area
{
  error: "Trip not in service area",
  message: "Trip coordinates outside defined service boundaries"
}
```

## ⚠️ Important Notes

### Incentive Event Types
- **INCENTIVE_FIRST_TRIP (1):** First-time user bonus
- **INCENTIVE_NON_FIRST_TRIP (2):** Regular trip reward
- **INCENTIVE_TRIP_LESS_THAN_1_MILE (3):** Distance threshold not met
- **INCENTIVE_TRIP_INVALID_TRIP (4):** Invalid trip data
- **INCENTIVE_REACH_THE_WEEKLY_CAP (5):** Weekly limit exceeded

### Travel Mode Support
- **Car (1):** Standard driving trips
- **Walking (3):** Pedestrian trips
- **Bicycle (4):** Cycling trips
- **Carpool (100):** Social carpooling with special validation
- **Other modes:** Based on incentive rule configuration

### Geospatial Validation
- **Service Area:** Uses WKT polygon definitions
- **Point-in-Polygon:** Turf.js for precise geospatial checks
- **Trajectory Sampling:** Checks 100 sampled points along route
- **Coordinate Validation:** Verifies start/end points and trajectory

### Weekly Limits and Fraud Prevention
- **Default Weekly Limit:** 5 points per week
- **Configurable Limits:** Set via incentive rules (rule.L)
- **Duplicate Prevention:** Checks existing rewards for same trip
- **Internal User Filtering:** Excludes internal/test users
- **Time Window Validation:** 2-hour maximum between planned and actual start

### AWS SQS Integration
- **Queue URL:** Configured via AWS config
- **Message Format:** JSON with action and data
- **Error Handling:** Graceful degradation if SQS fails
- **Retry Logic:** Built into AWS SDK

### Database Relationships
- **Points Transactions:** Links to wallet system
- **Incentive Queue:** Notification delivery tracking
- **Trip Logs:** Audit trail for all incentive decisions
- **Market Users:** User eligibility tracking
- **Carpool Data:** Driver/passenger relationship validation

## 🔗 Related File Links

- **Incentive Helper:** `allrepo/connectsmart/tsp-api/src/services/incentiveHelper.js`
- **Wallet Service:** `allrepo/connectsmart/tsp-api/src/services/wallet.js`
- **Utils Service:** `allrepo/connectsmart/tsp-api/src/services/utils.js`
- **Market Profile:** `allrepo/connectsmart/tsp-api/src/services/marketProfile.js`
- **Distance Calculator:** `allrepo/connectsmart/tsp-api/src/helpers/calculate-geodistance.js`

---
*This service provides comprehensive trip-based incentive management with geospatial validation, fraud prevention, and configurable reward rules.*