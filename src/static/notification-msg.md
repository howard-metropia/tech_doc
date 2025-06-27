# Static/Constants Documentation: notification-msg.js

## 📋 File Overview
- **Purpose:** Defines multilingual push notification message templates for all notification types in the mobile application
- **Usage:** Used by notification services to generate localized push notification titles and body content
- **Type:** Message templates / Notification constants

## 🔧 Main Exports
```javascript
module.exports = {
  title: {
    [NOTIFICATION_TYPE.DUO_GROUP_JOIN_REQUEST]: { en: 'Request to Join', zh: '申請加入群組', ... },
    [NOTIFICATION_TYPE.DUO_CARPOOL_MATCHING]: { en: 'You have new match!', ... },
    // ... titles for 40+ notification types
  },
  body: {
    [NOTIFICATION_TYPE.DUO_GROUP_JOIN_REQUEST]: { 
      en: '%ApplicantUserName% requests to join %CarpoolingGroupName%...', ... 
    },
    // ... detailed body messages with variable substitution
  }
};
```

## 📝 Constants Reference
| Category | Notification Types | Template Variables | Languages |
|----------|-------------------|-------------------|-----------|
| Group Management | JOIN_REQUEST, JOIN_ACCEPTED, JOIN_REJECTED, DISBANDED | %ApplicantUserName%, %CarpoolingGroupName%, %ManagerUserName% | en, es, zh, vi |
| Carpool Lifecycle | DRIVER_STARTING_TRIP, DRIVER_ARRIVE, CANCELLED | %firstName%, %userName%, %role_name% | en, es, zh, vi |
| Matching System | CARPOOL_MATCHING, MATCHING_RIDER, MATCHING_DRIVER | %driver_destination% | en, es, zh, vi |
| Payment/Wallet | DRIVER_FEE_RECEIVED, PASSENGER_FEE_DEDUCTED, AUTO_REFILL | %chipin%, %amount% | en, es, zh, vi |
| Token Management | TOKEN_EXPIRES_IN_14_DAYS, TOKEN_RECEIVED_FROM_AGENCY | %balance%, %agencyName%, %tokens%, %expireDate% | en, es, zh, vi |
| Surveys | MICROSURVEY_NOTIFICATION, MICROSURVEY_GET_REWARDS | %Coins%, %Appname% | en, es, zh, vi |
| Instant Carpool | INSTANT_CARPOOL_NOTIFY_DRIVER, INSTANT_CARPOOL_NOTIFY_RIDER | %userName% | en, es, zh, vi |

## 💡 Usage Examples
```javascript
// Import notification templates
const notificationMsg = require('./static/notification-msg');
const { notificationType } = require('./static/defines');

// Send carpool matching notification
const notifyType = notificationType.DUO_CARPOOL_MATCHING;
const title = notificationMsg.title[notifyType][userLanguage];
const body = notificationMsg.body[notifyType][userLanguage]
  .replace('%ApplicantUserName%', applicant.name)
  .replace('%CarpoolingGroupName%', group.name);

// Token expiration warning
const tokenTitle = notificationMsg.title[notificationType.TOKEN_EXPIRES_IN_14_DAYS][lang];
const tokenBody = notificationMsg.body[notificationType.TOKEN_EXPIRES_IN_14_DAYS][lang]
  .replace('%balance%', userTokens)
  .replace('%agencyName%', agency)
  .replace('%expireDate%', expirationDate);

// Instant carpool status with sub-states
const instantNotify = notificationMsg.title[notificationType.INSTANT_CARPOOL_NOTIFY_RIDER];
const riderTitle = instantNotify.started[userLang]; // or .canceled, .finished
```

## ⚠️ Important Notes
- All template variables must be replaced with actual values before sending notifications
- Some notification types have sub-states (started/canceled/finished for instant carpool)
- Spanish and Vietnamese translations may have empty strings for newer notification types
- Notification types reference constants from defines.js file
- Character limits should be considered for mobile push notification display
- Traditional Chinese support specifically for Taiwan market

## 🏷️ Tags
**Keywords:** push-notifications, message-templates, internationalization, carpool-notifications, user-engagement  
**Category:** #static #constants #notifications #i18n #messaging