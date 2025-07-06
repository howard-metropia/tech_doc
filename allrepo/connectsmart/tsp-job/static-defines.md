# System Constants and Definitions

## Overview
**File**: `src/static/defines.js`  
**Type**: System Constants Module  
**Purpose**: Central repository for all system-wide constants, enums, and configuration values used across the TSP job system

## Core Functionality

### Comprehensive Constants Library
This module serves as the authoritative source for all static definitions used throughout the TSP (Transportation Service Provider) system, including travel modes, notification types, status codes, third-party integrations, and system configurations.

### Modular Organization
Constants are organized into logical groups covering different aspects of the system: transportation, notifications, payments, weather, user management, and external service integrations.

## Configuration Dependencies

### AWS Configuration
```javascript
const awsConfig = require('config').vendor.aws;
```

**Usage**: Provides AWS region and S3 bucket configuration for CDN URL construction

## Time and Date Formats

### Standard Formats
```javascript
timeFormat: 'YYYY-MM-DD HH:mm:ss',
utcFormat: 'YYYY-MM-DDTHH:mm:ss+00:00',
```

**Purpose**: Consistent datetime formatting across the system
**Standards**: ISO 8601 compliant formats for database storage and API responses

### CDN Configuration
```javascript
cdnUrl: `https://s3-${awsConfig.region}.amazonaws.com/${awsConfig.s3.bucketName}`,
```

**Function**: Dynamically constructed CDN URL for static asset delivery

## Transportation System Constants

### Travel Mode Definitions
```javascript
const travelModeDefine = {
  DRIVING: 1,
  PUBLIC_TRANSIT: 2,
  WALKING: 3,
  BIKING: 4,
  INTERMODAL: 5,
  TRUCKING: 6,
  PARK_AND_RIDE: 7,
  RIDEHAIL: 8,
  DUO: 100,
  INSTANT_CARPOOL: 101,
};
```

**Extended Format**:
```javascript
travelMode: {
  ...travelModeDefine,
  driving: travelModeDefine.DRIVING,           // Alias for API compatibility
  public_transit: travelModeDefine.PUBLIC_TRANSIT,
  walking: travelModeDefine.WALKING,
  biking: travelModeDefine.BIKING,
  intermodal: travelModeDefine.INTERMODAL,
  trucking: travelModeDefine.TRUCKING,
  park_and_ride: travelModeDefine.PARK_AND_RIDE,
  ridehail: travelModeDefine.RIDEHAIL,
  duo: travelModeDefine.DUO,
  instant_carpool: travelModeDefine.INSTANT_CARPOOL,
},
```

**Categories**:
- **Individual Transport**: DRIVING, WALKING, BIKING
- **Public Transport**: PUBLIC_TRANSIT, INTERMODAL
- **Commercial Services**: RIDEHAIL, TRUCKING
- **Shared Mobility**: DUO, INSTANT_CARPOOL, PARK_AND_RIDE

### Reservation Status System
```javascript
reservationStatus: {
  NONE: 0,                    // No request or draft demand
  SEARCHING: 1,               // Actively searching for matches
  CHOOSING: 2,                // User selecting from options
  PENDING: 3,                 // Awaiting confirmation
  SUGGESTION: 4,              // System suggestion provided
  ACCEPTED: 5,                // User accepted suggestion
  REPEALED: 6,                // Reservation cancelled
  REPEALED_CONFLICT: 7,       // Cancelled due to conflict
  MATCHED: 11,                // Successfully matched
  RESERVED: 50,               // Confirmed reservation
  CANCELED: 51,               // User cancelled
  CANCELED_INACTION: 52,      // Cancelled due to inactivity
  CANCELED_PASSIVE: 53,       // System cancelled
  STARTED: 60,                // Trip in progress
},
```

### Instant Carpooling States
```javascript
instantCarpoolStatus: {
  waiting: 'waiting',         // Waiting for match
  started: 'started',         // Trip commenced
  finished: 'finished',       // Trip completed
  canceled: 'canceled',       // Trip cancelled
  removed: 'removed',         // Entry removed from system
},
```

## Notification System

### Notification Types
**Comprehensive notification type enumeration covering**:
- **General Notifications**: GENERAL (1)
- **DUO Carpooling**: Join requests, acceptances, rejections (2-11)
- **Suggestions**: Travel recommendations (12-17)
- **Micro-surveys**: User feedback collection (19-23)
- **Willingness to Accept (WTA)**: Behavioral economics (24-26)
- **Driver Communications**: Real-time updates (27-29)
- **Carpool Management**: Advanced carpool features (60-79)
- **System Notifications**: App events, incidents (91-95)
- **Ridehail Integration**: Third-party ridehail (100)

### Key Notification Categories
```javascript
notificationType: {
  GENERAL: 1,
  DUO_GROUP_JOIN_REQUEST: 2,
  DUO_GROUP_JOIN_ACCEPTED: 3,
  SUGGESTION_CARPOOL: 15,
  DUO_DRIVER_STARTING_TRIP: 18,
  MICROSURVEY_MULTIPLE_CHOICE_QUESTION: 20,
  WTA_GO_LATER: 24,
  DUO_DRIVER_ARRIVE_SOON: 27,
  TRANSIT_ALERT_NOTIFICATION: 94,
  RIDEHAIL_TRIP: 100,
},
```

### Notification Status Tracking
```javascript
notifyUserStatus: {
  NOTIFY_STATUS_QUEUE: 0,      // Queued for delivery
  NOTIFY_STATUS_SEND_FAIL: 1,  // Delivery failed
  NOTIFY_STATUS_SENT: 2,       // Successfully sent
  NOTIFY_STATUS_RECEIVED: 3,   // User received
  NOTIFY_STATUS_REPLIED: 4,    // User responded
},
```

## User and Group Management

### User Roles
```javascript
role: {
  DRIVER: 1,
  RIDER: 2,
  PASSENGER: 2,  // Alias for RIDER
},
```

### DUO Group Types
```javascript
duoGroupTypes: {
  SPORTS: 1,
  WORK: 2,
  SCHOOL: 3,
  EVENTS: 4,
  OTHERS: 5,
},
```

### Group Member Status
```javascript
duoGroupMemberStatus: {
  NONE: 0,        // No membership
  PENDING: 1,     // Membership pending
  MEMBER: 2,      // Active member
  MANAGEMENT: 3,  // Management role
},
```

## Event and Incident Management

### Event Type Enumeration
```javascript
eventTypeEnum: {
  ALL: 0,
  INCIDENT: 1,
  DMS: 2,              // Dynamic Message Signs
  FLOOD_WARNING: 3,
  LAND_CLOSURE: 4,
},
```

### String Event Types
```javascript
stringEventType: {
  INCIDENT: 'incident',
  DMS: 'DMS',
  FLOOD_WARNING: 'Flood',
  LAND_CLOSURE: 'Closure',
},
```

## Third-Party Service Integrations

### ParkMobile Integration
```javascript
parkMobile: {
  baseURL: 'https://api.parkmobile.io/platformrates/v1',
  endpoints: {
    zone: 'rates/zone',
    price: 'rates/price',
    activate: 'rates/activate',
  },
  status: {
    ON_GOING: 'on-going',
    ALERTED: 'alerted',
    FINISHED: 'finished',
    EXPIRED: 'expired',
  },
  paymentType: {
    COIN: 'coin',
    TOKEN: 'token',
  },
  testingCreditCard: {
    cc_number: '4242424242424242',
    expiry_month: '10',
    expiry_year: '26',
    cvv: '123',
    zip_code: '12345',
  },
  metropiaCardProcessingKey: 'metropia_credit_card',
},
```

### Uber Integration Constants
```javascript
uber: {
  hookTypes: {
    STATUS_CHANGED: 'guests.trips.status_changed',
    RECEIPT_READY: 'guests.trips.receipt_ready',
    TRIP_MESSAGE: 'guests.trips.trip_message',
    UCLID_INFO: 'orders.trips.uclid-info',
  },
  tripStatus: {
    PROCESSING: 'processing',
    NO_DRIVERS_AVAILABLE: 'no_drivers_available',
    ACCEPTED: 'accepted',
    ARRIVING: 'arriving',
    IN_PROGRESS: 'in_progress',
    DRIVER_CANCELED: 'driver_canceled',
    RIDER_CANCELED: 'rider_canceled',
    COMPLETED: 'completed',
    // Additional status values...
  },
  driverStatus: {
    ACCEPT: 'ACCEPT',
    ARRIVED: 'ARRIVED',
    BEGIN_TRIP: 'BEGIN_TRIP',
    DROPOFF: 'DROPOFF',
    CANCEL: 'CANCEL',
    GO_ONLINE: 'GO_ONLINE',
    GO_OFFLINE: 'GO_OFFLINE',
  },
  paymentStatus: {
    PAID: 'paid',
    REFUND_IN_PROGRESS: 'refund_inprogress',
    REFUNDED: 'refunded',
  },
},
```

## Financial System Constants

### Sales Types
```javascript
salesType: {
  SALE_TYPE_GENERAL: 1,
  SALE_TYPE_SPECIAL: 2,
  SALE_TYPE_EXCLUSIVE: 3,
},
```

### Escrow Activity Types
**Comprehensive escrow transaction tracking** (28 different activity types):
```javascript
escrowType: {
  ESCROW_ACTIVITY_INIT: 0,
  ESCROW_ACTIVITY_INC_FEE_RIDER: 1,
  ESCROW_ACTIVITY_INC_FEE_DRIVER: 2,
  ESCROW_ACTIVITY_INC_PREMIUM: 3,
  // ... additional 24 escrow activity types
  ESCROW_ACTIVITY_INC_EXPIRED: 25,
  ESCROW_ACTIVITY_DEC_CARPOOL_REJECT_BY_RIDER_DIFF: 26,
},
```

### System Accounts
```javascript
systemAccounts: {
  METROPIA_BUDGET: 2000,
  ESCROW: 2001,
  INCENTIVE_ENGINE: 2002,
},
```

## Weather and Environmental Systems

### Weather Configuration
```javascript
weather: {
  appliedTravelMode: [1, 3, 4],  // DRIVING, WALKING, BIKING
  characterLimit: 250,
  events: {
    UNDEFINED: -1,
    SIGNIFICANT_WITHOUT_DRIVING: 1,
    SIGNIFICANT_WITH_DRIVING: 2,
    LOW_OR_HIGH_TEMPERATURE: 3,
    CRITICAL: 4,
  },
  indicators: {
    WIND_SPEED: 'windSpeed',
    WIND_GUST: 'windGust',
    HEAVY_RAIN: 'rain',
    SNOW: 'snow',
    SNOW_CONTEXT: 'snowContext',
    HIGH_TEMPERATURE: 'highTemperature',
    LOW_TEMPERATURE: 'lowTemperature',
  },
  temperature: {
    low: 50,   // Fahrenheit
    high: 100, // Fahrenheit
  },
  wind: {
    speed: { low: 15, high: 40 },    // mph
    gust: { low: 25, high: 30 },     // mph
  },
  rain: 22.86,  // mm threshold
  infoUrlList: {
    snow: 'https://www.txdot.gov/safety/severe-weather/snow-and-ice.html',
    ice: 'https://www.txdot.gov/safety/severe-weather/snow-and-ice.html',
    hurricane: 'https://www.txdot.gov/safety/severe-weather/hurricane-preparation.html',
    flood: 'https://www.txdot.gov/safety/severe-weather/flash-floods.html',
    tornado: 'https://www.txdot.gov/safety/severe-weather/tornado-emergency.html',
    multi: 'https://www.txdot.gov/safety/severe-weather.html',
  },
  openAIModel: 'gpt-4o-mini',
  notificationSendingHour: 18,  // 6 PM
},
```

## Localization and Language Support

### Supported Languages
```javascript
language: {
  en: 'English',
  en_us: 'English',
  es: 'Spanish',
  vi: 'Vietnamese',
  vi_vn: 'Vietnamese',
  zh: 'Traditional Chinese',
  zh_tw: 'Traditional Chinese',
},
```

## User Analytics and Behavior

### User Action Tracking
```javascript
userActionList: {
  preTripAlertOpen: 'PRE_TRIP_ALERT_OPEN',
  enterSchoolZone: 'ENTER_SCHOOL_ZONE',
  enterSchoolZoneSpeeding: 'ENTER_SCHOOL_ZONE_SPEEDING',
  tripPlannerScreen: 'TRIP_PLANNER_SCREEN',
},
```

### Incentive Event Types
```javascript
incentiveEventType: {
  INCENTIVE_FIRST_TRIP: 1,
  INCENTIVE_NON_FIRST_TRIP: 2,
  INCENTIVE_TRIP_LESS_THAN_1_MILE: 3,
  INCENTIVE_TRIP_INVALID_TRIP: 4,
  INCENTIVE_REACH_THE_WEEKLY_CAP: 5,
},
```

## Geospatial and Activity Analysis

### Activity Area Configuration
```javascript
activityArea: {
  availableAppDateDurationDays: 7,
  clusterDistance: 0.2,           // kilometers
  clusterMinPoints: 5,
  bufferRadius: 0.5,              // kilometers
  convexConcavity: 4,
  TripTrajectorySampleFrequence: 5,
},
```

## Construction Alerts

### Construction Alert Configuration
```javascript
constructionAlert: {
  notificationSendingHour: 19,  // 7 PM
  characterLimit: 250,
},
```

## Usage Patterns and Integration

### Import and Usage
```javascript
const defines = require('@app/src/static/defines');

// Access travel modes
const drivingMode = defines.travelMode.DRIVING;
const carpoolMode = defines.travelMode.DUO;

// Use notification types
const notification = {
  type: defines.notificationType.DUO_GROUP_JOIN_REQUEST,
  status: defines.notifyUserStatus.NOTIFY_STATUS_QUEUE,
};

// Weather thresholds
if (windSpeed > defines.weather.wind.speed.high) {
  // Activate weather alert
}
```

### Database Schema Integration
```javascript
// Example: Using status constants in database queries
const activeReservations = await Reservations.query()
  .whereIn('status', [
    defines.reservationStatus.MATCHED,
    defines.reservationStatus.RESERVED,
    defines.reservationStatus.STARTED,
  ]);
```

### API Response Integration
```javascript
// Example: Standardized API responses using constants
const apiResponse = {
  travelMode: defines.travelMode.RIDEHAIL,
  status: defines.reservationStatus.ACCEPTED,
  notificationSent: defines.notifyUserStatus.NOTIFY_STATUS_SENT,
};
```

## Validation and Business Logic

### Status Validation
```javascript
// Example: Validate reservation status transitions
const validTransitions = {
  [defines.reservationStatus.PENDING]: [
    defines.reservationStatus.ACCEPTED,
    defines.reservationStatus.REPEALED,
  ],
  [defines.reservationStatus.ACCEPTED]: [
    defines.reservationStatus.MATCHED,
    defines.reservationStatus.CANCELED,
  ],
};
```

### Travel Mode Compatibility
```javascript
// Example: Check weather applicability
const weatherApplicableModes = defines.weather.appliedTravelMode;
const isWeatherRelevant = weatherApplicableModes.includes(selectedTravelMode);
```

## Maintenance and Extension

### Adding New Constants
```javascript
// Pattern for extending definitions
const newFeatureConstants = {
  FEATURE_A: 1,
  FEATURE_B: 2,
  FEATURE_C: 3,
};

// Extend existing module
Object.assign(defines.someCategory, newFeatureConstants);
```

### Deprecation Management
```javascript
// Pattern for handling deprecated constants
const legacyConstants = {
  OLD_CONSTANT: 'deprecated_value', // @deprecated Use NEW_CONSTANT instead
  NEW_CONSTANT: 'new_value',
};
```

## Performance Considerations

### Memory Efficiency
- **Static Objects**: All constants are defined as static objects
- **No Dynamic Generation**: Values computed at module load time
- **Reference Sharing**: Constant objects shared across all imports

### Access Patterns
- **Direct Access**: O(1) constant lookup time
- **Enumeration**: Efficient iteration over constant groups
- **Validation**: Fast membership testing using Object.values()

## Security and Compliance

### Sensitive Data Handling
- **Test Credentials**: ParkMobile test credit card data clearly marked
- **API Keys**: No production secrets stored in constants
- **URLs**: Only public endpoint URLs included

### Configuration Security
- **Environment Separation**: AWS configuration loaded from secure config
- **No Hardcoded Secrets**: All sensitive values externalized
- **URL Construction**: Dynamic URL building from configuration

This comprehensive constants module provides the foundation for consistent data representation, business logic validation, and system integration across the entire TSP job scheduling and mobility platform.