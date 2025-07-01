# CGI Handler Documentation

## Overview

The CGI Handler (`cgihandler.py`) is a Web2py framework component that provides Common Gateway Interface (CGI) support for Apache web servers. This handler enables Web2py applications to run as CGI scripts, providing a simple deployment mechanism for Web2py applications on Apache servers with mod_cgi or mod_cgid modules.

## Technical Specifications

### Core Components

#### Framework Integration
- **Framework**: Web2py Web Framework
- **License**: LGPLv3
- **Handler Type**: CGI (Common Gateway Interface)
- **WSGI Compatibility**: Full WSGI application support via wsgiref.handlers

#### Dependencies
```python
import os
import sys
import wsgiref.handlers
from gluon.settings import global_settings
import gluon.main
```

### Architecture

#### CGI Implementation
The handler implements a standard CGI interface using Python's `wsgiref.handlers.CGIHandler()` to bridge between the CGI protocol and Web2py's WSGI application.

#### Path Management
```python
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)
sys.path = [path] + [p for p in sys.path if not p == path]
```

#### Runtime Configuration
```python
global_settings.web2py_runtime_handler = True
```

### Apache Configuration

#### Required Modules
- `mod_cgi` or `mod_cgid` must be loaded
- Script alias configuration required

#### httpd.conf Configuration Example
```apache
LoadModule cgi_module modules/mod_cgi.so
ScriptAlias / /path/to/cgihandler.py/

<VirtualHost *:80>
  ServerName web2py.example.com
  ScriptAlias / /users/www-data/web2py/cgihandler.py/

  <Directory /users/www-data/web2py>
    AllowOverride None
    Order Allow,Deny
    Deny from all
    <Files cgihandler.py>
      Allow from all
    </Files>
  </Directory>

  # Static file serving
  AliasMatch ^/([^/]+)/static/(.*) \
           /users/www-data/web2py/applications/$1/static/$2
  <Directory /users/www-data/web2py/applications/*/static/>
    Order Allow,Deny
    Allow from all
  </Directory>

  # Security restrictions
  <Location /admin>
    Deny from all
  </Location>

  <LocationMatch ^/([^/]+)/appadmin>
    Deny from all
  </LocationMatch>

  CustomLog /private/var/log/apache2/access.log common
  ErrorLog /private/var/log/apache2/error.log
</VirtualHost>
```

### Security Features

#### Directory Protection
- Administrative interfaces (`/admin`, `/appadmin`) are denied by default
- Only the CGI handler script is accessible from the web2py directory
- Static files are served directly by Apache for performance

#### Path Validation
```python
if not os.path.isdir('applications'):
    raise RuntimeError('Running from the wrong folder')
```

### Performance Characteristics

#### Process Model
- **New Process**: Each request spawns a new Python process
- **Memory Usage**: Higher memory overhead due to process creation
- **Startup Time**: Slower due to Python interpreter initialization per request
- **Scalability**: Limited by process creation overhead

#### Use Cases
- **Development**: Simple deployment for testing
- **Low Traffic**: Suitable for applications with minimal concurrent users
- **Shared Hosting**: Common deployment option on shared hosting providers

### Deployment Process

#### Installation Steps
1. Place `cgihandler.py` in web2py root directory
2. Make script executable: `chmod +x cgihandler.py`
3. Configure Apache virtual host
4. Ensure proper file permissions
5. Test CGI execution

#### Directory Structure Requirements
```
/path/to/web2py/
├── cgihandler.py
├── applications/
│   └── [app_name]/
├── gluon/
└── ...
```

### Error Handling

#### Runtime Validation
- Validates execution from correct directory
- Ensures applications directory exists
- Proper Python path configuration

#### Common Issues
- **Permission Errors**: Ensure CGI script is executable
- **Path Issues**: Must run from web2py root directory
- **Module Import**: Verify gluon modules are accessible

### Integration Points

#### Web2py Framework
- Uses `gluon.main.wsgibase` as WSGI application
- Integrates with Web2py's global settings
- Supports all Web2py applications and features

#### Apache Integration
- Standard CGI protocol compliance
- Compatible with Apache security modules
- Supports virtual host configurations

### Monitoring and Logging

#### Apache Logs
- Access logs via Apache's CustomLog directive
- Error logs via Apache's ErrorLog directive
- CGI-specific errors appear in Apache error log

#### Web2py Logging
- Application-level logging handled by Web2py framework
- Database logging if configured in Web2py applications

### Best Practices

#### Security
- Restrict access to administrative interfaces
- Use proper file permissions (755 for script, 644 for static files)
- Implement proper error handling
- Keep Web2py framework updated

#### Performance
- Consider FastCGI for higher traffic applications
- Use Apache for static file serving
- Monitor process creation overhead
- Implement proper caching strategies

#### Maintenance
- Regular Apache configuration validation
- Monitor disk space for log files
- Keep CGI handler script updated with Web2py versions
- Test deployments in staging environment

### Alternatives

#### FastCGI Handler
- Better performance through process reuse
- Lower memory overhead
- Faster response times

#### mod_wsgi
- Native WSGI support
- Better Apache integration
- Superior performance characteristics

#### Standalone Server
- Web2py's built-in server
- Development and testing
- Simple deployment scenarios

### Troubleshooting

#### Common Error Messages
- `"Running from the wrong folder"`: Execute from web2py root
- `"Internal Server Error"`: Check Apache error logs
- `"Permission denied"`: Verify file permissions

#### Debugging Steps
1. Verify Apache CGI module is loaded
2. Check script permissions and ownership
3. Validate Apache configuration syntax
4. Test script execution manually
5. Review Apache error logs for detailed error information

This CGI handler provides a straightforward deployment mechanism for Web2py applications on Apache servers, though it's primarily recommended for development and low-traffic production environments due to its process-per-request model.