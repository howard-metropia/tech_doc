# Middlewares Configuration

## Overview
**File**: `src/middlewares.js`  
**Type**: Middleware Configuration Module  
**Purpose**: Central configuration for middleware chains used in TSP job scheduling system

## Core Functionality

### Middleware Chain Management
This module serves as the central registry for organizing and configuring middleware chains that are applied to different types of job executions within the TSP (Transportation Service Provider) system.

### Architecture Design
The configuration follows a modular approach where different execution contexts (schedule vs run) can have their own specific middleware chains, allowing for flexible and context-appropriate middleware application.

## Module Structure

### Dependencies
```javascript
const jobMeasure = require('@app/src/middlewares/job-measure');
```

### Export Configuration
```javascript
module.exports = {
  schedule: [
    jobMeasure,
  ],
  run: [
  ],
};
```

## Middleware Chains

### Schedule Chain
**Purpose**: Applied to all scheduled job executions
**Current Middleware**:
- `jobMeasure`: Performance monitoring and execution tracking

**Usage Context**: 
- Cron-based scheduled jobs
- Time-triggered job executions  
- Periodic maintenance tasks
- Automated system processes

### Run Chain
**Purpose**: Applied to manual job executions or one-time runs
**Current Middleware**: None configured (empty array)

**Usage Context**:
- Manual job triggers
- Administrative commands
- One-time execution tasks
- Development/debugging runs

## Implementation Details

### Module Structure Analysis
```javascript
// Explicit module export with dual assignment
module.exports = module.exports = {
  schedule: [jobMeasure],
  run: [],
};
```

**Note**: The double assignment `module.exports = module.exports = {}` appears to be a redundant pattern that could be simplified to a single assignment.

### Middleware Loading
The module uses relative path imports with alias resolution:
```javascript
const jobMeasure = require('@app/src/middlewares/job-measure');
```

**Path Resolution**: `@app` alias points to the application root directory

## Middleware Integration

### Job Measure Middleware
**Type**: Performance Monitoring  
**Function**: Tracks job execution lifecycle with InfluxDB metrics
**Applied To**: Schedule chain only

**Capabilities**:
- Unique job ID generation
- Start/end/failure status tracking
- InfluxDB time-series data collection
- Error-resilient logging
- Resource cleanup management

### Chain Execution Order
For scheduled jobs, the middleware execution follows:
1. **jobMeasure**: Generates job ID and logs start status
2. **Job Logic**: Actual job implementation executes
3. **jobMeasure**: Logs completion status and cleans up resources

## Configuration Patterns

### Middleware Registration
```javascript
// Pattern for adding new middleware
const newMiddleware = require('./path/to/middleware');

module.exports = {
  schedule: [
    jobMeasure,        // Existing middleware
    newMiddleware,     // New middleware added to chain
  ],
  run: [
    // Run-specific middleware would go here
  ],
};
```

### Context-Specific Configuration
The separation of `schedule` and `run` chains allows for:
- **Different monitoring needs** between scheduled and manual executions
- **Separate authentication/authorization** for different execution types
- **Distinct logging/auditing** requirements
- **Performance optimization** for specific use cases

## Usage in Job System

### Scheduler Integration
```javascript
// How the scheduler would use these middleware chains
const middlewares = require('./middlewares');

// For scheduled jobs
const scheduleMiddlewares = middlewares.schedule;
scheduleMiddlewares.forEach(middleware => {
  // Apply middleware to job execution context
});

// For manual runs
const runMiddlewares = middlewares.run;
runMiddlewares.forEach(middleware => {
  // Apply middleware to manual execution context
});
```

### Job Execution Flow
1. **Job Trigger**: Scheduled or manual execution initiated
2. **Middleware Selection**: Choose appropriate chain (schedule/run)
3. **Chain Execution**: Apply middlewares in order
4. **Job Logic**: Execute actual job implementation
5. **Cleanup**: Middleware cleanup and finalization

## Extension Points

### Adding New Middleware
```javascript
// Example: Adding authentication middleware
const authMiddleware = require('@app/src/middlewares/auth');
const rateLimitMiddleware = require('@app/src/middlewares/rate-limit');

module.exports = {
  schedule: [
    authMiddleware,      // Authentication first
    rateLimitMiddleware, // Rate limiting second
    jobMeasure,         // Performance monitoring third
  ],
  run: [
    authMiddleware,     // Auth for manual runs
    // Different middleware chain for manual executions
  ],
};
```

### Conditional Middleware
```javascript
// Example: Environment-specific middleware
const debugMiddleware = require('@app/src/middlewares/debug');

const middlewareChains = {
  schedule: [jobMeasure],
  run: [],
};

// Add debug middleware in development
if (process.env.NODE_ENV === 'development') {
  middlewareChains.schedule.push(debugMiddleware);
  middlewareChains.run.push(debugMiddleware);
}

module.exports = middlewareChains;
```

## Performance Considerations

### Middleware Overhead
- **Schedule Chain**: Currently minimal overhead with single middleware
- **Run Chain**: No overhead (empty chain)
- **Execution Order**: Middleware executed sequentially

### Optimization Strategies
```javascript
// Lazy loading for performance
const getScheduleMiddlewares = () => {
  return [
    require('@app/src/middlewares/job-measure'),
    // Other middlewares loaded on demand
  ];
};
```

## Configuration Management

### Environment-Based Configuration
```javascript
// Example: Environment-specific middleware configuration
const baseMiddlewares = {
  schedule: [jobMeasure],
  run: [],
};

if (process.env.MONITORING_ENABLED === 'true') {
  const monitoringMiddleware = require('@app/src/middlewares/monitoring');
  baseMiddlewares.schedule.push(monitoringMiddleware);
}

module.exports = baseMiddlewares;
```

### Feature Flags
```javascript
// Example: Feature flag controlled middleware
const featureFlags = require('@app/config/features');

const middlewares = {
  schedule: [jobMeasure],
  run: [],
};

if (featureFlags.ADVANCED_MONITORING) {
  middlewares.schedule.push(require('@app/src/middlewares/advanced-monitor'));
}

module.exports = middlewares;
```

## Error Handling

### Middleware Chain Resilience
Each middleware should handle its own errors gracefully to prevent breaking the entire chain:

```javascript
// Example middleware error handling pattern
const resilientMiddleware = async (ctx, next) => {
  try {
    // Middleware logic
    await next();
  } catch (error) {
    // Log error but don't break chain
    logger.error('Middleware error:', error);
    throw error; // Re-throw for job failure handling
  }
};
```

### Chain Validation
```javascript
// Example: Validate middleware chain configuration
const validateMiddlewares = (chains) => {
  Object.keys(chains).forEach(chainName => {
    const chain = chains[chainName];
    if (!Array.isArray(chain)) {
      throw new Error(`Middleware chain '${chainName}' must be an array`);
    }
    
    chain.forEach((middleware, index) => {
      if (typeof middleware !== 'function') {
        throw new Error(`Middleware at index ${index} in chain '${chainName}' is not a function`);
      }
    });
  });
};
```

## Testing Considerations

### Unit Testing
```javascript
// Example test for middleware configuration
describe('Middlewares Configuration', () => {
  test('should export schedule and run chains', () => {
    const middlewares = require('./middlewares');
    
    expect(middlewares).toHaveProperty('schedule');
    expect(middlewares).toHaveProperty('run');
    expect(Array.isArray(middlewares.schedule)).toBe(true);
    expect(Array.isArray(middlewares.run)).toBe(true);
  });
  
  test('should include jobMeasure in schedule chain', () => {
    const middlewares = require('./middlewares');
    const jobMeasure = require('@app/src/middlewares/job-measure');
    
    expect(middlewares.schedule).toContain(jobMeasure);
  });
});
```

### Integration Testing
```javascript
// Example integration test
describe('Middleware Chain Integration', () => {
  test('should execute schedule middleware chain', async () => {
    const middlewares = require('./middlewares');
    const mockContext = { name: 'test-job' };
    
    // Mock middleware execution
    for (const middleware of middlewares.schedule) {
      await middleware(mockContext, () => Promise.resolve());
    }
    
    // Verify middleware effects
    expect(mockContext).toHaveProperty('jobId');
  });
});
```

## Best Practices

### Configuration Organization
- **Separation of Concerns**: Keep schedule and run chains separate
- **Explicit Dependencies**: Import all required middleware modules
- **Documentation**: Comment complex middleware chains
- **Validation**: Validate middleware configuration at startup

### Middleware Ordering
- **Authentication**: Always first in chain
- **Authorization**: After authentication
- **Logging/Monitoring**: Early in chain for complete coverage
- **Business Logic**: Core middleware in middle
- **Cleanup**: Resource cleanup middleware last

### Maintenance Guidelines
- **Regular Review**: Periodically review middleware chains
- **Performance Monitoring**: Track middleware overhead
- **Error Analysis**: Monitor middleware-related errors
- **Version Management**: Keep middleware dependencies updated

## Security Implications

### Middleware Security
- **Input Validation**: Validate middleware configuration
- **Access Control**: Ensure appropriate middleware for each context
- **Error Disclosure**: Prevent sensitive information leakage in errors
- **Resource Limits**: Implement resource usage limits in middleware

### Configuration Security
- **Environment Variables**: Use secure configuration for sensitive settings
- **Feature Flags**: Secure feature flag management
- **Access Logging**: Log middleware configuration changes

This configuration module provides the foundation for a flexible and extensible middleware system in the TSP job scheduling infrastructure, enabling comprehensive monitoring, security, and operational capabilities across different job execution contexts.