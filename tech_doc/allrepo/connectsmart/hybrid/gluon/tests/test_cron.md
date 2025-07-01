# test_cron.py

## Overview
Unit test module for testing Web2py's cron job functionality, including token management, cron task execution, and process pool handling.

## Imports
```python
import os
import shutil
import sys
import time
import unittest
from gluon.fileutils import create_app, write_file
from gluon.newcron import (SimplePool, Token, crondance, reset, stopcron,
                           subprocess_count)
```

## Test Configuration

### Constants
- `test_app_name`: "_test_cron" - Name of the test application
- `appdir`: Path to the test application directory
- `TARGET`: Path to the cron request output file

### Test Data

#### TEST_CRONTAB
Cron schedule configuration that runs a test script at system reboot:
```
@reboot peppe **applications/_test_cron/cron/test.py
```

#### TEST_SCRIPT1
Python script that writes request information to a file:
```python
from os.path import join as pjoin

with open(pjoin(request.folder, 'private', 'cron_req'), 'w') as f:
    f.write(str(request))
```

#### TEST_SCRIPT2
Python script that sleeps for 13 seconds (used for testing long-running processes):
```python
import time
time.sleep(13)
```

## Module Setup/Teardown

### setUpModule()
Creates the test application directory and initializes a new Web2py application.

### tearDownModule()
Removes the test application directory and all its contents.

## Test Class: TestCron

### Class Methods

#### tearDownClass()
Cleans up cron master files after all tests complete.

### Test Methods

#### test_1_Token()
Tests the Token class functionality for cron job synchronization.

**Test Flow:**
1. Creates a Token instance for the test application path
2. Tests token acquisition (should return current time)
3. Tests release on already released token (should return False)
4. Tests acquisition when token is held (should return None)
5. Tests successful release (should return True)

**Purpose:** Ensures proper token-based synchronization for cron jobs to prevent concurrent execution.

#### test_2_crondance()
Tests the main cron execution functionality.

**Test Flow:**
1. Sets up cron directory structure
2. Writes crontab configuration file
3. Writes test Python script
4. Ensures target file doesn't exist
5. Executes crondance with startup=True
6. Waits for cron task completion
7. Verifies target file was created

**Key Parameters:**
- `os.getcwd()`: Current working directory
- `"hard"`: Cron mode
- `startup=True`: Indicates system startup
- `apps=[test_app_name]`: Specific app to process

**Purpose:** Validates that cron jobs execute correctly at startup and produce expected outputs.

#### test_3_SimplePool()
Tests the SimplePool class for managing concurrent cron processes.

**Test Flow:**
1. Writes a long-running test script (13 seconds)
2. Creates a SimplePool with 1 worker
3. Constructs Web2py command for cron job execution
4. Launches the cron job (should return True)
5. Tests launching with None (should return False)
6. Stops cron execution
7. Resets cron state

**Command Construction:**
```python
[sys.executable, w2p_path, "--cron_job", "--no_banner", 
 "--no_gui", "--plain", "-S", test_app_name, "-R", script_path]
```

**Purpose:** Tests process pool management for cron job execution and cleanup.

## Key Components Tested

### Token
- Provides mutual exclusion for cron job execution
- Prevents multiple instances of the same cron job

### crondance
- Main cron execution function
- Processes crontab files and executes scheduled tasks

### SimplePool
- Manages a pool of worker processes
- Limits concurrent cron job execution

### Process Management
- `subprocess_count()`: Monitors active subprocesses
- `stopcron()`: Stops all cron processes
- `reset()`: Resets cron state

## Notes
- Tests use time delays to ensure asynchronous operations complete
- The test creates a temporary application for isolation
- Cron functionality is tested in "hard" mode with actual process spawning
- Token-based synchronization prevents race conditions in cron execution