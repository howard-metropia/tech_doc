# Enterprise User Verification & Management Service Documentation

## 🔍 Quick Summary (TL;DR)
This is a comprehensive service that manages all business logic related to enterprise (corporate) user accounts. Its core responsibility is to handle the entire lifecycle of employee verification: a user submits their corporate email, the service sends a secure verification link to that email, and upon successful verification, the user is automatically integrated into the enterprise's ecosystem. This includes being added to the company's private Duo Group and having any telework features activated. The service is a critical gateway for all B2B functionality.

**Keywords:** enterprise | corporate | b2b | verification | onboarding | duo-group | telework

**Primary use cases:** 
- To allow users to prove their employment with a partner enterprise using their corporate email address.
- To manage the secure, token-based email verification workflow.
- To automatically add verified employees to their company's private carpool (Duo) group.
- To manage and activate telework-specific features for enterprise users.
- To handle the administrative side, including user rejections and blocking.

## ❓ Common Questions Quick Index
- **Q: What is this service for?** → It handles everything for corporate users. Its main job is to verify that a user actually works for a partner company (like "Acme Corp") by making them click a link sent to their `user@acme.com` email address.
- **Q: How does the verification work?** → When a user provides their work email, the service generates a secure, one-time-use token (a JWT) and embeds it in a special link. This link is emailed to their work address. When they click it, the service validates the token and marks them as a verified employee.
- **Q: What happens after a user is verified?** → They get automatically added to their company's private carpool group and any special "telework" features they are eligible for are turned on.
- **Q: Is this service secure?** → It is designed with security in mind. It uses JSON Web Tokens (JWTs) with a 30-day expiration for the verification links, which is a standard and secure method for this type of process.

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this service as the **Corporate Human Resources (HR) department for the app**.
1.  **New Employee Onboarding (`createVerificationEmail`):** A user claims they work for Acme Corp and provides their `@acme.com` email. The HR department (this service) says, "Great! To prove it, we're sending a confidential onboarding link to that email address. Please click it."
2.  **ID Badge Activation (`verifyEmail`):** The user receives the email and clicks the special link. This action confirms their identity. The HR department activates their official "Acme Corp Employee" status in the system.
3.  **Granting Access (`joinDuoGroup`, `activateTelework`):** Immediately after their ID badge is activated, the HR department automatically gives them a keycard to the exclusive Acme Corp carpool lounge (adds them to the private Duo Group). They also check a box to give them access to the company's telework program benefits.
4.  **Handling Problems (`createRejectEmail`):** If a manager later reports that this person doesn't actually work for Acme Corp, the HR department deactivates their status and sends them a formal email explaining why their access has been revoked.

**Technical explanation:** 
This service orchestrates the enterprise user verification workflow. The process starts when `createVerificationEmail` is called. This function generates a signed JSON Web Token (JWT) containing the `userId`, corporate `email`, and `enterpriseId`. This token is stored in the `Enterprises` model and embedded within a dynamic link in an EJS-templated HTML email, which is then sent to the user.
When the user clicks the link, the API endpoint calls the `verifyEmail` function. This function validates the JWT. On successful validation, it updates the user's status in the `Enterprises` table and then calls helper functions to complete the integration:
- `joinDuoGroup`: Finds the `DuoGroup` linked to the `enterpriseId` and adds the user to it.
- `activateTelework`: Updates the `acc_member_portal` table to link the user to their active telework organization.
The service uses `knex` to interact with multiple MySQL schemas (`carpooling`, `portal`) and Mongoose models for the main application's database.

**Business value explanation:**
This service is the engine for the platform's B2B strategy. By providing a seamless and secure way for partner companies to onboard their employees, it creates a powerful incentive for corporate adoption. Companies can use this to manage transportation demand, promote sustainable commuting, and provide valuable perks to their employees. The automated nature of the verification and group-joining process reduces administrative overhead and makes it easy for enterprises to roll out the program to their entire workforce, driving user growth and engagement in targeted, high-value cohorts.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/enterprise.js`
- **Language:** JavaScript (ES2017+)
- **Key Libraries:** `jsonwebtoken`, `ejs`, Mongoose, `knex`
- **Type:** Business Logic / User Onboarding Service
- **File Size:** ~30 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High. The service manages a secure, multi-step, stateful process that involves cryptography (JWT), email templating, and deep integration with multiple database schemas and application services.)

## 📝 Detailed Code Analysis

### Secure Token-Based Workflow
The core of the service is the use of JWT for email verification. This is a strong design pattern. It's stateless from the server's perspective (the token itself contains the necessary context) and is cryptographically signed to prevent tampering. Setting an expiration time (`expiresIn: '30 day'`) is a crucial security measure to limit the lifespan of a verification link.

### Multi-Schema Database Interaction
The service demonstrates a high level of integration by using `knex` to connect to both a `carpooling` database schema and a `portal` database schema, in addition to using Mongoose models for the main application database. This indicates it acts as a bridge, reading enterprise definitions from one database (`org_setting`, `acc_member`) and writing state to another (`Enterprises`, `DuoGroupMembers`). This is powerful but also increases complexity and the number of dependencies.

### Helper and Abstraction Usage
The service makes excellent use of helpers to abstract away implementation details, leading to cleaner code in the main logic functions. For example:
- `send_mail` encapsulates the details of sending an email.
- `get-dynamic-link` handles the creation of the specific link format needed.
- `randomText` is used for generating unique job numbers.
This separation of concerns makes the primary business logic in functions like `createVerificationEmail` easier to follow.

## 🚀 Usage Methods

```javascript
// This service provides the core implementation for the /enterprise API endpoints.

const enterpriseService = require('@app/src/services/enterprise');

// Example: A user submits their corporate email to start the verification process
async function startVerification(userId, userWorkEmail) {
  try {
    // This call will validate the email domain, create the JWT,
    // render the email template, and send the verification email.
    const result = await enterpriseService.createVerificationEmail(
      userId,
      null, // duoGroupName is optional here
      userWorkEmail,
      // ... other params
    );
    console.log('Verification email sent successfully.');
    return result;
  } catch (error) {
    console.error('Failed to start enterprise verification:', error);
  }
}

// Example: The API endpoint that the user hits when clicking the verification link
async function finalizeVerification(token) {
    try {
        // This function validates the JWT token and, if successful,
        // automatically joins the user to the company Duo Group and activates telework.
        const result = await enterpriseService.verifyEmail(token);
        console.log('User successfully verified!');
        return result; // Usually a redirect URL
    } catch (error) {
        console.error('Email verification failed:', error);
    }
}
```

## 🔗 Related File Links
- **JWT Library:** `jsonwebtoken`
- **Email Templating:** `ejs`
- **Helpers:** `send_mail`, `get-dynamic-link`
- **Database Models:** `Enterprises`, `DuoGroups`, `AuthUsers`

---
*This documentation was generated to explain the service's critical role in managing the secure onboarding and integration of corporate users.* 