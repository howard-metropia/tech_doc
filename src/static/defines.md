# Static/Constants Documentation: defines.js

## 📋 File Overview
- **Purpose:** Central configuration hub defining core application constants, enums, and default settings for the TSP API
- **Usage:** Used throughout controllers, services, and models for consistent data types, statuses, and configuration values
- **Type:** Constants / Enums / Configuration definitions

## 🔧 Main Exports
```javascript
module.exports = {
  timeFormat: 'YYYY-MM-DD HH:mm:ss',
  cdnUrl: 'https://s3-region.amazonaws.com/bucket',
  travelMode: { DRIVING: 1, PUBLIC_TRANSIT: 2, WALKING: 3, BIKING: 4, ... },
  notificationType: { GENERAL: 1, DUO_GROUP_JOIN_REQUEST: 2, ... },
  reservationStatus: { NONE: 0, SEARCHING: 1, MATCHED: 11, ... },
  // ... extensive configuration objects
};
```

## 📝 Constants Reference
| Category | Key Constants | Description | Used In |
|----------|---------------|-------------|---------|
| Travel Modes | DRIVING, PUBLIC_TRANSIT, WALKING, BIKING, RIDEHAIL, DUO | Transportation method identifiers | Trip planning, routing services |
| Notification Types | 100+ notification types | Push notification categorization | Notification service, mobile apps |
| Reservation Status | SEARCHING, MATCHED, STARTED, CANCELED | Carpool/trip lifecycle states | Reservation management |
| User Roles | DRIVER, RIDER/PASSENGER | Carpool participant roles | Matching algorithms |
| Weather Config | events, indicators, thresholds | Weather alert processing | Weather service, safety alerts |
| Payment Systems | ParkMobile, Uber integration | Third-party service configs | Payment processing |
| System Accounts | METROPIA_BUDGET, ESCROW, INCENTIVE_ENGINE | Internal transaction accounts | Financial operations |

## 💡 Usage Examples
```javascript
// Import definitions
const defines = require('./static/defines');

// Travel mode validation
if (request.mode === defines.travelMode.PUBLIC_TRANSIT) {
  // Handle transit routing
}

// Notification type checking
const notifyType = defines.notificationType.DUO_CARPOOL_MATCHING;
await sendNotification(userId, notifyType, message);

// Reservation status updates
await updateReservation(id, { 
  status: defines.reservationStatus.MATCHED 
});

// Weather threshold checking
if (windSpeed > defines.weather.wind.speed.high) {
  triggerWeatherAlert();
}
```

## ⚠️ Important Notes
- CDN URL dynamically constructed from AWS config
- Travel mode supports both numeric and string formats for API compatibility
- Weather configuration includes OpenAI model settings for AI-generated alerts
- ParkMobile includes test credit card data for development environments
- System account IDs are hardcoded for financial transaction integrity
- Language codes support internationalization (English, Spanish, Vietnamese, Chinese)

## 🏷️ Tags
**Keywords:** configuration, enums, travel-modes, notifications, status-definitions, weather-config  
**Category:** #static #constants #definitions #core-config