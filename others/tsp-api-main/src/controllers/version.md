# TSP API Version Controller Documentation

## 🔍 Quick Summary (TL;DR)
The version controller provides API version information and debugging utilities, including version retrieval and request echoing for testing and diagnostics.

**Keywords:** api-version | version-info | debugging | echo-service | api-diagnostics | testing-utilities | version-management

**Primary use cases:** Checking API version, debugging request payloads, testing connectivity, API health monitoring, development utilities

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, no external dependencies

## ❓ Common Questions Quick Index
- **Q: How do I check the API version?** → GET `/api/v2/version` endpoint
- **Q: What is the echo endpoint for?** → Testing and debugging request payloads
- **Q: Is authentication required?** → No, both endpoints are public
- **Q: Where does version info come from?** → package.json file in the project root
- **Q: Can I use echo for testing?** → Yes, it returns exactly what you send
- **Q: Is the echo endpoint secure?** → No authentication, use only for development

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as the **API information desk**. The version endpoint tells you exactly which version of the API you're talking to (like asking "what version of the app is this?"), while the echo endpoint is like a mirror that repeats back whatever you say to it - useful for testing if your messages are getting through correctly.

**Technical explanation:** 
A lightweight Koa.js controller that provides essential API metadata and debugging capabilities. The version endpoint serves semantic version information from package.json, while the echo endpoint returns request payloads for testing and debugging purposes.

**Business value explanation:**
Essential for API maintenance, version management, and debugging workflows. Enables proper version tracking for client compatibility, supports development and testing processes, and provides diagnostic capabilities for troubleshooting integration issues.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/version.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** Utility/Diagnostic Controller
- **File Size:** ~0.4 KB
- **Complexity Score:** ⭐ (Very Low - Simple utility endpoints)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing for echo endpoint (**Critical**)
- `@maas/core/response`: Standardized response formatting (**High**)
- `package.json`: Version information source (**Critical**)

## 📝 Detailed Code Analysis

### Version Endpoint (`GET /version`)

**Purpose:** Returns the current API version from package.json

**Implementation:**
```javascript
router.get('version', '/version', async (ctx) => {
  const { version } = require('../../package.json');
  ctx.body = success({ version });
});
```

**Process:**
1. **Package Import:** Dynamically imports package.json from project root
2. **Version Extraction:** Extracts version field from package metadata
3. **Response:** Returns version in standardized success format

### Echo Endpoint (`POST /echo`)

**Purpose:** Returns the exact request body for testing and debugging

**Implementation:**
```javascript
router.post('echo', '/echo', bodyParser(), async (ctx) => {
  console.log(ctx.request.body);
  ctx.body = ctx.request.body;
});
```

**Process:**
1. **Body Parsing:** Parses incoming request body via bodyParser middleware
2. **Logging:** Logs request body to console for debugging
3. **Echo Response:** Returns the exact same body that was received

## 🚀 Usage Methods

### Check API Version
```bash
curl -X GET "https://api.tsp.example.com/api/v2/version"
```

### Test Echo Endpoint
```bash
curl -X POST "https://api.tsp.example.com/api/v2/echo" \
  -H "Content-Type: application/json" \
  -d '{
    "test": "Hello, world!",
    "timestamp": "2024-06-25T14:30:00Z",
    "data": {
      "key": "value",
      "number": 42
    }
  }'
```

### JavaScript Client Examples
```javascript
// Check API version
async function getApiVersion() {
  try {
    const response = await fetch('/api/v2/version');
    const result = await response.json();
    
    if (result.result === 'success') {
      console.log('API Version:', result.data.version);
      return result.data.version;
    }
  } catch (error) {
    console.error('Failed to get version:', error);
  }
}

// Test echo endpoint
async function testEcho(payload) {
  try {
    const response = await fetch('/api/v2/echo', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });
    
    const echoed = await response.json();
    
    console.log('Original:', payload);
    console.log('Echoed:', echoed);
    
    // Verify echo worked correctly
    const isMatch = JSON.stringify(payload) === JSON.stringify(echoed);
    console.log('Echo test passed:', isMatch);
    
    return echoed;
  } catch (error) {
    console.error('Echo test failed:', error);
  }
}

// Usage examples
getApiVersion();

testEcho({
  message: "Testing connectivity",
  client: "web-app",
  timestamp: new Date().toISOString()
});
```

### Development Testing Script
```javascript
// Comprehensive API testing utility
class ApiTester {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
  }

  async checkVersion() {
    console.log('🔍 Checking API version...');
    const version = await this.getApiVersion();
    console.log(`✅ API Version: ${version}`);
    return version;
  }

  async testConnectivity() {
    console.log('🔗 Testing connectivity...');
    const testPayload = {
      test_id: Math.random().toString(36).substr(2, 9),
      timestamp: new Date().toISOString(),
      client_info: {
        user_agent: navigator.userAgent,
        platform: navigator.platform
      }
    };

    const echoed = await this.testEcho(testPayload);
    const isValid = JSON.stringify(testPayload) === JSON.stringify(echoed);
    
    console.log(isValid ? '✅ Connectivity test passed' : '❌ Connectivity test failed');
    return isValid;
  }

  async getApiVersion() {
    const response = await fetch(`${this.baseUrl}/api/v2/version`);
    const result = await response.json();
    return result.data.version;
  }

  async testEcho(payload) {
    const response = await fetch(`${this.baseUrl}/api/v2/echo`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return await response.json();
  }

  async runAllTests() {
    console.log('🚀 Starting API tests...');
    await this.checkVersion();
    await this.testConnectivity();
    console.log('✨ All tests completed');
  }
}

// Usage
const tester = new ApiTester('https://api.tsp.example.com');
tester.runAllTests();
```

## 📊 Output Examples

### Version Response
```json
{
  "result": "success",
  "data": {
    "version": "2.1.4"
  }
}
```

### Echo Response Examples

**Simple Echo:**
```json
// Request
{
  "message": "Hello, world!"
}

// Response (identical)
{
  "message": "Hello, world!"
}
```

**Complex Object Echo:**
```json
// Request
{
  "user": {
    "id": 12345,
    "name": "John Doe",
    "preferences": {
      "language": "en",
      "timezone": "America/New_York"
    }
  },
  "metadata": {
    "client": "mobile-app",
    "version": "1.2.3",
    "timestamp": "2024-06-25T14:30:00Z"
  },
  "test_data": [1, 2, 3, "test", true, null]
}

// Response (identical)
{
  "user": {
    "id": 12345,
    "name": "John Doe",
    "preferences": {
      "language": "en",
      "timezone": "America/New_York"
    }
  },
  "metadata": {
    "client": "mobile-app",
    "version": "1.2.3",
    "timestamp": "2024-06-25T14:30:00Z"
  },
  "test_data": [1, 2, 3, "test", true, null]
}
```

## ⚠️ Important Notes

### Security Considerations
- **No Authentication:** Both endpoints are publicly accessible
- **Data Exposure:** Echo endpoint logs request data to console
- **Production Use:** Echo endpoint should be disabled or restricted in production
- **Input Validation:** No validation on echo requests - accepts any JSON

### Version Management
- **Semantic Versioning:** Follows semver format (MAJOR.MINOR.PATCH)
- **Package.json Source:** Version comes from project's package.json
- **Build Integration:** Version automatically updated during deployment
- **Client Compatibility:** Clients can check version for feature compatibility

### Echo Endpoint Uses
- **Payload Testing:** Verify request body formatting
- **Network Debugging:** Test connectivity and data transmission
- **Integration Testing:** Validate client-server communication
- **Development:** Debug request serialization issues

### Logging Behavior
- **Console Output:** Echo requests logged to console
- **Data Visibility:** All echoed data visible in server logs
- **Privacy Impact:** Sensitive data should not be sent to echo
- **Debug Information:** Useful for troubleshooting request issues

### Performance Considerations
- **Lightweight:** Minimal processing overhead
- **No Database:** No external dependencies or database calls
- **Fast Response:** Near-instant response times
- **Memory Usage:** Request data temporarily held in memory

### Development Workflow Integration
- **Health Checks:** Version endpoint for monitoring
- **CI/CD Integration:** Version checking in automated tests
- **Client Updates:** Version-based feature flagging
- **Debugging:** Echo for payload troubleshooting

### Production Recommendations
- **Rate Limiting:** Consider rate limits on echo endpoint
- **Access Control:** Restrict echo to development environments
- **Monitoring:** Track version endpoint usage
- **Logging:** Implement structured logging for echo requests

## 🔗 Related File Links

- **Package.json:** `allrepo/connectsmart/tsp-api/package.json` (version source)
- **Response Service:** `@maas/core/response` (response formatting)
- **Router Configuration:** Main routing configuration files

---
*This controller provides essential API version information and debugging utilities for development and maintenance workflows.*