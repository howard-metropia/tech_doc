# Error Code Definitions

## Overview
**File**: `src/static/error-code.js`  
**Type**: Error Code Constants Module  
**Purpose**: Central repository for standardized error codes used throughout the TSP job system for consistent error handling and reporting

## Core Functionality

### Standardized Error Management
This module provides a comprehensive set of predefined error codes that enable consistent error handling, debugging, and monitoring across the entire TSP (Transportation Service Provider) system.

### Error Code Organization
Error codes are organized by functional domain using numeric prefixes to categorize different types of errors, making it easy to identify the source and nature of issues.

## Error Code Categories

### Request Validation Errors (10xxx)
**Range**: 10001-10999  
**Purpose**: Client request validation and parameter errors

```javascript
ERROR_BAD_REQUEST_PARAMS: 10001,
ERROR_BAD_REQUEST_BODY: 10002,
```

**Usage Context**:
- **10001**: Invalid or missing request parameters
- **10002**: Malformed or invalid request body content

**Common Scenarios**:
```javascript
// Parameter validation failure
if (!userId || !isValidId(userId)) {
  throw new Error(ERROR_BAD_REQUEST_PARAMS);
}

// Request body validation
if (!validateRequestBody(body)) {
  throw new Error(ERROR_BAD_REQUEST_BODY);
}
```

### User Management Errors (20xxx)
**Range**: 20001-20999  
**Purpose**: User-related operations and authentication errors

```javascript
ERROR_USER_NOT_FOUND: 20001,
ERROR_ENTERPRISE_EMAIL_DUPLICATE: 20020,
ERROR_NOT_FOUND: 20022,
```

**Error Definitions**:
- **20001**: User does not exist in the system
- **20020**: Enterprise email address already registered
- **20022**: Generic resource not found error

**Integration Examples**:
```javascript
// User lookup failure
const user = await User.findById(userId);
if (!user) {
  throw new ApplicationError(ERROR_USER_NOT_FOUND, 'User not found');
}

// Enterprise email validation
const existingUser = await User.findByEmail(email);
if (existingUser) {
  throw new ApplicationError(ERROR_ENTERPRISE_EMAIL_DUPLICATE, 'Email already registered');
}
```

### DUO Carpooling Errors (21xxx)
**Range**: 21001-21999  
**Purpose**: DUO carpooling system specific errors

```javascript
ERROR_DUPLICATE_DUO_GROUP_NAME: 21001,
ERROR_DUO_GROUP_TYPE_INVALID: 21002,
ERROR_DUO_GROUP_NOT_FOUND: 21003,
ERROR_USER_ALREADY_IN_GROUP: 21005,
ERROR_NO_CREATOR_PERMISSIONS: 21006,
ERROR_REQUEST_JOIN_GROUP_NOT_FOUND: 21008,
ERROR_ALREADY_REQUEST_JOIN_GROUP: 21009,
ERROR_NOT_GROUP_MEMBER: 21016,
```

**Carpool Group Management**:
- **21001**: Group name already exists in system
- **21002**: Invalid group type specified
- **21003**: Requested group does not exist
- **21005**: User is already a member of the group
- **21006**: User lacks creator/admin permissions
- **21008**: Join request not found
- **21009**: User has already requested to join
- **21016**: User is not a member of the group

**Business Logic Integration**:
```javascript
// Group creation validation
const existingGroup = await DuoGroup.findByName(groupName);
if (existingGroup) {
  throw new ApplicationError(ERROR_DUPLICATE_DUO_GROUP_NAME);
}

// Permission validation
if (!user.hasCreatorPermissions(groupId)) {
  throw new ApplicationError(ERROR_NO_CREATOR_PERMISSIONS);
}

// Membership validation
const membership = await GroupMember.findByUserAndGroup(userId, groupId);
if (!membership) {
  throw new ApplicationError(ERROR_NOT_GROUP_MEMBER);
}
```

### Wallet and Payment Errors (23xxx)
**Range**: 23001-23999  
**Purpose**: Financial transaction and wallet operation errors

```javascript
ERROR_POINT_INSUFFICIENT: 23018,
```

**Financial Validation**:
- **23018**: Insufficient points/credits for transaction

**Usage Example**:
```javascript
// Wallet balance validation
const userWallet = await Wallet.findByUserId(userId);
if (userWallet.balance < transactionAmount) {
  throw new ApplicationError(ERROR_POINT_INSUFFICIENT, 'Insufficient wallet balance');
}
```

### Route and Navigation Errors (24xxx)
**Range**: 24001-24999  
**Purpose**: Route calculation and navigation service errors

```javascript
ERROR_TOLLS_ROUTE_INVAILD_HERE_POLYLINE: 24001,
ERROR_TOLLGURU_RESPONSE_SCHEMA: 24002,
ERROR_GOOGLE_PHOTO_REFERENCE: 24101,
```

**Navigation Service Errors**:
- **24001**: Invalid HERE Maps polyline format
- **24002**: TollGuru API response schema validation failure
- **24101**: Invalid Google Places photo reference

**Service Integration Examples**:
```javascript
// HERE Maps polyline validation
if (!isValidHerePolyline(polyline)) {
  throw new ApplicationError(ERROR_TOLLS_ROUTE_INVAILD_HERE_POLYLINE);
}

// TollGuru response validation
const tollData = await tollGuruAPI.calculateTolls(route);
if (!validateTollGuruResponse(tollData)) {
  throw new ApplicationError(ERROR_TOLLGURU_RESPONSE_SCHEMA);
}

// Google Places photo validation
if (!isValidPhotoReference(photoRef)) {
  throw new ApplicationError(ERROR_GOOGLE_PHOTO_REFERENCE);
}
```

### Third-Party System Errors (40xxx)
**Range**: 40001-40999  
**Purpose**: External service integration and third-party system errors

```javascript
ERROR_THIRD_PARTY_FAILED: 40000,
ERROR_TRANSIT_TICKET_TRANSACTION: 40014,
ERROR_TRANSIT_TICKET_PAYMENT: 40015,
ERROR_TRANSIT_TICKET_SYSTEM: 40016,
ERROR_BYTEMARK_PASS_DATA: 40017,
```

**External Service Categories**:
- **40000**: General third-party service failure
- **40014**: Transit ticket transaction failure
- **40015**: Transit ticket payment processing error
- **40016**: Transit ticketing system unavailable
- **40017**: Bytemark pass data validation error

**Third-Party Integration Patterns**:
```javascript
// Generic third-party error handling
try {
  const result = await externalAPI.makeRequest(params);
  return result;
} catch (error) {
  logger.error('Third-party service failed:', error);
  throw new ApplicationError(ERROR_THIRD_PARTY_FAILED, error.message);
}

// Transit ticket specific errors
try {
  const ticket = await transitAPI.purchaseTicket(ticketData);
  return ticket;
} catch (error) {
  if (error.type === 'payment_failed') {
    throw new ApplicationError(ERROR_TRANSIT_TICKET_PAYMENT);
  } else if (error.type === 'system_unavailable') {
    throw new ApplicationError(ERROR_TRANSIT_TICKET_SYSTEM);
  } else {
    throw new ApplicationError(ERROR_TRANSIT_TICKET_TRANSACTION);
  }
}

// Bytemark integration
const passData = await bytemarkAPI.getPassData(passId);
if (!validateBytemarkPassData(passData)) {
  throw new ApplicationError(ERROR_BYTEMARK_PASS_DATA);
}
```

## Error Code Structure and Design

### Numbering Convention
```javascript
// Error code format: XYZNN
// X: Major category (1=client, 2=user, 3=business, 4=external)
// Y: Subcategory within major category
// Z: Specific error type
// NN: Sequential number within type
```

### Category Mapping
- **1xxxx**: Client and request errors
- **2xxxx**: User and authentication errors
- **3xxxx**: Business logic and validation errors
- **4xxxx**: External system and integration errors

## Usage Patterns and Integration

### Error Handling Middleware
```javascript
const errorCodes = require('@app/src/static/error-code');

const errorHandler = (error, req, res, next) => {
  const errorCode = error.code || errorCodes.ERROR_THIRD_PARTY_FAILED;
  
  res.status(getHttpStatusFromErrorCode(errorCode)).json({
    error: {
      code: errorCode,
      message: error.message,
      timestamp: new Date().toISOString(),
    },
  });
};
```

### Service Layer Integration
```javascript
const { ERROR_USER_NOT_FOUND, ERROR_POINT_INSUFFICIENT } = require('@app/src/static/error-code');

class UserService {
  async transferPoints(fromUserId, toUserId, amount) {
    const fromUser = await User.findById(fromUserId);
    if (!fromUser) {
      throw new ServiceError(ERROR_USER_NOT_FOUND, 'Source user not found');
    }
    
    const wallet = await Wallet.findByUserId(fromUserId);
    if (wallet.balance < amount) {
      throw new ServiceError(ERROR_POINT_INSUFFICIENT, 'Insufficient balance');
    }
    
    // Process transfer
  }
}
```

### API Response Standardization
```javascript
// Success response
{
  success: true,
  data: responseData,
}

// Error response with error code
{
  success: false,
  error: {
    code: 21001,
    message: "Duplicate DUO group name",
    details: "A group with this name already exists"
  }
}
```

## Error Monitoring and Analytics

### Logging Integration
```javascript
const { logger } = require('@maas/core/log');

const logError = (errorCode, context, error) => {
  logger.error('Application error occurred', {
    errorCode,
    context,
    error: error.message,
    stack: error.stack,
    timestamp: new Date().toISOString(),
  });
};

// Usage
try {
  await someOperation();
} catch (error) {
  logError(ERROR_DUO_GROUP_NOT_FOUND, { userId, groupId }, error);
  throw error;
}
```

### Metrics Collection
```javascript
// Error metrics for monitoring
const errorMetrics = {
  [ERROR_USER_NOT_FOUND]: 0,
  [ERROR_POINT_INSUFFICIENT]: 0,
  [ERROR_THIRD_PARTY_FAILED]: 0,
};

const incrementErrorMetric = (errorCode) => {
  if (errorCode in errorMetrics) {
    errorMetrics[errorCode]++;
  }
};
```

## Error Recovery and Retry Logic

### Retry Patterns
```javascript
const retryableErrors = [
  ERROR_THIRD_PARTY_FAILED,
  ERROR_TRANSIT_TICKET_SYSTEM,
];

const isRetryableError = (errorCode) => {
  return retryableErrors.includes(errorCode);
};

const retryOperation = async (operation, maxRetries = 3) => {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error) {
      if (attempt === maxRetries || !isRetryableError(error.code)) {
        throw error;
      }
      
      await delay(attempt * 1000); // Exponential backoff
    }
  }
};
```

### Circuit Breaker Integration
```javascript
const circuitBreakerErrors = [
  ERROR_THIRD_PARTY_FAILED,
  ERROR_TRANSIT_TICKET_SYSTEM,
  ERROR_BYTEMARK_PASS_DATA,
];

const shouldTriggerCircuitBreaker = (errorCode) => {
  return circuitBreakerErrors.includes(errorCode);
};
```

## Internationalization Support

### Error Message Mapping
```javascript
const errorMessages = {
  [ERROR_USER_NOT_FOUND]: {
    en: 'User not found',
    es: 'Usuario no encontrado',
    vi: 'Không tìm thấy người dùng',
  },
  [ERROR_POINT_INSUFFICIENT]: {
    en: 'Insufficient points',
    es: 'Puntos insuficientes',
    vi: 'Không đủ điểm',
  },
};

const getLocalizedErrorMessage = (errorCode, locale = 'en') => {
  return errorMessages[errorCode]?.[locale] || 'Unknown error';
};
```

## Testing and Validation

### Unit Test Examples
```javascript
describe('Error Code Constants', () => {
  test('should have unique error codes', () => {
    const errorCodes = require('./error-code');
    const values = Object.values(errorCodes);
    const uniqueValues = new Set(values);
    
    expect(values.length).toBe(uniqueValues.size);
  });
  
  test('should follow numbering convention', () => {
    const errorCodes = require('./error-code');
    
    Object.values(errorCodes).forEach(code => {
      expect(code).toBeGreaterThan(10000);
      expect(code).toBeLessThan(50000);
    });
  });
});
```

### Integration Testing
```javascript
describe('Error Handling Integration', () => {
  test('should handle user not found error', async () => {
    const response = await request(app)
      .get('/api/users/999999')
      .expect(404);
    
    expect(response.body.error.code).toBe(ERROR_USER_NOT_FOUND);
  });
});
```

## Best Practices

### Error Code Management
- **Consistency**: Use error codes consistently across all services
- **Documentation**: Document each error code's purpose and usage
- **Versioning**: Avoid changing existing error codes, add new ones instead
- **Categorization**: Use the numbering scheme to categorize errors logically

### Implementation Guidelines
- **Specific Errors**: Use specific error codes rather than generic ones
- **Context**: Provide meaningful error messages with context
- **Logging**: Always log errors with sufficient detail for debugging
- **User Experience**: Map technical errors to user-friendly messages

### Monitoring and Alerting
- **Error Rates**: Monitor error frequency by code
- **Patterns**: Identify error patterns and trends
- **Alerting**: Set up alerts for critical error thresholds
- **Resolution**: Track error resolution times and patterns

## Security Considerations

### Error Information Disclosure
- **Sensitive Data**: Avoid exposing sensitive information in error messages
- **Internal Details**: Don't leak internal system details to clients
- **Stack Traces**: Filter stack traces in production environments
- **Audit Trail**: Log security-related errors for audit purposes

### Error Rate Limiting
```javascript
// Prevent abuse through error monitoring
const errorRateLimiter = {
  [ERROR_BAD_REQUEST_PARAMS]: { limit: 10, window: '1m' },
  [ERROR_USER_NOT_FOUND]: { limit: 20, window: '5m' },
};
```

This comprehensive error code system provides the foundation for robust error handling, monitoring, and debugging across the entire TSP job scheduling and mobility platform, enabling consistent error management and improved system reliability.