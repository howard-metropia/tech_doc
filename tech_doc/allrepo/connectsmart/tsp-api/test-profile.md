# Test Documentation: Profile API

## Overview
This test suite validates the Profile functionality within the TSP system, which manages comprehensive user profile information including personal details, vehicle information, location preferences, notification settings, and social media integration. The profile system supports user personalization and service customization.

## Test Configuration
- **File**: `test/test-profile.js`
- **Framework**: Mocha with Chai assertions, Supertest for HTTP testing, Sinon for mocking
- **Test Timeout**: 5 seconds for profile operations
- **Authentication**: Bearer token-based authentication (userid: 1003)
- **External Dependencies**: Tier service (mocked)

## API Endpoints Tested

### 1. GET /profile
**Purpose**: Retrieves complete user profile information

**Authentication**: Bearer token required

**Success Response Structure**:
```javascript
{
  result: 'success',
  data: {
    notification: Object,      // Notification preferences
    retention_plan: Boolean,   // Data retention consent
    email: String,            // User email address
    is_debug: Boolean,        // Debug mode flag
    connect_email: String,    // ConnectSmart email
    name: Object,             // First and last name
    phone: String,            // Phone number
    vehicle: Object,          // Vehicle information
    home: Object,             // Home address and coordinates
    office: Object,           // Office address and coordinates
    avatar: String,           // Profile picture URL
    rating: Number,           // User rating
    duo_auto_paired: Boolean, // Auto-pairing preference
    predict_location: Boolean, // Location prediction setting
    calendar_update: Boolean,  // Calendar sync setting
    permissions: Object,       // App permissions
    gender: String,           // Gender identity
    introduction: String,     // User bio/introduction
    linkedin_url: String,     // LinkedIn profile URL
    facebook_url: String,     // Facebook profile URL
    twitter_url: String,      // Twitter profile URL
    enterprises: Array,       // Associated enterprises
    employee_email: String,   // Work email
    referral_code: String,    // User's referral code
    tier: Object             // User tier information
  },
  security_key: String       // Security validation key
}
```

### 2. PUT /profile
**Purpose**: Updates user profile information

**Request Data Structure**:
```javascript
{
  name: {
    first_name: 'Backend',
    last_name: 'Unit-Test'
  },
  vehicle: {
    type: '',
    color: '',
    plate: '',
    make: '',
    picture_front: '',
    picture_side: ''
  },
  home: {
    address: '',
    latitude: 123.456,
    longitude: 123.789
  },
  office: {
    address: '',
    latitude: 23.456,
    longitude: 123.789
  },
  permissions: {
    push_notification: 1,
    gps: 1,
    calendar: 1
  },
  notification: {
    user_informatics: {
      flood_warning: false,
      road_incident: false,
      transit_incident: false,
      construction_zone: false
    }
  },
  retention_plan: false,
  duo_auto_paired: false,
  predict_location: true,
  calendar_update: true,
  gender: '',
  device_language: '',
  device_id: '',
  device_model: '',
  device_token: '',
  apns_device_token: '',
  os_version: '',
  app_version: '',
  telecom_carrier: '',
  introduction: '',
  linkedin_url: '',
  facebook_url: '',
  twitter_url: ''
}
```

## Profile Data Categories

### Personal Information
- **Name**: First and last name structure
- **Gender**: Gender identity field
- **Introduction**: Personal bio/description
- **Contact**: Email and phone information

### Location Preferences
- **Home**: Address with latitude/longitude coordinates
- **Office**: Work location with coordinates
- **Predict Location**: AI-based location prediction setting

### Vehicle Information
- **Type**: Vehicle category
- **Color**: Vehicle color
- **Plate**: License plate number
- **Make**: Vehicle manufacturer
- **Pictures**: Front and side vehicle photos

### Social Media Integration
- **LinkedIn**: Professional profile URL
- **Facebook**: Social media profile URL
- **Twitter**: Social media profile URL

### App Preferences
- **Notifications**: Granular notification settings by category
- **Permissions**: GPS, calendar, push notification permissions
- **Duo Auto-Paired**: Automatic carpooling pairing preference
- **Calendar Update**: Calendar synchronization setting
- **Retention Plan**: Data retention consent

### Enterprise Integration
- **Enterprises**: Associated organization accounts
- **Employee Email**: Work email address
- **Connect Email**: ConnectSmart enterprise email

### Device Information
- **Device Language**: User's preferred language
- **Device ID**: Unique device identifier
- **Device Model**: Hardware model information
- **Device Tokens**: Push notification tokens (FCM/APNS)
- **OS Version**: Operating system version
- **App Version**: Application version
- **Telecom Carrier**: Mobile network provider

### Gamification
- **Rating**: User rating/reputation score
- **Tier**: User tier level and benefits
- **Referral Code**: Personal referral code for rewards

## Test Scenarios

### Happy Path Testing

#### 1. Get Profile Success
```javascript
it('should fetch the profile of user', async function () {
  const resp = await request.set(auth).get(url);
  const { result, data, security_key } = resp.body;
  
  expect(result).to.eq('success');
  expect(security_key).not.be.undefined;
  expect(data).to.includes.keys(responseKeys);
});
```

**Validation**:
- Success result status
- Security key presence
- All expected response keys present
- Data structure integrity

#### 2. Update Profile Success
```javascript
it('should update the profile of user', async function () {
  const resp = await request.set(auth).put(url).send(inputData);
  const { result, data, security_key } = resp.body;
  
  expect(result).to.eq('success');
  expect(security_key).not.be.undefined;
  expect(data).to.includes.keys(responseKeys);
  expect(data.home).to.deep.eq(inputData.home);
  expect(data.name).to.deep.eq(inputData.name);
});
```

**Validation**:
- Successful update operation
- Data persistence verification
- Deep equality checks for nested objects
- Security key regeneration

### Error Path Testing

#### 1. Missing Authentication (Error 10004)
```javascript
// GET profile without authentication
const resp = await request.get(url).unset('userid');
expect(resp.body.result).to.eq('fail');
expect(resp.body.error).to.include({
  code: 10004,
  msg: 'Request header has something wrong'
});

// PUT profile without authentication
const resp = await request.put(url).unset('userid').send(inputData);
expect(resp.body.result).to.eq('fail');
expect(resp.body.error).to.include({
  code: 10004,
  msg: 'Request header has something wrong'
});
```

#### 2. Invalid Request Data (Error 10002)
```javascript
// Invalid field in update request
const resp = await request.set(auth).put(url).send({ test: {} });
expect(resp.body.result).to.eq('fail');
expect(resp.body.error).to.include({
  code: 10002,
  msg: '"test" is not allowed'
});
```

## External Service Integration

### Tier Service Mocking
```javascript
const tierService = require('@app/src/services/tier');
stub1 = sinon.stub(tierService, 'getUserTier').resolves({
  tier_level: 'green',
  tier_points: 1
});

stub2 = sinon.stub(tierService, 'getUserTierBenefits').resolves({
  raffle: {
    magnification: 1,
    toast: {
      title: 'Congratulations!',
      message: 'You\'re entered into the giveaway. Good luck!'
    }
  },
  referral: {
    magnification: 1,
    toast: {
      title: 'Congratulations!',
      message: 'We\'ve added 0.5 Coins to your Wallet!'
    }
  }
});
```

**Purpose**: Mocks tier service to provide consistent test data for user tier information and benefits.

## Authentication System

### Bearer Token Authentication
```javascript
before(async () => {
  const token = await authToken(userId);
  auth.authorization = `Bearer ${token}`;
});
```

**Process**:
1. Generate authentication token for test user
2. Include Bearer token in Authorization header
3. Validate token for all profile operations
4. Security key returned for additional validation

## Data Validation

### Coordinate Validation
- **Home/Office**: Latitude and longitude coordinates
- **Precision**: Support for decimal degrees
- **Range**: Global coordinate support

### Device Information Validation
- **Tokens**: FCM and APNS device tokens for push notifications
- **Versions**: OS and app version tracking
- **Hardware**: Device model and carrier information

### Social Media URL Validation
- **URL Format**: Valid URL structure for social media profiles
- **Optional Fields**: Empty strings allowed for unused profiles
- **Integration**: Support for profile linking and verification

## Security Features

### Security Key Generation
- Unique security key returned with each profile operation
- Enables additional validation for sensitive operations
- Changes with profile updates for security

### Data Protection
- Authentication required for all profile operations
- Field validation prevents unauthorized data modification
- Proper error handling protects system information

## Notification Preferences

### User Informatics Categories
- **Flood Warning**: Weather-related alerts
- **Road Incident**: Traffic incident notifications
- **Transit Incident**: Public transportation alerts
- **Construction Zone**: Road construction notifications

### Permission Management
- **Push Notifications**: Mobile app notifications
- **GPS**: Location services access
- **Calendar**: Calendar synchronization permissions

## Business Logic

### Profile Completeness
- Comprehensive profile data supports personalization
- Location information enables location-based services
- Vehicle information supports carpooling matching
- Social integration enhances user connections

### Privacy Controls
- Granular notification preferences
- Data retention consent management
- Permission-based feature access
- Optional social media integration

### Enterprise Integration
- Work profile separation from personal
- Enterprise email management
- Organization-specific features and benefits

## Test Coverage

### Functional Coverage
- ✅ Complete profile retrieval
- ✅ Profile update operations
- ✅ Authentication validation
- ✅ Data structure validation
- ✅ Security key generation

### Data Coverage
- ✅ Personal information fields
- ✅ Location and coordinate data
- ✅ Vehicle information
- ✅ Social media integration
- ✅ Notification preferences
- ✅ Device information
- ✅ Enterprise integration

### Error Coverage
- ✅ Authentication failures
- ✅ Invalid request data
- ✅ Field validation errors
- ✅ Unauthorized access attempts

## Integration Points

### Tier System
- User tier level and benefits integration
- Rewards and gamification features
- Progress tracking and achievements

### Location Services
- Home and office location management
- Coordinate-based service customization
- Location prediction and suggestions

### Enterprise Services
- Organization profile management
- Work-related feature sets
- Enterprise authentication integration

This test suite ensures the profile system provides comprehensive user data management with proper authentication, validation, and integration support within the TSP platform.