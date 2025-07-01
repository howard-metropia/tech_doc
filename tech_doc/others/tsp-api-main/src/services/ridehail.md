# TSP API Ridehail Service Documentation

## 🔍 Quick Summary (TL;DR)
The Ridehail service provides comprehensive Uber integration for ride-hailing services including fare estimation, trip booking, balance management, tier-based benefits, refund processing, enterprise telework tracking, and sandbox testing capabilities.

**Keywords:** uber-integration | ridehail-booking | fare-estimation | tier-benefits | refund-processing | enterprise-tracking | sandbox-testing | balance-management

**Primary use cases:** Getting Uber fare estimates, booking guest rides, managing user benefits, processing refunds, tracking enterprise trips, handling cancellations, sandbox environment testing

**Compatibility:** Node.js >= 16.0.0, Uber Guest API integration, USA geographic restrictions, complex financial transaction processing

## ❓ Common Questions Quick Index
- **Q: What regions are supported?** → USA only (geographic bounds enforced)
- **Q: How do tier benefits work?** → Automatic discount application based on user tier level
- **Q: What refund scenarios exist?** → User cancellation, driver cancellation, fare adjustments with benefit handling
- **Q: How are enterprise trips tracked?** → Automatic telework logging for qualifying routes
- **Q: What sandbox features exist?** → Non-production testing with simulated drivers and trips
- **Q: How is balance validation handled?** → Pre-trip balance checks including tier benefits

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as your **personal Uber booking assistant** that not only helps you get rides but also applies any discounts you've earned, tracks business trips automatically, handles refunds fairly, and makes sure you have enough money before booking. It's specifically designed for the USA and includes special testing features for developers.

**Technical explanation:** 
A comprehensive Uber integration service providing end-to-end ride-hailing functionality with advanced features including tier-based benefit calculations, complex refund processing with benefit reconciliation, enterprise telework tracking, geographic restrictions, and sophisticated error handling with Slack notifications.

**Business value explanation:**
Enables revenue-generating ride-hailing services, supports enterprise B2B telework tracking, provides user engagement through tier benefits, ensures financial integrity through comprehensive refund handling, and maintains service quality through robust error monitoring.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/ridehail.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with Uber Guest API integration
- **Type:** Comprehensive Ride-Hailing Service
- **File Size:** ~28.8 KB
- **Complexity Score:** ⭐⭐⭐⭐⭐ (Very High - Complex external API integration with financial processing)

**Dependencies:**
- `moment-timezone`: Date/time handling (**Critical**)
- `@maas/core/redis`: Caching for sandbox operations (**Medium**)
- `@app/src/services/uber-guest-ride`: Uber API integration (**Critical**)
- `@app/src/services/tier`: User tier benefits (**High**)
- `@app/src/services/wallet`: Financial transactions (**Critical**)
- Multiple models for data persistence (**Critical**)

## 📝 Detailed Code Analysis

### Core Service Functions

### getUberEstimation Function
**Purpose:** Retrieves fare estimates from Uber API with comprehensive validation

```javascript
const getUberEstimation = async (pickup, dropoff) => {
  excludeNonUsaTrip(pickup, dropoff);
  
  const response = await getTripEstimation({ pickup, dropoff });
  
  for (const resp of response.data.product_estimates) {
    if (!resp.product || !resp.estimate_info) {
      slack.sendVendorIncorrectMsg({
        vendor: 'Uber',
        errorMsg: 'Missing field: product or estimate_info'
      });
      continue;
    }
    
    // Validate pickup ETA
    let pickupEta = -1;
    let noCarsAvailable = true;
    if (resp.estimate_info?.pickup_estimate >= 0) {
      pickupEta = resp.estimate_info.pickup_estimate;
      noCarsAvailable = false;
    }
    
    // Process fare information
    if (resp.estimate_info.fare) {
      fareDisplay = parseFare(resp.estimate_info.fare);
      fareCurrency = resp.estimate_info.fare.currency_code;
      
      if (fareCurrency !== 'USD') continue; // USD only
    }
    
    estimates.push({
      product_id: resp.product.product_id,
      product_display: resp.product.display_name,
      fare_display: fareDisplay,
      pickup_eta: pickupEta,
      trip_duration: Math.round(resp.estimate_info.trip.duration_estimate / 60),
      no_cars_available: noCarsAvailable
    });
  }
  
  await cacheFareEstimations(estimates);
  return estimates;
};
```

### Geographic Restrictions

### USA Bounds Validation
```javascript
const isWithinUsaBounds = ({ latitude, longitude }) => {
  const upLeft = { latitude: 48.869373, longitude: -125.484481 };
  const lowRight = { latitude: 24.978368, longitude: -66.275417 };
  
  const lat = parseFloat(latitude);
  const long = parseFloat(longitude);
  
  return (
    lat <= upLeft.latitude &&
    lat >= lowRight.latitude &&
    long <= lowRight.longitude &&
    long >= upLeft.longitude
  );
};

const excludeNonUsaTrip = (pickup, dropoff) => {
  if (!isWithinUsaBounds(pickup) || !isWithinUsaBounds(dropoff)) {
    throw new MaasError(ERROR_CODE.ERROR_BAD_REQUEST_BODY, ...);
  }
};
```
- Enforces strict USA geographic boundaries
- Prevents international ride requests
- Clear error messaging for out-of-bounds requests

### Tier Benefits Integration

### Balance and Benefit Processing
```javascript
const balancePreProcessing = async (userId, fareId, credit = 0) => {
  const fareCache = await UberFareEstimation.findOne({ fare_id: fareId });
  let fare = fareCache.fare_value;
  
  // TWD to USD conversion for testing
  if (fareCache.fare_currency === 'TWD') {
    fare = fixedPoint(fare / 30, 2);
  }
  
  const wallet = await UserWallets.query().where('user_id', userId).first();
  const enough = Number(wallet.balance) + Number(credit) >= fare;
  
  return { enough, fare };
};

const checkBenefitCredit = async (userId, zone, credit) => {
  if (!credit || credit <= 0) return 0;
  
  const tierInfo = await getUserTier(userId, zone);
  const benefit = tierInfo.uber_benefit;
  
  if (benefit !== credit) {
    logger.warn(`Benefit discrepancy, input: ${credit}, system: ${benefit}`);
  }
  
  return benefit;
};
```
- Validates user wallet balance including tier benefits
- Supports currency conversion for testing environments
- Cross-validates benefit amounts with tier service

### Complex Trip Creation

### createTrip Function
**Purpose:** Orchestrates complete trip creation with enterprise tracking

```javascript
const createTrip = async (inputs) => {
  const { userId, zone, guest, pickup, dropoff, ridehail_trip } = inputs;
  
  // Duplicate trip prevention
  if (await checkDuplicatedTrip(userId)) {
    throw new MaasError(ERROR_CODE.ERROR_DUPLICATED_RIDEHAIL, ...);
  }
  
  // Benefit validation
  const benefit = await checkBenefitCredit(userId, zone, ridehail_trip.benefit_credit);
  
  // Balance verification
  const { enough, fare } = await balancePreProcessing(userId, ridehail_trip.fare_id, benefit);
  if (!enough) {
    throw new MaasError(ERROR_CODE.ERROR_POINT_INSUFFICIENT, ...);
  }
  
  // Create Uber trip
  const responseData = await createUberGuestTrip({
    guest, pickup, dropoff,
    product_id: ridehail_trip.product_id,
    fare_id: ridehail_trip.fare_id,
    sender_display_name: 'ConnectSmart'
  });
  
  // Process financial transaction
  await transaction(userId, fare, benefit);
  
  // Record trip details
  await RidehailTrips.query().insert({
    user_id: userId,
    uber_request_id: responseData.request_id,
    estimated_fare: fare,
    benefit_credit: benefit > 0 ? benefit : undefined
  });
  
  // Enterprise tracking
  const enterpriseId = await checkEnterprise(userId, origin, destination);
  await Teleworks.query().insert({
    user_id: userId,
    enterprise_id: enterpriseId,
    is_autolog: 1
  });
  
  return { trip_id: tripResult.id, request_id: responseData.request_id };
};
```

### Advanced Refund Processing

### refundWithBenefit Function
**Purpose:** Handles complex refund scenarios with tier benefits

```javascript
const refundWithBenefit = async (userId, eFare, aFare, benefit, note) => {
  const returnBenefit = Math.min(eFare, benefit);
  const newBenefitShouldPay = aFare >= benefit ? benefit : aFare;
  const discountFare = eFare >= benefit ? eFare - benefit : 0;
  const refundFare = discountFare - (aFare > benefit ? aFare - benefit : 0);
  
  // User refund (if overpaid)
  if (refundFare > 0) {
    const { _id: transactionId1 } = await pointsTransaction(
      userId, activityId, refundFare, note, false, null, uberAccount, userId
    );
    
    await UberBenefitTransaction.query().insert({
      user_id: userId,
      transaction_amount: refundFare,
      transaction_id: transactionId1
    });
  }
  
  // System benefit return
  await pointsTransaction(
    incentiveEngine, benefitActivityId, returnBenefit, note, false, null, uberAccount, incentiveEngine
  );
  
  // System pays actual benefit
  if (newBenefitShouldPay > 0) {
    await pointsTransaction(
      incentiveEngine, benefitActivityId, -1 * newBenefitShouldPay, note, false, null, incentiveEngine, uberAccount
    );
  }
};
```
**Three-way transaction processing:**
1. **User Refund:** Returns excess charges to user
2. **System Benefit Return:** Returns original benefit allocation
3. **System Benefit Payment:** Pays actual benefit amount used

### Enterprise Integration

### checkEnterprise Function
```javascript
const checkEnterprise = async (userId, origin, destination) => {
  const enterprise = await AccMemberPortal.query()
    .where('user_id', userId)
    .andWhere('telework_og_id', '>', 0)
    .first();

  const isWorkSpace = await verifyODIsWorkPlace(userId, origin, destination);
  return enterprise && isWorkSpace ? enterprise.org_id : 0;
};
```
- Validates enterprise membership
- Checks if trip qualifies as work-related
- Enables automatic telework logging

### Sandbox Testing Features

### Sandbox Operations
```javascript
createSbRun: async (inputData) => {
  if (stage === 'production') {
    throw new MaasError(99999, 'error', 'Sandbox only works in non-production environments', 400);
  }
  
  const { pickup, dropoff, isForcedUpdate } = inputData;
  const runId = await createSandboxRun(pickup, dropoff, isForcedUpdate);
  
  return { runId };
},

changeSbDriverStatus: async (inputData) => {
  const { run_id: runId, driver_state: status, driver_id: driverId } = inputData;
  const cachedRunId = await cache.get(sandboxRunKey);
  
  if (!cachedRunId || runId !== cachedRunId) {
    throw new MaasError(ERROR_CODE.ERROR_NOT_FOUND, 'warn', 'Run ID deprecated', 400);
  }
  
  await changeDriverStatus(status, cachedRunId, driverId);
}
```
- Production environment protection
- Cached run ID validation
- Simulated driver state management

## 🚀 Usage Methods

### Basic Ridehail Operations
```javascript
const ridehailService = require('@app/src/services/ridehail');

// Get fare estimates
const estimates = await ridehailService.create({
  pickup: { latitude: 29.7604, longitude: -95.3698 },
  dropoff: { latitude: 29.7500, longitude: -95.3600 }
});

// Book a ride
const booking = await ridehailService.orderGuestTrip({
  userId: 12345,
  zone: 'America/Chicago',
  pickup: { latitude: 29.7604, longitude: -95.3698 },
  dropoff: { latitude: 29.7500, longitude: -95.3600 },
  guest: { phone_number: '+15551234567' },
  ridehail_trip: {
    product_id: 'uber_product_123',
    fare_id: 'fare_456',
    benefit_credit: 5.00,
    note_for_driver: 'Please wait at main entrance'
  }
});

// Get trip details
const tripDetail = await ridehailService.tripDetail({
  trip_id: booking.trip_id
});

// Cancel trip
const cancellation = await ridehailService.cancel({
  trip_id: booking.trip_id
});
```

### Advanced Benefit Management
```javascript
class RidehailBenefitManager {
  constructor() {
    this.ridehailService = require('@app/src/services/ridehail');
  }

  async calculateRideAffordability(userId, fareId, userZone) {
    try {
      // Get user tier benefits
      const tierInfo = await getUserTier(userId, userZone);
      const availableBenefit = tierInfo.uber_benefit || 0;
      
      // Check balance with benefits
      const { enough, fare } = await this.ridehailService.balancePreProcessing(
        userId, fareId, availableBenefit
      );
      
      const userBalance = await UserWallets.query()
        .where('user_id', userId)
        .select('balance')
        .first();
      
      const actualBalance = Number(userBalance?.balance || 0);
      const effectiveBalance = actualBalance + availableBenefit;
      
      return {
        canAfford: enough,
        breakdown: {
          fareAmount: fare,
          userBalance: actualBalance,
          tierBenefit: availableBenefit,
          effectiveBalance,
          shortfall: enough ? 0 : fare - effectiveBalance
        },
        recommendations: this.generateAffordabilityRecommendations(
          enough, fare, actualBalance, availableBenefit
        )
      };
    } catch (error) {
      console.error('Error calculating ride affordability:', error);
      throw error;
    }
  }

  generateAffordabilityRecommendations(canAfford, fare, balance, benefit) {
    const recommendations = [];
    
    if (canAfford) {
      recommendations.push({
        type: 'success',
        message: 'You can afford this ride',
        priority: 'low'
      });
      
      if (benefit > 0) {
        recommendations.push({
          type: 'benefit',
          message: `$${benefit.toFixed(2)} tier benefit will be applied`,
          priority: 'medium'
        });
      }
    } else {
      const shortfall = fare - (balance + benefit);
      recommendations.push({
        type: 'warning',
        message: `Insufficient funds. Need $${shortfall.toFixed(2)} more`,
        priority: 'high'
      });
      
      if (benefit === 0) {
        recommendations.push({
          type: 'tip',
          message: 'Increase your tier level to unlock ride benefits',
          priority: 'medium'
        });
      }
    }
    
    return recommendations;
  }

  async processRideWithOptimalBenefits(userId, rideRequest) {
    try {
      // Calculate optimal benefit usage
      const affordability = await this.calculateRideAffordability(
        userId, rideRequest.ridehail_trip.fare_id, rideRequest.zone
      );
      
      if (!affordability.canAfford) {
        throw new Error(`Insufficient funds: ${affordability.breakdown.shortfall}`);
      }
      
      // Apply optimal benefit amount
      rideRequest.ridehail_trip.benefit_credit = affordability.breakdown.tierBenefit;
      
      // Create the trip
      const result = await this.ridehailService.orderGuestTrip(rideRequest);
      
      return {
        success: true,
        tripDetails: result,
        benefitApplied: affordability.breakdown.tierBenefit,
        savings: affordability.breakdown.tierBenefit
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        suggestions: ['Check account balance', 'Consider adding funds', 'Review tier benefits']
      };
    }
  }
}
```

## 📊 Output Examples

### Fare Estimation Response
```json
{
  "estimates": [
    {
      "product_id": "uber_pool_123",
      "product_display": "UberX",
      "fare_id": "fare_abc456",
      "fare_display": "$12.45",
      "fare_value": 12.45,
      "fare_currency": "USD",
      "pickup_eta": 8,
      "trip_duration": 25,
      "no_cars_available": false
    }
  ],
  "last_update": "2024-06-25T14:30:00+00:00"
}
```

### Trip Creation Response
```json
{
  "trip_id": 78901,
  "request_id": "uber_request_xyz789"
}
```

### Trip Detail Response
```json
{
  "ridehail_trip": {
    "id": 78901,
    "rider_tracking_url": "https://trip.uber.com/track/xyz789",
    "request_id": "uber_request_xyz789",
    "status": "accepted",
    "payment_status": "paid",
    "estimated_fare": 12.45,
    "benefit_credit": 3.00
  },
  "product": {
    "display_name": "UberX",
    "product_id": "uber_pool_123"
  },
  "driver": {
    "name": "John Smith",
    "image_url": "https://uber-driver-photos.s3.amazonaws.com/abc123.jpg"
  },
  "vehicle": {
    "model": "Camry",
    "make": "Toyota",
    "license_plate": "ABC123TX",
    "color": "Blue"
  },
  "pickup": {
    "title": "Main Street",
    "address": "123 Main St, Houston, TX",
    "eta": 8,
    "latitude": 29.7604,
    "longitude": -95.3698
  },
  "dropoff": {
    "title": "Business District",
    "address": "456 Business Ave, Houston, TX",
    "latitude": 29.7500,
    "longitude": -95.3600
  }
}
```

### Benefit Affordability Analysis
```json
{
  "canAfford": true,
  "breakdown": {
    "fareAmount": 12.45,
    "userBalance": 8.50,
    "tierBenefit": 5.00,
    "effectiveBalance": 13.50,
    "shortfall": 0
  },
  "recommendations": [
    {
      "type": "benefit",
      "message": "$5.00 tier benefit will be applied",
      "priority": "medium"
    }
  ]
}
```

## ⚠️ Important Notes

### Geographic and Service Restrictions
- **USA Only:** Strict geographic bounds enforcement for all ride requests
- **USD Currency:** Only USD transactions supported, TWD conversion for testing
- **Enterprise Integration:** Automatic telework tracking for qualifying business trips
- **Sandbox Limitations:** Testing features disabled in production environments

### Financial Transaction Complexity
- **Tier Benefits:** Automatic application of user tier-based discounts
- **Three-Way Refunds:** Complex refund processing involving user, system, and Uber
- **Balance Validation:** Pre-trip verification including benefit calculations
- **Transaction Logging:** Comprehensive audit trail for all financial operations

### Error Handling and Monitoring
- **Slack Integration:** Automatic vendor error notifications for critical issues
- **Rate Limiting:** Proper handling of Uber API rate limits and quotas
- **Duplicate Prevention:** Built-in checks to prevent duplicate trip bookings
- **Graceful Degradation:** Fallback handling for various API failure scenarios

### Enterprise and Business Features
- **Telework Tracking:** Automatic logging of work-related trips
- **Benefit Management:** Integration with tier service for discount application
- **Compliance Logging:** Detailed transaction records for business compliance
- **Multi-User Support:** Handles complex organizational structures

## 🔗 Related File Links

- **Uber Guest Ride Service:** `allrepo/connectsmart/tsp-api/src/services/uber-guest-ride.js`
- **Tier Service:** `allrepo/connectsmart/tsp-api/src/services/tier.js`
- **Wallet Service:** `allrepo/connectsmart/tsp-api/src/services/wallet.js`
- **Ridehail Models:** `allrepo/connectsmart/tsp-api/src/models/RidehailTrips.js`

---
*This service provides comprehensive Uber ride-hailing integration with advanced benefit management and enterprise tracking for the TSP platform.*