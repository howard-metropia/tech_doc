# Escrow Service

## Overview

The Escrow service manages financial transactions for carpool services, handling payment holds, fee collection, and transaction reconciliation with comprehensive activity tracking and automatic balance management.

## Service Information

- **Service Name**: Escrow
- **File Path**: `/src/services/escrow.js`
- **Type**: Financial Escrow Service
- **Dependencies**: Wallet Service, MySQL, Error Handling

## Activity Types

### Escrow Activities (39 types)
- **INIT (0)**: Initial escrow setup
- **INC_FEE_RIDER (1-2)**: Rider/driver fee increases
- **INC_PREMIUM (3)**: Premium service charges
- **INC_RIDER_INVITE (4-5)**: Rider invitation handling
- **DEC_CARPOOL_CANCEL (7-9)**: Cancellation refunds
- **DEC_CARPOOL_REJECT (10-11)**: Rejection handling
- **DEC_PAY_TO_DRIVER (17)**: Driver payment release
- **DEC_FEE (18-19)**: Fee deductions
- **DEC_EXPIRED (22, 25)**: Expiration handling

### Activity Flow Types
- **Increase Activities (1-5, 12, 24)**: Money into escrow
- **Decrease Activities (6-11, 13-23, 25-26)**: Money out of escrow

## Core Functions

### get_carpool_fee()

Returns configured carpool transaction fees.

**Purpose**: Provides fee structure for carpool transactions
**Returns**: Object with driver fee, passenger fee, and premium rates

**Configuration**:
- **CARPOOL_DRIVER_TRANSACTION_FEE**: 0 (default)
- **CARPOOL_PASSENGER_TRANSACTION_FEE**: 0 (default)
- **CARPOOL_ERH_PREMIUM**: 2 (fixed premium)

### add_escrow(trx, userId, reservationId, offerId, tripId)

Creates new escrow record for carpool transaction.

**Purpose**: Establishes escrow account for transaction tracking
**Parameters**:
- `trx`: Database transaction object
- `userId`: User creating escrow
- `reservationId`: Associated reservation
- `offerId`: Carpool offer identifier
- `tripId`: Trip identifier

### add_escrow_detail(trx, userId, escrowId, activityType, fund, offerId, createdOn)

Processes escrow transactions with automatic wallet integration.

**Purpose**: Records escrow activities with wallet balance updates
**Parameters**:
- `escrowId`: Escrow account identifier
- `activityType`: Type of escrow activity (0-39)
- `fund`: Transaction amount (positive/negative)
- `offerId`: Associated offer
- `createdOn`: Transaction timestamp

**Transaction Processing**:
- **Increase Activities**: Deduct from user wallet (activity type 9)
- **Decrease Activities**: Add to user wallet (activity type 10)
- **Validation**: Ensures fund sign matches activity type

## Transaction Management

### Wallet Integration
- **Into Escrow (Type 9)**: User pays into escrow account
- **From Escrow (Type 10)**: User receives from escrow account
- **Balance Tracking**: Maintains accurate wallet balances
- **Reference Linking**: Links escrow and wallet transactions

### System Accounts
- **User Account**: Individual user wallet
- **Escrow Account (2001)**: Central escrow holding account
- **Metropia Budget (2000)**: System fee collection

### Fee Processing
- **trans_carpool_fee_metropia()**: Processes transaction fees to system account
- **Activity Type 8**: Carpool rider fee collection
- **System Coins**: Tracks fee revenue

## Maintenance Functions

### close_escrow(trx, userId, reservationId)

Closes escrow account and converts pending transactions.

**Purpose**: Finalizes escrow when carpool transaction completes
**Process**:
1. Finds all escrow details for user/reservation
2. Converts activity types 9→8 and 10→8
3. Updates escrow status to closed (2)

### clear_old_pending_pt(trx)

Cleans up old pending transactions.

**Purpose**: Converts abandoned escrow transactions to completed
**Criteria**:
- Transactions older than 24 hours
- Activity types 9 or 10 (pending escrow)
- Excludes blocked users

### fix_wrong_transit_ticket_type(trx)

Corrects incorrectly categorized transit transactions.

**Purpose**: Fixes activity type misclassification
**Process**:
1. Finds transactions with UUID-like notes
2. Verifies against bytemark_orders
3. Updates activity type from 8→11 for transit tickets

## Error Handling

### Validation Errors
- **Activity/Fund Mismatch**: MaasError 10001 for invalid combinations
- **Database Errors**: Comprehensive error logging
- **Transaction Integrity**: Rollback on failures

### Fund Validation
- **Increase Activities**: Must have positive fund amounts
- **Decrease Activities**: Must have zero or negative fund amounts
- **Error Responses**: Structured error codes and messages

## Database Schema

### Tables
- **escrow**: Main escrow accounts
- **escrow_detail/escrow_detail_upgrade**: Transaction details
- **points_transaction**: Wallet transaction records
- **system_coins_transaction**: Fee tracking

### Transaction Linking
- **escrow_id**: Links details to escrow account
- **transaction_id**: Links to wallet transactions
- **ref_transaction_id**: Bidirectional transaction references

## Integration Points

### Used By
- Carpool reservation systems
- Payment processing workflows
- Transaction reconciliation jobs
- Fee collection systems

### External Dependencies
- **Wallet Service**: Balance management and transactions
- **MySQL Portal**: Database operations
- **Error Handling**: Custom MaasError system
- **Logging**: Comprehensive operation tracking

## Security Features

### Transaction Integrity
- **Atomic Operations**: Database transactions ensure consistency
- **Balance Validation**: Prevents negative balances
- **Activity Validation**: Ensures proper fund flow direction
- **Reference Tracking**: Complete audit trail

### Error Recovery
- **Transaction Rollback**: Failed operations don't affect balances
- **Maintenance Jobs**: Automatic cleanup of orphaned transactions
- **Status Tracking**: Prevents duplicate processing

## Usage Guidelines

1. **Transaction Context**: Always use within database transactions
2. **Activity Types**: Use correct activity type for fund direction
3. **Error Handling**: Implement proper error recovery
4. **Maintenance**: Run cleanup jobs regularly
5. **Monitoring**: Track escrow account balances and aging

## Dependencies

- **Wallet Service**: Core financial transaction management
- **@maas/core**: Database connections and error handling
- **@maas/core/log**: Centralized logging system
- **Config**: Escrow configuration and fee settings