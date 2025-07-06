# Wallet Service

## Overview

The Wallet service manages comprehensive digital wallet functionality including coin transactions, token operations, Stripe payments, auto-refill capabilities, and transaction tracking across multiple payment systems.

## Service Information

- **Service Name**: Wallet
- **File Path**: `/src/services/wallet.js`
- **Type**: Financial Transaction Service
- **Dependencies**: Stripe, MySQL, Moment.js, Notification Service

## Core Functions

### pointsTransaction(userId, activityType, points, note, notify, time, payer, payee)

Handles all coin-based transactions with automatic refill support.

**Purpose**: Core transaction processing with balance management
**Parameters**:
- `userId` (number): User performing transaction
- `activityType` (number): Transaction type (1-18)
- `points` (number): Point amount (positive/negative)
- `note` (string): Transaction description
- `notify` (boolean): Send refill notifications
- `time` (string): Transaction timestamp
- `payer/payee` (number): Transaction parties

**Returns**: Object with balance and transaction ID

### getUserWallet(userId)

Retrieves comprehensive user wallet information.

**Purpose**: Fetches wallet balance, settings, and refill configuration
**Returns**: Wallet object with balance, auto-refill settings, and payment plans

### tokenTransaction(userId, activityType, tokens, tokenId, note)

Manages token-based transactions for transit agencies.

**Purpose**: Processes agency token usage and validation
**Returns**: Token balance and transaction ID

## Activity Types

### Payment Categories
- **Adjustment (1)**: Manual coin adjustments
- **Purchase (2)**: Stripe coin purchases
- **Redemption (3)**: Gift card redemptions
- **Promotion (4)**: Promotional coin distribution
- **Auto-refill (5)**: Automatic balance top-ups
- **Incentive (6)**: Reward system payments
- **Carpool (7-10)**: Driver/rider payments and escrow
- **Transit (11)**: Transit ticket purchases
- **Ridehail (16,18)**: Uber fare payments and benefits

### System Accounts
- **Metropia Budget (2000)**: General adjustments
- **Escrow (2001)**: Carpool transaction holding
- **Incentive Engine (2002)**: Reward distributions
- **Stripe (2100)**: Payment processing
- **Bytemark (2101)**: Transit payments
- **TANGO (2102)**: Gift card redemptions
- **Uber (2107)**: Ridehail services

## Auto-Refill System

### Trigger Conditions
- Auto-refill enabled on user wallet
- Current balance < configured threshold
- Negative transaction occurring
- Daily purchase limit not exceeded

### Stripe Integration
- Customer ID validation
- Payment method charging
- Transaction fee handling
- Purchase limit enforcement

### Safety Features
- **Daily Limits**: Configurable purchase limits (default 200 coins)
- **Auto-pause**: Disables refill on limit exceeded
- **Notifications**: Success/failure notifications
- **Error Handling**: Graceful payment failures

## Token Management

### Token Operations
- **Balance Checking**: Current token balances by campaign
- **Expiration Validation**: Ensures tokens not expired
- **Availability Queries**: Active tokens for payment options
- **Transaction Recording**: Token usage tracking

### Campaign Integration
- **Agency Association**: Links tokens to transit agencies
- **Expiration Management**: Handles token lifecycle
- **Balance Calculations**: Aggregates token transactions

## Database Schema

### Transaction Tables
- **points_transaction/points_transaction_upgrade**: Coin transactions
- **token_transaction**: Agency token transactions
- **purchase_transaction**: Stripe payment records
- **user_wallet**: User balance and settings
- **refill_plan**: Auto-refill configurations

### Dual Schema Support
- Supports both legacy and upgrade transaction schemas
- Dynamic table selection based on configuration
- Consistent API across schema versions

## Stripe Payment Processing

### Payment Flow
1. Customer validation
2. Charge creation with description
3. Success/failure handling
4. Transaction recording
5. Balance updates

### Error Handling
- Missing API key detection
- Customer ID validation
- Charge failure management
- Comprehensive logging

## Security Features

### Transaction Validation
- Balance sufficiency checks
- System account privilege handling
- Double-entry bookkeeping
- Reference transaction linking

### Daily Limits
- Purchase amount tracking
- 24-hour rolling windows
- Automatic limit enforcement
- Suspicious activity detection

## Performance Optimization

### Database Transactions
- Atomic multi-table updates
- Efficient balance calculations
- Minimal lock duration
- Error rollback capability

### Query Efficiency
- Indexed lookups by user ID
- Aggregated balance calculations
- Optimized join operations
- Cached wallet configurations

## Integration Points

### Used By
- Payment processing systems
- Transit ticket purchasing
- Carpool transaction management
- Reward and incentive systems
- Auto-refill scheduling

### External Dependencies
- **Stripe API**: Payment processing
- **MySQL**: Transaction storage
- **Notification Service**: User notifications
- **Error Handling**: Custom error codes

## Error Handling

### Transaction Errors
- Insufficient balance detection
- Token expiration validation
- Payment processing failures
- System account validation

### Recovery Mechanisms
- Auto-refill pause on limits
- Graceful payment failures
- Transaction rollback capability
- Comprehensive error logging

## Usage Guidelines

1. **Balance Checks**: Always verify sufficient funds
2. **Transaction Logging**: Maintain detailed audit trails
3. **Auto-refill**: Monitor daily limits and user preferences
4. **Token Validation**: Check expiration before transactions
5. **Error Handling**: Implement proper fallback mechanisms

## Dependencies

- **Stripe**: Payment processing
- **@maas/core/mysql**: Database connections
- **@maas/core/log**: Centralized logging
- **Moment.js**: Date/time manipulation
- **Send Notification Service**: User notifications
- **Config**: Stripe and database configuration