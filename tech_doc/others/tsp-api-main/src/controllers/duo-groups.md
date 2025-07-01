# DUO Groups Controller Documentation

## 🔍 Quick Summary (TL;DR)
This controller manages the entire lifecycle of "DUO Groups," which are essentially private or semi-private carpooling groups. It provides a comprehensive set of endpoints for creating, managing, joining, leaving, and administering these groups and their members.

**Keywords:** duo-group | carpool | rideshare | group-management | social-ride | tsp-api | user-groups | private-carpool | community-transit

**Primary use cases:** 
- Creating a new carpool group.
- Searching for and joining existing groups.
- Managing group members (adding, removing, accepting requests).
- Administering group settings and profiles.
- Leaving or canceling membership in a group.

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x.

## ❓ Common Questions Quick Index
- **Q: How do I create a new carpool group?** → [POST /](#post-)
- **Q: How do I find a group to join?** → [GET /search](#get-search)
- **Q: What's the process for joining a group?** → [POST /join](#post-join), followed by an admin's action [POST /accept_user](#post-accept_user).
- **Q: How do I see who is in a group?** → [GET /member](#get-member)
- **Q: What is an "Admin Profile"?** → It's a profile for a group administrator, likely with extended details.
- **Q: Can a regular user remove another user?** → No, actions like removing users are typically restricted to group admins.
- **Q: What's the difference between `/cancel` and `/leave`?** → `/cancel` is likely for the group creator to disband the group, while `/leave` is for a member to exit.
- **Q: How are permissions managed?** → Through a combination of authentication and business logic within the service layer that checks if a user is an admin of a specific group.

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this controller as the **clubhouse manager for a university's carpool-to-campus program**. It handles everything:
- **Starting a New Club (`POST /`):** A student can register a new carpool club.
- **Club Directory (`GET /`, `GET /search`):** You can see a list of all clubs or search for one from your department.
- **Joining a Club (`POST /join`):** You can apply to join a club.
- **Membership Management (Admin):** The club president (`admin`) can approve new members (`POST /accept_user`), invite people (`POST /add_user`), or remove members (`POST /remove_user`).
- **Leaving a Club (`POST /leave`):** You can resign your membership at any time.
- **Viewing the Roster (`GET /member`):** You can see a list of current members in your club.
- **Updating Club Info (`PUT /:id`):** The president can update the club's meeting points or description.

**Technical explanation:** 
A comprehensive Koa.js REST controller that exposes a large number of endpoints under the `/api/v1/duo_group` prefix to manage all aspects of DUO carpool groups. It follows a standard pattern: each endpoint is protected by JWT `auth` middleware, parses the request payload with `bodyParser`, validates the combined headers/body/query against a specific Joi schema, and then delegates the full business logic to a corresponding function in the `duo-groups` service. The controller is purely a routing and validation layer, with all complex logic and database interaction handled by the service.

**Business value explanation:**
This controller provides the backbone for a community-based, trusted carpooling feature. By allowing users to form their own private or semi-private groups (e.g., for coworkers, neighbors, or fellow students), it builds a layer of trust and safety that is often missing from open ridesharing platforms. This encourages carpooling, reduces traffic and environmental impact, and creates a powerful social feature that increases user retention and platform value.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/duo-groups.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** REST API Controller
- **File Size:** ~7 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High - Due to the large number of distinct, interrelated endpoints managing a complex entity.)

**Dependencies (Criticality Level):**
- `@koa/router`, `koa-bodyparser`: Core routing and body parsing (**Critical**).
- `@app/src/middlewares/auth`: JWT authentication (**Critical**).
- `@app/src/services/duo-groups`: The service layer containing all business logic (**Critical**).
- `@app/src/schemas/duo-groups`: Joi schemas for input validation (**Critical**).
- `@app/src/helpers/fields-of-header`: Utility to extract user context (**High**).

## 📝 Detailed Code Analysis

This controller is a prime example of a resource-oriented API with many distinct actions. It can be broken down into logical groups:

#### Group Lifecycle Management
- `POST /`: Creates a new group.
- `GET /`: Lists groups the user is part of.
- `PUT /:id`: Updates a specific group's details.
- `DELETE /:id`: Deletes a group.
- `POST /cancel`: Cancels/disbands a group.

#### User Membership Actions
- `POST /join`: A user requests to join a group.
- `POST /leave`: A member leaves a group.
- `GET /search`: Searches for public groups.

#### Group Administration Actions
- `POST /set_admin`: Assigns a user as an admin for a group.
- `POST /add_user`: An admin invites/adds a user directly to the group.
- `POST /accept_user`: An admin accepts a user's join request.
- `POST /reject_user`: An admin rejects a user's join request.
- `POST /remove_user`: An admin removes a member from the group.

#### Information Retrieval
- `GET /member`: Gets the list of members for a specific group.
- `GET /member_profile`: Gets the detailed profile of a specific member within a group.
- `POST/GET /admin_profile`: CRUD operations for the special profile of a group's administrator.

The implementation pattern for every single endpoint is identical and robust:
1.  Define the route with Koa Router.
2.  Apply `auth` and `bodyParser` middleware.
3.  Combine all sources of input (`headers`, `body`, `query`, `params`).
4.  Validate the combined input object against a highly specific Joi schema (e.g., `inputValidator.create`, `inputValidator.joinDuoGroup`).
5.  Pass the single, validated `input` object to the corresponding service function (e.g., `service.create(input)`).
6.  Wrap the return value from the service in a standard `success` response.

This clean, repetitive pattern makes the controller easy to understand and maintain, despite its large size. All complexity is correctly abstracted away into the `duo-groups` service.

## 🚀 Usage Methods
*(Examples for key endpoints)*

**Base URL:** `https://api.tsp.example.com/api/v1/duo_group`
**Headers:** All requests require `Authorization: Bearer <TOKEN>` and `userid: usr_...`

### Create a Group
```bash
curl -X POST "https://api.tsp.example.com/api/v1/duo_group" \
  -H "Authorization: Bearer <TOKEN>" -H "userid: usr_123" \
  -H "Content-Type: application/json" \
  -d '{ "group_name": "Morning Commute Crew", "description": "Carpooling from The Heights to Downtown" }'
```

### Search for a Group
```bash
curl -X GET "https://api.tsp.example.com/api/v1/duo_group/search?keyword=Commute" \
  -H "Authorization: Bearer <TOKEN>" -H "userid: usr_456"
```

### Join a Group
```bash
curl -X POST "https://api.tsp.example.com/api/v1/duo_group/join" \
  -H "Authorization: Bearer <TOKEN>" -H "userid: usr_456" \
  -H "Content-Type: application/json" \
  -d '{ "group_id": 12345 }'
```

### Accept a Join Request (Admin action)
```bash
curl -X POST "https://api.tsp.example.com/api/v1/duo_group/accept_user" \
  -H "Authorization: Bearer <TOKEN>" -H "userid: usr_123" \
  -H "Content-Type: application/json" \
  -d '{ "group_id": 12345, "target_user_id": "usr_456" }'
```

### Get Group Members
```bash
curl -X GET "https://api.tsp.example.com/api/v1/duo_group/member?group_id=12345" \
  -H "Authorization: Bearer <TOKEN>" -H "userid: usr_456"
```

## ⚠️ Important Notes
- **Service Layer is Key**: This controller is a thin routing/validation layer. All the complex rules (e.g., "only an admin can remove a user," "a user cannot join a full group") are handled in the `duo-groups` service.
- **Permissions**: The API relies on the service layer to enforce role-based permissions (e.g., admin vs. member) for actions. The controller itself does not contain any permission logic.
- **Schemas as Contract**: The Joi schemas in `schemas/duo-groups.js` are the definitive source of truth for the API contract of each endpoint, detailing all required and optional parameters.

## 🔗 Related File Links
- **The Brains of the Operation (Service):** `allrepo/connectsmart/tsp-api/src/services/duo-groups.js`
- **The Rulebook (Validation):** `allrepo/connectsmart/tsp-api/src/schemas/duo-groups.js`
- **Authentication:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`
- **Header Helper:** `allrepo/connectsmart/tsp-api/src/helpers/fields-of-header.js`

---
*This documentation was generated to provide a comprehensive guide to the many endpoints and functionalities managed by the DUO Groups controller.* 