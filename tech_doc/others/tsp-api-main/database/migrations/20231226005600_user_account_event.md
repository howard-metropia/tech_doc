# Migration Documentation

## 📋 Migration Overview
- **Purpose:** Create user account event tracking and backup system
- **Date:** 2023-12-26 00:56:00
- **Ticket:** N/A
- **Risk Level:** Low

## 🔧 Schema Changes
```sql
CREATE TABLE auth_user_event (id, auth_user_bk_id, auth_user_id, event, login_type, purge_status, created_at, updated_at);
CREATE TABLE auth_user_bk (id, auth_user_id, bk_timestamp, first_name, last_name, email, common_email, google_email, facebook_email, apple_email, ...);
```

## 📝 Changes Summary
| Operation | Table/Collection | Field/Index | Description |
|-----------|-----------------|-------------|-------------|
| CREATE | auth_user_event | - | User account event tracking table |
| CREATE | auth_user_bk | - | User account backup/history table |
| ADD | auth_user_event | event | Event types: register, merge, login, delete, change_tel |
| ADD | auth_user_event | login_type | OAuth provider: apple, google, facebook, common_email |
| ADD | auth_user_bk | All user fields | Complete user profile backup |

## ⬆️ Up Migration
- Creates comprehensive user account event tracking system
- Creates full user account backup table with all profile fields
- Supports multiple OAuth providers (Apple, Google, Facebook)
- Tracks account lifecycle events (register, merge, login, delete)
- Includes purge status tracking for account deletion events

## ⬇️ Down Migration
- Drops both auth_user_event and auth_user_bk tables
- Removes all user event tracking and backup capabilities

## ⚠️ Important Notes
- Comprehensive user data backup including all profile fields
- Supports multiple email addresses per user (OAuth providers)
- Tracks account deletion and purge status
- Large table creation with 80+ fields for complete user backup

## 🏷️ Tags
**Keywords:** user, account, event, backup, oauth, tracking, history
**Category:** #migration #database #schema #user #auth #tracking #backup