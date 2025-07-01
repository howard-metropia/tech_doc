# TSP API Profile Service Documentation

## 🔍 Quick Summary (TL;DR)
The Profile service manages comprehensive user profile data including personal information, vehicle details, location preferences, notification settings, social links, enterprise affiliations, and avatar/image uploads to AWS S3 with extensive customization and security features.

**Keywords:** user-profile | profile-management | aws-s3-upload | image-upload | user-settings | notification-preferences | enterprise-integration | vehicle-data | location-data

**Primary use cases:** Managing user profile information, uploading profile and vehicle images, configuring notification settings, managing enterprise affiliations, handling user preferences, social media integration

**Compatibility:** Node.js >= 16.0.0, AWS S3 integration, MySQL databases (portal and carpooling), Hashids for encoding, comprehensive user data management

## ❓ Common Questions Quick Index
- **Q: What profile data is managed?** → Personal info, vehicle details, locations (home/office), notifications, social links, enterprise data
- **Q: How are images handled?** → Base64 upload to AWS S3 with CDN URLs and hash-based naming
- **Q: What notification settings exist?** → Road incidents, construction zones, flood warnings, transit incidents, weather alerts
- **Q: How do enterprise affiliations work?** → Integration with carpool and telework enterprise systems
- **Q: Can users have multiple email addresses?** → Yes, supports Google, Facebook, Apple, and common email addresses
- **Q: What vehicle information is stored?** → Type, color, plate, make, front/side pictures

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as your **complete digital identity** in the transportation app. It stores everything about you - your name, photo, car details, home and work addresses, notification preferences, and even which companies you work with for carpooling. You can upload photos of yourself and your car, and everything gets saved securely in the cloud.

**Technical explanation:** 
A comprehensive user profile management service that handles complex user data structures including personal information, vehicle details, location preferences, notification configurations, and enterprise integrations. Features AWS S3 image upload with CDN delivery, hash-based file naming, multi-database operations, and extensive user customization options.

**Business value explanation:**
Enables rich user personalization, supports enterprise B2B integrations, provides secure image storage and delivery, facilitates user engagement through comprehensive profiles, enables targeted notifications and features, and supports complex organizational structures for carpooling and telework programs.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/profile.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Node.js with Objection.js ORM
- **Type:** Comprehensive User Profile Management Service
- **File Size:** ~9.4 KB
- **Complexity Score:** ⭐⭐⭐⭐ (High - Complex data management with image upload)

**Dependencies:**
- `hashids`: Unique ID generation for images (**High**)
- `@maas/core/mysql`: Multi-database connectivity (**Critical**)
- `@maas/core/log`: Logging infrastructure (**High**)
- `@app/src/services/s3`: AWS S3 upload service (**Critical**)
- `@app/src/services/tier`: User tier management (**Medium**)
- Various models for data persistence (**Critical**)

## 📝 Detailed Code Analysis

### Core Configuration Constants

**CDN URL Construction:**
```javascript
const CDN_URL = `https://s3-${awsConfig.region}.amazonaws.com/${awsConfig.s3.bucketName}`;
```

**Default UIS (User Informatics) Settings:**
```javascript
const UIS_DEFAULT_SETTING = {
  road_incident: true,
  construction_zone: true,
  flood_warning: true,
  transit_incident: true,
  weather_alert: true,
};
```

### uploadImage Function

**Purpose:** Handles image upload to AWS S3 with hash-based naming

**Parameters:**
- `content`: String - Base64 encoded image data
- `mode`: String - Image category ('avatar', 'picture_front', 'picture_side')
- `userId`: Number - User identifier
- `email`: String - User email for hash generation

**Returns:** Promise resolving to S3 object key

**Implementation Details:**

### Image Type Detection
```javascript
const contentType = content.indexOf('iVBORw0KGgo') === -1 ? 'image/jpeg' : 'image/png';
const extension = content.indexOf('iVBORw0KGgo') === -1 ? 'jpg' : 'png';
```
- Detects PNG vs JPEG based on PNG signature
- Sets appropriate MIME type and file extension

### Hash-Based File Naming
```javascript
switch (mode) {
  case 'avatar':
    hashids = new Hashids(userId + email, 10);
    objectKey = hashids.encode(1);
    break;
  case 'picture_front':
    hashids = new Hashids(userId + 'v1' + email, 10);
    objectKey = hashids.encode(1);
    break;
  case 'picture_side':
    hashids = new Hashids(userId + 'v2' + email, 10);
    objectKey = hashids.encode(1);
    break;
}
fileName = `user/${objectKey}.${extension}`;
```
- Generates unique, collision-resistant filenames
- Different hash seeds for different image types
- Organized under 'user/' prefix in S3

### get Function

**Purpose:** Retrieves comprehensive user profile data

**Parameters:**
- `userId`: Number - User identifier

**Returns:** Promise resolving to complete profile object with security key

**Complex Data Assembly:**

### Notification Settings Management
```javascript
returnData.notification = { user_informatics: UIS_DEFAULT_SETTING };
if (userConfig && userConfig.uis_setting !== null) {
  returnData.notification = {
    user_informatics: { ...UIS_DEFAULT_SETTING, ...userConfig.uis_setting },
  };
}
```
- Merges user custom settings with defaults
- Ensures all notification types have values

### Multi-Email Support
```javascript
returnData.connect_email = {
  default_email: userData.email ?? '',
  common: userData.common_email ?? '',
  google: userData.google_email ?? '',
  facebook: userData.facebook_email ?? '',
  apple: userData.apple_email ?? '',
  now_choose: userData.now_choose_email ?? '',
};

switch (userData.now_choose_email) {
  case 'google':
    returnData.email = userData.google_email;
    break;
  case 'facebook':
    returnData.email = userData.facebook_email;
    break;
  // ... etc
}
```
- Supports multiple OAuth provider emails
- Dynamic email selection based on user choice

### Vehicle Information with CDN URLs
```javascript
returnData.vehicle = {
  type: userData.vehicle_type ?? '',
  color: userData.vehicle_color ?? '',
  plate: userData.vehicle_plate ?? '',
  make: userData.vehicle_make ?? '',
  picture_front: userData.vehicle_picture_front
    ? `${CDN_URL}/${userData.vehicle_picture_front}`
    : '',
  picture_side: userData.vehicle_picture_side
    ? `${CDN_URL}/${userData.vehicle_picture_side}`
    : '',
};
```
- Constructs full CDN URLs for vehicle images
- Graceful handling of missing images

### Enterprise Integration
```javascript
const enterpriseData = await Enterprises.query().where({
  user_id: userId,
  email_verify_token: 'success',
});

await Promise.all(
  enterpriseData.map(async (raw) => {
    const employee = await carpoolKnex
      .select({
        telework_og_id: 'amp.telework_og_id',
        enterprise_name: 'os.name_zh',
      })
      .from({ amp: 'acc_member_portal' })
      .where({ user_id: userId, email: raw.enterprise_email })
      .leftJoin({ os: 'org_setting' }, 'os.id', raw.enterprise_id)
      .first();
    // Process enterprise and telework data
  }),
);
```
- Cross-database queries between portal and carpooling databases
- Separate tracking of carpool and telework eligibility

### Referral Code Generation
```javascript
const referralHash = new Hashids(portalConfig.projectTitle, 10);
returnData.referral_code = referralHash.encode(userId);
```
- Project-specific referral code generation
- Consistent encoding based on user ID

### update Function

**Purpose:** Updates user profile data across multiple tables

**Parameters:**
- `inputData`: Object - Contains userId, zone, and various profile fields

**Complex Update Logic:**

### Data Categorization
```javascript
const objectKeys = [];
const noneObjectKeys = [];
for (const key of Object.keys(inputData)) {
  if (typeof inputData[key] === 'object') {
    objectKeys.push(key);
  } else if (['zone', 'lang', 'userId', 'newversion'].indexOf(key) === -1) {
    noneObjectKeys.push(key);
  }
}
```
- Separates nested objects from flat fields
- Excludes header/system fields from processing

### Field Mapping and Prefixing
```javascript
let prefix = null;
switch (parent) {
  case 'name':
    prefix = '';
    break;
  case 'home':
    prefix = `home_`;
    break;
  case 'office':
    prefix = `office_`;
    break;
  case 'vehicle':
    prefix = `vehicle_`;
    break;
  case 'permissions':
    prefix = `per_`;
    break;
}
```
- Maps nested object keys to database column names
- Consistent naming convention across profile sections

### Image Upload Handling
```javascript
if (parent === 'vehicle' && ['picture_front', 'picture_side'].indexOf(key) !== -1) {
  updateUserData[fieldName] = await uploadImage(
    inputData.vehicle[key],
    key,
    userId,
    userData.email,
  );
}
```
- Automatic image upload for vehicle pictures
- Stores S3 object keys in database

### Multi-Table Updates
```javascript
// Update auth_user table
if (Object.keys(updateUserData).length) {
  await AuthUsers.query().update(updateUserData).where('id', userId);
}

// Update user_config table
if (Object.keys(updateUserConfig).length) {
  const result = await UserConfig.query()
    .update(updateUserConfig)
    .where('user_id', userId);
    
  if (!result) {
    // Create user_config if doesn't exist
    await UserConfig.query().insert(updateUserConfig).onConflict('user_id').merge();
  }
}
```
- Handles updates across multiple database tables
- Creates user_config record if it doesn't exist

## 🚀 Usage Methods

### Basic Profile Management
```javascript
const profileService = require('@app/src/services/profile');

async function getUserProfile(userId) {
  try {
    const profileData = await profileService.get(userId);
    
    console.log('User Profile:');
    console.log('Name:', profileData.data.name);
    console.log('Email:', profileData.data.email);
    console.log('Vehicle:', profileData.data.vehicle);
    console.log('Avatar:', profileData.data.avatar);
    console.log('Enterprise Count:', profileData.data.enterprises.length);
    
    return profileData;
  } catch (error) {
    console.error('Error getting user profile:', error);
    throw error;
  }
}

async function updateBasicProfile(userId, updates) {
  try {
    await profileService.update({
      userId: userId,
      zone: 'UTC',
      ...updates
    });
    
    console.log('Profile updated successfully');
    
    // Get updated profile
    return await getUserProfile(userId);
  } catch (error) {
    console.error('Error updating profile:', error);
    throw error;
  }
}

// Usage
const userId = 12345;
const profile = await getUserProfile(userId);

const updates = {
  name: {
    first_name: 'John',
    last_name: 'Doe'
  },
  phone: {
    country_code: '+1',
    phone_number: '5551234567'
  }
};
await updateBasicProfile(userId, updates);
```

### Vehicle Information Management
```javascript
class VehicleProfileManager {
  constructor() {
    this.profileService = require('@app/src/services/profile');
  }

  async updateVehicleInfo(userId, vehicleData) {
    try {
      const updates = {
        userId: userId,
        zone: 'UTC',
        vehicle: {
          type: vehicleData.type,
          color: vehicleData.color,
          plate: vehicleData.plate,
          make: vehicleData.make
        }
      };

      // Add vehicle images if provided
      if (vehicleData.frontImage) {
        updates.vehicle.picture_front = vehicleData.frontImage; // Base64 string
      }
      
      if (vehicleData.sideImage) {
        updates.vehicle.picture_side = vehicleData.sideImage; // Base64 string
      }

      await this.profileService.update(updates);

      return {
        success: true,
        message: 'Vehicle information updated successfully'
      };
    } catch (error) {
      console.error('Error updating vehicle info:', error);
      throw error;
    }
  }

  async getVehicleProfile(userId) {
    try {
      const profile = await this.profileService.get(userId);
      
      return {
        userId,
        vehicle: profile.data.vehicle,
        hasImages: {
          front: !!profile.data.vehicle.picture_front,
          side: !!profile.data.vehicle.picture_side
        }
      };
    } catch (error) {
      console.error('Error getting vehicle profile:', error);
      throw error;
    }
  }

  async removeVehicleImages(userId) {
    try {
      await this.profileService.update({
        userId: userId,
        zone: 'UTC',
        vehicle: {
          picture_front: '',
          picture_side: ''
        }
      });

      return {
        success: true,
        message: 'Vehicle images removed successfully'
      };
    } catch (error) {
      console.error('Error removing vehicle images:', error);
      throw error;
    }
  }
}
```

### Location and Address Management
```javascript
class LocationProfileManager {
  constructor() {
    this.profileService = require('@app/src/services/profile');
  }

  async updateHomeAddress(userId, addressData) {
    try {
      await this.profileService.update({
        userId: userId,
        zone: 'UTC',
        home: {
          address: addressData.address,
          latitude: addressData.latitude,
          longitude: addressData.longitude
        }
      });

      return {
        success: true,
        addressType: 'home',
        newAddress: addressData
      };
    } catch (error) {
      console.error('Error updating home address:', error);
      throw error;
    }
  }

  async updateOfficeAddress(userId, addressData) {
    try {
      await this.profileService.update({
        userId: userId,
        zone: 'UTC',
        office: {
          address: addressData.address,
          latitude: addressData.latitude,
          longitude: addressData.longitude
        }
      });

      return {
        success: true,
        addressType: 'office',
        newAddress: addressData
      };
    } catch (error) {
      console.error('Error updating office address:', error);
      throw error;
    }
  }

  async getLocationSummary(userId) {
    try {
      const profile = await this.profileService.get(userId);
      
      return {
        userId,
        home: {
          address: profile.data.home.address,
          coordinates: {
            latitude: profile.data.home.latitude,
            longitude: profile.data.home.longitude
          },
          isSet: !!profile.data.home.address
        },
        office: {
          address: profile.data.office.address,
          coordinates: {
            latitude: profile.data.office.latitude,
            longitude: profile.data.office.longitude
          },
          isSet: !!profile.data.office.address
        }
      };
    } catch (error) {
      console.error('Error getting location summary:', error);
      throw error;
    }
  }

  async calculateHomeOfficeDistance(userId) {
    try {
      const locations = await this.getLocationSummary(userId);
      
      if (!locations.home.isSet || !locations.office.isSet) {
        return {
          available: false,
          reason: 'Both home and office addresses required'
        };
      }

      const distance = this.calculateDistance(
        locations.home.coordinates,
        locations.office.coordinates
      );

      return {
        available: true,
        distance: {
          kilometers: distance,
          miles: distance * 0.621371
        },
        commute: {
          home: locations.home.address,
          office: locations.office.address
        }
      };
    } catch (error) {
      console.error('Error calculating home-office distance:', error);
      throw error;
    }
  }

  calculateDistance(coord1, coord2) {
    const R = 6371; // Earth's radius in kilometers
    const dLat = this.toRadians(coord2.latitude - coord1.latitude);
    const dLon = this.toRadians(coord2.longitude - coord1.longitude);
    
    const a = 
      Math.sin(dLat/2) * Math.sin(dLat/2) +
      Math.cos(this.toRadians(coord1.latitude)) * Math.cos(this.toRadians(coord2.latitude)) * 
      Math.sin(dLon/2) * Math.sin(dLon/2);
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
  }

  toRadians(degrees) {
    return degrees * (Math.PI/180);
  }
}
```

### Notification Preferences Manager
```javascript
class NotificationPreferencesManager {
  constructor() {
    this.profileService = require('@app/src/services/profile');
  }

  async updateNotificationSettings(userId, notificationPrefs) {
    try {
      await this.profileService.update({
        userId: userId,
        zone: 'UTC',
        notification: {
          user_informatics: notificationPrefs
        }
      });

      return {
        success: true,
        updatedPreferences: notificationPrefs
      };
    } catch (error) {
      console.error('Error updating notification settings:', error);
      throw error;
    }
  }

  async getNotificationSettings(userId) {
    try {
      const profile = await this.profileService.get(userId);
      
      return {
        userId,
        notifications: profile.data.notification.user_informatics,
        categories: {
          safety: {
            road_incident: profile.data.notification.user_informatics.road_incident,
            construction_zone: profile.data.notification.user_informatics.construction_zone,
            flood_warning: profile.data.notification.user_informatics.flood_warning
          },
          transportation: {
            transit_incident: profile.data.notification.user_informatics.transit_incident
          },
          weather: {
            weather_alert: profile.data.notification.user_informatics.weather_alert
          }
        }
      };
    } catch (error) {
      console.error('Error getting notification settings:', error);
      throw error;
    }
  }

  async enableAllNotifications(userId) {
    const allEnabled = {
      road_incident: true,
      construction_zone: true,
      flood_warning: true,
      transit_incident: true,
      weather_alert: true
    };

    return await this.updateNotificationSettings(userId, allEnabled);
  }

  async disableAllNotifications(userId) {
    const allDisabled = {
      road_incident: false,
      construction_zone: false,
      flood_warning: false,
      transit_incident: false,
      weather_alert: false
    };

    return await this.updateNotificationSettings(userId, allDisabled);
  }

  async updateSafetyNotifications(userId, enabled) {
    try {
      const current = await this.getNotificationSettings(userId);
      
      const updated = {
        ...current.notifications,
        road_incident: enabled,
        construction_zone: enabled,
        flood_warning: enabled
      };

      return await this.updateNotificationSettings(userId, updated);
    } catch (error) {
      console.error('Error updating safety notifications:', error);
      throw error;
    }
  }
}
```

### Avatar and Image Management
```javascript
class ProfileImageManager {
  constructor() {
    this.profileService = require('@app/src/services/profile');
  }

  async updateAvatar(userId, base64Image) {
    try {
      await this.profileService.update({
        userId: userId,
        zone: 'UTC',
        avatar: base64Image
      });

      // Get updated profile to return new avatar URL
      const profile = await this.profileService.get(userId);

      return {
        success: true,
        avatarUrl: profile.data.avatar,
        message: 'Avatar updated successfully'
      };
    } catch (error) {
      console.error('Error updating avatar:', error);
      throw error;
    }
  }

  async removeAvatar(userId) {
    try {
      await this.profileService.update({
        userId: userId,
        zone: 'UTC',
        avatar: ''
      });

      return {
        success: true,
        message: 'Avatar removed successfully'
      };
    } catch (error) {
      console.error('Error removing avatar:', error);
      throw error;
    }
  }

  validateImageData(base64String) {
    // Basic validation
    if (!base64String || typeof base64String !== 'string') {
      return { valid: false, error: 'Invalid image data' };
    }

    // Check if it's a valid base64 string
    if (!base64String.match(/^[A-Za-z0-9+/]+=*$/)) {
      return { valid: false, error: 'Invalid base64 format' };
    }

    // Check image type
    const isPNG = base64String.indexOf('iVBORw0KGgo') !== -1;
    const isJPEG = !isPNG;

    // Estimate file size (base64 is ~33% larger than binary)
    const estimatedSize = (base64String.length * 3) / 4;
    const maxSize = 5 * 1024 * 1024; // 5MB

    if (estimatedSize > maxSize) {
      return { 
        valid: false, 
        error: `Image too large: ${Math.round(estimatedSize / 1024 / 1024)}MB (max 5MB)` 
      };
    }

    return {
      valid: true,
      imageType: isPNG ? 'PNG' : 'JPEG',
      estimatedSize: Math.round(estimatedSize / 1024) + 'KB'
    };
  }

  async batchUpdateVehicleImages(userId, frontImage, sideImage) {
    try {
      // Validate both images
      if (frontImage) {
        const frontValidation = this.validateImageData(frontImage);
        if (!frontValidation.valid) {
          throw new Error(`Front image: ${frontValidation.error}`);
        }
      }

      if (sideImage) {
        const sideValidation = this.validateImageData(sideImage);
        if (!sideValidation.valid) {
          throw new Error(`Side image: ${sideValidation.error}`);
        }
      }

      const vehicleUpdates = {};
      if (frontImage) vehicleUpdates.picture_front = frontImage;
      if (sideImage) vehicleUpdates.picture_side = sideImage;

      await this.profileService.update({
        userId: userId,
        zone: 'UTC',
        vehicle: vehicleUpdates
      });

      // Get updated URLs
      const profile = await this.profileService.get(userId);

      return {
        success: true,
        vehicleImages: {
          front: profile.data.vehicle.picture_front,
          side: profile.data.vehicle.picture_side
        },
        message: 'Vehicle images updated successfully'
      };
    } catch (error) {
      console.error('Error updating vehicle images:', error);
      throw error;
    }
  }
}
```

### Enterprise Integration Manager
```javascript
class EnterpriseProfileManager {
  constructor() {
    this.profileService = require('@app/src/services/profile');
  }

  async getEnterpriseAffiliations(userId) {
    try {
      const profile = await this.profileService.get(userId);
      
      return {
        userId,
        enterprises: profile.data.enterprises,
        employeeEmails: profile.data.employee_email,
        summary: {
          totalEnterprises: profile.data.enterprises.length,
          carpoolEligible: profile.data.employee_email.carpool.length,
          teleworkEligible: profile.data.employee_email.telework.length
        }
      };
    } catch (error) {
      console.error('Error getting enterprise affiliations:', error);
      throw error;
    }
  }

  async checkCarpoolEligibility(userId) {
    try {
      const affiliations = await this.getEnterpriseAffiliations(userId);
      
      return {
        eligible: affiliations.summary.carpoolEligible > 0,
        enterpriseCount: affiliations.summary.carpoolEligible,
        enterprises: affiliations.employeeEmails.carpool
      };
    } catch (error) {
      console.error('Error checking carpool eligibility:', error);
      throw error;
    }
  }

  async checkTeleworkEligibility(userId) {
    try {
      const affiliations = await this.getEnterpriseAffiliations(userId);
      
      return {
        eligible: affiliations.summary.teleworkEligible > 0,
        enterpriseCount: affiliations.summary.teleworkEligible,
        enterprises: affiliations.employeeEmails.telework
      };
    } catch (error) {
      console.error('Error checking telework eligibility:', error);
      throw error;
    }
  }
}
```

## 📊 Output Examples

### Complete Profile Response
```json
{
  "data": {
    "email": "john.doe@example.com",
    "is_debug": 0,
    "connect_email": {
      "default_email": "john.doe@example.com",
      "common": "john.doe@example.com",
      "google": "john.doe@gmail.com",
      "facebook": "john.doe@facebook.com",
      "apple": "",
      "now_choose": "google"
    },
    "name": {
      "first_name": "John",
      "last_name": "Doe"
    },
    "phone": {
      "country_code": "+1",
      "phone_number": "5551234567",
      "phone_verified": true
    },
    "vehicle": {
      "type": "sedan",
      "color": "blue",
      "plate": "ABC123",
      "make": "Toyota",
      "picture_front": "https://s3-us-west-2.amazonaws.com/bucket/user/xyz123.jpg",
      "picture_side": "https://s3-us-west-2.amazonaws.com/bucket/user/abc456.jpg"
    },
    "home": {
      "address": "123 Main St, Houston, TX",
      "latitude": 29.7604,
      "longitude": -95.3698
    },
    "office": {
      "address": "456 Business Ave, Houston, TX",  
      "latitude": 29.7500,
      "longitude": -95.3600
    },
    "avatar": "https://s3-us-west-2.amazonaws.com/bucket/user/def789.jpg",
    "rating": 4.8,
    "notification": {
      "user_informatics": {
        "road_incident": true,
        "construction_zone": true,
        "flood_warning": true,
        "transit_incident": false,
        "weather_alert": true
      }
    },
    "retention_plan": 1,
    "preferred_travel_mode": "transit",
    "enterprises": [
      {
        "id": 123,
        "email": "john.doe@company.com"
      }
    ],
    "employee_email": {
      "carpool": [
        {
          "enterprise_id": 123,
          "enterprise_email": "john.doe@company.com",
          "enterprise_name": "Company Inc"
        }
      ],
      "telework": []
    },
    "referral_code": "xyz123abc",
    "tier": {
      "current": "gold",
      "points": 1500
    }
  },
  "security_key": "secure_key_123"
}
```

### Vehicle Profile Response
```json
{
  "userId": 12345,
  "vehicle": {
    "type": "sedan",
    "color": "blue", 
    "plate": "ABC123",
    "make": "Toyota",
    "picture_front": "https://s3-us-west-2.amazonaws.com/bucket/user/xyz123.jpg",
    "picture_side": "https://s3-us-west-2.amazonaws.com/bucket/user/abc456.jpg"
  },
  "hasImages": {
    "front": true,
    "side": true
  }
}
```

### Location Summary Response
```json
{
  "userId": 12345,
  "home": {
    "address": "123 Main St, Houston, TX",
    "coordinates": {
      "latitude": 29.7604,
      "longitude": -95.3698
    },
    "isSet": true
  },
  "office": {
    "address": "456 Business Ave, Houston, TX",
    "coordinates": {
      "latitude": 29.7500,
      "longitude": -95.3600
    },
    "isSet": true
  }
}
```

### Notification Settings Response
```json
{
  "userId": 12345,
  "notifications": {
    "road_incident": true,
    "construction_zone": true,
    "flood_warning": true,
    "transit_incident": false,
    "weather_alert": true
  },
  "categories": {
    "safety": {
      "road_incident": true,
      "construction_zone": true,
      "flood_warning": true
    },
    "transportation": {
      "transit_incident": false
    },
    "weather": {
      "weather_alert": true
    }
  }
}
```

### Enterprise Affiliations Response
```json
{
  "userId": 12345,
  "enterprises": [
    {
      "id": 123,
      "email": "john.doe@company.com"
    }
  ],
  "employeeEmails": {
    "carpool": [
      {
        "enterprise_id": 123,
        "enterprise_email": "john.doe@company.com",
        "enterprise_name": "Company Inc"
      }
    ],
    "telework": []
  },
  "summary": {
    "totalEnterprises": 1,
    "carpoolEligible": 1,
    "teleworkEligible": 0
  }
}
```

## ⚠️ Important Notes

### Image Upload and Storage
- **AWS S3 Integration:** All images stored in S3 with CDN delivery
- **Hash-Based Naming:** Collision-resistant file naming using Hashids
- **Image Type Detection:** Automatic PNG/JPEG detection and appropriate handling
- **Base64 Processing:** Handles base64 encoded image uploads

### Multi-Database Architecture
- **Portal Database:** Main user profile data (auth_user, user_config tables)
- **Carpooling Database:** Enterprise and carpool-related data
- **Cross-Database Queries:** Complex joins across database boundaries
- **Transaction Safety:** Proper handling of multi-table updates

### Notification System Integration
- **Default Settings:** Comprehensive defaults for all notification types
- **User Customization:** Granular control over notification preferences
- **Backwards Compatibility:** Graceful handling of new notification types
- **JSON Storage:** Efficient storage of complex notification preferences

### Enterprise and B2B Features
- **Multi-Enterprise Support:** Users can belong to multiple enterprises
- **Carpool vs Telework:** Separate tracking of different program eligibilities
- **Email Verification:** Only verified enterprise emails are processed
- **Organization Integration:** Deep integration with organizational structures

### Security and Privacy
- **Security Key Management:** Separate security key handling
- **Email Privacy:** Multiple email address support with user control
- **Image Security:** Secure image upload and delivery
- **Data Validation:** Comprehensive input validation and sanitization

### Performance Considerations
- **CDN Delivery:** Fast image delivery through AWS CloudFront
- **Efficient Queries:** Optimized database queries with proper joins
- **Parallel Processing:** Concurrent enterprise data fetching
- **Image Processing:** Efficient base64 handling and S3 upload

### User Experience Features
- **Rich Profiles:** Comprehensive user profile management
- **Social Integration:** Support for multiple social media platforms
- **Location Services:** Home and office address management
- **Personalization:** Extensive customization options

## 🔗 Related File Links

- **S3 Service:** `allrepo/connectsmart/tsp-api/src/services/s3.js`
- **Tier Service:** `allrepo/connectsmart/tsp-api/src/services/tier.js`
- **User Models:** `allrepo/connectsmart/tsp-api/src/models/AuthUsers.js`
- **Enterprise Models:** `allrepo/connectsmart/tsp-api/src/models/Enterprises.js`

---
*This service provides essential comprehensive user profile management with advanced image handling, enterprise integration, and extensive customization features for the TSP platform.*