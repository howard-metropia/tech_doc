# TmpUser Model Documentation

## 📋 Model Overview
- **Purpose:** Temporary user storage for registration and authentication processes
- **Table/Collection:** tmp_user
- **Database Type:** MongoDB
- **Relationships:** Temporary staging for AuthUsers creation

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|------------------|
| _id | ObjectId | Yes | MongoDB document identifier |
| registration_id | String | No | Unique registration session ID |
| first_name | String | No | User's first name |
| last_name | String | No | User's last name |
| email | String | No | Primary email address |
| google_email | String | No | Google account email |
| facebook_email | String | No | Facebook account email |
| apple_email | String | No | Apple ID email |
| phone_number | String | No | Phone number |
| verification_code | String | No | Email/SMS verification code |
| verification_expires | Date | No | Code expiration time |
| oauth_data | Object | No | OAuth provider data |
| device_info | Object | No | Device registration info |
| created_at | Date | No | Temporary record creation |

## 🔑 Key Information
- **Primary Key:** _id (MongoDB ObjectId)
- **Indexes:** Likely on registration_id, email fields
- **Unique Constraints:** None (temporary data)
- **Default Values:** Flexible schema allows additional fields

## 📝 Usage Examples
```javascript
// Create temporary user during registration
const tmpUser = new TempUser({
  registration_id: generateRegistrationId(),
  first_name: 'John',
  last_name: 'Doe',
  email: 'john@example.com',
  verification_code: '123456',
  verification_expires: new Date(Date.now() + 10*60*1000) // 10 minutes
});
await tmpUser.save();

// Verify user and complete registration
const tmp = await TempUser.findOne({
  registration_id: regId,
  verification_code: code,
  verification_expires: { $gte: new Date() }
});

// Clean up after successful registration
await TempUser.deleteOne({ _id: tmp._id });
```

## 🔗 Related Models
- **AuthUsers**: Temporary users become permanent users after verification
- **UserProfiles**: Profile data may be pre-populated from temp data

## 📌 Important Notes
- Uses flexible schema (strict: false) for varying registration flows
- Supports multiple OAuth provider emails
- Temporary storage with manual cleanup after registration
- Verification code system for email/phone validation
- Consider TTL index for automatic cleanup of expired records

## 🏷️ Tags
**Keywords:** temporary, registration, verification, oauth
**Category:** #model #database #authentication #temporary