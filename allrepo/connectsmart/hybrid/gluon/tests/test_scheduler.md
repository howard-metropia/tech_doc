# test_scheduler.py

## Overview
This file contains unit tests for the web2py Scheduler system, which provides background task processing, cron-like scheduling, and job management functionality. It tests the scheduler's cron parser, job management, and task execution capabilities.

## Purpose
- Tests web2py Scheduler background task processing
- Validates CronParser for cron-style scheduling
- Tests JobGraph for task dependencies
- Verifies scheduler database operations
- Tests job queuing and execution workflow
- Validates cron expression parsing and scheduling

## Key Classes and Methods

### BaseTestScheduler Class
Base test class providing common scheduler testing infrastructure.

#### Setup Methods

##### `setUp(self)`
Initializes test environment for scheduler testing.

**Test Application Setup:**
- Creates temporary test application
- Sets up application directory structure
- Initializes database for scheduler tables
- Configures global context for testing

**Database Configuration:**
```python
self.db = DAL(
    "sqlite://dummy2.db",
    folder="applications/%s/databases" % test_app_name,
    check_reserved=["all"]
)
```

##### `tearDown(self)`
Cleans up test environment and removes temporary files.

### CronParserTest Class
Tests cron expression parsing and scheduling functionality.

#### Test Methods

##### `testMinute(self)`
Tests minute-based cron scheduling.

**Every Minute Testing:**
```python
base = datetime.datetime(2010, 1, 23, 12, 18)
itr = CronParser("*/1 * * * *", base)
n1 = itr.next()  # Next minute: 12:19
```

**Every 5 Minutes:**
```python
itr = CronParser("*/5 * * * *", base)
n4 = itr.next()  # Next 5-minute interval
```

**Complex Minute Patterns:**
```python
itr = CronParser("4/34 * * * *", base)
# Pattern: every 34 minutes starting at minute 4
```

##### `testHour(self)`
Tests hour-based cron scheduling.

```python
base = datetime.datetime(2010, 1, 24, 12, 2)
itr = CronParser("0 */3 * * *", base)  # Every 3 hours at minute 0
n1 = itr.next()  # Next occurrence: 15:00
```

##### `testDay(self)`
Tests day-based scheduling with leap year handling.

**Every 3 Days:**
```python
itr = CronParser("0 0 */3 * *", base)
# Pattern: every 3 days at midnight
```

**Leap Year Testing:**
```python
# Test 1996 (leap year)
base = datetime.datetime(1996, 2, 27)
itr = CronParser("0 0 * * *", base)
# Should correctly handle February 29th

# Test 2000 (leap year)
base2 = datetime.datetime(2000, 2, 27)
# Should also handle February 29th correctly
```

##### `testWeekDay(self)`
Tests weekday-based scheduling.

```python
base = datetime.datetime(2010, 2, 25)
itr = CronParser("0 0 * * sat", base)  # Every Saturday at midnight
n1 = itr.next()
# Should return next Saturday
```

## Dependencies
- `unittest` - Python testing framework
- `datetime` - Date and time operations
- `glob` - File pattern matching
- `os` - Operating system interface
- `shutil` - High-level file operations
- `sys` - System-specific parameters
- `gluon.dal` - Database Abstraction Layer
- `gluon.fileutils` - File utilities
- `gluon.languages` - Internationalization
- `gluon.scheduler` - Scheduler system components
- `gluon.storage` - Storage utilities

## Scheduler Components Tested

### CronParser
- **Cron Expression Parsing**: Converts cron syntax to datetime schedules
- **Pattern Support**: Supports */interval, range, and specific value patterns
- **Time Calculations**: Accurate next execution time calculations
- **Edge Cases**: Leap years, month boundaries, year rollovers

### JobGraph
- **Task Dependencies**: Manages job dependencies and execution order
- **Dependency Resolution**: Resolves complex dependency chains
- **Cycle Detection**: Prevents circular dependencies
- **Execution Planning**: Optimizes job execution sequences

### Scheduler
- **Background Processing**: Asynchronous task execution
- **Job Queuing**: Task queuing and prioritization
- **Worker Management**: Multiple worker process coordination
- **Database Integration**: Persistent job storage and state management

## Cron Expression Features

### Supported Patterns
- **Asterisk (*)**: Every unit (minute, hour, day, etc.)
- **Interval (*/n)**: Every n units
- **Range (a-b)**: Values from a to b
- **List (a,b,c)**: Specific values
- **Step (a/n)**: Every n units starting at a

### Time Units
- **Minute**: 0-59
- **Hour**: 0-23  
- **Day**: 1-31
- **Month**: 1-12
- **Weekday**: 0-6 (Sunday=0) or named days

### Special Cases
- **Leap Years**: Proper February 29th handling
- **Month Boundaries**: Correct month transitions
- **Year Rollovers**: Proper year boundary handling
- **Weekday Names**: Support for named weekdays (sat, sun, etc.)

## Usage Example
```python
from gluon.scheduler import Scheduler, CronParser
from gluon.dal import DAL
import datetime

# Setup database
db = DAL('sqlite://scheduler.db')

# Define background tasks
def send_emails():
    # Send scheduled emails
    return "Emails sent"

def cleanup_logs():
    # Clean up old log files
    return "Logs cleaned"

# Initialize scheduler
scheduler = Scheduler(db, tasks={'send_emails': send_emails, 'cleanup_logs': cleanup_logs})

# Schedule tasks
scheduler.queue_task('send_emails', cron='0 9 * * *')  # Daily at 9 AM
scheduler.queue_task('cleanup_logs', cron='0 2 * * 0')  # Weekly on Sunday at 2 AM

# Test cron parser
base_time = datetime.datetime.now()
parser = CronParser('*/15 * * * *', base_time)  # Every 15 minutes
next_run = parser.next()
print(f"Next execution: {next_run}")

# Start scheduler (in production)
# scheduler.loop()
```

## Integration with web2py Framework

### Application Integration
- **Model Integration**: Tasks defined in application models
- **Controller Access**: Schedule tasks from controllers
- **Database Sharing**: Uses application database connections
- **Configuration**: Application-specific scheduler configuration

### Task Management
- **Task Definition**: Define tasks as Python functions
- **Parameter Passing**: Pass parameters to scheduled tasks
- **Return Values**: Capture and store task results
- **Error Handling**: Automatic error logging and retry mechanisms

### Monitoring and Management
- **Web Interface**: Admin interface for job monitoring
- **Status Tracking**: Real-time job status and progress
- **Performance Metrics**: Job execution time and resource usage
- **Log Management**: Comprehensive logging and audit trails

## Test Coverage
- **Cron Parsing**: All cron expression formats and edge cases
- **Time Calculations**: Accurate scheduling calculations
- **Leap Year Handling**: Proper calendar date handling
- **Weekday Scheduling**: Named and numeric weekday support
- **Boundary Conditions**: Month, year, and time boundaries
- **Error Conditions**: Invalid cron expressions and edge cases

## Expected Results
- **Accurate Scheduling**: Cron expressions should schedule correctly
- **Time Precision**: Next execution times should be precise
- **Edge Case Handling**: Leap years and boundaries handled properly
- **Performance**: Fast cron parsing and calculation
- **Reliability**: Consistent scheduling across different time zones

## File Structure
```
gluon/tests/
├── test_scheduler.py     # This file
└── ... (other test files)

applications/_test_scheduler/  # Test application
├── databases/               # Scheduler database
├── models/                 # Task definitions
└── ... (application structure)
```

This test suite ensures web2py's Scheduler system provides reliable, accurate background task processing with robust cron-style scheduling capabilities for production web applications.