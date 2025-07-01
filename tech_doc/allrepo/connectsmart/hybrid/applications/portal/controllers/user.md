# Portal User Controller

## Overview
Comprehensive user management controller for the ConnectSmart Portal, handling user registration, authentication, profile management, phone verification, favorites management, and enterprise integration. This controller serves as the central hub for all user-related operations within the mobility platform.

## File Details
- **Location**: `/applications/portal/controllers/user.py`
- **Type**: web2py Controller (Large File: 2,221 lines)
- **Authentication**: Mixed (some endpoints public, others JWT-protected)
- **Dependencies**: Twilio, SMS services, enterprise integration, contact management

## Core Imports & Dependencies
```python
import json
import ast
import random
import re
import string
import datetime
from twilio.rest import Client
from upload_tools import UploadTool
from sqs_helper import send_sqs_task
from mongo_helper import MongoManager
from datetime_utils import utcnow_to_tz
from slack_helper import SlackManager
```

## Authentication Functions

### `register()` - POST User Registration
Creates new user accounts with email verification.

#### Endpoint
```
POST /api/v1/register
```

#### Request Structure
```python
{
    "email": "user@example.com",
    "password": "secure_password",
    "first_name": "John",
    "last_name": "Doe",
    "latitude": 32.7767,        # Optional registration location
    "longitude": -96.7970,      # Optional registration location
    "security_key": "string"    # Optional security key
}
```

#### Registration Process
1. **User Creation**: Creates user with `is_active=False`
2. **Group Assignment**: Adds user to general group
3. **Email Verification**: Sends activation code
4. **Auto-login**: Attempts login after registration

```python
user = auth.register_bare(
    registration_id=email,
    first_name=first_name,
    last_name=last_name,
    email=email,
    password=password,
    registration_key='new',
    is_active=False,
    created_on=request.utcnow,
    phone_verification_key='new'
)
```

### `login()` - POST User Authentication
Authenticates existing users with JWT token generation.

#### Endpoint
```
POST /api/v1/login
```

#### Request Structure
```python
{
    "email": "user@example.com",
    "password": "secure_password",
    "security_key": "string"  # Optional
}
```

#### Authentication Flow
```python
def _do_login(email, password, security_key=None):
    login_user = auth.login_bare(email, password)
    
    if not login_user:
        # Check for user existence and activation status
        table_user = auth.table_user()
        login_user = table_user(registration_id=email)
        
        if not login_user:
            return json_response.fail(ERROR_USER_NOT_FOUND, T('User not found'))
        
        # Verify password and activation status
        if not login_user.is_active:
            if login_user.registration_key == 'new':
                _send_activation_code(email)  # Auto-send activation
            return json_response.fail(ERROR_USER_NOT_ACTIVATED, T('User not activated'))
    
    # Generate JWT token
    access_token = jwt_helper.generate_token(login_user.id)
    login_user.update_record(access_token=access_token, security_key=security_key)
```

### `activation()` - POST Email Verification
Handles email activation and resend functionality.

#### Endpoints
```
POST /api/v1/activation                    # Verify activation code
POST /api/v1/activation/resend_code       # Resend activation code
```

#### Activation Process
```python
# Verify activation code
user.update_record(
    registration_key=None,
    registration_key_created_on=None,
    registration_key_resend_count=0,
    is_active=True
)

# Generate access token
access_token = jwt_helper.generate_token(user.id)
```

## Social Authentication

### `openid_login()` - POST OAuth Integration
Handles Facebook, Google, and Apple authentication.

#### Endpoint
```
POST /api/v1/openid_login/{provider}
```

#### Supported Providers
- **fb**: Facebook authentication
- **gplus**: Google Plus authentication  
- **apple**: Apple Sign-In authentication

#### OAuth Flow
```python
# Check for existing merged accounts
if provider == 'fb':
    user = table_user(facebook_id=rid)
elif provider == 'gplus':
    user = table_user(google_id=rid)
elif provider == 'apple':
    user = table_user(apple_id=rid)

if not user:
    # Create new user for first-time OAuth
    registration_id = '%s_%s' % (provider, rid)
    user = auth.get_or_create_user({
        'registration_id': registration_id,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'is_active': True,
        'security_key': security_key
    })
```

## Profile Management

### `profile()` - GET/PUT User Profile
Comprehensive user profile management with file uploads.

#### GET Profile Information
```
GET /api/v1/profile
```

**Response Structure**:
```python
{
    "bytemark_email": "string",
    "email": "string",
    "name": {
        "first_name": "string",
        "last_name": "string"
    },
    "avatar": "string",
    "rating": float,
    "phone": {
        "country_code": "string",
        "phone_number": "string",
        "phone_verified": bool
    },
    "vehicle": {
        "type": "string",
        "color": "string",
        "plate": "string",
        "make": "string",
        "picture_front": "string",
        "picture_side": "string"
    },
    "home": {
        "address": "string",
        "latitude": float,
        "longitude": float
    },
    "office": {
        "address": "string",
        "latitude": float,
        "longitude": float
    },
    "enterprises": []
}
```

#### PUT Update Profile
Supports updating multiple profile sections:

**Device Tokens**:
```python
# FCM or APNS token management
if device_token:
    user.device_token = device_token
    user.apns_device_token = None
elif apns_device_token:
    user.apns_device_token = apns_device_token
    user.device_token = None
```

**Location Data**:
```python
# Home and office address management
if home and ('address' and 'latitude' and 'longitude') in home:
    user.home_address = home['address']
    user.home_latitude = home['latitude']
    user.home_longitude = home['longitude']
```

**Vehicle Information**:
```python
# Vehicle details with image upload
if vehicle and ('type' and 'color' and 'plate') in vehicle:
    user.vehicle_type = vehicle['type']
    user.vehicle_color = vehicle['color']
    user.vehicle_plate = vehicle['plate']
    
    # Handle vehicle images
    if vehicle.get('picture_front'):
        vf_path = 'user/user_{}_vehicle_front.jpg'.format(auth.user.id)
        vehicle_front_url = upload_tool.upload_base64_image(vf_path, vehicle['picture_front'])
```

## Phone Verification

### `verify_phone()` - POST Phone Verification
Two-step phone verification with SMS integration.

#### Endpoints
```
POST /api/v1/verify_phone/resend_code    # Send verification SMS
POST /api/v1/verify_phone               # Verify SMS code
```

#### SMS Integration
```python
def _send_sms(to, body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    try:
        message = client.messages.create(
            from_=TWILIO_FROM,
            to=to,
            body=body
        )
        logger.info('[SMS] Successfully Sent SMS to %s: sid=%s' % (to, message.sid))
        return True
    except TwilioRestException as e:
        logger.error('[SMS] Failed to send SMS: code=%s, msg=%s' % (e.code, e.msg))
        return False
```

#### Phone Number Validation
```python
# Prevent duplicate phone numbers across providers
provider_email = 1    # 0001
provider_facebook = 2 # 0010
provider_google = 4   # 0100
provider_apple = 8    # 1000

# Check for conflicts across authentication providers
for other in rows_other:
    provider_other = 0
    if email_regex.match(other.registration_id):
        provider_other = provider_other | provider_email
    if other.facebook_id:
        provider_other = provider_other | provider_facebook
    # ... additional provider checks
```

## Favorites Management

### `favorites()` - POST/PUT/GET/DELETE Favorites
Manages user favorite locations with categorization.

#### Categories
- **1**: Home (max 1)
- **2**: Company/Work (max 1)  
- **3**: Often visited (max 8)
- **4**: General favorites (unlimited)

#### POST Create Favorite
```python
{
    "icon_type": int,
    "place_id": "string",
    "name": "string",
    "address": "string",
    "access_latitude": float,
    "access_longitude": float,
    "latitude": float,
    "longitude": float,
    "category": int
}
```

#### Business Logic
```python
# Validate category limits
if (category == 1 and len(rows.find(lambda _row: _row.category == 1)) + 1 > 1) or \
   (category == 2 and len(rows.find(lambda _row: _row.category == 2)) + 1 > 1) or \
   (category == 3 and len(rows.find(lambda _row: _row.category == 3)) + 1 > 8):
    return json_response.fail(ERROR_EXCEED_FAVORITES, T('Exceed count of favorite'))
```

#### App Data Integration
```python
# Record user actions for analytics
if category in (1,2):
    user_action_text = 'HomeLocation' if category == 1 else 'WorkLocation'
    save_location = 'SaveHome' if category == 1 else 'SaveWork'
    
    db.app_data.insert(
        user_id=user_id,
        user_action=user_action_text,
        lat=lat,
        lon=lon,
        gmt_time=now,
        local_time=user_local_time
    )
```

## Contact Management

### `contact()` - POST/GET/PUT/DELETE Contact Management
Manages user emergency and priority contacts.

#### Contact Structure
```python
{
    "contacts": [
        {
            "name": "string",
            "email": "string",
            "country_code": "string",
            "phone_number": "string",
            "priority": int
        }
    ]
}
```

#### Priority Management
```python
# Automatic priority reordering
rows = db(db.contact.owner_id == auth.user.id).select(
    db.contact.id, db.contact.priority,
    orderby=db.contact.priority
)
for i, row in enumerate(rows):
    row.update_record(priority=i + 1)
```

## Enterprise Integration

### `verify_carpool_email()` - GET/POST Enterprise Email Verification
Handles enterprise email verification for carpooling groups.

#### Verification Process
```python
from enterpirse_helper import EnterpriseHelper
from enterprise_carpool import check_verification, send_verification_mail

enterprise_result = enterprise_helper.get_enterprise(email, auth.user_id, verify_type)

if verify_type == 'carpool':
    if not enterprise_result or enterprise_result.get('have_duo_group') is False:
        raise Exception(ERROR_ENTERPRISE_EMAIL_INVALID, 
                       T('This email is not recognize.'))
```

#### Email Verification Flow
```python
# Send verification email
verify_token = send_verification_mail(response, auth.user_id, email, verify_type)

# Process verification callback
payload = auth.jwt_handler.load_token(verify_token)
user_id = payload.get('user').get('id')
enterprise_email = payload.get('user').get('email')

# Update enterprise association
row.update_record(
    email_verify_token='success',
    enterprise_id=employee_data['org_id'],
    employee_status=employee_data['status']
)
```

## Security Features

### Password Management
```python
# Change password with current password verification
def change_password():
    current_pwd = fields['current_password']
    new_pwd = fields['new_password']
    
    # Verify current password
    verify_pwd = table_user['password'].validate(current_pwd)[0]
    if verify_pwd != user.password:
        return json_response.fail(ERROR_WRONG_PASSWORD, T('Wrong password'))
    
    # Set new password
    password = table_user['password'].validate(new_pwd)[0]
    user.update_record(password=password)
```

### Account Merging
```python
# Merge accounts during phone verification
for other in rows_other:
    if not other.registration_key and not other.phone_verification_key:
        # Merge account data
        other.email = user.email
        other.password = user.password
        other.first_name = user.first_name
        other.last_name = user.last_name
        other.access_token = jwt_helper.generate_token(other.id)
        other.update_record()
        
        user.delete_record()  # Remove duplicate account
```

## File Upload Management

### Avatar and Vehicle Images
```python
upload_tool = UploadTool(AWS_S3_BUCKET)

# Avatar upload
if avatar:
    avatar_path = 'user/user_{}.jpg'.format(auth.user.id)
    avatar_url = upload_tool.upload_base64_image(avatar_path, avatar)
    user.avatar = avatar_url

# Vehicle image upload
if vehicle.get('picture_front'):
    vf_path = 'user/user_{}_vehicle_front.jpg'.format(auth.user.id)
    vehicle_front_url = upload_tool.upload_base64_image(vf_path, vehicle['picture_front'])
```

## Data Analytics Integration

### App Data Tracking
```python
# Track user actions for analytics
def _record_user_action(user_id, action, location_data):
    user_local_time = utcnow_to_tz(request.env.http_zone)
    
    db.app_data.insert(
        user_id=user_id,
        user_action=action,
        lat=location_data['lat'],
        lon=location_data['lon'],
        gmt_time=now,
        local_time=user_local_time,
        created_on=now,
        modified_on=now
    )
```

## Dependencies
- **Twilio**: SMS verification services
- **AWS S3**: File upload and storage
- **Enterprise Helper**: Enterprise integration
- **MongoDB**: App state and analytics data
- **Upload Tools**: Image processing and storage
- **SQS**: Event and notification queuing

## Usage Examples

### User Registration
```python
# Request
POST /api/v1/register
{
    "email": "john@example.com",
    "password": "securepass123",
    "first_name": "John",
    "last_name": "Doe",
    "latitude": 32.7767,
    "longitude": -96.7970
}

# Response
{
    "status": "success",
    "data": {
        "id": 12345,
        "phone": {
            "country_code": null,
            "phone_number": null,
            "phone_verified": false
        }
    }
}
```

### Profile Update
```python
# Request
PUT /api/v1/profile
{
    "name": {
        "first_name": "John",
        "last_name": "Smith"
    },
    "vehicle": {
        "type": "Sedan",
        "color": "Blue",
        "plate": "ABC123",
        "picture_front": "base64_image_data"
    }
}

# Response: Updated profile data
```

This controller provides comprehensive user management capabilities for the ConnectSmart mobility platform, handling everything from basic authentication to complex enterprise integration and profile management features.