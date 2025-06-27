# Campaign Logic Handler Service Documentation

## 🔍 Quick Summary (TL;DR)
This service is a core business logic handler for user interactions within marketing or behavioral campaigns. It is responsible for updating a user's status as they progress through a campaign's steps and for recording their actions and awarded points in a `portal` MySQL database. It also provides a utility function for generating alternative time slots around a given time, likely for "go earlier/later" campaign suggestions. The service exports a set of critical constants defining notification types and expiration times used throughout the campaign system.

**Keywords:** campaign | business-logic | mysql | knex | user-status | points | notification

**Primary use cases:** 
- Updating the status of a user's interaction with a specific campaign notification or "card."
- Recording and aggregating points for a user within a campaign.
- Generating alternative time slots for travel suggestions.
- Providing centralized constants for notification types and expiration timeouts.

**Compatibility:** Node.js >= 16.0.0, Knex.js.

## ❓ Common Questions Quick Index
- **Q: What is this service for?** → It handles the backend logic when a user interacts with a campaign, like clicking "accept" on a notification. It updates the database to track their progress and points.
- **Q: What database does it talk to?** → It uses `knex` to talk to a MySQL database named `portal`, specifically modifying the `cm_campaign_user` and `cm_user_record` tables.
- **Q: What is `uodtsGenerator`?** → Its name is unclear, but its function is to generate a couple of alternative time slots (e.g., 30 minutes before and 30 minutes after) a given time. This is likely for a "suggest a better travel time" feature.
- **Q: What are the exported constants for?** → They provide a single source of truth for important magic numbers used elsewhere in the application, such as the ID for a "GO_EARLY" notification (21) or how long a microsurvey should be valid (300 seconds).

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this service as the **scorekeeper and administrator for a game show (the campaign)**.
- **`changeStatus` (Updating the Contestant's Status):** A contestant presses a buzzer to answer a question. The scorekeeper finds the contestant's file for that specific question (`cm_campaign_user` table) and marks down whether they got it right or wrong (`statusId`, `accept`).
- **`actionCardRecord` (Updating the Main Scoreboard):** After the contestant answers, the scorekeeper goes to the main scoreboard (`cm_user_record` table). If this is the contestant's first time scoring, the scorekeeper creates a new entry for them. Otherwise, they find their existing score and add the new points to their total.
- **`uodtsGenerator` (The "Bonus Round" Calculator):** The game show has a bonus round where it suggests, "You could have played 30 minutes earlier or 30 minutes later for a better prize!" This calculator is the tool the host uses to figure out what those earlier and later times are.
- **Constants (The Official Rulebook):** The service also holds the official rulebook, defining things like the official number for a "Microsurvey Question" is 20, and contestants have exactly 300 seconds to answer it.

**Technical explanation:** 
This service provides two main database manipulation functions and a utility function, all interacting with a MySQL `portal` database via `knex`.
- `changeStatus`: Performs a targeted `update` on the `cm_campaign_user` table. It finds a specific record based on `userId`, `campaign_id`, and `step_id` and updates its `status` and `reply_status`.
- `actionCardRecord`: Implements manual "upsert" logic on the `cm_user_record` table. It first `select`s a record; if not found, it `insert`s a new one. If found, it `update`s the existing record, incrementing the `points` total. This aggregates user actions at the campaign level.
- `uodtsGenerator`: A pure utility function that takes a time string (e.g., "HH:mm") and calculates two new time strings that are a fixed interval before and after the input time.
The module also exports several objects containing constant values for `NOTIFICATION_TYPE` IDs and various expiration timeouts in seconds, centralizing these configuration values.

**Business value explanation:**
This service forms the backbone of the campaign engine's business logic. It directly translates user engagement with campaign prompts into state changes within the database, enabling the system to track user progress, award points, and manage the campaign lifecycle. By centralizing this logic and the associated constants, it ensures consistency across the platform and makes the campaign system easier to manage and extend. The `uodtsGenerator` is a key component for campaigns designed to influence user travel behavior by providing concrete, alternative travel times.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/campaignHandler.js`
- **Language:** JavaScript (ES2017+)
- **Key Libraries:** `knex`, `moment-timezone`
- **Type:** Business Logic Handler / Database Service
- **File Size:** ~5 KB
- **Complexity Score:** ⭐⭐ (Low-Medium. The database logic is straightforward, but the purpose of `uodtsGenerator` is not immediately obvious from its name or implementation.)

## 📝 Detailed Code Analysis

### Manual Upsert Logic
The `actionCardRecord` function implements an "upsert" by performing a `SELECT` then an `INSERT` or `UPDATE`. This is a common pattern when not using a database engine that supports a native `ON DUPLICATE KEY UPDATE` command through the chosen ORM/query builder, or when more complex logic is needed before the update. While functional, it is less performant than a native upsert as it requires two separate database round-trips in the update case.

### `uodtsGenerator` Implementation
The logic within `uodtsGenerator` is slightly convoluted. The `if (i < (uodtRange - 1)) continue;` where `uodtRange = 2` is a confusing way to write a loop that only executes its main logic on the last iteration (when `i = 2`). The result is that it calculates one time slot 30 minutes before the input time and another 30 minutes after. The code could be simplified for better readability. For example:
```javascript
// A clearer way to write the same logic
const generateSlots = (time) => {
    const intervalMinutes = 30;
    const inputMoment = moment(time, 'HH:mm:ss');
    const earlier = inputMoment.clone().subtract(intervalMinutes, 'minutes').format('HH:mm:ss');
    const later = inputMoment.clone().add(intervalMinutes, 'minutes').format('HH:mm:ss');
    return [earlier, later];
}
```

### Centralized Constants
Exporting the `NOTIFICATION_TYPE` and `EXPIRATION` constants is a very good practice. It prevents "magic numbers" from being scattered across the codebase, making the system easier to understand, maintain, and modify. If a new notification type is added or an expiration time needs to be changed, it only needs to be updated in this one location.

## 🚀 Usage Methods

```javascript
const campaignHandler = require('@app/src/services/campaignHandler');
const pushNotificationService = require('@app/src/services/notification');

// When a user replies to a notification for a "Go Later" campaign
async function handleGoLaterReply(userId, campaignId, stepId, wasAccepted) {
  const newStatus = wasAccepted ? 5 : 4; // Example statuses for accepted/rejected
  const points = wasAccepted ? 100 : 0;
  
  // 1. Update the status of this specific interaction
  await campaignHandler.changeStatus(userId, campaignId, stepId, newStatus, wasAccepted);
  
  // 2. Record the action and update total points for the campaign
  await campaignHandler.actionCardRecord(userId, campaignId, points, newStatus);
  
  console.log(`Processed reply for campaign ${campaignId} for user ${userId}.`);
}

// When preparing a "Go Later" notification, get the time slots
function getAlternativeTimes(originalTime) {
    return campaignHandler.uodtsGenerator(originalTime);
    // Returns something like ['10:00:00', '11:00:00'] for an input of '10:30:00'
}

// When creating a push notification
function sendMicrosurveyPush() {
    const type = campaignHandler.NOTIFICATION_TYPE.MICROSURVEY; // Uses the constant
    const ttl = campaignHandler.MICROSURVEY_EXPIRATION_TIME; // Uses the constant
    pushNotificationService.send(..., { type, ttl });
}
```

## 🔗 Related File Links
- **Database Access:** `knex`
- **Dependent Services:** Likely used by notification services, trip planners, and other campaign-related logic.

---
*This documentation was generated to explain the service's role as a central handler for campaign business logic and database updates.* 