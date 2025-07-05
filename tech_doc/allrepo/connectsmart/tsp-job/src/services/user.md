# User Service

## Overview

The User Service provides comprehensive user profile management and data retrieval functionality. It handles user profile formatting, internationalization support, avatar management, and flexible metadata inclusion for various application contexts across the TSP platform.

## Service Information

- **Service Name**: User Service
- **File Path**: `/src/services/user.js`
- **Type**: User Profile Management Service
- **Dependencies**: AuthUsers Model, AWS S3 CDN, Application Configuration

## Core Functions

### profiles(userIds, meta = [])

Retrieves and formats user profiles with flexible metadata inclusion and internationalization support.

**Purpose**: Provides formatted user profile data with configurable additional information
**Parameters**:
- `userIds` (array): Array of user IDs to retrieve profiles for
- `meta` (array, optional): Array of metadata fields to include in response
**Returns**: Promise resolving to array of formatted user profile objects

**Base Profile Structure**:
```javascript
{
  id: 123,
  user_id: 123,                    // Duplicate for backward compatibility
  email: "user@example.com",
  name: {
    first_name: "John",
    last_name: "Doe"
  },
  full_name: "John D.",             // Formatted display name
  avatar: "https://s3.../avatar.jpg", // CDN URL
  rating: 4.8                       // User rating
}
```

**Usage Examples**:

**Basic Profile Retrieval**:
```javascript
const userService = require('@app/src/services/user');

const profiles = await userService.profiles([123, 456, 789]);
console.log(`Retrieved ${profiles.length} user profiles`);

profiles.forEach(profile => {
  console.log(`${profile.full_name} (${profile.email}) - Rating: ${profile.rating}`);
});
```

**Extended Profile with Metadata**:
```javascript
const extendedProfiles = await userService.profiles(
  [123, 456], 
  ['vehicle', 'phone', 'device']
);

extendedProfiles.forEach(profile => {
  console.log(`User: ${profile.full_name}`);
  console.log(`Vehicle: ${profile.vehicle.type} ${profile.vehicle.color}`);
  console.log(`Phone: +${profile.phone.country_code}${profile.phone.phone_number}`);
  console.log(`Device: ${profile.device.model} (${profile.device.language})`);
});
```

### Full Name Formatting Logic

The service implements sophisticated full name formatting with internationalization support:

**Chinese Name Detection**:
```javascript
const containsChinese = (text) => {
  return text.split('').some(char => 
    char.charCodeAt(0) >= 0x4e00 && char.charCodeAt(0) <= 0x9fff
  );
};
```

**Formatting Rules**:
```javascript
// Single name scenarios
if (!row.last_name) fullName = row.first_name;
if (!row.first_name) fullName = row.last_name;

// Dual name scenarios
if (!!row.first_name && !!row.last_name) {
  const hasChineseFirst = containsChinese(row.first_name);
  const hasChineseLast = containsChinese(row.last_name);
  
  if (hasChineseFirst || hasChineseLast) {
    // Chinese naming convention: LastFirst
    fullName = row.last_name + '' + row.first_name;
  } else {
    // Western naming convention: First Last Initial
    fullName = row.first_name + ' ' + row.last_name[0] + '.';
  }
}
```

**Formatting Examples**:
- **Western Names**: "John Smith" → "John S."
- **Chinese Names**: "张" + "伟" → "张伟"
- **Mixed Names**: "John" + "李" → "李John"
- **Single Names**: "Madonna" → "Madonna"

## Metadata Extensions

### Vehicle Information (`vehicle`)

Basic vehicle information for ride-sharing and carpool contexts.

**Data Structure**:
```javascript
vehicle: {
  type: "Toyota Camry",
  color: "Blue",
  plate: "ABC123"
}
```

**Usage Context**:
- Driver profile displays
- Carpool matching information
- Ride identification

### Detailed Vehicle Information (`vehicle_detail`)

Extended vehicle information including verification photos.

**Data Structure**:
```javascript
vehicle_detail: {
  type: "Toyota Camry",
  color: "Blue", 
  plate: "ABC123",
  picture_front: "https://s3.../front.jpg",
  picture_side: "https://s3.../side.jpg"
}
```

**Usage Context**:
- Driver verification screens
- Vehicle registration workflows
- Safety and security features

### Phone Information (`phone`)

Contact information with international formatting support.

**Data Structure**:
```javascript
phone: {
  country_code: "1",
  phone_number: "5551234567"
}
```

**Usage Context**:
- Emergency contact information
- Ride coordination communication
- Account verification

### Device Information (`device`)

Device and notification configuration data.

**Data Structure**:
```javascript
device: {
  model: "iPhone 12",
  language: "en",
  token_type: "apns",           // 'fcm' or 'apns'
  token: "device_token_string"
}
```

**Token Type Logic**:
```javascript
token_type: row.device_token ? 'fcm' : 'apns',
token: row.device_token ? row.device_token : row.apns_device_token
```

**Usage Context**:
- Push notification delivery
- Localization and language preferences
- Platform-specific features

### Dynamic Field Inclusion

The service supports dynamic inclusion of any database field:

**Custom Field Example**:
```javascript
const profiles = await userService.profiles([123], ['status', 'created_on', 'preferences']);

// Results in:
{
  id: 123,
  // ... base profile fields
  status: "active",
  created_on: "2024-01-01 00:00:00",
  preferences: "{\"theme\":\"dark\"}"
}
```

**Implementation Logic**:
```javascript
meta.forEach((data) => {
  switch (data) {
    case 'vehicle':
      // Special handling for vehicle data
      break;
    case 'phone':
      // Special handling for phone data
      break;
    default:
      // Dynamic field inclusion
      if (row[data]) {
        user[data] = row[data];
      }
  }
});
```

## CDN Integration

### cdnURL(path) Function

Generates complete CDN URLs for user-uploaded assets.

**Purpose**: Converts relative paths to fully qualified CDN URLs
**Parameters**:
- `path` (string): Relative path to asset
**Returns**: Complete HTTPS URL to asset

**Implementation**:
```javascript
function cdnURL(path) {
  return `https://s3-${awsConfig.region}.amazonaws.com/${awsConfig.s3.bucketName}/${path}`;
}
```

**Configuration Source**:
```javascript
const awsConfig = require('config').vendor.aws;

// Expected config structure:
{
  vendor: {
    aws: {
      region: "us-east-1",
      s3: {
        bucketName: "user-assets-bucket"
      }
    }
  }
}
```

**Usage Examples**:
```javascript
// Avatar URL generation
avatar: cdnURL(row.avatar)
// Result: "https://s3-us-east-1.amazonaws.com/user-assets-bucket/avatars/user123.jpg"

// Vehicle photo URLs
picture_front: cdnURL(row.vehicle_picture_front)
picture_side: cdnURL(row.vehicle_picture_side)
```

## Database Integration

### AuthUsers Model Integration

The service primarily interacts with the AuthUsers model:

**Query Pattern**:
```javascript
const rows = await AuthUsers.query().whereIn('id', userIds);
```

**Expected Database Schema**:
```sql
CREATE TABLE auth_users (
  id INT PRIMARY KEY,
  email VARCHAR(255),
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  avatar VARCHAR(255),
  rating DECIMAL(3,2),
  vehicle_type VARCHAR(100),
  vehicle_color VARCHAR(50),
  vehicle_plate VARCHAR(20),
  vehicle_picture_front VARCHAR(255),
  vehicle_picture_side VARCHAR(255),
  country_code VARCHAR(5),
  phone_number VARCHAR(20),
  device_model VARCHAR(100),
  device_language VARCHAR(10),
  device_token TEXT,
  apns_device_token TEXT,
  -- Additional dynamic fields
  status VARCHAR(20),
  created_on DATETIME,
  preferences TEXT
);
```

### Query Optimization

**Indexed Fields**:
- Primary key (id) for efficient lookups
- Email for unique constraint and searches
- Status for filtering active users

**Performance Considerations**:
```javascript
// Efficient batch retrieval
const profiles = await userService.profiles([1,2,3,4,5]); // Single query

// Avoid N+1 queries
// DON'T: Loop through individual profile calls
// DO: Pass array of IDs for batch processing
```

## Error Handling & Data Validation

### Missing Data Handling

The service gracefully handles missing or null data:

**Null Safety for Names**:
```javascript
if (!row.last_name) fullName = row.first_name;
if (!row.first_name) fullName = row.last_name;
```

**Conditional Field Inclusion**:
```javascript
if (row[data]) {
  user[data] = row[data];
}
```

**Default Values**:
- Empty strings for missing names result in empty `full_name`
- Missing avatar paths result in CDN URLs to null paths
- Missing metadata fields are omitted from response

### Data Consistency

**Rating Validation**:
- Database should enforce rating range (0.0 to 5.0)
- Display handles null ratings gracefully

**Phone Number Formatting**:
- Stores country code and number separately
- Supports international formatting

**Device Token Management**:
- Prioritizes FCM tokens over APNS tokens
- Handles missing tokens for notification services

## Performance Optimization

### Batch Processing

The service is optimized for batch user retrieval:

```javascript
// Efficient: Single database query
const profiles = await userService.profiles([1,2,3,4,5,6,7,8,9,10]);

// Inefficient: Multiple queries
for (const userId of userIds) {
  const profile = await userService.profiles([userId]); // Don't do this
}
```

### Memory Management

**Large Batch Considerations**:
```javascript
// For very large user sets, consider chunking
const chunkSize = 100;
const userChunks = chunk(userIds, chunkSize);
const allProfiles = [];

for (const chunk of userChunks) {
  const chunkProfiles = await userService.profiles(chunk, meta);
  allProfiles.push(...chunkProfiles);
}
```

### CDN Caching

CDN URLs benefit from browser and CDN caching:
- **Static URLs**: Same path always generates same URL
- **Cache Headers**: S3 can be configured with appropriate cache headers
- **CDN Distribution**: CloudFront or similar CDN for global distribution

## Security Considerations

### Data Privacy

**Personal Information Handling**:
- Email addresses included in profile data
- Phone numbers only included when explicitly requested
- Device tokens handled securely for notifications

**Access Control**:
- Service doesn't implement user-level access control
- Calling code responsible for authorization
- Consider implementing data filtering based on privacy settings

### Input Validation

**User ID Validation**:
```javascript
const validateUserIds = (userIds) => {
  if (!Array.isArray(userIds)) {
    throw new Error('userIds must be an array');
  }
  
  if (userIds.some(id => typeof id !== 'number' || id <= 0)) {
    throw new Error('All user IDs must be positive numbers');
  }
  
  if (userIds.length > 1000) {
    throw new Error('Too many user IDs requested');
  }
};
```

### CDN Security

**URL Generation**:
- Uses HTTPS for all CDN URLs
- Bucket permissions should restrict direct access
- Consider signed URLs for sensitive assets

## Integration Patterns

### Common Usage Patterns

**Profile Display**:
```javascript
// User profile page
const profile = await userService.profiles([userId], ['vehicle', 'phone'])[0];
```

**Driver Lists**:
```javascript
// Available drivers
const drivers = await userService.profiles(driverIds, ['vehicle', 'device']);
```

**Contact Information**:
```javascript
// Emergency contacts
const contacts = await userService.profiles(contactIds, ['phone']);
```

**Notification Targeting**:
```javascript
// Push notification recipients
const recipients = await userService.profiles(userIds, ['device']);
const tokens = recipients.map(user => user.device.token).filter(Boolean);
```

### API Response Formatting

**Standard API Response**:
```javascript
const formatUserResponse = async (userIds, meta = []) => {
  try {
    const profiles = await userService.profiles(userIds, meta);
    return {
      success: true,
      data: profiles,
      count: profiles.length
    };
  } catch (error) {
    return {
      success: false,
      error: error.message,
      data: []
    };
  }
};
```

## Testing Strategies

### Unit Testing

```javascript
const userService = require('@app/src/services/user');

describe('User Service', () => {
  test('formats Western names correctly', async () => {
    // Mock AuthUsers.query()
    const mockUser = {
      id: 123,
      first_name: 'John',
      last_name: 'Smith',
      email: 'john@example.com',
      rating: 4.5,
      avatar: 'avatars/john.jpg'
    };
    
    AuthUsers.query = jest.fn().mockReturnValue({
      whereIn: jest.fn().mockResolvedValue([mockUser])
    });
    
    const profiles = await userService.profiles([123]);
    expect(profiles[0].full_name).toBe('John S.');
  });
  
  test('formats Chinese names correctly', async () => {
    const mockUser = {
      id: 124,
      first_name: '伟',
      last_name: '张',
      email: 'zhang@example.com',
      rating: 4.8,
      avatar: 'avatars/zhang.jpg'
    };
    
    const profiles = await userService.profiles([124]);
    expect(profiles[0].full_name).toBe('张伟');
  });
});
```

### Integration Testing

**Database Integration**:
```javascript
test('retrieves real user profiles from database', async () => {
  const profiles = await userService.profiles([1, 2, 3]);
  expect(profiles).toHaveLength(3);
  expect(profiles[0]).toHaveProperty('id');
  expect(profiles[0]).toHaveProperty('email');
  expect(profiles[0]).toHaveProperty('full_name');
});
```

**CDN Integration**:
```javascript
test('generates valid CDN URLs', () => {
  const url = userService.cdnURL('avatars/test.jpg');
  expect(url).toMatch(/^https:\/\/s3-/);
  expect(url).toContain('avatars/test.jpg');
});
```

## Configuration Requirements

### AWS Configuration

**Required Config Structure**:
```javascript
module.exports = {
  vendor: {
    aws: {
      region: process.env.AWS_REGION || 'us-east-1',
      s3: {
        bucketName: process.env.S3_BUCKET_NAME || 'user-assets'
      }
    }
  }
};
```

### Environment Variables

```bash
# AWS S3 Configuration
AWS_REGION=us-east-1
S3_BUCKET_NAME=maas-user-assets

# Database Configuration
DB_HOST=localhost
DB_NAME=portal
DB_USER=app_user
DB_PASS=secure_password
```

## Migration & Deployment

### Database Migration Considerations

**Schema Changes**:
- Adding new metadata fields requires no code changes
- Removing fields needs service update to avoid errors
- Changing field types requires data migration

**Backward Compatibility**:
- Maintain dual field support during transitions
- Use feature flags for new metadata types
- Version API responses appropriately

### CDN Migration

**Bucket Changes**:
- Update configuration for new bucket names
- Implement gradual migration for existing assets
- Verify CORS settings for new buckets

## Dependencies

- **AuthUsers**: User model for database access
- **config**: Application configuration management for AWS settings
- **@maas/core/log**: Logging system for debugging and monitoring