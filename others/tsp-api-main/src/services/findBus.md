# Promotional Bus Ticket Finder Service Documentation

## 🔍 Quick Summary (TL;DR)
This is a specialized utility service with a very specific purpose: to find the corresponding **zero-dollar ($0.00) promotional ticket UUID** for a given bus route ID. It operates on the assumption that for every standard, full-price bus ticket defined in the Bytemark system, there is a corresponding promotional ticket with the same name plus a " - 0" suffix. This service is a key component for enabling features like "free ride" promotions or subsidies, as the system still requires a valid ticket product UUID to process a transaction, even if its value is zero.

**Keywords:** promotional-ticket | zero-dollar-fare | bytemark | bus-ticket | free-ride | subsidy

**Primary use cases:** 
- To look up the correct, transactable, $0 Bytemark ticket product for a standard bus route.
- To find the promotional ticket for both regular bus routes and special Park & Ride (P&R) routes.

## ❓ Common Questions Quick Index
- **Q: What does this service do?** → Given a bus number (e.g., "70"), it finds the UUID of the "free" version of that bus ticket.
- **Q: Why would you need a "free" ticket?** → For promotions, subsidies, or rewards. Even if the user pays nothing, the ticketing system (Bytemark) needs a valid ticket product with a unique ID to record the transaction. This service finds that ID.
- **Q: How does it link a paid ticket to a free one?** → It uses a specific naming convention. It finds the full-price ticket (e.g., with the name "Local Bus Ride") and then searches for another ticket named "Local Bus Ride - 0".
- **Q: What is the `##` format for?** → The service is designed to be called with contextual data (`level1`, `level2`). It preserves this context in its output, returning a `##` delimited string with the original context plus the new ticket information it found.

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this service as a **specialized coupon finder at a grocery store**.
1.  **You Have a Product:** You bring a standard item, like a can of soup, to the coupon finder. This is the regular, full-price bus ticket.
2.  **The Coupon Finder Checks Its Book:** The coupon finder looks up the soup in its master list of products. It finds the soup's price, say $1.25.
3.  **It Finds the "Free" Version:** The coupon finder knows a secret rule: for every product, there's a special "promotional" version with a unique barcode. To find it, it looks for the product's name with " - PROMO" at the end. It finds the "Can of Soup - PROMO" item in its system.
4.  **It Gives You the Special Barcode:** The coupon finder doesn't give you the soup itself; it gives you the unique barcode (the UUID) for the promotional version. You can now take this barcode to the checkout, and it will ring up as $0.00. This service does the exact same thing, but for bus tickets.

**Technical explanation:** 
The service, exported as a singleton `findBus` instance, has two main methods: `find` and `search`.
-   **`find`**: This method takes an array of `##` delimited strings. For each string, it splits it into context (`level1`, `level2`) and a `busID`, and then calls the `search` method in parallel for all items using `Promise.all`.
-   **`search`**: This is the core logic. It first queries the `mogonBusTickets` collection to find the fare for the given `busID`. It then uses this fare (converted to cents) to find the corresponding full-price product in the `mogonBytemarkTickets` collection. Using the `name` from this full-price product, it constructs a new name by appending `" - 0"` and queries `mogonBytemarkTickets` again to find the zero-dollar promotional ticket. If the initial search fails, it attempts a fallback search for Park & Ride (P&R) routes using a regex on the `long_description` field.
-   The final output is a `##` delimited string containing the original context, the UUID of the $0 ticket, the original fare, and the promotional ticket's name.

**Business value explanation:**
This service is the technical enabler for a wide range of marketing promotions, corporate subsidies, and user reward programs. By providing a reliable way to transact "free" rides through the official Bytemark ticketing system, it allows the business to offer compelling incentives to drive user acquisition, engagement, and retention, without needing to bypass or re-architect the core ticketing integration.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/findBus.js`
- **Language:** JavaScript (ES6 Class)
- **Key Libraries:** Mongoose
- **Type:** Utility / Data Lookup Service
- **File Size:** ~4 KB
- **Complexity Score:** ⭐⭐ (Low-Medium. The logic is nested and follows a specific, non-obvious convention, but it is contained and single-purpose.)

## 📝 Detailed Code Analysis

### Reliance on Naming Convention
The entire logic hinges on the assumption that for a ticket named `TICKET_NAME`, a corresponding promotional ticket named `TICKET_NAME - 0` will always exist. This is a fragile design choice. If a content manager or an automated process were to create a promotional ticket with a slightly different name (e.g., `TICKET_NAME - Free` or `TICKET_NAME-0`), this service would fail to find it. A more robust design would be to have an explicit link in the database, such as a `promotional_ticket_id` field on the full-price ticket's document.

### String Manipulation and Type Conversion
The service performs several small but important data manipulations:
-   `tmpAry[2].substr(0, 1) === '0' ? tmpAry[2].replace('0', '') : tmpAry[2]`: This removes a leading zero from a bus ID (e.g., "070" -> "70").
-   `ticketResult.full_fare * 100`: This converts a dollar value (e.g., 1.25) to cents (125) to match the `sale_price` format in the Bytemark tickets collection, which is a common practice for storing currency.

### The Buddha Comment
This file also contains the "Buddha bless, never crash, never have bugs" ASCII art comment, which appears to be a signature of the original developer.

## 🚀 Usage Methods

```javascript
const findBusService = require('@app/src/services/findBus');

// Example: Processing a trip plan to find promotional tickets for the bus legs
async function findPromoTicketsForTrip(tripPlan) {
    const busLegsToProcess = [];
    
    // Assume tripPlan has routes and sections
    tripPlan.routes.forEach((route, routeIndex) => {
        route.sections.forEach((section, sectionIndex) => {
            if (section.type === 'transit') {
                const context = `${routeIndex}##${sectionIndex}`;
                const busId = section.transport.shortName; // e.g., "70"
                busLegsToProcess.push(`${context}##${busId}`);
            }
        });
    });

    // Call the service to get the results
    const results = await findBusService.find(busLegsToProcess);
    // results = [ '0##1##uuid-for-free-ticket##1.25##Local Bus Ride' ]

    // Now, process the results to enrich the original trip plan
    results.forEach(resultString => {
        const [routeIndex, sectionIndex, uuid, price, name] = resultString.split('##');
        // Add the promotional ticket info to the trip plan object
        tripPlan.routes[routeIndex].sections[sectionIndex].transport.promo_uuid = uuid;
    });

    return tripPlan;
}
```

## 🔗 Related File Links
- **Database Models:** `@app/src/models/busTickets.js`

---
*This documentation was generated to explain the service's specific and unconventional logic for finding promotional, zero-dollar bus tickets.* 