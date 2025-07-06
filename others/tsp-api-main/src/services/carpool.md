# Carpool Matching Engine Service Documentation

## 🔍 Quick Summary (TL;DR)
This service is the **matchmaking engine** at the heart of the carpooling (Duo) feature. Its primary and highly complex responsibility is to take a user's carpool request and find the best possible matches from a pool of other users' requests. It does this by executing a sophisticated, multi-stage filtering pipeline that considers user preferences, time windows, geographic proximity, and real-world travel times calculated via the HERE Maps API. This service handles the entire pre-match lifecycle, from creating and canceling carpool reservations to suggesting trip prices based on oil prices. It works in tandem with its sister service, `carpoolHandler.js`, which handles the financial and post-match logic.

**Keywords:** carpool | matching-engine | filter-pipeline | here-api | reservation | matchmaking | algorithm

**Primary use cases:** 
- Creating, managing, and canceling carpool reservations before a match is finalized.
- Executing the core carpool matching algorithm to find suitable drivers/riders.
- Enriching potential matches with real-world travel time data from the HERE Maps API.
- Suggesting a fair market price for a trip based on distance and fuel costs.

**Service Distinction:**
-   **`carpool.js` (This Service - The Matchmaker):** Focuses on the **pre-match** phase. It *finds* potential partners.
-   **`carpoolHandler.js` (The Accountant):** Focuses on the **post-match** phase. It handles the financial escrow and state changes *after* a match has been accepted.

## ❓ Common Questions Quick Index
- **Q: What does this service do?** → It's the "brains" of carpool matching. It takes your request to find a carpool and searches through all other requests to find the best fits.
- **Q: How does it find matches?** → It uses a multi-step process. First, it finds people going in the same direction at roughly the same time. Then, it uses the HERE Maps API to check if the driver's route is a good fit and calculate the real travel time for the detour, ensuring it's efficient.
- **Q: Is this related to `carpoolHandler.js`?** → Yes, they are two halves of the same system. This service finds the match, and `carpoolHandler` handles the money and status updates after the match is accepted.
- **Q: What is `createAndMatchCarpool`?** → This is the main "entry point" function. It's a huge function that gets called when a user submits a new carpool request. It saves the request to the database and immediately kicks off the matching process.

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this service as an **elite, high-tech matchmaking agency for carpoolers**.
1.  **New Client Onboarding (`createAndMatchCarpool`):** A new client (a user wanting a carpool) comes in and fills out a detailed form with where they're going, when, and their preferences (e.g., gender). The agency files this request.
2.  **The Matching Process (`carpoolMatching`):** The agency immediately begins searching for a match by going through its files in several stages:
    *   **Stage 1: Basic Filtering:** They pull out all files for people traveling on the same day. They filter this pile for people with compatible preferences.
    *   **Stage 2: Location Check:** They look at a big map and only keep the files for people whose start and end points are reasonably close to the new client's.
    *   **Stage 3: Real-World Logistics (The expensive part):** For the remaining handful of potential matches, the agency calls a traffic consultant (the HERE Maps API). They ask, "What is the *actual* travel time for this driver to detour and pick up this rider?" and "How much longer will the driver's total trip be?"
    *   **Stage 4: Final Selection:** Based on the traffic consultant's report, the agency presents the client with a final, curated list of the very best matches.
3.  **Cancellation Department (`cancelCarpool`):** If a client cancels their request, this department handles all the paperwork, removing their file and notifying the "Accountant" (`carpoolHandler`) to process any necessary refunds.

**Technical explanation:** 
This service is the implementation of the carpool matching algorithm. The primary function, `carpoolMatching`, executes a filtering cascade. It begins with broad, cheap database queries (e.g., selecting users with active reservations) and progressively applies more specific and expensive filters. The most critical and costly filters are `filterByPickupTravelTime` and `filterByRoute`, which make external `axios` calls to the HERE Maps API to get real-world routing and duration data. This data is used to determine if a potential match is logistically feasible within the given time constraints. The service's main entry point is `createAndMatchCarpool`, a large orchestrator function that creates the initial `reservation` in the database and then invokes the matching pipeline. The `cancelCarpool` function manages the complex process of unwinding a reservation, which includes calling `carpoolHandler.cancelCarpoolEscrowReturn` to settle the financial aspect. The service also includes robust monitoring, logging metrics to InfluxDB and sending alerts to Slack.

**Business value explanation:**
The quality of the matching algorithm is arguably the single most important factor in the success of a carpooling product. This service *is* that algorithm. Its effectiveness directly determines user satisfaction. A good match means users save time and money, leading to high engagement and retention. A bad match (e.g., a driver is sent far out of their way) leads to frustration and churn. The sophisticated, multi-stage filtering pipeline is designed to maximize the quality of matches while managing the cost of expensive API calls. This service is the core intellectual property and primary value driver of the carpooling feature.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/carpool.js`
- **Language:** JavaScript (ES2017+)
- **Key Libraries:** `knex`, `axios`, `@maas/services` (InfluxManager, SlackManager)
- **Type:** Matching Engine / Core Business Logic
- **File Size:** ~70 KB
- **Complexity Score:** ⭐⭐⭐⭐⭐ (Very High. This service contains extremely long functions, a complex algorithmic pipeline, external API integrations, and tight coupling with other complex services. It is a system hub.)

## 📝 Detailed Code Analysis

### The Filtering Pipeline
The architecture of `carpoolMatching` is a classic filtering pipeline. It's designed to reduce the set of potential candidates at each step, saving the most expensive operations for last.
1.  **DB Query:** Broad and fast.
2.  **Profile/Time/Location Filters:** In-memory filtering or simple DB queries. Still fast.
3.  **HERE API Calls:** The bottleneck. These are network-bound, have latency, and likely cost money per call. By placing them at the end of the pipeline, the service ensures they are only ever called for the most promising potential matches, which is a critical performance optimization.

### Monitoring and Reliability
Unlike many other services, this one has explicit, robust monitoring built-in. Every call to the HERE Maps API is wrapped in a block that writes metrics to InfluxDB via `influx.writeIntoServiceMonitor`. It logs the API called, the status (SUCCESS/ERROR), the duration, and the request metadata. This is essential for debugging performance issues and monitoring the health and cost of the third-party integration.

### Large, Complex Functions
Functions like `createAndMatchCarpool` (over 200 lines) and `cancelCarpool` (over 100 lines) are extremely large and have very high cyclomatic complexity. They handle a vast number of variables and conditional paths. While they may be functionally correct, their size makes them very difficult to read, maintain, and test. Breaking them down into smaller, more focused helper functions would significantly improve the code's quality and long-term maintainability.

## 🚀 Usage Methods

```javascript
// This service is the entry point for a user starting a carpool search.

const carpoolService = require('@app/src/services/carpool');

async function requestCarpool(user, tripDetails) {
  try {
    // This single, massive function handles everything:
    // 1. Creates the reservation record in the database.
    // 2. Kicks off the entire matching pipeline.
    // 3. Returns a list of the best initial matches.
    const results = await carpoolService.createAndMatchCarpool({
      userId: user.id,
      role: tripDetails.role, // 'DRIVER' or 'PASSENGER'
      origin: tripDetails.origin,
      destination: tripDetails.destination,
      // ... and many other parameters
    });
    
    console.log(`Found ${results.matched.length} initial matches.`);
    return results.matched;
  } catch (error) {
    console.error(`Failed to create and match carpool for user ${user.id}`, error);
  }
}
```

## ⚠️ Important Notes
- **CRITICAL COMPLEXITY:** This service, along with `carpoolHandler.js`, defines the entire carpool feature. Modifications require a holistic understanding of the full system.
- **COST MANAGEMENT:** The service makes calls to the paid HERE Maps API. Any changes to the filtering logic could have significant cost implications.
- **CANDIDATE FOR REFACTORING:** The very large functions in this service are prime candidates for refactoring into smaller, more manageable units to improve code quality.

## 🔗 Related File Links
- **Financial Counterpart:** `@app/src/services/carpoolHandler.js`
- **External API:** HERE Maps Routing API
- **Monitoring:** InfluxDB, Slack

---
*This documentation was generated to explain the service's role as the core carpool matching engine, detailing its filtering pipeline architecture and its relationship with other critical services.* 