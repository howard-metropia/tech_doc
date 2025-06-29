# Account Service Documentation

## 🔍 Quick Summary (TL;DR)
This service is primarily responsible for generating and managing JSON Web Tokens (JWTs) for user authentication and session management. It contains the core logic for creating new JWTs with specific payloads and expiration times.

**NOTE:** A significant portion of this file (over 90%) is commented out, including logic for user registration, phone verification, password resets, social logins (Google, Facebook, Apple), and profile updates. This strongly indicates that these features have been deprecated, moved to another service, or are undergoing a major refactor. The only active, non-commented-out functionality relates to JWT creation.

**Keywords:** account | authentication | auth | jwt | json-web-token | session-management | user-token | security

**Primary use cases (Active Logic):** 
- Generating a new, signed JWT for a user upon successful login or session refresh.
- Synchronizing the user's latest token in the database.

**Primary use cases (Commented-out Logic):**
- User registration with email verification.
- User login with password or social providers.
- Phone number verification and account merging.
- "Forgot Password" flows.
- User profile management (get/update).

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this service as the **bouncer at a private club who issues and validates entry stamps (JWTs)**.
- **Issuing a Stamp (`generateJwt`):** When a member proves who they are, the bouncer gives them a special, tamper-proof hand stamp. This stamp (the JWT) contains their member ID, what areas they can access, and when the stamp expires.
- **The Secret Ink (`createJwt`):** The bouncer uses a secret, invisible ink (the `JWT_KEY`) to make the stamp. Only they know the secret, so no one can forge it.
- **Updating the Roster (`syncTokenStatus`):** After issuing a new stamp, the bouncer updates their master list to note the member's latest stamp number, ensuring their records are always current.
- **(Formerly...)** This bouncer used to also handle new member sign-ups, check IDs, and even help members who forgot their secret handshake, but it seems those duties have been passed to someone else.

**Technical explanation:** 
This service exclusively handles JWT generation and management. The primary function, `generateJwt`, creates a standard JWT payload including `userId`, issued-at (`iat`), and expiration (`exp`) claims, signs it using a secret key from the configuration (`config.auth.jwtKey`), and then calls `syncTokenStatus` to update the `auth_user_tokens` table with the newly generated token for the user. A large amount of commented-out code suggests this file was once a monolithic service for all user account operations but has since been stripped down to only handle token generation.

**Business value explanation:**
Secure and reliable token generation is the cornerstone of the entire application's security model. This service ensures that every authenticated user is issued a standard, secure, and time-limited JSON Web Token. This prevents unauthorized access to user data and API endpoints. By centralizing token creation logic here, the application ensures consistency and makes it easy to update security policies (like token expiration times) in one place.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/account.js`
- **Language:** JavaScript (ES2020)
- **Key Libraries:** `jsonwebtoken`
- **Type:** Authentication Service (JWT)
- **Complexity Score (Active Code):** ⭐⭐ (Low-Medium - Standard JWT implementation.)
- **Complexity Score (Including Commented Code):** ⭐⭐⭐⭐⭐ (Very High - Was previously a monolithic and highly complex service.)

**Dependencies (Active Code):**
- `jsonwebtoken`: The core library for creating and signing JWTs (**Critical**).
- `moment-timezone`: For handling timestamps and token expiration (**High**).
- `config`: Used to fetch the secret JWT signing key (**Critical**).
- `@app/src/models/AuthUserTokens`: The Mongoose/Objection model for the database table that stores user tokens (**Critical**).

## 📝 Detailed Code Analysis (Active Functions)

### `generateJwt(userId, payload)`
- **Purpose**: To create and sign a new JWT for a given user.
- **Logic**:
    1. It defines a default JWT payload containing the `userId`.
    2. If an additional `payload` object is provided, it merges it into the default payload.
    3. It calls the internal `createJwt` function to do the actual signing, passing the payload and a configured expiration time (`config.auth.expiresIn`).
    4. It then calls `syncTokenStatus` to record this new token in the database for the user.
    5. It returns the signed token string.

### `createJwt(jwtKey, payload, expiresIn)`
- **Purpose**: A generic wrapper around the `jsonwebtoken.sign` method.
- **Logic**:
    1. It takes a secret key, a payload, and an optional expiration time.
    2. If `expiresIn` is provided, it passes it in the `options` object to `jwt.sign`.
    3. It calls `jwt.sign` to create the token string.
    4. It returns the signed token string.

### `syncTokenStatus(userId, newToken)`
- **Purpose**: To update the user's record in the database with their latest access token.
- **Logic**:
    1. It uses the `UserToken` model to find a token record associated with the `userId`.
    2. **If a record exists**, it updates it with the `newToken` and the current timestamp.
    3. **If a record does not exist**, it creates a new one for the user with the `newToken`.
    4. This ensures that the `auth_user_tokens` table always holds the most recent token for each user, which can be useful for session management or forcing logouts.

## 🚀 Usage Methods

```javascript
// Example of how another service (e.g., a login service) would use this
const accountService = require('@app/src/services/account');

async function handleSuccessfulLogin(userId) {
  // ... after verifying user credentials ...

  // Generate a new JWT for the user
  const userToken = await accountService.generateJwt(userId);

  // Return the token to the client
  return { token: userToken };
}
```

## ⚠️ Important Notes
- **Monolith Decomposition**: This file is a prime example of monolith decomposition. The vast amount of commented-out code for registration, login, profile management, etc., strongly implies these functions were moved into more focused, separate services (e.g., `profile.js`, `user.js`, or new services for each social provider). The remaining code is a small, focused microservice for JWTs.
- **Security**: The security of the entire system relies on the `JWT_KEY` being kept secret and complex. This key is correctly loaded from the application's configuration, not hard-coded.

---
*This documentation was generated focusing on the currently active JWT-related functions and noting the extensive amount of deprecated, commented-out code.* 