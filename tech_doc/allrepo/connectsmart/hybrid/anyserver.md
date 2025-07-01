# anyserver.py Documentation

## 🔍 Quick Summary (TL;DR)

**Function**: Universal WSGI server adapter that provides unified interface for running Web2py applications across 17+ different Python web servers including Rocket, Gunicorn, Tornado, Gevent, and more.

**Keywords**: WSGI | Web2py | server adapter | multi-server | universal deployment | Python web framework | HTTP server | CGI | FastCGI | async server | production deployment | development server

**Primary Use Cases**: 
- Production deployment with choice of optimal server (Gunicorn, uWSGI, Gevent)
- Development testing across different server environments
- Performance benchmarking and server comparison
- Legacy application migration between server technologies

**Compatibility**: Python 2.7+ and 3.x, Web2py framework, requires specific server packages (gunicorn, tornado, gevent, etc.)

## ❓ Common Questions Quick Index

**Q: How do I choose the right server for production?**  
A: Use Gunicorn or uWSGI for production, Gevent for high-concurrency, Rocket for development. [→ Technical Specifications](#technical-specifications)

**Q: What if I get import errors when starting a server?**  
A: Install the required server package (pip install gunicorn/tornado/gevent). [→ Important Notes](#important-notes)

**Q: How to enable profiling for performance debugging?**  
A: Use rocket_with_repoze_profiler server type with -P flag. [→ Usage Methods](#usage-methods)

**Q: Can I run multiple workers for scaling?**  
A: Yes, use Gevent server with -w workers option. [→ Output Examples](#output-examples)

**Q: What's the difference between synchronous and asynchronous servers?**  
A: Sync servers (wsgiref, paste) handle one request at a time; async (tornado, gevent) handle concurrent requests. [→ Detailed Code Analysis](#detailed-code-analysis)

**Q: How to troubleshoot server startup failures?**  
A: Check port availability, server package installation, and Web2py dependencies. [→ Important Notes](#important-notes)

**Q: Which servers support SSL/HTTPS termination?**  
A: Most production servers support SSL; typically handled by reverse proxy (nginx/Apache). [→ Use Cases](#use-cases)

**Q: How to monitor server performance in production?**  
A: Use profiler options, logging, and external monitoring tools like New Relic. [→ Improvement Suggestions](#improvement-suggestions)

## 📋 Functionality Overview

**Non-technical Explanation**: 
Think of anyserver.py as a universal power adapter for electronics - just as one adapter can power different devices by converting electricity to the right format, this file acts as a universal adapter that can run your Web2py application on any of 17+ different web servers. Like choosing between a sports car (fast, single-purpose) versus a truck (heavy-duty, reliable) for different driving needs, you can choose the optimal server for your specific requirements - development, testing, or production deployment.

**Technical Explanation**: 
anyserver.py implements the adapter pattern to provide a unified interface for WSGI server deployment. It encapsulates server-specific initialization logic within static methods of the Servers class, enabling dynamic server selection at runtime while maintaining consistent application behavior across different server implementations.

**Business Value**: 
Eliminates vendor lock-in by providing server flexibility, reduces deployment complexity, enables performance optimization through server selection, and supports gradual migration between technologies without application code changes.

**System Context**: 
Core component of Web2py's deployment infrastructure, bridging the gap between the Web2py application framework and various Python WSGI server implementations in the ConnectSmart hybrid platform.

## 🔧 Technical Specifications

**File Information**:
- **Path**: `/allrepo/connectsmart/hybrid/anyserver.py`
- **Language**: Python 2.7/3.x compatible
- **Type**: WSGI Server Adapter/Launcher
- **Size**: ~12KB, 366 lines
- **Complexity**: Medium (multiple server integrations, CLI handling)

**Dependencies**:
- **Core**: `os`, `sys`, `optparse`, `urllib` (Python standard library)
- **WSGI**: `wsgiref` (built-in reference server)
- **Optional Servers** (install as needed):
  - `gunicorn` (production WSGI server) - HIGH criticality
  - `tornado` (async web framework) - MEDIUM criticality  
  - `gevent` (async networking) - HIGH criticality
  - `eventlet` (concurrent networking) - MEDIUM criticality
  - `cherrypy`/`cheroot` (WSGI server) - MEDIUM criticality
  - `paste` (middleware and utilities) - LOW criticality
  - `twisted` (networking engine) - LOW criticality
  - `waitress` (pure Python WSGI) - MEDIUM criticality

**Compatibility Matrix**:
- Python 2.7: Full support (legacy)
- Python 3.6+: Full support (recommended)
- Web2py: All versions
- Server Dependencies: Version-specific requirements per server package

**Configuration Parameters**:
- `servername`: Server type selection (default: 'rocket')
- `ip`: Bind IP address (default: '127.0.0.1')
- `port`: Port number (default: '8000')
- `workers`: Worker process count (Gevent only)
- `logging`: HTTP request logging (default: False)
- `profiler_dir`: Performance profiling directory

**System Requirements**:
- **Minimum**: Python 2.7+, 512MB RAM, single CPU core
- **Recommended**: Python 3.8+, 2GB+ RAM, multi-core for production servers
- **Network**: Available ports, firewall configuration for chosen port

## 📝 Detailed Code Analysis

**Main Components**:

```python
class Servers:
    @staticmethod
    def gunicorn(app, address, **options):
        # Production-ready WSGI server with worker processes
        # Handles high concurrency, automatic worker recycling
        
    @staticmethod  
    def gevent(app, address, **options):
        # Async server using coroutines for I/O-bound applications
        # Excellent for WebSocket, long-polling scenarios
```

**Execution Flow**:
1. **CLI Parsing**: `optparse` processes command-line arguments with validation
2. **Path Setup**: Sets working directory and Python path for Web2py imports  
3. **Server Selection**: Dynamic method lookup using `getattr(Servers, servername)`
4. **Application Factory**: Creates WSGI application via `gluon.main.wsgibase`
5. **Server Launch**: Calls server-specific initialization with unified parameters

**Design Patterns**:
- **Static Factory Pattern**: Each server method acts as a factory for server instances
- **Adapter Pattern**: Unified interface despite varying server APIs
- **Template Method**: Common initialization steps with server-specific implementations

**Error Handling**:
- **Import Protection**: Try/except blocks for optional server dependencies
- **CLI Validation**: Default values and help text for all parameters
- **Server Failures**: Graceful degradation with error messages

**Performance Characteristics**:
- **Memory**: Varies by server (wsgiref: ~10MB, gunicorn: ~50MB per worker)
- **Concurrency**: Single-threaded (wsgiref) to thousands (gevent/tornado)
- **Startup Time**: 0.1-2 seconds depending on server complexity

## 🚀 Usage Methods

**Basic Command Line Usage**:
```bash
# Development server (single-threaded)
python anyserver.py -s wsgiref -i 127.0.0.1 -p 8000

# Production server with logging
python anyserver.py -s gunicorn -i 0.0.0.0 -p 80 -l

# High-concurrency async server  
python anyserver.py -s gevent -i 0.0.0.0 -p 8080 -w 4

# Performance profiling
python anyserver.py -s rocket_with_repoze_profiler -P /tmp/profiles
```

**Programmatic Usage**:
```python
from anyserver import run
# Run server programmatically
run('gunicorn', '0.0.0.0', 8000, logging=True, softcron=False)
```

**Environment-Specific Configurations**:

*Development*:
```bash
python anyserver.py -s wsgiref -i 127.0.0.1 -p 8000 -l
# Single-threaded, local access, request logging
```

*Staging*:
```bash  
python anyserver.py -s waitress -i 0.0.0.0 -p 8080 -l
# Multi-threaded, external access, logging enabled
```

*Production*:
```bash
python anyserver.py -s gunicorn -i 0.0.0.0 -p 80 -w 4
# Multi-worker, optimized for production load
```

**Advanced Configuration**:
- **Custom Options**: Pass server-specific options via options parameter
- **SSL Configuration**: Typically handled at reverse proxy level
- **Process Management**: Use systemd, supervisor, or container orchestration
- **Load Balancing**: Multiple instances behind nginx/HAProxy

## 📊 Output Examples

**Successful Startup**:
```
starting gunicorn on 0.0.0.0:8000...
[2024-01-15 10:30:45] [INFO] Starting gunicorn 20.1.0
[2024-01-15 10:30:45] [INFO] Listening at: http://0.0.0.0:8000
[2024-01-15 10:30:45] [INFO] Using worker: sync
[2024-01-15 10:30:45] [INFO] Booting worker with pid: 12345
```

**Server Performance Comparison**:
```
wsgiref:    ~100 req/sec,  single-threaded
waitress:   ~500 req/sec,  multi-threaded  
gunicorn:   ~1000 req/sec, multi-process
gevent:     ~2000 req/sec, async I/O
tornado:    ~1500 req/sec, async framework
```

**Error Scenarios**:
```
# Missing server dependency
ImportError: No module named 'gunicorn'
Solution: pip install gunicorn

# Port already in use  
OSError: [Errno 98] Address already in use
Solution: Change port or kill existing process

# Permission denied (port < 1024)
PermissionError: [Errno 13] Permission denied
Solution: Use sudo or port >= 1024
```

**Profiling Output** (rocket_with_repoze_profiler):
```
Profile data saved to: wsgi.prof
Access profile at: http://localhost:8000/__profile__
Top functions by cumulative time:
- application(): 45.2% (2.1s)
- database queries: 23.1% (1.0s)  
- template rendering: 15.7% (0.7s)
```

## ⚠️ Important Notes

**Security Considerations**:
- **Binding Interface**: Never bind to 0.0.0.0 in development; use 127.0.0.1
- **Port Permissions**: Ports < 1024 require root privileges
- **Reverse Proxy**: Always use nginx/Apache for SSL termination in production
- **Process Isolation**: Run with dedicated user account, not root

**Performance Gotchas**:
- **wsgiref**: Development only - single-threaded, not for production
- **Global Interpreter Lock**: Python GIL limits threading benefits
- **Memory Leaks**: Some servers may leak memory under high load
- **File Descriptors**: High-concurrency servers need increased ulimits

**Common Troubleshooting**:

*Symptom*: Server won't start  
*Diagnosis*: Check port availability with `netstat -tlnp | grep :8000`  
*Solution*: Kill existing process or change port

*Symptom*: Import errors for server modules  
*Diagnosis*: Missing optional dependencies  
*Solution*: `pip install [server-name]` (gunicorn, tornado, etc.)

*Symptom*: Poor performance under load  
*Diagnosis*: Wrong server choice for workload  
*Solution*: Switch to async server (gevent, tornado) for I/O-bound apps

**Breaking Changes**:
- Python 2 to 3 migration: String handling differences
- Server version updates: API changes in newer versions
- Web2py updates: WSGI interface modifications

## 🔗 Related File Links

**Project Structure**:
```
hybrid/
├── anyserver.py          # This file - server launcher
└── [other hybrid files]  # Additional Web2py hybrid components
```

**Dependencies**:
- `gluon/main.py`: Web2py WSGI application factory
- `gluon/rocket.py`: Default Rocket server implementation  
- `gluon/settings.py`: Global Web2py configuration

**Configuration**:
- Web2py app configuration in individual application directories
- Server-specific config files (gunicorn.conf.py, etc.)

**Related Documentation**:
- Web2py Book: Deployment chapter
- Server-specific documentation (Gunicorn docs, Tornado docs)
- WSGI specification (PEP 3333)

## 📈 Use Cases

**Development Workflow**:
- **Local Testing**: Use wsgiref for simple development server
- **Integration Testing**: Test with production-like servers (waitress, gunicorn)
- **Performance Testing**: Compare different servers under load
- **Debugging**: Use profiling-enabled servers for bottleneck identification

**Production Deployment**:
- **High Traffic**: Gunicorn with multiple workers behind reverse proxy
- **Real-time Apps**: Gevent/Tornado for WebSocket support
- **Legacy Systems**: Paste/CherryPy for compatibility requirements
- **Container Deployment**: Waitress for simple containerized deployments

**Migration Scenarios**:
- **Server Evaluation**: Test application compatibility across servers
- **Gradual Migration**: Phase out legacy servers with minimal risk
- **Disaster Recovery**: Quick failover between server technologies
- **Load Testing**: Benchmark performance across different server types

**Anti-patterns**:
- ❌ **Using wsgiref in production**: Single-threaded, development only
- ❌ **Running as root**: Security risk, use dedicated user account
- ❌ **No reverse proxy**: Direct exposure, missing SSL termination
- ❌ **Ignoring server-specific tuning**: Each server has optimal configuration

## 🛠️ Improvement Suggestions

**Code Optimization** (Medium effort, High impact):
- **Async/await support**: Modernize for Python 3.5+ async syntax
- **Configuration management**: YAML/JSON config file support instead of CLI-only
- **Health checks**: Built-in health check endpoints for monitoring
- **Graceful shutdown**: Signal handling for clean server shutdown

**Feature Expansion** (High effort, Medium impact):
- **Auto-scaling**: Dynamic worker adjustment based on load
- **Hot reloading**: Application reload without server restart  
- **Server pooling**: Multiple server types running simultaneously
- **Monitoring integration**: Built-in metrics export (Prometheus, StatsD)

**Technical Debt Reduction** (Low effort, High impact):
- **Python 2 removal**: Drop legacy Python 2 support
- **Error handling**: More specific exception handling and error messages
- **Logging standardization**: Use Python logging module instead of print statements
- **Type hints**: Add type annotations for better IDE support

**Maintenance Recommendations**:
- **Monthly**: Update server package dependencies for security patches
- **Quarterly**: Performance benchmarking across server types
- **Annually**: Evaluate new server technologies (ASGI servers like Uvicorn)
- **Continuous**: Monitor deprecation warnings from server packages

## 🏷️ Document Tags

**Keywords**: anyserver, WSGI, Web2py, server-adapter, multi-server, deployment, Python-web-server, HTTP-server, production-deployment, gunicorn, tornado, gevent, async-server, server-launcher, universal-adapter, CGI, FastCGI, performance-tuning, scalability

**Technical Tags**: #wsgi #web2py #python #server-adapter #deployment #async #production #http-server #gunicorn #tornado #gevent #performance

**Target Roles**: 
- **DevOps Engineers** (⭐⭐⭐): Server deployment and configuration
- **Backend Developers** (⭐⭐⭐): Application deployment and debugging  
- **System Administrators** (⭐⭐): Server management and monitoring
- **Performance Engineers** (⭐⭐⭐): Server optimization and benchmarking

**Difficulty Level**: ⭐⭐⭐ (Intermediate)
- Requires understanding of WSGI, HTTP servers, and deployment concepts
- Multiple server options with different characteristics
- Production deployment considerations

**Maintenance Level**: Medium
- Server dependency updates required
- Performance monitoring needed
- Configuration adjustments for different environments

**Business Criticality**: High
- Core deployment infrastructure component
- Single point of failure for application availability
- Performance directly impacts user experience

**Related Topics**: WSGI deployment, Python web servers, async programming, load balancing, reverse proxy configuration, containerization, performance monitoring, production deployment strategies