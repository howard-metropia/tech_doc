# ConnectSmart Hybrid Fabric Deployment Automation

🔍 **Quick Summary (TL;DR)**
- Fabric-based deployment automation for Web2py applications with Nginx/uWSGI stack
- fabric | python | deployment | automation | web2py | nginx | uwsgi | ubuntu | server | management
- Primary use cases: automated deployment, server management, backup/restore, maintenance mode
- Python 2.7+ compatibility with Fabric 1.x, Ubuntu 14.04+ server environments

❓ **Common Questions Quick Index**
- **Q: How do I deploy a Web2py application?** → [Usage Methods](#usage-methods)
- **Q: What if deployment fails midway?** → [Important Notes](#important-notes)
- **Q: How to restore from backup?** → [Output Examples](#output-examples)
- **Q: Can I deploy without creating backups?** → [Detailed Code Analysis](#detailed-code-analysis)
- **Q: How to create maintenance mode?** → [Usage Methods](#usage-methods)
- **Q: What servers does this support?** → [Technical Specifications](#technical-specifications)
- **Q: How to troubleshoot permission errors?** → [Important Notes](#important-notes)
- **Q: What's the difference between deploy and git_deploy?** → [Use Cases](#use-cases)
- **Q: How to configure multiple hosts?** → [Technical Specifications](#technical-specifications)
- **Q: What files get deployed by default?** → [Detailed Code Analysis](#detailed-code-analysis)

📋 **Functionality Overview**
**Non-technical explanation:** Like a restaurant manager who can simultaneously update menus across multiple locations, backup old menus, and temporarily post "closed for maintenance" signs - this tool orchestrates Web2py application deployments across multiple servers with safety nets and rollback capabilities. Think of it as a digital theater director coordinating scene changes while the show continues running.

**Technical explanation:** Python Fabric-based deployment orchestration system that automates Web2py application lifecycle management including deployment, backup, rollback, and maintenance operations across multiple Ubuntu servers running Nginx/uWSGI stack.

**Business value:** Reduces deployment time from hours to minutes, eliminates human error in production deployments, provides automatic backup/rollback capabilities, and enables zero-downtime maintenance windows for critical Web2py applications.

**System context:** Core deployment infrastructure for ConnectSmart hybrid applications, integrating with the broader MaaS platform's deployment pipeline and serving as the bridge between development and production environments.

🔧 **Technical Specifications**
- **File:** fabfile.py (178 lines, Medium complexity)
- **Language:** Python 2.7+ with Fabric 1.x framework
- **Dependencies:** 
  - fabric>=1.0.0 (remote execution, critical)
  - crypt (password hashing, required)
  - datetime (timestamping, required)
  - getpass (secure input, required)
- **Compatibility:** Ubuntu 14.04+, Python 2.7-3.6, Web2py 2.0+
- **Configuration:** hosts file or interactive input, sudo access required
- **System requirements:** SSH access, 1GB+ disk space, www-data user/group
- **Security:** SSH key authentication, sudo privileges, encrypted passwords

📝 **Detailed Code Analysis**
**Main Functions:**
- `deploy(appname, all)` - Core deployment with selective file packaging
- `git_deploy(appname, repo)` - Git-based deployment with repository cloning
- `install_web2py()` - Complete Web2py stack installation
- `create_user(username)` - Secure user creation with sudo privileges

**Execution Flow:** Host configuration → Authentication → Task execution → File transfer → Permission adjustment → Service management

**Key Code Patterns:**
```python
# Selective deployment based on file types
if all=='all' or not backup:
    local('zip -r _update.zip * -x *~ -x .* -x \#* -x *.bak -x *.bak2')
else:
    local('zip -r _update.zip */*.py */*/*.py views/*.html views/*/*.html static/*')
```

**Design Patterns:** Command pattern for remote execution, Template method for deployment workflows, Strategy pattern for backup/restore operations

**Error Handling:** Try-finally blocks ensure cleanup, graceful degradation with optional operations, comprehensive permission management

🚀 **Usage Methods**
**Basic Deployment:**
```bash
# Deploy current directory as application
fab -H username@server.com deploy:myapp

# Deploy with full backup
fab -H username@server.com deploy:myapp,all

# Git-based deployment
fab -H username@server.com git_deploy:myapp,username/repository
```

**Server Management:**
```bash
# Install complete Web2py stack
fab -H root@server.com install_web2py

# Create user with proper permissions
fab -H root@server.com create_user:developer

# Web server control
fab -H username@server.com start_webserver
fab -H username@server.com restart_webserver
```

**Maintenance Operations:**
```bash
# Enable maintenance mode
fab -H username@server.com notify:myapp down:myapp

# Disable maintenance mode
fab -H username@server.com up:myapp

# Backup and retrieve
fab -H username@server.com retrieve:myapp
```

📊 **Output Examples**
**Successful Deployment:**
```
[server.com] Executing task 'deploy'
[server.com] sudo: mkdir /home/www-data/web2py/applications/myapp
[server.com] put: _update.zip -> /tmp/_update.zip
[server.com] sudo: unzip -o /tmp/_update.zip
[server.com] sudo: chown -R www-data:www-data *
TO RESTORE: fab restore:myapp.25-12-30-14-30.zip
```

**Backup Creation:**
```bash
# Automatic timestamped backup before deployment
myapp.25-12-30-14-30.zip created
Backup contains: 1,245 files (15.3MB)
Previous version safely stored
```

**Error Scenarios:**
```
[server.com] Fatal error: sudo: unzip: command not found
[server.com] Aborting.
Solution: Install unzip package on target server
```

**Git Deployment Output:**
```
[server.com] sudo: git clone git@github.com:user/repo myapp
[server.com] Cloning into 'myapp'...
[server.com] sudo: chown -R www-data:www-data myapp
Deployment complete: 47 files updated
```

⚠️ **Important Notes**
**Security Considerations:** Requires SSH key authentication, sudo access creates security surface, deployment scripts should use dedicated deployment user, never run as root in production

**Permission Requirements:** www-data group membership required, sudo NOPASSWD for deployment operations, proper SSH key management essential

**Common Troubleshooting:**
- **Permission denied errors:** Check www-data group membership and file ownership
- **Git clone failures:** Verify SSH key access to repository
- **Service restart issues:** Ensure upstart/systemd services are properly configured
- **Backup restoration:** Always test restore procedure in staging environment

**Performance Considerations:** Large applications may timeout during zip operations, consider using deploynobackup for rapid iterations, network bandwidth affects transfer times

**Breaking Changes:** Fabric 2.x requires syntax updates, Python 3 compatibility needs print function syntax, Ubuntu 18+ uses systemd instead of upstart

🔗 **Related File Links**
- **setup-web2py-nginx-uwsgi-ubuntu.sh** - Web2py installation script
- **hosts** - Server configuration file for multi-host deployments
- **/home/www-data/web2py/applications/** - Application deployment directory
- **Web2py routes.py** - URL routing configuration
- **nginx.conf** - Web server configuration
- **uwsgi.ini** - Application server configuration

📈 **Use Cases**
**Development Deployment:** Rapid iteration deployment for testing new features, selective file deployment for faster updates, automatic backup before each deployment

**Production Deployment:** Full application deployment with comprehensive backups, zero-downtime deployment using maintenance mode, git-based deployment for version control integration

**Maintenance Operations:** Scheduled maintenance windows with user notifications, emergency rollback capabilities, application cleanup and optimization

**Multi-Environment Management:** Staging environment synchronization, production hot-fixes, disaster recovery deployment

**Anti-patterns:** Never deploy directly to production without staging validation, avoid running as root user, don't skip backup creation in production

🛠️ **Improvement Suggestions**
**Code Optimization:** Implement parallel deployment for multi-server setups (High priority, Medium effort), add deployment verification and health checks (High priority, Low effort), integrate with CI/CD pipelines (Medium priority, High effort)

**Feature Expansion:** Add database migration support, implement blue-green deployment strategy, create deployment hooks for custom scripts, add metrics collection and deployment analytics

**Technical Debt:** Migrate to Fabric 2.x for Python 3 compatibility, implement proper logging instead of print statements, add comprehensive error handling and retry logic

**Monitoring:** Add deployment success/failure notifications, implement rollback automation, create deployment audit trails

🏷️ **Document Tags**
**Keywords:** fabric, python, deployment, automation, web2py, nginx, uwsgi, ubuntu, server, management, devops, ci-cd, backup, restore, maintenance, ssh, sudo, git, repository

**Technical tags:** #deployment #automation #python #fabric #web2py #nginx #uwsgi #ubuntu #devops #server-management #backup #git-deployment

**Target roles:** DevOps Engineers (Intermediate), System Administrators (Intermediate), Python Developers (Advanced), Site Reliability Engineers (Advanced)

**Difficulty level:** ⭐⭐⭐ (Complex deployment automation requiring server administration knowledge, SSH/sudo configuration, and understanding of Web2py application structure)

**Maintenance level:** Medium (Regular updates needed for security patches, server configuration changes, and application deployment patterns)

**Business criticality:** High (Critical for production deployments, application availability, and disaster recovery operations)

**Related topics:** Server administration, Web2py framework, Nginx configuration, uWSGI deployment, Ubuntu system management, SSH automation, Git workflow integration