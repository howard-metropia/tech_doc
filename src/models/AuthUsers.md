# AuthUsers Model Documentation

## 📋 Model Overview
- **Purpose:** Manages user authentication and core user information
- **Table/Collection:** auth_user
- **Database Type:** MySQL (portal database)
- **Relationships:** Referenced by multiple models for user associations

## 🔧 Schema Definition
| **Field Name** | **Type** | **Required** | **Description** |
|----------------|----------|--------------|-----------------|
| id | INT | Yes | Primary key, auto-increment |
| username | VARCHAR | Yes | Unique username for login |
| email | VARCHAR | Yes | User email address |
| password | VARCHAR | Yes | Hashed password |
| status | VARCHAR | No | User account status (active/inactive/suspended) |
| created_at | TIMESTAMP | Yes | Account creation timestamp |
| updated_at | TIMESTAMP | Yes | Last update timestamp |

## 🔑 Key Information
- **Primary Key:** id
- **Indexes:** username (unique), email (unique), status
- **Unique Constraints:** username, email
- **Default Values:** status = 'active', created_at = CURRENT_TIMESTAMP

## 📝 Usage Examples
```javascript
// Basic query example
const users = await AuthUsers.query().where('status', 'active');

// Find user by email
const user = await AuthUsers.query().where('email', 'user@example.com').first();

// Update user status
await AuthUsers.query().where('id', userId).update({ status: 'suspended' });
```

## 🔗 Related Models
- `UserWallets` - One-to-one relationship via user_id
- `Trips` - One-to-many relationship via user_id
- `Reservations` - One-to-many relationship via user_id
- `CoinActivityLogs` - One-to-many relationship via user_id

## 📌 Important Notes
- Password field stores hashed values using bcrypt
- User authentication is handled via JWT tokens
- Status field controls access to the platform
- Email verification may be required based on configuration

## 🏷️ Tags
**Keywords:** authentication, users, login, security, portal
**Category:** #model #database #authentication #mysql

---
Note: This model serves as the foundation for user authentication across the MaaS platform.