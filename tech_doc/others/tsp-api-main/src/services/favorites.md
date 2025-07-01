# User Favorites Management Service Documentation

## 🔍 Quick Summary (TL;DR)
This service provides the core Create, Update, and Delete (CUD) logic for managing a user's favorite locations. It allows users to save, modify, and remove locations, while enforcing key business rules, such as limiting users to one "Home" and one "Work" location, and a maximum of eight other custom favorites. The service also handles instrumentation by logging user actions to an analytics service.

**Keywords:** favorites | saved-places | crud | home | work | user-profile

**Primary use cases:** 
- Creating a new favorite location (e.g., setting a Home address).
- Updating the details of an existing favorite location.
- Deleting a favorite location.
- Enforcing the business logic that limits the number of favorites per category.

## ❓ Common Questions Quick Index
- **Q: What does this service do?** → It manages a user's saved places, like "Home," "Work," and other custom favorites.
- **Q: Can I save more than one "Home" address?** → No. The service's logic prevents this. You can only have one favorite of category 1 (Home) and one of category 2 (Work). You are also limited to 8 custom favorites (category 3).
- **Q: Does this service fetch the list of favorites?** → No. This service only handles creating, updating, and deleting. The corresponding API controller is responsible for fetching the list of existing favorites for a user, likely by querying the `Favorites` database model directly.
- **Q: What are `insertAppData` and `sendEvent`?** → These are helper functions used for analytics. They log a user's actions (e.g., "SaveHome", "RemoveOffice") so that user behavior can be tracked and analyzed.

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this service as the **manager of the "Favorites" page in your phone's contact list or map app**.
- **`create` (Adding a New Favorite):** You tap "Add Favorite." The manager first checks its rulebook. If you're trying to add a second "Home" address, the manager says, "Sorry, you can only have one Home." If the rules pass, the manager saves the new location to your list and makes a note in its daily logbook that you added a favorite.
- **`update` (Editing a Favorite):** You want to change the address for your "Work" favorite. The manager finds the entry, updates the details, and makes a note in its logbook that you edited your Work location.
- **`delete` (Removing a Favorite):** You decide you no longer need a favorite. You tap "delete." The manager removes it from your list and notes in its logbook that you removed a favorite.

**Technical explanation:** 
This service exports three functions—`create`, `update`, and `delete`—that operate on the `Favorites` Mongoose model.
-   **`create`**: Before inserting a new record, it performs a query to check if creating this favorite would violate category limits (max 1 for category < 3, max 8 for category 3). If the check passes, it inserts the new favorite into the database. It then calls the `insertAppData` and `sendEvent` helpers to log analytics events.
-   **`update`**: It first validates that the favorite exists. It then performs the same category limit validation as `create` to prevent a user from, for example, changing a custom favorite into a second "Home" favorite. It prepares the update payload by removing internal fields from the input and then updates the record in the database.
-   **`delete`**: It verifies the favorite exists, logs the appropriate removal action to `insertAppData` based on the favorite's category, and then deletes the record by its ID.

**Business value explanation:**
The ability for users to save and easily access frequently used locations is a fundamental and expected feature of any location-based application. It reduces friction and saves users time, directly improving the user experience and increasing engagement. This service provides the robust backend logic to power this feature, and the analytics instrumentation it includes is valuable for understanding user behavior, such as how many users have set up their Home and Work locations, which is a key metric for user retention.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/favorites.js`
- **Language:** JavaScript (ES2017+)
- **Key Libraries:** `moment-timezone`, Mongoose
- **Type:** CRUD Service
- **File Size:** ~5 KB
- **Complexity Score:** ⭐⭐ (Low. The logic is straightforward CRUD with clear business rule validation.)

## 📝 Detailed Code Analysis

### Business Logic in the Service Layer
This service is a good example of placing business logic correctly in the service layer. Instead of allowing a controller to simply insert data into the database, this service intercepts the request and applies rules first (e.g., "a user cannot have two Home locations"). This ensures the logic is centralized and consistently applied, regardless of where the `create` or `update` function is called from.

### Clear Instrumentation
The service makes clear and purposeful calls to `insertAppData` and `sendEvent`. The event names are descriptive (`SaveHome`, `EditOffice`, `set_favorite`), which makes the resulting analytics data easy to understand and use. This is a good practice for tracking user engagement with core features.

### Clean Update Payload
In the `update` function, the code explicitly `delete`s properties from the input object that should not be written to the database.
```javascript
const update = { ...inputData };
delete update.userId;
delete update.zone;
// ...
await Favorites.query().where('id', id).update(update);
```
This is a safe way to handle updates, preventing potentially malicious or extraneous data from the client from being persisted. It acts as a whitelist of updatable fields, even though it's implemented as a blacklist in this case.

## 🚀 Usage Methods

```javascript
// This service provides the core implementation for the /favorites API endpoints.

const favoritesService = require('@app/src/services/favorites');

// Example: Controller logic for creating a new favorite
async function httpCreateFavorite(req, res) {
    const inputData = {
        userId: req.user.id,
        zone: req.body.zone,
        name: req.body.name,
        // ... other properties from the request body
    };

    try {
        const newFavorite = await favoritesService.create(inputData);
        res.status(201).json(newFavorite);
    } catch (error) {
        // handle error, e.g., ERROR_EXCEED_FAVORITES
        res.status(error.statusCode || 500).json({ message: error.message });
    }
}

// Example: Controller logic for deleting a favorite
async function httpDeleteFavorite(req, res) {
    const inputData = {
        id: req.params.id,
        userId: req.user.id,
        zone: req.body.zone,
    };

    try {
        await favoritesService.delete(inputData);
        res.status(200).json({});
    } catch (error) {
        // handle error, e.g., ERROR_FAVORITES_NOT_FOUND
        res.status(error.statusCode || 500).json({ message: error.message });
    }
}
```

## 🔗 Related File Links
- **Database Model:** `@app/src/models/Favorites.js`
- **Helpers:** `@app/src/helpers/insert-app-data.js`, `@app/src/helpers/send-event.js`

---
*This documentation was generated to explain the service's role in managing the CRUD operations and business logic for user favorite locations.*