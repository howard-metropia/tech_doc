# Carpool Handler Module

## Overview

The `carpool_handler.py` module provides comprehensive business logic for managing carpool (duo) reservations, financial transactions, and trip lifecycle management within the Web2py portal application. This module handles complex carpool operations including matching, pricing, escrow management, and real-time trip coordination.

## Purpose

- **Carpool Lifecycle Management**: Handles complete carpool journey from reservation to completion
- **Financial Transaction Processing**: Manages escrow system, payments, and fee distribution
- **Conflict Resolution**: Prevents and resolves scheduling conflicts between reservations
- **Real-time Trip Coordination**: Supports live tracking and status updates during trips

## Dependencies

```python
import logging
import datetime
import trip_reservation as trvel
import carpool as duo
from decimal import Decimal
from datetime_utils import datetime_to_string, utcnow_to_tz
from gluon import current
from sqs_helper import send_sqs_task
```

## Module Structure

### Core Functions

**Conflict Management**
- `get_conflicting_reservation()` - Identifies scheduling conflicts
- `cancel_unpaired_conflict()` - Resolves unpaired carpool conflicts
- `cancel_paired()` - Handles matched carpool cancellations

**Financial Management**
- `_points_transaction()` - Processes point-based payments
- `add_escrow()` / `close_escrow()` - Manages escrow accounts
- `transfer_carpool_fee_driver()` - Handles driver payments
- `stripe_charge()` - Processes credit card payments

**Carpool Operations**
- `paired_partners()` - Retrieves carpool partner information
- `get_suggestion_carpool()` - Manages carpool suggestions
- `check_carpool_balance()` - Validates user payment capacity

## Conflict Management System

### get_conflicting_reservation()

Identifies existing reservations that conflict with a new carpool request.

#### Parameters
- `db`: Database connection object
- `user_id`: Integer user identifier
- `start_on`: Datetime start of time range
- `end_on`: Datetime end of time range

#### Logic Flow

**General Travel Conflicts**
```python
genral_travel_rows = db(
    (db.reservation.user_id == user_id) &
    db.reservation.travel_mode.belongs([
        define.DRIVING, define.PUBLIC_TRANSIT, define.WALKING, 
        define.BIKING, define.INTERMODAL, define.TRUCKING
    ]) &
    (db.reservation.status == define.RESERVATION_STATUS_RESERVED) &
    # Time overlap logic
).select(db.reservation.ALL)
```

**Carpool-Specific Conflicts**
```python
carpool_travel_rows = db(
    (db.reservation.user_id == user_id) &
    (db.reservation.travel_mode == define.DUO) &
    (db.reservation.status == define.RESERVATION_STATUS_MATCHED) &
    # Extended time window for carpool coordination
).select(db.reservation.ALL)
```

#### Return Format
```python
{
    'id': reservation_id,
    'travel_mode': travel_mode,
    'role': user_role,
    'origin': {
        'name': location_name,
        'address': full_address,
        'latitude': coordinate,
        'longitude': coordinate
    },
    'destination': {/* similar structure */},
    'started_on': start_datetime,
    'estimated_arrival_on': arrival_datetime
}
```

### cancel_unpaired_conflict()

Resolves conflicts by canceling unpaired carpool reservations.

#### Conflict Resolution Strategy

**Carpool Creator Cancellation**
- Cancels all pending applicants for the offer
- Updates status to `RESERVATION_STATUS_REPEALED`
- Notifies affected users

**Non-Creator Cancellation**
- Simple reservation deletion
- No cascade effects to other users

#### Offer ID Tracking
```python
conflict_offer_ids = []
for row in rows:
    if row.duo_reservation.offer_id:
        conflict_offer_ids.append(row.duo_reservation.offer_id)
```

## Financial Transaction System

### Points Transaction Framework

#### Dual Ledger Architecture

The system maintains both old and new transaction tables for gradual migration:

```python
doubles = {
    "targetTable": configuration.get('points_transaction.target_table', 'points_transaction'),
    "write": {
        "points_transaction": _write_old_points_transaction,
        "points_transaction_upgrade": _write_new_points_transaction
    },
    "update": {/* similar structure */},
    "find": {/* similar structure */}
}
```

#### System Account Management

```python
system_user_id = {
    'metropia_budget': 1000,
    'escrow': 2001,
    'incentive_engine': 2002,
    'stripe': 2100,
    'bytemark': 2101,
    'tango': 2102,        
}
```

### _points_transaction()

Core financial transaction processor with comprehensive error handling.

#### Transaction Flow

**Balance Validation**
```python
available_balance = _get_available_points(db, user_id)
balance = round(float(available_balance) + float(points), 2)
if balance < 0:
    raise InsufficientPoint
```

**Double Entry Bookkeeping**
```python
# Primary transaction
_id = _write_points_transaction(db, user_id=user_id, activity_id=activity_id, 
                               points=points, balance=balance)

# Corresponding entry for counterpart
_user_id = payer if payer != user_id else payee
_balance = round((float(_balance) - float(points)), 2)
_id1 = _write_points_transaction(db, user_id=_user_id, activity_id=activity_id, 
                                points=0-points, balance=_balance, ref_transaction_id=_id)
```

#### Auto-Refill System

**Trigger Conditions**
- User balance falls below configured threshold
- Auto-refill is enabled in user settings
- Valid payment method on file

**Processing Logic**
```python
if setting and setting.auto_refill and setting.refill_plan_id and (points < 0):
    if balance < setting.below_balance:
        charge = float(refill.points) - float(balance)
        charge_amount = int(round(charge * refill.display_rate))
        
        if exceed_coin_daily_limit(user_id, charge):
            # Pause auto-refill and notify user
            db(db.user_wallet.user_id == user_id).update(auto_refill=False)
            push_template_notification(notif.WALLET_AUTO_REFILL_PAUSED, [user_id])
```

### Escrow Management System

#### add_escrow()

Creates escrow accounts for carpool transactions.

```python
def add_escrow(db, user_id, reservation_id, offer_id=0, trip_id=0):
    row = db((db.escrow.user_id == user_id) & 
             (db.escrow.reservation_id == reservation_id)).select(db.escrow.ALL).first()
    if row:
        return row.id
    else:
        id = db.escrow.insert(user_id=user_id, reservation_id=reservation_id, 
                             offer_id=offer_id, trip_id=trip_id, status=1)
        return id
```

#### Escrow Activity Types

**Income Activities** (Funds INTO escrow)
- Activity types: 1, 2, 3, 4, 5, 12, 13, 24
- Deduct from user wallet, credit to escrow

**Outgoing Activities** (Funds FROM escrow)
- Activity types: 6, 7, 8, 9, 10, 11, 14-26
- Credit to user wallet, deduct from escrow

#### escrow_total()

Calculates current escrow balances with premium separation.

```python
def escrow_total(db, user_id, reservation_id):
    # Query all escrow transactions
    fund_row = db(/* escrow query */).select(/* fields */)
    
    total, premium, net = 0, 0, 0
    for r in fund_row:
        if r.activity_type in [PREMIUM_ACTIVITIES]:
            premium += float(r.fund)
        else:
            net += float(r.fund)
    
    return round(net + premium, 2), round(premium, 2), round(net, 2), has_premium
```

## Carpool Operations

### paired_partners()

Retrieves information about carpool partners for a given reservation.

#### Partner Data Structure

```python
data = {
    'offer_id': offer_id,
    'reservation_id': reservation_id,
    'role': user_role,
    'origin': {
        'name': origin_name,
        'address': origin_address,
        'access_latitude': access_lat,
        'access_longitude': access_lng,
        'latitude': lat,
        'longitude': lng
    },
    'destination': {/* similar structure */},
    'user': user_profile_data,  # if include_profile=True
    'price': calculated_price
}
```

#### Dynamic Pricing Integration

**Unit Price Calculation**
```python
if enable_unit_price == 'true' or enable_unit_price == True:
    total_price, unit_price = calculate_total_price_by_unit_price(
        self_reservation, partner_reservation, enable_unit_price)
    
    if self_reservation.role == trvel.ROLE_PASSENGER and total_price > 0:
        data['price'] = total_price + float(passenger_transaction_fee)
    elif self_reservation.role == trvel.ROLE_DRIVER and total_price > 0:
        data['price'] = max(0, total_price - float(driver_transaction_fee))
```

### get_suggestion_carpool()

Manages carpool suggestion system for matching drivers and passengers.

#### Suggestion Logic

**Query Active Suggestions**
```python
rows = db(
    (db.duo_reservation.offer_id == offer_id) &
    db.reservation.status.belongs([
        define.RESERVATION_STATUS_SEARCHING,
        define.RESERVATION_STATUS_CHOOSING,
        define.RESERVATION_STATUS_PENDING,
        define.RESERVATION_STATUS_SUGGESTION,
        define.RESERVATION_STATUS_MATCHED
    ])
).select(/* fields */)
```

**Response Format**
```python
{
    'offer_id': offer_id,
    'driver': {
        'user_id': driver_id,
        'started_on': start_time,
        'estimated_arrival_on': arrival_time,
        'origin': location_data,
        'destination': location_data,
        'price': driver_price
    },
    'passenger': {/* similar structure */}
}
```

## Payment Processing

### transfer_carpool_fee_driver()

Handles payment transfer from passenger to driver upon trip completion.

#### Payment Calculation Logic

```python
sum, p, n, erh = escrow_total(db, passenger_id, reservation_id)
fp = float(passenger_transaction_fee)  # Fee for passenger
fd = float(driver_transaction_fee)     # Fee for driver

if round(n, 2) > round((fp + fd), 2):
    pay = n - fp - fd  # Full amount minus both fees
    with_driver_fee = True
else:
    pay = n - fp       # Only deduct passenger fee
    with_driver_fee = False
```

#### Fee Distribution

**Passenger Transaction Fee**
```python
if fp > 0:
    db.escrow_detail.insert(escrow_id=escrow_row['id'], 
                           activity_type=trvel.ESCROW_ACTIVITY_DEC_FEE_RIDER,
                           fund=(0 - fp))
    trans_carpool_fee_metropia(db, passenger_id=passenger_id, 
                              activity_type=2, fee=fp, api_key=api_key)
```

**Driver Payment**
```python
balance, pt_id = _points_transaction(db, user_id=driver_id, activity_id=activity_id,
                                   points=pay, notify=False, api_key=api_key,
                                   payer=passenger_id, payee=driver_id)
```

### stripe_charge()

Processes credit card payments through Stripe integration.

#### Payment Processing

```python
def stripe_charge(amount, currency, points, user_id, transaction_token=None, 
                 customer_id=None, api_key=None):
    import stripe
    if api_key:
        stripe.api_key = api_key
        params = dict(
            amount=amount,
            currency=currency.lower(),
            description='Purchase %s coins' % points,
        )
        
        if customer_id:
            params['customer'] = customer_id
        else:
            params['source'] = transaction_token
```

#### Error Handling

**Stripe Error Management**
```python
except Exception as e:
    errorMsg = '%s' % e
    if errorMsg not in ['Your card has insufficient funds.', 
                       'Your card does not support this type of purchase.']:
        # Send Slack notification for unexpected errors
        slack_manager.send_vendor_failed_msg({
            'status': 'ERROR',
            'vendor': 'Stripe',
            'vendorApi': 'Charge.create',
            'originApi': '_points_transaction',
            'errorMsg': '%s' % e,
            'meta': json.dumps(params)
        })
```

## Enhanced Routing & Handling (ERH) Premium System

### pay_erh_premium()

Processes premium payments for enhanced routing services.

#### Premium Payment Logic

**In-Escrow Premium**
```python
if in_escrow:
    # Premium already held in escrow, just transfer to system
    ed_rows = db(/* query existing premium transaction */).first()
    if ed_rows:
        ed_rows.points_transaction.update_record(activity_type=8)
        db.escrow_detail.insert(escrow_id=escrow_row.id, 
                               activity_type=trvel.ESCROW_ACTIVITY_DEC_PREMIUM,
                               fund=0-premium)
```

**Direct Premium Payment**
```python
else:
    # Premium not in escrow, charge directly
    balance, pt_id = _points_transaction(db, user_id, 8, 0-premium, 
                                       notify=False, api_key=api_key,
                                       payer=user_id, payee=1000)
    db.system_coins_transaction.insert(activity_type=4, coins=premium,
                                      transaction_id=pt_id)
```

### return_erh_premium()

Handles premium refunds when enhanced routing is not used.

```python
def return_erh_premium(db, user_id, owner, other, premium, now, api_key=None):
    # Find existing premium transaction
    ed_rows = db(/* query premium escrow */).first()
    if ed_rows:
        ed_rows.points_transaction.update_record(activity_type=8)
    
    # Refund premium to user
    balance, pt_id = _points_transaction(db, user_id, 8, premium, 
                                       notify=False, api_key=api_key,
                                       payer=1000, payee=user_id)
```

## Cancellation Management

### cancel_paired()

Handles cancellation of matched carpool reservations.

#### Cancellation Logic

**Partner Notification**
```python
partners = db(/* query carpool partners */).select(/* fields */)
for partner in partners:
    notify_user_ids.append(partner.user_id)
    if partner.card_id:
        # From suggestion card - mark as cancelled
        partner.update_record(status=define.RESERVATION_STATUS_CANCELED_PASSIVE)
    else:
        # Regular reservation - return to searching
        partner.update_record(status=define.RESERVATION_STATUS_SEARCHING)
```

**Penalty System Integration**
```python
if row.reservation.status == define.RESERVATION_STATUS_MATCHED:
    # Apply penalty to canceling user
    db.penalty.update_or_insert(db.penalty.user_id == row.reservation.user_id,
                               user_id=row.reservation.user_id,
                               last_on=datetime.datetime.utcnow())
```

### Cancellation During Trip

#### cancel_carpool_return_passenger()

Handles in-trip cancellations with appropriate refund calculations.

**Status-Based Processing**
```python
if status in [
    trvel.DUO_REALTIME_STATUS_RUNNING_LATE,
    trvel.DUO_REALTIME_STATUS_PARTNER_RUNNING_LATE,
    trvel.DUO_REALTIME_STATUS_NO_SHOW_AND_END,
    trvel.DUO_REALTIME_STATUS_CHANGE_PLAN,
    trvel.DUO_REALTIME_STATUS_OTHER
]:
    # Process refund based on trip progress
    sum, p, n, erh = escrow_total(db, escrow_row.user_id, reservation_id)
    pay = n  # Return net amount
    if pay > 0:
        add_escrow_detail(db, escrow_row.user_id, escrow_row.id, 
                         activity_type, (0 - pay), offer_id)
```

## Real-time Trip Validation

### check_duo_realtime()

Validates completion of required carpool milestones.

```python
def check_duo_realtime(db, driver_trip_id):
    duo_realtime = db(db.duo_realtime.trip_id == driver_trip_id).select(db.duo_realtime.ALL)
    
    required_statuses = [
        trvel.DUO_REALTIME_STATUS_STARTED,
        trvel.DUO_REALTIME_STATUS_ARRIVE_PICKUP_POINT,
        trvel.DUO_REALTIME_STATUS_PICKUP_MANUALLY,
        trvel.DUO_REALTIME_STATUS_DROPOFF_MANUALLY
    ]
    
    # Check if all required statuses have been recorded
    completed_statuses = {status: False for status in required_statuses}
    for record in duo_realtime:
        if record.status in required_statuses:
            completed_statuses[record.status] = True
    
    return all(completed_statuses.values())
```

## Notification System Integration

### push_notification()

Sends point balance notifications to users via SQS.

```python
def push_notification(user_ids, points, activity_name):
    title = dict(en='Metropia')
    body = dict(en=('You got %s coins by %s.' % (points, activity_name)))
    
    send_sqs_task('cloud_message', {
        "user_list": user_ids,
        "notification_type": 1,
        "ended_on": ended_on.strftime("%Y-%m-%d %H:%M:%S"),
        "title": title,
        "body": body,
    })
```

## Error Handling and Logging

### Exception Classes

```python
class InsufficientPoint(Exception):
    pass
```

### Comprehensive Logging

```python
logger = logging.getLogger('carpool_handler')
logger.setLevel(logging.DEBUG)

# Example usage throughout module
logger.debug('[DUO] [ESCROW] add_escrow(db, user_id=%s, reservation_id=%s)' % 
            (user_id, reservation_id))
logger.info('[Strip] User(%s) auto-refill %s coins.' % (user_id, refill.points))
logger.error('[Stripe] Auto-refill failure reason: %s' % e)
```

## Security Considerations

### Input Validation

**User Blocking Checks**
```python
# is_blocked_user(user_id)  # Called before financial operations
driver_blocked = db((db.block_users.user_id == driver_id) & 
                   (db.block_users.is_deleted == 'F')).select(db.block_users.ALL).first()
```

**Daily Limit Enforcement**
```python
if exceed_coin_daily_limit(user_id, charge):
    db(db.user_wallet.user_id == user_id).update(auto_refill=False)
    push_template_notification(notif.WALLET_AUTO_REFILL_PAUSED, [user_id])
```

### Financial Security

**Transaction Atomicity**
- All financial operations wrapped in database transactions
- Rollback capabilities for failed operations
- Audit trail maintenance for all point movements

**Escrow Protection**
- Funds held in escrow until trip completion
- Automatic refund mechanisms for failed trips
- Multi-level approval for large transactions

## Performance Optimization

### Query Optimization

**Efficient Partner Queries**
```python
# Use aliases and joins for complex carpool queries
viewer = db.duo_reservation.with_alias('viewer')
partners = db(/* optimized query with joins */).select(/* specific fields */)
```

**Index-Friendly Queries**
- Queries designed to use database indexes effectively
- Minimal data transfer through field selection
- Proper use of groupby for aggregation

### Caching Strategy

**Configuration Caching**
```python
configuration = current.globalenv['configuration']  # Cached at module level
```

**Database Connection Reuse**
```python
db = current.db  # Reuse Web2py database connection
```

This carpool handler module provides a comprehensive foundation for managing complex carpool operations, from initial matching through trip completion and payment processing, while maintaining financial security and user experience quality.