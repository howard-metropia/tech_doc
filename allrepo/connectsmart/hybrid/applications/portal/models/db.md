# Portal Database Models - MaaS Data Architecture

## 🔍 Quick Summary (TL;DR)
Comprehensive database schema definition for Portal MaaS platform including user management, financial transactions, carpooling services, notifications, campaigns, and multi-modal transportation data with dual MySQL database architecture.

**Keywords**: `database-schema | mysql-models | web2py-dal | maas-database | user-wallet | carpooling-data | notification-system | financial-transactions`

**Use Cases**: MaaS data persistence, user account management, payment processing, carpooling coordination, notification delivery, campaign management

**Compatibility**: Web2py DAL, MySQL 5.7+, Python 2.7+, ConnectSmart platform

## ❓ Common Questions Quick Index
- Q: How is the database structured? → [Database Architecture](#database-architecture)
- Q: What are the main data models? → [Core Data Models](#core-data-models)
- Q: How does the wallet system work? → [Financial Models](#financial-models)
- Q: What carpooling data is stored? → [Carpooling Models](#carpooling-models)
- Q: How are notifications handled? → [Notification Models](#notification-models)
- Q: What's the dual database setup? → [Technical Specifications](#technical-specifications)
- Q: How do I access the database? → [Usage Methods](#usage-methods)
- Q: What external integrations exist? → [External Integrations](#external-integrations)

## 📋 Functionality Overview
**Non-technical**: Like a comprehensive filing system for a transportation company - stores everything from customer profiles and payment cards to trip records, carpooling matches, and notification preferences, organized across multiple specialized databases.

**Technical**: Complete data access layer (DAL) defining 50+ database tables across two MySQL databases (portal and admin) with comprehensive user management, financial transaction tracking, carpooling coordination, notification systems, and campaign management for MaaS platform operations.

**Business Value**: Provides robust data foundation for MaaS services enabling user account management, financial transactions, service delivery tracking, and business intelligence across all transportation modes and services.

**System Context**: Central data layer for ConnectSmart Portal connecting user interfaces, payment systems, transportation services, notification systems, and administrative tools through standardized database schemas.

## 🔧 Technical Specifications
- **File**: `portal/models/db.py` (869 lines)
- **Databases**: Dual MySQL setup (portal + admin)
- **Framework**: Web2py Data Abstraction Layer (DAL)
- **Tables**: 50+ tables across user, financial, transportation, and administrative domains
- **Authentication**: JWT-based with Web2py Auth integration
- **External APIs**: Stripe, Twilio, AWS S3, HERE Maps, Enterprise systems
- **Migration**: Configurable database migration support

### Database Configuration
```python
# Primary portal database
_db_uri = os.environ.get('MYSQL_PORTAL_URI') or configuration.get('db.uri')
db = DAL(_db_uri, pool_size=config.pool_size, migrate_enabled=True)

# Secondary admin database  
_db_uri1 = os.environ.get('MYSQL_ADMIN_URI') or configuration.get('db.uri1')
db1 = DAL(_db_uri1, pool_size=config.pool_size, migrate_enabled=True)
```

## 📝 Detailed Code Analysis

### Core Data Models

**User Management (auth_user extension)**:
```python
auth.settings.extra_fields['auth_user'] = [
    Field('common_email', type='string'),
    Field('phone_number', type='string'),
    Field('vehicle_type', type='string'),
    Field('device_token', type='string'),
    Field('facebook_id', type='string'),
    Field('enterprise_id', type='integer', default=0),
    # 40+ additional user profile fields
]
```

**Financial System**:
```python
# User wallet management
db.define_table('user_wallet',
    Field('user_id', 'integer', required=True),
    Field('balance', 'decimal(10,2)', default=0),
    Field('stripe_customer_id', 'string'),
    Field('auto_refill', 'boolean', default=0),
    Field('below_balance', 'integer', default=0)
)

# Transaction tracking with dual table support
db.define_table('points_transaction',
    Field('user_id', 'integer', required=True),
    Field('activity_type', db.activity_type),
    Field('points', 'decimal(10,2)', required=True),
    Field('balance', 'decimal(10,2)', required=True),
    Field('payer', 'integer', default=0),
    Field('payee', 'integer', default=0)
)
```

**Carpooling System**:
```python
# DUO carpooling groups and reservations
db.define_table('duo_group', table_class=duo.DuoGroupTable)
db.define_table('reservation', table_class=trvel.ReservationTable)
db.define_table('duo_reservation', table_class=trvel.DuoReservationTable)
db.define_table('duo_rating', table_class=trvel.DuoRatingTable)
```

**Notification System**:
```python
db.define_table('notification_type', table_class=NotificationTypeTable)
db.define_table('notification', table_class=NotificationTable)
db.define_table('notification_user', table_class=NotificationUserTable)
```

### External Service Integration Tables

**Payment Processing**:
- `wallet_user_cards` - Stripe card storage
- `wallet_user_transactions` - Payment transaction history
- `purchase_transaction` - Points purchase records
- `refill_plan` - Auto-refill configurations

**Communication Services**:
- `bytemark_tokens` - Transit ticket authentication
- `enterprise` - Corporate account integration
- `contact` - Emergency contact management

## 🚀 Usage Methods

### Database Connection Access
```python
from applications.portal.models.db import db, db1, auth

# Portal database operations
user = db.auth_user[user_id]
wallet = db(db.user_wallet.user_id == user_id).select().first()

# Admin database operations  
org = db1(db1.organization_settings.id == org_id).select().first()
```

### User Account Management
```python
# Create new user with extended fields
user_id = db.auth_user.insert(
    email='user@example.com',
    first_name='John',
    last_name='Doe',
    phone_number='+1234567890',
    device_token='fcm_token_123',
    enterprise_id=5
)

# Update user profile
db(db.auth_user.id == user_id).update(
    vehicle_type='sedan',
    vehicle_color='blue',
    home_latitude=37.7749,
    home_longitude=-122.4194
)
```

### Financial Operations
```python
# Create user wallet
db.user_wallet.insert(
    user_id=user_id,
    balance=0.00,
    auto_refill=True,
    below_balance=5,
    refill_plan_id=1
)

# Record transaction
db.points_transaction.insert(
    user_id=user_id,
    activity_type=2,  # Purchase
    points=10.00,
    balance=15.00,
    payer=2100,  # Stripe system user
    payee=user_id
)
```

### Carpooling Data Management
```python
# Create carpooling group
group_id = db.duo_group.insert(
    name='Morning Commute',
    creator_id=user_id,
    group_type_id=1,
    max_members=4
)

# Add reservation
reservation_id = db.reservation.insert(
    user_id=user_id,
    departure_time=datetime.utcnow(),
    origin_latitude=37.7749,
    origin_longitude=-122.4194,
    travel_mode=1  # Carpool
)
```

## 📊 Output Examples

**Database Connection Success**:
```
<DAL {
  'portal': <Database 'mysql://portal_db'>,
  'admin': <Database 'mysql://admin_db'>
}>
```

**User Query Result**:
```python
user = db.auth_user[123]
print(f"User: {user.first_name} {user.last_name}")
print(f"Email: {user.email}")
print(f"Enterprise: {user.enterprise_id}")
print(f"Vehicle: {user.vehicle_color} {user.vehicle_type}")
```

**Wallet Balance Query**:
```python
wallet = db(db.user_wallet.user_id == 123).select().first()
# Returns: <Row {'user_id': 123, 'balance': 25.50, 'auto_refill': True}>
```

**Transaction History**:
```sql
SELECT * FROM points_transaction 
WHERE user_id = 123 
ORDER BY created_on DESC LIMIT 10;
```

## ⚠️ Important Notes

### Security Considerations
- **JWT Authentication**: Secure token-based authentication with configurable expiration
- **Database Encryption**: MySQL connections use UTF8MB4 encoding
- **API Key Management**: External service credentials stored in configuration
- **User Privacy**: Personal data fields require proper access controls

### Performance Considerations
- **Connection Pooling**: Configurable database connection pools
- **Indexing Strategy**: Requires indexes on frequently queried fields (user_id, created_on)
- **Migration Management**: Controllable database schema migrations
- **Query Optimization**: Use DAL's built-in query optimization features

### Data Integrity
- **Foreign Keys**: Proper referential integrity between related tables
- **Constraints**: Required fields and data validation rules
- **Transaction Safety**: Use database transactions for multi-table operations
- **Backup Strategy**: Regular database backups essential for financial data

### Common Issues
- **Migration Conflicts**: Coordinate schema changes across environments
- **Connection Limits**: Monitor database connection pool usage
- **Encoding Issues**: Ensure UTF8MB4 support for international characters
- **Table Locks**: Avoid long-running transactions on high-traffic tables

## 🔗 Related File Links
- **Business Logic**: `/portal/models/common.py` (transaction processing)
- **Error Handling**: `/portal/models/error_code.py` (database error codes)
- **Notifications**: `/portal/models/notify.py` (notification data access)
- **External Modules**: `/carpool.py`, `/trip_reservation.py`, `/campaign.py`
- **Configuration**: `/private/appconfig.ini` (database credentials)
- **Helpers**: `/jwt_helper.py`, `/sqs_helper.py`

## 📈 Use Cases
- **User Onboarding**: Account creation with profile and preferences
- **Payment Processing**: Wallet management and transaction recording
- **Carpooling Coordination**: Group management and trip matching
- **Campaign Management**: Marketing campaign tracking and analytics
- **Notification Delivery**: Message queuing and delivery tracking
- **Enterprise Integration**: Corporate account and employee management
- **Analytics**: Data mining for business intelligence and reporting

## 🛠️ Improvement Suggestions
- **Read Replicas**: Add read-only database replicas for analytics queries
- **Sharding Strategy**: Implement user-based sharding for scalability
- **Caching Layer**: Add Redis caching for frequently accessed data
- **Audit Logging**: Implement comprehensive audit trail for financial operations
- **Performance Monitoring**: Add database performance monitoring and alerting
- **Data Archiving**: Implement data retention policies for historical records

## 🏷️ Document Tags
**Keywords**: database-schema, mysql, web2py-dal, user-management, financial-transactions, carpooling-data, notifications, campaign-management, maas-database

**Technical Tags**: `#database #mysql #web2py #dal #schema #user-management #payments #carpooling #notifications`

**Target Roles**: Database administrators (expert), Backend developers (intermediate), MaaS architects (advanced)

**Difficulty**: ⭐⭐⭐⭐ (Advanced) - Complex multi-database schema with extensive relationships

**Maintenance**: High - Critical data layer requiring careful schema evolution

**Business Criticality**: Critical - Core data foundation for entire MaaS platform

**Related Topics**: Database design, Data modeling, MySQL optimization, Web2py DAL, MaaS architecture