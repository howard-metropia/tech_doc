# Guest (Anonymous) User Account Service Documentation

## 🔍 Quick Summary (TL;DR)
This service is the cornerstone of the application's **anonymous user experience**. It manages the entire lifecycle of "guest" accounts, allowing users to interact with the app without providing any personal information like an email or phone number. It handles both the creation of new guest accounts and the login process for returning guests, using a unique, securely generated `guest_token` as the sole identifier. A notable feature is its massive `INSERT` statement, designed to create a fully-formed user record with default values to maintain compatibility with a legacy database schema.

**Keywords:** guest-account | anonymous-user | session | authentication | token | JWT | registration

**Primary use cases:** 
- To create a new, persistent anonymous user account for first-time users.
- To log in a returning anonymous user using their `guest_token`.
- To issue a standard JWT `access_token` for a guest user, allowing them to access protected APIs just like a registered user.

## ❓ Common Questions Quick Index
- **Q: What does this service do?** → It creates and manages user accounts for people who haven't signed up with an email, allowing them to use the app anonymously.
- **Q: How does it identify a guest user?** → It uses a `guest_token`, a long, random string that is stored on the user's device and sent with each request.
- **Q: Why is the `insert` statement so huge?** → To ensure compatibility. It creates a complete user record in the database, filling all the columns that a normal, registered user would have with empty or default values. This prevents database errors and simplifies logic in other parts of the app that expect a full user object.
- **Q: Is a guest account a "real" account?** → Yes. It's a full record in the `AuthUsers` table, marked with `is_guest: 1`. It has a unique user ID and can be issued a valid `access_token`.

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this service as a **concierge at a hotel who provides temporary key cards**.
1.  **A New Guest Arrives (No `guest_token`):** A visitor walks into the hotel for the first time. The concierge doesn't ask for their name or ID. Instead, they:
    *   Generate a new, unique key card number (`guest_token = genToken(128)`).
    *   Create a new guest file in their system (`INSERT` into `AuthUsers`). They fill in "Guest" for the name and leave fields like "Phone Number" and "Mailing Address" blank.
    *   They hand the visitor the key card.
2.  **A Returning Guest Arrives (With `guest_token`):** A visitor returns with a key card from a previous stay. The concierge:
    *   Looks up the key card number in their system to retrieve the guest's file (`SELECT` from `AuthUsers`).
3.  **Issuing Access:** For both new and returning guests, the concierge then programs a standard room key (`access_token`) that will work on all the doors the guest is allowed to open, and hands it to them. The guest can now use the hotel's amenities.

**Technical explanation:** 
The service exposes a single async function, `guest_login`.
-   **Registration Flow:** If the `guest_token` in the input is falsy, the service enters registration mode. It generates a new 128-character random token and enters a `while` loop to guarantee its uniqueness in the `AuthUsers` table. Upon finding a unique token, it performs a massive `User.query().insert({...})` operation. This statement populates every conceivable field of the user model with default empty strings, `0`, or `'T'` to satisfy database constraints and legacy code expectations.
-   **Login Flow:** If a `guest_token` is provided, the service attempts to find a matching user record where `is_guest` is `1`.
-   **Token Issuance:** For both flows, if a valid `user` object is obtained, the service calls `generateJwt(user.id)` to create a standard, stateful JWT. It then updates the user's record with this new `access_token` and the `security_key` from the request. Finally, it calls `syncTokenStatus`, likely to write the token's status to a cache like Redis, before returning the necessary tokens and IDs to the client. If at any point a user is not found when one is expected, a `MaasError` is thrown.

**Business value explanation:**
This service is crucial for reducing user friction and increasing initial adoption. By allowing users to immediately access the app's features without the upfront barrier of a mandatory registration form, it significantly improves the onboarding experience. Users can explore the app's value proposition first and only decide to register later. The persistent nature of the `guest_token` also means their initial activity and preferences can be seamlessly migrated to a full account if they choose to convert, providing a smooth upgrade path.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/guest.js`
- **Language:** JavaScript (Node.js)
- **Key Libraries:** `@maas/core/log`, `objection.js` (implied by `.query()`)
- **Type:** Authentication / User Management Service
- **File Size:** ~7 KB
- **Complexity Score:** ⭐⭐ (Low-Medium. The core logic is straightforward, but the enormous `INSERT` statement is a significant code smell and a sign of high coupling with the database schema.)

## 🚀 Usage Methods

```javascript
const guestService = require('@app/src/services/guest');

// Example: On app launch, check for a stored guest token and log the user in.
async function initializeUserSession(storedGuestToken, deviceSecurityKey) {
    try {
        // If storedGuestToken is null, the service will create a new guest.
        // If it's a valid token, the service will log in the existing guest.
        const authData = await guestService.guest_login({
            security_key: deviceSecurityKey,
            guest_token: storedGuestToken,
        });

        // The client now has a standard access_token to use for API calls.
        const { access_token, user_id, guest_token } = authData;

        // The client should securely store the new guest_token for future sessions.
        saveTokenToLocalStorage('guest_token', guest_token);
        
        // Use the access_token for all subsequent API requests.
        apiClient.setAuthHeader(access_token);

        return { success: true, userId: user_id };

    } catch (error) {
        // Handle cases like user not found, etc.
        logger.error(`Guest login failed: ${error.message}`);
        return { success: false, error: 'Session could not be initialized.' };
    }
}
```

## 🔗 Related File Links
- **Database Model:** `@app/src/models/AuthUsers.js`
- **Dependent Service:** `@app/src/services/account.js` (for `generateJwt`, `syncTokenStatus`)
- **Error Codes:** `@app/src/static/error-code.js`

---
*This documentation was generated to explain the service's critical role in managing the lifecycle of anonymous guest accounts.*