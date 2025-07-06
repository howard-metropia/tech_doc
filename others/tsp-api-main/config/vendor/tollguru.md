# TollGuru Configuration Module

## 🔍 Quick Summary (TL;DR)
- **Functionality**: TollGuru API configuration module providing toll calculation service credentials and endpoints for route-based toll estimation in transportation services
- **Keywords**: tollguru | toll-calculation | route-pricing | api-config | transportation-costs | toll-roads | travel-expenses | navigation-costs | routing-fees | traffic-tolls
- **Use Cases**: Route cost estimation, travel expense calculation, transportation planning, toll-aware navigation
- **Compatibility**: Node.js ≥14.0, Express/Koa.js frameworks, REST API integration

## ❓ Common Questions Quick Index
1. **Q: How do I configure TollGuru API credentials?** → [Configuration Parameters](#configuration-parameters)
2. **Q: What is the TollGuru service endpoint URL?** → [Technical Specifications](#technical-specifications)
3. **Q: How to integrate TollGuru with routing services?** → [Usage Methods](#usage-methods)
4. **Q: What if TollGuru API key is missing or invalid?** → [Important Notes](#important-notes)
5. **Q: How to troubleshoot TollGuru connection issues?** → [Important Notes](#troubleshooting)
6. **Q: What data source does TollGuru use for calculations?** → [Technical Specifications](#data-source)
7. **Q: How to handle TollGuru API rate limits?** → [Important Notes](#rate-limiting)
8. **Q: Can I use different map providers with TollGuru?** → [Usage Methods](#map-provider-integration)
9. **Q: How to test TollGuru integration in development?** → [Output Examples](#testing-scenarios)
10. **Q: What are TollGuru's pricing and billing considerations?** → [Important Notes](#pricing-considerations)

## 📋 Functionality Overview
- **Non-technical explanation**: Like a GPS calculator that estimates highway tolls - imagine planning a road trip where you need to know not just the distance and time, but also how much you'll pay in tolls. TollGuru acts like a financial advisor for your route, telling you the cost of taking toll roads versus free alternatives, similar to how a restaurant menu shows prices for different meal options.
- **Technical explanation**: Configuration module that exports TollGuru API credentials and service endpoints for real-time toll calculation integration. Provides standardized access to TollGuru's REST API using HERE Maps as the routing data source for accurate toll estimations.
- **Business value**: Enables accurate travel cost forecasting, improves route planning decisions, and provides transparent pricing for transportation services, essential for ride-sharing, logistics, and travel planning applications.
- **System context**: Part of the TSP API vendor configuration layer, integrating with routing services to provide comprehensive trip cost analysis including toll expenses for end-to-end transportation cost calculation.

## 🔧 Technical Specifications
- **File info**: tollguru.js | /config/vendor/ | JavaScript | Module export | 5 lines | Complexity: ⭐ (Simple)
- **Dependencies**: 
  - Node.js process.env (built-in) - Environment variable access - Critical
  - TollGuru REST API v1 - External service dependency - High
  - HERE Maps integration - Data source provider - Medium
- **Environment variables**:
  - `TOLLGURU_API_KEY` (required) - TollGuru service authentication token
- **API compatibility**: TollGuru REST API v1, HERE Maps Platform API
- **System requirements**: 
  - Minimum: Node.js 14.0+, 512MB RAM, network connectivity
  - Recommended: Node.js 18.0+, 1GB RAM, stable internet connection
- **Security**: API key-based authentication, HTTPS endpoints, environment variable protection

## 📝 Detailed Code Analysis
```javascript
module.exports = {
  apiKey: process.env.TOLLGURU_API_KEY,    // Authentication credential from environment
  url: 'https://apis.tollguru.com',        // TollGuru service base endpoint
  source: 'here',                          // Map data provider specification
};
```
- **Module pattern**: Simple object export providing configuration constants
- **Execution flow**: Immediate module loading → environment variable resolution → object export
- **Error handling**: Relies on consuming modules for validation and error management
- **Security pattern**: Environment variable injection prevents credential hardcoding
- **Performance**: Zero computational overhead, static configuration loading
- **Memory usage**: Minimal footprint (~50 bytes), single object allocation

## 🚀 Usage Methods
**Basic Integration**:
```javascript
const tollguruConfig = require('./config/vendor/tollguru');
const axios = require('axios');

// Initialize TollGuru client
const tollguruClient = axios.create({
  baseURL: tollguruConfig.url,
  headers: {
    'x-api-key': tollguruConfig.apiKey,
    'Content-Type': 'application/json'
  }
});
```

**Route Toll Calculation**:
```javascript
async function calculateTolls(origin, destination) {
  const response = await tollguruClient.post('/v1/calc/route', {
    from: origin,
    to: destination,
    vehicleType: '2AxlesAuto',
    departure_time: Date.now(),
    map: tollguruConfig.source
  });
  return response.data;
}
```

**Environment Configuration**:
```bash
# Development
TOLLGURU_API_KEY=your_dev_api_key_here

# Production
TOLLGURU_API_KEY=your_prod_api_key_here
```

## 📊 Output Examples
**Successful Configuration Loading**:
```javascript
{
  apiKey: "tk_12345abcdef67890",
  url: "https://apis.tollguru.com",
  source: "here"
}
```

**TollGuru API Response Example**:
```json
{
  "summary": {
    "cost": 15.50,
    "currency": "USD",
    "distance": 125.5,
    "duration": 7200
  },
  "tolls": [
    {
      "name": "Golden Gate Bridge",
      "cost": 8.20,
      "currency": "USD"
    }
  ]
}
```

**Error Scenarios**:
```javascript
// Missing API key
{ apiKey: undefined, url: "https://apis.tollguru.com", source: "here" }
// API Error Response: 401 Unauthorized
```

## ⚠️ Important Notes
**Security Considerations**:
- Never commit API keys to version control
- Use environment-specific API keys (dev/staging/prod)
- Implement API key rotation policies
- Monitor API usage for suspicious activity

**Troubleshooting**:
- **Missing API key**: Verify TOLLGURU_API_KEY environment variable is set
- **403 Forbidden**: Check API key validity and account status
- **Rate limiting**: Implement exponential backoff and request queuing
- **Network errors**: Add retry logic with circuit breaker pattern

**Rate Limiting**: TollGuru enforces rate limits (typically 1000 requests/hour for free tier)
**Pricing**: Usage-based billing, monitor API call volume for cost management

## 🔗 Related File Links
- **Main config**: `/config/default.js` - Central configuration aggregation
- **Vendor configs**: `/config/vendor/` - Other external service configurations (AWS, HERE Maps)
- **Route services**: `/src/services/routing/` - Consumers of toll calculation data
- **Test files**: `/test/config/vendor/tollguru.test.js` - Configuration validation tests
- **Environment examples**: `/.env.example` - Environment variable templates

## 📈 Use Cases
**Route Planning**:
- Transportation apps calculating trip costs including tolls
- Logistics companies optimizing delivery routes based on toll expenses
- Travel planning platforms providing comprehensive cost estimates

**Business Intelligence**:
- Fleet management systems tracking toll expenses
- Expense reporting applications categorizing travel costs
- Financial planning tools for transportation budgets

**Integration Scenarios**:
- Real-time route optimization with cost considerations
- Multi-modal transportation planning including toll roads
- Dynamic pricing for ride-sharing services

## 🛠️ Improvement Suggestions
**Configuration Enhancements** (Low complexity, High impact):
- Add validation for API key format and presence
- Implement configuration caching with TTL
- Add support for multiple TollGuru environments

**Monitoring Integration** (Medium complexity, High impact):
- Add API usage tracking and alerting
- Implement health check endpoints for TollGuru connectivity
- Create dashboards for toll calculation metrics

**Performance Optimization** (Medium complexity, Medium impact):
- Implement request batching for multiple routes
- Add response caching for frequently calculated routes
- Optimize payload size by filtering unnecessary response data

## 🏷️ Document Tags
**Keywords**: tollguru, toll-calculation, api-configuration, route-pricing, transportation-costs, toll-roads, travel-expenses, navigation-costs, routing-fees, traffic-tolls, here-maps, cost-estimation, trip-planning, vehicle-routing
**Technical tags**: #config #vendor #api-client #transportation #toll-service #routing #cost-calculation #here-maps #travel-planning
**Target roles**: Backend developers (intermediate), DevOps engineers (beginner), Transportation engineers (advanced), System integrators (intermediate)
**Difficulty level**: ⭐ (Simple configuration module with external API dependency)
**Maintenance level**: Low (static configuration, occasional API key rotation)
**Business criticality**: Medium (affects cost calculation accuracy but not core functionality)
**Related topics**: Transportation APIs, Route optimization, Cost calculation, HERE Maps integration, External service configuration