# TSP API Incentive Helper Service Documentation

## 🔍 Quick Summary (TL;DR)
The Incentive Helper service provides utilities for calculating trip rewards, distance validation, and statistical reward distribution using Gamma distribution algorithms for the incentive system.

**Keywords:** incentive-rewards | gamma-distribution | trip-distance | reward-calculation | statistical-modeling | first-trip-bonus | travel-mode-mapping | distance-validation

**Primary use cases:** Calculating reward points for trips, validating trip distances using routing APIs, generating statistically distributed reward values, handling first-trip bonuses

**Compatibility:** Node.js >= 16.0.0, MySQL database integration, HERE/Google Maps API integration

## ❓ Common Questions Quick Index
- **Q: How are reward points calculated?** → Uses Gamma distribution with configurable parameters for random but controlled rewards
- **Q: What's the first trip bonus?** → Fixed reward of $0.99 for new users' first completed trip
- **Q: How is trip distance validated?** → Multi-tier approach: HERE API → Google Maps API → linear distance fallback
- **Q: What travel modes are supported?** → All major modes including driving, transit, walking, biking, ridehail, trucking
- **Q: How does the Gamma distribution work?** → Statistical algorithm ensuring reward variance while maintaining target mean values
- **Q: What's the minimum distance threshold?** → 10 meters - trips below this use linear distance calculation

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **reward calculator and trip validator** for the incentive system. When someone completes a trip, this service figures out how many reward points they should get (with some randomness to keep it interesting), validates that the trip distance makes sense by checking with mapping services, and gives special bonuses for first-time users.

**Technical explanation:** 
A comprehensive utility service that handles trip reward calculations using statistical Gamma distribution, multi-tier distance validation through HERE and Google APIs, and travel mode normalization. Implements sophisticated algorithms for fair reward distribution while maintaining statistical properties for business analytics.

**Business value explanation:**
Critical for incentive program effectiveness and user engagement. Ensures fair reward distribution, prevents distance fraud through API validation, maintains user engagement through varied rewards, and provides data integrity for analytics and business intelligence reporting.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/incentiveHelper.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js service with MySQL and external API integration
- **Type:** Incentive Calculation and Validation Service
- **File Size:** ~6.8 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High - Complex mathematical algorithms and multi-API integration)

**Dependencies:**
- `@maas/core/mysql`: Database connectivity (**Critical**)
- `@maas/core/log`: Logging infrastructure (**High**)
- `@app/src/services/hereRouting`: HERE Maps routing API (**High**)
- `@app/src/services/googleApis`: Google Maps routing API (**High**)
- `@app/src/helpers/calculate-geodistance`: Linear distance calculation (**High**)
- `@app/src/static/defines`: Travel mode definitions (**Medium**)
- `@app/src/services/utils`: Utility functions (**Medium**)

## 📝 Detailed Code Analysis

### Gamma Distribution Algorithm (rGamma Function)

**Purpose:** Generates statistically distributed random numbers for reward calculation

**Parameters:**
- `alpha`: Number - Shape parameter (controls distribution shape)
- `beta`: Number - Scale parameter (controls distribution scale)

**Returns:** Number - Random value following Gamma distribution

**Implementation:** Uses R.C.H. Cheng algorithm for alpha > 1, special cases for alpha = 1 and alpha < 1

```javascript
function rGamma(alpha, beta) {
  const SG_MAGICCONST = 1 + Math.log(4.5);
  const log4 = Math.log(4.0);
  
  if (alpha > 1) {
    // Cheng algorithm for alpha > 1
    const ainv = Math.sqrt(2.0 * alpha - 1.0);
    const bbb = alpha - log4;
    const ccc = alpha + ainv;
    // ... complex mathematical implementation
  }
  // ... other cases
}
```

### Reward Point Calculation (getIncentiveRewardPoint Function)

**Purpose:** Calculates reward points based on trip type and configured rules

**Parameters:**
- `isFirstTrip`: Boolean - Whether this is user's first trip
- `rule`: Object - Market-specific incentive rules
- `modeRule`: Object - Travel mode specific parameters (max, min, mean, beta)

**Returns:** Number - Calculated reward points

**Logic:**
- First trip: Returns fixed bonus (rule.W or $0.99)
- Regular trips: Uses Gamma distribution with mode-specific parameters

### Distance Validation (fixTripDistance Function)

**Purpose:** Multi-tier distance validation and calculation system

**Parameters:**
- `originLat/originLng`: Numbers - Trip origin coordinates
- `destinationLat/destinationLng`: Numbers - Trip destination coordinates  
- `travelMode`: Number - Travel mode identifier

**Returns:** Number - Validated trip distance in meters

**Validation Tiers:**
1. **Linear Distance Check:** If ≤ 10m, use straight-line distance
2. **HERE API Routing:** Primary validation using HERE Maps
3. **Google Maps API:** Fallback if HERE fails
4. **Linear Distance:** Final fallback

```javascript
async function fixTripDistance(originLat, originLng, destinationLat, destinationLng, travelMode) {
  const linearDistance = calcDistance(originLat, originLng, destinationLat, destinationLng);
  
  if (linearDistance <= MIN_DISTANCE) return linearDistance;
  
  // Try HERE API first
  let distance = await hereRouting(mode, origin, destination, 'summary', 'incentive');
  if (distance) return distance;
  
  // Fallback to Google Maps
  const { routes } = await fetchGoogleRoute({ origin, destination, mode }, 'incentive fixTripDistance');
  if (routes.length > 0) return routes[0].legs[0].distance.value;
  
  // Final fallback to linear distance
  return linearDistance;
}
```

### Database Distance Recalculation (recalculateTripDistance Function)

**Purpose:** Recalculates and updates stored trip distances for existing records

**Parameters:**
- `tripId`: Number - Database trip identifier

**Returns:** Number - Updated distance value

**Process:**
1. Queries trip and telework tables for coordinates
2. Calculates distance if not already stored
3. Updates both trip and telework_log tables
4. Returns final distance value

## 🚀 Usage Methods

### Basic Reward Calculation
```javascript
const incentiveHelper = require('@app/src/services/incentiveHelper');

async function calculateTripReward(userId, tripData, incentiveRules) {
  try {
    // Check if this is user's first trip
    const isFirstTrip = await checkUserFirstTrip(userId);
    
    // Get mode-specific rules
    const modeRule = incentiveRules.modes[tripData.travelMode];
    
    // Calculate reward points
    const rewardPoints = await incentiveHelper.getIncentiveRewardPoint(
      isFirstTrip,
      incentiveRules,
      modeRule
    );
    
    console.log(`Calculated reward: ${rewardPoints} points`);
    return {
      points: rewardPoints,
      isFirstTrip: isFirstTrip,
      appliedRule: modeRule
    };
  } catch (error) {
    console.error('Reward calculation failed:', error);
    throw error;
  }
}
```

### Distance Validation Pipeline
```javascript
async function validateAndUpdateTripDistance(tripData) {
  const incentiveHelper = require('@app/src/services/incentiveHelper');
  
  try {
    // Validate distance using external APIs
    const validatedDistance = await incentiveHelper.fixTripDistance(
      tripData.originLatitude,
      tripData.originLongitude,
      tripData.destinationLatitude,
      tripData.destinationLongitude,
      tripData.travelMode
    );
    
    // Update trip record if distance differs significantly
    const originalDistance = tripData.distance || 0;
    const distanceDifference = Math.abs(validatedDistance - originalDistance);
    const percentageDifference = originalDistance > 0 ? (distanceDifference / originalDistance) * 100 : 100;
    
    if (percentageDifference > 10) { // More than 10% difference
      console.log(`Distance validation: ${originalDistance}m → ${validatedDistance}m (${percentageDifference.toFixed(1)}% change)`);
      
      await updateTripDistance(tripData.id, validatedDistance);
      
      return {
        updated: true,
        originalDistance,
        validatedDistance,
        percentageChange: percentageDifference
      };
    }
    
    return {
      updated: false,
      distance: validatedDistance
    };
  } catch (error) {
    console.error('Distance validation failed:', error);
    return {
      updated: false,
      error: error.message,
      fallbackDistance: tripData.distance || 0
    };
  }
}
```

### Incentive Rules Engine
```javascript
class IncentiveRewardsEngine {
  constructor() {
    this.incentiveHelper = require('@app/src/services/incentiveHelper');
  }

  async processTrip(tripData, userProfile, marketRules) {
    try {
      // Step 1: Validate and fix trip distance
      const validatedDistance = await this.incentiveHelper.fixTripDistance(
        tripData.originLatitude,
        tripData.originLongitude,
        tripData.destinationLatitude,
        tripData.destinationLongitude,
        tripData.travelMode
      );

      // Step 2: Check eligibility criteria
      const eligibility = await this.checkTripEligibility(tripData, validatedDistance);
      if (!eligibility.eligible) {
        return {
          eligible: false,
          reason: eligibility.reason,
          distance: validatedDistance
        };
      }

      // Step 3: Determine if first trip bonus applies
      const isFirstTrip = userProfile.completedTrips === 0;

      // Step 4: Get travel mode specific rules
      const travelModeText = this.incentiveHelper.travelModes[tripData.travelMode];
      const modeRule = marketRules.modes[travelModeText];

      if (!modeRule) {
        throw new Error(`No incentive rules defined for travel mode: ${travelModeText}`);
      }

      // Step 5: Calculate reward points
      const rewardPoints = await this.incentiveHelper.getIncentiveRewardPoint(
        isFirstTrip,
        marketRules,
        modeRule
      );

      // Step 6: Apply any multipliers or adjustments
      const finalReward = await this.applyRewardModifiers(rewardPoints, tripData, userProfile);

      return {
        eligible: true,
        rewardPoints: finalReward,
        isFirstTrip,
        validatedDistance,
        appliedRule: modeRule,
        travelMode: travelModeText
      };
    } catch (error) {
      console.error('Trip processing failed:', error);
      throw error;
    }
  }

  async checkTripEligibility(tripData, distance) {
    // Minimum distance requirement
    if (distance < 100) { // 100 meters minimum
      return { eligible: false, reason: 'Trip too short' };
    }

    // Maximum distance check (prevent fraud)
    if (distance > 1000000) { // 1000km maximum
      return { eligible: false, reason: 'Trip distance suspicious' };
    }

    // Time-based checks
    const tripDuration = new Date(tripData.endTime) - new Date(tripData.startTime);
    const minDurationMs = 30 * 1000; // 30 seconds minimum
    
    if (tripDuration < minDurationMs) {
      return { eligible: false, reason: 'Trip duration too short' };
    }

    return { eligible: true };
  }

  async applyRewardModifiers(baseReward, tripData, userProfile) {
    let finalReward = baseReward;

    // Peak hours bonus (example: 7-9 AM, 5-7 PM)
    const tripHour = new Date(tripData.startTime).getHours();
    if ((tripHour >= 7 && tripHour <= 9) || (tripHour >= 17 && tripHour <= 19)) {
      finalReward *= 1.2; // 20% bonus for peak hours
    }

    // Frequent user bonus
    if (userProfile.completedTrips >= 50) {
      finalReward *= 1.1; // 10% bonus for frequent users
    }

    // Weekend bonus
    const dayOfWeek = new Date(tripData.startTime).getDay();
    if (dayOfWeek === 0 || dayOfWeek === 6) { // Sunday or Saturday
      finalReward *= 1.15; // 15% weekend bonus
    }

    // Round to 2 decimal places
    return Math.round(finalReward * 100) / 100;
  }

  generateRewardDistributionReport(marketRules, sampleSize = 1000) {
    const results = [];
    
    for (const [modeName, modeRule] of Object.entries(marketRules.modes)) {
      const samples = [];
      
      for (let i = 0; i < sampleSize; i++) {
        const reward = this.incentiveHelper.randomDecimalGenerator(
          modeRule.max,
          modeRule.min,
          modeRule.mean,
          modeRule.beta
        );
        samples.push(reward);
      }
      
      const sum = samples.reduce((acc, val) => acc + val, 0);
      const mean = sum / samples.length;
      const variance = samples.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / samples.length;
      const stdDev = Math.sqrt(variance);
      
      results.push({
        travelMode: modeName,
        sampleSize,
        configuredMean: modeRule.mean,
        actualMean: Math.round(mean * 100) / 100,
        standardDeviation: Math.round(stdDev * 100) / 100,
        minValue: Math.min(...samples),
        maxValue: Math.max(...samples),
        configuredMax: modeRule.max,
        configuredMin: modeRule.min
      });
    }
    
    return results;
  }
}
```

### Batch Distance Recalculation
```javascript
async function batchRecalculateDistances(tripIds, options = {}) {
  const incentiveHelper = require('@app/src/services/incentiveHelper');
  const { batchSize = 10, delayMs = 100 } = options;
  
  const results = {
    processed: 0,
    updated: 0,
    errors: 0,
    details: []
  };
  
  // Process in batches to avoid overwhelming APIs
  for (let i = 0; i < tripIds.length; i += batchSize) {
    const batch = tripIds.slice(i, i + batchSize);
    
    console.log(`Processing batch ${Math.floor(i / batchSize) + 1} of ${Math.ceil(tripIds.length / batchSize)}`);
    
    const batchPromises = batch.map(async (tripId) => {
      try {
        const distance = await incentiveHelper.recalculateTripDistance(tripId);
        results.processed++;
        
        if (distance > 0) {
          results.updated++;
        }
        
        results.details.push({
          tripId,
          success: true,
          distance
        });
      } catch (error) {
        results.errors++;
        results.details.push({
          tripId,
          success: false,
          error: error.message
        });
      }
    });
    
    await Promise.all(batchPromises);
    
    // Delay between batches to be respectful to external APIs
    if (i + batchSize < tripIds.length && delayMs > 0) {
      await new Promise(resolve => setTimeout(resolve, delayMs));
    }
  }
  
  console.log(`Batch recalculation complete: ${results.processed} processed, ${results.updated} updated, ${results.errors} errors`);
  return results;
}
```

### Testing and Validation
```javascript
class IncentiveHelperTester {
  constructor() {
    this.incentiveHelper = require('@app/src/services/incentiveHelper');
  }

  testGammaDistribution(alpha, beta, sampleSize = 1000) {
    const samples = [];
    
    for (let i = 0; i < sampleSize; i++) {
      const value = this.incentiveHelper.rGamma(alpha, beta);
      samples.push(value);
    }
    
    const mean = samples.reduce((sum, val) => sum + val, 0) / samples.length;
    const variance = samples.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / samples.length;
    
    // Theoretical values for Gamma distribution
    const theoreticalMean = alpha * beta;
    const theoreticalVariance = alpha * beta * beta;
    
    return {
      sampleSize,
      sampleMean: Math.round(mean * 100) / 100,
      theoreticalMean: Math.round(theoreticalMean * 100) / 100,
      sampleVariance: Math.round(variance * 100) / 100,
      theoreticalVariance: Math.round(theoreticalVariance * 100) / 100,
      minValue: Math.min(...samples),
      maxValue: Math.max(...samples)
    };
  }

  async testDistanceCalculation() {
    // Test coordinates: Houston downtown to Houston airport
    const testData = {
      originLat: 29.7604,
      originLng: -95.3698,
      destinationLat: 29.9844,
      destinationLng: -95.3414,
      travelMode: 1 // DRIVING
    };
    
    try {
      const distance = await this.incentiveHelper.fixTripDistance(
        testData.originLat,
        testData.originLng,
        testData.destinationLat,
        testData.destinationLng,
        testData.travelMode
      );
      
      console.log(`Test distance calculation: ${distance} meters`);
      return {
        success: true,
        distance,
        testData
      };
    } catch (error) {
      console.error('Distance calculation test failed:', error);
      return {
        success: false,
        error: error.message,
        testData
      };
    }
  }

  testRewardCalculation() {
    const testRules = {
      W: 0.99, // First trip bonus
      market: 'test-market'
    };
    
    const testModeRule = {
      max: 5.0,
      min: 0.5,
      mean: 2.0,
      beta: 0.5
    };
    
    // Test first trip bonus
    const firstTripReward = this.incentiveHelper.getIncentiveRewardPoint(true, testRules, testModeRule);
    console.log(`First trip reward: ${firstTripReward}`);
    
    // Test regular trip rewards
    const regularRewards = [];
    for (let i = 0; i < 10; i++) {
      const reward = this.incentiveHelper.getIncentiveRewardPoint(false, testRules, testModeRule);
      regularRewards.push(reward);
    }
    
    console.log(`Regular trip rewards sample: ${regularRewards.join(', ')}`);
    
    return {
      firstTripReward,
      regularRewards,
      averageRegularReward: regularRewards.reduce((sum, val) => sum + val, 0) / regularRewards.length
    };
  }

  async runAllTests() {
    console.log('Running Incentive Helper Tests...');
    
    // Test 1: Gamma distribution
    const gammaTest = this.testGammaDistribution(4, 0.5, 1000);
    console.log('Gamma distribution test:', gammaTest);
    
    // Test 2: Distance calculation
    const distanceTest = await this.testDistanceCalculation();
    console.log('Distance calculation test:', distanceTest);
    
    // Test 3: Reward calculation
    const rewardTest = this.testRewardCalculation();
    console.log('Reward calculation test:', rewardTest);
    
    return {
      gamma: gammaTest,
      distance: distanceTest,
      reward: rewardTest
    };
  }
}
```

## 📊 Output Examples

### Reward Calculation Results
```json
{
  "eligible": true,
  "rewardPoints": 2.47,
  "isFirstTrip": false,
  "validatedDistance": 15420,
  "appliedRule": {
    "max": 5.0,
    "min": 0.5,
    "mean": 2.0,
    "beta": 0.5
  },
  "travelMode": "driving"
}
```

### Distance Validation Results
```json
{
  "updated": true,
  "originalDistance": 12000,
  "validatedDistance": 14250,
  "percentageChange": 18.8,
  "validationMethod": "here_api"
}
```

### Gamma Distribution Statistics
```json
{
  "sampleSize": 1000,
  "sampleMean": 2.03,
  "theoreticalMean": 2.0,
  "sampleVariance": 0.98,
  "theoreticalVariance": 1.0,
  "minValue": 0.12,
  "maxValue": 7.89
}
```

### Batch Recalculation Summary
```json
{
  "processed": 150,
  "updated": 142,
  "errors": 8,
  "summary": {
    "successRate": 94.7,
    "averageDistanceChange": 8.3,
    "apiCallsUsed": {
      "here": 127,
      "google": 15,
      "linear": 8
    }
  }
}
```

## ⚠️ Important Notes

### Gamma Distribution Properties
- **Shape Parameter (alpha):** Controls distribution skewness
- **Scale Parameter (beta):** Controls distribution spread
- **Mean:** alpha × beta
- **Variance:** alpha × beta²
- **Range:** (0, ∞) with proper parameter validation

### Distance Validation Hierarchy
1. **Linear Distance:** Used for trips < 10 meters
2. **HERE API:** Primary routing service with high accuracy
3. **Google Maps API:** Fallback with different route algorithms
4. **Linear Distance:** Final fallback for API failures

### Travel Mode Mapping
```javascript
// Internal ID → API-compatible mode
{
  1: 'driving',      // DRIVING
  2: 'public_transit', // PUBLIC_TRANSIT
  3: 'walking',      // WALKING
  4: 'biking',       // BIKING
  5: 'intermodal',   // INTERMODAL
  6: 'trucking',     // TRUCKING
  7: 'intermodal',   // PARK_AND_RIDE
  8: 'ridehail',     // RIDEHAIL
  9: 'duo',          // DUO
  10: 'instant_duo'  // INSTANT_CARPOOL
}
```

### API Rate Limiting Considerations
- **HERE API:** Rate limits may apply based on subscription
- **Google Maps API:** Quota limits and per-request costs
- **Batch Processing:** Implement delays between API calls
- **Caching:** Consider caching results for frequently calculated routes

### Statistical Accuracy
- **Sample Size:** Larger samples provide more accurate statistical properties
- **Parameter Tuning:** Adjust alpha/beta to achieve desired mean/variance
- **Outlier Handling:** Min/max bounds prevent extreme values
- **Business Logic:** Statistical distribution supports fair reward allocation

### Database Performance
- **Batch Updates:** Use transactions for multiple distance updates
- **Index Optimization:** Ensure trip ID columns are properly indexed
- **Connection Pooling:** Manage database connections efficiently
- **Error Recovery:** Handle database failures gracefully

### Error Scenarios
- **API Failures:** Graceful degradation to fallback methods
- **Invalid Coordinates:** Validation and error logging
- **Network Issues:** Retry logic with exponential backoff
- **Database Errors:** Transaction rollback and error reporting

## 🔗 Related File Links

- **Incentive Rules:** `allrepo/connectsmart/tsp-api/src/services/incentiveRule.js`
- **HERE Routing:** `allrepo/connectsmart/tsp-api/src/services/hereRouting.js`
- **Google APIs:** `allrepo/connectsmart/tsp-api/src/services/googleApis.js`
- **Distance Calculator:** `allrepo/connectsmart/tsp-api/src/helpers/calculate-geodistance.js`
- **Travel Modes:** `allrepo/connectsmart/tsp-api/src/static/defines.js`
- **Incentive Controllers:** Controllers handling reward processing

---
*This service provides essential mathematical and validation utilities for fair and accurate incentive reward distribution in the TSP platform.*