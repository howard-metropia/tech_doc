# Routes.py - Web2py URL Routing Configuration

**File:** `/home/datavan/METROPIA/metro_combine/allrepo/connectsmart/hybrid/routes.py`  
**Type:** Web2py URL Routing Configuration  
**Framework:** Web2py  
**Purpose:** RESTful API route mapping and URL rewriting for MaaS platform endpoints

## Overview

This file defines the URL routing configuration for the Web2py-based hybrid portal application. It implements a comprehensive RESTful API routing system that maps clean, semantic URLs to Web2py controller/function endpoints. The configuration handles bidirectional URL rewriting, enabling both incoming request routing and outgoing URL generation.

## Architecture

### Routing Pattern
The routing system follows a tuple-based mapping structure:
```python
routes_in = (
    ('/api/v1/endpoint', '/portal/controller/function.json'),
    ('/api/v1/endpoint/$param', '/portal/controller/function.json/$param'),
)
```

### URL Structure
- **Incoming URLs**: Clean RESTful API endpoints (`/api/v1/...`)
- **Internal Routes**: Web2py MVC pattern (`/portal/controller/function.json`)
- **Response Format**: JSON-based API responses (`.json` extension)

## Route Categories

### 1. App Update Management
```python
('/', '/portal/app_version/index'),
('/api/v1/app_version/$os', '/portal/app_version/latest.json/$os'),
```
- **Root Route**: Application version index page
- **Version Check**: OS-specific app version retrieval
- **Parameters**: `$os` - Operating system identifier (iOS, Android)

### 2. Authentication & Security
```python
('/api/v1/register', '/portal/user/register.json'),
('/api/v1/login', '/portal/user/login.json'),
('/api/v1/openid_login/$type', '/portal/user/openid_login.json/$type'),
('/api/v1/logout', '/portal/user/logout.json'),
('/api/v1/forget_password', '/portal/user/forget_password.json'),
('/api/v1/reset_password', '/portal/user/forget_password.json/reset'),
('/api/v1/change_password', '/portal/user/change_password.json'),
```
- **User Registration**: Account creation and validation
- **Authentication**: Login/logout with multiple methods
- **OpenID Integration**: Third-party authentication support
- **Password Management**: Reset, change, and recovery functions

### 3. Account Verification
```python
('/api/v1/verify_registration_code', '/portal/user/verify_registration_code.json'),
('/api/v1/activation', '/portal/user/activation.json'),
('/api/v1/resend_activation_code', '/portal/user/activation.json/resend_code'),
('/api/v1/verify_phone', '/portal/user/verify_phone.json'),
('/api/v1/resend_phone_code', '/portal/user/verify_phone.json/resend_code'),
```
- **Multi-factor Verification**: Email and phone verification
- **Code Management**: Resend and validation workflows
- **Account Activation**: User account status management

### 4. User Profile Management
```python
('/api/v1/profile', '/portal/user/profile.json'),
('/api/v1/change_openid', '/portal/user/change_openid.json'),
('/api/v1/contact', '/portal/user/contact.json'),
('/api/v1/contact/$id', '/portal/user/contact.json/$id'),
```
- **Profile Operations**: CRUD operations for user profiles
- **Contact Management**: User contact information handling
- **OpenID Management**: Third-party account linking

### 5. Enterprise Features
```python
('/api/v1/setting_carpool_email', '/portal/user/verify_carpool_email.json'),
('/api/v1/enterprise/delete', '/portal/telework/enterprise.json'),
('/api/v1/verify_carpool_email.html', '/portal/user/verify_carpool_email.html'),
('/api/v1/telework', '/portal/telework/employee.json'),
('/api/v1/telework/search', '/portal/telework/search.json'),
```
- **Corporate Integration**: Enterprise user management
- **Telework Support**: Remote work coordination
- **Email Verification**: Corporate email validation

### 6. Favorites & Preferences
```python
('/api/v1/favorites', '/portal/user/favorites.json'),
('/api/v1/favorites/$id', '/portal/user/favorites.json/$id'),
('/api/v1/preference', '/portal/preference/setting.json'),
('/api/v1/preference_default', '/portal/preference/default.json'),
```
- **Location Favorites**: Saved locations management
- **User Preferences**: Application settings and defaults
- **RESTful CRUD**: Create, read, update, delete operations

### 7. Communication Services
```python
('/api/v1/call_token', '/portal/twilio_server/token.json'),
('/api/v1/make_call', '/portal/twilio_server/make_call.xml'),
('/api/v1/blacklist', '/portal/blacklist/blacklist.json'),
('/api/v1/blacklist/$id', '/portal/blacklist/blacklist.json/$id'),
```
- **VoIP Integration**: Twilio-based calling features
- **User Blocking**: Blacklist management for safety
- **Communication Control**: Call token generation

### 8. Group Management (DUO)
```python
('/api/v1/duo_group', '/portal/duo_group/group.json'),
('/api/v1/duo_group/search', '/portal/duo_group/search.json'),
('/api/v1/duo_group/member', '/portal/duo_group/members.json'),
('/api/v1/member_profile', '/portal/duo_group/member_profile.json'),
('/api/v1/duo_group/accept_user', '/portal/duo_group/accept_user.json'),
('/api/v1/duo_group/join', '/portal/duo_group/join.json'),
('/api/v1/duo_group/leave', '/portal/duo_group/leave.json'),
```
- **Group Operations**: Create, manage, and search groups
- **Member Management**: Add, remove, and moderate members
- **Social Features**: Join requests and member profiles
- **Administrative Functions**: Group admin controls

### 9. Carpool Services
```python
('/api/v1/carpool', '/portal/carpools/carpool.json'),
('/api/v1/carpool/match', '/portal/carpools/matching.json'),
('/api/v1/carpool/modify', '/portal/carpools/modify_carpool.json'),
('/api/v1/carpool/join', '/portal/carpools/join_carpool.json'),
('/api/v1/carpool/accept_user', '/portal/carpools/accept_invite.json'),
('/api/v1/carpool_pairing', '/portal/carpools/carpool_pairing.json'),
('/api/v1/suggested_price', '/portal/carpools/suggested_price.json'),
```
- **Carpool Management**: Create, modify, and manage carpools
- **Matching Algorithm**: Driver-passenger matching system
- **Invitation System**: Accept/reject carpool invitations
- **Price Calculation**: Dynamic pricing suggestions

### 10. Trip & Navigation
```python
('/api/v1/prediction', '/portal/prediction_agent/location.json'),
('/api/v1/reservation', '/portal/reservation/reservation.json'),
('/api/v1/trip', '/portal/trip/trip.json'),
('/api/v1/trip_trajectory', '/portal/trip/trip_trajectory.json'),
('/api/v1/trip_rating', '/portal/trip/rating.json'),
('/api/v1/cycling_routing/path', '/portal/cycling_routing/path.json'),
```
- **Location Prediction**: AI-powered location forecasting
- **Trip Management**: Trip planning and execution
- **Navigation Services**: Route calculation and guidance
- **Quality Control**: Trip rating and feedback

### 11. Data Collection & Analytics
```python
('/api/v1/trace/trip_trajectory', '/portal/trace/trip_trajectory.json'),
('/api/v1/trace/app_state', '/portal/trace/app_state.json'),
('/api/v1/trace/user_visit', '/portal/trace/user_visit.json'),
('/api/v1/trace/uodtm', '/portal/trace/uodtm.json'),
('/api/v1/upload/log/here/(?P<any>.*)', '/portal/trace/log_here.json/$any'),
```
- **Usage Analytics**: App state and user behavior tracking
- **Location Tracking**: Trip trajectory data collection
- **External Integration**: HERE Maps data upload
- **Flexible Logging**: Regex-based log endpoint matching

### 12. Notifications & Messaging
```python
('/api/v1/notification', '/portal/messenger/notification.json'),
('/api/v1/notification/$id', '/portal/messenger/notification.json/$id'),
('/api/v1/notifications', '/portal/messenger/notifications.json'),
('/api/v1/notification_receive/$id', '/portal/messenger/receive.json/$id'),
```
- **Push Notifications**: User notification management
- **Message Delivery**: Notification receipt confirmation
- **Bulk Operations**: Multiple notification handling
- **Internal APIs**: System-to-system messaging

### 13. Rewards & Gamification
```python
('/api/v1/activity_type', '/portal/activity_type/maintain.json'),
('/api/v1/point_store', '/portal/store/point.json'),
('/api/v1/point_product', '/portal/store/point_product.json'),
('/api/v1/promotion', '/portal/promo/maintain.json'),
('/api/v1/promo_redeem', '/portal/promo/redeem.json'),
('/api/v1/giftcards', '/portal/reward/gift_card.json'),
('/api/v1/redeem', '/portal/reward/redeem.json'),
```
- **Points System**: Activity tracking and point allocation
- **Rewards Store**: Product catalog and redemption
- **Promotions**: Campaign management and code redemption
- **Gift Cards**: Digital gift card system

### 14. Wallet & Payments
```python
('/api/v1/points', '/portal/wallet/point.json'),
('/api/v1/points/history', '/portal/wallet/point_history.json'),
('/api/v1/wallet_setting', '/portal/wallet/setting.json'),
('/api/v1/card_setting', '/portal/wallet/card.json'),
('/api/v1/cards', '/portal/credit_card/cards.json'),
('/api/v1/tappay_notify', '/portal/transaction/tappay_notify.json'),
('/api/v1/transaction', '/portal/transaction/transaction.json'),
('/api/v1/transaction_history', '/portal/transaction/transaction_history.json'),
```
- **Digital Wallet**: Points and payment management
- **Payment Processing**: Credit card and transaction handling
- **Transaction History**: Financial record keeping
- **Third-party Integration**: TapPay payment gateway

### 15. Surveys & Feedback
```python
('/api/v1/microsurvey/first', '/portal/microsurvey/first.json'),
('/api/v1/microsurvey/submit', '/portal/microsurvey/submit.json'),
('/api/v1/microsurvey/skip', '/portal/microsurvey/skip.json'),
('/api/v1/suggestion_card/$anything', '/portal/suggestion_card/record.json/$anything'),
```
- **User Research**: Micro-survey system
- **Feedback Collection**: User suggestion recording
- **Engagement Tracking**: Survey completion analytics
- **Flexible Endpoints**: Dynamic suggestion card handling

### 16. Integration Services
```python
('/api/v1/wta/get_pokies', '/portal/wta/get_pokies.json'),
('/api/v1/carpooling_register', '/portal/user/carpooling_register.json'),
```
- **Third-party APIs**: WTA service integration
- **Specialized Registration**: Carpool-specific user registration

## URL Parameters

### Path Parameters
- `$id` - Resource identifier (numeric or UUID)
- `$os` - Operating system (iOS, Android, web)
- `$type` - Authentication type (google, facebook, apple)
- `$action` - Action verb (accept, reject, cancel)
- `$reason` - Cancellation or modification reason
- `$card_id` - Payment card identifier
- `$anything` - Wildcard parameter for flexible endpoints

### Regex Parameters
```python
('/api/v1/upload/log/here/(?P<any>.*)', '/portal/trace/log_here.json/$any')
```
- **Named Groups**: Uses Python regex named groups
- **Flexible Matching**: Captures arbitrary path segments
- **HERE Integration**: Handles complex HERE Maps API paths

## Bidirectional Routing

### Incoming Routes (routes_in)
- Maps external API URLs to internal Web2py paths
- Handles URL rewriting for clean REST endpoints
- Supports parameterized routes with variable substitution

### Outgoing Routes (routes_out)
```python
routes_out = ((x, y) for (y, x) in routes_in)
```
- **Automatic Generation**: Creates reverse mapping from routes_in
- **URL Generation**: Enables clean URL generation in templates
- **Consistency**: Ensures bidirectional route consistency

## Web2py Integration

### Controller Structure
```
/portal/controller/function.json/$param
├── portal/ - Application name
├── controller/ - Web2py controller
├── function.json - Function with JSON response
└── $param - URL parameter
```

### Response Format
- **JSON API**: All endpoints return JSON responses
- **HTML Exceptions**: Email verification pages return HTML
- **XML Responses**: VoIP endpoints return XML for Twilio

### MVC Pattern
- **Models**: Database abstraction layer
- **Views**: JSON/HTML template rendering
- **Controllers**: Business logic and request handling

## Configuration Features

### Route Organization
- **Functional Grouping**: Routes organized by feature area
- **Consistent Naming**: Predictable URL patterns
- **Version Control**: API versioning through URL path

### Parameter Handling
- **Type Safety**: Parameter validation in controllers
- **Optional Parameters**: Flexible route matching
- **Default Values**: Fallback parameter handling

### Error Handling
- **404 Routing**: Unmatched routes handled by Web2py
- **Parameter Validation**: Invalid parameters return errors
- **Graceful Degradation**: Fallback for missing endpoints

## Security Considerations

### Authentication Routes
- **Protected Endpoints**: Most routes require authentication
- **Public Endpoints**: App version and registration are public
- **Token Validation**: JWT token verification in controllers

### Input Validation
- **Parameter Sanitization**: URL parameters validated in controllers
- **CSRF Protection**: Built-in Web2py CSRF handling
- **Rate Limiting**: Implemented at application level

### Data Privacy
- **User Isolation**: User-specific data access controls
- **Enterprise Separation**: Multi-tenant data segregation
- **Audit Logging**: Request tracking for compliance

## Performance Optimization

### Route Efficiency
- **Direct Mapping**: Minimal URL processing overhead
- **Caching**: Web2py built-in route caching
- **Static Routes**: No complex regex for simple routes

### Load Balancing
- **Stateless Design**: Routes support horizontal scaling
- **Session Management**: External session storage
- **Database Routing**: Connection pooling and failover

## API Versioning Strategy

### Current Version (v1)
- **Stable API**: Production-ready endpoints
- **Backward Compatibility**: Maintained for existing clients
- **Deprecation Policy**: Planned migration to v2

### Future Versions
- **Version Isolation**: Separate controller namespaces
- **Feature Flags**: Gradual rollout of new features
- **Client Migration**: Seamless version transitions

## Monitoring & Debugging

### Route Analytics
- **Usage Tracking**: Route access patterns
- **Performance Metrics**: Response time monitoring
- **Error Rates**: Failed request analysis

### Development Tools
- **Route Testing**: Automated endpoint validation
- **URL Generation**: Development helper functions
- **Debug Mode**: Verbose routing information

This routing configuration forms the backbone of the MaaS platform's API infrastructure, providing a clean, RESTful interface for mobile and web clients while maintaining the flexibility and power of the Web2py framework underneath.