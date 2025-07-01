# Scheduler Module

## Overview
The Gluon Scheduler is a powerful background task processing system for web2py applications. It provides a database-backed job queue with support for recurring tasks, cron-like scheduling, task dependencies, and distributed worker processes. The scheduler enables long-running tasks to execute outside of web requests, improving application responsiveness and reliability.

## Architecture

### Core Components

#### Scheduler Class
Main coordinator managing tasks and workers.

**Key Attributes:**
- `db`: DAL database connection
- `tasks`: Dictionary of callable functions
- `group_names`: Worker group assignments
- `heartbeat`: Worker check-in interval (default: 3 seconds)
- `worker_name`: Unique worker identifier

**Threading Model:**
- Main thread: Task assignment and monitoring
- Heartbeat thread: Worker status updates
- Process pool: Task execution isolation

#### Task System
Tasks represent units of work to be executed.

**Task States:**
- `QUEUED`: Waiting for execution
- `ASSIGNED`: Allocated to worker
- `RUNNING`: Currently executing
- `COMPLETED`: Successfully finished
- `FAILED`: Execution error
- `TIMEOUT`: Exceeded time limit
- `STOPPED`: Manually terminated
- `EXPIRED`: Passed stop_time

#### Worker Management
Workers are processes that execute tasks.

**Worker States:**
- `ACTIVE`: Available for tasks
- `PICK`: Force task assignment
- `DISABLED`: Temporarily suspended
- `TERMINATE`: Graceful shutdown
- `KILL`: Immediate termination
- `STOP_TASK`: Cancel current task

### Database Schema

#### scheduler_task
Stores task definitions and status.

**Fields:**
- `application_name`: Source application
- `task_name`: Human-readable name
- `function_name`: Callable to execute
- `args`: JSON-encoded arguments
- `vars`: JSON-encoded keyword arguments
- `enabled`: Task active flag
- `start_time`: Earliest execution time
- `stop_time`: Latest execution time
- `repeats`: Execution count (0=unlimited)
- `period`: Seconds between runs
- `timeout`: Maximum execution seconds
- `times_run`: Successful execution count
- `times_failed`: Failed execution count

#### scheduler_run
Execution history and results.

**Fields:**
- `task_id`: Reference to task
- `status`: Execution result
- `start_time`: Execution start
- `stop_time`: Execution end
- `run_output`: Captured stdout
- `run_result`: Function return value
- `traceback`: Error details
- `worker_name`: Executing worker

#### scheduler_worker
Active worker registry.

**Fields:**
- `worker_name`: Unique identifier
- `first_heartbeat`: Registration time
- `last_heartbeat`: Latest check-in
- `status`: Current state
- `is_ticker`: Task distributor flag
- `group_names`: Assigned groups
- `worker_stats`: Performance metrics

## Task Scheduling

### Basic Scheduling
```python
# Define task function
def send_email(to, subject, body):
    # Email sending logic
    return "Email sent to %s" % to

# Initialize scheduler
scheduler = Scheduler(db, dict(
    send_email=send_email
))

# Queue a task
scheduler.queue_task(
    send_email,
    pargs=['user@example.com', 'Hello', 'Message body'],
    start_time=request.now
)
```

### Recurring Tasks
```python
# Run every hour
scheduler.queue_task(
    cleanup_old_sessions,
    period=3600,  # seconds
    repeats=0     # 0 = unlimited
)

# Run 10 times with retry
scheduler.queue_task(
    sync_data,
    period=300,
    repeats=10,
    retry_failed=3
)
```

### Cron Expressions
```python
# Run at 2:30 AM daily
scheduler.queue_task(
    daily_backup,
    cronline='30 2 * * *'
)

# Every Monday at noon
scheduler.queue_task(
    weekly_report,
    cronline='0 12 * * 1'
)
```

### Task Dependencies
```python
# Create job graph
job = JobGraph(db, 'data_pipeline')

# Define dependencies
parent_id = scheduler.queue_task(extract_data).id
child_id = scheduler.queue_task(transform_data).id
job.add_deps(parent_id, child_id)

# Validate execution order
job.validate()
```

## Worker Processes

### Starting Workers
```bash
# Single worker
python web2py.py -K myapp

# Multiple workers
python web2py.py -K myapp,myapp,myapp

# Specific groups
python web2py.py -K myapp:group1,myapp:group2
```

### Programmatic Control
```python
# Start worker in code
scheduler = Scheduler(db, tasks)
scheduler.loop()

# Control workers
scheduler.disable()    # Pause processing
scheduler.resume()     # Resume processing
scheduler.terminate()  # Graceful shutdown
scheduler.kill()       # Force termination
```

### Worker Configuration
```python
scheduler = Scheduler(
    db,
    tasks,
    worker_name='worker1',
    group_names=['default', 'reports'],
    heartbeat=3,
    max_empty_runs=10,
    discard_results=False,
    utc_time=False
)
```

## Advanced Features

### Task Execution Context
```python
def my_task():
    # Access task metadata
    from gluon import current
    task_id = current.W2P_TASK.id
    run_id = current.W2P_TASK.run_id
    
    # Update progress
    print("Processing step 1...")
    print(CLEAROUT + "Progress: 25%")
    
    return "Task completed"
```

### Dynamic Task Assignment
```python
# Ticker process distributes tasks
# One worker elected as ticker
# Considers worker load and groups
# Handles broadcast tasks
```

### Result Management
```python
# Check task status
status = scheduler.task_status(task_id, output=True)
if status.scheduler_run.status == 'COMPLETED':
    result = loads(status.scheduler_run.run_result)

# Stop running task
scheduler.stop_task(task_id)
```

### Monitoring
```python
# Get all workers
workers = scheduler.get_workers()

# Check worker stats
for name, info in workers.items():
    print("%s: %s tasks, %s errors" % (
        name, 
        info.worker_stats['total'],
        info.worker_stats['errors']
    ))
```

## CronParser Utility

### Syntax Support
- Standard cron: `minute hour day month dayofweek`
- Shortcuts: `@yearly`, `@monthly`, `@daily`, `@hourly`
- Ranges: `1-5`, `*/5`, `1-10/2`
- Lists: `1,3,5,7`
- Names: `mon`, `jan`

### Usage
```python
# Parse and validate
cron = CronParser('0 */4 * * *')
next_run = cron.next()

# Iterate schedules
for run_time in cron:
    print(run_time)
    if run_time > end_date:
        break
```

## Performance Optimization

### Database Considerations
- Index scheduler tables properly
- Regular cleanup of old runs
- Partition large history tables
- Use connection pooling

### Task Design
- Avoid long-running monolithic tasks
- Implement progress reporting
- Handle interruption gracefully
- Minimize database queries

### Worker Tuning
```python
# Adjust empty run tolerance
scheduler = Scheduler(
    db, 
    tasks,
    max_empty_runs=50  # Higher for infrequent tasks
)

# Control task batching
# Ticker assigns up to 50 tasks per cycle
# Adjust based on task frequency
```

## Error Handling

### Task Failures
```python
def robust_task():
    try:
        # Task logic
        return "Success"
    except Exception as e:
        # Log but don't raise
        logger.error(str(e))
        return "Failed: %s" % e
```

### Retry Logic
```python
scheduler.queue_task(
    unreliable_api_call,
    retry_failed=5,      # Retry 5 times
    period=60,           # Wait 1 minute between
    timeout=30           # 30 second timeout
)
```

### Monitoring Failures
```python
# Query failed tasks
failed = db(
    (db.scheduler_task.times_failed > 0) &
    (db.scheduler_task.status == 'FAILED')
).select()
```

## Security Considerations

### Task Isolation
- Each task runs in separate process
- No shared memory between tasks
- Limited environment access
- Configurable timeout protection

### Access Control
```python
# Restrict task functions
allowed_tasks = {
    'safe_task': safe_function,
    # Don't expose dangerous operations
}
scheduler = Scheduler(db, allowed_tasks)
```

## Common Patterns

### Email Queue
```python
def send_queued_email(email_id):
    email = db.email_queue(email_id)
    if email:
        mail.send(
            to=email.recipient,
            subject=email.subject,
            message=email.body
        )
        email.update_record(sent=True)
```

### Report Generation
```python
def generate_report(report_type, user_id):
    # Long running report
    data = compile_report_data(report_type)
    pdf = render_pdf(data)
    
    # Notify user
    notify_user(user_id, pdf_path)
    return pdf_path
```

### Data Synchronization
```python
def sync_external_data():
    # Prevent overlapping runs
    if db(db.scheduler_task.function_name == 'sync_external_data'
          ).count() > 1:
        return "Already running"
    
    # Sync logic
    return "Synced %d records" % count
```

## Troubleshooting

### Common Issues

1. **Tasks not executing**
   - Check worker processes running
   - Verify task enabled and not expired
   - Confirm correct group assignment

2. **Database locks**
   - Enable row-level locking
   - Reduce transaction scope
   - Add connection retry logic

3. **Memory growth**
   - Implement result size limits
   - Use result_in_file for large data
   - Monitor worker memory usage

### Debug Mode
```python
# Increase logging
logging.getLogger('web2py.scheduler').setLevel(logging.DEBUG)

# Run single task
scheduler = Scheduler(db, tasks)
task = scheduler.pop_task()
result = scheduler.execute(task)
```

## Best Practices

### Task Development
1. Keep tasks idempotent
2. Implement proper logging
3. Handle partial failures
4. Clean up resources
5. Test timeout scenarios

### Deployment
1. Monitor worker health
2. Implement alerting
3. Plan capacity properly
4. Regular maintenance
5. Document dependencies

## See Also
- Web2py book scheduler chapter
- DAL documentation for schema
- Python multiprocessing module
- Cron expression reference