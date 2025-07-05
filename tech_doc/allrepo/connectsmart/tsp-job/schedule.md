# schedule.js

## Overview
Configuration file defining scheduled job execution patterns for the TSP (Transportation Service Provider) job system. Manages cron-based scheduling for various transportation services, analytics, experiments, and maintenance tasks across different project environments (goezy, hcs) and deployment stages (production, develop, sandbox).

## File Location
- **Path**: `/allrepo/connectsmart/tsp-job/src/schedule.js`
- **Module Type**: Configuration Module
- **Export**: Array of job scheduling configurations

## Key Dependencies
- `config` - Application configuration system for project and environment settings

## Core Structure

### Job Configuration Schema
Each job entry contains:
```javascript
{
  name: string,        // Job identifier matching filename
  cron: string,        // Cron expression for scheduling
  args: array          // Optional command-line arguments
}
```

### Base Jobs (All Projects)
Common jobs that run across all project configurations:

```javascript
const baseJobs = [
  { name: 'mod', cron: '20 0 * * *' },                    // Daily MOD calculations
  { name: 'escrow', cron: '*/10 * * * *' },               // Escrow processing every 10 minutes
  { name: 'check-carpool-records', cron: '0 22 * * *' },  // Daily carpool record validation
  { name: 'carpool_block_validation', cron: '*/3 * * * *' }, // Carpool validation every 3 minutes
  { name: 'modify_status_account_delete', cron: '30 0 * * *' }, // Daily account cleanup
  { name: 'fix-trip-distance', cron: '30 6 * * *', args: ['false'] }, // Daily trip distance fixes
  { name: 'delete-backup-account', cron: '30 1 * * *', args: ['false'] }, // Daily backup cleanup
  { name: 'carpool_trip_processing', cron: '*/10 * * * *' }, // Carpool processing every 10 minutes
  { name: 'update-cluster-id', cron: '*/30 * * * *' }     // Cluster updates every 30 minutes
];
```

## Project-Specific Configurations

### Goezy Project Jobs
Additional jobs for goezy project environment:
```javascript
if (config.project === 'goezy') {
  jobs.push({
    name: 'analytic-database',
    cron: '30 5-6 * * *',           // Daily 5:30-6:30 AM
    args: ['null', 'null']
  });
  jobs.push({
    name: 'recalculate-instant-carpool',
    cron: '0 */12 * * *',           // Every 12 hours
    args: ['false']
  });
  jobs.push({
    name: 'pima',
    cron: '30 5-6 * * *',           // Daily 5:30-6:30 AM
    args: ['null', 'null']
  });
}
```

### HCS Project Jobs
Comprehensive job set for HCS (Houston City Services) project:

#### Core HCS Services
```javascript
if (config.project === 'hcs') {
  // Token and notification management
  { name: 'token-notification', cron: '10 0 * * *' },
  
  // Real-time data updates
  { name: 'update-incident-events', cron: '*/5 * * * *' },
  { name: 'index-trip-trajectory', cron: '30 * * * *' },
  
  // Hourly processing
  { name: 'experiment_user_market', cron: '0 * * * *' },
  { name: 'incentive-process', cron: '0 * * * *' },
  { name: 'market-user', cron: '0 * * * *' },
  { name: 'retention-process', cron: '0 * * * *' },
  
  // Frequent monitoring
  { name: 'incentive-notify', cron: '*/30 * * * *' },
  { name: 'microsurvey-push-notification', cron: '*/5 * * * *' }
}
```

#### Transportation Services
```javascript
// MTC integration
{ name: 'mtc-user-signup', cron: '0 */2 * * *' },

// Transit services
{ name: 'transit-alert', cron: '*/5 * * * *' },

// Parking services
{ name: 'update-parkmobile-token', cron: '*/10 * * * *' },
{ name: 'purge-parkmobile-cache', cron: '0 8 * * *' },
{ name: 'parkmobile-event-monitoring', cron: '*/5 * * * *' },

// Ridehail services
{ name: 'ridehail-refund-process', cron: '*/5 * * * *' },
{ name: 'ridehail-zombie-killer', cron: '*/30 * * * *' },
{ name: 'ridehail-clear-cache', cron: '17 * * * *' }
```

#### Analytics and Reporting
```javascript
// Daily analytics
{ name: 'analytic-database', cron: '30 5-6 * * *', args: ['null', 'null'] },
{ name: 'update-bi-mongodb-views', cron: '0 8 * * *' },
{ name: 'aws_report', cron: '13 0 * * *' },

// Account management
{ name: 'check-daily-account-balance', cron: '0 5 * * *' },

// Bi-daily processing
{ name: 'recalculate-instant-carpool', cron: '0 */12 * * *', args: ['false'] }
```

#### Gamification and Engagement
```javascript
// Challenge management
{ name: 'add-explorer-challenge', cron: '42 * * * *' },

// User engagement
{ name: 'check-realtimedb-incentive-red-dot', cron: '*/5 * * * *' },
{ name: 'weather-notify', cron: '1 * * * *' },

// Activity tracking
{ name: 'update-activity-area', cron: '0 0 * * 0', args: ['0'] }, // Weekly on Sunday

// Badge system
{ name: 'update-user-badge-log', cron: '10 17 * * *', args: ['daily'] },
{ name: 'update-user-badge-log-status', cron: '30 17 * * *', args: ['daily'] }
```

## Environment-Specific Configurations

### Production Environment
```javascript
if (project.stage === 'production') {
  jobs.push({
    name: 'add-rpt-mail-list',
    cron: '22 7 * * *'              // Daily 7:22 AM
  });
}
```

### Development/Sandbox Environment
```javascript
if (project.stage === 'develop' || project.stage === 'sandbox') {
  jobs.push({
    name: 'm3_experiment-tile',
    cron: '0 8 * * *'               // Daily 8:00 AM
  });
  jobs.push({
    name: 'm3_compensation',
    cron: '30 * * * *'              // Every 30 minutes
  });
} else {
  // Production-only jobs
  jobs.push({
    name: 'check-broken-trips',
    cron: '0 7 * * *',
    args: ['null', 'null']
  });
  jobs.push({
    name: 'hntb-etl',
    cron: '0 7 * * *',
    args: ['null', 'null']
  });
}
```

### Reporting and Communication
```javascript
// Mail batch processing
{ name: 'add-rpt-mail-batch', cron: '0 21 * * 2' },      // Tuesdays 9 PM (4 PM CDT)
{ name: 'execute-rpt-mail-batch', cron: '12 * * * *' },   // Every hour at :12

// Construction alerts
{ name: 'construction-alert-notification', cron: '0 * * * *' },
{ name: 'construction-alert-rcs', cron: '5 * * * *' },

// User labeling
{ name: 'add-local-user-label', cron: '35 7 * * *' }
```

## Cron Expression Patterns

### Frequency Categories
- **Every Few Minutes**: `*/3`, `*/5`, `*/10` - High-frequency monitoring
- **Half-Hourly**: `*/30` - Regular processing tasks
- **Hourly**: `0 * * * *` - Standard recurring jobs
- **Multi-Hourly**: `0 */2`, `0 */12` - Periodic heavy processing
- **Daily**: `0 5 * * *`, `30 6 * * *` - Once-per-day operations
- **Weekly**: `0 0 * * 0` - Sunday weekly tasks

### Time Distribution Strategy
Jobs are distributed across different times to avoid system overload:
- **Early Morning (0-6 AM)**: Heavy analytics and maintenance
- **Business Hours (7-17)**: User-facing services and notifications
- **Evening (18-23)**: Reporting and batch processing
- **Various Minutes**: `:10`, `:17`, `:22`, `:42` - Load distribution

## Job Categories

### Real-Time Processing
High-frequency jobs for immediate response:
```javascript
{ name: 'escrow', cron: '*/10 * * * *' },
{ name: 'carpool_block_validation', cron: '*/3 * * * *' },
{ name: 'update-incident-events', cron: '*/5 * * * *' },
{ name: 'ridehail-refund-process', cron: '*/5 * * * *' }
```

### Analytics and ETL
Data processing and analysis jobs:
```javascript
{ name: 'analytic-database', cron: '30 5-6 * * *' },
{ name: 'update-bi-mongodb-views', cron: '0 8 * * *' },
{ name: 'hntb-etl', cron: '0 7 * * *' }
```

### User Engagement
Gamification and notification jobs:
```javascript
{ name: 'incentive-notify', cron: '*/30 * * * *' },
{ name: 'add-explorer-challenge', cron: '42 * * * *' },
{ name: 'weather-notify', cron: '1 * * * *' }
```

### Maintenance Tasks
System cleanup and optimization:
```javascript
{ name: 'delete-backup-account', cron: '30 1 * * *' },
{ name: 'purge-parkmobile-cache', cron: '0 8 * * *' },
{ name: 'fix-trip-distance', cron: '30 6 * * *' }
```

## Configuration Management

### Project Detection
```javascript
const config = require('config').app;
const project = require('config').project;

// Conditional job loading based on project type
if (config.project === 'goezy') { /* goezy-specific jobs */ }
if (config.project === 'hcs') { /* hcs-specific jobs */ }
```

### Environment Staging
```javascript
if (project.stage === 'production') { /* production jobs */ }
if (project.stage === 'develop' || project.stage === 'sandbox') { /* test jobs */ }
```

## Performance Considerations
- **Load Distribution**: Jobs scheduled at different times to prevent system overload
- **Resource Management**: Heavy analytics jobs scheduled during low-usage hours
- **Dependency Awareness**: Related jobs scheduled with appropriate intervals
- **Scalability**: Configuration supports multiple project environments

## Security Considerations
- **Environment Isolation**: Different job sets for different deployment stages
- **Resource Access**: Jobs configured with appropriate system permissions
- **Data Privacy**: Sensitive operations scheduled during secure time windows

## Monitoring and Management
- **Job Identification**: Clear naming convention matches job filenames
- **Scheduling Visibility**: Cron expressions provide clear execution timing
- **Environment Control**: Project-specific job loading prevents conflicts
- **Argument Passing**: Support for job-specific parameters

## Usage Integration
This configuration file is used by the job scheduler system to:
1. **Load Job Definitions**: Read scheduled job configurations
2. **Initialize Cron Jobs**: Set up automated execution schedules
3. **Environment Management**: Apply appropriate job sets per environment
4. **Resource Coordination**: Manage system resource allocation across jobs

## Notes
- **Comprehensive Coverage**: Supports multiple transportation service domains
- **Environment Aware**: Adapts job scheduling to deployment environment
- **Performance Optimized**: Distributes processing load across time periods
- **Maintainable Structure**: Clear organization by project and job type
- **Scalable Design**: Supports addition of new projects and job types
- **Production Ready**: Includes both development testing and production operations
- **Critical Infrastructure**: Central configuration for entire job scheduling system