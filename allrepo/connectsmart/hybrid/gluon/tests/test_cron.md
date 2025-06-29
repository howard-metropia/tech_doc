# test_cron.py

## Overview
This file contains unit tests for the web2py cron system (newcron), which provides scheduled task execution functionality. It tests the cron job scheduler, token-based locking, process management, and task execution within the web2py framework.

## Purpose
- Tests cron job scheduling and execution
- Validates token-based locking mechanism for concurrent access
- Tests process pooling and management
- Verifies cron script execution within web2py context
- Tests startup and shutdown procedures for cron system

## Key Classes and Methods

### Global Configuration
- `test_app_name` - Test application name ("_test_cron")
- `appdir` - Test application directory path
- `TEST_CRONTAB` - Sample crontab configuration for testing
- `TEST_SCRIPT1` - First test script for cron execution
- `TEST_SCRIPT2` - Second test script for timeout testing
- `TARGET` - Target file for cron execution verification

### Module Setup/Teardown Functions

#### `setUpModule()`
Module-level setup for cron tests:
- **Test App Creation**: Creates test application if it doesn't exist
- **Directory Structure**: Initializes proper application directory structure
- **Environment Setup**: Prepares test environment for cron operations

#### `tearDownModule()`
Module-level cleanup:
- **Directory Cleanup**: Removes test application directory
- **Resource Cleanup**: Cleans up temporary files and processes

### Test Scripts

#### `TEST_CRONTAB`
Sample crontab configuration:
```
@reboot peppe **applications/_test_cron/cron/test.py
```
- **Reboot Trigger**: Executes script on system startup
- **Application Specific**: Targets specific test application
- **Script Path**: Points to test script location

#### `TEST_SCRIPT1`
First test script that creates a verification file:
```python
from os.path import join as pjoin

with open(pjoin(request.folder, 'private', 'cron_req'), 'w') as f:
    f.write(str(request))
```

#### `TEST_SCRIPT2`
Second test script for timeout testing:
```python
import time
time.sleep(13)
```

### TestCron Class
Comprehensive test suite for cron functionality.

#### Class Methods

##### `tearDownClass(cls)`
Class-level cleanup:
- **Master File Cleanup**: Removes cron.master files from both app and root directories
- **Process Cleanup**: Ensures no hanging cron processes

#### Test Methods

##### `test_1_Token(self)`
Tests token-based locking mechanism for cron jobs.

**Token Operations:**
- **Acquisition**: Tests `t.acquire()` returns timestamp on success
- **Blocking**: Tests `t.acquire()` returns None when already acquired
- **Release**: Tests `t.release()` returns False when not acquired
- **Cycle**: Tests complete acquire-release cycle

**Concurrency Control:**
- **Mutual Exclusion**: Ensures only one process can acquire token
- **Proper Cleanup**: Validates token release allows re-acquisition
- **Timestamp Tracking**: Verifies acquisition timestamp recording

##### `test_2_crondance(self)`
Tests main cron execution functionality.

**Test Setup:**
- **Crontab Creation**: Creates test crontab file with reboot trigger
- **Script Creation**: Creates test script that writes to verification file
- **File Cleanup**: Removes existing target file before test

**Execution Testing:**
```python
crondance(os.getcwd(), "hard", startup=True, apps=[test_app_name])
```
- **Hard Mode**: Tests cron execution in hard mode
- **Startup Flag**: Tests startup cron job execution
- **App Filtering**: Tests execution for specific applications

**Verification:**
- **Process Waiting**: Waits for subprocess completion
- **File Creation**: Verifies target file is created by cron script
- **Content Validation**: Ensures cron script executed properly

##### `test_3_SimplePool(self)`
Tests process pool management for cron jobs.

**Pool Setup:**
- **Pool Creation**: Creates SimplePool with capacity of 1
- **Command Preparation**: Prepares web2py command for cron execution
- **Script Configuration**: Uses long-running test script

**Command Structure:**
```python
cmd1 = [
    sys.executable, "web2py.py",
    "--cron_job", "--no_banner", "--no_gui", "--plain",
    "-S", test_app_name,
    "-R", "applications/_test_cron/cron/test.py"
]
```

**Pool Testing:**
- **Job Submission**: Tests `launcher(cmd1)` returns True for valid commands
- **Null Handling**: Tests `launcher(None)` returns False
- **Capacity Management**: Tests pool capacity limitations
- **Cleanup**: Tests proper shutdown with `stopcron()` and `reset()`

## Dependencies
- `unittest` - Python testing framework
- `os` - Operating system interface
- `shutil` - High-level file operations
- `sys` - System-specific parameters
- `time` - Time-related functions
- `gluon.fileutils` - File utility functions
- `gluon.newcron` - New cron system components

## Cron System Components Tested

### Token Class
- **File-based Locking**: Prevents concurrent cron execution
- **Timestamp Management**: Tracks acquisition times
- **Process Safety**: Ensures atomic lock operations

### crondance Function
- **Cron Execution**: Main cron job execution engine
- **Mode Support**: Supports different execution modes
- **Application Filtering**: Executes cron for specific applications
- **Startup Handling**: Special handling for startup cron jobs

### SimplePool Class
- **Process Management**: Manages pool of worker processes
- **Capacity Control**: Limits concurrent process execution
- **Command Execution**: Executes web2py commands in separate processes
- **Resource Cleanup**: Proper cleanup of finished processes

## Usage Example
```python
from gluon.newcron import crondance, SimplePool, Token

# Execute cron jobs
crondance("/path/to/web2py", "soft", startup=False, apps=["myapp"])

# Token-based locking
token = Token(path="/path/to/app")
if token.acquire():
    try:
        # Execute critical section
        pass
    finally:
        token.release()

# Process pool management
pool = SimplePool(max_processes=5)
command = ["python", "script.py"]
if pool(command):
    print("Command submitted successfully")
```

## Integration with web2py Framework

### Application Context
- **Request Context**: Cron scripts run with proper web2py request context
- **Database Access**: Full access to application database and models
- **Configuration**: Access to application configuration and settings
- **Module Loading**: Proper loading of application modules and libraries

### Security and Isolation
- **Application Isolation**: Each application's cron jobs run in isolation
- **User Permissions**: Respects file system permissions and security
- **Resource Limits**: Manages system resources and process limits
- **Token Locking**: Prevents concurrent execution conflicts

### Scheduling Integration
- **Crontab Format**: Uses standard crontab format for scheduling
- **Flexible Triggers**: Supports various trigger types (@reboot, time-based, etc.)
- **Application Scope**: Schedules jobs per application
- **Startup Integration**: Handles application startup cron jobs

## Test Coverage
- **Token Locking**: Concurrent access control and mutual exclusion
- **Job Execution**: Cron job execution and verification
- **Process Management**: Process pool management and cleanup
- **File Operations**: Cron file creation and management
- **Context Integration**: web2py context and request handling
- **Resource Cleanup**: Proper cleanup of processes and files

## Expected Results
- **Token Operations**: Should provide reliable mutual exclusion
- **Job Execution**: Cron scripts should execute within web2py context
- **Process Management**: Pool should manage processes effectively
- **File Creation**: Test scripts should create verification files
- **Cleanup**: All resources should be properly cleaned up

## File Structure
```
gluon/tests/
├── test_cron.py          # This file
└── ... (other test files)

applications/_test_cron/
├── cron/
│   ├── crontab          # Cron schedule configuration
│   └── test.py          # Test cron script
└── private/
    └── cron_req         # Verification file created by cron
```

This test suite ensures the web2py cron system provides reliable scheduled task execution with proper concurrency control, process management, and framework integration.