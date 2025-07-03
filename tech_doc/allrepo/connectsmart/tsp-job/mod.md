# TSP Job: Mode Choice Modeling (MOD)

## Quick Summary

The `mod.js` job implements sophisticated transportation mode choice modeling using Google Maps API data to calculate travel times, costs, and probabilities for different transportation modes (walking, transit, driving, bicycling). It processes unprocessed activity trips from the database, calculates multi-modal routing scenarios, applies logit modeling to determine mode choice probabilities, and stores results for transportation planning analysis. This job is essential for understanding travel behavior patterns and supporting mobility planning decisions.

## Technical Analysis

### Core Architecture

The job implements a comprehensive mode choice analysis workflow:

```javascript
const moment = require('moment-timezone');
const map = require('@app/src/services/googleMap');
const knex = require('@maas/core/mysql')('portal');
const { logger } = require('@maas/core/log');

module.exports = {
  inputs: {},
  fn: async function () {
    // Process all unprocessed trips
    const data = await knex
      .select('activity_trip.id')
      .from('cm_activity_location AS activity_trip')
      .whereNull('activity_trip.job_time');
      
    for (const row of data) {
      await processTrip(row.id);
      await markProcessed(row.id);
    }
  },
};
```

### Google Maps Integration

```javascript
async function directions(mode, origin, destination, departureTime) {
  const request = {
    mode,
    origin,
    destination,
    departure_time: departureTime,
  };
  
  switch (mode) {
    case 'transit':
      request.transit_mode = 'bus|rail';
      break;
    default:
  }
  
  return map.directions(request);
}
```

### Mode Choice Calculation Algorithm

The job implements a sophisticated logit model for mode choice probability:

```javascript
// Mode-specific utility coefficients
const conf = {
  walking: {
    CST: -0.335,    // Constant
    WKT: -0.0632,   // Walking time coefficient
    WT: -0.0759,    // Waiting time coefficient
    TT: -0.0632,    // Travel time coefficient
    RL: 0,          // Route length coefficient
    TC: -0.0048,    // Travel cost coefficient
    TS: 0,          // Transfer count coefficient
  },
  transit: {
    CST: -0.946,
    WKT: -0.0759,
    WT: -0.0759,
    TT: -0.0025,
    RL: 0,
    TC: -0.0048,
    TS: 0,
  },
  driving: {
    CST: 0,
    WKT: -0.0759,
    WT: -0.0759,
    TT: -0.0025,
    RL: 0,
    TC: -0.0048,
    TS: 0,
  },
  bicycling: {
    CST: -2.695,
    WKT: -0.0632,
    WT: -0.0759,
    TT: -0.0632,
    RL: 0,
    TC: -0.0048,
    TS: 0,
  },
};

// Logit utility calculation
function mod(mode, data) {
  const C = conf[mode];
  return Math.exp(
    C.CST +
    (C.WKT * Math.round(data.walking_time / 0.6)) / 100 +
    (C.WT * Math.round(data.waiting_time / 0.6)) / 100 +
    (C.TT * Math.round(data.invehicle_time / 0.6)) / 100 +
    C.RL * data.route_length +
    C.TC * data.travel_cost +
    C.TS * data.transfer_count,
  );
}
```

### Travel Metrics Calculation

```javascript
function calculate(result, departureTime) {
  let [walkingTime, inVehicleTime, travelCost, transferCount] = Array(4).fill(0);
  
  if (result.status != 'OK') {
    return {
      walking_time: 0,
      waiting_time: 0,
      invehicle_time: 0,
      route_length: 0,
      travel_cost: 0,
      transfer_count: 0,
    };
  }
  
  const [route] = result.routes;
  const [leg] = route.legs;
  const totalTime = leg.duration.value;
  const realDeparture = leg.departure_time ? leg.departure_time.value : departureTime;
  
  // Analyze each step of the route
  for (const step of leg.steps) {
    switch (step.travel_mode) {
      case 'WALKING':
        walkingTime += step.duration.value;
        break;
      case 'TRANSIT':
        transferCount += 1;
        inVehicleTime += step.duration.value;
        break;
      case 'DRIVING':
      case 'BICYCLING':
        inVehicleTime += step.duration.value;
        break;
      default:
        break;
    }
  }
  
  return {
    walking_time: walkingTime,
    waiting_time: totalTime - inVehicleTime - walkingTime + (realDeparture - departureTime),
    invehicle_time: inVehicleTime,
    route_length: leg.distance.value,
    travel_cost: travelCost,
    transfer_count: transferCount,
  };
}
```

## Usage/Integration

### Database Schema

The job works with several database tables:

```sql
-- Activity trips to process
CREATE TABLE cm_activity_location (
  id INT PRIMARY KEY,
  o_id INT,                    -- Origin location ID
  d_id INT,                    -- Destination location ID
  departure_time DATETIME,     -- Trip departure time
  job_time TIMESTAMP NULL      -- Processing timestamp
);

-- Location coordinates
CREATE TABLE cm_location (
  id INT PRIMARY KEY,
  latitude DECIMAL(10,8),
  longitude DECIMAL(11,8)
);

-- Mode choice results
CREATE TABLE cm_activity_mod (
  activity_id INT,
  travel_mode VARCHAR(20),
  walking_time INT,
  waiting_time INT,
  invehicle_time INT,
  route_length INT,
  travel_cost DECIMAL(10,2),
  transfer_count INT,
  mod_value DECIMAL(15,10),
  probability DECIMAL(5,2),
  PRIMARY KEY (activity_id, travel_mode)
);
```

### Processing Workflow

```javascript
async function processTrip(activityId) {
  // 1. Fetch trip details
  const trip = await getTrip(activityId);
  if (!trip) return;
  
  // 2. Calculate future departure time
  const weekday = moment(trip.departure_time).utc().day() < 6 ? 2 : 6;
  const time = moment(trip.departure_time).utc().format('HH:mm:ss');
  const newday = moment().utc().add(7, 'days').weekday(weekday).format('YYYY-MM-DD');
  const departureTime = moment(`${newday} ${time}`);
  
  // 3. Process all modes
  const data = [];
  let total = 0;
  
  for (const mode of ['bicycling', 'driving', 'transit', 'walking']) {
    const result = await directions(
      mode,
      [trip.origin_latitude, trip.origin_longitude],
      [trip.destination_latitude, trip.destination_longitude],
      departureTime.unix()
    );
    
    const insert = calculate(result, departureTime.unix());
    
    // Calculate utility value
    if (mode === 'transit' && insert.transfer_count == 0) {
      insert.mod_value = 0; // No transit available
    } else {
      insert.mod_value = mod(mode, insert);
    }
    
    total += insert.mod_value;
    insert.activity_id = activityId;
    insert.travel_mode = mode;
    data.push(insert);
  }
  
  // 4. Calculate probabilities
  for (const i in data) {
    data[i].probability = parseFloat((data[i].mod_value / total) * 100);
  }
  
  // 5. Store results with upsert
  await knex.raw(
    knex('cm_activity_mod').insert(data).toQuery() +
    ' ON DUPLICATE KEY UPDATE ' +
    [
      'walking_time', 'waiting_time', 'invehicle_time',
      'route_length', 'travel_cost', 'transfer_count',
      'mod_value', 'probability'
    ].map(field => `${field}=VALUES(${field})`).join(', ')
  );
}
```

## Dependencies

### External Services
- **Google Maps API**: Directions service for multi-modal routing
- **MySQL Database**: Trip data storage and results persistence

### Internal Dependencies
- **@app/src/services/googleMap**: Google Maps API wrapper
- **@maas/core/mysql**: Database connection management
- **@maas/core/log**: Centralized logging system

### Configuration Requirements

```javascript
// Google Maps API configuration
{
  googleMaps: {
    apiKey: 'YOUR_API_KEY',
    timeout: 30000,
    rateLimit: 10 // requests per second
  },
  database: {
    connection: 'portal',
    batchSize: 100
  }
}
```

## Code Examples

### Manual Processing Example

```javascript
// Process specific activity
const modJob = require('./mod');
await modJob.fn();

// Or process individual trip
const { processTrip } = modJob;
await processTrip(12345);
```

### Batch Processing with Rate Limiting

```javascript
// Enhanced processing with API rate limiting
const processWithRateLimit = async () => {
  const data = await knex
    .select('activity_trip.id')
    .from('cm_activity_location AS activity_trip')
    .whereNull('activity_trip.job_time')
    .limit(100); // Process in batches
    
  for (let i = 0; i < data.length; i++) {
    try {
      await processTrip(data[i].id);
      await markProcessed(data[i].id);
      
      // Rate limiting - 10 requests per second
      if (i % 10 === 0) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    } catch (error) {
      logger.error('Failed to process trip', { 
        tripId: data[i].id, 
        error: error.message 
      });
    }
  }
};
```

### Mode Choice Analysis

```javascript
// Analyze mode choice results
const analyzeModeChoice = async (activityId) => {
  const results = await knex('cm_activity_mod')
    .where('activity_id', activityId)
    .orderBy('probability', 'desc');
    
  const analysis = {
    dominantMode: results[0].travel_mode,
    probability: results[0].probability,
    alternatives: results.slice(1),
    sustainabilityScore: calculateSustainabilityScore(results)
  };
  
  return analysis;
};

const calculateSustainabilityScore = (modes) => {
  const weights = {
    walking: 1.0,
    bicycling: 0.9,
    transit: 0.7,
    driving: 0.2
  };
  
  return modes.reduce((score, mode) => {
    return score + (mode.probability * weights[mode.travel_mode]) / 100;
  }, 0);
};
```

### Error Handling and Retry Logic

```javascript
const processWithRetry = async (activityId, maxRetries = 3) => {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      await processTrip(activityId);
      return true;
    } catch (error) {
      logger.warn(`Attempt ${attempt} failed for activity ${activityId}`, error);
      
      if (attempt === maxRetries) {
        // Mark as failed for manual review
        await knex('cm_activity_location')
          .where('id', activityId)
          .update({
            job_time: knex.fn.now(),
            error_message: error.message,
            status: 'failed'
          });
        throw error;
      }
      
      // Exponential backoff
      await new Promise(resolve => 
        setTimeout(resolve, Math.pow(2, attempt) * 1000)
      );
    }
  }
};
```

### Performance Monitoring

```javascript
const monitoredModeProcessing = async () => {
  const startTime = Date.now();
  const metrics = {
    tripsProcessed: 0,
    apiCalls: 0,
    errors: []
  };
  
  try {
    const pendingTrips = await knex('cm_activity_location')
      .whereNull('job_time')
      .count('* as count');
    
    logger.info(`Starting MOD processing: ${pendingTrips[0].count} trips pending`);
    
    // Process trips with monitoring
    const data = await knex
      .select('activity_trip.id')
      .from('cm_activity_location AS activity_trip')
      .whereNull('activity_trip.job_time');
    
    for (const row of data) {
      await processTrip(row.id);
      metrics.tripsProcessed++;
      metrics.apiCalls += 4; // 4 modes per trip
    }
    
    const duration = Date.now() - startTime;
    logger.info('MOD processing completed', {
      ...metrics,
      duration,
      averageTimePerTrip: duration / metrics.tripsProcessed
    });
  } catch (error) {
    logger.error('MOD processing failed', { ...metrics, error });
    throw error;
  }
};
```

This job is fundamental to transportation modeling and planning, providing data-driven insights into travel behavior patterns. The sophisticated logit modeling approach enables accurate prediction of mode choice probabilities, supporting urban planning decisions and mobility service optimization.