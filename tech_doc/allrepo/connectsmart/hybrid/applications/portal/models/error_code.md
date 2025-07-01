# Portal Error Code Constants - MaaS Error Handling System

## 🔍 Quick Summary (TL;DR)
Comprehensive error code definition system for Portal MaaS platform providing standardized error handling across user management, payments, carpooling, notifications, and transportation services with categorized numeric codes.

**Keywords**: `error-codes | error-handling | maas-errors | payment-errors | carpooling-errors | user-errors | api-errors | http-status-codes`

**Use Cases**: API error responses, payment failure handling, user validation errors, carpooling coordination errors, system debugging

**Compatibility**: Python 2.7+, Web2py framework, RESTful APIs, ConnectSmart platform

## ❓ Common Questions Quick Index
- Q: What error code should I use for user issues? → [User Error Codes](#user-error-codes)
- Q: How are payment errors categorized? → [Payment Error Codes](#payment-error-codes)
- Q: What carpooling errors exist? → [Carpooling Error Codes](#carpooling-error-codes)
- Q: How do I handle API request errors? → [Request Error Codes](#request-error-codes)
- Q: What's the error code naming convention? → [Error Code Structure](#error-code-structure)
- Q: How do I add new error codes? → [Usage Methods](#usage-methods)
- Q: What notification errors are defined? → [Notification Error Codes](#notification-error-codes)
- Q: How do TapPay errors work? → [TapPay Error Codes](#tappay-error-codes)

## 📋 Functionality Overview
**Non-technical**: Like a comprehensive troubleshooting manual for a transportation app - provides specific error numbers and messages for every possible problem users might encounter, from login issues to payment failures to carpooling conflicts.

**Technical**: Centralized error code constants module defining 100+ standardized error codes across 10 functional categories (10xxx-99xxx range) for consistent error handling throughout the MaaS platform API responses and internal systems.

**Business Value**: Enables consistent error reporting, improves customer support efficiency, facilitates debugging and monitoring, and provides standardized API responses for frontend applications and third-party integrations.

**System Context**: Core error handling foundation for ConnectSmart Portal, used by all API endpoints, payment processing, user management, and transportation services to provide consistent error responses.

## 🔧 Technical Specifications
- **File**: `portal/models/error_code.py` (410 lines)
- **Error Categories**: 10 functional domains with numeric ranges
- **Code Range**: 10001-99999 (5-digit standardized codes)
- **Dependencies**: None (pure constants module)
- **Usage**: Import as constants in API controllers and business logic
- **Maintenance**: Centralized error definition management

### Error Code Categories
- **10xxx**: Request/API errors (tokens, params, encryption)
- **11xxx**: App maintenance errors (version updates)
- **20xxx**: User management errors (registration, authentication)
- **21xxx**: DUO carpooling errors (groups, matching, rides)
- **22xxx**: Trip management errors (routing, validation)
- **23xxx**: Wallet/payment errors (transactions, cards, redemption)
- **24xxx**: Location/trace errors (GPS, mapping)
- **25xxx**: Escrow/balance errors (financial holdings)
- **31xxx**: Notification errors (messaging, delivery)
- **90xxx**: Campaign management errors (marketing)

## 📝 Detailed Code Analysis

### Request Error Codes (10xxx)
```python
# API request validation errors
ERROR_BAD_REQUEST_PARAMS = 10001     # Incorrect action parameters
ERROR_BAD_REQUEST_BODY = 10002       # Invalid request body format
ERROR_TOKEN_REQUIRED = 10003         # Missing authentication token
ERROR_INVALID_TOKEN = 10301          # Invalid token format
ERROR_TOKEN_EXPIRED = 10005          # Expired authentication token
ERROR_TOKEN_CHANGED = 10006          # Token invalidated by new login
ERROR_DECRYPTION_FAILED = 10007      # Payload decryption failed
ERROR_ENCRYPTION_FAILED = 10008      # Response encryption failed
```

### User Error Codes (20xxx)
```python
# User account and authentication errors
ERROR_USER_NOT_FOUND = 20001         # User account doesn't exist
ERROR_USER_NOT_ACTIVATED = 20002     # Account not verified
ERROR_EMAIL_HAS_BEEN_REGISTERED = 20004  # Duplicate email registration
ERROR_WRONG_PASSWORD = 20005         # Invalid login credentials
ERROR_WRONG_ACTIVATE_CODE = 20006    # Invalid verification code
ERROR_NEW_PHONE_HAS_BEEN_USED = 20015   # Phone number already taken
ERROR_ENTERPRISE_EMAIL_INVALID = 20018  # Invalid corporate email
```

### Carpooling Error Codes (21xxx)
```python
# DUO carpooling system errors
ERROR_DUPLICATE_DUO_GROUP_NAME = 21001   # Group name already exists
ERROR_DUO_GROUP_NOT_FOUND = 21003       # Group doesn't exist
ERROR_USER_ALREADY_IN_GROUP = 21005     # User already member
ERROR_NO_CREATOR_PERMISSIONS = 21006    # Insufficient group permissions
ERROR_OFFER_NOT_FOUND = 21011           # Ride offer not found
ERROR_ALREADY_PAIRED = 21021            # Already matched with rider
ERROR_OTHER_SIDE_TIME_CONFLICT = 21023  # Schedule conflict detected
```

### Payment Error Codes (23xxx)
```python
# Wallet and payment processing errors
ERROR_CHARGE_FAILED = 23003              # Stripe payment failed
ERROR_CUSTOMER_CREATE_FAILED = 23004     # Stripe customer creation failed
ERROR_POINT_PRODUCT_EXPIRED = 23010      # Points package expired
ERROR_PROMO_CODE_INVALID = 23011         # Invalid promotion code
ERROR_POINT_INSUFFICIENT = 23018         # Insufficient balance
ERROR_EXCEED_COINS_PURCHASE_LIMIT = 23031 # Daily purchase limit exceeded
ERROR_USER_COIN_SUSPENDED = 23032        # Account suspended for coin activity
```

## 🚀 Usage Methods

### Import Error Constants
```python
from applications.portal.models.error_code import (
    ERROR_USER_NOT_FOUND,
    ERROR_POINT_INSUFFICIENT,
    ERROR_INVALID_TOKEN,
    ERROR_CHARGE_FAILED
)
```

### API Error Response Pattern
```python
from gluon.tools import JSONHTTP

def api_endpoint():
    try:
        # Business logic here
        user = get_user(user_id)
        if not user:
            raise JSONHTTP(404, ERROR_USER_NOT_FOUND, 
                          T('User not found', lazy=False))
        
        # Process payment
        result = process_payment(amount)
        if not result.success:
            raise JSONHTTP(402, ERROR_CHARGE_FAILED,
                          T('Payment processing failed', lazy=False))
            
    except InsufficientBalance:
        raise JSONHTTP(402, ERROR_POINT_INSUFFICIENT,
                      T('Insufficient coins in wallet', lazy=False))
```

### Custom Error Handling
```python
def validate_carpooling_request(user_id, group_id):
    """Validate carpooling request with specific error codes"""
    
    # Check if group exists
    group = db.duo_group[group_id]
    if not group:
        return ERROR_DUO_GROUP_NOT_FOUND
    
    # Check if user already in group
    membership = db((db.group_member.user_id == user_id) & 
                   (db.group_member.group_id == group_id)).select().first()
    if membership:
        return ERROR_USER_ALREADY_IN_GROUP
    
    # Check penalty period
    if user_in_penalty_period(user_id):
        return ERROR_IN_THE_PENALTY_PERIOD
    
    return None  # Success
```

### Frontend Error Handling
```javascript
// JavaScript error handling example
function handleApiError(errorCode, message) {
    switch(errorCode) {
        case 20001: // ERROR_USER_NOT_FOUND
            showLoginDialog();
            break;
        case 23018: // ERROR_POINT_INSUFFICIENT  
            showTopUpDialog();
            break;
        case 21021: // ERROR_ALREADY_PAIRED
            showCarpoolStatusDialog();
            break;
        default:
            showGenericErrorDialog(message);
    }
}
```

## 📊 Output Examples

**API Error Response Format**:
```json
{
    "status": "error",
    "error_code": 20001,
    "message": "User not found",
    "details": "The requested user account does not exist in the system"
}
```

**Payment Error Response**:
```json
{
    "status": "error", 
    "error_code": 23003,
    "message": "Payment processing failed",
    "stripe_error": "Your card has insufficient funds"
}
```

**Carpooling Error Response**:
```json
{
    "status": "error",
    "error_code": 21005,
    "message": "User already in group",
    "group_name": "Morning Commute",
    "user_role": "member"
}
```

**Validation Error Response**:
```json
{
    "status": "error",
    "error_code": 10002,
    "message": "Request body validation failed",
    "validation_errors": [
        "email field is required",
        "phone_number format is invalid"
    ]
}
```

## ⚠️ Important Notes

### Error Code Management
- **Uniqueness**: Each error code must be unique across the entire system
- **Categorization**: Follow numeric range conventions for error categories
- **Documentation**: Update this file when adding new error codes
- **Backward Compatibility**: Never change existing error codes in production

### API Integration
- **HTTP Status Codes**: Map error codes to appropriate HTTP status codes
- **Localization**: Error messages should support multiple languages
- **Client Handling**: Frontend applications should handle all defined error codes
- **Monitoring**: Track error code frequency for system health monitoring

### Best Practices
- **Specific Errors**: Use specific error codes rather than generic ones
- **User-Friendly Messages**: Provide clear, actionable error messages
- **Logging**: Log error codes with context for debugging
- **Testing**: Test error scenarios in automated test suites

## 🔗 Related File Links
- **Business Logic**: `/portal/models/common.py` (uses error codes for validation)
- **Database Models**: `/portal/models/db.py` (database constraint errors)
- **Notifications**: `/portal/models/notify.py` (notification delivery errors)
- **API Controllers**: `/portal/controllers/` (API endpoint error handling)
- **Frontend Integration**: Client applications consuming error codes
- **Logging System**: Error tracking and monitoring systems

## 📈 Use Cases
- **API Development**: Consistent error responses across all endpoints
- **Payment Processing**: Specific error handling for financial transactions
- **User Experience**: Clear error messages for user-facing applications
- **System Monitoring**: Error tracking and alerting based on error codes
- **Customer Support**: Rapid issue identification using error codes
- **Third-Party Integration**: Standardized error responses for external consumers
- **Mobile App Development**: Native error handling in iOS/Android apps

## 🛠️ Improvement Suggestions
- **Error Hierarchy**: Create error code inheritance for related errors
- **Internationalization**: Add multilingual error message support
- **Error Analytics**: Implement error code tracking and reporting
- **Auto-Documentation**: Generate API documentation from error codes
- **Validation Framework**: Create automated error code validation
- **Recovery Suggestions**: Add automatic recovery suggestion system

## 🏷️ Document Tags
**Keywords**: error-codes, error-handling, api-errors, payment-errors, user-errors, carpooling-errors, validation-errors, http-status-codes, maas-errors

**Technical Tags**: `#error-handling #api-errors #payment-errors #user-management #carpooling #validation #http-status`

**Target Roles**: API developers (intermediate), Frontend developers (beginner), QA engineers (intermediate), Support staff (beginner)

**Difficulty**: ⭐⭐ (Moderate) - Understanding error categorization and API integration

**Maintenance**: Medium - Regular updates as new features are added

**Business Criticality**: High - Essential for user experience and system reliability

**Related Topics**: API design, Error handling, User experience, Payment processing, System monitoring