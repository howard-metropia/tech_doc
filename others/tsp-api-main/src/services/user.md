# User Service Documentation

## 🔍 Quick Summary (TL;DR)
The User Service handles user account deletion, logout, and profile management operations in the TSP API, ensuring secure removal of sensitive data across multiple systems while maintaining audit trails and enterprise compliance.

**Core Keywords:** user management | account deletion | profile service | logout | GDPR compliance | data privacy | user profiles | enterprise integration | duo groups | backup system

**Primary Use Cases:**
- Complete user account deletion with data anonymization
- User logout with token invalidation
- Bulk user profile retrieval with metadata enrichment
- Enterprise group management during account deletion

**Compatibility:** Node.js 14+, Koa.js, MySQL, MongoDB, Knex.js, Mongoose

## ❓ Common Questions Quick Index
1. **Q: How do I delete a user account completely?** → [See delete() method](#delete-method)
2. **Q: What happens to user data after deletion?** → [See Data Anonymization](#data-anonymization)
3. **Q: How to logout a user securely?** → [See logout() method](#logout-method)
4. **Q: Can I retrieve multiple user profiles at once?** → [See profiles() method](#profiles-method)
5. **Q: What if user deletion fails due to enterprise groups?** → [See Error Handling](#error-handling)
6. **Q: How to troubleshoot failed user deletions?** → [See Troubleshooting](#troubleshooting-deletions)
7. **Q: What data is backed up before deletion?** → [See Backup Process](#backup-process)
8. **Q: How does CDN URL generation work?** → [See cdnURL() utility](#cdnurl-utility)
9. **Q: What are the performance implications of bulk operations?** → [See Performance Notes](#performance-notes)
10. **Q: How to handle guest user accounts?** → [See Guest Users](#guest-users)

## 📋 Functionality Overview

### Non-technical Explanation
Think of this service as a **professional data custodian** that manages three critical operations:
1. **Account Deletion** - Like a secure shredding service that not only destroys documents but keeps a receipt of what was destroyed for legal compliance
2. **Logout** - Similar to a hotel checkout that invalidates your room key and clears your access
3. **Profile Management** - Like a directory service that can quickly provide formatted contact cards for multiple people

### Technical Explanation
The User Service implements GDPR-compliant user data management with cascading deletion across MySQL and MongoDB databases, maintaining audit trails through backup tables, and providing efficient bulk profile retrieval with customizable metadata enrichment. It follows a defensive programming pattern with comprehensive error handling and transaction-like operations across multiple data stores.

### Business Value
- **Compliance**: Ensures GDPR and privacy law compliance through complete data anonymization
- **Security**: Prevents data leaks by thoroughly clearing sensitive information
- **Efficiency**: Bulk operations reduce API calls and improve performance
- **Auditability**: Maintains deletion history for compliance reporting

### System Context
This service integrates with the authentication system, enterprise management, duo groups, and various data storage systems (MySQL, MongoDB) to provide comprehensive user lifecycle management within the TSP ecosystem.

## 🔧 Technical Specifications

### File Information
- **Path**: `/allrepo/connectsmart/tsp-api/src/services/user.js`
- **Type**: Service Module
- **Language**: JavaScript (ES6+)
- **Size**: ~290 lines
- **Complexity Score**: Medium-High (involves multiple database operations)

### Dependencies
| Package | Version | Purpose | Criticality |
|---------|---------|---------|-------------|
| @maas/core/mysql | Latest | Database connection (Knex) | Critical |
| @maas/core/log | Latest | Logging infrastructure | High |
| @app/src/services/duo-groups | Internal | Enterprise group management | High |
| @app/src/models/* | Internal | ORM models | Critical |
| config | Latest | AWS configuration | Medium |

### Configuration Parameters
```javascript
// AWS S3 Configuration (from config/default.js)
{
  vendor: {
    aws: {
      region: 'us-west-2', // Default region
      s3: {
        bucketName: 'maas-assets' // CDN bucket
      }
    }
  }
}
```

### System Requirements
- **Database**: MySQL 5.7+, MongoDB 4.0+
- **Node.js**: 14.x or higher
- **Memory**: 512MB minimum for bulk operations
- **Network**: Access to AWS S3 for CDN operations

## 📝 Detailed Code Analysis

### Main Exports
```javascript
module.exports = {
  delete: async (userId) => Promise<void>,
  logout: async (userId) => Promise<void>,
  profiles: async (userIds, meta = []) => Promise<Array>,
  getById: async (userId) => Promise<Object>,
  cdnURL: (path) => String
}
```

### Delete Method
**Purpose**: Comprehensive user account deletion with data anonymization

**Execution Flow**:
1. Verify user existence
2. Backup user profile to `auth_user_bk` table
3. Log deletion event
4. Leave all duo groups (with error handling)
5. Clear Bytemark ticket sensitive data
6. Anonymize enterprise data
7. Delete user favorites
8. Anonymize all user fields in auth_users table

**Key Code Snippet**:
```javascript
// Backup process
const bkUser = { ...userProfile, auth_user_id: userId };
delete bkUser.id;
delete bkUser.is_guest;
// ... remove transient fields

// Anonymization example
await AuthUsers.query().update({
  first_name: '',
  last_name: '',
  email: '',
  // ... set all sensitive fields to empty/default
}).where('id', userId);
```

### Logout Method
**Purpose**: Invalidate user session and clear device tokens

**Implementation**:
```javascript
await AuthUsers.query().update({
  access_token: 'LOGOUT',
  device_token: '',
  apns_device_token: ''
}).where('id', userId);
```

### Profiles Method
**Purpose**: Bulk user profile retrieval with metadata enrichment

**Features**:
- Chinese name formatting support
- Configurable metadata inclusion (vehicle, phone, device)
- CDN URL generation for avatars
- Guest user identification

**Metadata Options**:
- `vehicle`: Basic vehicle information
- `vehicle_detail`: Extended vehicle data with images
- `phone`: Contact information
- `device`: Device and notification details

## 🚀 Usage Methods

### Basic Usage
```javascript
const userService = require('./services/user');

// Delete a user account
try {
  await userService.delete(12345);
  console.log('User deleted successfully');
} catch (error) {
  console.error('Deletion failed:', error.message);
}

// Logout a user
await userService.logout(12345);

// Get multiple user profiles
const profiles = await userService.profiles(
  [123, 456, 789], 
  ['vehicle', 'phone']
);
```

### Advanced Configuration
```javascript
// Retrieve profiles with all metadata
const detailedProfiles = await userService.profiles(
  userIds,
  ['vehicle_detail', 'phone', 'device', 'custom_field']
);

// Get single user by ID (with email validation)
const user = await userService.getById(userId);
```

## 📊 Output Examples

### Successful Profile Retrieval
```json
[
  {
    "id": 123,
    "user_id": 123,
    "email": "user@example.com",
    "name": {
      "first_name": "John",
      "last_name": "Doe"
    },
    "full_name": "John D.",
    "avatar": "https://s3-us-west-2.amazonaws.com/maas-assets/avatar123.jpg",
    "rating": 4.5,
    "is_guest": false,
    "vehicle": {
      "type": "sedan",
      "color": "blue",
      "plate": "ABC123"
    }
  }
]
```

### Error Responses
```javascript
// User not found
{
  "error": "ERROR_USER_NOT_FOUND",
  "code": 404,
  "message": "User not found"
}

// Duo group deletion failure (handled internally)
{
  "code": "ERROR_DUO_GROUP_NOT_FOUND",
  "message": "Group no longer exists"
}
```

## ⚠️ Important Notes

### Security Considerations
- All sensitive data is permanently anonymized, not just deleted
- Backup records maintain audit trail without sensitive information
- Token invalidation prevents session hijacking
- CDN URLs are generated securely with AWS S3

### Permission Requirements
- Database write access for user tables
- MongoDB write access for Bytemark tickets
- AWS S3 read access for CDN operations

### Common Troubleshooting

**Issue: User deletion fails with duo group error**
- **Symptom**: Error during deletion process
- **Diagnosis**: Private duo group may be disabled
- **Solution**: Service automatically handles by force-deleting group membership

**Issue: Slow bulk profile retrieval**
- **Symptom**: Timeout on large user lists
- **Diagnosis**: Too many users in single request
- **Solution**: Batch requests to 100 users maximum

### Performance Optimization
- Use `profiles()` for bulk retrieval instead of multiple `getById()` calls
- Consider caching CDN URLs as they don't change frequently
- Monitor duo group operations as they involve external service calls

## 🔗 Related File Links

### Project Structure
```
tsp-api/
├── src/
│   ├── services/
│   │   ├── user.js (this file)
│   │   └── duo-groups.js (enterprise groups)
│   ├── models/
│   │   ├── AuthUsers.js
│   │   ├── AuthUserBk.js
│   │   └── DuoGroupMembers.js
│   └── static/
│       └── error-code.js
```

### Related Services
- **Authentication Service**: Token management and validation
- **Enterprise Service**: Company-specific user management
- **Duo Groups Service**: Team and group functionality

## 📈 Use Cases

### Daily Operations
- **Customer Support**: Handling GDPR deletion requests
- **Session Management**: Force logout for security incidents
- **Profile Display**: Mobile app user listings

### Development Integration
- **Testing**: Create and delete test users
- **Migration**: Bulk user data updates
- **Analytics**: Export user profile data

### Scaling Scenarios
- **High Traffic**: Cache profile data for frequently accessed users
- **Large Datasets**: Implement pagination for profile retrieval
- **Multi-region**: Consider CDN edge locations for avatars

## 🛠️ Improvement Suggestions

### Code Optimization
1. **Transaction Support**: Wrap deletion in database transaction (High Priority)
2. **Async Optimization**: Parallelize independent operations (Medium Priority)
3. **Caching Layer**: Add Redis caching for profile data (Low Priority)

### Feature Expansion
1. **Soft Delete Option**: Add flag to preserve data for recovery (Medium Effort)
2. **Bulk Operations**: Add bulk delete and logout methods (High Effort)
3. **Event Streaming**: Emit deletion events for downstream systems (Medium Effort)

### Technical Debt
- Extract magic strings to constants
- Add comprehensive input validation
- Implement retry logic for external service calls

## 🏷️ Document Tags

**Keywords**: user management, account deletion, profile service, logout, GDPR, data privacy, anonymization, enterprise integration, duo groups, bytemark tickets, AWS S3, CDN, bulk operations, audit trail, compliance

**Technical Tags**: #service #user-management #database #mysql #mongodb #knex #mongoose #aws-s3 #async #data-privacy

**Target Roles**: 
- Backend Developer (Mid-Senior level)
- DevOps Engineer (Security focus)
- Customer Support (GDPR requests)
- System Administrator (User management)

**Difficulty Level**: ⭐⭐⭐ (Medium-High complexity due to multi-system coordination)

**Maintenance Level**: Medium (Monthly reviews for compliance updates)

**Business Criticality**: Critical (User data management is core functionality)

**Related Topics**: Authentication, Authorization, Data Privacy, GDPR Compliance, Enterprise Management, Cloud Storage, Database Operations