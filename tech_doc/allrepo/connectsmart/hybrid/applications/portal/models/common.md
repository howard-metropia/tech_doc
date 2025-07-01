# Portal Common Models - MaaS Business Logic

## 🔍 Quick Summary (TL;DR)
Core business logic module for Portal MaaS platform providing points transaction system, wallet management, payment processing with Stripe, and notification services for carpooling and transportation services.

**Keywords**: `points-transaction | wallet-management | stripe-payment | maas-business-logic | carpooling-payments | auto-refill | transaction-ledger | notification-system`

**Use Cases**: Digital wallet operations, carpooling payment processing, points earning and redemption, auto-refill functionality, payment validation

**Compatibility**: Python 2.7+, Web2py framework, Stripe API, MySQL database, SQS messaging

## ❓ Common Questions Quick Index
- Q: How do I process points transactions? → [Usage Methods](#usage-methods)
- Q: What is the double-ledger system? → [Detailed Code Analysis](#detailed-code-analysis)
- Q: How does auto-refill work? → [Auto-Refill System](#auto-refill-system)
- Q: What payment methods are supported? → [Payment Processing](#payment-processing)
- Q: How are carpooling payments handled? → [Carpooling Payments](#carpooling-payments)
- Q: How do I check user balance? → [Balance Management](#balance-management)
- Q: What happens when points are insufficient? → [Error Handling](#error-handling)
- Q: How are notifications sent? → [Notification System](#notification-system)

## 📋 Functionality Overview
**Non-technical**: Like a digital bank for transportation services - manages your coins/points, automatically tops up your account when low, processes payments for rides, and sends you notifications about your transactions and carpooling activities.

**Technical**: Comprehensive financial transaction system implementing double-entry bookkeeping for points/coins management, integrated with Stripe payment processing, auto-refill functionality, and SQS-based notification system for MaaS platform operations.

**Business Value**: Enables monetization of MaaS services through digital wallet system, supports carpooling revenue sharing, provides automated payment processing, and ensures financial transaction integrity.

**System Context**: Core financial engine for ConnectSmart Portal, interfacing with payment providers, notification systems, and transportation services to handle all monetary transactions within the MaaS ecosystem.

## 🔧 Technical Specifications
- **File**: `portal/models/common.py` (421 lines)
- **Dependencies**: Web2py DAL, Stripe API, SQS helper, datetime, logging
- **Database**: MySQL (points_transaction tables), MongoDB (caching)
- **External APIs**: Stripe payments, SQS messaging, Slack notifications
- **Configuration**: AppConfig for API keys and settings
- **Transaction System**: Double-entry ledger with payer/payee tracking

## 📝 Detailed Code Analysis

### Core Functions

**Points Transaction System**:
```python
def points_transaction(user_id, activity_id, points, note=None, notify=True):
    """
    Main transaction processor implementing double-entry bookkeeping
    - Validates sufficient balance
    - Creates paired transactions for payer/payee
    - Updates user wallet balance
    - Triggers auto-refill if configured
    """
```

**Balance Management**:
```python
def get_available_points(user_id):
    """Returns user's current point balance from wallet"""
    row = db(db.user_wallet.user_id == user_id).select().first()
    return round(float(row.balance), 2) if row else 0
```

**Payer/Payee Calculation**:
```python
def _calc_payer_payee(user_id, activity_id, points):
    """
    Determines transaction counterparty based on activity type:
    - Activity 1: Coin adjustment (system budget)
    - Activity 2: Purchase (Stripe)
    - Activity 6: Incentive (incentive engine)
    - Activity 7-8: Carpooling (escrow system)
    """
```

### Auto-Refill System
Sophisticated automatic payment system that:
- Monitors user balance against threshold
- Validates daily purchase limits
- Processes Stripe charges automatically
- Handles failed payments gracefully
- Pauses auto-refill on suspicious activity

### Payment Processing
Stripe integration supporting:
- Customer creation and management
- Card tokenization and storage
- Charge processing with retry logic
- Error handling and reporting
- Slack notification for failed transactions

## 🚀 Usage Methods

### Basic Points Transaction
```python
from applications.portal.models.common import points_transaction

# Add points (positive value)
balance, tx_id = points_transaction(
    user_id=123,
    activity_id=6,  # Incentive
    points=10.50,
    note="Trip completion bonus"
)

# Deduct points (negative value)  
balance, tx_id = points_transaction(
    user_id=123,
    activity_id=11,  # Transit ticket
    points=-5.00,
    note="Bus ticket purchase"
)
```

### Check User Balance
```python
from applications.portal.models.common import get_available_points

user_balance = get_available_points(user_id=123)
print(f"Available balance: ${user_balance}")
```

### Stripe Payment Processing
```python
from applications.portal.models.common import stripe_charge

success, charge_result = stripe_charge(
    amount=1000,  # cents
    currency='usd',
    points=10.0,
    user_id=123,
    customer_id='cus_stripe123'
)
```

### Field Validation
```python
from applications.portal.models.common import verify_required_fields

required = ['email', 'user.profile.name', 'payment.amount']
data = {'email': 'test@example.com', 'user': {'profile': {'name': 'John'}}}
is_valid = verify_required_fields(required, data)
```

## 📊 Output Examples

**Successful Transaction**:
```python
balance, tx_id = points_transaction(123, 6, 10.0, "Bonus")
# Returns: (25.50, 15847)  # New balance and transaction ID
```

**Auto-Refill Trigger**:
```
[INFO] User(123) balance (2.50) below threshold (5.00)
[INFO] [Stripe] User(123) auto-refill 10.0 coins
[INFO] Auto-refill completed: $10.0 deposited
```

**Insufficient Balance Error**:
```python
try:
    points_transaction(123, 11, -50.0)  # User only has 25.50
except InsufficientPoint:
    print("Transaction failed: Insufficient balance")
```

**Stripe Charge Response**:
```json
{
  "id": "ch_1234567890",
  "status": "succeeded",
  "amount": 1000,
  "currency": "usd",
  "balance_transaction": "txn_987654321"
}
```

## ⚠️ Important Notes

### Security Considerations
- **API Key Management**: Stripe keys stored in configuration, not hardcoded
- **Transaction Integrity**: Double-entry system prevents balance corruption
- **Fraud Prevention**: Daily purchase limits and suspicious activity detection
- **User Blocking**: Automatic blocking for users with suspended accounts

### Performance Considerations
- **Database Optimization**: Efficient queries with proper indexing needed
- **Transaction Atomicity**: Uses database transactions for consistency
- **Rate Limiting**: Built-in daily purchase limits (200 coins default)
- **Monitoring**: Slack integration for payment failures

### Common Issues
- **Stripe API Errors**: Network timeouts, card failures, insufficient funds
- **Auto-Refill Loops**: Prevented by balance threshold checks
- **Timezone Issues**: All timestamps use UTC
- **Database Migration**: Supports dual table structure for upgrades

## 🔗 Related File Links
- **Database Schema**: `/portal/models/db.py` (wallet tables, transaction schemas)
- **Error Codes**: `/portal/models/error_code.py` (financial error constants)
- **Notifications**: `/portal/models/notify.py` (transaction notifications)
- **SQS Helper**: `/sqs_helper.py` (async notification processing)
- **JWT Helper**: `/jwt_helper.py` (authentication tokens)
- **Slack Helper**: `/slack_helper.py` (error reporting)

## 📈 Use Cases
- **MaaS Monetization**: Revenue collection from transportation services
- **Carpooling Payments**: Driver-rider payment processing and escrow
- **Loyalty Programs**: Points earning and redemption system
- **Subscription Services**: Auto-refill for recurring transportation costs
- **Gift Cards**: Third-party reward redemption through Tango integration
- **Enterprise Solutions**: Corporate account management and billing

## 🛠️ Improvement Suggestions
- **Async Processing**: Move heavy operations to background tasks
- **Caching Layer**: Add Redis for frequent balance queries
- **Audit Trail**: Enhance transaction logging with more metadata
- **Currency Support**: Multi-currency transaction handling
- **Performance Monitoring**: Add detailed transaction timing metrics
- **Testing Framework**: Comprehensive unit tests for edge cases

## 🏷️ Document Tags
**Keywords**: points-transaction, wallet-management, stripe-payments, auto-refill, carpooling-payments, double-ledger, maas-financial-system, payment-processing

**Technical Tags**: `#payments #stripe #wallet #transactions #maas #carpooling #auto-refill #financial-system`

**Target Roles**: Backend developers (intermediate), Payment system engineers (advanced), MaaS developers (expert)

**Difficulty**: ⭐⭐⭐ (Complex) - Financial system with multiple integrations

**Maintenance**: High - Critical payment processing system requiring constant monitoring

**Business Criticality**: Critical - Core revenue and payment processing system

**Related Topics**: Digital wallets, Payment processing, Double-entry bookkeeping, MaaS monetization, Financial transactions