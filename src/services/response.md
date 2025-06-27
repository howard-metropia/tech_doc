# TSP API Response Service Documentation

## 🔍 Quick Summary (TL;DR)
The response service provides standardized response formatting for API endpoints, ensuring consistent success and error response structures with internationalization and logging support.

**Keywords:** api-response | response-formatting | error-handling | standardized-responses | i18n-support | api-consistency | logging-integration

**Primary use cases:** Formatting successful API responses, handling error responses with localization, logging failed requests, maintaining consistent API response structure

**Compatibility:** Node.js >= 16.0.0, Koa.js context objects, internationalization support

## ❓ Common Questions Quick Index
- **Q: What response formats are supported?** → Standardized success/fail objects with consistent structure
- **Q: How are errors localized?** → Uses i18n middleware for translating error messages
- **Q: What data is logged on failures?** → User ID, request path, query parameters, and request body
- **Q: Can custom error information be added?** → Yes, via optional information parameter
- **Q: Are responses JSON-ready?** → Yes, returns objects suitable for JSON serialization
- **Q: How are error codes handled?** → Maps error types to numeric codes via error-code definitions

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **response template generator** for the API. Instead of each endpoint creating its own format for success or error messages, this service ensures all API responses look the same - making it easier for mobile apps and websites to understand and process the responses consistently.

**Technical explanation:** 
A response standardization service that provides uniform API response formatting with success/fail patterns. Integrates with internationalization for localized error messages, includes comprehensive request logging for failures, and maintains consistent response structures across all API endpoints.

**Business value explanation:**
Critical for API consistency and developer experience. Reduces integration complexity for client applications, supports international markets through localized error messages, enables effective debugging through comprehensive logging, and ensures professional API standards compliance.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/response.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js context integration
- **Type:** Response Formatting Service
- **File Size:** ~0.8 KB
- **Complexity Score:** ⭐ (Low - Simple formatting with logging)

**Dependencies:**
- `@app/src/static/error-code`: Error code definitions (**Critical**)
- `@maas/core/log`: Logging infrastructure (**High**)

## 📝 Detailed Code Analysis

### success Function

**Purpose:** Creates standardized success response format

**Parameters:**
- `ctx`: Koa context object (not actively used but maintains interface consistency)
- `data`: Any - Data payload to return to client

**Returns:** Object with success result and data

**Implementation:**
```javascript
success: (ctx, data) => {
  return {
    result: 'success',
    data,
  };
}
```

### fail Function

**Purpose:** Creates standardized error response with logging and localization

**Parameters:**
- `ctx`: Koa context object for request information and localization
- `errorType`: String - Error type key for code lookup and translation
- `information`: String (optional) - Additional error context

**Returns:** Object with fail result and detailed error information

**Processing Flow:**
1. **Request Context Extraction:** Captures user ID, path, query, and body
2. **Error Code Lookup:** Maps error type to numeric code
3. **Message Localization:** Translates error message using i18n
4. **Response Assembly:** Creates structured error response
5. **Logging:** Records failure details for debugging

**Implementation:**
```javascript
fail: (ctx, errorType, information = '') => {
  const input = {
    user_id: ctx.request.headers.userid || 0,
    path: ctx.request.path,
    query: ctx.request.query,
    body: ctx.request.body,
  };
  
  const result = {
    result: 'fail',
    error: {
      code: parseInt(ErrorCode[errorType]),
      msg: ctx.res.__(errorType),
      info: information,
    },
  };
  
  logger.warn(
    `[${result.error.code}] ${result.error.msg} ${JSON.stringify(input)}`,
  );
  
  return result;
}
```

## 🚀 Usage Methods

### Basic Success Response
```javascript
const ResponseService = require('@app/src/services/response');

// In a controller endpoint
router.get('/users/:id', async (ctx) => {
  try {
    const user = await getUserById(ctx.params.id);
    
    ctx.body = ResponseService.success(ctx, {
      user: {
        id: user.id,
        name: user.name,
        email: user.email
      }
    });
  } catch (error) {
    ctx.body = ResponseService.fail(ctx, 'ERROR_USER_NOT_FOUND');
  }
});
```

### Error Response with Additional Information
```javascript
const ResponseService = require('@app/src/services/response');

// In a controller with custom error details
router.post('/trip/create', async (ctx) => {
  try {
    const tripData = await validateTripData(ctx.request.body);
    const trip = await createTrip(tripData);
    
    ctx.body = ResponseService.success(ctx, {
      trip: trip,
      message: 'Trip created successfully'
    });
  } catch (error) {
    if (error.code === 'VALIDATION_ERROR') {
      ctx.body = ResponseService.fail(
        ctx, 
        'ERROR_BAD_REQUEST_PARAMS',
        `Validation failed: ${error.details.join(', ')}`
      );
    } else {
      ctx.body = ResponseService.fail(ctx, 'ERROR_INTERNAL_SERVER');
    }
  }
});
```

### Response Wrapper Service
```javascript
class ApiResponseHandler {
  constructor() {
    this.responseService = require('@app/src/services/response');
  }

  handleSuccess(ctx, data, message = null) {
    const responseData = message ? { ...data, message } : data;
    return this.responseService.success(ctx, responseData);
  }

  handleError(ctx, error, customMessage = null) {
    // Map different error types to appropriate response codes
    let errorType;
    let additionalInfo = customMessage || '';

    switch (error.name) {
      case 'ValidationError':
        errorType = 'ERROR_BAD_REQUEST_PARAMS';
        additionalInfo = error.message;
        break;
      case 'NotFoundError':
        errorType = 'ERROR_NOT_FOUND';
        break;
      case 'UnauthorizedError':
        errorType = 'ERROR_UNAUTHORIZED';
        break;
      case 'DatabaseError':
        errorType = 'ERROR_DATABASE_CONNECTION';
        additionalInfo = 'Database operation failed';
        break;
      default:
        errorType = 'ERROR_INTERNAL_SERVER';
        additionalInfo = error.message;
    }

    return this.responseService.fail(ctx, errorType, additionalInfo);
  }

  wrapAsyncHandler(handlerFunction) {
    return async (ctx) => {
      try {
        const result = await handlerFunction(ctx);
        
        if (result && typeof result === 'object') {
          ctx.body = this.handleSuccess(ctx, result);
        } else {
          ctx.body = this.handleSuccess(ctx, { result });
        }
      } catch (error) {
        console.error('Handler error:', error);
        ctx.body = this.handleError(ctx, error);
        ctx.status = this.getHttpStatusFromError(error);
      }
    };
  }

  getHttpStatusFromError(error) {
    const statusMap = {
      'ValidationError': 400,
      'NotFoundError': 404,
      'UnauthorizedError': 401,
      'ForbiddenError': 403,
      'DatabaseError': 500
    };
    return statusMap[error.name] || 500;
  }
}

// Usage in controllers
const responseHandler = new ApiResponseHandler();

router.get('/users/:id', responseHandler.wrapAsyncHandler(async (ctx) => {
  const userId = ctx.params.id;
  const user = await userService.findById(userId);
  
  if (!user) {
    throw new NotFoundError('User not found');
  }
  
  return { user };
}));
```

### Middleware Integration
```javascript
// Middleware to automatically format responses
function responseFormatterMiddleware() {
  const ResponseService = require('@app/src/services/response');
  
  return async (ctx, next) => {
    try {
      await next();
      
      // If body is already set and formatted, don't modify
      if (ctx.body && typeof ctx.body === 'object' && ctx.body.result) {
        return;
      }
      
      // Auto-format successful responses
      if (ctx.body !== undefined) {
        ctx.body = ResponseService.success(ctx, ctx.body);
      }
    } catch (error) {
      console.error('Middleware caught error:', error);
      
      // Determine error type based on status or error properties
      let errorType = 'ERROR_INTERNAL_SERVER';
      
      if (ctx.status === 404 || error.status === 404) {
        errorType = 'ERROR_NOT_FOUND';
      } else if (ctx.status === 401 || error.status === 401) {
        errorType = 'ERROR_UNAUTHORIZED';
      } else if (ctx.status === 400 || error.status === 400) {
        errorType = 'ERROR_BAD_REQUEST_PARAMS';
      }
      
      ctx.body = ResponseService.fail(ctx, errorType, error.message);
      ctx.status = error.status || 500;
    }
  };
}

// Apply middleware to app
app.use(responseFormatterMiddleware());
```

### Testing Utilities
```javascript
const ResponseService = require('@app/src/services/response');

class ResponseTester {
  static createMockContext(overrides = {}) {
    return {
      request: {
        headers: { userid: '123' },
        path: '/test',
        query: {},
        body: {},
        ...overrides.request
      },
      res: {
        __: (key) => key // Mock i18n function
      }
    };
  }

  static testSuccessResponse(data) {
    const ctx = this.createMockContext();
    const response = ResponseService.success(ctx, data);
    
    console.assert(response.result === 'success', 'Should have success result');
    console.assert(response.data === data, 'Should contain provided data');
    
    return response;
  }

  static testFailResponse(errorType, information = '') {
    const ctx = this.createMockContext();
    const response = ResponseService.fail(ctx, errorType, information);
    
    console.assert(response.result === 'fail', 'Should have fail result');
    console.assert(response.error, 'Should contain error object');
    console.assert(response.error.code, 'Should have error code');
    console.assert(response.error.msg, 'Should have error message');
    
    if (information) {
      console.assert(response.error.info === information, 'Should contain additional information');
    }
    
    return response;
  }
}

// Run tests
ResponseTester.testSuccessResponse({ userId: 123, name: 'Test User' });
ResponseTester.testFailResponse('ERROR_NOT_FOUND', 'User does not exist');
```

## 📊 Output Examples

### Successful Response
```json
{
  "result": "success",
  "data": {
    "user": {
      "id": 123,
      "name": "John Doe",
      "email": "john@example.com"
    },
    "timestamp": "2024-06-25T14:30:00Z"
  }
}
```

### Error Response
```json
{
  "result": "fail",
  "error": {
    "code": 404,
    "msg": "User not found",
    "info": "No user exists with ID: 123"
  }
}
```

### Complex Success Response
```json
{
  "result": "success",
  "data": {
    "trips": [
      {
        "id": 1,
        "origin": "Home",
        "destination": "Office",
        "status": "completed"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 25
    },
    "meta": {
      "requestTime": "2024-06-25T14:30:00Z",
      "version": "1.0"
    }
  }
}
```

### Validation Error Response
```json
{
  "result": "fail",
  "error": {
    "code": 400,
    "msg": "Invalid request parameters",
    "info": "Validation failed: email is required, age must be a number"
  }
}
```

## ⚠️ Important Notes

### Response Structure Consistency
- **Success Format:** Always uses `result: 'success'` with `data` property
- **Error Format:** Always uses `result: 'fail'` with detailed `error` object
- **No Variations:** Consistent structure across all endpoints
- **JSON Ready:** Objects can be directly JSON.stringify'd

### Error Code Integration
- **Numeric Codes:** Maps string error types to numeric codes
- **Code Lookup:** Uses ErrorCode static definitions
- **Consistency:** Same error type always returns same code
- **Client Handling:** Clients can rely on consistent error codes

### Internationalization Support
- **i18n Integration:** Uses `ctx.res.__()` for message translation
- **Locale-aware:** Error messages translated based on request locale
- **Fallback:** Error type key used if translation unavailable
- **Multi-language:** Supports multiple client languages

### Logging Behavior
- **Failure Logging:** All failures automatically logged with context
- **Request Context:** Includes user ID, path, query, and body
- **Debug Information:** Comprehensive information for troubleshooting
- **Warning Level:** Uses logger.warn for error responses

### Security Considerations
- **Data Sanitization:** Should sanitize sensitive data before logging
- **Information Disclosure:** Be careful with error information detail
- **User Context:** Safely handles missing user IDs
- **Request Body:** Logs may contain sensitive request data

### Performance Impact
- **Minimal Overhead:** Simple object creation and logging
- **JSON Serialization:** Objects optimized for JSON conversion
- **Memory Usage:** Temporary objects created for responses
- **Logging Cost:** Consider log volume in high-traffic scenarios

## 🔗 Related File Links

- **Error Codes:** `allrepo/connectsmart/tsp-api/src/static/error-code.js`
- **i18n Configuration:** Internationalization setup and message files
- **Controller Examples:** Controllers using this response service
- **Middleware:** Request/response processing middleware

---
*This service provides essential API response standardization for consistent client experience and effective error handling.*