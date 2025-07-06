# TSP API User Controller Documentation

## 🔍 Quick Summary (TL;DR)
The user controller handles critical user account operations including account deletion and logout functionality with proper authentication and service delegation.

**Keywords:** user-management | account-deletion | user-logout | authentication | user-service | account-operations | user-lifecycle

**Primary use cases:** Deleting user accounts, logging out users, managing user lifecycle, handling account termination

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, user management systems

## ❓ Common Questions Quick Index
- **Q: What user operations are supported?** → Account deletion and logout
- **Q: Is authentication required?** → Yes, JWT authentication for both operations
- **Q: What happens during account deletion?** → Complete account removal via UserService
- **Q: How is logout handled?** → Session termination and cleanup via UserService
- **Q: Why different API versions?** → Logout uses v1 for backward compatibility, deletion uses v2
- **Q: Are operations reversible?** → Deletion is permanent, logout can be reversed by re-login

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as the **account management center** for users. It handles two critical actions: when someone wants to permanently delete their account and all their data, and when they want to log out of the app. It's like having a secure reception desk that can either help you check out temporarily or completely close your account forever.

**Technical explanation:** 
A minimal Koa.js REST controller that provides essential user lifecycle management through two secure endpoints. It handles account deletion with complete data removal and user logout with session termination, both requiring authentication and delegating complex operations to the UserService layer.

**Business value explanation:**
Essential for user privacy compliance (GDPR/CCPA), account security, and user experience. Enables users to exercise data deletion rights, provides secure session management, and supports user retention through proper logout/re-login workflows while maintaining platform security standards.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/user.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** User Management Controller
- **File Size:** ~0.8 KB
- **Complexity Score:** ⭐⭐ (Low-Medium - Critical operations with service delegation)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `@maas/core/response`: Standardized response formatting (**High**)
- `@app/src/services/user`: Core user management service (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `@app/src/middlewares/auth`: JWT authentication (**Critical**)

## 📝 Detailed Code Analysis

### Account Deletion Endpoint (`POST /api/v2/deletion`)

**Purpose:** Permanently deletes user account and all associated data

**Processing Flow:**
1. **Authentication:** JWT validation via auth middleware
2. **User ID Extraction:** Gets user ID from request headers
3. **Type Conversion:** Converts user ID to integer
4. **Service Delegation:** Calls UserService.delete for complete removal
5. **Response:** Returns empty success response

**Implementation:**
```javascript
const userId = parseInt(ctx.request.header.userid);
await UserService.delete(userId);
ctx.body = success({});
```

### User Logout Endpoint (`POST /api/v1/logout`)

**Purpose:** Logs out user and terminates active sessions

**Processing Flow:**
1. **Authentication:** JWT validation required
2. **User Context:** Extracts user ID from headers
3. **Session Termination:** Calls UserService.logout for cleanup
4. **Response:** Returns empty success confirmation

**Backward Compatibility Note:**
```javascript
// 此為 API 重構項目，因此 URL 仍為 /api/v1/logout
// This is an API refactoring project, so URL remains /api/v1/logout
```

**Implementation:**
```javascript
await UserService.logout(parseInt(ctx.request.header.userid));
ctx.body = success({});
```

## 🚀 Usage Methods

### Account Deletion
```bash
curl -X POST "https://api.tsp.example.com/api/v2/deletion" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json"
```

### User Logout
```bash
curl -X POST "https://api.tsp.example.com/api/v1/logout" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "userid: usr_12345" \
  -H "Content-Type: application/json"
```

### JavaScript Client Example
```javascript
class UserManager {
  constructor(authToken, userId) {
    this.authToken = authToken;
    this.userId = userId;
    this.baseHeaders = {
      'Authorization': `Bearer ${authToken}`,
      'userid': userId,
      'Content-Type': 'application/json'
    };
  }

  async deleteAccount() {
    try {
      const response = await fetch('/api/v2/deletion', {
        method: 'POST',
        headers: this.baseHeaders
      });
      
      const result = await response.json();
      
      if (result.result === 'success') {
        console.log('Account deleted successfully');
        // Clear local storage, redirect to homepage, etc.
        localStorage.clear();
        window.location.href = '/';
        return true;
      } else {
        console.error('Account deletion failed:', result.error);
        throw new Error(result.error);
      }
    } catch (error) {
      console.error('Account deletion error:', error);
      throw error;
    }
  }

  async logout() {
    try {
      const response = await fetch('/api/v1/logout', {
        method: 'POST',
        headers: this.baseHeaders
      });
      
      const result = await response.json();
      
      if (result.result === 'success') {
        console.log('Logged out successfully');
        // Clear auth tokens, redirect to login, etc.
        localStorage.removeItem('authToken');
        localStorage.removeItem('userId');
        window.location.href = '/login';
        return true;
      } else {
        console.error('Logout failed:', result.error);
        throw new Error(result.error);
      }
    } catch (error) {
      console.error('Logout error:', error);
      throw error;
    }
  }
}

// Usage examples
const userManager = new UserManager(authToken, userId);

// User logout
userManager.logout();

// Account deletion (with confirmation)
if (confirm('Are you sure you want to permanently delete your account? This action cannot be undone.')) {
  userManager.deleteAccount();
}
```

### Frontend Integration Example
```javascript
// React component example
function AccountSettings({ authToken, userId }) {
  const [isDeleting, setIsDeleting] = useState(false);
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  const handleLogout = async () => {
    setIsLoggingOut(true);
    try {
      await fetch('/api/v1/logout', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'userid': userId,
          'Content-Type': 'application/json'
        }
      });
      // Handle successful logout
      onLogout();
    } catch (error) {
      console.error('Logout failed:', error);
      alert('Logout failed. Please try again.');
    }
    setIsLoggingOut(false);
  };

  const handleDeleteAccount = async () => {
    if (!confirm('This will permanently delete your account and all data. Continue?')) {
      return;
    }
    
    setIsDeleting(true);
    try {
      await fetch('/api/v2/deletion', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'userid': userId,
          'Content-Type': 'application/json'
        }
      });
      // Account deleted successfully
      alert('Account deleted successfully');
      onAccountDeleted();
    } catch (error) {
      console.error('Account deletion failed:', error);
      alert('Account deletion failed. Please try again.');
    }
    setIsDeleting(false);
  };

  return (
    <div>
      <button 
        onClick={handleLogout}
        disabled={isLoggingOut}
      >
        {isLoggingOut ? 'Logging out...' : 'Logout'}
      </button>
      
      <button 
        onClick={handleDeleteAccount}
        disabled={isDeleting}
        className="danger"
      >
        {isDeleting ? 'Deleting...' : 'Delete Account'}
      </button>
    </div>
  );
}
```

## 📊 Output Examples

### Successful Account Deletion
```json
{
  "result": "success",
  "data": {}
}
```

### Successful Logout
```json
{
  "result": "success",
  "data": {}
}
```

### Authentication Error
```json
{
  "error": "AuthenticationError",
  "message": "Invalid or expired JWT token",
  "code": 401
}
```

### User Not Found Error
```json
{
  "error": "UserNotFoundError",
  "message": "User account not found",
  "code": 404
}
```

### Account Already Deleted Error
```json
{
  "error": "AccountStateError",
  "message": "User account has already been deleted",
  "code": 400
}
```

## ⚠️ Important Notes

### Account Deletion Considerations
- **Permanent Action:** Account deletion cannot be undone
- **Data Removal:** All user data should be permanently removed
- **Cascade Deletion:** Related data (trips, payments, etc.) must be handled
- **Compliance:** Must meet GDPR/CCPA data deletion requirements
- **Confirmation:** Should require explicit user confirmation
- **Audit Trail:** May need to log deletion events for compliance

### Logout Functionality
- **Session Termination:** Invalidates current user sessions
- **Token Management:** May invalidate JWT tokens
- **Device Cleanup:** May clear device-specific data
- **Multi-device:** May affect sessions on other devices
- **Security:** Ensures secure session termination

### API Versioning
- **Mixed Versions:** Deletion uses v2, logout uses v1
- **Backward Compatibility:** Logout maintains v1 for existing clients
- **Migration Path:** Future versions may standardize on v2
- **Documentation:** Clear version differences for developers

### Security Considerations
- **Authentication Required:** Both operations require valid JWT
- **User Verification:** Operations only affect authenticated user
- **Rate Limiting:** May implement limits to prevent abuse
- **Audit Logging:** Security-sensitive operations should be logged

### Service Layer Delegation
- **Complex Operations:** Heavy lifting done in UserService
- **Transaction Management:** Service handles database transactions
- **Error Handling:** Service layer manages detailed error scenarios
- **Business Logic:** All deletion/logout logic in service layer

### Frontend Integration
- **User Experience:** Provide clear feedback during operations
- **Confirmation Dialogs:** Especially important for account deletion
- **Loading States:** Show progress during async operations
- **Error Handling:** Graceful error messaging to users
- **Cleanup:** Clear local storage and redirect appropriately

### Data Privacy Compliance
- **Right to Deletion:** Supports GDPR Article 17
- **Data Portability:** Should work with data export features
- **Consent Management:** Aligns with privacy policy requirements
- **Retention Policies:** Follows data retention guidelines

## 🔗 Related File Links

- **User Service:** `allrepo/connectsmart/tsp-api/src/services/user.js`
- **Authentication:** `allrepo/connectsmart/tsp-api/src/middlewares/auth.js`
- **User Models:** Related user data models and schemas
- **Privacy Documentation:** Data handling and privacy policies

---
*This controller provides essential user lifecycle management for account security and privacy compliance.*