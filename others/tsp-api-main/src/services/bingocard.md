# Bingo Card Challenge Service Documentation

## 🔍 Quick Summary (TL;DR)
This service provides a single function, `addToChallenge`, which is responsible for automatically enrolling a user into an active "onboarding" incentive campaign. It acts as a bridge between the main application's database and a separate microservice that manages incentive programs (like "Bingo Cards"). When called with a `userId`, it gathers the user's travel preferences and notification permissions, finds a relevant onboarding campaign from the incentive service, and then adds the user to that campaign's "bingo card."

**Keywords:** incentive | gamification | bingo | challenge | onboarding | campaign | microservice-integration

**Primary use cases:** 
- To automatically engage new users by adding them to a starting "Bingo Card" challenge upon registration or another trigger.
- To synchronize user data (persona, permissions) between the main application and the incentive service.

**Compatibility:** Node.js >= 16.0.0, Knex.js, Superagent.

## ❓ Common Questions Quick Index
- **Q: What is a "Bingo Card"?** → In this context, it's a gamification feature. Users are likely given a "card" with tasks to complete (e.g., "Take a bus trip," "Log a carpool") to earn rewards. This service enrolls them in such a game.
- **Q: What does "onboard" mean?** → The service specifically looks for campaigns with "onboard" in their `gen_weight` field. This indicates it's a special campaign designed for new users as part of their initial experience with the app.
- **Q: What does this service actually *do*?** → It takes a `userId`, looks up their data in the local database, asks an external "incentive service" what campaigns are available, and then tells that service to add the user to a specific onboarding campaign.
- **Q: Is this service self-contained?** → No. It is highly dependent on two external systems: the `portal` MySQL database and the `incentive-admin` microservice, which it communicates with via HTTP requests.

## 📋 Functionality Overview

**Non-technical explanation:** 
Imagine a new employee joins a company. This service is like the **HR onboarding coordinator**.
1.  **Check for Onboarding Programs:** The coordinator first calls the "Fun Committee" (the incentive microservice) to see if there are any "Welcome" games running for new hires.
2.  **Gather Employee Info:** The coordinator looks up the new employee's file (`portal` database) to find their job role (preferred travel mode) and if they agreed to receive company newsletters (notification permissions).
3.  **Find the Right Game:** The coordinator filters the list of games to find one specifically labeled "for new hires" (an "onboard" campaign).
4.  **Sign Them Up:** Once found, the coordinator sends the employee's details over to the Fun Committee and officially signs them up for the welcome game. The Fun Committee then gives back a confirmation number (`created_user_id`).
5.  **First Game Only:** The coordinator only signs them up for the very first welcome game they find and then considers their job done.

**Technical explanation:** 
The `addToChallenge` function orchestrates a process to enroll a user in an incentive campaign. It starts by making a `GET` request with `superagent` to an `incentiveAdminUrl` to fetch all current campaigns. It then uses `knex` to query the local `portal` database for the user's `user_config` (to determine a travel "persona") and `auth_user` (to get notification permissions). It iterates through the fetched campaigns, looking for one with "onboard" in its `gen_weight` property and ensuring the user isn't already enrolled. Upon finding a match, it makes a `POST` request to the incentive service's `/bingocards/:bingocard_id` endpoint, sending the user's ID, persona, and permissions. If successful, it returns the user's data along with the new ID created in the incentive service. The entire process is wrapped in a `try...catch` block for error handling.

**Business value explanation:**
This service automates the crucial first-engagement step for new users. By automatically enrolling them in a gamified onboarding experience, it can significantly improve user retention and encourage them to explore the app's features from day one. It bridges the core application with a specialized gamification engine, allowing the business to create and manage complex incentive campaigns without cluttering the main application's codebase.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/bingocard.js`
- **Language:** JavaScript (ES2017+)
- **Key Libraries:** `@maas/core/mysql` (knex), `superagent`, `config`
- **Type:** Microservice Integration / Business Logic Service
- **File Size:** ~3 KB
- **Complexity Score:** ⭐⭐ (Low-Medium. The logic is linear, but it involves coordinating between a database and an external API, which adds points of failure.)

## 📝 Detailed Code Analysis

### Key Logic Steps
1.  **Fetch Campaigns:** The service first polls the incentive microservice to see what's active. This is a good design, as it decouples the TSP-API from the lifecycle of campaigns.
2.  **User Data Hydration:** It gathers necessary user information from two different tables (`user_config`, `auth_user`). This "hydration" step is necessary to provide the incentive service with the context it needs.
3.  **Persona Mapping:** A hardcoded `map` object translates the database's `preferred_travel_mode` into a `persona` for the incentive service. This is a common pattern in microservice integration but can become brittle if the values diverge.
4.  **Campaign Filtering:** The loop `for (const campaign of campaigns)` contains the core business rule: it filters for "onboard" campaigns and checks for pre-existing enrollment.
5.  **Enrollment and Exit:** `return result;` is called immediately after the first successful enrollment. This means a user will only ever be added to one onboarding campaign by this service, even if multiple are active.
6.  **Error Handling:** The `try...catch` block is broad, covering the entire flow. Any failure (network error, database error, API error) will be caught, logged, and will cause the function to return a default result object, making it resilient.

## 🚀 Usage Methods

```javascript
// This service would typically be called after a user-creation event.
const bingocardService = require('@app/src/services/bingocard');
const userEvents = require('@app/src/events/users');

// Listen for a new user being created
userEvents.on('user_created', async (newUser) => {
  try {
    const result = await bingocardService.addToChallenge(newUser.id);
    console.log(`User ${newUser.id} enrollment result:`, result);
    // result might be { userId: newUser.id, persona: 'driving', ..., created_user_id: 12345 }
  } catch (error) {
    console.error(`Failed to add user ${newUser.id} to challenge.`, error);
  }
});
```

## ⚠️ Important Notes
- **External Dependencies:** The reliability of this service is directly tied to the availability and performance of the `portal` database and the `incentive-admin` microservice.
- **Configuration-driven:** The endpoint for the incentive service is stored in a configuration file (`config.get('vendor.incentive')`), which is a good practice.
- **Single Onboarding:** The logic is designed to add a user to only the *first* "onboard" campaign it finds. This is an important business rule to be aware of.

## 🔗 Related File Links
- **Database Access:** `@maas/core/mysql`
- **HTTP Client:** `superagent`
- **Configuration:** `config` library
- **External Service:** The `incentive-admin` microservice (URL from config)

---
*This documentation was generated to explain the service's role in integrating the main application with a gamified incentive system for user onboarding.* 