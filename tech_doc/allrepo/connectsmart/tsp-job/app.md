# TSP Job Service CLI Entry Point

## 🔍 Quick Summary (TL;DR)
Command-line interface bootstrap for the Transportation Service Provider (TSP) Job service that manages scheduled background jobs, batch processing, and maintenance tasks in the MaaS platform.

**Keywords:** tsp-job | cli | command-line | bootstrap | scheduler | background-jobs | batch-processing | maas-core | transportation | mobility | job-runner | task-scheduler | service-automation

**Primary Use Cases:**
- Running scheduled background jobs for transit operations
- Executing batch processing tasks for data analytics
- Managing maintenance and cleanup operations
- Providing CLI access to service functionality

**Compatibility:** Node.js >=16, @maas/core framework, Unix-like systems (Linux/macOS)

## ❓ Common Questions Quick Index
1. **Q: How do I run the TSP job scheduler?** → [Usage Methods](#usage-methods)
2. **Q: What background jobs are available?** → [Functionality Overview](#functionality-overview)
3. **Q: How do I run in development vs production mode?** → [Usage Methods](#usage-methods)
4. **Q: What if the job fails to start?** → [Important Notes](#important-notes)
5. **Q: How do I add new scheduled jobs?** → [Related File Links](#related-file-links)
6. **Q: What's the difference between api and schedule modes?** → [Usage Methods](#usage-methods)
7. **Q: How do I monitor job execution?** → [Output Examples](#output-examples)
8. **Q: What databases does this connect to?** → [Technical Specifications](#technical-specifications)
9. **Q: How do I troubleshoot job failures?** → [Important Notes](#important-notes)
10. **Q: Can I run specific jobs manually?** → [Usage Methods](#usage-methods)
11. **Q: What's the performance impact of running jobs?** → [Important Notes](#important-notes)
12. **Q: How do I scale job processing?** → [Improvement Suggestions](#improvement-suggestions)

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **mission control center** for a transportation company's automated tasks - like having a digital supervisor that runs important background jobs 24/7. Similar to how a **factory assembly line** has automated stations performing specific tasks, this service orchestrates various transportation-related jobs. It's also like a **smart home system** that automatically performs maintenance tasks on schedule without human intervention.

**Technical explanation:**
CLI bootstrap service that initializes the @maas/core framework and provides command-line access to the TSP job processing system. Uses Commander.js for argument parsing and delegates actual functionality to the core framework's job scheduling and execution engine.

**Business value:** Ensures critical transportation operations run continuously through automated job processing, including data synchronization, user notifications, payment processing, and system maintenance tasks essential for mobility services.

**System context:** Acts as the operational backbone for the TSP API service, handling background processing that supports real-time transportation features, user engagement, and data analytics in the broader MaaS ecosystem.

## 🔧 Technical Specifications

**File Information:**
- **Name:** app.js
- **Path:** /home/datavan/METROPIA/metro_combine/allrepo/connectsmart/tsp-job/app.js
- **Language:** JavaScript (Node.js)
- **Type:** CLI Entry Point / Bootstrap
- **File Size:** 9 lines (minimal Bootstrap)
- **Complexity Score:** ⭐ (Very Low - delegated to framework)

**Dependencies:**
- **@maas/core:** ^1.2.6 (Critical) - Core framework providing job infrastructure
- **Node.js:** >=16 (Required) - Runtime environment
- **Commander.js:** ^8.3.0 (Embedded in core) - CLI argument parsing
- **package.json:** Local - Version and configuration metadata

**System Requirements:**
- **Minimum:** Node.js 16+, 512MB RAM, 100MB disk space
- **Recommended:** Node.js 18+, 2GB RAM, 1GB disk space
- **Production:** Node.js 18+, 4GB RAM, 10GB disk space, Redis, MySQL, MongoDB

**Environment Variables:**
- Standard @maas/core configuration variables
- Database connection strings (MySQL, MongoDB, Redis)
- AWS credentials and region settings
- Third-party API keys (Google Maps, HERE, Stripe)

**Security Requirements:**
- Proper file permissions (755 for executable)
- Secure environment variable handling
- Database access controls
- API key rotation policies

## 📝 Detailed Code Analysis

**Main Components:**
```javascript
#!/usr/bin/env node                    // Unix shebang for CLI execution
require('@maas/core/bootstrap');       // Initialize framework bootstrapping
const { getProgram } = require('@maas/core'); // Import CLI program factory
const pjson = require('./package.json');      // Load package metadata
const program = getProgram();          // Create Commander.js instance
program.version(pjson.version);       // Set version from package.json
program.parse(process.argv);          // Parse command-line arguments
```

**Execution Flow:**
1. **Bootstrap Phase:** Framework initialization and dependency injection
2. **Program Setup:** Commander.js configuration with version info
3. **Argument Parsing:** Command-line parameter processing
4. **Framework Delegation:** Hands control to @maas/core for job execution

**Design Patterns:**
- **Bootstrap Pattern:** Minimal entry point with framework delegation
- **Factory Pattern:** getProgram() creates configured CLI instance
- **Command Pattern:** CLI arguments mapped to job execution commands

**Error Handling:**
- Framework-level error handling in @maas/core
- Process exit codes for success/failure states
- Logging through core framework logging system

**Resource Management:**
- Memory management delegated to framework
- Database connection pooling in core services
- Graceful shutdown handling for long-running jobs

## 🚀 Usage Methods

**Basic CLI Usage:**
```bash
# Run as binary (if installed globally)
maas api                    # Start API server mode
maas schedule              # Start job scheduler mode
maas -h                    # Show help information
maas --version             # Display version

# Direct execution
node app.js api            # API server mode
node app.js schedule       # Scheduler mode
node app.js --help         # Help information
```

**Development Mode:**
```bash
npm run dev                # Development server with auto-reload
npm run schedule           # Development scheduler
npm run cli                # Direct CLI execution
```

**Production Mode:**
```bash
npm run prod               # Production server mode
npm run prod schedule      # Production scheduler
```

**Advanced Configuration:**
```bash
# Environment-specific execution
NODE_ENV=production node app.js schedule
NODE_ENV=staging node app.js api -p

# With custom configuration
CONFIG_PATH=/custom/config node app.js schedule
```

**Integration Examples:**
```bash
# Docker container usage
docker run tsp-job node app.js schedule

# PM2 process management
pm2 start app.js --name "tsp-scheduler" -- schedule
pm2 start app.js --name "tsp-api" -- api
```

## 📊 Output Examples

**Successful Scheduler Start:**
```
TSP Job Scheduler v0.1.0
✓ Connected to MySQL database
✓ Connected to MongoDB cluster
✓ Connected to Redis cache
✓ Loaded 47 job definitions
✓ Scheduler started successfully
[2025-07-02 10:30:00] INFO: Next job: incentive-process in 2 minutes
[2025-07-02 10:30:00] INFO: Active jobs: 3, Queue size: 12
```

**API Server Mode:**
```
TSP Job API v0.1.0
✓ Server listening on port 3000
✓ Health check endpoint active
✓ Job management API ready
[2025-07-02 10:30:00] INFO: API server started
[2025-07-02 10:30:00] INFO: Available endpoints: /health, /jobs, /status
```

**Job Execution Success:**
```
[2025-07-02 10:32:00] INFO: Starting job: incentive-process
[2025-07-02 10:32:05] INFO: Processed 1,247 user incentives
[2025-07-02 10:32:05] INFO: Updated 892 point balances
[2025-07-02 10:32:05] SUCCESS: Job completed in 5.2 seconds
```

**Error Conditions:**
```
[2025-07-02 10:30:00] ERROR: Database connection failed
[2025-07-02 10:30:00] ERROR: MySQL: Connection timeout after 30s
[2025-07-02 10:30:00] FATAL: Unable to start scheduler
Process exited with code 1
```

**Version Information:**
```bash
$ node app.js --version
0.1.0

$ node app.js --help
Usage: app [options] [command]
Options:
  -V, --version  display version number
  -h, --help     display help for command
Commands:
  api           Start API server
  schedule      Start job scheduler
```

## ⚠️ Important Notes

**Security Considerations:**
- Executable runs with Node.js permissions - ensure proper user privileges
- Environment variables may contain sensitive credentials
- Job execution can access all connected databases and external APIs
- Implement proper logging rotation to prevent disk space issues

**Common Troubleshooting:**
- **Job fails to start:** Check database connections and environment variables
- **Permission denied:** Ensure app.js has executable permissions (chmod +x app.js)
- **Version conflicts:** Verify Node.js version compatibility (>=16)
- **Memory issues:** Monitor heap usage during large batch jobs
- **Database timeouts:** Check connection pool settings and network connectivity

**Performance Considerations:**
- Job scheduler can consume significant CPU during peak processing
- Memory usage scales with job complexity and data volume
- Database connection limits may be reached with concurrent jobs
- Monitor disk I/O for jobs that process large datasets

**Scaling Recommendations:**
- Use PM2 cluster mode for API server instances
- Implement job queue partitioning for high-volume processing
- Consider separate job worker processes for different job types
- Monitor and tune database connection pool sizes

**Breaking Changes:**
- Node.js version updates may affect @maas/core compatibility
- Database schema changes require migration coordination
- Environment variable changes need deployment updates

## 🔗 Related File Links

**Core Configuration:**
- `/config/default.js` - Main service configuration
- `/config/database.js` - Database connection settings
- `/package.json` - Dependencies and scripts
- `/knexfile.js` - Database migration configuration

**Job Definitions:**
- `/src/jobs/` - Individual job implementation files
- `/src/schedule.js` - Job scheduling configuration
- `/src/services/` - Business logic services used by jobs

**Supporting Infrastructure:**
- `/src/models/` - Database models and schemas
- `/src/helpers/` - Utility functions and helpers
- `/database/migrations/` - Database schema migrations

**Testing and Documentation:**
- `/test/` - Unit and integration tests
- `/docs/` - Additional documentation
- `README.md` - Project overview and setup instructions

**Related Services:**
- `../tsp-api/app.js` - Main TSP API service
- `../admin-platform-api/` - Administrative interface
- `../../gomyway/maas-workspace/` - Monorepo workspace

## 📈 Use Cases

**Daily Operations:**
- Automated incentive calculation and distribution
- Transit alert processing and notification delivery
- Payment processing and reconciliation
- User engagement and retention campaigns

**Development Scenarios:**
- Local development with hot-reload scheduler
- Testing new job implementations
- Database migration execution
- Performance profiling and optimization

**Production Deployment:**
- Containerized job processing in Kubernetes
- Horizontal scaling with multiple scheduler instances
- Blue-green deployment of job updates
- Disaster recovery and failover scenarios

**Maintenance Tasks:**
- Database cleanup and archival operations
- Cache warming and optimization
- Report generation and data exports
- System health monitoring and alerting

**Anti-patterns to Avoid:**
- Running long-running jobs in API mode
- Mixing scheduler and API functionality in same process
- Ignoring job failure alerts and monitoring
- Hardcoding configuration values instead of using environment variables

## 🛠️ Improvement Suggestions

**Performance Optimization:**
- Implement job result caching (Redis) - **High Priority, Medium Effort**
- Add job execution parallelization - **Medium Priority, High Effort**
- Optimize database queries in job services - **High Priority, Medium Effort**
- Implement job queue prioritization - **Medium Priority, Low Effort**

**Feature Enhancements:**
- Add job execution history API - **Medium Priority, Medium Effort**
- Implement job dependency management - **Low Priority, High Effort**
- Add real-time job monitoring dashboard - **Medium Priority, High Effort**
- Support for job parameter validation - **High Priority, Low Effort**

**Operational Improvements:**
- Add comprehensive health check endpoints - **High Priority, Low Effort**
- Implement job execution metrics collection - **Medium Priority, Medium Effort**
- Add automated job failure recovery - **High Priority, High Effort**
- Support for job execution environments (dev/staging/prod) - **Medium Priority, Low Effort**

**Maintenance Schedule:**
- Weekly: Review job execution logs and performance metrics
- Monthly: Update dependencies and security patches
- Quarterly: Performance optimization and resource usage review
- Annually: Architecture review and modernization planning

## 🏷️ Document Tags

**Keywords:** #cli #nodejs #transportation #job-scheduler #background-processing #automation #mobility #maas #batch-jobs #service-orchestration #transit #scheduler #command-line #bootstrap #framework #task-runner #cron-jobs #worker-process #microservice #api-gateway

**Technical Tags:** #node-js #commander-js #bootstrap-pattern #cli-application #job-processing #service-automation #framework-delegation #process-management #background-services #task-scheduling

**Target Roles:** Backend Developers (Intermediate), DevOps Engineers (Intermediate), System Administrators (Beginner), Transportation Engineers (Advanced)

**Difficulty Level:** ⭐⭐ (Easy to run, moderate to extend - complexity lies in job implementations)

**Maintenance Level:** Medium (requires regular monitoring and updates)

**Business Criticality:** High (essential for automated transportation operations)

**Related Topics:** #microservices #job-queues #background-processing #cli-tools #service-automation #transportation-tech #mobility-services #distributed-systems #process-orchestration #operational-automation