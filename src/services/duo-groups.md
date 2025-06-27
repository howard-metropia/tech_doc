# Carpool (Duo) Groups Management Service Documentation

## 🔍 Quick Summary (TL;DR)
This is a massive, multifaceted, and critical service that provides the entire backend functionality for the carpooling "Duo Groups" feature. It is a monolithic handler for the full lifecycle of groups, including creating, reading, updating, and deleting groups (CRUD), as well as comprehensive member management (inviting, joining, leaving, promoting/demoting managers). A key and highly complex responsibility of this service is to orchestrate the cleanup of associated carpool reservations and financial data (via `carpoolHandler`) whenever a group's membership changes, ensuring the integrity of the entire carpooling ecosystem.

**Keywords:** carpool | duo-group | groups | community | crud | member-management | reservation-cleanup

**Primary use cases:** 
- To perform all CRUD operations on Duo Groups.
- To manage the entire lifecycle of group membership for all users.
- To fetch detailed group information, including members, types, and enterprise links.
- To trigger complex cleanup procedures for carpool reservations when a user leaves a group.
- To handle the notification and email logic for group invitations.

**Service Relationships:**
This service is the third pillar of the carpooling system, alongside `carpool.js` (The Matchmaker) and `carpoolHandler.js` (The Accountant). It provides the "social layer" that allows the other two services to function within the context of trusted groups.

## ❓ Common Questions Quick Index
- **Q: What is this service for?** → It runs everything related to carpool groups. Creating them, inviting friends, leaving groups, etc.
- **Q: What is the most important part of this service?** → The cleanup logic. When a user leaves a group, the `removeDuoProcedure` function performs a critical and complex task: it finds all of that user's active carpool requests within the group and cancels them, preventing orphaned matches and ensuring any money in escrow is returned correctly.
- **Q: Does this service handle carpool matching or payments?** → No, not directly. It *triggers* the other services to do so. For example, when cleaning up, it calls `carpoolHandler` to handle the payment side and `matchingHandler` to handle the matching side.
- **Q: Is this service simple?** → No. It is extremely large and complex, interacting with many different database tables and other critical services.

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this service as the **Community Manager and Administrative Office for an exclusive carpooling club**.
1.  **Founding a New Club (`create`):** A user wants to start a new club. The office handles all the paperwork: registering the club name, setting its rules (public or private), and designing its logo and banner (uploading images to S3).
2.  **Membership Management (`invite`, `acceptInvite`, `leave`, `removeMember`):** The office manages the entire membership process. It sends out official invitation letters (push notifications and emails), processes RSVPs, and updates the club's member list. It also handles departures, whether a member leaves voluntarily or is removed by a club manager.
3.  **Club Directory (`get`, `getGroupById`):** The office maintains a directory of all the clubs, which can be searched and filtered. It can also provide a detailed file on any specific club, including its purpose, rules, and a list of its current members.
4.  **The "Departure Protocol" (`removeDuoProcedure`):** This is the office's most critical and complex job. When a member leaves a club, the office immediately goes through all the club's event plans (the carpool reservations). It finds every single carpool request that the departing member was involved in and cancels it. It then calls the matchmaking department (`matchingHandler`) to scrub any pending matches and the finance department (`carpoolHandler`) to ensure all deposits are correctly refunded. This prevents chaos and ensures the club's operations remain smooth.

**Technical explanation:** 
This service is a monolithic CRUD and business logic handler for Duo Groups. It uses Mongoose models to interact with numerous MongoDB collections (`DuoGroups`, `DuoGroupMembers`, `Notifications`, `Reservations`, etc.) and `knex` for connections to other MySQL databases.
-   **CRUD Operations:** The service exports functions that map directly to Create (`create`), Read (`get`, `getGroupById`), Update (`update`), and Delete (`delete`) operations.
-   **Member Lifecycle:** It contains a suite of functions to manage the member lifecycle, such as `invite`, `acceptInvite`, `leave`, `removeMember`, and role changes. These functions typically involve creating/updating records in `DuoGroupMembers` and sending notifications via the `Notifications` system and `sendMail` helper.
-   **Data Presentation:** It uses a "presenter" pattern in the `prepareGroupResp` function, which takes raw database objects and transforms them into the final API response format by fetching and attaching related data (like member counts and types) and cleaning up internal fields.
-   **Core Cleanup Logic:** The `removeDuoProcedure` function is a critical, multi-step process. It finds all `SEARCHING` reservations belonging to users who are leaving a group. For these reservations, it invokes `matchingHandler.removeInvitesForGroup` and `matchingHandler.removeMatch` to clear pending matches, and `carpoolHandler.rejectInviteEscrowProcess` to settle any financial holds in the escrow system.

**Business value explanation:**
Carpooling with strangers can be daunting. This service enables the "trusted groups" feature, which is a cornerstone of building user trust and encouraging adoption of the carpooling feature. By allowing users to form private groups with friends, colleagues, or neighbors, it lowers the barrier to entry and fosters a sense of community and safety. The robust cleanup logic ensures that the user experience is seamless even when group memberships change, which is vital for maintaining the integrity and reliability of the platform.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/duo-groups.js`
- **Language:** JavaScript (ES2017+)
- **Key Libraries:** Mongoose, `knex`, `moment-timezone`
- **Type:** Core Business Logic / Monolithic CRUD Service
- **File Size:** ~60 KB
- **Complexity Score:** ⭐⭐⭐⭐⭐ (Very High. The service is exceptionally large, interacts with a vast number of database tables across different connections, and orchestrates complex, high-consequence procedures.)

## 📝 Detailed Code Analysis

### High Degree of Coupling
This service is a central hub and is therefore tightly coupled with a large number of other modules. It directly requires over 15 models and helpers, and its logic is deeply intertwined with `carpoolHandler` and `matchingHandler`. This makes the system powerful but also very difficult to reason about, as changes in this one file can have cascading effects across the entire carpooling ecosystem.

### Circular Dependency Handling
The code includes a notable pattern to avoid circular dependencies:
```javascript
// to avoid inside circular dependency, so import on here
const matchingHandler = require('@app/src/services/matchingHandler');
const carpoolHandler = require('@app/src/services/carpoolHandler');
```
This import is done *inside* the `removeDuoProcedure` function rather than at the top level of the module. This is a common workaround in Node.js when two modules depend on each other, but it can be a sign of a deeper architectural issue where responsibilities might need to be further separated.

### Presenter Pattern
The `prepareGroupResp` function is a good example of the Presenter (or Serializer) pattern. It decouples the internal database representation of a group from the public-facing API representation. This is a good practice as it allows the database schema to change without necessarily breaking the API contract, and vice-versa.

## 🚀 Usage Methods

```javascript
// This service provides the core implementation for the /duo-groups API endpoints.

const duoGroupService = require('@app/src/services/duo-groups');

// Example: Creating a new group
async function createNewGroup(userId, groupData) {
  const newGroup = await duoGroupService.create(userId, groupData);
  return newGroup;
}

// Example: A user accepts an invite to a group
async function acceptGroupInvite(userId, notificationId) {
  const result = await duoGroupService.acceptInvite(userId, notificationId);
  return result;
}

// Example: A user leaves a group
async function leaveGroup(userId, groupId) {
  // This single call will trigger the entire cleanup procedure.
  const result = await duoGroupService.leave(userId, groupId);
  return result;
}
```

## 🔗 Related File Links
- **Carpooling Pillars:** `@app/src/services/carpool.js`, `@app/src/services/carpoolHandler.js`
- **Database Models:** `DuoGroups`, `DuoGroupMembers`, `Reservations`, `Notifications`, etc.

---
*This documentation was generated to demystify the complex, monolithic service that powers the entire Duo Groups feature, from CRUD and member management to critical reservation cleanup.* 