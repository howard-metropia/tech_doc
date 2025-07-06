# TSP Job Service - Version Controller

## Overview

The `src/controllers/version.js` file implements a simple version endpoint controller for the TSP Job service. This controller provides version information about the currently running application instance, which is essential for deployment verification, debugging, and system monitoring.

## File Information

- **File Path**: `/src/controllers/version.js`
- **File Type**: JavaScript Controller Module
- **Primary Purpose**: Application version endpoint implementation
- **Dependencies**: @koa/router, @maas/core/log, @maas/core/response, package.json

## Implementation Details

### Dependencies
```javascript
const Router = require('@koa/router');
const { logger } = require('@maas/core/log');
const { success } = require('@maas/core/response');
```

**Dependency Analysis**:
- **@koa/router**: Koa.js routing middleware for HTTP endpoint handling
- **@maas/core/log**: Centralized logging system from MaaS core library
- **@maas/core/response**: Standardized response formatting utilities

### Router Initialization
```javascript
const router = new Router({});
```

**Purpose**: Creates a new Koa router instance for version-related endpoints

### Version Endpoint Implementation
```javascript
router.get('version', '/version', async (ctx) => {
  const { version } = require('../../package.json');
  logger.info('version router test');
  ctx.body = success({ version });
});
```

## Endpoint Specification

### GET /version

**Purpose**: Returns the current application version information

**Request Method**: GET
**Endpoint Path**: `/version`
**Route Name**: `version`

**Request Parameters**: None

**Response Format**:
```javascript
{
  "success": true,
  "data": {
    "version": "1.0.0"
  },
  "message": null,
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**Response Fields**:
- `success`: Boolean indicating request success
- `data.version`: Current application version from package.json
- `message`: Optional message field (null for successful requests)
- `timestamp`: Response generation timestamp

## Implementation Flow

### 1. Version Retrieval
```javascript
const { version } = require('../../package.json');
```

**Process**:
- Dynamically loads the package.json file
- Extracts the version field
- Provides real-time version information

### 2. Logging
```javascript
logger.info('version router test');
```

**Purpose**:
- Logs version endpoint access for monitoring
- Helps track API usage and debugging
- Provides audit trail for version checks

### 3. Response Formatting
```javascript
ctx.body = success({ version });
```

**Process**:
- Uses standardized success response format
- Wraps version data in consistent response structure
- Ensures compatibility with client applications

## Use Cases

### 1. Deployment Verification
```bash
# Verify deployment version
curl -X GET http://localhost:8888/version

# Expected response
{
  "success": true,
  "data": {
    "version": "2.1.0"
  },
  "message": null,
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### 2. Health Check Integration
```javascript
// Health check that includes version
async function healthCheck() {
  const response = await fetch('/version');
  const data = await response.json();
  
  return {
    status: 'healthy',
    version: data.data.version,
    timestamp: new Date().toISOString()
  };
}
```

### 3. Client Compatibility Checking
```javascript
// Client-side version compatibility
async function checkCompatibility() {
  const response = await fetch('/version');
  const { data } = await response.json();
  
  const serverVersion = data.version;
  const clientVersion = '2.0.0';
  
  if (!isCompatible(serverVersion, clientVersion)) {
    throw new Error('Client version incompatible with server');
  }
}
```

## Enhanced Version Controller

### Extended Version Information
```javascript
// Enhanced version endpoint (potential improvement)
router.get('version', '/version', async (ctx) => {
  const packageInfo = require('../../package.json');
  const startTime = process.env.START_TIME || new Date().toISOString();
  
  const versionInfo = {
    version: packageInfo.version,
    name: packageInfo.name,
    description: packageInfo.description,
    node: process.version,
    platform: process.platform,
    uptime: process.uptime(),
    startTime: startTime,
    environment: process.env.NODE_ENV || 'development',
    commit: process.env.GIT_COMMIT || 'unknown',
    buildDate: process.env.BUILD_DATE || 'unknown'
  };
  
  logger.info('Version information requested', { version: versionInfo.version });
  ctx.body = success(versionInfo);
});
```

### Version Comparison Endpoint
```javascript
// Version comparison functionality
router.post('version/compare', '/version/compare', async (ctx) => {
  const { clientVersion } = ctx.request.body;
  const serverVersion = require('../../package.json').version;
  
  const comparison = {
    server: serverVersion,
    client: clientVersion,
    compatible: isVersionCompatible(serverVersion, clientVersion),
    updateRequired: isUpdateRequired(serverVersion, clientVersion)
  };
  
  ctx.body = success(comparison);
});
```

## Integration with Application

### Mounting the Router
```javascript
// In main application file
const versionRouter = require('./controllers/version');
app.use(versionRouter.routes());
app.use(versionRouter.allowedMethods());
```

### Middleware Integration
```javascript
// Version middleware for all requests
app.use(async (ctx, next) => {
  ctx.state.appVersion = require('./package.json').version;
  await next();
});
```

## Testing

### Unit Tests
```javascript
// Test version endpoint
describe('Version Controller', () => {
  it('should return version information', async () => {
    const response = await request(app)
      .get('/version')
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.version).toBeDefined();
    expect(typeof response.body.data.version).toBe('string');
  });
  
  it('should log version request', async () => {
    const logSpy = jest.spyOn(logger, 'info');
    
    await request(app).get('/version');
    
    expect(logSpy).toHaveBeenCalledWith('version router test');
  });
});
```

### Integration Tests
```javascript
// Integration test with real server
describe('Version Endpoint Integration', () => {
  it('should be accessible without authentication', async () => {
    const response = await fetch(`${baseUrl}/version`);
    expect(response.status).toBe(200);
    
    const data = await response.json();
    expect(data.success).toBe(true);
    expect(data.data.version).toMatch(/^\d+\.\d+\.\d+/);
  });
});
```

## Monitoring and Analytics

### Version Access Metrics
```javascript
// Enhanced logging with metrics
router.get('version', '/version', async (ctx) => {
  const { version } = require('../../package.json');
  
  // Track version endpoint access
  metrics.versionRequests.inc({
    version: version,
    userAgent: ctx.get('user-agent'),
    ip: ctx.ip
  });
  
  logger.info('Version requested', {
    version: version,
    timestamp: new Date().toISOString(),
    userAgent: ctx.get('user-agent'),
    ip: ctx.ip
  });
  
  ctx.body = success({ version });
});
```

### Performance Monitoring
```javascript
// Response time monitoring
const responseTimeHistogram = new prometheus.Histogram({
  name: 'version_endpoint_response_time',
  help: 'Version endpoint response time',
  buckets: [0.1, 0.5, 1, 2, 5]
});

router.get('version', '/version', async (ctx) => {
  const timer = responseTimeHistogram.startTimer();
  
  try {
    const { version } = require('../../package.json');
    logger.info('version router test');
    ctx.body = success({ version });
  } finally {
    timer();
  }
});
```

## Security Considerations

### Rate Limiting
```javascript
// Rate limiting for version endpoint
const rateLimit = require('koa-ratelimit');

const versionRateLimit = rateLimit({
  driver: 'memory',
  db: new Map(),
  duration: 60000, // 1 minute
  errorMessage: 'Too many version requests',
  id: (ctx) => ctx.ip,
  headers: {
    remaining: 'Rate-Limit-Remaining',
    reset: 'Rate-Limit-Reset',
    total: 'Rate-Limit-Total'
  },
  max: 10 // 10 requests per minute
});

router.get('version', '/version', versionRateLimit, async (ctx) => {
  // ... version logic
});
```

### Information Disclosure
```javascript
// Sanitized version information for production
router.get('version', '/version', async (ctx) => {
  const { version } = require('../../package.json');
  
  // In production, limit exposed information
  const versionInfo = process.env.NODE_ENV === 'production' 
    ? { version } 
    : {
        version,
        environment: process.env.NODE_ENV,
        uptime: process.uptime()
      };
  
  logger.info('version router test');
  ctx.body = success(versionInfo);
});
```

## Error Handling

### Robust Error Handling
```javascript
router.get('version', '/version', async (ctx) => {
  try {
    const { version } = require('../../package.json');
    
    if (!version) {
      throw new Error('Version information not available');
    }
    
    logger.info('version router test');
    ctx.body = success({ version });
  } catch (error) {
    logger.error('Version endpoint error:', error);
    ctx.body = error({
      message: 'Unable to retrieve version information',
      code: 'VERSION_ERROR'
    });
    ctx.status = 500;
  }
});
```

## Module Export

```javascript
module.exports = router;
```

**Purpose**: Exports the configured router for integration with the main application

This version controller provides a simple but essential service for the TSP Job application, enabling version tracking, deployment verification, and system monitoring capabilities. The implementation follows Koa.js best practices and integrates seamlessly with the MaaS framework's logging and response formatting systems.