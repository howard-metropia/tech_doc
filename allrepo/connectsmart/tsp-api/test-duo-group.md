# Test Documentation: Duo Group API

## Overview
This test suite validates the Duo Group functionality, which enables users to create and manage carpooling groups within the TSP (Transportation Service Provider) system. The test suite provides comprehensive coverage of group management operations, member management, and admin functionality.

## Test Configuration
- **File**: `test/test-duo-group.js`
- **Framework**: Mocha with Chai assertions and Supertest for HTTP testing
- **Test Timeout**: 5 seconds for most operations
- **Models Used**: `DuoGroups`, `DuoGroupMembers`
- **Authentication**: User ID-based authentication with test users (1005, 1003, 1004)

## Test Data Structure

### Group Data
```javascript
const groupData = {
  name: 'Unit-Test duo group',
  description: 'This group is created by unit-test',
  types: [1, 5],
  is_private: false,
  geofence: {
    latitude: 123.123456,
    longitude: 987.987654,
    radius: 50,
    address: 'TEST ADDRESS',
  },
  enterprise_id: 1,
};
```

### Admin Profile Data
```javascript
const adminProfile = {
  introduction: 'This admin profile is created by unit test',
  open_contact: true,
  gender: 'other',
  email: 'unit_test@metropia.com',
  linkedin_url: 'linkedin.com/in/unit_test',
  facebook_url: 'facebook.com/unit_test',
  twitter_url: 'twitter.com/unit_test',
};
```

## API Endpoints Tested

### 1. Create Duo Group - `POST /duo_group`
**Purpose**: Creates a new duo group for carpooling

**Success Scenario**:
- Creates duo group with valid data
- Returns success with group ID
- Validates group properties

**Error Scenarios**:
- `10004`: Request header missing (no userid)
- `10002`: Required field validation (name required)
- `21001`: Duplicate group name validation

### 2. Get Duo Groups - `GET /duo_group`
**Purpose**: Retrieves all duo groups for the authenticated user

**Success Scenario**:
- Returns paginated list of groups
- Includes group details, members, and enterprise information
- Validates response structure with required keys

**Error Scenarios**:
- `10004`: Missing authentication header
- `10001`: Invalid sort parameter validation

### 3. Update Duo Group - `PUT /duo_group/:id`
**Purpose**: Updates existing duo group properties

**Success Scenario**:
- Updates group with valid data
- Returns empty success response
- Validates ownership permissions

**Error Scenarios**:
- `10004`: Missing authentication
- `10002`: Invalid data type validation
- `21003`: Group not found
- `21006`: No permissions (non-owner)

### 4. Create Admin Profile - `POST /duo_group/admin_profile`
**Purpose**: Creates admin profile for group management

**Success Scenario**:
- Creates admin profile with social links and contact info
- Returns group data with admin profile and security key
- Links profile to group creator

**Error Scenarios**:
- `10004`: Missing authentication
- `10002`: Required group_id validation
- `21003`: Group not found
- `21006`: No permissions (non-creator)

### 5. Get Admin Profile - `GET /duo_group/admin_profile/:group_id`
**Purpose**: Retrieves admin profile for a specific group

**Success Scenario**:
- Returns admin profile with user details and security key
- Includes social media links and contact information

**Error Scenarios**:
- `10004`: Missing authentication
- `10001`: Invalid group_id parameter
- `21003`: Group not found

### 6. Get Last Admin Profile - `GET /duo_group/last_admin_profile`
**Purpose**: Retrieves the most recent admin profile for the user

**Success Scenario**:
- Returns latest admin profile data
- Includes security key for verification

**Error Scenarios**:
- `10004`: Missing authentication

### 7. Search Duo Groups - `GET /duo_group/search`
**Purpose**: Searches for duo groups by name or criteria

**Success Scenario**:
- Returns matching groups with geofence details
- Flattens geofence structure for response format
- Supports case-insensitive search

**Error Scenarios**:
- `10004`: Missing authentication
- `10001`: Missing search query parameter

### 8. Join Group - `POST /duo_group/join`
**Purpose**: Allows users to request joining a duo group

**Success Scenario**:
- Creates join request with pending status
- Returns request ID and status (1 = pending)

**Error Scenarios**:
- `10004`: Missing authentication
- `10002`: Required group_id validation
- `21003`: Group not found
- `21009`: Already requested to join
- `21005`: User already in group

### 9. Cancel Join Request - `POST /duo_group/cancel`
**Purpose**: Cancels a pending join request

**Success Scenario**:
- Removes pending join request
- Returns empty success response

**Error Scenarios**:
- `10004`: Missing authentication
- `10002`: Required group_id validation
- `21003`: Group not found
- `21008`: No pending join request found
- `21005`: User already member

### 10. Accept User - `POST /duo_group/accept_user`
**Purpose**: Admin accepts a user's join request

**Success Scenario**:
- Converts pending request to membership
- Admin-only operation with permission validation

**Error Scenarios**:
- `10004`: Missing authentication
- `10002`: Required parameters validation
- `21003`: Group not found
- `21005`: User already member
- `21006`: No admin permissions

### 11. Set Admin User - `POST /duo_group/set_admin`
**Purpose**: Promotes a group member to admin status

**Success Scenario**:
- Elevates member to management role
- Creator-only operation

**Error Scenarios**:
- `10004`: Missing authentication
- `10002`: Required parameters validation
- `21003`: Group not found
- `21016`: User not a group member
- `21006`: No permissions (non-creator)

### 12. Leave Group - `POST /duo_group/leave`
**Purpose**: Allows users to leave a duo group

**Success Scenario**:
- Removes user from group membership
- Updates member status

**Error Scenarios**:
- `10004`: Missing authentication
- `10002`: Required group_id validation
- `21003`: Group not found
- `21016`: Not a group member

### 13. Add User - `POST /duo_group/add_user`
**Purpose**: Admin directly adds a user to the group

**Success Scenario**:
- Adds user with accepted status (2)
- Bypasses join request process
- Admin-only operation

**Error Scenarios**:
- `10004`: Missing authentication
- `10002`: Required parameters validation
- `21003`: Group not found
- `21005`: User already member
- `21006`: No admin permissions

### 14. Get Members - `GET /duo_group/member`
**Purpose**: Retrieves paginated list of group members

**Success Scenario**:
- Returns member list with user details and ratings
- Includes security key and pagination data
- Shows member profiles and blacklist status

**Error Scenarios**:
- `10004`: Missing authentication
- `21003`: Group not found

### 15. Get Member Profile - `GET /duo_group/member_profile`
**Purpose**: Retrieves detailed profile of a specific member

**Success Scenario**:
- Returns comprehensive member profile
- Includes vehicle info, social media, and ride statistics
- Shows matching compatibility and blacklist status

**Error Scenarios**:
- `10004`: Missing authentication
- `10001`: Required user_id parameter
- `20001`: Member profile not found

### 16. Remove User - `POST /duo_group/remove_user`
**Purpose**: Admin removes a user from the group

**Success Scenario**:
- Removes user from group membership
- Admin-only operation with permission validation
- Prevents self-removal by admin

**Error Scenarios**:
- `10004`: Missing authentication
- `10002`: Required parameters validation
- `21003`: Group not found
- `21016`: User not a member
- `21006`: No permissions or attempting self-removal

### 17. Reject User - `POST /duo_group/reject_user`
**Purpose**: Admin rejects a user's join request

**Success Scenario**:
- Rejects pending join request with reason/comment
- Removes request from pending status
- Admin-only operation

**Error Scenarios**:
- `10004`: Missing authentication
- `10002`: Required parameters validation
- `21003`: Group not found
- `21005`: User already member
- `21006`: No admin permissions
- `21008`: No pending join request

### 18. Delete Group - `DELETE /duo_group/:id`
**Purpose**: Permanently deletes a duo group

**Success Scenario**:
- Removes group and associated data
- Creator-only operation
- Returns empty success response

**Error Scenarios**:
- `10004`: Missing authentication
- `21003`: Group not found
- `21006`: No permissions (non-creator)

## Member Status Types
- **Status 1**: Pending join request
- **Status 2**: Accepted member
- **Management**: Admin/moderator role

## Key Features Tested

### Group Management
- CRUD operations for duo groups
- Privacy settings and geofencing
- Enterprise association
- Group search and discovery

### Member Management
- Join request workflow
- Member acceptance/rejection with reasons
- Admin role promotion
- Member removal and departure

### Admin Features
- Admin profile creation with social media links
- Permission-based operations
- Group moderation capabilities
- Security key generation

### Data Validation
- Required field validation
- Parameter type checking
- Permission verification
- Duplicate prevention

### Error Handling
- Authentication validation
- Resource existence checks
- Permission enforcement
- Business rule validation

## Security Features
- User ID-based authentication
- Role-based access control
- Creator/admin permission separation
- Security key generation for sensitive operations

## Test Coverage
The test suite provides comprehensive coverage of:
- All CRUD operations for duo groups
- Complete member lifecycle management
- Admin functionality and permissions  
- Error scenarios and edge cases
- Data validation and security checks
- Geofencing and enterprise integration

This test suite ensures the duo group system functions correctly for carpooling community management within the TSP platform.