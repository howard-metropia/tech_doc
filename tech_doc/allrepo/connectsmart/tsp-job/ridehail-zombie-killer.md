# TSP Job: Ridehail Zombie Killer

## Quick Summary

The `ridehail-zombie-killer.js` job is a critical maintenance utility that identifies and terminates "zombie" ridehail trips - rides that are stuck in intermediate states due to system failures, network issues, or edge cases. This job prevents resource leaks, ensures accurate trip accounting, and maintains system health by cleaning up orphaned ride requests that would otherwise remain in limbo indefinitely. It's an essential component for maintaining the integrity of the guest ride system.

## Technical Analysis

### Job Design

The job follows a minimalist pattern, delegating all zombie detection and cleanup logic to a dedicated service:

```javascript
const { processZombieTrips } = require('@app/src/services/uber/guest-ride');

module.exports = {
  inputs: {},
  fn: async function () {
    await processZombieTrips();
  },
};
```

### Zombie Trip Characteristics

Zombie trips typically exhibit these patterns:
- **Stuck States**: Trips frozen in 'processing', 'driver_assigned', or 'en_route' states
- **Timeout Violations**: Active trips exceeding reasonable time limits
- **Orphaned Records**: Trips with missing or disconnected related data
- **Failed Webhooks**: Trips awaiting status updates that never arrived
- **Network Failures**: Trips interrupted by connectivity issues

### Detection Strategies

The underlying service likely implements multiple detection methods:

```javascript
// Example zombie detection patterns
const zombieDetectionRules = {
  STUCK_PROCESSING: {
    state: 'processing',
    maxAge: 300, // 5 minutes
    description: 'Trip stuck in processing state'
  },
  ABANDONED_RIDE: {
    state: 'driver_en_route',
    maxAge: 3600, // 1 hour
    noUpdates: 1800, // No updates for 30 minutes
    description: 'Driver en route but no updates'
  },
  ORPHANED_REQUEST: {
    state: 'requested',
    maxAge: 600, // 10 minutes
    noDriverAssigned: true,
    description: 'Request with no driver assignment'
  },
  INCOMPLETE_TRIP: {
    state: 'on_trip',
    maxAge: 14400, // 4 hours
    description: 'Trip exceeding maximum duration'
  }
};
```

## Usage/Integration

### Scheduling Recommendations

This job should run frequently to prevent zombie accumulation:

```javascript
// Recommended scheduling options
{
  name: 'ridehail-zombie-killer',
  schedule: '*/15 * * * *', // Every 15 minutes
  job: 'ridehail-zombie-killer'
}
```

### Processing Workflow

1. **Identification Phase**
   - Query trips in suspicious states
   - Check age and update timestamps
   - Verify related data integrity

2. **Validation Phase**
   - Confirm zombie status
   - Check for recent updates
   - Verify with external APIs

3. **Cleanup Phase**
   - Cancel/complete zombie trips
   - Release held resources
   - Update user notifications
   - Log cleanup actions

### Integration Points

The zombie killer interacts with several system components:
- **Trip State Manager**: Updates trip statuses
- **Payment System**: Releases payment holds
- **Driver Allocation**: Frees assigned drivers
- **User Notifications**: Sends cleanup notifications
- **Audit System**: Logs all zombie terminations

## Dependencies

### Core Services
- **@app/src/services/uber/guest-ride**: Zombie detection and cleanup logic
- **Trip Management Service**: Core trip state handling
- **Payment Service**: Payment hold releases

### Data Systems
- **MongoDB**: Primary trip storage
- **Redis**: Real-time trip state cache
- **MySQL**: Audit trail and reporting

### External APIs
- **Uber API**: Status verification
- **Payment Providers**: Hold releases
- **Notification Services**: User communications

## Code Examples

### Manual Zombie Cleanup

```javascript
// Direct execution for immediate cleanup
const zombieKiller = require('./ridehail-zombie-killer');
await zombieKiller.fn();

// Or call service directly with options
const { processZombieTrips } = require('@app/src/services/uber/guest-ride');
await processZombieTrips({ 
  dryRun: true, // Preview without cleanup
  maxAge: 7200  // Custom timeout
});
```

### Monitoring Integration

```javascript
// Enhanced monitoring wrapper
const monitoredZombieKiller = async () => {
  const startTime = Date.now();
  const results = {
    zombiesFound: 0,
    zombiesKilled: 0,
    errors: []
  };
  
  try {
    const killResults = await processZombieTrips();
    results.zombiesFound = killResults.found;
    results.zombiesKilled = killResults.killed;
    
    logger.info('Zombie killer completed', {
      ...results,
      duration: Date.now() - startTime
    });
    
    // Alert if too many zombies
    if (results.zombiesFound > 10) {
      alertService.send('High zombie count detected', results);
    }
  } catch (error) {
    results.errors.push(error);
    logger.error('Zombie killer failed', results);
    throw error;
  }
};
```

### Expected Service Implementation

```javascript
// Typical zombie processing logic
const processZombieTrips = async (options = {}) => {
  const results = { found: 0, killed: 0, errors: [] };
  
  // Find potential zombies
  const zombieConditions = [
    // Stuck in processing
    {
      status: 'processing',
      updatedAt: { $lt: new Date(Date.now() - 5 * 60 * 1000) }
    },
    // Abandoned by driver
    {
      status: 'driver_en_route',
      updatedAt: { $lt: new Date(Date.now() - 30 * 60 * 1000) }
    },
    // Trip too long
    {
      status: 'on_trip',
      startedAt: { $lt: new Date(Date.now() - 4 * 60 * 60 * 1000) }
    }
  ];
  
  const zombies = await GuestRides.find({ $or: zombieConditions });
  results.found = zombies.length;
  
  for (const zombie of zombies) {
    try {
      // Verify zombie status with external API
      const isReallyZombie = await verifyZombieStatus(zombie);
      
      if (isReallyZombie && !options.dryRun) {
        await killZombie(zombie);
        results.killed++;
      }
    } catch (error) {
      results.errors.push({ tripId: zombie._id, error: error.message });
    }
  }
  
  return results;
};

// Zombie termination logic
const killZombie = async (trip) => {
  // Release payment holds
  if (trip.paymentHoldId) {
    await paymentService.releaseHold(trip.paymentHoldId);
  }
  
  // Free assigned driver
  if (trip.driverId) {
    await driverService.markAvailable(trip.driverId);
  }
  
  // Update trip status
  await GuestRides.updateOne(
    { _id: trip._id },
    {
      status: 'terminated',
      terminationReason: 'zombie_cleanup',
      terminatedAt: new Date()
    }
  );
  
  // Notify user
  await notificationService.send(trip.userId, {
    type: 'trip_terminated',
    message: 'Your trip was cancelled due to a system issue',
    tripId: trip._id
  });
  
  // Log for audit
  logger.info('Zombie trip terminated', {
    tripId: trip._id,
    previousStatus: trip.status,
    age: Date.now() - trip.createdAt
  });
};
```

### Safety Mechanisms

```javascript
// Zombie verification to prevent false positives
const verifyZombieStatus = async (trip) => {
  // Check multiple sources before killing
  const checks = await Promise.all([
    checkUberAPI(trip.externalId),
    checkRecentUpdates(trip._id),
    checkRelatedRecords(trip)
  ]);
  
  // Require multiple confirmations
  const confirmations = checks.filter(check => check === true).length;
  return confirmations >= 2;
};

// Grace period implementation
const hasGracePeriodExpired = (trip, graceMinutes = 5) => {
  const lastUpdate = new Date(trip.updatedAt);
  const gracePeriod = graceMinutes * 60 * 1000;
  return Date.now() - lastUpdate > gracePeriod;
};
```

### Metrics and Alerting

```javascript
// Zombie metrics tracking
const trackZombieMetrics = async (results) => {
  await metrics.gauge('ridehail.zombies.found', results.found);
  await metrics.gauge('ridehail.zombies.killed', results.killed);
  await metrics.gauge('ridehail.zombies.errors', results.errors.length);
  
  // Calculate zombie rate
  const totalTrips = await GuestRides.count({ 
    createdAt: { $gte: new Date(Date.now() - 24 * 60 * 60 * 1000) }
  });
  const zombieRate = (results.found / totalTrips) * 100;
  await metrics.gauge('ridehail.zombies.rate', zombieRate);
};
```

This job serves as a critical safety mechanism in the ridehail system, preventing resource exhaustion and ensuring system reliability. By proactively identifying and cleaning up zombie trips, it maintains system health and improves user experience by preventing indefinite waiting states.