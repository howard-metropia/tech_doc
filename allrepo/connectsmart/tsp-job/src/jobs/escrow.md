# Escrow Job

## Overview
Complex financial escrow management job that processes carpool payments, handles fund transfers between drivers and passengers, and manages escrow closures with comprehensive transaction tracking.

## File Location
`/src/jobs/escrow.js`

## Dependencies
- `@maas/core/mysql` - MySQL database connection
- `@app/src/services/escrow` - Escrow service operations
- `@maas/core/log` - Logging framework
- `@app/src/services/sendNotification` - Push notification service
- `@maas/core` - MaasError handling
- `@app/src/services/wallet` - Wallet and transaction services
- `moment-timezone` - Date/time manipulation

## Job Configuration

### Inputs
```javascript
inputs: {}
```
No input parameters required.

### Timeout Configuration
```javascript
const timeout = 2; // 2 hours timeout for escrow processing
```

## Core Escrow Processing Logic

### Main Processing Query
```sql
select ES.id as es_id, RE.id as re_id, ES.status as escrow_status, 
       RE.status as reservation_status, RE.started_on, RE.estimated_arrival_on, 
       RE.overlap_off 
from reservation RE
join escrow ES on ES.reservation_id = RE.id
where ES.status < 2 and RE.status > 0
```

### Processing Decision Tree
1. **Timeout Check**: If `now - targetTime > 2 hours`
   - **Reservation not started** (`status < 60`): Close and return funds
   - **Reservation started**: Validate duo result and transfer or return

2. **Within Timeout**: Validate duo result immediately
   - **Valid result**: Close and transfer to driver
   - **Invalid result**: Close and return to passenger

## Core Functions

### 1. isDuoResultValid(reservationId)
**Purpose**: Validates carpool completion status
**Returns**:
- `0`: Return after 24 hours (default)
- `1`: Pay immediately (validated and confirmed)
- `2`: Pay after 24 hours (status complete but pending)
- `3`: Return immediately (passenger confirmed NOT dropped off)

### 2. closeAndTransfer(escrowId, offerId)
**Purpose**: Transfers funds to driver after successful carpool
**Process**:
- Calculates fees (passenger + driver transaction fees)
- Transfers remaining amount to driver wallet
- Records escrow details and transactions
- Sends notifications to both parties

### 3. closeAndReturn(escrowId, reId)
**Purpose**: Returns funds to passenger for failed/expired carpool
**Process**:
- Returns chip-in funds to passenger
- Returns premium fees if applicable
- Records return transactions
- Handles both positive and negative balances

### 4. closeEscrow(escrowId)
**Purpose**: Finalizes escrow closure
**Process**:
- Updates transaction activity types to "completed"
- Sets escrow status to 2 (closed)
- Ensures data consistency

## Fee Structure

### Transaction Fees
```javascript
const fees = EscrowService.get_carpool_fee();
const fp = fees.CARPOOL_PASSENGER_TRANSACTION_FEE;
const fd = fees.CARPOOL_DRIVER_TRANSACTION_FEE;
```

### Payment Calculation
```javascript
const pay = sum - parseFloat(fp) - parseFloat(fd);
```
Driver receives: Total escrow - passenger fee - driver fee

## Notification System

### Transfer Notifications
- **Driver**: "You've received {amount} Coins from your carpool passenger"
- **Passenger**: "Your Chip-In of {amount} Coins has been paid to your driver"

### Validation Failure Notifications
- **Driver**: "Because we could not confirm that your passenger was onboard, no Chip-In was paid"
- **Passenger**: "Because we could not confirm that you were onboard, no Chip-In was paid"

### Multi-language Support
- English (en-us)
- Traditional Chinese (zh-tw)
- Spanish (es)
- Vietnamese (vi)

## Database Tables Involved

### Primary Tables
- `escrow` - Main escrow records
- `escrow_detail` - Detailed transaction logs
- `reservation` - Carpool reservations
- `trip` - Trip records
- `duo_validated_result` - Carpool validation results
- `duo_realtime` - Real-time carpool status
- `user_wallet` - User wallet balances
- `points_transaction` - Transaction history

### Activity Types
- `7`: Standard payment to driver
- `8`: Completed transaction
- `10`: Payment to blocked driver
- `16`: Premium return
- `17`: Payment from escrow

## Error Handling

### Transaction Safety
- All database operations wrapped in transactions
- Step-by-step error tracking with rollback capability
- Comprehensive error logging with context

### Recovery Mechanisms
- Graceful handling of missing data
- Validation of user accounts and balances
- Proper handling of blocked users

## Additional Services

### EscrowService Integration
- `clear_old_pending_pt()`: Cleans up old pending transactions
- `fix_wrong_transit_ticket_type()`: Fixes ticket type mismatches
- `fixPaymentStatus()`: Corrects payment status inconsistencies

### Payment Status Fixes
- Updates validation status for expired successful trips
- Corrects payment status for failed validations
- Ensures data consistency across validation tables

## Performance Considerations
- Processes multiple reservations in sequential order
- Uses database transactions for consistency
- Implements timeout-based processing
- Efficient SQL queries with proper joins

## Security Features
- Validates user permissions before transfers
- Checks for blocked users before payments
- Maintains audit trail of all transactions
- Prevents duplicate processing

## Related Components
- Carpool validation system
- User wallet management
- Push notification service
- Financial transaction tracking
- Multi-language notification system

## Schedule Context
Typically scheduled to run frequently (every few minutes) to ensure timely processing of carpool payments and escrow closures.