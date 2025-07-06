# HereRouteQeuryLog Model

## Overview
MongoDB logging model for tracking HERE Maps API route query operations. This model provides audit trail and analytics capabilities for monitoring routing service usage, performance, and integration within the TSP system.

## File Location
`/src/models/HereRouteQeuryLog.js`

## Model Definition
```javascript
const { Schema } = require('mongoose');
const conn = require('@maas/core/mongo')('cache');

// ses_event
const mongoSchema = new Schema({
  query_from: { type: String },
  timestamp: { type: Date }
});
// eslint-disable-next-line new-cap
const HereRouteQeuryLog = conn.model('here_route_qeury_log', mongoSchema);

module.exports = HereRouteQeuryLog;
```

## Database Configuration
- **Database**: MongoDB cache instance
- **Collection**: `here_route_qeury_log`
- **Framework**: Mongoose ODM
- **Connection**: Managed by @maas/core MongoDB connection pool
- **Schema Mode**: Strict schema with defined fields

## Schema Definition

### query_from
- **Type**: String
- **Purpose**: Identifies the source component or service that initiated the route query
- **Examples**: "trip_planning", "route_optimization", "navigation_service"
- **Usage**: Track which system components are making routing requests

### timestamp
- **Type**: Date
- **Purpose**: Records when the HERE Maps API query was executed
- **Format**: ISO 8601 date format
- **Usage**: Chronological analysis and performance monitoring

## Purpose and Functionality
- **API Usage Tracking**: Monitor HERE Maps API consumption and patterns
- **Performance Analytics**: Analyze routing service response times and success rates
- **Service Integration Monitoring**: Track which services utilize routing capabilities
- **Cost Management**: Monitor API usage for billing and optimization purposes

## Key Features
- **Simple Schema**: Focused on essential routing query metadata
- **Source Tracking**: Identifies origin of routing requests
- **Timestamp Precision**: Accurate timing for performance analysis
- **MongoDB Integration**: Leverages document database for scalable logging

## Integration with HERE API Service
The model is primarily used by the **hereAPI.js** service which provides routing functionality:

```javascript
// From hereAPI.js service
const HereRouteQeuryLog = require('@app/src/models/HereRouteQeuryLog');

async function hereRouting(transportMode, originLocation, destinationLocation, returnMode, queryFrom) {
  const params = {
    transportMode: transportMode,
    origin: originLocation,
    destination: destinationLocation,
    return: returnMode,
    apikey: hereConfig.apiKey,
  };

  try {
    const response = await axiosApiInstance.get('/v8/routes', {
      params,
    });
    const result = response.data;
    
    // Log successful query
    await HereRouteQeuryLog.create({
      query_from: queryFrom,
      timestamp: new Date()
    });
    
    return result;
  } catch (e) {
    logger.error(`hereRouting ${e}`);
    // Optional: Log failed queries for analysis
    // await HereRouteQeuryLog.create({
    //   query_from: queryFrom,
    //   timestamp: new Date()
    // });
  }
}
```

## Routing Service Integration
The HERE Maps integration supports various routing scenarios:

### Transport Modes
- **Car Routing**: Optimal driving routes with traffic considerations
- **Public Transit**: Multi-modal transit routing
- **Walking**: Pedestrian-friendly routes
- **Bicycle**: Bike-friendly path planning

### Query Sources
- **Trip Planning**: User-initiated route requests
- **Real-time Navigation**: Dynamic route recalculation
- **Batch Processing**: Bulk route optimization
- **Service Integration**: Third-party service routing requests

## Usage Patterns

### Standard Route Query Logging
```javascript
// Log a successful route query
const queryLog = {
  query_from: 'mobile_app_trip_planning',
  timestamp: new Date()
};

await HereRouteQeuryLog.create(queryLog);
```

### Batch Query Analysis
```javascript
// Analyze queries from specific source
const serviceCalls = await HereRouteQeuryLog.find({
  query_from: 'trip_planning_service',
  timestamp: {
    $gte: new Date(Date.now() - 24 * 60 * 60 * 1000) // Last 24 hours
  }
});
```

## Analytics and Monitoring

### API Usage Metrics
- **Query Volume**: Track daily/hourly API call patterns
- **Source Distribution**: Identify which services use routing most
- **Peak Usage**: Determine high-traffic periods for capacity planning
- **Growth Trends**: Monitor increasing API usage over time

### Performance Analysis
- **Response Time Correlation**: Cross-reference with response time logs
- **Error Rate Tracking**: Monitor failed vs successful queries
- **Service Reliability**: Identify patterns in service disruptions
- **Optimization Opportunities**: Find frequently queried routes for caching

## Query Patterns for Analysis

### Daily Usage Summary
```javascript
// Get daily query counts by source
const dailyStats = await HereRouteQeuryLog.aggregate([
  {
    $match: {
      timestamp: {
        $gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
      }
    }
  },
  {
    $group: {
      _id: {
        date: { $dateToString: { format: "%Y-%m-%d", date: "$timestamp" } },
        source: "$query_from"
      },
      count: { $sum: 1 }
    }
  }
]);
```

### Peak Usage Hours
```javascript
// Identify peak usage patterns
const hourlyUsage = await HereRouteQeuryLog.aggregate([
  {
    $group: {
      _id: { $hour: "$timestamp" },
      count: { $sum: 1 }
    }
  },
  { $sort: { count: -1 } }
]);
```

## Integration Points
- **hereAPI.js Service**: Primary integration point for routing operations
- **Trip Planning Components**: Route calculation for user journeys
- **Navigation Services**: Real-time routing and re-routing
- **Analytics Dashboards**: Usage monitoring and reporting

## Performance Considerations
- **Lightweight Logging**: Minimal overhead on routing operations
- **Async Operations**: Non-blocking log insertion
- **Index Strategy**: Consider indexing timestamp and query_from fields
- **Bulk Operations**: Support batch logging for high-volume scenarios

## Cost Management
- **API Usage Monitoring**: Track HERE Maps API consumption
- **Budget Alerts**: Monitor approaching API limits
- **Optimization Identification**: Find opportunities to reduce API calls
- **Caching Strategy**: Identify frequently requested routes for caching

## Data Retention Strategy
- **Short-term Analysis**: Keep recent data for operational monitoring
- **Long-term Trends**: Archive historical data for trend analysis
- **Storage Optimization**: Balance retention needs with storage costs
- **Cleanup Automation**: Regular purging of old log entries

## Security and Compliance
- **API Key Protection**: Ensure API keys not logged in clear text
- **Location Privacy**: Consider privacy implications of route logging
- **Access Control**: Restrict access to routing usage data
- **Audit Requirements**: Maintain logs for system audit purposes

## Troubleshooting Applications
- **Service Downtime**: Identify gaps in routing service availability
- **Error Pattern Analysis**: Correlate errors with specific query sources
- **Performance Degradation**: Track changes in routing service performance
- **Integration Issues**: Debug problems with routing service integration

## Future Enhancements
- **Extended Metadata**: Add route complexity, distance, and duration fields
- **Error Logging**: Include error details for failed queries
- **Response Time Tracking**: Add timing information for performance analysis
- **Geographic Analysis**: Include origin/destination regions for spatial analysis

Note: The model name contains a typo ("Qeury" instead of "Query") which is preserved for compatibility with existing implementations.