# Test Documentation: Enterprise API

## Overview
This test suite validates the Enterprise functionality, which manages corporate organization integration within the TSP system. The test covers enterprise email verification, telework management, and organizational domain validation for corporate carpooling programs.

## Test Configuration
- **File**: `test/test-enterprise.js`
- **Framework**: Mocha with Chai assertions and Supertest for HTTP testing
- **Test Timeout**: 10 seconds for email operations, 5 seconds for other tests
- **Models Used**: `DuoGroups`, `Enterprises`, `DuoGroupMembers`, `AuthUsers`
- **Database**: Uses Knex for raw SQL operations on carpooling schema
- **Authentication**: Bearer token-based authentication

## Test Data Structure

### Enterprise Setup Data
```javascript
const testData = {
  userId: 1003,
  testEmail: 'unit-test@abc.com',
  existedEmail: 'existed@abc.com',
  enterpriseId: 336, // Dynamic from org_setting insert
  testDomain: 'abc.com',
  testGroupId: 80,
};
```

### Organization Configuration
```javascript
const orgSetting = {
  code_name: 'abc',
  logo_img_menu: ' ',
  logo_img_index: '',
  name_zh: 'abc',
  name_en: 'abc',
  address: 'taiwan',
  create_user: '1',
  is_telework: 1,
};
```

## Database Schema Integration

### Tables Used
- `carpooling.org_setting` - Organization configuration
- `carpooling.org_setting_domain` - Domain validation
- `carpooling.org_setting_area` - Geographic areas
- `DuoGroups` - Corporate carpooling groups
- `Enterprises` - User-enterprise relationships
- `DuoGroupMembers` - Group membership

## API Endpoints Tested

### 1. Send Verification Email - `POST /setting_carpool_email`
**Purpose**: Sends email verification for enterprise carpool registration

**Request Data**:
```javascript
{
  email: 'unit-test@abc.com',
  verify_type: 'carpool',
  group_id: 80
}
```

**Success Scenario**:
- Validates email domain against organization settings
- Sends verification email with JWT token
- Returns empty success response
- Associates email with duo group

**Error Scenarios**:
- `10003`: Missing Authorization token
- `10002`: Required email field validation
- `20018`: Invalid email domain for group
- `20020`: Email already registered

### 2. Verify Email - `GET /verify_carpool_email.html`
**Purpose**: HTML endpoint for email verification completion

**Success Scenarios**:
- **Valid Token**: Returns success page with "officially joined" message
- **Already Verified**: Returns "Verification passed" message
- **Invalid Token**: Returns "Invalid validation token" error
- **Expired/Malformed**: Returns "Unable verify email" error

**Response Format**: HTML pages (not JSON API responses)

### 3. Delete Enterprise - `POST /enterprise/delete`
**Purpose**: Removes unverified enterprise email associations

**Request Data**:
```javascript
{
  user_id: 1003,
  enterprise_id: 25
}
```

**Success Scenario**:
- Deletes enterprise relationship
- Returns security key for confirmation
- Cleans up unverified associations

**Error Scenarios**:
- `10003`: Missing Authorization token
- `10002`: Required user_id validation

### 4. Search Telework - `GET /telework/search`
**Purpose**: Searches for telework organizations by email domain

**Query Parameters**:
- `email`: Email address to check for enterprise association

**Success Scenario**:
- Returns enterprise list matching email domain
- Includes enterprise details and verification status
- Shows duo group associations

**Response Structure**:
```javascript
{
  list: [{
    enterprise_id: 336,
    enterprise_name: 'abc',
    enterprise_email: 'unit-test@abc.com',
    email_verify_status: true,
    avatar: '',
    duo_group_id: 80,
    status: 1
  }],
  security_key: 'generated_key'
}
```

**Error Scenarios**:
- `10003`: Missing Authorization token
- `10001`: Required email parameter

### 5. Get Telework - `GET /telework`
**Purpose**: Retrieves user's telework enterprise associations

**Success Scenario**:
- Returns all user's verified enterprise associations
- Includes telework status flag
- Shows enterprise and group relationships

**Response Structure**:
```javascript
{
  list: [{
    enterprise_id: 336,
    enterprise_name: 'abc',
    enterprise_email: 'unit-test@abc.com',
    email_verify_status: true,
    avatar: '',
    duo_group_id: 80,
    chk_telework: true
  }],
  security_key: 'generated_key'
}
```

**Error Scenarios**:
- `10003`: Missing Authorization token

### 6. Update Telework - `POST /telework`
**Purpose**: Updates telework status for an enterprise association

**Request Data**:
```javascript
{
  enterprise_id: 336,
  chk_telework: false
}
```

**Success Scenario**:
- Updates telework preference
- Returns updated enterprise list
- Toggles telework availability

**Error Scenarios**:
- `10003`: Missing Authorization token
- `10002`: Required enterprise_id validation

## Test Data Setup and Cleanup

### Before Hook (Setup)
1. **Token Retrieval**: Fetches Bearer token from AuthUsers table
2. **Organization Creation**: Creates test organization in org_setting
3. **Domain Setup**: Adds domain validation record
4. **Area Configuration**: Creates geographic area record
5. **Group Creation**: Sets up duo group for enterprise
6. **Enterprise Association**: Links user to enterprise with verification
7. **Member Setup**: Adds users to duo group with different roles

### After Hook (Cleanup)
1. **Group Deletion**: Removes test duo group
2. **Enterprise Cleanup**: Deletes enterprise associations
3. **Member Cleanup**: Removes group memberships
4. **Schema Cleanup**: Removes org_setting records and dependencies

## Key Features Tested

### Email Verification Flow
- Domain validation against organization settings
- JWT token generation and validation
- HTML response rendering for verification pages
- Duplicate email prevention

### Enterprise Management
- Organization-user relationship management
- Domain-based email validation
- Enterprise deletion and cleanup
- Multi-user enterprise support

### Telework Integration
- Telework status management
- Enterprise search by email domain
- User preference toggling
- Corporate carpooling integration

### Security Features
- Bearer token authentication
- Domain validation for email registration
- Security key generation
- User ownership validation

## Error Handling Patterns

### Authentication Errors
- `10003`: Token required - Missing or invalid Bearer token
- JWT token validation for email verification

### Validation Errors
- `10002`: Required field validation
- `10001`: Parameter validation and format checking

### Business Logic Errors
- `20018`: Domain validation for enterprise email
- `20020`: Duplicate email prevention

## Database Integration
The test suite demonstrates complex database operations:
- Multi-table relationships between organizations, domains, and users
- Transaction handling for data consistency
- Foreign key relationships and constraint handling
- Data cleanup and integrity maintenance

## Corporate Features
- **Domain Validation**: Ensures users belong to registered organizations
- **Telework Management**: Enables/disables remote work carpooling
- **Group Integration**: Links enterprises to carpooling groups
- **Multi-tenant Support**: Handles multiple organizations and domains

## Test Coverage
The test suite provides comprehensive coverage of:
- Complete email verification workflow
- Enterprise-user association management
- Telework preference management
- Domain validation and security
- HTML page rendering for verification
- Database schema integrity
- Authentication and authorization
- Error scenarios and edge cases

This test suite ensures the enterprise integration functions correctly for corporate carpooling programs within the TSP platform.