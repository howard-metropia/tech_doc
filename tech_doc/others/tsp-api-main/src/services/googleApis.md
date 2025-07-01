# Google Maps API Client Service Documentation

## 🔍 Quick Summary (TL;DR)
This service acts as a centralized, robust, and observable client for interacting with various **Google Maps Platform APIs**. It wraps several key Google Maps endpoints (like Directions, Geocoding, and Place Photos) into standardized asynchronous functions. More importantly, it enriches these basic API calls with critical production-grade features: **service monitoring** via InfluxDB and **error alerting** via Slack. Every call made through this service is timed, logged, and in case of failure, an immediate alert is dispatched.

**Keywords:** google-maps | api-client | wrapper | observability | monitoring | influxdb | slack-alert

**Primary use cases:** 
- To provide a single, reliable point of access for all Google Maps API calls within the application.
- To automatically handle API key attachment, request timeouts, and standardized error responses.
- To monitor the performance and success/failure rate of Google Maps API dependencies.
- To immediately alert developers via Slack when a Google Maps API call fails.

## ❓ Common Questions Quick Index
- **Q: What does this service do?** → It's a wrapper around the Google Maps API that adds logging, monitoring, and alerting.
- **Q: Which Google APIs does it use?** → It uses the Geocoding API (for addresses), the Directions API (for routes), and the Place Photo API (for images).
- **Q: What is InfluxDB used for?** → To record the performance (duration) and status (success/error) of every single API call made to Google. This is used for creating dashboards and monitoring system health.
- **Q: What is Slack used for?** → To send an immediate notification to a specific channel whenever a call to a Google API fails, allowing for rapid response to outages or issues.
- **Q: Does it just pass requests through?** → No. It adds a significant layer of value through robust error handling and deep integration with our monitoring and alerting infrastructure.

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this service as a **highly professional and responsible courier for delivering messages to Google**.
1.  **You Have a Message:** You give the courier a request, like "Please ask Google for directions from A to B."
2.  **The Courier Prepares the Message:** The courier takes your request, attaches the required postage (the API key), and puts it in a special trackable envelope.
3.  **The Courier Times the Delivery:** The courier starts a stopwatch the moment the message is sent (`const start = new Date();`).
4.  **The Delivery Succeeds:** When Google replies, the courier stops the stopwatch, logs the total delivery time and a "SUCCESS" status in a central logbook (InfluxDB), and then hands you the reply.
5.  **The Delivery Fails:** If Google's office is closed or the message gets lost, the courier stops the stopwatch, logs the time and an "ERROR" status in the logbook, and immediately sends an urgent message to the office manager (Slack) saying, "Delivery to Google failed! Here are the details." It then informs you that the request couldn't be completed.

**Technical explanation:** 
This module exports several async functions, each corresponding to a specific Google Maps API endpoint. An `axios` instance is pre-configured with the base URL and a timeout.
Each function (`fetchGooglePlacePhoto`, `fetchGoogleGeocodingInfo`, `fetchGoogleRoute`, etc.) follows a similar pattern:
1.  It accepts input parameters and the `originApi` (to identify the caller).
2.  It merges the input parameters with the required Google Maps `key`.
3.  It records a start time.
4.  It wraps the `axios` call in a `try...catch` block.
5.  **On success:** It writes a `SUCCESS` record to the `service_monitor` measurement in InfluxDB, including the duration, and returns the data from Google's response.
6.  **On failure:** It writes an `ERROR` record to InfluxDB with the error message. It then uses the `SlackManager` to dispatch a formatted alert. Finally, it throws a custom `MaasError` with an internally-defined error code, abstracting the raw HTTP error into a form the rest of the application can handle gracefully.
This robust pattern ensures that all interactions with the third-party dependency are instrumented and handled consistently.

**Business value explanation:**
This service is critical for operational stability and reliability. Third-party APIs like Google Maps are external dependencies that can fail or experience performance degradation without warning. By wrapping all calls in this service, we gain immediate insight into the health of this dependency. If our application starts failing, the monitoring data from this service allows us to instantly determine if the root cause is with Google's services or our own code. The proactive Slack alerts reduce downtime by enabling developers to address third-party outages or configuration issues (like an expired API key) almost immediately.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/googleApis.js`
- **Language:** JavaScript (Node.js)
- **Key Libraries:** `axios`, `@maas/core/log`, `@maas/services` (for Slack and Influx managers)
- **Type:** API Client / Service Wrapper
- **File Size:** ~10 KB
- **Complexity Score:** ⭐⭐⭐ (Medium. The logic is repetitive but the integration with external monitoring and alerting systems adds a moderate level of complexity.)

## 🚀 Usage Methods

```javascript
const googleApis = require('@app/src/services/googleApis');

// Example: Get the address for a given latitude and longitude
async function getAddressFromCoordinates(lat, lng) {
    try {
        const geocodingParams = {
            latlng: `${lat},${lng}`
        };

        // By calling through our service, this action is automatically
        // timed, monitored, and will trigger alerts on failure.
        const geocodingResults = await googleApis.fetchGoogleGeocodingInfo(
            geocodingParams,
            'my-awesome-feature' // This identifies which part of our app made the call
        );
        
        if (geocodingResults.length > 0) {
            return geocodingResults[0].formatted_address;
        }
        return 'No address found';

    } catch (error) {
        // The error will be a custom MaasError, which can be handled predictably.
        logger.error(`Failed to get address: ${error.message}`);
        // Potentially show a user-friendly message
        return 'Could not retrieve address at this time.';
    }
}
```

## 🔗 Related File Links
- **Configuration:** `config/default.js` (for `vendor.google.maps`, `database.influx`, `vendor.slack`)
- **Error Codes:** `@app/src/static/error-code.js`
- **Managers:** `@maas/services/SlackManager`, `@maas/services/InfluxManager`

---
*This documentation was generated to explain the service's role as a robust, observable client for the Google Maps Platform API.*