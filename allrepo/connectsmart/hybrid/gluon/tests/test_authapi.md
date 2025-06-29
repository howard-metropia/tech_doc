# test_authapi.py

## Overview
This file contains comprehensive unit tests for the web2py AuthAPI system. It tests the authentication API functionality including user registration, login, logout, profile management, password changes, and email verification processes.

## Purpose
- Tests AuthAPI class functionality for programmatic authentication
- Validates user registration with various configurations
- Tests login/logout operations and session management
- Verifies profile update and password change features
- Tests email verification and registration approval workflows

## Key Classes and Methods

### TestAuthAPI Class
A comprehensive test suite for the AuthAPI authentication system.

#### Setup Method

##### `setUp(self)`
Initializes the test environment with:
- Request, Response, and Session objects
- Database connection with authentication tables
- AuthAPI instance configuration
- Sample user creation for testing
- Global context setup for web2py environment

**Created Test User:**
- Username: "bart"
- Email: "bart@simpson.com"
- Password: "bart_password"
- Name: "Bart Simpson"

#### Test Methods

##### `test_login(self)`
Tests user authentication functionality.
- **Basic Login**: Tests login with correct credentials
- **Login State**: Verifies `is_logged_in()` returns True after login
- **User Data**: Validates returned user information
- **Logout**: Tests logout functionality and state change
- **Case Sensitivity**: Tests case-insensitive username login

**Test Scenarios:**
- Successful login with correct credentials
- User state verification after login
- Logout and state verification
- Case-insensitive username handling

##### `test_logout(self)`
Tests user logout functionality.
- **Logout Process**: Tests logout after successful login
- **State Verification**: Ensures `is_logged_in()` returns False
- **User Data**: Validates user data is cleared after logout

##### `test_register(self)`
Comprehensive user registration testing.
- **Registration with Auto-Login**: Tests `login_after_registration = True`
- **Duplicate Registration Prevention**: Tests preventing registration while logged in
- **Registration without Auto-Login**: Tests `login_after_registration = False`
- **Email Field Login**: Tests using email as login field
- **Duplicate Email Handling**: Tests error handling for duplicate emails
- **Email Verification**: Tests registration requiring email verification

**Test User Created:**
- Username: "lisa"
- Email: "lisa@simpson.com"
- Password: "lisa_password"
- Name: "Lisa Simpson"

##### `test_profile(self)`
Tests user profile management.
- **Authentication Required**: Tests that profile access requires login
- **Profile Update**: Tests updating user profile information
- **Database Persistence**: Verifies profile changes are saved to database

**Profile Update Test:**
- Changes email from "bart@simpson.com" to "bartolo@simpson.com"
- Verifies update in both return value and database

##### `test_change_password(self)`
Tests password change functionality.
- **Authentication Required**: Tests that password change requires login
- **Successful Change**: Tests valid password change process
- **Password Validation**: Tests various validation scenarios
- **Minimum Length**: Tests minimum password length enforcement

**Test Scenarios:**
- Password change with correct old password
- Mismatch between new password confirmations
- Incorrect old password handling
- Minimum password length validation (4 characters)

##### `test_verify_key(self)`
Tests email verification system.
- **Registration with Verification**: Tests registration requiring verification
- **Key Generation**: Validates verification key generation
- **Invalid Key Handling**: Tests error handling for invalid keys
- **Successful Verification**: Tests successful key verification
- **Approval Workflow**: Tests registration requiring approval after verification

**Test Users Created:**
- Homer Simpson (verification required)
- Lisa Simpson (verification + approval required)

## Dependencies
- `unittest` - Python testing framework
- `os` - Environment variable access
- `gluon._compat` - Compatibility utilities
- `gluon.authapi.AuthAPI` - Authentication API class
- `gluon.dal` - Database Abstraction Layer
- `gluon.globals` - Global context objects
- `gluon.languages` - Internationalization support
- `gluon.storage` - Storage utilities

## Configuration
- `DEFAULT_URI` - Database connection string from environment or SQLite memory default

## Usage Example
```python
# Run specific test
python -m unittest test_authapi.TestAuthAPI.test_login

# Run all auth API tests
python -m unittest test_authapi.TestAuthAPI

# Test specific functionality
auth = AuthAPI(db)
result = auth.login(username="bart", password="bart_password")
if result['user']:
    print("Login successful")
```

## Integration with web2py Framework

### Database Integration
- Uses web2py's DAL for database operations
- Integrates with auth table structure
- Supports field validation and constraints

### Session Management
- Integrates with web2py session system
- Maintains authentication state across requests
- Supports session-based user tracking

### Validation and Security
- Uses web2py validators for input validation
- Implements secure password handling
- Supports email verification workflows

### Configuration Management
- Supports various authentication settings
- Configurable registration and verification options
- Flexible user field mapping

## API Methods Tested

### Authentication Methods
- `login(**credentials)` - User authentication
- `logout()` - User logout
- `is_logged_in()` - Authentication state check

### User Management Methods
- `register(**user_data)` - User registration
- `profile(**profile_data)` - Profile updates
- `change_password()` - Password modification

### Verification Methods
- `verify_key(key)` - Email verification
- Key generation and validation

## Test Coverage
- **Login/Logout**: Complete authentication cycle
- **Registration**: Various registration scenarios
- **Profile Management**: User data updates
- **Password Security**: Password change and validation
- **Email Verification**: Verification key handling
- **Error Handling**: Invalid inputs and edge cases
- **Configuration**: Different auth settings

## Expected Behavior
- All authentication operations should work programmatically
- User state should be maintained correctly
- Validation should prevent invalid operations
- Email verification should work end-to-end
- Error handling should provide meaningful feedback

## File Structure
```
gluon/tests/
├── test_authapi.py       # This file
└── ... (other test files)
```

This test suite ensures the web2py AuthAPI provides reliable and secure authentication functionality for programmatic use cases.