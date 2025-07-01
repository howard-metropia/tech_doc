# AuthUserEvent Model Documentation

## 📋 Model Overview
- **Purpose:** Tracks user authentication and activity events
- **Table/Collection:** auth_user_event
- **Database Type:** MySQL
- **Relationships:** Links to user authentication system for event logging

## 🔧 Schema Definition
Schema details not explicitly defined in model file. This table likely stores user authentication events and activity logs.

## 🔑 Key Information
- **Primary Key:** Likely id (standard MySQL convention)
- **Indexes:** Not defined in model (handled at database level)
- **Unique Constraints:** Not defined in model
- **Default Values:** Not defined in model

## 📝 Usage Examples
```javascript
// Query user events
const userEvents = await AuthUserEvent.query()
  .where('user_id', 12345)
  .orderBy('created_at', 'desc');

// Log new authentication event
const loginEvent = await AuthUserEvent.query()
  .insert({
    user_id: 12345,
    event_type: 'login',
    ip_address: '192.168.1.1',
    user_agent: 'Mozilla/5.0...',
    timestamp: new Date()
  });

// Find recent failed login attempts
const failedLogins = await AuthUserEvent.query()
  .where('event_type', 'login_failed')
  .where('created_at', '>', new Date(Date.now() - 24*60*60*1000));
```

## 🔗 Related Models
- **AuthUsers** - Source of user data for event tracking
- **User session models** - Related to authentication state
- **Security audit models** - Part of security monitoring system
- **Activity log models** - General user activity tracking

## 📌 Important Notes
- Missing Model import from 'objection' (implementation issue)
- Critical for security auditing and user activity monitoring
- Likely tracks login, logout, password changes, and other auth events
- Connected to 'portal' MySQL database
- Important for compliance and security analysis
- Supports forensic investigation of user activities

## 🏷️ Tags
**Keywords:** auth, user, event, activity, security, audit
**Category:** #model #database #mysql #authentication #audit