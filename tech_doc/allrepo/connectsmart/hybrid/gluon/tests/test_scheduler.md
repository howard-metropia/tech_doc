# test_scheduler.py

## Overview
Comprehensive unit tests for Web2py's task scheduler system, including cron expression parsing, job dependency graphs, and scheduler execution functionality.

## Imports
```python
import datetime
import glob
import os
import shutil
import sys
import unittest
from gluon.dal import DAL
from gluon.fileutils import create_app
from gluon.languages import TranslatorFactory
from gluon.scheduler import CronParser, JobGraph, Scheduler
from gluon.storage import Storage
```

## Test Structure

### BaseTestScheduler
Base class providing common setup/teardown for scheduler tests.

#### setUp()
- Creates test application directory
- Initializes DAL with SQLite database
- Sets up current request context
- Creates translator instance

#### tearDown()
- Cleans up test application directory
- Handles errors gracefully

## Test Classes

### CronParserTest
Tests the cron expression parser for various scheduling patterns.

#### testMinute()
Tests minute-based cron expressions:
- `*/1 * * * *` - Every minute
- `*/5 * * * *` - Every 5 minutes
- `4/34 * * * *` - Starting at minute 4, every 34 minutes

**Verifies:**
- Correct minute increments
- Hour rollover at 60 minutes
- Offset starting times

#### testHour()
Tests hourly cron expressions:
- `0 */3 * * *` - Every 3 hours at minute 0
- Day rollover when hours exceed 24

#### testDay()
Tests daily scheduling:
- `0 0 */3 * *` - Every 3 days
- Leap year handling (Feb 29)
- Month boundary transitions

#### testWeekDay()
Tests weekday-based scheduling:
- `0 0 * * sat` - Every Saturday
- `0 0 1 * wed` - First day of month OR Wednesdays
- ISO weekday numbers (1-7)

#### testMonth()
Tests monthly scheduling:
- `0 0 1 * *` - First day of each month
- `0 0 1 */4 *` - Every 4 months
- `0 0 1 1-3 *` - January through March

#### testSundayToThursdayWithAlphaConversion()
Tests day name ranges:
- `30 22 * * sun-thu` - Sunday through Thursday
- Alpha day name conversion

#### testISOWeekday()
Tests ISO weekday numbers:
- `0 0 * * 7` - Sundays (ISO 7)
- `0 0 * * */2` - Every other day

#### testBug2(), testBug3()
Regression tests for specific bug fixes:
- Month-specific scheduling
- Multiple day values

#### test_rangeGenerator()
Tests range with step syntax:
- `1-9/2 0 1 * *` - Minutes 1,3,5,7,9

#### test_iterGenerator()
Tests iterator protocol implementation.

#### test_invalidcron()
Tests error handling for invalid expressions:
- `5 4 31 2 *` - Feb 31 (invalid)
- `1- * * * *` - Incomplete range
- `-1 * * * *` - Negative values
- Too many/few fields

#### testLastDayOfMonth()
Tests 'L' syntax for last day of month:
- `0 0 L * *` - Last day of each month
- Handles different month lengths

#### testSpecialExpr()
Tests special expressions:
- `@yearly` / `@annually` - Once per year
- `@monthly` - First day of month
- `@weekly` - Every Sunday
- `@daily` / `@midnight` - Every day at midnight
- `@hourly` - Top of every hour

### TestsForJobGraph
Tests task dependency management using directed acyclic graphs.

#### testJobGraph()
Tests valid dependency graph creation:
- Creates "getting dressed" dependency graph
- Tasks: watch, jacket, shirt, tie, pants, undershorts, belt, shoes, socks
- Dependencies represent order constraints
- Validates topological sort

**Example Dependencies:**
- Tie requires shirt
- Belt requires shirt and pants
- Jacket requires tie and belt
- Shoes require pants and socks

#### testJobGraphFailing()
Tests cyclic dependency detection:
- Adds circular dependency
- Validates that cycle is detected
- No dependencies inserted on failure

#### testJobGraphDifferentJobs()
Tests multiple job graphs:
- Two separate job dependency sets
- Individual validation
- Combined validation detects cycles

### TestsForSchedulerAPIs
Tests scheduler API methods.

#### testQueue_Task()
Tests task queuing functionality:
- Return value structure (id, uuid, errors)
- Parameter validation
- UUID uniqueness enforcement
- Invalid parameter handling

#### testTask_Status()
Tests task status retrieval:
- Query by ID
- Query by UUID
- Query by DAL query
- Output parameter for detailed results

### testForSchedulerRunnerBase
Base class for scheduler execution tests.

#### Helper Methods:
- `writefunction()` - Creates test task functions
- `writeview()` - Creates test view files
- `exec_sched()` - Executes scheduler process
- `fetch_results()` - Retrieves task results
- `exec_asserts()` - Batch assertion execution

### TestsForSchedulerRunner
Tests scheduler execution behavior.

#### testRepeats_and_Expired_and_Prio()
Tests:
- **Repeats**: Task repetition with period
- **Expired**: Tasks with past stop_time
- **Priority**: Next run time ordering

#### testNoReturn_and_Timeout_and_Progress()
Tests:
- **No Return**: Functions without return statements
- **Timeout**: Task timeout handling
- **Progress**: Output synchronization with `!clear!` syntax

#### testDrift_and_env_and_immediate()
Tests:
- **Drift Prevention**: Exact period maintenance
- **Environment**: W2P_TASK variable access
- **Immediate**: Immediate execution flag

#### testRetryFailed()
Tests failure retry mechanisms:
- Simple retry on failure
- Consecutive failure counting
- State file handling

#### testRegressions()
Tests for specific regression issues:
- Large result handling
- View rendering in tasks

## Key Components

### CronParser
- Parses cron expressions
- Generates next execution times
- Supports standard and special syntax

### JobGraph
- Manages task dependencies
- Performs topological sorting
- Detects circular dependencies

### Scheduler
- Queues tasks with various options
- Manages task execution
- Handles retries and failures

## Task Options

### Timing Options
- `period`: Seconds between runs
- `repeats`: Maximum execution count
- `start_time`: First execution time
- `stop_time`: Expiration time
- `prevent_drift`: Maintain exact periods

### Execution Options
- `timeout`: Maximum execution time
- `retry_failed`: Retry count on failure
- `immediate`: Skip scheduling delay
- `sync_output`: Output update frequency

### Tracking Options
- `uuid`: Unique identifier
- `task_name`: Human-readable name
- `group_name`: Task grouping

## Testing Patterns

### Subprocess Testing
- Spawns actual scheduler process
- Tests real execution behavior
- Verifies database state

### Time-based Testing
- Uses datetime calculations
- Verifies scheduling accuracy
- Tests period enforcement

### State Verification
- Database record checks
- Status field validation
- Output content verification

## Notes
- Extensive cron syntax support
- Dependency graph for complex workflows
- Robust error handling and retries
- Real subprocess testing for accuracy
- Regression test coverage