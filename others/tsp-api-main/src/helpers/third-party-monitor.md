# Third-Party Monitor Helper

## 🔍 Quick Summary (TL;DR)
Event-driven error monitoring system that sends third-party service failures to Slack channels for immediate alerting and debugging. | error monitoring | event emitter | slack alerts | third party monitoring | service failures | real-time notifications | system health | vendor monitoring | error tracking | alert system | failure detection | monitoring system | slack integration | error reporting | service monitoring

**Core functionality:** Centralized error alerting system using EventEmitter pattern to monitor third-party service failures
**Primary use cases:** Monitor vendor API failures, send real-time alerts to operations teams, track service health
**Compatibility:** Node.js 14+, Koa.js framework, requires @maas/services package

## ❓ Common Questions Quick Index
1. **How to send error alerts?** → [Usage Methods](#usage-methods)
2. **What errors get monitored?** → [Technical Specifications](#technical-specifications)
3. **How to customize alert destinations?** → [Usage Methods](#usage-methods)
4. **Why are alerts not being sent?** → [Important Notes](#important-notes)
5. **How to test error monitoring?** → [Output Examples](#output-examples)
6. **What happens when Slack is down?** → [Important Notes](#important-notes)
7. **How to add new error types?** → [Usage Methods](#usage-methods)
8. **Can I disable Slack notifications?** → [Usage Methods](#usage-methods)
9. **How to monitor multiple services?** → [Use Cases](#use-cases)
10. **What's the error handling flow?** → [Detailed Code Analysis](#detailed-code-analysis)

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a "smoke detector" for your software services. Just like a smoke detector alerts you when there's fire, this monitor alerts your team when external services (like payment processors, map providers, or transit APIs) fail. It's like having a dedicated security guard who immediately calls the fire department when something goes wrong.

**Technical explanation:** 
Event-driven monitoring utility that implements the Observer pattern using Node.js EventEmitter to capture third-party service failures and route them to configured notification channels (primarily Slack). Provides abstraction layer for error reporting with pluggable receiver architecture.

**Business value:** Reduces mean time to detection (MTTD) for third-party service failures, enabling faster incident response and minimizing user impact. Critical for maintaining SLA compliance in MaaS platform operations.

**System context:** Central component in TSP API monitoring infrastructure, used by controllers and services to report vendor failures. Integrates with Slack for real-time operations team notifications.

## 🔧 Technical Specifications

**File Information:**
- Name: third-party-monitor.js
- Path: /src/helpers/third-party-monitor.js
- Language: JavaScript (Node.js)
- Type: Helper utility module
- Size: ~32 lines
- Complexity: Low (single responsibility, simple event handling)

**Dependencies:**
- `events` (Node.js built-in) - Core EventEmitter functionality [Critical]
- `@maas/services` (^1.0.0) - SlackManager for notifications [Critical]
- `config` - Configuration management for Slack/PM settings [Critical]

**Configuration Parameters:**
- `vendor.slack.token` - Slack bot token (required)
- `vendor.pm.slackChannel` - Target Slack channel (required)
- Environment: Development, staging, production support

**System Requirements:**
- Node.js 14+ (EventEmitter compatibility)
- Network access for Slack API calls
- Valid Slack bot token with channel permissions

**Security Requirements:**
- Slack token stored in environment variables
- No sensitive data in error messages
- Channel access controls via Slack permissions

## 📝 Detailed Code Analysis

**Main Components:**
```javascript
// Event emitter for decoupled error handling
const eventEmitter = new EventEmitter();

// Configurable receiver with default Slack implementation
let receiver = {
  send: async (error) => {
    await slack.sendVendorFailedMsg(error);
  }
};
```

**Execution Flow:**
1. Error occurs in service/controller
2. `errorAlert` event emitted with error details
3. Event listener triggers receiver.send()
4. SlackManager formats and sends notification
5. Async operation completes without blocking caller

**Key Functions:**
- `eventEmitter.emit('errorAlert', error)` - Trigger error notification
- `eventEmitter.setReceiver(newReceiver)` - Replace notification handler
- `receiver.send(error)` - Process error notification

**Design Patterns:**
- **Observer Pattern:** EventEmitter for loose coupling
- **Strategy Pattern:** Pluggable receiver architecture
- **Singleton Pattern:** Module exports single instance

**Error Handling:**
- Async error handling in receiver.send()
- No error propagation to prevent cascading failures
- Silent failure mode for resilience

## 🚀 Usage Methods

**Basic Usage:**
```javascript
const monitor = require('./helpers/third-party-monitor');

// Send error alert
monitor.emit('errorAlert', {
  service: 'stripe',
  error: 'Payment processing failed',
  timestamp: new Date(),
  details: { orderId: '12345' }
});
```

**Custom Receiver Configuration:**
```javascript
// For testing or custom notifications
const testReceiver = {
  send: async (error) => {
    console.log('Test alert:', error);
    // Custom logic here
  }
};

monitor.setReceiver(testReceiver);
```

**Service Integration Pattern:**
```javascript
// In service files
const monitor = require('../helpers/third-party-monitor');

async function callThirdPartyAPI() {
  try {
    const result = await externalAPI.call();
    return result;
  } catch (error) {
    monitor.emit('errorAlert', {
      service: 'external-api',
      error: error.message,
      stack: error.stack
    });
    throw error; // Re-throw for local handling
  }
}
```

**Production Configuration:**
```javascript
// config/production.js
module.exports = {
  vendor: {
    slack: {
      token: process.env.SLACK_BOT_TOKEN
    },
    pm: {
      slackChannel: '#operations-alerts'
    }
  }
};
```

## 📊 Output Examples

**Successful Alert Transmission:**
```
✅ Slack notification sent successfully
Channel: #operations-alerts
Message: "🚨 Vendor Service Alert: stripe - Payment processing failed"
Timestamp: 2024-01-15T10:30:00Z
Response time: 200ms
```

**Error Alert Format:**
```json
{
  "service": "stripe",
  "error": "Payment processing failed",
  "timestamp": "2024-01-15T10:30:00Z",
  "details": {
    "orderId": "12345",
    "amount": 29.99,
    "errorCode": "card_declined"
  }
}
```

**Slack Message Format:**
```
🚨 Third-Party Service Alert
Service: Stripe Payment
Error: card_declined - Payment processing failed
Time: 2024-01-15 10:30:00 UTC
Order: #12345
```

**Test Mode Output:**
```javascript
// When using test receiver
console.log('Test alert:', {
  service: 'test-service',
  error: 'Simulated failure',
  timestamp: '2024-01-15T10:30:00Z'
});
```

## ⚠️ Important Notes

**Security Considerations:**
- Never include sensitive data (passwords, tokens, PII) in error messages
- Validate Slack token permissions before deployment
- Use environment variables for all configuration

**Common Troubleshooting:**
- **No alerts received:** Check Slack token validity and channel permissions
- **Duplicate alerts:** Implement debouncing in calling code
- **Missing error details:** Ensure error objects contain required fields

**Performance Considerations:**
- Async operations prevent blocking main thread
- Single EventEmitter instance prevents memory leaks
- No retry logic - implement in calling code if needed

**Rate Limiting:**
- Slack API has rate limits (1 message/second per channel)
- Consider implementing alert aggregation for high-volume errors
- Use circuit breaker pattern for repeated failures

**Disaster Recovery:**
- Service continues operating if Slack is unavailable
- No local logging fallback - implement separately if needed
- Consider multiple notification channels for redundancy

## 🔗 Related File Links

**Dependencies:**
- `/config/default.js` - Configuration settings for Slack integration
- `@maas/services/SlackManager` - Slack notification implementation
- `/src/controllers/*.js` - Controllers that emit error alerts

**Usage Examples:**
- `/src/services/stripe-webhook.js` - Payment failure monitoring
- `/src/services/ridehail.js` - Third-party transport API monitoring
- `/src/controllers/parking.js` - Parking service error handling

**Testing Files:**
- `/test/helpers/third-party-monitor.test.js` - Unit tests for monitoring
- `/test/integration/slack-alerts.test.js` - Integration tests

**Configuration:**
- `/config/production.js` - Production Slack settings
- `/config/development.js` - Development notification settings

## 📈 Use Cases

**Daily Operations:**
- Monitor payment gateway failures during peak hours
- Track third-party transit API outages
- Alert on mapping service degradation

**Development Phase:**
- Test error handling with custom receivers
- Validate notification formatting
- Debug integration issues

**Production Scenarios:**
- High-volume error aggregation during incidents
- Multi-service failure correlation
- Operations team incident response

**Anti-patterns:**
- Don't use for application logic errors (use for external service failures only)
- Avoid sending sensitive data in error messages
- Don't rely solely on Slack for critical alerts

## 🛠️ Improvement Suggestions

**Code Optimization:**
- Add error message deduplication (Medium complexity, High benefit)
- Implement retry logic with exponential backoff (Low complexity, Medium benefit)
- Add structured logging fallback (Low complexity, High benefit)

**Feature Enhancements:**
- Multiple notification channels (email, SMS) (Medium complexity, High benefit)
- Error categorization and severity levels (Medium complexity, Medium benefit)
- Alert aggregation and summarization (High complexity, High benefit)

**Monitoring Improvements:**
- Health check endpoint for monitor status (Low complexity, Medium benefit)
- Metrics collection for alert frequency (Medium complexity, High benefit)
- Dashboard integration for error visualization (High complexity, High benefit)

**Maintenance Recommendations:**
- Weekly: Review alert frequency and adjust thresholds
- Monthly: Validate Slack token and channel permissions
- Quarterly: Assess notification effectiveness and user feedback

## 🏷️ Document Tags

**Keywords:** error monitoring, event emitter, slack alerts, third party monitoring, service failures, real-time notifications, system health, vendor monitoring, error tracking, alert system, failure detection, monitoring system, slack integration, error reporting, service monitoring, async notifications, observer pattern, EventEmitter, notification system

**Technical Tags:** #monitoring #alerts #slack #event-emitter #error-handling #third-party #notifications #async #observer-pattern #koa-helpers #maas-services #vendor-monitoring #real-time #system-health

**Target Roles:** 
- DevOps Engineers (Intermediate) - System monitoring and alerting
- Backend Developers (Beginner) - Error handling integration
- Operations Teams (Beginner) - Alert management and response

**Difficulty Level:** ⭐⭐ (Simple EventEmitter usage with external service integration)

**Maintenance Level:** Low (Stable module with minimal changes needed)

**Business Criticality:** High (Critical for incident detection and response)

**Related Topics:** error handling, system monitoring, incident management, service reliability, notification systems, third-party integrations, DevOps practices, alert fatigue prevention