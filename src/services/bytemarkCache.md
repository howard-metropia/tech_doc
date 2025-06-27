# Bytemark Ticketing Cache Service Documentation

## 🔍 Quick Summary (TL;DR)
This service is a comprehensive caching layer for a user's transit tickets, which are originally sourced from the Bytemark third-party ticketing platform. To improve performance and reduce reliance on external API calls, it maintains a local copy of a user's tickets in a MongoDB database. The service handles building the cache from scratch, intelligently updating it with the latest ticket statuses, detecting changes using MD5 hashes, and maintaining a historical log. It interacts with multiple versions of the Bytemark API to fetch both active and expired passes.

**Keywords:** cache | bytemark | ticketing | mongodb | performance | api-integration | data-synchronization | md5

**Primary use cases:** 
- Providing a fast, local source for a user's Bytemark tickets.
- Building and maintaining an up-to-date cache of tickets for all users.
- Synchronizing ticket status changes (e.g., activation, expiration) between the Bytemark platform and the local application.
- Reducing latency and the number of API calls to the external Bytemark service.

**Compatibility:** Node.js >= 16.0.0, MongoDB (Mongoose), Knex.js, Bytemark API.

## ❓ Common Questions Quick Index
- **Q: What is Bytemark?** → A third-party company that provides mobile ticketing solutions for transit agencies. This service is all about integrating with them.
- **Q: Why is this cache needed?** → To make the app faster. Instead of asking Bytemark for a user's tickets every time, the app asks this local, much faster cache.
- **Q: How does it know when a ticket has changed?** → It stores an MD5 hash (a unique fingerprint) of each ticket's data. When it gets fresh data from Bytemark, it compares the new fingerprint to the old one. If they don't match, it knows the ticket was updated.
- **Q: Where is the data stored?** → The cache itself is in MongoDB (`BytemarkTicketsCache` collection). The user's permission token to access Bytemark is stored in MySQL (`bytemark_tokens` table).
- **Q: What's the difference between `buildTicketCache` and `updateTicketCache`?** → `build` creates the cache for a user for the first time. `update` intelligently synchronizes an existing cache with the latest data from Bytemark.

## 📋 Functionality Overview

**Non-technical explanation:** 
Imagine you have a library card for a large, slow, city-wide library (Bytemark). Going there every time you want to see which books you have checked out is a pain.
- **`buildTicketCache` (Getting Your First Library Snapshot):** The first time you use the service, it acts like a **librarian's assistant** who goes to the main library for you. They make a complete list of all the books you have (active tickets) and all the books you've returned in the past (expired tickets). They write this all down on a personal file card and keep it at your local branch (MongoDB cache). For each book entry, they also take a quick photo of the cover (the MD5 hash).
- **`updateTicketCache` (Syncing Your Snapshot):** Later, when you want an update, the assistant goes back to the main library with your file card. Instead of re-writing the whole list, they are more clever:
    - For each book on their list, they just compare their photo of the cover (`payload_hash`) with the actual book cover at the library. If it's different (maybe the book got a new sticker), they update your file card.
    - If the library has a new book you checked out, the assistant adds it to your card.
    - They keep your personal card tidy and up-to-date.
- **`checkTicketCache` (The Main Librarian):** This is the main librarian you talk to. You ask for your ticket list. They check if you have a file card. If you don't, they send the assistant to make one (`build`). If you do, they ask the assistant to quickly sync it (`update`). This ensures you always get the latest information.

**Technical explanation:** 
This service manages a MongoDB collection (`BytemarkTicketsCache`) that mirrors ticket data from the Bytemark API. The core workflow is managed by `checkTicketCache`, which delegates to `buildTicketCache` for new users or `updateTicketCache` for existing ones. `buildTicketCache` fetches a user's Bytemark token from MySQL, calls two Bytemark API endpoints (`/passes` and `/v4.0/passes` for expired tickets), transforms the results, computes an MD5 `payload_hash` for each ticket's JSON body, and saves it all as a single document. `updateTicketCache` is more nuanced: it also fetches fresh data but then iterates through its existing cached tickets and the new API data, using the `payload_hash` to efficiently detect changes. It updates existing ticket objects, adds new ones, and filters out expired ones. All ticket creations or updates are also logged to a separate `BytemarkTicketsLog` collection. A `checkTicketCacheTimeout` function provides a rate-limited version of the update logic.

**Business value explanation:**
This caching service is critical for the performance, reliability, and user experience of the application's transit ticketing feature. By decoupling the app from a third-party API, it reduces latency, making the app feel faster to the user. It also provides a layer of resilience; if the Bytemark API is temporarily down, users can still view their cached tickets. The change detection and logging provide a robust audit trail and a mechanism for keeping user data synchronized with an external system of record.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/bytemarkCache.js`
- **Language:** JavaScript (ES2017+)
- **Key Libraries:** `knex`, `mongoose`, `@maas/services` (BytemarkManager), `crypto`, `moment-timezone`.
- **Type:** Caching & Data Synchronization Service
- **File Size:** ~14 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High. The logic involves coordinating two databases and multiple external API endpoints, with complex state management and change-detection logic.)

## 📝 Detailed Code Analysis

### Change Detection with MD5
The use of `crypto.createHash('md5').update(JSON.stringify(cur)).digest('hex')` is the most important architectural pattern in this file. It allows the `updateTicketCache` function to avoid a deep, field-by-field comparison of ticket objects. By comparing a single hash string, it can instantly determine if a ticket's payload has been modified on the Bytemark server, triggering an update of the local record. This is highly efficient.

### Dual API Version Handling
The code makes separate calls to a legacy `/passes` endpoint and a `/v4.0/passes` endpoint. The v4 endpoint is specifically used to fetch `EXPIRED` passes. This adds complexity, as the results from both sources need to be managed and merged correctly within the cache document, which has two distinct arrays: `passes` and `passes4`.

### Cache Structure
The cache is a single MongoDB document per user. This is a good design for this use case, as a user's tickets are almost always retrieved as a complete set. Storing them in one document is efficient. The document contains a top-level `timestamp` field which is used by `checkTicketCacheTimeout` to implement a simple time-to-live (TTL) caching strategy.

### Maintenance Functions
- `buildCacheIfEmpty`: This function is clearly intended for a cron job or maintenance script. It scours the database for users who *should* have a cache but don't, and then builds it for them. This is crucial for back-filling data and ensuring system-wide consistency.
- `dayPassExp`: A utility to calculate the expiration time for a day pass, which has special business rules.

## 🚀 Usage Methods

```javascript
// To ensure a user's ticket cache is up-to-date before displaying tickets
const bytemarkCache = require('@app/src/services/bytemarkCache');

async function getTicketsForUser(userId) {
  // This single call will either build or update the cache as needed.
  await bytemarkCache.checkTicketCache(userId);
  
  // Now, we can safely read from the cache knowing it's fresh.
  const BytemarkTicketsCache = require('@app/src/models/BytemarkTickets');
  const userTickets = await BytemarkTicketsCache.findOne({ user_id: userId }).lean();
  
  return userTickets;
}

// In a nightly cron job
async function dailyCacheMaintenance() {
    await bytemarkCache.buildCacheIfEmpty();
}
```

## ⚠️ Important Notes
- **High Complexity:** This service is vital but complex. Changes should be made with extreme care and thorough testing.
- **Dependencies:** The service's operation is critically dependent on the availability of the `portal` MySQL database, the `cache` MongoDB database, and the Bytemark external APIs.
- **Error Handling:** The code includes logging but may benefit from more robust error handling and retry logic, especially for external API calls.

## 🔗 Related File Links
- **MySQL Data Access:** `knex`
- **MongoDB Models:** `@app/src/models/BytemarkTickets`, `@app/src/models/BytemarkTicketsLog`
- **Bytemark API Client:** `@maas/services` (BytemarkManager)

---
*This documentation was generated to explain the complex caching and data synchronization mechanisms for integrating the Bytemark mobile ticketing platform.* 