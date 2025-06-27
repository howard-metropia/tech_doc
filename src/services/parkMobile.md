# TSP API ParkMobile Service Documentation

## 🔍 Quick Summary (TL;DR)
The ParkMobile service integrates with ParkMobile's parking API to enable mobile parking payments, rate queries, event management, and reminder notifications. It handles parking zone lookups, price calculations, payment processing via points/coins, and tracks parking events with comprehensive error handling and transaction logging.

**Keywords:** mobile-parking | parkmobile-integration | parking-payments | zone-rates | parking-events | payment-processing | parking-reminders | transaction-logging

**Primary use cases:** Mobile parking payments, parking zone rate lookup, parking session management, payment via digital coins, parking reminder notifications, parking event tracking

**Compatibility:** Node.js >= 16.0.0, ParkMobile API integration, MongoDB for logs, MySQL for events, AWS Secrets Manager for payment data

## ❓ Common Questions Quick Index
- **Q: What payment methods are supported?** → Currently only digital coins/points from user wallets
- **Q: Does it work in all environments?** → Uses test zones for non-production, real zones for production
- **Q: How are parking events tracked?** → Events stored in MySQL with status tracking (ON_GOING, ALERTED, FINISHED)
- **Q: Can users set parking reminders?** → Yes, configurable alerts before parking expires
- **Q: How is pricing calculated?** → Real-time rates from ParkMobile API with area/zone/time parameters
- **Q: Are transactions logged?** → Comprehensive logging in MongoDB with payment details and responses

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **digital parking meter on your phone**. Users can find parking spots, check how much they cost, pay with digital coins from their app wallet, start a parking session, and get reminded before their time runs out - all without using physical parking meters or cash.

**Technical explanation:** 
A comprehensive parking payment integration service that interfaces with ParkMobile's API for real-time parking operations. Manages zone rate queries, price calculations, payment processing through digital wallet systems, parking event lifecycle management, and reminder notifications with extensive transaction logging and error handling.

**Business value explanation:**
Enables cashless parking solutions, reduces friction in urban mobility, provides detailed parking analytics, supports digital payment ecosystems, enhances user experience with mobile-first parking, and creates revenue streams through parking transaction fees.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/parkMobile.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with Axios HTTP client
- **Type:** Third-Party Parking Integration Service
- **File Size:** ~26.1 KB
- **Complexity Score:** ⭐⭐⭐⭐⭐ (Very High - Complex API integration with payment processing)

**Dependencies:**
- `axios`: HTTP client for ParkMobile API calls (**Critical**)
- `moment`: Date/time manipulation (**High**)
- `lodash`: Utility library for object manipulation (**Medium**)
- `uuid`: UUID generation for transactions (**Medium**)
- `@maas/services`: AWS services integration (**High**)
- `@maas/core/log`: Logging infrastructure (**High**)
- Various models for data persistence (**Critical**)

## 📝 Detailed Code Analysis

### Core Configuration and Setup

**API Configuration:**
- **Base URL:** Configured via `parkMobile.baseURL`
- **Timeout:** 10 second request timeout
- **Authentication:** Bearer token authentication
- **Environment Handling:** Test zones for non-production, real zones for production

**Security Features:**
- **AWS Secrets Manager:** Stores credit card information securely
- **Token Management:** Database-stored API tokens with expiration tracking
- **Payment Data Scrubbing:** Removes sensitive data from logs
- **Environment Isolation:** Separate test/production payment flows

### Key Functions Analysis

### getRateZone Function

**Purpose:** Retrieves parking zone information and rate structures

**Parameters:**
- `zone`: String - Parking zone identifier

**Returns:** Promise resolving to zone rate data

**Implementation Details:**
```javascript
const getRateZone = async (zone) => {
  const areaZoneNumber = `${hardcodedArea}${zone}`; // Area 953 + zone
  const info = await pmRateZone(areaZoneNumber);
  
  if (info.status === 200) {
    return info.data;
  }
  // Error handling for token and general API issues
};
```

**Data Processing:**
- Replaces null values with empty arrays for frontend compatibility
- Validates time block IDs and replaces invalid ones
- Handles multiple rate structures (hourly, daily, predetermined blocks)

### getRatePrice Function

**Purpose:** Calculates exact pricing for specific parking duration

**Parameters:**
- `zone`: String - Parking zone
- `timeBlockUnit`: String - Unit of time (hours, minutes)
- `timeBlockQuantity`: Number - Amount of time units
- `timeBlockId`: Number - Time block identifier

**Returns:** Promise resolving to price calculation

**Price Calculation Logic:**
```javascript
const realTimeBlockQuantity = checkTimeBlockQuantity({
  timeBlockUnit,
  timeBlockQuantity,
  parkingStartTimeUtc: resp.data.parkingStartTimeUtc,
  parkingStopTimeUtc: resp.data.parkingStopTimeUtc
});
```

**Database Recording:**
- Stores price objects in MongoDB with UUID
- Records zone, time parameters, and calculated pricing
- Implements locking mechanism to prevent double-payment

### startParking Function

**Purpose:** Initiates parking session with payment processing

**Parameters:**
- `userId`: Number - User identifier
- `priceId`: String - Pre-calculated price record ID
- `lpn`: String - License plate number
- `lpnState`: String - License plate state
- `paymentType`: String - Payment method (currently only COIN)

**Returns:** Promise resolving to parking event details

**Complex Flow:**
1. **Preprocessing:** Locks price record, validates duplication, checks balance
2. **API Call:** Activates parking via ParkMobile API
3. **Transaction Logging:** Records API response and payment details
4. **Event Creation:** Creates parking event in MySQL database
5. **Payment Processing:** Deducts coins from user wallet
6. **Error Handling:** Rollback mechanisms for failed operations

**Payment Processing:**
```javascript
// Environment-specific pricing due to ParkMobile test limitations
let parkingFee = price.parkingPrice;
let transactionFee = price.transactionFee;
if (isNonProduction()) {
  parkingFee = priceRecord.price.parkingPrice;
  transactionFee = priceRecord.price.transactionFee;
}
```

### setParkingReminder Function

**Purpose:** Configures expiration alerts for parking sessions

**Parameters:**
- `userId`: Number - User identifier
- `eventId`: Number - Parking event ID
- `alertBefore`: Number - Minutes before expiration to alert

**Logic:**
- Validates minimum 5-minute buffer for alert scheduling
- Updates event status and alert timing
- Supports alert cancellation with `alertBefore: 0`

### listOnGoingParkingEvents Function

**Purpose:** Retrieves user's active and recent parking events

**Parameters:**
- `userId`: Number - User identifier

**Returns:** Array of formatted parking events with status information

**Event Filtering:**
- Active events (ON_GOING, ALERTED, FINISHED)
- Events from last 24 hours
- Formatted timestamps and location data

### Credit Card Management

**getCreditCardInfo Function:**
- **AWS Integration:** Retrieves payment data from Secrets Manager
- **Environment Handling:** Uses test card data for non-production
- **Validation:** Ensures all required fields present
- **Security:** Clears sensitive data after use

**Required Fields:**
- `cc_number`: Credit card number
- `expiry_month`: Expiration month
- `expiry_year`: Expiration year
- `cvv`: Security code
- `zip_code`: Billing ZIP code

### Error Handling and Monitoring

**Comprehensive Error Tracking:**
- Third-party API monitoring via event emitter
- Detailed error logging with request/response data
- Status code mapping for different error types
- Rollback mechanisms for transaction failures

**Error Categories:**
- `ERROR_PARKING_TOKEN_THIRD_PARTY`: Authentication issues
- `ERROR_PARKING_DETAIL_THIRD_PARTY`: API communication problems
- `ERROR_PARKING_PAYMENT_THIRD_PARTY`: Payment processing failures
- `ERROR_POINT_INSUFFICIENT`: Insufficient wallet balance
- `ERROR_PARKING_DUPLICATE`: Duplicate parking attempt

## 🚀 Usage Methods

### Basic Zone Rate Lookup
```javascript
const parkMobileService = require('@app/src/services/parkMobile');

async function lookupParkingRates(zoneId) {
  try {
    const rateInfo = await parkMobileService.getRateZone(zoneId);
    
    console.log('Zone Information:');
    console.log('- Parking Allowed:', rateInfo.isParkingAllowed);
    console.log('- Zone Name:', rateInfo.zoneName);
    console.log('- Rate Options:', rateInfo.preDefinedTmeBlocks.length);
    
    return {
      zoneId,
      allowed: rateInfo.isParkingAllowed,
      zoneName: rateInfo.zoneName,
      rateOptions: rateInfo.preDefinedTmeBlocks,
      hourlySelections: rateInfo.durationSelections.hasHourMinuteSelections
    };
  } catch (error) {
    console.error('Error looking up parking rates:', error);
    throw error;
  }
}

// Usage
const zoneRates = await lookupParkingRates('12345');
```

### Price Calculation and Booking
```javascript
async function calculateAndBookParking(userId, zoneId, duration, licenseInfo) {
  const parkMobileService = require('@app/src/services/parkMobile');
  
  try {
    // Step 1: Get zone information
    const zoneInfo = await parkMobileService.getRateZone(zoneId);
    
    if (!zoneInfo.isParkingAllowed) {
      throw new Error('Parking not allowed in this zone');
    }
    
    // Step 2: Calculate price for specific duration
    const priceParams = {
      zone: zoneId,
      timeBlockUnit: duration.unit, // 'hours' or 'minutes'
      timeBlockQuantity: duration.quantity,
      timeBlockId: zoneInfo.durationSelections.timeBlockId
    };
    
    const priceInfo = await parkMobileService.getRatePrice(priceParams);
    
    console.log('Pricing Information:');
    console.log('- Parking Fee:', priceInfo.price.parkingPrice);
    console.log('- Transaction Fee:', priceInfo.price.transactionFee);
    console.log('- Total Cost:', priceInfo.price.totalPrice);
    console.log('- Start Time:', priceInfo.parkingStartTimeUtc);
    console.log('- End Time:', priceInfo.parkingStopTimeUtc);
    
    // Step 3: Start parking session
    const parkingParams = {
      userId,
      priceId: priceInfo.uuid,
      lpn: licenseInfo.plateNumber,
      lpnState: licenseInfo.state,
      paymentType: 'COIN' // Currently only supported payment type
    };
    
    const parkingEvent = await parkMobileService.startParking(parkingParams);
    
    return {
      success: true,
      eventId: parkingEvent.id,
      zoneInfo: {
        id: parkingEvent.zone,
        latitude: parkingEvent.zone_lat,
        longitude: parkingEvent.zone_lng
      },
      timing: {
        start: parkingEvent.parkingStartTimeUtc,
        end: parkingEvent.parkingStopTimeUtc
      },
      payment: {
        parkingFee: priceInfo.price.parkingPrice,
        transactionFee: priceInfo.price.transactionFee,
        totalCost: priceInfo.price.totalPrice
      }
    };
  } catch (error) {
    console.error('Error in parking calculation/booking:', error);
    throw error;
  }
}

// Usage
const licenseInfo = { plateNumber: 'ABC123', state: 'TX' };
const duration = { unit: 'hours', quantity: 2 };
const result = await calculateAndBookParking(12345, '67890', duration, licenseInfo);
```

### Parking Session Management
```javascript
class ParkingSessionManager {
  constructor() {
    this.parkMobileService = require('@app/src/services/parkMobile');
  }

  async getUserActiveSessions(userId) {
    try {
      const events = await this.parkMobileService.listOnGoingParkingEvents(userId);
      
      return {
        userId,
        totalEvents: events.events.length,
        lastUpdate: events.last_update,
        sessions: events.events.map(event => ({
          id: event.id,
          zone: event.zone,
          location: {
            latitude: event.zone_lat,
            longitude: event.zone_lng
          },
          vehicle: {
            licensePlate: event.lpn,
            state: event.lpnState
          },
          timing: {
            start: event.parkingStartTimeUtc,
            end: event.parkingStopTimeUtc,
            status: event.status
          },
          alert: {
            enabled: event.alert_before > 0,
            minutesBefore: event.alert_before,
            scheduledAt: event.alert_at
          }
        }))
      };
    } catch (error) {
      console.error('Error getting user parking sessions:', error);
      throw error;
    }
  }

  async setSessionReminder(userId, eventId, reminderMinutes) {
    try {
      const updatedEvent = await this.parkMobileService.setParkingReminder({
        userId,
        eventId,
        alertBefore: reminderMinutes
      });
      
      return {
        success: true,
        eventId: updatedEvent.id,
        reminder: {
          enabled: reminderMinutes > 0,
          minutesBefore: reminderMinutes,
          scheduledAt: updatedEvent.alert_at
        },
        status: updatedEvent.status
      };
    } catch (error) {
      console.error('Error setting parking reminder:', error);
      throw error;
    }
  }

  async cancelSessionReminder(userId, eventId) {
    return this.setSessionReminder(userId, eventId, 0);
  }

  async getSessionDetails(userId, eventId) {
    try {
      const events = await this.getUserActiveSessions(userId);
      const session = events.sessions.find(s => s.id === eventId);
      
      if (!session) {
        throw new Error(`Session ${eventId} not found for user ${userId}`);
      }
      
      // Calculate time remaining
      const now = new Date();
      const endTime = new Date(session.timing.end);
      const timeRemaining = Math.max(0, endTime.getTime() - now.getTime());
      
      return {
        ...session,
        timeRemaining: {
          milliseconds: timeRemaining,
          minutes: Math.floor(timeRemaining / (1000 * 60)),
          hours: Math.floor(timeRemaining / (1000 * 60 * 60)),
          expired: timeRemaining <= 0
        }
      };
    } catch (error) {
      console.error('Error getting session details:', error);
      throw error;
    }
  }
}
```

### Zone Discovery and Rate Comparison
```javascript
class ParkingZoneExplorer {
  constructor() {
    this.parkMobileService = require('@app/src/services/parkMobile');
  }

  async compareZoneRates(zoneIds, duration) {
    const comparisons = [];
    
    for (const zoneId of zoneIds) {
      try {
        // Get zone information
        const zoneInfo = await this.parkMobileService.getRateZone(zoneId);
        
        if (!zoneInfo.isParkingAllowed) {
          comparisons.push({
            zoneId,
            available: false,
            reason: 'Parking not allowed'
          });
          continue;
        }
        
        // Calculate price for specified duration
        const priceParams = {
          zone: zoneId,
          timeBlockUnit: duration.unit,
          timeBlockQuantity: duration.quantity,
          timeBlockId: zoneInfo.durationSelections.timeBlockId
        };
        
        const priceInfo = await this.parkMobileService.getRatePrice(priceParams);
        
        comparisons.push({
          zoneId,
          available: true,
          zoneName: zoneInfo.zoneName,
          pricing: {
            parkingFee: priceInfo.price.parkingPrice,
            transactionFee: priceInfo.price.transactionFee,
            totalCost: priceInfo.price.totalPrice,
            pricePerHour: this.calculateHourlyRate(
              priceInfo.price.parkingPrice, 
              duration
            )
          },
          timing: {
            start: priceInfo.parkingStartTimeUtc,
            end: priceInfo.parkingStopTimeUtc
          },
          rateOptions: {
            hasHourlyRates: zoneInfo.durationSelections.hasHourMinuteSelections,
            hasDailyRates: zoneInfo.durationSelections.hasDaySelections,
            predefinedOptions: zoneInfo.preDefinedTmeBlocks.length
          }
        });
        
      } catch (error) {
        comparisons.push({
          zoneId,
          available: false,
          error: error.message
        });
      }
    }
    
    // Sort by total cost (available zones first)
    return comparisons.sort((a, b) => {
      if (a.available && !b.available) return -1;
      if (!a.available && b.available) return 1;
      if (a.available && b.available) {
        return a.pricing.totalCost - b.pricing.totalCost;
      }
      return 0;
    });
  }

  calculateHourlyRate(parkingFee, duration) {
    const hours = duration.unit === 'hours' ? 
      duration.quantity : 
      duration.quantity / 60;
    
    return parseFloat((parkingFee / hours).toFixed(2));
  }

  async findCheapestZone(zoneIds, duration) {
    const comparisons = await this.compareZoneRates(zoneIds, duration);
    const availableZones = comparisons.filter(z => z.available);
    
    if (availableZones.length === 0) {
      throw new Error('No available parking zones found');
    }
    
    return availableZones[0]; // Already sorted by cost
  }

  async getZoneAvailabilityStatus(zoneIds) {
    const results = {};
    
    for (const zoneId of zoneIds) {
      try {
        const zoneInfo = await this.parkMobileService.getRateZone(zoneId);
        results[zoneId] = {
          available: zoneInfo.isParkingAllowed,
          zoneName: zoneInfo.zoneName,
          rateOptionsCount: zoneInfo.preDefinedTmeBlocks.length,
          supportsHourlyRates: zoneInfo.durationSelections.hasHourMinuteSelections
        };
      } catch (error) {
        results[zoneId] = {
          available: false,
          error: error.message
        };
      }
    }
    
    return results;
  }
}
```

### Payment and Transaction Analytics
```javascript
class ParkingPaymentAnalytics {
  constructor() {
    this.parkMobileService = require('@app/src/services/parkMobile');
  }

  async estimateParkingCosts(userId, zoneId, startTime, endTime) {
    try {
      const duration = this.calculateDuration(startTime, endTime);
      
      // Get zone rates
      const zoneInfo = await this.parkMobileService.getRateZone(zoneId);
      
      if (!zoneInfo.isParkingAllowed) {
        return {
          available: false,
          reason: 'Parking not allowed in this zone'
        };
      }
      
      // Calculate costs for different durations
      const estimates = [];
      
      for (const timeBlock of zoneInfo.preDefinedTmeBlocks) {
        try {
          const priceInfo = await this.parkMobileService.getRatePrice({
            zone: zoneId,
            timeBlockUnit: timeBlock.timeBlockUnit,
            timeBlockQuantity: timeBlock.timeBlockQuantity,
            timeBlockId: timeBlock.timeBlockId
          });
          
          estimates.push({
            duration: {
              quantity: timeBlock.timeBlockQuantity,
              unit: timeBlock.timeBlockUnit,
              description: timeBlock.timeBlockDescription
            },
            cost: {
              parking: priceInfo.price.parkingPrice,
              transaction: priceInfo.price.transactionFee,
              total: priceInfo.price.totalPrice
            },
            timing: {
              start: priceInfo.parkingStartTimeUtc,
              end: priceInfo.parkingStopTimeUtc
            }
          });
        } catch (error) {
          console.warn(`Error calculating price for time block ${timeBlock.timeBlockId}:`, error.message);
        }
      }
      
      // Find best match for requested duration
      const bestMatch = this.findBestDurationMatch(estimates, duration);
      
      return {
        available: true,
        zoneId,
        zoneName: zoneInfo.zoneName,
        requestedDuration: duration,
        estimates,
        recommendedOption: bestMatch,
        totalOptions: estimates.length
      };
    } catch (error) {
      console.error('Error estimating parking costs:', error);
      throw error;
    }
  }

  calculateDuration(startTime, endTime) {
    const start = new Date(startTime);
    const end = new Date(endTime);
    const diffMs = end.getTime() - start.getTime();
    const diffMinutes = Math.floor(diffMs / (1000 * 60));
    const diffHours = Math.floor(diffMinutes / 60);
    
    return {
      minutes: diffMinutes,
      hours: diffHours,
      preferredUnit: diffHours >= 1 ? 'hours' : 'minutes',
      preferredQuantity: diffHours >= 1 ? diffHours : diffMinutes
    };
  }

  findBestDurationMatch(estimates, requestedDuration) {
    // Convert all durations to minutes for comparison
    const requestedMinutes = requestedDuration.preferredUnit === 'hours' ? 
      requestedDuration.preferredQuantity * 60 : 
      requestedDuration.preferredQuantity;
    
    let bestMatch = null;
    let smallestDifference = Infinity;
    
    for (const estimate of estimates) {
      const estimateMinutes = estimate.duration.unit === 'hours' ?
        estimate.duration.quantity * 60 :
        estimate.duration.quantity;
      
      // Only consider options that cover the requested duration
      if (estimateMinutes >= requestedMinutes) {
        const difference = estimateMinutes - requestedMinutes;
        if (difference < smallestDifference) {
          smallestDifference = difference;
          bestMatch = estimate;
        }
      }
    }
    
    return bestMatch;
  }

  async checkUserParkingBalance(userId, estimatedCost) {
    try {
      const UserWallet = require('@app/src/models/UserWallets');
      
      const wallet = await UserWallet.query()
        .select('balance')
        .where('user_id', userId)
        .first();
      
      if (!wallet) {
        return {
          hasWallet: false,
          hasSufficientFunds: false,
          message: 'User wallet not found'
        };
      }
      
      const balance = parseFloat(wallet.balance);
      const cost = parseFloat(estimatedCost);
      
      return {
        hasWallet: true,
        currentBalance: balance,
        estimatedCost: cost,
        hasSufficientFunds: balance >= cost,
        shortfall: Math.max(0, cost - balance),
        message: balance >= cost ? 
          'Sufficient funds available' : 
          `Need ${(cost - balance).toFixed(2)} more coins`
      };
    } catch (error) {
      console.error('Error checking user parking balance:', error);
      throw error;
    }
  }
}
```

## 📊 Output Examples

### Zone Rate Information
```json
{
  "isParkingAllowed": true,
  "zoneName": "Downtown Main Street",
  "preDefinedTmeBlocks": [
    {
      "timeBlockId": 1,
      "timeBlockDescription": "1 Hour",
      "timeBlockQuantity": 1,
      "timeBlockUnit": "hours"
    },
    {
      "timeBlockId": 2,
      "timeBlockDescription": "2 Hours",
      "timeBlockQuantity": 2,
      "timeBlockUnit": "hours"
    }
  ],
  "durationSelections": {
    "timeBlockId": 1,
    "hasHourMinuteSelections": true,
    "hasDaySelections": false
  }
}
```

### Price Calculation Response
```json
{
  "uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "price": {
    "parkingPrice": 3.50,
    "transactionFee": 0.35,
    "totalPrice": 3.85
  },
  "parkingStartTimeUtc": "2024-06-25T14:30:00Z",
  "parkingStopTimeUtc": "2024-06-25T16:30:00Z",
  "timeBlockQuantity": 2,
  "timeBlockUnit": "hours"
}
```

### Parking Event Response
```json
{
  "id": 12345,
  "lpn": "ABC123",
  "lpnState": "TX",
  "area": 953,
  "zone": 67890,
  "zone_lat": 29.7604,
  "zone_lng": -95.3698,
  "status": "ON_GOING",
  "parkingStartTimeUtc": "2024-06-25T14:30:00+00:00",
  "parkingStopTimeUtc": "2024-06-25T16:30:00+00:00",
  "alert_before": 15,
  "alert_at": "2024-06-25T16:15:00+00:00"
}
```

### User Parking Sessions
```json
{
  "events": [
    {
      "id": 12345,
      "lpn": "ABC123",
      "zone": 67890,
      "status": "ON_GOING",
      "parkingStartTimeUtc": "2024-06-25T14:30:00+00:00",
      "parkingStopTimeUtc": "2024-06-25T16:30:00+00:00",
      "alert_before": 15
    }
  ],
  "last_update": "2024-06-25T15:00:00+00:00"
}
```

### Zone Rate Comparison
```json
[
  {
    "zoneId": "12345",
    "available": true,
    "zoneName": "Main Street Parking",
    "pricing": {
      "parkingFee": 3.50,
      "transactionFee": 0.35,
      "totalCost": 3.85,
      "pricePerHour": 1.93
    }
  },
  {
    "zoneId": "67890",
    "available": true,
    "zoneName": "City Center Garage",
    "pricing": {
      "parkingFee": 5.00,
      "transactionFee": 0.50,
      "totalCost": 5.50,
      "pricePerHour": 2.75
    }
  }
]
```

## ⚠️ Important Notes

### ParkMobile API Limitations
- **No Sandbox Environment:** Uses test zones/cards for non-production
- **Test Zone Override:** Non-production uses hardcoded test zone '9939972'
- **Price Discrepancies:** Non-production uses calculated prices vs API response
- **Authentication:** Requires valid API tokens stored in database

### Payment Processing
- **Digital Coins Only:** Currently only supports coin/points payment
- **Wallet Integration:** Integrates with internal user wallet system
- **Transaction Fees:** Separate charges for parking and transaction fees
- **Balance Validation:** Pre-validates sufficient funds before API calls

### Error Handling and Reliability
- **Comprehensive Monitoring:** Third-party API monitoring with event emission
- **Rollback Mechanisms:** Automatic rollback on payment/API failures
- **Status Tracking:** Detailed event status management (ON_GOING, ALERTED, FINISHED)
- **Duplicate Prevention:** Prevents multiple active sessions per user/zone

### Environment Considerations
- **AWS Secrets Manager:** Production credit card data stored securely
- **Test Card Fallback:** Development environments use hardcoded test data
- **Environment Detection:** Automatic detection of production vs non-production
- **Zone Mapping:** Hardcoded area 953 with dynamic zone selection

### Security and Compliance
- **PCI Compliance:** Credit card data handled through AWS Secrets Manager
- **Data Scrubbing:** Sensitive payment data removed from logs
- **Token Management:** Secure API token storage and rotation
- **Audit Trail:** Comprehensive transaction logging for compliance

### Performance and Scalability
- **HTTP Client Optimization:** Persistent connections with keepalive
- **Timeout Handling:** 10-second request timeouts with proper error handling
- **Database Optimization:** Efficient queries with proper indexing
- **Caching Opportunity:** Zone rate data could benefit from caching

### Integration Dependencies
- **Smarking Integration:** Location data from Smarking station records
- **Wallet Service:** Internal points/coins transaction system
- **User Management:** User authentication and profile integration
- **Notification System:** Alert scheduling for parking expiration

## 🔗 Related File Links

- **Parking Models:** `allrepo/connectsmart/tsp-api/src/models/pmParkingEvent.js`
- **Wallet Service:** `allrepo/connectsmart/tsp-api/src/services/wallet.js`
- **Input Validation:** `allrepo/connectsmart/tsp-api/src/schemas/park-mobile.js`
- **Error Definitions:** `allrepo/connectsmart/tsp-api/src/static/error-code.js`

---
*This service provides essential mobile parking payment capabilities with comprehensive API integration, transaction management, and event tracking for the TSP platform.*