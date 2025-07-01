# Gluon NewCron Module Technical Documentation

## Module: `newcron.py`

### Overview
The `newcron` module provides a comprehensive cron-style task scheduling system for the Gluon web framework. It supports both hard cron (separate daemon thread) and soft cron (request-based) scheduling modes, with thread pool management, file locking for concurrency control, and support for multiple web2py applications.

### Table of Contents
1. [Core Components](#core-components)
2. [Cron Types](#cron-types)
3. [Thread Management](#thread-management)
4. [Task Parsing](#task-parsing)
5. [Execution Modes](#execution-modes)
6. [Usage Examples](#usage-examples)
7. [Advanced Features](#advanced-features)

### Core Components

#### Dependencies
```python
import datetime
import os
import re
import sched
import shlex
import sys
import threading
import time
from functools import reduce
from logging import getLogger
from pydal.contrib import portalocker
from gluon import fileutils
from gluon._compat import pickle, to_bytes
```

#### Global Variables
```python
logger_name = "web2py.cron"
_stopping = False          # Global stop flag
_subprocs_lock = threading.RLock()  # Subprocess management lock
_subprocs = []            # Active subprocess list
```

### Cron Types

#### Hard Cron (`hardcron` class)
Runs in a separate daemon thread with precise timing:

```python
class hardcron(threading.Thread):
    def __init__(self, applications_parent, apps=None):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.path = applications_parent
        self.apps = apps
        # Process '@reboot' entries at startup
        crondance(self.path, "hard", startup=True, apps=self.apps)
```

**Features:**
- Runs every minute on the minute
- Separate daemon thread
- Handles `@reboot` tasks at startup
- Precise scheduling with `sched.scheduler`

#### Soft Cron
Request-triggered cron execution:

```python
def softcron(applications_parent, apps=None):
    logger = getLogger(logger_name)
    try:
        if not _dancer((applications_parent, apps)):
            logger.warning("no thread available for soft crondance")
    except Exception:
        logger.exception("error executing soft crondance")
```

**Features:**
- Triggered by web requests
- Non-blocking execution
- Thread pool managed
- Graceful error handling

#### External Cron
Manually triggered cron execution:

```python
def extcron(applications_parent, apps=None):
    getLogger(logger_name).debug("external cron invocation")
    crondance(applications_parent, "external", startup=False, apps=apps)
```

### Thread Management

#### `SimplePool` Class
Thread pool for managing cron task execution:

```python
class SimplePool(object):
    def __init__(self, size, worker_cls=Worker):
        self.size = size
        self.worker_cls = worker_cls
        self.lock = threading.RLock()
        self.idle = list()
        self.running = set()
```

**Methods:**
- `grow(size)`: Increase pool size
- `start(t)`: Move thread from idle to running
- `stop(t)`: Move thread from running to idle
- `__call__(payload)`: Execute task with available thread

#### `Worker` Class
Thread worker for executing cron commands:

```python
class Worker(threading.Thread):
    def run(self):
        logger = getLogger(logger_name)
        while True:
            with self.run_lock:
                cmd = " ".join(self.payload)
                proc = subprocess.Popen(
                    self.payload,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                # Handle process execution and logging
```

#### `SoftWorker` Class
Specialized worker for soft cron tasks:

```python
class SoftWorker(threading.Thread):
    def run(self):
        while True:
            with self.run_lock:
                applications_parent, apps = self.payload
                crondance(applications_parent, "soft", startup=False, apps=apps)
```

### Task Parsing

#### Crontab Format Support
Standard cron format with extensions:

```python
# Standard format: minute hour day month weekday user command
# 0 2 * * * root /path/to/script

# Special formats supported:
@reboot     # Run at startup
@yearly     # 0 0 1 1 *
@annually   # 0 0 1 1 *
@monthly    # 0 0 1 * *
@weekly     # 0 0 * * 0
@daily      # 0 0 * * *
@midnight   # 0 0 * * *
@hourly     # 0 * * * *
```

#### `parsecronline(line)` Function
Parses cron line into task dictionary:

```python
def parsecronline(line):
    """
    Parses cron line into task dictionary
    Returns: {
        'min': [0, 15, 30, 45],    # Minutes list
        'hr': [2],                  # Hours list
        'dom': [1, 15],            # Day of month list
        'mon': [1, 6, 12],         # Months list
        'dow': [0, 6],             # Day of week list
        'user': 'root',            # User
        'cmd': '/path/to/script'   # Command
    }
    """
```

#### Range Parsing
Supports complex time specifications:

```python
def rangetolist(s, period="min"):
    """
    Convert range specification to list
    Examples:
        "*/5" -> [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
        "1-5" -> [1, 2, 3, 4, 5]
        "1-10/2" -> [2, 4, 6, 8, 10]
    """
```

### Execution Modes

#### Web2py Command Execution
Special handling for web2py scripts:

```python
# Command prefixes:
# *  -> Execute with models loaded (-M flag)
# ** -> Execute without models (script only)

# Examples in crontab:
# Run with models: 0 2 * * * root *applications/myapp/scripts/backup.py
# Run without models: 0 3 * * * root **applications/myapp/scripts/cleanup.py
```

#### Command Types

1. **Web2py Scripts with Models (`*command`)**:
   ```bash
   python web2py.py -S myapp -R script.py -M
   ```

2. **Web2py Scripts without Models (`**command`)**:
   ```bash
   python web2py.py -S myapp -R script.py
   ```

3. **External Commands**:
   ```bash
   /bin/bash -c "command with args"
   ```

### Locking and Concurrency

#### `Token` Class
File-based locking system:

```python
class Token(object):
    def __init__(self, path):
        self.path = os.path.join(path, "cron.master")
        # Lock implementation using pickle and file locking
    
    def acquire(self, startup=False):
        """Acquire lock with timestamp"""
        
    def release(self):
        """Release lock with completion timestamp"""
```

**Lock File Format:**
```python
# cron.master content: (start_time, stop_time)
(1640995200.0, 1640995260.0)  # start, stop timestamps
(1640995260.0, 0)             # running (stop=0)
```

### Usage Examples

#### Basic Crontab Setup
```python
# Create applications/myapp/cron/crontab file:

# Run backup every day at 2 AM with models
0 2 * * * root *applications/myapp/scripts/backup.py

# Run cleanup every hour without models
0 * * * * root **applications/myapp/scripts/cleanup.py

# Run external script every 15 minutes
*/15 * * * * root /usr/local/bin/monitor.sh

# Run at startup
@reboot root *applications/myapp/scripts/initialize.py

# Run weekly report on Sundays at midnight
@weekly root *applications/myapp/scripts/weekly_report.py
```

#### Hard Cron Setup
```python
# In main.py or startup script
from gluon.newcron import hardcron

def start_cron():
    applications_parent = '/path/to/web2py'
    apps = ['myapp1', 'myapp2']  # or None for all apps
    
    # Start hard cron daemon
    cron_thread = hardcron(applications_parent, apps)
    cron_thread.start()
    
    return cron_thread

# Start cron
cron = start_cron()
```

#### Soft Cron Integration
```python
# In models/scheduler.py
from gluon.newcron import softcron

def trigger_softcron():
    """Trigger soft cron on web requests"""
    if not session.cron_last_run or \
       time.time() - session.cron_last_run > 60:  # Once per minute
        
        softcron(request.folder.split('/')[-2])  # applications parent
        session.cron_last_run = time.time()

# Call in model or controller
trigger_softcron()
```

#### Custom Cron Scripts
```python
# applications/myapp/scripts/backup.py
#!/usr/bin/env python
"""
Backup script for web2py application
Run with: 0 2 * * * root *applications/myapp/scripts/backup.py
"""

import os
import datetime
from gluon import *

def main():
    # Database backup
    backup_filename = f"backup_{datetime.date.today()}.sql"
    backup_path = os.path.join(request.folder, 'private', backup_filename)
    
    # Export database
    with open(backup_path, 'w') as f:
        db.export_to_csv_file(f)
    
    # Log completion
    logger = logging.getLogger('web2py.cron.backup')
    logger.info(f"Backup completed: {backup_filename}")
    
    # Email notification
    if mail:
        mail.send(
            to=['admin@example.com'],
            subject=f"Backup completed: {backup_filename}",
            message=f"Database backup saved to {backup_path}"
        )

if __name__ == '__main__':
    main()
```

### Advanced Features

#### Multi-Application Management
```python
def setup_multi_app_cron():
    """Setup cron for multiple applications"""
    
    applications_parent = '/path/to/web2py'
    
    # Different apps with different schedules
    app_configs = {
        'app1': {'cron_type': 'hard', 'enabled': True},
        'app2': {'cron_type': 'soft', 'enabled': True},
        'app3': {'cron_type': 'external', 'enabled': False},
    }
    
    for app_name, config in app_configs.items():
        if not config['enabled']:
            continue
            
        if config['cron_type'] == 'hard':
            cron_thread = hardcron(applications_parent, [app_name])
            cron_thread.start()
        
        elif config['cron_type'] == 'soft':
            # Set up soft cron trigger in app's models
            pass
```

#### Dynamic Crontab Management
```python
class CrontabManager:
    """Dynamic crontab management for web2py applications"""
    
    def __init__(self, app_path):
        self.app_path = app_path
        self.crontab_path = os.path.join(app_path, 'cron', 'crontab')
    
    def add_task(self, schedule, command, user='root'):
        """Add new cron task"""
        task_line = f"{schedule} {user} {command}\n"
        
        with open(self.crontab_path, 'a') as f:
            f.write(task_line)
    
    def remove_task(self, command):
        """Remove cron task by command"""
        if not os.path.exists(self.crontab_path):
            return
        
        with open(self.crontab_path, 'r') as f:
            lines = f.readlines()
        
        # Filter out matching lines
        filtered_lines = [line for line in lines if command not in line]
        
        with open(self.crontab_path, 'w') as f:
            f.writelines(filtered_lines)
    
    def list_tasks(self):
        """List all cron tasks"""
        if not os.path.exists(self.crontab_path):
            return []
        
        tasks = []
        with open(self.crontab_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    task = parsecronline(line)
                    if task:
                        task['line_number'] = line_num
                        task['raw_line'] = line
                        tasks.append(task)
        
        return tasks

# Usage
manager = CrontabManager('/path/to/applications/myapp')
manager.add_task('0 3 * * *', '*applications/myapp/scripts/cleanup.py')
tasks = manager.list_tasks()
```

#### Monitoring and Logging
```python
def setup_cron_monitoring():
    """Setup comprehensive cron monitoring"""
    
    # Configure logger
    logger = logging.getLogger('web2py.cron')
    logger.setLevel(logging.INFO)
    
    # File handler for cron logs
    log_file = os.path.join(request.folder, 'logs', 'cron.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    return logger

def log_cron_execution(task, start_time, end_time, success, output=None):
    """Log cron task execution details"""
    logger = logging.getLogger('web2py.cron.execution')
    
    duration = end_time - start_time
    status = "SUCCESS" if success else "FAILED"
    
    logger.info(f"Task: {task['cmd']} | Status: {status} | Duration: {duration:.2f}s")
    
    if output:
        logger.debug(f"Output: {output}")
```

#### Error Recovery
```python
def setup_error_recovery():
    """Setup error recovery for failed cron tasks"""
    
    def retry_failed_task(task, max_retries=3, delay=60):
        """Retry failed task with exponential backoff"""
        for attempt in range(max_retries):
            try:
                # Execute task
                result = execute_cron_task(task)
                if result['success']:
                    return result
                
                # Wait before retry
                time.sleep(delay * (2 ** attempt))
                
            except Exception as e:
                logger = logging.getLogger('web2py.cron.retry')
                logger.warning(f"Retry {attempt + 1} failed: {e}")
                
                if attempt == max_retries - 1:
                    # Final failure - send alert
                    send_failure_alert(task, e)
        
        return {'success': False, 'error': 'Max retries exceeded'}
    
    def send_failure_alert(task, error):
        """Send alert for task failure"""
        if mail:
            mail.send(
                to=['admin@example.com'],
                subject=f"Cron task failed: {task['cmd']}",
                message=f"Task: {task['cmd']}\nError: {error}\nTime: {datetime.datetime.now()}"
            )
```

### Best Practices

1. **Lock Management**: Always use proper locking to prevent concurrent execution
2. **Error Handling**: Implement comprehensive error handling and logging
3. **Resource Management**: Clean up subprocesses and file handles
4. **Monitoring**: Log all cron activities for debugging
5. **Testing**: Test cron scripts independently before scheduling
6. **Security**: Validate user permissions and command execution
7. **Performance**: Use appropriate thread pool sizes
8. **Graceful Shutdown**: Implement proper cleanup on application shutdown

### Security Considerations

1. **Command Injection**: Validate all command inputs
2. **File Permissions**: Secure crontab and lock files
3. **User Context**: Run tasks with appropriate user permissions
4. **Path Validation**: Validate script and executable paths
5. **Resource Limits**: Implement timeouts and resource constraints

### Troubleshooting

#### Common Issues
1. **Lock File Corruption**: Clear `cron.master` if stale
2. **Permission Errors**: Check file and directory permissions
3. **Missing Modules**: Ensure all imports are available
4. **Thread Deadlocks**: Monitor thread pool utilization
5. **Process Zombies**: Properly handle subprocess cleanup

#### Debug Mode
```python
# Enable debug logging
import logging
logging.getLogger('web2py.cron').setLevel(logging.DEBUG)

# Check cron status
def check_cron_status():
    status = {
        'stopping': _stopping,
        'subprocess_count': subprocess_count(),
        'active_threads': len(_subprocs),
        'dancer_size': _dancer.size,
        'launcher_size': _launcher.size
    }
    return status
```

### Module Metadata

- **License**: LGPLv3 (web2py framework)
- **Authors**: Attila Csipa, Massimo Di Pierro, Paolo Pastori
- **Thread Safety**: Yes (with proper locking)
- **Platform**: Cross-platform
- **Dependencies**: Standard library, PyDAL, Gluon
- **Python**: 2.7+, 3.x compatible