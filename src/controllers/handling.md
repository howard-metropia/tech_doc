# TSP API Error Handling Controller Documentation

## 🔍 Quick Summary (TL;DR)
The handling controller provides centralized error reporting and monitoring capabilities, collecting error information from various system components and routing it to monitoring services like Slack and InfluxDB for operational visibility.

**Keywords:** error-handling | monitoring | observability | slack-notifications | influxdb | vendor-errors | api-monitoring | centralized-logging | operational-alerts

**Primary use cases:** System error reporting, vendor API failure notifications, operational monitoring, debugging assistance

**Compatibility:** Node.js >= 16.0.0, Koa.js v2.x, Slack API, InfluxDB

## ❓ Common Questions Quick Index
- **Q: What is this controller used for?** → Centralized error reporting and monitoring
- **Q: How does Slack notification work?** → [Slack Integration](#slack-integration)
- **Q: What data gets stored in InfluxDB?** → [InfluxDB Metrics](#influxdb-metrics)
- **Q: What types of errors are tracked?** → Vendor API failures and system errors
- **Q: How are alerts configured?** → Through Slack channels and InfluxDB dashboards
- **Q: Who receives error notifications?** → Development and operations teams via Slack

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **centralized emergency dispatch system** for software problems. When something goes wrong anywhere in the system (like a payment processor failing or a mapping service being down), this controller acts like a 911 operator - it receives the error report, logs all the details, and immediately notifies the right people through Slack while also storing the information in a database for later analysis.

**Technical explanation:** 
A specialized Koa.js controller that serves as a centralized error collection endpoint. It receives error reports, formats them appropriately, sends notifications via Slack using SlackManager, and stores metrics in InfluxDB for monitoring and analysis. This enables real-time operational awareness and historical error tracking.

**Business value explanation:**
Critical for maintaining system reliability and operational excellence. Enables rapid response to system issues, provides visibility into vendor service dependencies, and supports data-driven decisions about system improvements and vendor relationships.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/controllers/handling.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Koa.js v2.x with @koa/router
- **Type:** Monitoring/Observability Controller
- **File Size:** ~1.3 KB
- **Complexity Score:** ⭐⭐ (Medium - Integration with multiple monitoring services)

**Dependencies:**
- `@koa/router`: HTTP routing framework (**Critical**)
- `koa-bodyparser`: Request body parsing (**Critical**)
- `@maas/services/SlackManager`: Slack notification service (**Critical**)
- `@app/src/services/influxDb`: InfluxDB metrics service (**Critical**)
- `@app/src/schemas/handling`: Input validation schemas (**High**)
- `config`: Configuration management (**High**)

**External Integrations:**
- **Slack API:** Real-time error notifications
- **InfluxDB:** Time-series metrics storage
- **Environment Variables:** PROJECT_NAME, PROJECT_STAGE for context

## 📝 Detailed Code Analysis

### Error Reporting Endpoint (`POST /`)

**Purpose:** Receives and processes error reports from system components

**Flow:**
1. **Input Validation:** Validates error data against handling schema
2. **Slack Notification:** Sends formatted error message to Slack channel
3. **Logging:** Records error details in application logs
4. **Metrics Storage:** Stores error metrics in InfluxDB for analysis
5. **Response:** Returns success acknowledgment

**Slack Integration:**
```javascript
const slack = new SlackManager(
  slackConfig.token,
  slackConfig.channelId,
  'C05BYMEPD3P', // Specific channel for vendor errors
);

slack.sendVendorFailedMsg({
  project: process.env.PROJECT_NAME,
  stage: process.env.PROJECT_STAGE,
  status: 'ERROR',
  vendor: 'Handling',
  vendorApi: data.error.api,
  originApi: 'POST /api/v2/handling',
  errorMsg: data.error.msg,
  meta: JSON.stringify(data.error),
});
```

**InfluxDB Metrics:**
```javascript
await influxService.write({
  tags: {
    api: 'handling',
    project: process.env.PROJECT_NAME,
    stage: process.env.PROJECT_STAGE,
  },
  fields: {
    errorCode: data.error.code,
    errorMsg: data.error.msg,
    apiUrl: data.error.api,
    userId: data.error.user_id,
    response: JSON.stringify(data.error.response),
  },
  measurement: 'api_handling',
  timestamp: new Date(),
});
```

## 🚀 Usage Methods

### Report System Error
```bash
curl -X POST "https://api.tsp.example.com/api/v2/handling" \
  -H "Content-Type: application/json" \
  -d '{
    "error": {
      "code": "VENDOR_API_FAILURE",
      "msg": "Payment processor timeout",
      "api": "/api/v1/payments/process",
      "user_id": "usr_12345",
      "response": {
        "status": 500,
        "error": "Gateway timeout"
      }
    }
  }'
```

### JavaScript Error Reporting
```javascript
async function reportError(errorInfo) {
  try {
    const response = await fetch('/api/v2/handling', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        error: {
          code: errorInfo.code,
          msg: errorInfo.message,
          api: errorInfo.endpoint,
          user_id: errorInfo.userId,
          response: errorInfo.responseData
        }
      })
    });
    
    if (response.ok) {
      console.log('Error reported successfully');
    }
  } catch (error) {
    console.error('Failed to report error:', error);
  }
}
```

## 📊 Output Examples

### Successful Error Report
```json
{
  "result": "success",
  "data": {}
}
```

### Validation Error
```json
{
  "error": "ValidationError",
  "message": "Invalid error data format",
  "details": [
    {
      "field": "error.code",
      "message": "error.code is required"
    }
  ]
}
```

**Slack Notification Format:**
```
🔴 VENDOR ERROR ALERT
Project: tsp-api
Stage: production
Status: ERROR
Vendor: Handling
Vendor API: /api/v1/payments/process
Origin API: POST /api/v2/handling
Error: Payment processor timeout
Meta: {"code":"VENDOR_API_FAILURE","response":{"status":500}}
```

## ⚠️ Important Notes

### Monitoring Strategy
- **Real-time Alerts:** Slack notifications provide immediate visibility
- **Historical Analysis:** InfluxDB enables trend analysis and reporting
- **Error Classification:** Vendor errors are specifically categorized for vendor management
- **Context Preservation:** Full error context is preserved for debugging

### Configuration Requirements
- **Slack Configuration:** Requires valid Slack token and channel IDs
- **InfluxDB Setup:** Needs properly configured InfluxDB connection
- **Environment Variables:** PROJECT_NAME and PROJECT_STAGE must be set
- **Channel Permissions:** Slack bot must have appropriate channel permissions

### Security Considerations
- **Sensitive Data:** Error messages may contain sensitive information
- **Access Control:** Endpoint should be restricted to internal services
- **Data Retention:** Consider data retention policies for error logs
- **Rate Limiting:** Implement rate limiting to prevent spam

### Operational Benefits
- **Faster Incident Response:** Real-time notifications enable quick response
- **Vendor Accountability:** Track vendor service reliability
- **System Health Visibility:** Comprehensive error monitoring
- **Data-Driven Decisions:** Historical data supports improvement planning

## 🔗 Related File Links

- **Validation Schema:** `allrepo/connectsmart/tsp-api/src/schemas/handling.js`
- **InfluxDB Service:** `allrepo/connectsmart/tsp-api/src/services/influxDb.js`
- **Slack Configuration:** Configured via `config.vendor.slack`
- **SlackManager Service:** `@maas/services/SlackManager`

---
*This controller provides essential operational monitoring and error reporting capabilities for system reliability.*