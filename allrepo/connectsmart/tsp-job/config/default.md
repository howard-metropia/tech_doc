# TSP Job Service - Default Configuration

## Overview

The `config/default.js` file serves as the primary configuration module for the TSP Job service, defining all essential settings, environment variables, and service parameters required for the application to function properly. This comprehensive configuration system supports multi-environment deployment and provides centralized management of all service dependencies.

## File Information

- **File Path**: `/config/default.js`
- **File Type**: JavaScript Configuration Module
- **Primary Purpose**: Centralized application configuration management
- **Dependencies**: dotenv, database configurations, vendor configurations

## Configuration Structure

### Environment Loading
```javascript
require('dotenv').config();
```

The configuration begins by loading environment variables from `.env` files, ensuring secure and flexible configuration management across different deployment environments.

## Core Configuration Sections

### 1. Project Configuration
```javascript
project: {
  name: process.env.PROJECT_NAME,
  stage: process.env.PROJECT_STAGE,
  title: process.env.PROJECT_TITLE,
}
```

**Purpose**: Defines project identity and deployment stage information
- `name`: Project identifier for logging and monitoring
- `stage`: Deployment environment (development, staging, production)
- `title`: Human-readable project title for administrative interfaces

### 2. Application Configuration
```javascript
app: {
  port: process.env.APP_PORT || 8888,
  logLevel: process.env.APP_LOG_LEVEL || 'info',
  debug: process.env.APP_DEBUG || false,
  apiVersion: process.env.API_VERSION || '/api/v1',
  project: process.env.APP_PROJECT || '/api/v1',
}
```

**Purpose**: Core application runtime settings
- `port`: HTTP server port for health checks and admin endpoints
- `logLevel`: Logging verbosity (error, warn, info, debug, trace)
- `debug`: Development debugging mode toggle
- `apiVersion`: API versioning for backward compatibility
- `project`: Project-specific API routing prefix

### 3. Database Configuration
```javascript
database: require('./database.js')
```

**Purpose**: Imports comprehensive database configuration including:
- MySQL connection settings for transactional data
- MongoDB configuration for job queues and analytics
- Redis settings for caching and session management
- InfluxDB configuration for time-series metrics

### 4. Vendor Services Configuration
```javascript
vendor: require('./vendor.js')
```

**Purpose**: External service integration settings including:
- AWS services (S3, SQS, SNS, Pinpoint)
- Payment processors (Stripe)
- Mapping services (Google Maps, HERE Maps)
- Communication services (Slack, Email)
- Transportation providers (Uber, ByteMark)

### 5. Pagination Settings
```javascript
page: {
  rows: 10,
}
```

**Purpose**: Default pagination configuration for database queries and API responses

### 6. JWT Authentication Configuration
```javascript
jwtKey: process.env.JWT_KEY,
jwtRotateKey: process.env.JWT_ROTATE_KEY,
```

**Purpose**: JSON Web Token security configuration
- `jwtKey`: Primary signing key for token generation
- `jwtRotateKey`: Secondary key for seamless token rotation

## Advanced Configuration Sections

### 7. Habitual Trip Processing
```javascript
habitualTripIntersectionMode: process.env.HABITUAL_TRIP_INTERSECTION_MODE || 'original',
// habitualTripIntersectionMode:
// 1: 'original': indexed trajectory
// 2: 'buffered': indexed buffered trajectory
```

**Purpose**: Controls trip intersection analysis algorithms
- `original`: Uses indexed trajectory data for intersection detection
- `buffered`: Uses buffered trajectory data for more accurate spatial analysis

### 8. Email Service Configuration
```javascript
mail: {
  url: process.env.MAIL_SERVER,
  smtp: {
    host: process.env.SMTP_HOST,
    port: process.env.SMTP_PORT,
    user: process.env.SMTP_USERNAME,
    pass: process.env.SMTP_PASSWORD,
    from: process.env.SMTP_FROM,
  },
}
```

**Purpose**: Email service configuration for notifications and reports
- `url`: Mail server endpoint for API-based sending
- `smtp`: Traditional SMTP configuration for direct email sending
- Supports both API and SMTP delivery methods

### 9. Portal Integration Configuration
```javascript
portal: {
  hashid: {
    key: 'gogogokey',
    length: 16,
  },
  sailsUrl: process.env.PORTAL_SAILS_URL || 'http://local_client:1337',
  web2pyUrl: process.env.PORTAL_WEB2PY_URL || 'http://local_client:8080',
  enableUnitPrice: process.env.PORTAL_ENABLE_UNIT_PRICE || 'true',
  escrow: {
    passengerTransactionFee: process.env.PORTAL_ESCROW_PASSENGER_TRANSACTION_FEE || 0,
    driverTransactionFee: process.env.PORTAL_ESCROW_DRIVER_TRANSACTION_FEE || 0,
  },
  pointsTransactionSchema: process.env.POINTS_TRANSACTION_SCHEMA || 'points_transaction',
}
```

**Purpose**: Integration with legacy portal systems
- `hashid`: ID obfuscation for security
- `sailsUrl`: Sails.js framework endpoint
- `web2pyUrl`: Web2py framework endpoint
- `escrow`: Transaction fee configuration for ridesharing
- `pointsTransactionSchema`: Database schema for points management

### 10. Instant Carpool Configuration
```javascript
instantCarpool: {
  timeThreshold: process.env.PORTAL_INSTANT_CARPOOL_TIME_THRESHOLD || 80,
  trajectoryThreshold: process.env.PORTAL_INSTANT_CARPOOL_TRAJECTORY_THRESHOLD || 80,
  reCalculateRange: process.env.PORTAL_INSTANT_CARPOOL_RECALCULATE_RANGE || 72,
}
```

**Purpose**: Real-time carpooling matching algorithms
- `timeThreshold`: Maximum time difference for trip matching (minutes)
- `trajectoryThreshold`: Minimum trajectory similarity percentage
- `reCalculateRange`: Recalculation window for optimizing matches (hours)

### 11. Engine Integration
```javascript
engine: {
  url: process.env.ENGINE_URL,
}
```

**Purpose**: Integration with the core MaaS processing engine

### 12. WTA Integration
```javascript
wta: {
  url: process.env.WTA_URL,
}
```

**Purpose**: Washington Transit Authority integration for public transit data

### 13. Daily Account Monitoring
```javascript
dailyAccount: {
  receipts: process.env.ACCOUNT_ALERT_RECIPIENTS,
  blacklist: process.env.ACCOUNT_ALERT_BLACK_LIST,
  mailActivated: process.env.ACCOUNT_ALERT_MAIL_ACTIVATED || false,
}
```

**Purpose**: Account balance monitoring and alerting
- `receipts`: Email recipients for account alerts
- `blacklist`: Accounts to exclude from monitoring
- `mailActivated`: Toggle for email alert functionality

### 14. Incentive System Configuration
```javascript
incentive: {
  incentiveWebUrl: process.env.INCENTIVE_WEB_URL,
  incentiveAdminUrl: process.env.INCENTIVE_ADMIN_URL,
  incentiveHookUrl: process.env.INCENTIVE_HOOK_URL || 'https://dev-incentive-hook.connectsmartx.com',
}
```

**Purpose**: Integration with incentive management system
- `incentiveWebUrl`: Public-facing incentive portal
- `incentiveAdminUrl`: Administrative interface
- `incentiveHookUrl`: Webhook endpoint for incentive processing

### 15. Firebase Integration
```javascript
firebase: {
  realtimeDBUrl: process.env.FIREBASE_REALTIMEDB_URL
}
```

**Purpose**: Real-time database integration for live features

### 16. Weather Service Configuration
```javascript
weather: {
  mockAllowed: process.env.WEATHER_MOCK_ALLOW || false,
}
```

**Purpose**: Weather service integration and testing
- `mockAllowed`: Enables mock weather data for testing environments

## Configuration Usage Patterns

### Environment-Based Configuration
The configuration system supports multiple deployment environments:

```javascript
// Development environment
NODE_ENV=development
APP_DEBUG=true
APP_LOG_LEVEL=debug

// Production environment
NODE_ENV=production
APP_DEBUG=false
APP_LOG_LEVEL=info
```

### Security Considerations
- All sensitive credentials are loaded from environment variables
- No hardcoded secrets or API keys
- JWT keys support rotation for enhanced security
- Database connections use encrypted protocols

### Configuration Validation
```javascript
// Example validation logic (not in current file)
function validateConfig(config) {
  const required = [
    'database.mysql.host',
    'jwtKey',
    'vendor.aws.accessKeyId'
  ];
  
  for (const path of required) {
    if (!get(config, path)) {
      throw new Error(`Missing required configuration: ${path}`);
    }
  }
}
```

## Integration with Application

### Loading Configuration
```javascript
const config = require('config');

// Access configuration values
const port = config.get('app.port');
const dbConfig = config.get('database.mysql');
const jwtKey = config.get('jwtKey');
```

### Dynamic Configuration
Some configuration values support runtime modification:
- Feature flags can be toggled without restart
- Thresholds can be adjusted for algorithm tuning
- Connection pool sizes can be modified for performance

## Best Practices

### 1. Environment Variable Naming
- Use consistent prefixes (APP_, DATABASE_, VENDOR_)
- Follow SCREAMING_SNAKE_CASE convention
- Group related variables logically

### 2. Default Values
- Provide sensible defaults for non-critical settings
- Require explicit configuration for security-sensitive values
- Use environment-appropriate defaults

### 3. Configuration Documentation
- Document the purpose of each configuration section
- Provide examples of valid values
- Explain the impact of configuration changes

### 4. Secret Management
- Store secrets in environment variables or secret management systems
- Rotate credentials regularly
- Use different credentials for different environments

## Deployment Considerations

### Container Deployment
```dockerfile
# Environment variables in Dockerfile
ENV NODE_ENV=production
ENV APP_LOG_LEVEL=info
ENV DATABASE_SSL=true
```

### Kubernetes Configuration
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: tsp-job-config
data:
  NODE_ENV: "production"
  APP_PORT: "8888"
  APP_LOG_LEVEL: "info"
```

### Health Check Configuration
The configuration supports health check endpoints that monitor:
- Database connectivity
- External service availability
- Configuration validity
- System resource utilization

This comprehensive configuration system ensures that the TSP Job service can be deployed across various environments while maintaining security, flexibility, and operational excellence.