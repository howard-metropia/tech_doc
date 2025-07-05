# TSP Job Service: carpoolHandler.js

## Quick Summary

The `carpoolHandler.js` service manages complex carpool financial transactions, escrow operations, and reservation pairing within the ConnectSmart platform. It handles rider-driver payment processing, fee calculations, escrow fund management, and cancellation refunds with comprehensive support for unit pricing, transaction fees, and premium services.

## Technical Analysis

### Core Architecture

The service implements a sophisticated financial management system for carpool operations with the following key components:

- **Reservation Pairing**: Links driver and passenger reservations through duo_reservation relationships
- **Escrow Management**: Handles secure fund holding and release for carpool transactions
- **Fee Calculation**: Supports unit-based pricing with route distance calculations
- **Transaction Processing**: Manages payments, refunds, and fee distributions
- **Premium Services**: Handles ERH (Early Request Handling) premium features

### Key Functions

#### findPairedReservation(reservationId)
Core function for finding matched carpool partners:
```javascript
const partners = await knex('duo_reservation as A')
  .join('duo_reservation as B', 'B.offer_id', '=', 'A.offer_id')
  .join('reservation as R', 'R.id', '=', 'B.reservation_id')
  .where('A.reservation_id', '=', reservationId)
  .where('B.reservation_id', '!=', 'A.reservation_id')
  .whereIn('R.status', [
    reservationStatus.SEARCHING,
    reservationStatus.MATCHED,
    reservationStatus.STARTED,
  ]);
```

#### calculateTotalPriceByUnitPrice(owner, target)
Calculates carpool pricing based on unit rates and distance:
```javascript
if (enableUnitPrice) {
  if (owner.unit_price && owner.role === role.DRIVER) {
    unitPrice = Number(owner.unit_price);
    totalPrice = unitPrice * Number(target.route_meter);
  } else {
    unitPrice = Number(target.unit_price);
    totalPrice = unitPrice * Number(owner.route_meter);
  }
}
```

#### Escrow System Implementation

**escrowTotal(userId, reservationId)**: Calculates current escrow balances
```javascript
const fundRow = await knex('escrow as es')
  .join(escrowDetailTable, `esd.escrow_id`, '=', 'es.id')
  .where('es.user_id', '=', userId)
  .where('es.reservation_id', '=', reservationId);

// Separate premium from net funds
if ([
  escrowType.ESCROW_ACTIVITY_INC_PREMIUM,
  escrowType.ESCROW_ACTIVITY_DEC_PREMIUM_NOT_IN_DRIVER_ACCEPTED_INVITE,
  // ... other premium types
].indexOf(r.activity_type) > -1) {
  premium += Number(r.fund);
} else {
  net += Number(r.fund);
}
```

**addEscrowDetail(userId, escrowId, activityType, fund, offerId)**: Records escrow transactions
```javascript
// Credit transactions (increase escrow)
if ([1, 2, 3, 4, 5, 12, 13, 24].indexOf(activityType) > -1) {
  if (fund > 0) {
    const { _id } = await pointsTransaction(userId, 9, 0 - fund, '', false);
    await knex(escrowDetailTable).insert({
      escrow_id: escrowId,
      activity_type: activityType,
      fund,
      offer_id: offerId,
      transaction_id: _id,
    });
  }
}
```

### Financial Transaction Management

#### transferCarpoolFeeDriver()
Handles driver payment processing with fee deductions:
```javascript
const fp = parseFloat(passengerTransactionFee);
const fd = parseFloat(driverTransactionFee);
let withDriverFee = true;

if (Math.round(n * 100) / 100 > Math.round((fp + fd) * 100) / 100) {
  pay = n - fp - fd; // Deduct both fees
} else {
  pay = n - fp; // Only passenger fee if insufficient funds
  withDriverFee = false;
}
```

#### cancelCarpoolEscrowReturn()
Manages refund processing for cancellations:
```javascript
if (activityType === escrowType.ESCROW_ACTIVITY_DEC_CARPOOL_CANCEL_RIDER) {
  const pay = Math.round((escrowNet - fp) * 100) / 100;
  if (pay > 0) {
    await addEscrowDetail(userId, escrowRow.id, 
      escrowType.ESCROW_ACTIVITY_DEC_CARPOOL_CANCEL_RIDER, 
      0 - pay, offerId);
    await closeEscrow(escrowRow.id);
  }
}
```

## Usage/Integration

### Typical Workflow

1. **Reservation Matching**: Find paired reservations using `findPairedReservation()`
2. **Price Calculation**: Calculate costs with `calculateTotalPriceByUnitPrice()`
3. **Escrow Setup**: Initialize escrow with `addEscrowDetail()`
4. **Trip Completion**: Process payment with `transferCarpoolFeeDriver()`
5. **Escrow Closure**: Finalize with `closeEscrow()`

### Integration with Job Scheduler
```javascript
// Called by carpool processing jobs
const carpoolHandler = require('./carpoolHandler');

// Process completed trip
const payment = await carpoolHandler.transferCarpoolFeeDriver(
  driverId, passengerId, tripId, driverFee, passengerFee
);

// Handle cancellation
await carpoolHandler.cancelCarpoolEscrowReturn(
  reservationId, escrowType.ESCROW_ACTIVITY_DEC_CARPOOL_CANCEL_RIDER, offerId
);
```

### Error Handling and Logging
```javascript
try {
  await rejectInviteEscrowProcess(owner, partners);
} catch (e) {
  logger.warn(`[rejectInviteEscrowProcess] error: ${e.message}`);
  logger.debug(`[rejectInviteEscrowProcess] stack: ${e.stack}`);
  throw e;
}
```

## Dependencies

### External Packages
- `@maas/core/mysql`: Database connectivity for portal database
- `config`: Configuration management for fees and pricing
- `@maas/core/log`: Centralized logging system

### Internal Services
- `@app/src/static/defines`: Status constants and enums
- `@app/src/services/wallet`: Points transaction and wallet management

### Configuration Dependencies
```javascript
config.portal = {
  duo: {
    enableUnitPrice: 'true' // Enable distance-based pricing
  },
  escrow: {
    passengerTransactionFee: 0.50, // Passenger fee amount
    driverTransactionFee: 0.25     // Driver fee amount
  }
}
```

### Database Schema Dependencies
- **reservation**: Carpool reservation records
- **duo_reservation**: Pairing relationships
- **escrow**: Fund holding accounts
- **escrow_detail/escrow_detail_upgrade**: Transaction history
- **points_transaction/points_transaction_upgrade**: Point movements
- **match_statistic**: Matching statistics

## Code Examples

### Basic Reservation Pairing
```javascript
const { findPairedReservation } = require('./carpoolHandler');

// Find all paired reservations for a given reservation
const [partners, owner] = await findPairedReservation(reservationId);
console.log(`Found ${partners.length} partners for reservation ${reservationId}`);
```

### Price Calculation
```javascript
const { calculateTotalPriceByUnitPrice } = require('./carpoolHandler');

const owner = { unit_price: 0.25, role: 1, route_meter: 5000 }; // Driver
const target = { unit_price: null, role: 2, route_meter: 4800 }; // Passenger

const { totalPrice, unitPrice } = await calculateTotalPriceByUnitPrice(owner, target);
console.log(`Total price: $${totalPrice} at $${unitPrice}/meter`);
```

### Escrow Operations
```javascript
const { escrowTotal, addEscrowDetail } = require('./carpoolHandler');

// Check current escrow balance
const { currentEscrow, currentPremium, escrowNet } = await escrowTotal(userId, reservationId);

// Add funds to escrow
await addEscrowDetail(
  userId,
  escrowId,
  escrowType.ESCROW_ACTIVITY_INC_CARPOOL_ACCEPT_BY_RIDER,
  15.50, // Amount
  offerId
);
```

### Payment Processing
```javascript
const { transferCarpoolFeeDriver } = require('./carpoolHandler');

// Process driver payment after trip completion
const paymentAmount = await transferCarpoolFeeDriver(
  12345, // driverId
  67890, // passengerId
  54321, // tripId
  0.25,  // driverTransactionFee
  0.50   // passengerTransactionFee
);

console.log(`Driver paid: $${paymentAmount}`);
```

### Cancellation Handling
```javascript
const { cancelCarpoolEscrowReturn } = require('./carpoolHandler');

// Process rider cancellation refund
await cancelCarpoolEscrowReturn(
  reservationId,
  escrowType.ESCROW_ACTIVITY_DEC_CARPOOL_CANCEL_RIDER,
  offerId
);
```

The carpoolHandler service provides a comprehensive financial management system for carpool operations, ensuring secure fund handling, accurate fee calculations, and proper refund processing within the ConnectSmart platform's mobility ecosystem.