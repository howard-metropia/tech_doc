# TSP API Configuration Module Documentation

## 🔍 Quick Summary (TL;DR)

Central configuration module for TSP API that manages all environment variables, service connections, and application settings to enable multi-modal transportation services and administrative functions.

**Keywords:** configuration | config | environment | settings | env-vars | tsp-api | transportation | maas | mobility | service-config | app-config | system-settings

**Primary Use Cases:**
- Application bootstrapping and initialization
- Database and external service connection management
- JWT authentication configuration for multi-tenant security
- Email and notification service setup
- Portal and UI integration settings

**Compatibility:** Node.js 14+, Koa.js framework, supports production and development environments

## ❓ Common Questions Quick Index

**Q: How do I configure database connections?** → [Technical Specifications](#technical-specifications)
**Q: What environment variables are required?** → [Usage Methods](#usage-methods)
**Q: How to set up JWT authentication keys?** → [Detailed Code Analysis](#detailed-code-analysis)
**Q: How to configure email services?** → [Usage Methods](#usage-methods)
**Q: What if portal domain URL is not working?** → [Important Notes](#important-notes)
**Q: How to troubleshoot configuration loading errors?** → [Important Notes](#important-notes)
**Q: How to set up Firebase integration?** → [Usage Methods](#usage-methods)
**Q: What are the security requirements?** → [Important Notes](#important-notes)
**Q: How to configure for different environments?** → [Usage Methods](#usage-methods)
**Q: What happens if required keys are missing?** → [Output Examples](#output-examples)
**Q: How to optimize performance settings?** → [Improvement Suggestions](#improvement-suggestions)
**Q: How to scale configuration for high traffic?** → [Use Cases](#use-cases)

## 📋 Functionality Overview

**Non-technical explanation:** Think of this file as the master control panel for a transportation app - like the electrical panel in a building that controls all the lights, heating, and power outlets. Just as an electrical panel connects different circuits to provide power where needed, this configuration connects the app to databases, email services, payment systems, and other external services. It's like a recipe book that tells the application exactly what ingredients (services) to use and how much of each.

**Technical explanation:** Environment-driven configuration module that exports a JavaScript object containing structured settings for database connections, external service integrations, authentication mechanisms, and application parameters. Implements the configuration pattern with environment variable fallbacks and modular organization.

**Business value:** Enables rapid deployment across multiple environments (development, staging, production) while maintaining security through environment-based secrets management. Supports multi-tenant architecture and reduces configuration drift between deployments.

**System context:** Core dependency for TSP API initialization, loaded during application bootstrap to establish all external connections and service configurations required for mobility-as-a-service operations.

## 🔧 Technical Specifications

**File Information:**
- **Name:** default.js
- **Path:** /config/default.js
- **Language:** JavaScript (Node.js)
- **Type:** Configuration module
- **Size:** ~4KB
- **Complexity:** Medium (environment-dependent, multiple integrations)

**Dependencies:**
- **dotenv** (Critical): Environment variable loader for .env file support
- **./database.js** (Critical): Database connection configurations
- **./vendor.js** (Critical): Third-party service configurations

**Environment Variables (47 total):**
- **App Config:** APP_PORT, APP_LOG_LEVEL, APP_DEBUG, API_VERSION
- **JWT Security:** JWT_KEY, JWT_ROTATE_KEY, JWT_ENTERPRISE_KEY
- **Email:** MAIL_SERVER, SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SMTP_FROM
- **Portal:** PROTAL_DOMAIN, PORTAL_SAILS_URL, PORTAL_WEB2PY_URL (and 15 more)
- **Firebase:** FIREBASE_WEB_API_KEY, FIREBASE_DOMAIN_URI_PREFIX (and 2 more)
- **APNS:** APNS_KEY_ID, APNS_TEAM_ID, APNS_BUNDLE_ID, APNS_PRODUCTION
- **External Services:** ENGINE_ROUTING_URL, WTA_URL, WEATHER_MOCK_ALLOW (and 5 more)

**System Requirements:**
- **Minimum:** Node.js 14+, 512MB RAM, environment variable support
- **Recommended:** Node.js 18+, 1GB RAM, container orchestration for env management
- **Production:** Load balancer support, secrets management system, monitoring

## 📝 Detailed Code Analysis

**Main Module Structure:**
```javascript
module.exports = {
  app: { /* Application settings */ },
  database: require('./database.js'),
  vendor: require('./vendor.js'),
  // ... other sections
};
```

**Key Configuration Sections:**

1. **Application Settings (`app`)**: Port, logging, debug mode, API versioning
2. **Authentication (`jwtKey`, `jwtRotateKey`, `jwtEnterpriseKey`)**: Multi-key JWT system
3. **Email Configuration (`mail`)**: SMTP settings and mail server URL
4. **Portal Settings (`portal`)**: Domain URLs, feature flags, escrow settings
5. **Mobile Services (`firebase`, `apns`)**: Push notifications and deep linking
6. **External Engines (`engine`, `wta`, `cycling`)**: Routing and transit services

**Error Handling:** Configuration module relies on runtime validation - missing critical environment variables will cause service failures at startup or during operation.

**Design Patterns:** 
- **Configuration Object Pattern**: Structured settings organization
- **Environment Abstraction**: Consistent interface across deployment environments
- **Modular Configuration**: Separation of concerns through file inclusion

## 🚀 Usage Methods

**Basic Application Loading:**
```javascript
const config = require('./config/default.js');
console.log(`Starting on port: ${config.app.port}`);
```

**Environment-Specific Configuration:**
```bash
# Development
APP_PORT=3000 APP_DEBUG=true node app.js

# Production
APP_PORT=8888 APP_LOG_LEVEL=warn JWT_KEY=prod_secret node app.js
```

**Required Environment Variables (.env file):**
```env
# Essential
JWT_KEY=your_jwt_secret_key_here
PROTAL_DOMAIN=your-domain.com
MAIL_SERVER=https://your-mail-service.com

# Database (see database.js)
DB_HOST=localhost
DB_USER=tsp_user
DB_PASSWORD=secure_password

# Optional with defaults
APP_PORT=8888
APP_LOG_LEVEL=info
WELCOME_COIN=3.5
```

**Integration Pattern:**
```javascript
const config = require('./config/default');
const jwt = require('jsonwebtoken');

// Using JWT configuration
const token = jwt.sign(payload, config.jwtKey);

// Using portal settings
const redirectUrl = `${config.portal.domainUrl}/redirect`;
```

## 📊 Output Examples

**Successful Configuration Load:**
```javascript
{
  app: { port: 8888, logLevel: 'info', debug: false, apiVersion: 'v2' },
  jwtKey: 'prod_jwt_key_value',
  portal: {
    domainUrl: 'https://production-domain.com',
    welcomeCoin: '3.5',
    // ... other settings
  }
}
```

**Missing Environment Variable (JWT_KEY):**
```javascript
{
  jwtKey: undefined, // Will cause authentication failures
  // Application may start but JWT operations will fail
}
```

**Development vs Production Output:**
```javascript
// Development
{ portal: { domainUrl: 'http://localhost:8888' } }

// Production (with PROTAL_DOMAIN=app.example.com)
{ portal: { domainUrl: 'https://app.example.com' } }
```

**Error Scenarios:**
- **Missing .env file**: Uses fallback defaults, may cause service failures
- **Invalid port value**: Node.js will reject non-numeric ports
- **Missing database config**: Application will fail to start

## ⚠️ Important Notes

**Security Considerations:**
- **Never commit .env files** containing production secrets
- **Rotate JWT keys regularly** using JWT_ROTATE_KEY for zero-downtime updates
- **Use environment-specific secrets** - avoid hardcoded values
- **SMTP credentials exposure** - ensure proper secrets management

**Common Troubleshooting:**

**Symptom:** "Cannot read property of undefined" errors
**Diagnosis:** Missing environment variables
**Solution:** Check .env file exists and contains required variables

**Symptom:** JWT authentication failures
**Diagnosis:** JWT_KEY not set or rotated incorrectly
**Solution:** Verify JWT_KEY and JWT_ROTATE_KEY in environment

**Symptom:** Email not sending
**Diagnosis:** SMTP configuration incomplete
**Solution:** Verify all SMTP_* variables are set correctly

**Performance Considerations:**
- Configuration loading occurs once at startup - no runtime performance impact
- Large environment variable counts may slow container startup
- Database connection pooling configured in database.js affects performance

**Breaking Changes:**
- Renaming environment variables requires deployment coordination
- Adding required variables needs infrastructure updates
- URL format changes affect client applications

## 🔗 Related File Links

**Direct Dependencies:**
- `/config/database.js` - Database connection settings and pool configuration
- `/config/vendor.js` - Third-party service API keys and endpoints
- `.env` - Environment variables file (not committed to repository)

**Configuration Consumers:**
- `/src/app.js` - Main application bootstrap
- `/src/middlewares/auth.js` - JWT authentication middleware
- `/src/services/mail.js` - Email service initialization
- `/src/controllers/*` - All controllers access config for external services

**Related Documentation:**
- Database configuration schema in database.js
- JWT authentication flow documentation
- Email service integration guide
- Firebase setup documentation

## 📈 Use Cases

**Daily Operations:**
- **DevOps Engineers**: Environment-specific deployments and configuration management
- **Backend Developers**: Service integration and feature flag management
- **Security Teams**: Secrets rotation and access control configuration

**Development Workflows:**
- **Local Development**: Quick setup with default values and local services
- **Testing Environments**: Isolated configurations for automated testing
- **Staging Deployment**: Production-like settings with test external services

**Scaling Scenarios:**
- **High Traffic**: Increase connection pools and adjust timeout values
- **Multi-Region**: Region-specific URLs and service endpoints
- **Load Balancing**: Shared configuration across multiple application instances

## 🛠️ Improvement Suggestions

**Security Enhancements (High Priority):**
- Implement configuration validation at startup with detailed error messages
- Add environment variable encryption for sensitive values
- Create configuration schema validation using Joi or similar

**Operational Improvements (Medium Priority):**
- Add configuration change detection and hot-reloading capabilities
- Implement configuration versioning and rollback mechanisms
- Create automated configuration testing and validation pipelines

**Performance Optimizations (Low Priority):**
- Cache configuration object to prevent repeated environment variable reads
- Implement lazy loading for optional service configurations
- Add configuration monitoring and alerting for runtime changes

**Maintenance Recommendations:**
- **Weekly**: Review environment variable usage and remove unused configs
- **Monthly**: Audit security configurations and rotate sensitive keys
- **Quarterly**: Update default values based on operational experience

## 🏷️ Document Tags

**Keywords:** configuration, config, environment-variables, env-vars, tsp-api, koa-config, node-config, app-settings, service-configuration, jwt-config, smtp-config, firebase-config, apns-config, portal-config, database-config, vendor-config, mobility-config, transportation-settings

**Technical Tags:** #config #environment #nodejs #koa #jwt #authentication #email #firebase #apns #portal #database #vendor #mobility #transportation #maas #settings #env-vars

**Target Roles:** 
- **DevOps Engineers** (⭐⭐⭐): Environment management and deployment
- **Backend Developers** (⭐⭐): Service integration and configuration
- **Security Engineers** (⭐⭐⭐): Secrets management and authentication setup
- **System Administrators** (⭐⭐): Infrastructure configuration and monitoring

**Difficulty Level:** ⭐⭐⭐ (3/5) - Requires understanding of environment variables, external service integrations, and security best practices

**Maintenance Level:** Medium - Regular updates needed for new services, security rotations, and environment changes

**Business Criticality:** Critical - Application cannot function without proper configuration; affects all system components

**Related Topics:** nodejs-configuration, environment-management, secrets-management, service-integration, authentication-setup, deployment-configuration, container-orchestration, microservices-config