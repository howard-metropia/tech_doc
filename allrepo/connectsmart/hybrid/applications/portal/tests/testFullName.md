# testFullName.py - Profile Full Name Testing Documentation

## File Overview
**Path:** `/applications/portal/tests/testFullName.py`
**Purpose:** Unit tests for user profile full name generation functionality, testing the profiles_helper module's user_profiles function with database integration.

## Functionality Overview
This module contains unit tests for validating the full name generation logic in the profiles_helper module. It tests how user profiles are processed and formatted, specifically focusing on the full_name field generation from first_name and last_name database fields.

## Key Components

### Test Class

#### `TestProfileFullName(unittest.TestCase)`
Main test class that inherits from unittest.TestCase to provide testing infrastructure for profile full name functionality.

**Methods:**

##### `init(self)`
- **Purpose:** Initializes instance variables for storing original user data
- **Variables:**
  - `self._last_name`: Stores original last name for restoration
  - `self._first_name`: Stores original first name for restoration
- **Note:** This method initializes backup variables but doesn't use standard `__init__` naming

##### `setUp(self)`
- **Purpose:** Sets up test fixtures before each test method execution
- **Database Operations:**
  - Retrieves user record with ID 1003 from auth_user table
  - Stores original first_name and last_name values
  - Updates the user record with test data: 'Monica' and 'Tsai'
  - Commits changes to database
- **Test Data:** Creates a known state with first_name='Monica', last_name='Tsai'

##### `tearDown(self)`
- **Purpose:** Cleans up test environment after each test method
- **Database Operations:**
  - Retrieves the same user record (ID 1003)
  - Restores original first_name and last_name values
  - Commits changes to restore database to original state
- **Cleanup:** Ensures test doesn't leave permanent changes in database

##### `testFullName(self)`
- **Purpose:** Tests the full name generation functionality
- **Test Logic:**
  - Imports user_profiles function from profiles_helper
  - Calls user_profiles with database and user ID list [1003]
  - Retrieves the first profile from results
  - Asserts that full_name equals 'Monica T.' (first name + last initial)
- **Expected Result:** 'Monica T.' format for full name display

## Dependencies

### External Libraries
- **`unittest`**: Python's built-in testing framework
- **`gluon.globals`**: web2py globals for accessing current context
- **`current.db`**: Database access through web2py's current object

### Internal Modules
- **`profiles_helper`**: Module containing user_profiles function being tested
- **Database Tables**: auth_user table for user profile data

## Database Integration

### Database Access Pattern
```python
from gluon.globals import current
db = current.db

# Database operations using web2py DAL
user = db(db.auth_user.id == 1003).select(db.auth_user.ALL).first()
user.update_record(first_name='Monica', last_name='Tsai')
db.commit()
```

### Test User Data
- **User ID:** 1003 (hardcoded test user)
- **Test First Name:** 'Monica'
- **Test Last Name:** 'Tsai'
- **Expected Full Name:** 'Monica T.'

## Integration with web2py Framework

### web2py Testing Patterns
- Uses web2py's DAL (Database Abstraction Layer) for database operations
- Accesses database through current.db global object
- Follows web2py's model/controller/view architecture for testing
- Integrates with web2py's auth system (auth_user table)

### Database Transaction Management
- Uses explicit db.commit() calls to ensure changes are persisted
- Implements proper cleanup in tearDown to restore original state
- Maintains database integrity across test runs

## Usage Examples

### Running the Test
```python
# The test is executed with unittest framework
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestProfileFullName))
unittest.TextTestRunner(verbosity=2).run(suite)
```

### Test Execution Flow
1. **init()** - Initialize backup variables
2. **setUp()** - Store original data and set test data
3. **testFullName()** - Execute the actual test
4. **tearDown()** - Restore original database state

## Profiles Helper Integration

### Function Under Test
```python
from profiles_helper import user_profiles

# Function call being tested
profiles = user_profiles(db, [1003])[0]
full_name = profiles['full_name']
```

### Expected Behavior
- **Input:** Database instance and list of user IDs
- **Processing:** Generates profile data including formatted full_name
- **Output:** Profile dictionary with full_name field
- **Format:** "FirstName LastInitial." (e.g., "Monica T.")

## Test Data Management

### Database State Management
- **Before Test:** Original user data preserved
- **During Test:** Known test data applied
- **After Test:** Original data restored
- **Isolation:** Each test run is independent

### Test User Requirements
- Must use existing user ID (1003) in the database
- User record must exist in auth_user table
- Test assumes user has modifiable first_name and last_name fields

## Business Logic Testing

### Full Name Generation Logic
- Tests the specific format: "FirstName LastInitial."
- Validates that profiles_helper correctly processes user data
- Ensures consistent formatting across the application
- Tests integration between database layer and business logic

### Profile Data Structure
The test validates that user_profiles returns a structure containing:
- Profile dictionary with full_name field
- Proper formatting of personal information
- Consistent data presentation for UI components

## Error Handling Considerations

### Potential Issues
- Database connection problems
- Missing user record (ID 1003)
- profiles_helper import failures
- Database permission issues

### Test Robustness
- Assumes database and user record exist
- Relies on specific user ID being available
- No explicit error handling for missing dependencies

## Integration Points

### Portal Application
- Tests core functionality used throughout the portal
- Validates user profile display logic
- Ensures consistent name formatting across UI
- Tests integration with authentication system

### Database Schema
- Depends on auth_user table structure
- Requires first_name and last_name fields
- Uses standard web2py auth table design
- Tests real database operations, not mocked data

## File Execution
- Executed through unittest framework with custom test suite
- Can be integrated into larger test suites
- Provides detailed test output with verbosity=2
- Supports continuous integration testing scenarios