# testUseridType.py

## Overview
This file contains unit tests for testing user ID type handling in the portal application. It validates that the authentication system correctly handles both integer and string user ID types, ensuring consistent behavior across different data representations.

## Purpose
- Tests user ID type compatibility between integer and string formats
- Validates user authentication and login functionality
- Ensures database queries work correctly with different ID types
- Tests web2py's authentication system integration

## Key Classes and Methods

### TestUseridType Class
A unittest.TestCase subclass that tests user ID type handling.

#### Methods

##### `init(self)`
Initializes test data with default values.
- Sets `self.userid1` to 0 (integer)
- Sets `self.userid2` to '0' (string)

##### `setUp(self)`
Sets up test data before each test method execution.
- Sets `self.userid1` to 1003 (integer)
- Sets `self.userid2` to '1003' (string)

##### `testUserid1(self)`
Tests user authentication with integer user ID.
- Retrieves user table from current.auth
- Queries user by integer ID (1003)
- Asserts user exists and has correct ID
- Tests login functionality with integer ID
- Validates authenticated user ID matches expected value

##### `testUserid2(self)`
Tests user authentication with string user ID.
- Retrieves user table from current.auth
- Queries user by string ID ('1003')
- Asserts user exists and has correct ID (converted to integer)
- Tests login functionality with string ID
- Validates authenticated user ID matches expected value

## Dependencies
- `unittest` - Python's built-in testing framework
- `gluon.globals.current` - web2py's global context object providing access to:
  - `current.db` - Database connection
  - `current.auth` - Authentication system

## Usage Example
```python
# Run the test suite
import unittest
from testUseridType import TestUseridType

# Create test suite
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestUseridType))

# Run tests with verbose output
unittest.TextTestRunner(verbosity=2).run(suite)
```

## Integration with web2py Framework

### Authentication System Integration
- Uses `current.auth.table_user()` to access the user table
- Leverages `current.auth.login` for user authentication
- Tests `current.auth.user` for authenticated user access

### Database Integration
- Relies on web2py's DAL (Database Abstraction Layer)
- Uses table record access patterns: `table(id=value)`
- Demonstrates type conversion handling in database queries

### Global Context Usage
- Utilizes web2py's `current` object for accessing application context
- Ensures tests run within proper web2py environment

## Test Scenarios Covered
1. **Integer ID Authentication**: Validates login with numeric user ID
2. **String ID Authentication**: Validates login with string representation of user ID
3. **Type Conversion**: Ensures both integer and string IDs resolve to same user
4. **Authentication State**: Verifies proper authentication state after login

## Expected Behavior
- Both integer (1003) and string ('1003') user IDs should authenticate the same user
- Database queries should handle type conversion transparently
- Authentication system should maintain consistent user state regardless of ID type
- All assertions should pass, confirming type compatibility

## File Structure
```
applications/portal/tests/
└── testUseridType.py
```

This test file is part of the portal application's test suite, ensuring robust user authentication functionality across different data type scenarios.