# TSP Job: Ridehail Refund Process

## Quick Summary

The `ridehail-refund-process.js` job manages automated refund processing for Uber guest rides, handling both rider-initiated cancellations and system-triggered refunds. It runs continuously to process cancelled trips that require refunds and performs comprehensive refund processing during a specific time window (first 4 minutes of each hour). This job ensures timely refund processing, maintains payment integrity, and handles edge cases in the guest ride payment flow.

## Technical Analysis

### Job Architecture

The job implements a time-sensitive dual processing pattern:

```javascript
const { processRefundingTrips } = require('@app/src/services/uber/guest-ride');
const { processRiderCanceledTrips } = require('@app/src/services/uber/guest-ride');

const isWithinRange = () => {
  const now = new Date();
  const minutes = now.getMinutes();
  return minutes >= 0 && minutes <= 4;
};

module.exports = {
  inputs: {},
  fn: async function () {
    // Always process rider cancellations
    await processRiderCanceledTrips();
    
    // Only process general refunds during specific time window
    if (isWithinRange()) {
      await processRefundingTrips();
    }
  },
};
```

### Processing Strategy

1. **Continuous Processing**: `processRiderCanceledTrips()` runs every execution
2. **Scheduled Processing**: `processRefundingTrips()` runs only during minutes 0-4 of each hour
3. **Time Window Logic**: Prevents overwhelming payment systems with bulk refunds

### Refund Categories

The job handles two distinct refund scenarios:

#### Rider Cancelled Trips
- Immediate cancellations by riders
- Pre-ride cancellations
- Early ride terminations
- Real-time refund requirements

#### System Refunding Trips
- Failed ride completions
- Payment processing errors
- Disputed charges
- Batch refund processing

## Usage/Integration

### Scheduling Configuration

This job requires frequent execution due to its time-sensitive nature:

```javascript
// Recommended scheduling (every minute)
{
  name: 'ridehail-refund-process',
  schedule: '* * * * *', // Every minute
  job: 'ridehail-refund-process'
}
```

### Time Window Strategy

The 0-4 minute window serves multiple purposes:
- **Load Distribution**: Prevents all instances from processing refunds simultaneously
- **API Rate Limiting**: Respects external payment provider limits
- **Audit Trail**: Creates predictable refund processing windows
- **System Resources**: Concentrates heavy processing in defined periods

### Process Flow

```javascript
// Rider cancellation flow (runs every minute)
processRiderCanceledTrips() {
  1. Query cancelled trips awaiting refund
  2. Validate cancellation eligibility
  3. Calculate refund amount
  4. Process payment reversal
  5. Update trip status
  6. Send notifications
}

// Batch refund flow (runs minutes 0-4)
processRefundingTrips() {
  1. Query all trips in 'refunding' state
  2. Group by payment method
  3. Batch process refunds
  4. Handle partial refunds
  5. Retry failed refunds
  6. Generate refund reports
}
```

## Dependencies

### Service Layer
- **@app/src/services/uber/guest-ride**: Core refund processing logic
- **Payment Service**: Stripe/payment provider integration
- **Notification Service**: Customer refund notifications

### External Systems
- **Uber API**: Ride cancellation webhooks
- **Payment Providers**: Stripe, credit card processors
- **Banking Systems**: ACH/wire transfer handling

### Data Stores
- **MongoDB**: Trip and refund tracking
- **MySQL**: Transaction records
- **Redis**: Temporary refund state management

## Code Examples

### Manual Refund Processing

```javascript
// Force immediate refund processing
const refundJob = require('./ridehail-refund-process');

// Process both types regardless of time
await refundJob.fn();

// Or call services directly
const { processRefundingTrips, processRiderCanceledTrips } = 
  require('@app/src/services/uber/guest-ride');

await processRiderCanceledTrips();
await processRefundingTrips();
```

### Custom Time Window Implementation

```javascript
// Extend time window for testing
const isWithinRange = (startMinute = 0, endMinute = 4) => {
  const now = new Date();
  const minutes = now.getMinutes();
  return minutes >= startMinute && minutes <= endMinute;
};

// Process refunds during extended window
if (isWithinRange(0, 10)) {
  await processRefundingTrips();
}
```

### Monitoring Integration

```javascript
// Add metrics tracking
const monitoredRefundProcess = async () => {
  const metrics = {
    cancelledTripsProcessed: 0,
    refundsProcessed: 0,
    errors: []
  };
  
  try {
    // Track cancelled trips
    const cancelResult = await processRiderCanceledTrips();
    metrics.cancelledTripsProcessed = cancelResult.processed;
    
    // Track batch refunds
    if (isWithinRange()) {
      const refundResult = await processRefundingTrips();
      metrics.refundsProcessed = refundResult.processed;
    }
    
    // Log metrics
    logger.info('Refund job completed', metrics);
  } catch (error) {
    metrics.errors.push(error);
    logger.error('Refund job failed', metrics);
    throw error;
  }
};
```

### Service Implementation Patterns

```javascript
// Expected service implementation
const processRiderCanceledTrips = async () => {
  const cancelledTrips = await GuestRides.find({
    status: 'rider_cancelled',
    refundStatus: 'pending'
  });
  
  for (const trip of cancelledTrips) {
    try {
      // Calculate refund based on cancellation time
      const refundAmount = calculateRefundAmount(trip);
      
      // Process refund through payment service
      const refund = await paymentService.refund({
        chargeId: trip.chargeId,
        amount: refundAmount,
        reason: 'rider_cancelled'
      });
      
      // Update trip record
      await GuestRides.updateOne(
        { _id: trip._id },
        { 
          refundStatus: 'completed',
          refundId: refund.id,
          refundAmount: refundAmount
        }
      );
      
      // Send notification
      await notificationService.sendRefundNotification(trip.userId, refund);
    } catch (error) {
      logger.error('Failed to process refund', { tripId: trip._id, error });
      // Mark for retry
      await GuestRides.updateOne(
        { _id: trip._id },
        { refundStatus: 'failed', retryCount: trip.retryCount + 1 }
      );
    }
  }
};
```

### Error Handling Strategies

```javascript
// Robust error handling with retry logic
const processRefundWithRetry = async (trip, maxRetries = 3) => {
  let lastError;
  
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      await processRefund(trip);
      return true;
    } catch (error) {
      lastError = error;
      logger.warn(`Refund attempt ${attempt} failed`, { 
        tripId: trip._id, 
        error: error.message 
      });
      
      // Exponential backoff
      if (attempt < maxRetries) {
        await new Promise(resolve => 
          setTimeout(resolve, Math.pow(2, attempt) * 1000)
        );
      }
    }
  }
  
  // All retries failed
  throw lastError;
};
```

This job is essential for maintaining customer trust and payment integrity in the ridehail system. The sophisticated time-windowing approach balances immediate refund needs with system resource management, while the dual-processing pattern ensures both urgent and batch refunds are handled appropriately.