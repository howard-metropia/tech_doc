# Gluon Contrib TimeCollect Module

## Overview
Time tracking and collection utilities for web2py applications. Provides functionality to track time spent on various activities, measure performance, and collect timing statistics.

## Module Information
- **Module**: `gluon.contrib.timecollect`
- **Purpose**: Time tracking and performance monitoring
- **Use Case**: Performance analysis, time logging, activity tracking

## Key Features
- **Time Tracking**: Track time spent on operations
- **Performance Monitoring**: Measure execution times
- **Statistics Collection**: Gather timing statistics
- **Activity Logging**: Log time-based activities
- **Reporting**: Generate time-based reports

## Basic Usage

### Time Tracking
```python
from gluon.contrib.timecollect import TimeCollector

# Create time collector
timer = TimeCollector()

# Track operation time
with timer.track('database_query'):
    users = db(db.users).select()

with timer.track('template_rendering'):
    response.render('users/list.html', users=users)

# Get timing results
stats = timer.get_statistics()
print(f"Database query took: {stats['database_query']['total_time']:.3f}s")
```

### Performance Monitoring
```python
def monitor_controller_performance():
    """Monitor controller performance"""
    
    timer = TimeCollector()
    
    # Track different phases
    timer.start('total_request')
    
    with timer.track('authentication'):
        # Authentication logic
        authenticate_user()
    
    with timer.track('data_processing'):
        # Data processing
        process_request_data()
    
    with timer.track('response_generation'):
        # Response generation
        generate_response()
    
    timer.stop('total_request')
    
    # Log performance metrics
    log_performance_metrics(timer.get_statistics())

def log_performance_metrics(stats):
    """Log performance metrics to database"""
    
    db.performance_logs.insert(
        request_url=request.url,
        total_time=stats['total_request']['total_time'],
        auth_time=stats.get('authentication', {}).get('total_time', 0),
        processing_time=stats.get('data_processing', {}).get('total_time', 0),
        response_time=stats.get('response_generation', {}).get('total_time', 0),
        timestamp=datetime.datetime.now()
    )
    db.commit()
```

### Activity Tracking
```python
class ActivityTracker:
    def __init__(self, user_id):
        self.user_id = user_id
        self.timer = TimeCollector()
        self.current_activity = None
    
    def start_activity(self, activity_name):
        """Start tracking an activity"""
        if self.current_activity:
            self.stop_activity()
        
        self.current_activity = activity_name
        self.timer.start(activity_name)
        
        # Log activity start
        db.activity_logs.insert(
            user_id=self.user_id,
            activity=activity_name,
            action='start',
            timestamp=datetime.datetime.now()
        )
    
    def stop_activity(self):
        """Stop current activity tracking"""
        if self.current_activity:
            self.timer.stop(self.current_activity)
            
            # Get time spent
            stats = self.timer.get_statistics()
            time_spent = stats[self.current_activity]['total_time']
            
            # Log activity end
            db.activity_logs.insert(
                user_id=self.user_id,
                activity=self.current_activity,
                action='stop',
                duration=time_spent,
                timestamp=datetime.datetime.now()
            )
            
            self.current_activity = None
    
    def get_daily_summary(self, date=None):
        """Get daily activity summary"""
        if date is None:
            date = datetime.date.today()
        
        start_time = datetime.datetime.combine(date, datetime.time.min)
        end_time = datetime.datetime.combine(date, datetime.time.max)
        
        activities = db(
            (db.activity_logs.user_id == self.user_id) &
            (db.activity_logs.timestamp >= start_time) &
            (db.activity_logs.timestamp <= end_time) &
            (db.activity_logs.action == 'stop')
        ).select()
        
        summary = {}
        for activity in activities:
            activity_name = activity.activity
            if activity_name not in summary:
                summary[activity_name] = 0
            summary[activity_name] += activity.duration or 0
        
        return summary

# Usage
tracker = ActivityTracker(auth.user_id)
tracker.start_activity('project_development')
# ... work on project ...
tracker.stop_activity()
```

This module provides comprehensive time tracking capabilities for web2py applications, enabling performance monitoring and activity tracking functionality.