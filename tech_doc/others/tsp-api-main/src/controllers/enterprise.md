# TSP API Enterprise Controller Documentation

## 🔍 Quick Summary (TL;DR)
The enterprise controller manages corporate carpool group functionality, handling email verification, enterprise membership management, and telework scheduling for employees of registered organizations.

**Keywords:** enterprise | carpool-groups | email-verification | corporate-mobility | employee-management | domain-verification | telework | duo-groups | business-authentication | organization-management | company-transport | employee-verification

**Primary use cases:** 
- Corporate employees joining company carpool groups through email verification
- Managing enterprise-specific features and user permissions
- Telework scheduling and management for remote workers
- Enterprise admin functions for managing employee access

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, @koa/router v10.x, Knex.js

## ❓ Common Questions Quick Index
- **Q: How do employees join their company's carpool group?** → [Enterprise Email Verification](#enterprise-email-verification-post-setting_carpool_email)
- **Q: What happens when someone uses their work email to register?** → [Email Domain Validation](#email-domain-validation)
- **Q: How does the system verify someone actually works at a company?** → [Employee Status Verification](#employee-status-verification)
- **Q: Can invited users join groups from different enterprises?** → [Invited Domain Handling](#invited-domain-handling)
- **Q: What is the telework feature for?** → [Telework Management](#telework-management)
- **Q: How do administrators manage enterprise users?** → [Enterprise Administration](#enterprise-administration)
- **Q: What happens if someone's work email is already being used?** → [Duplicate Email Handling](#duplicate-email-handling)
- **Q: How does the system prevent spam or abuse?** → [Email Blocking System](#email-blocking-system)
- **Q: What's the difference between invited and domain-based membership?** → [Membership Types](#membership-types)
- **Q: How is multi-language support handled?** → [Internationalization](#internationalization)

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this controller as a **corporate security gate with a HR system**. When employees want to join their company's ride-sharing program, they show their company email (like a work badge). The system acts like a security guard who: 1) checks if their company has a carpool program, 2) verifies they really work there by sending a confirmation email, 3) lets them into the appropriate carpool groups, and 4) manages their work-from-home schedules. It's like having an automated HR assistant that handles all the paperwork for corporate transportation benefits.

**Technical explanation:** 
A comprehensive Koa.js REST controller that provides enterprise integration services for corporate mobility programs. It implements a sophisticated email-based verification system that validates employee membership through domain matching and invitation systems. The controller manages the complex relationship between enterprises, employees, and carpool groups (DuoGroups), while also providing telework scheduling functionality for remote work management.

**Business value explanation:**
This controller enables large organizations to seamlessly integrate their employees into the MaaS platform while maintaining security and organizational boundaries. It reduces administrative overhead for corporate transportation programs by automating employee verification and group assignments, while providing valuable telework scheduling that supports hybrid work policies and reduces unnecessary commuting.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/enterprise.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** REST API Controller
- **File Size:** ~11 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High - Complex business logic, multiple database interactions, email verification flows)

**Dependencies (Criticality Level):**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing middleware (**Critical**)
- `@maas/core/response`: Standardized success/error response formatting (**High**)
- `@maas/core`: Core framework including MaasError (**Critical**)
- `@app/src/middlewares/auth`: JWT authentication middleware (**Critical**)
- `@app/src/helpers/fields-of-header`: Header field extraction utility (**High**)
- `@app/src/schemas/enterprise`: Joi validation schemas (**Critical**)
- `@app/src/services/enterprise`: Business logic service layer (**Critical**)

**Database Models (Criticality Level):**
- `DuoGroups`: Carpool group management (**Critical**)
- `Enterprise`: Enterprise and employee records (**Critical**)
- `AuthUsers`: User authentication data (**Critical**)
- `EnterpriseInvites`: Email invitation system (**High**)
- `EnterpriseBlocks`: Email blocking/spam prevention (**Medium**)

**Security Requirements:**
- **Authentication:** JWT-based authentication required for all endpoints
- **Email Verification:** Multi-step email verification process for security
- **Domain Validation:** Enterprise domain verification to prevent unauthorized access
- **Anti-Abuse:** Email blocking system to prevent spam and misuse

## 📝 Detailed Code Analysis

### Main Endpoints

#### Enterprise Email Verification (`POST /setting_carpool_email`)
- **Purpose:** Initiates or completes the process for employees to join enterprise carpool groups
- **Flow:**
    1. **Input Validation:** Validates email, verify_type, group_id, and user context
    2. **Enterprise Discovery:** Finds enterprise ID from email domain or invitation list
    3. **Group Validation:** For carpool verification, checks if requested DuoGroup exists for the enterprise
    4. **Duplicate Check:** Ensures email isn't already used by another user
    5. **Block Check:** Verifies email isn't in the blocked list
    6. **Status Evaluation:** Either directly joins verified employees or sends verification email

#### Email Verification Confirmation (`GET /verify_carpool_email.html`)
- **Purpose:** Handles the verification link clicked in enterprise verification emails
- **Flow:**
    1. **Token Validation:** Validates the verification token from the email link
    2. **Language Processing:** Extracts language code for localized response
    3. **Verification Processing:** Delegates to service layer for completion
    4. **HTML Response:** Returns appropriate HTML page based on verification result

#### Enterprise User Management (`POST /enterprise/delete`)
- **Purpose:** Allows deletion of unverified enterprise users
- **Flow:**
    1. **Permission Check:** Validates user has permission to delete the target user
    2. **Status Filter:** Only deletes users who haven't completed email verification
    3. **Database Cleanup:** Removes unverified enterprise records
    4. **Security Response:** Returns updated security key for session management

#### Telework Management (`GET|POST /telework`)
- **Purpose:** Manages remote work schedules for enterprise employees
- **Flow:**
    1. **User Context:** Extracts user ID from headers
    2. **Data Retrieval/Update:** Gets or updates telework settings
    3. **Service Delegation:** Uses enterprise service for business logic
    4. **Consistent Response:** Returns current telework status

#### Telework Search (`GET /telework/search`)
- **Purpose:** Provides search functionality for telework-related data
- **Advanced Features:** Supports filtering and searching telework records

### Key Business Logic Components

#### Email Domain Validation
The system implements sophisticated logic to determine enterprise membership:
```javascript
// Fetch enterprise ID from email domain
const enterpriseIdFromEmail = await getEnterpriseId(email);

// Check invitation list for explicit invitations
const invited = await EnterpriseInvites.query()
  .where('email', email)
  .first();
```

#### Membership Types
1. **Domain-based:** Users with emails matching enterprise domains
2. **Invitation-based:** Users explicitly invited to specific enterprises
3. **Priority System:** Invitation-based membership takes precedence over domain-based

#### Employee Status Verification
The system checks multiple conditions before allowing group access:
- Enterprise group existence validation
- Email duplication prevention
- Email blocking verification
- Employee verification status

## 🚀 Usage Methods

### Enterprise Email Verification
```bash
# Employee initiating carpool group join process
curl -X POST "https://api.tsp.example.com/api/v1/setting_carpool_email" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@company.com",
    "verify_type": "carpool",
    "group_id": 100
  }'
```

### Telework Schedule Management
```bash
# Get current telework settings
curl -X GET "https://api.tsp.example.com/api/v1/telework" \
  -H "userid: usr_12345"

# Update telework schedule
curl -X POST "https://api.tsp.example.com/api/v1/telework" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "schedule": {
      "monday": "office",
      "tuesday": "home",
      "wednesday": "office",
      "thursday": "home",
      "friday": "office"
    }
  }'
```

### Enterprise User Deletion
```bash
# Remove unverified enterprise user
curl -X POST "https://api.tsp.example.com/api/v1/enterprise/delete" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_admin" \
  -H "Content-Type: application/json" \
  -d '{
    "enterprise_id": 500,
    "user_id": "usr_target"
  }'
```

## 📊 Output Examples

### Successful Email Verification Initiation
```json
{
  "result": "success",
  "data": {}
}
```

### Enterprise Group Not Found Error
```json
{
  "error": "ERROR_ENTERPRISE_EMAIL_INVALID",
  "message": "The provided email domain is not associated with any enterprise carpool groups",
  "code": 403
}
```

### Email Already in Use Error
```json
{
  "error": "ERROR_ENTERPRISE_EMAIL_DUPLICATE",
  "message": "This enterprise email is already registered to another user",
  "code": 400
}
```

### Telework Schedule Response
```json
{
  "result": "success",
  "data": {
    "schedule": {
      "monday": "office",
      "tuesday": "home",
      "wednesday": "office",
      "thursday": "home",
      "friday": "office"
    },
    "preferences": {
      "notification_enabled": true,
      "auto_update_location": true
    }
  }
}
```

### Email Blocked Response
```json
{
  "error": "ERROR_EMAIL_ALREADY_IN_BLOCKED",
  "message": "This email address has been blocked from enterprise services",
  "code": 403
}
```

## ⚠️ Important Notes

### Security Considerations
- **Email Verification:** Multi-step verification prevents unauthorized enterprise access
- **Domain Validation:** Prevents users from joining enterprises they don't belong to
- **Invitation System:** Allows controlled access for contractors and external users
- **Blocking System:** Prevents abuse through email-based blocking mechanism

### Enterprise Integration Patterns
1. **Automatic Discovery:** Users with matching email domains are automatically eligible
2. **Explicit Invitation:** HR departments can invite specific users regardless of domain
3. **Hybrid Approach:** System supports both automatic and manual enrollment methods

### Business Logic Complexity
The controller implements complex decision trees for enterprise membership:
- Domain matching vs invitation precedence
- Group availability validation
- Employee status verification
- Anti-abuse mechanisms

### Telework Feature Integration
The telework functionality provides:
- Schedule management for hybrid work arrangements
- Integration with transportation planning
- Support for corporate mobility policies
- Analytics for enterprise transportation optimization

### Troubleshooting Guide

1. **Symptom: User can't join enterprise group despite valid work email**
   - **Diagnosis:** Enterprise domain may not be registered or group doesn't exist
   - **Solution:** Verify enterprise domain registration and group configuration

2. **Symptom: Email verification emails not being received**
   - **Diagnosis:** Email may be blocked or SMTP configuration issue
   - **Solution:** Check EnterpriseBlocks table and verify email service configuration

3. **Symptom: Users getting duplicate email errors**
   - **Diagnosis:** Email already associated with another user account
   - **Solution:** Check Enterprise table for existing email associations

4. **Symptom: Telework features not working**
   - **Diagnosis:** User may not be properly associated with enterprise
   - **Solution:** Verify enterprise membership and employee_status flag

## 🔗 Related File Links

- **Services:** `allrepo/connectsmart/tsp-api/src/services/enterprise.js`
- **Validation Schemas:** `allrepo/connectsmart/tsp-api/src/schemas/enterprise.js`
- **Database Models:** 
  - `allrepo/connectsmart/tsp-api/src/models/DuoGroups.js`
  - `allrepo/connectsmart/tsp-api/src/models/Enterprises.js`
  - `allrepo/connectsmart/tsp-api/src/models/EnterpriseInvites.js`
  - `allrepo/connectsmart/tsp-api/src/models/EnterpriseBlocks.js`
- **Middleware:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`
- **Helpers:** `allrepo/connectsmart/tsp-api/src/helpers/fields-of-header.js`

## 📈 Use Cases

### Daily Usage Scenarios
- **New Employee Onboarding:** Automatic integration into company carpool programs
- **Contractor Management:** Invitation-based access for temporary workers
- **Telework Planning:** Daily schedule management for hybrid workers
- **Administrative Tasks:** Enterprise admin managing user access and permissions

### Integration Application Scenarios
- **HR System Integration:** Automated employee verification and onboarding
- **Corporate Mobility Programs:** Seamless integration with company transportation benefits
- **Remote Work Management:** Integration with corporate telework policies
- **Security Compliance:** Enterprise-grade access control and audit trails

### Scaling Scenarios
- **Large Enterprise Deployment:** Handling thousands of employees across multiple domains
- **Multi-tenant Architecture:** Supporting multiple enterprises with isolated data
- **High-volume Verification:** Managing large-scale email verification campaigns
- **Global Organizations:** Supporting international enterprises with complex domain structures

## 🛠️ Improvement Suggestions

### Performance Optimizations
- **Database Indexing:** Add composite indexes on enterprise_id + email combinations
- **Caching Strategy:** Implement Redis caching for enterprise domain lookups
- **Batch Processing:** Add bulk invitation processing for large enterprise deployments

### Feature Enhancements
- **SAML Integration:** Support for enterprise single sign-on (SSO) systems
- **Advanced Telework:** Calendar integration and smart schedule suggestions
- **Analytics Dashboard:** Enterprise-level reporting and usage analytics
- **Mobile App Integration:** Enhanced mobile experience for enterprise features

### Security Improvements
- **Multi-factor Authentication:** Add MFA for enterprise admin functions
- **Audit Logging:** Comprehensive audit trails for compliance requirements
- **Rate Limiting:** Advanced rate limiting for verification endpoints
- **Email Security:** Enhanced email validation and anti-spoofing measures

---
*This documentation provides comprehensive coverage of the enterprise controller functionality, focusing on corporate mobility integration and employee management features.*