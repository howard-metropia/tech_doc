# TSP API App Version Controller Documentation

## 🔍 Quick Summary (TL;DR)
The `app-version` controller provides a critical service for mobile clients to check for available application updates, determine if an upgrade is required or optional, and verify if their current version is still supported.

**Keywords:** app-version | version-check | semantic-versioning | semver | force-upgrade | mobile-update | application-support | version-management | tsp-api | ios-update | android-update

**Primary use cases:** 
- Mobile application startup version check.
- Notifying users about available updates.
- Enforcing mandatory updates for critical security patches or features.
- Preventing outdated clients from accessing the API.

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, `semver` for version comparison.

## ❓ Common Questions Quick Index
- **Q: How do I check for the latest app version?** → [Basic Usage](#basic-usage)
- **Q: What's the difference between `required_upgrade` and `can_upgrade`?** → [Response Fields Explained](#response-fields-explained)
- **Q: How do you handle different operating systems (iOS/Android)?** → [URL Parameters](#url-parameters)
- **Q: What version format should the client send?** → [Semantic Versioning (semver)](#semantic-versioning-semver)
- **Q: What happens if I send an invalid version string?** → [Error Handling](#error-handling)
- **Q: How is the "newest" version determined?** → [Execution Flow Analysis](#execution-flow-analysis)
- **Q: Can this endpoint be used for web applications?** → Primarily for mobile, but OS parameter is flexible.
- **Q: What is the `base_version` field for?** → [Response Fields Explained](#response-fields-explained)

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this controller as a **gatekeeper at an event**. When you arrive, the gatekeeper checks your ticket (your app version). They can tell you if a newer, better ticket is available (`can_upgrade`), if your current ticket is so old that you *must* get a new one to enter (`required_upgrade`), or if your ticket is no longer valid at all (`supported: false`). This ensures everyone inside has a modern ticket, providing a consistent and secure experience for all attendees.

**Technical explanation:** 
This Koa.js controller exposes a `GET /api/v1/app_version/:os` endpoint to facilitate client application version management. It retrieves the latest published version for a given operating system (`os`) from the `AppUpdate` database model. It then uses the `semver` library to compare the client's version (passed in headers or query parameters) against the latest version, calculating boolean flags (`required_upgrade`, `can_upgrade`, `supported`) to inform the client's update strategy.

**Business value explanation:**
This controller is essential for maintaining a healthy and secure mobile application ecosystem. It allows the business to seamlessly roll out new features, deprecate old ones, and enforce critical updates, reducing fragmentation in the user base. This minimizes support costs for outdated versions and ensures a consistent user experience, while also providing a mechanism to quickly patch security vulnerabilities across all active clients.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/app-version.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** REST API Controller
- **File Size:** ~2.1 KB
- **Complexity Score:** ⭐⭐ (Medium-Low - Involves database queries and specific logic with the `semver` library)

**Dependencies (Criticality Level):**
- `@koa/router`: HTTP routing framework (**Critical**)
- `semver`: Semantic versioning parser and comparator (**Critical**)
- `@maas/core/response`: Standardized success/error response formatting (**High**)
- `@maas/core/log`: Centralized logging utility (**High**)
- `@app/src/schemas/app-version`: Joi validation schemas for input (**High**)
- `@app/src/models/AppUpdate`: Bookshelf/Knex model for database interaction (**Critical**)
- `@app/src/static/error-code`: Static error code definitions (**Medium**)

**Database Schema (`AppUpdate` model):**
- `app_os` (string): The operating system (e.g., 'ios', 'android').
- `app_version` (string): The version string, compliant with semver (e.g., '2.1.0').
- `published` (char): A flag indicating if the version is live ('T' for true, 'F' for false).
- `id`: Primary key, used for ordering to find the latest entry.

## 📝 Detailed Code Analysis

### Main Route Definition

**`GET /app_version/:os` Endpoint Signature:**
```javascript
router.get('getAppVersion', '/app_version/:os', async (ctx) => { ... })
```

**URL Parameters:**
- `os`: (Required) The operating system of the client application. Examples: `ios`, `android`.

**Query/Header Parameters (Validated by Joi):**
- `newversion` (Header): The client's current version string.
- `version` (Query): An alternative way to pass the client's version string. `newversion` is prioritized.

### Execution Flow Analysis

1.  **Input Validation**: The `inputValidator` (Joi schema) validates and extracts parameters from the URL (`os`), headers (`newversion`), and query string (`version`).
2.  **Database Query**: The code queries the `AppUpdate` table to find the latest version for the specified `os`.
    - It filters for `app_os: os` and `published: 'T'`.
    - It orders by `id` in descending order and takes the `first()` result. This assumes that higher `id` values correspond to newer entries.
3.  **Initialization**: It initializes several variables:
    - `newestVersion` defaults to `'0.0.0'`.
    - `requiredUpgrade`, `canUpgrade`, `supported` are set to `false`.
4.  **Latest Version Check**: If a record is found in the database, `newestVersion` is updated with the version from the database, and `supported` is set based on the `published` flag.
5.  **Client Version Comparison**: If the client provided its version (`version` or `newversion`), the comparison logic is executed:
    - `semver.coerce(version)` is used to clean up the version string into a valid semver format (e.g., `v2.1` becomes `2.1.0`). This adds resilience.
    - `semver.valid()` checks if the coerced version is a valid semantic version. If not, it throws a `400 Bad Request` error.
    - `semver.lt(parsedVersion, newestVersion)` is used to determine if an upgrade is needed. In the current logic, both `requiredUpgrade` and `canUpgrade` are set to `true` if the client's version is less than the newest version.
    - `semver.lte(parsedVersion, newestVersion)` determines if the client version is supported.
6.  **Response Formation**: The controller constructs a success response containing the calculated flags and version information and sends it to the client.

### Semantic Versioning (`semver`)
This controller relies heavily on the `semver` library, which follows the standard `MAJOR.MINOR.PATCH` versioning scheme.
- `semver.lt()`: Checks if version A is **less than** version B.
- `semver.lte()`: Checks if version A is **less than or equal to** version B.
- `semver.coerce()`: This is a crucial function that attempts to convert a potentially "dirty" version string into a clean one. For example, `v2.1-beta` would be coerced to `2.1.0`. This makes the endpoint more robust against slightly different version formats sent by clients.

## 🚀 Usage Methods

### Basic Usage
Check the latest version for an Android client that is currently on version `2.0.5`.

**cURL Example:**
```bash
curl -X GET "https://api.tsp.example.com/api/v1/app_version/android?version=2.0.5" \
  -H "Content-Type: application/json"
```
*Alternatively, using the header:*
```bash
curl -X GET "https://api.tsp.example.com/api/v1/app_version/android" \
  -H "Content-Type: application/json" \
  -H "newversion: 2.0.5"
```

**JavaScript Fetch Usage:**
```javascript
async function checkAppVersion(os, currentVersion) {
  try {
    const response = await fetch(`/api/v1/app_version/${os}?version=${currentVersion}`);
    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }
    const versionData = await response.json();
    console.log(versionData);
    return versionData.data;
  } catch (error) {
    console.error('Failed to check app version:', error);
    // Return a default state allowing the app to continue if the check fails
    return { required_upgrade: false, can_upgrade: false, supported: true };
  }
}

// Example call
checkAppVersion('ios', '3.1.0');
```

## 📊 Output Examples

### Scenario 1: Upgrade is Available and Required
Client version `2.0.0`, newest version `2.1.0`.

```json
{
  "result": "success",
  "data": {
    "newest_version": "2.1.0",
    "base_version": "2.1.0",
    "required_upgrade": true,
    "can_upgrade": true,
    "supported": true,
    "headerVersion": null
  }
}
```

### Scenario 2: Client is Up-to-Date
Client version `2.1.0`, newest version `2.1.0`.

```json
{
  "result": "success",
  "data": {
    "newest_version": "2.1.0",
    "base_version": "2.1.0",
    "required_upgrade": false,
    "can_upgrade": false,
    "supported": true,
    "headerVersion": null
  }
}
```

### Scenario 3: No Client Version Provided
The response simply returns the latest available version information without any comparison flags.

```json
{
  "result": "success",
  "data": {
    "newest_version": "2.1.0",
    "base_version": "2.1.0",
    "required_upgrade": false,
    "can_upgrade": false,
    "supported": true,
    "headerVersion": null
  }
}
```

### Error Response (Invalid Version String)
Client sends `version=invalid`.

```json
{
    "error": "ERROR_BAD_REQUEST_PARAMS",
    "message": "Invalid Version: invalid",
    "code": 400
}
```

## ⚠️ Important Notes

### Response Fields Explained
- `newest_version`: The latest published version available for the specified OS.
- `base_version`: Currently, this is redundant and always equals `newest_version`. It might be intended for future use where a "minimum supported version" is different from the "latest version".
- `required_upgrade`: This boolean flag tells the client that it *must* upgrade. In the current implementation, this is true any time the client's version is lower than the newest.
- `can_upgrade`: This flag indicates an upgrade is available. It is also true any time the client's version is lower than the newest.
- `supported`: Indicates if the client's current version is considered supported. True if the client version is less than or equal to the newest version. An unsupported version would imply the app should stop working.

### Logic Anomaly
The current logic sets `required_upgrade` and `can_upgrade` to the same value (`semver.lt(parsedVersion, newestVersion)`). In a more typical scenario, there would be two different versions in the database: a `minimum_required_version` and a `latest_available_version`. This would allow for optional updates. For example:
- `required_upgrade = semver.lt(parsedVersion, minimum_required_version)`
- `can_upgrade = semver.lt(parsedVersion, latest_available_version)`

As it stands, every available update is presented as a required one.

### Troubleshooting Guide
- **Symptom: Getting a 400 error.**
  - **Diagnosis:** The version string sent by the client is not in a format that `semver.coerce` can understand.
  - **Solution:** Ensure the client sends a version string with numbers, like `2.1.0` or `v2.1`. Check the server logs for the exact `Invalid Version` message.

- **Symptom: `required_upgrade` is always true, even for minor patches.**
  - **Diagnosis:** This is the expected behavior based on the current implementation. Any version that is not the absolute latest is considered to require an upgrade.
  - **Solution:** If optional updates are needed, the backend logic and database schema must be modified to support a "minimum required version" alongside the "newest version".

## 🔗 Related File Links
- **Database Model:** `allrepo/connectsmart/tsp-api/src/models/AppUpdate.js` (*The source of truth for version information.*)
- **Input Schema:** `allrepo/connectsmart/tsp-api/src/schemas/app-version.js` (*Defines the validation rules for incoming requests.*)
- **External Library:** [npm `semver`](https://www.npmjs.com/package/semver) (*The core dependency for all version comparison logic.*)

---
*This documentation was regenerated to provide more comprehensive details, analysis, and context based on the provided template.*
