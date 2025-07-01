# TSP API Test Suite - Uber Webhook Integration Tests

## Overview
The `test-uber-webhook.js` file contains comprehensive tests for Uber webhook integration, covering trip status updates, payment processing, receipt handling, and real-time communication with Uber's guest ride API.

## File Location
`/allrepo/connectsmart/tsp-api/test/test-uber-webhook.js`

## Dependencies
- **chai**: Testing assertions and expectations
- **crypto**: Signature verification for webhooks
- **moment-timezone**: Date/time manipulation
- **axios**: HTTP client for webhook testing
- **nock**: HTTP mocking for external services
- **uuid**: Unique identifier generation

## Test Architecture

### Service Integration
```javascript
const { notificationMessages } = require('@app/src/services/uber-webhook');
const { uber: uberDefinitions, travelMode } = require('@app/src/static/defines');
const uberConfig = require('config').vendor.uber;
```

### Model Dependencies
```javascript
const Trips = require('@app/src/models/Trips');
const Teleworks = require('@app/src/models/Teleworks');
const TeleworkLogs = require('@app/src/models/TeleworkLogs');
const RidehailTrips = require('@app/src/models/RidehailTrips');
const UberGuestRideLogs = require('@app/src/models/UberGuestRideLogs');
const Notifications = require('@app/src/models/Notifications');
```

### Test Application Setup
```javascript
const createApp = require('@maas/core/api');
const { getRouter } = require('@maas/core');

const app = createApp();
const router = getRouter();
const port = Math.floor(Math.random() * 64311) + 1024;
app.listen(port);

const httpClient = axios.create({
  baseURL: `http://localhost:${port}`
});
```

## Webhook Signature Verification

### Signature Generation
```javascript
const generateWebhookSignature = (payload, secret) => {
  const hmac = crypto.createHmac('sha256', secret);
  hmac.update(JSON.stringify(payload));
  return hmac.digest('hex');
};
```

### Request Authentication
```javascript
const authenticateWebhookRequest = (payload, signature, secret) => {
  const expectedSignature = generateWebhookSignature(payload, secret);
  return crypto.timingSafeEqual(
    Buffer.from(signature, 'hex'),
    Buffer.from(expectedSignature, 'hex')
  );
};
```

## Mock Request Generation

### Webhook Request Factory
```javascript
const mockRequest = (
  status = 'processing',
  requestId = '123e4567-e89b-12d3-a456-426614174001',
  eventType = 'guests.trips.status_changed'
) => {
  return {
    event_id: uuidv4(),
    event_time: new Date().getTime(),
    event_type: eventType,
    resource_href: 'https://metropia.demo.resources/1',
    meta: {
      user_id: 'user123',
      org_uuid: uuidv4(),
      resource_id: requestId,
      status
    }
  };
};
```

### Trip Data Preparation
```javascript
const prepareMockData = async (tripStatus = null) => {
  const now = moment().utc().toISOString();
  const startLocation = [29.756046, -95.408081];
  const endLocation = [29.717299, -95.402483];
  
  const mockTrip = {
    user_id: userId,
    travel_mode: travelMode.RIDEHAIL,
    origin: '1015 S Shepherd Dr, Houston, TX 77019, US',
    origin_latitude: startLocation[0],
    origin_longitude: startLocation[1],
    started_on: now,
    destination: '6100 Main St, Houston, TX 77005, US',
    destination_latitude: endLocation[0],
    destination_longitude: endLocation[1]
  };
  
  return mockTrip;
};
```

## Webhook Event Processing

### Status Change Handling
```javascript
describe('Uber Webhook Status Changes', () => {
  let tripId, ridehailTripId;
  
  beforeEach(async () => {
    const tripData = await prepareMockData();
    const trip = await Trips.query().insert(tripData);
    tripId = trip.id;
    
    const ridehailTrip = await RidehailTrips.query().insert({
      trip_id: tripId,
      uber_request_id: '123e4567-e89b-12d3-a456-426614174001',
      status: 'processing',
      product_id: '9c0fd086-b4bd-44f1-a278-bdae3cdb3d9f'
    });
    ridehailTripId = ridehailTrip.id;
  });
  
  it('should process trip accepted status', async () => {
    const webhook = mockRequest('accepted', ridehailTrip.uber_request_id);
    const signature = generateWebhookSignature(webhook, uberConfig.clientSecret);
    
    const response = await httpClient.post('/webhook/uber', webhook, {
      headers: {
        'X-Uber-Signature': signature,
        'Content-Type': 'application/json'
      }
    });
    
    expect(response.status).to.equal(200);
    
    // Verify database update
    const updatedTrip = await RidehailTrips.query().findById(ridehailTripId);
    expect(updatedTrip.status).to.equal('accepted');
  });
});
```

### Payment Status Updates
```javascript
describe('Payment Processing', () => {
  it('should handle completed trip with payment', async () => {
    const webhook = mockRequest('completed', ridehailTrip.uber_request_id);
    
    // Mock receipt data
    nock(uberConfig.baseUrl)
      .get(`/trips/${ridehailTrip.uber_request_id}/receipt`)
      .reply(200, mockData.receiptResponse);
    
    const signature = generateWebhookSignature(webhook, uberConfig.clientSecret);
    
    const response = await httpClient.post('/webhook/uber', webhook, {
      headers: { 'X-Uber-Signature': signature }
    });
    
    expect(response.status).to.equal(200);
    
    // Verify payment processing
    const updatedTrip = await RidehailTrips.query().findById(ridehailTripId);
    expect(updatedTrip.status).to.equal('completed');
    expect(updatedTrip.final_fare).to.be.above(0);
  });
});
```

## Event Type Handling

### Trip Status Events
```javascript
const WEBHOOK_EVENTS = {
  TRIP_STATUS_CHANGED: 'guests.trips.status_changed',
  TRIP_CANCELLED: 'guests.trips.cancelled',
  TRIP_COMPLETED: 'guests.trips.completed',
  PAYMENT_UPDATED: 'guests.payments.updated'
};

const processWebhookEvent = async (eventType, payload) => {
  switch (eventType) {
    case WEBHOOK_EVENTS.TRIP_STATUS_CHANGED:
      return await processTripStatusChange(payload);
    
    case WEBHOOK_EVENTS.TRIP_CANCELLED:
      return await processTripCancellation(payload);
    
    case WEBHOOK_EVENTS.TRIP_COMPLETED:
      return await processTripCompletion(payload);
    
    case WEBHOOK_EVENTS.PAYMENT_UPDATED:
      return await processPaymentUpdate(payload);
    
    default:
      throw new Error(`Unknown event type: ${eventType}`);
  }
};
```

### Status Transition Logic
```javascript
const validateStatusTransition = (currentStatus, newStatus) => {
  const validTransitions = {
    'processing': ['accepted', 'cancelled'],
    'accepted': ['arriving', 'cancelled'],
    'arriving': ['in_progress', 'cancelled'],
    'in_progress': ['completed', 'cancelled'],
    'completed': [],
    'cancelled': []
  };
  
  return validTransitions[currentStatus]?.includes(newStatus) || false;
};
```

## Receipt Processing

### Receipt Data Structure
```javascript
const receiptResponse = {
  request_id: '123e4567-e89b-12d3-a456-426614174001',
  subtotal: '$12.50',
  total_charged: '$15.75',
  total_owed: null,
  currency_code: 'USD',
  charge_adjustments: [
    {
      name: 'Safe Rides Fee',
      amount: '$1.25',
      type: 'fee'
    },
    {
      name: 'Tolls',
      amount: '$2.00',
      type: 'toll'
    }
  ],
  duration: '15 minutes 23 seconds',
  distance: '3.2 miles',
  distance_label: 'Distance'
};
```

### Receipt Processing Logic
```javascript
const processReceipt = async (requestId, receiptData) => {
  const ridehailTrip = await RidehailTrips.query()
    .where('uber_request_id', requestId)
    .first();
  
  if (!ridehailTrip) {
    throw new Error(`Trip not found for request ID: ${requestId}`);
  }
  
  const finalFare = convertCurrencyToNumber(receiptData.total_charged);
  const distance = parseFloat(receiptData.distance);
  const duration = parseDuration(receiptData.duration);
  
  await RidehailTrips.query()
    .where('id', ridehailTrip.id)
    .update({
      final_fare: finalFare,
      actual_distance: distance,
      actual_duration: duration,
      receipt_data: JSON.stringify(receiptData),
      completed_at: new Date()
    });
  
  return { success: true, fareProcessed: finalFare };
};
```

## Notification System

### User Notifications
```javascript
const notificationMessages = {
  TRIP_ACCEPTED: {
    title: 'Trip Accepted',
    message: 'Your driver has accepted the trip and is on the way!',
    type: 'trip_status'
  },
  TRIP_ARRIVING: {
    title: 'Driver Arriving',
    message: 'Your driver is arriving at the pickup location.',
    type: 'trip_status'
  },
  TRIP_IN_PROGRESS: {
    title: 'Trip Started',
    message: 'Your trip has started. Enjoy your ride!',
    type: 'trip_status'
  },
  TRIP_COMPLETED: {
    title: 'Trip Completed',
    message: 'Your trip has been completed. Thank you for riding!',
    type: 'trip_status'
  },
  TRIP_CANCELLED: {
    title: 'Trip Cancelled',
    message: 'Your trip has been cancelled.',
    type: 'trip_status'
  }
};
```

### SQS Integration for Notifications
```javascript
const { SQSClient, SendMessageCommand } = require('@aws-sdk/client-sqs');

const sendNotification = async (userId, notificationType, tripData) => {
  const notification = {
    user_id: userId,
    type: notificationType,
    title: notificationMessages[notificationType].title,
    message: notificationMessages[notificationType].message,
    data: {
      trip_id: tripData.trip_id,
      status: tripData.status,
      timestamp: new Date()
    }
  };
  
  // Save to database
  await Notifications.query().insert(notification);
  
  // Send via SQS
  const sqsClient = new SQSClient({ region: 'us-east-1' });
  await sqsClient.send(new SendMessageCommand({
    QueueUrl: config.aws.sqs.notificationQueue,
    MessageBody: JSON.stringify(notification)
  }));
};
```

## Error Handling

### Webhook Validation Errors
```javascript
describe('Webhook Validation', () => {
  it('should reject webhook with invalid signature', async () => {
    const webhook = mockRequest('accepted');
    const invalidSignature = 'invalid_signature';
    
    const response = await httpClient.post('/webhook/uber', webhook, {
      headers: { 'X-Uber-Signature': invalidSignature }
    });
    
    expect(response.status).to.equal(401);
    expect(response.data.error).to.include('Invalid signature');
  });
  
  it('should handle malformed webhook payload', async () => {
    const malformedPayload = { invalid: 'data' };
    const signature = generateWebhookSignature(malformedPayload, uberConfig.clientSecret);
    
    const response = await httpClient.post('/webhook/uber', malformedPayload, {
      headers: { 'X-Uber-Signature': signature }
    });
    
    expect(response.status).to.equal(400);
    expect(response.data.error).to.include('Invalid payload');
  });
});
```

### Database Transaction Safety
```javascript
const processWebhookSafely = async (webhook) => {
  const transaction = await RidehailTrips.knex.transaction();
  
  try {
    // Process webhook within transaction
    const result = await processWebhookEvent(webhook.event_type, webhook, transaction);
    
    // Log webhook processing
    await UberGuestRideLogs.query(transaction).insert({
      event_id: webhook.event_id,
      event_type: webhook.event_type,
      resource_id: webhook.meta.resource_id,
      status: webhook.meta.status,
      processed_at: new Date(),
      success: true
    });
    
    await transaction.commit();
    return result;
  } catch (error) {
    await transaction.rollback();
    
    // Log failure
    await UberGuestRideLogs.query().insert({
      event_id: webhook.event_id,
      event_type: webhook.event_type,
      error_message: error.message,
      processed_at: new Date(),
      success: false
    });
    
    throw error;
  }
};
```

## Performance Testing

### Concurrent Webhook Processing
```javascript
describe('Performance Tests', () => {
  it('should handle multiple concurrent webhooks', async () => {
    const webhooks = Array(10).fill().map((_, i) => 
      mockRequest('accepted', `request_${i}`)
    );
    
    const startTime = Date.now();
    
    const promises = webhooks.map(webhook => {
      const signature = generateWebhookSignature(webhook, uberConfig.clientSecret);
      return httpClient.post('/webhook/uber', webhook, {
        headers: { 'X-Uber-Signature': signature }
      });
    });
    
    const results = await Promise.all(promises);
    const endTime = Date.now();
    
    expect(endTime - startTime).to.be.lessThan(5000); // 5 seconds
    expect(results.every(r => r.status === 200)).to.be.true;
  });
});
```

## Quality Assurance

### Data Integrity
- **Signature Verification**: Ensure webhook authenticity
- **Status Consistency**: Maintain valid status transitions
- **Payment Accuracy**: Correct fare and receipt processing
- **Notification Delivery**: Reliable user communication

### Security Considerations
- **HMAC Validation**: Secure webhook signature verification
- **Request Validation**: Proper payload structure validation
- **Rate Limiting**: Protection against webhook flooding
- **Error Logging**: Comprehensive failure tracking

This comprehensive test suite ensures the Uber webhook integration provides reliable real-time updates, secure payment processing, and effective user communication while maintaining high performance and data integrity standards for ridehail operations.