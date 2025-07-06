# ISAPI WSGI Handler Documentation

## Overview

The `isapiwsgihandler.py` module provides an ISAPI (Internet Server Application Programming Interface) integration bridge for deploying web2py applications on Microsoft IIS (Internet Information Services) web server through the WSGI protocol.

## Purpose

This handler enables web2py applications to run on Windows-based IIS servers by:
- Creating an ISAPI extension factory for web2py applications
- Providing automated IIS configuration and installation
- Bridging the gap between IIS and Python WSGI applications
- Supporting enterprise Windows deployment scenarios

## Key Components

### Extension Factory

The `__ExtensionFactory__()` function serves as the main entry point for the ISAPI extension:

```python
def __ExtensionFactory__():
    import os
    import sys
    path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path)
    # ... configuration logic
    return isapi_wsgi.ISAPIThreadPoolHandler(application)
```

**Core Functionality:**
- **Path Resolution**: Determines the web2py installation directory
- **Environment Setup**: Configures Python path and working directory
- **Runtime Configuration**: Sets web2py runtime handler mode
- **WSGI Bridge**: Creates ISAPI-WSGI thread pool handler
- **Application Binding**: Links web2py WSGI application to IIS

### Installation Configuration

The module includes automated IIS configuration:

```python
params = ISAPIParameters()
sm = [ScriptMapParams(Extension="*", Flags=0)]
vd = VirtualDirParameters(Name="appname",
                          Description="Web2py in Python",
                          ScriptMaps=sm,
                          ScriptMapUpdate="replace")
```

**Configuration Elements:**
- **Script Mapping**: Maps all extensions (*) to the ISAPI handler
- **Virtual Directory**: Creates IIS virtual directory for the application
- **Parameter Management**: Handles ISAPI-specific configuration parameters
- **Command Line Processing**: Supports installation via command line

## Dependencies

### External Requirements

- **isapi-wsgi**: Google Code ISAPI-WSGI bridge library
- **Microsoft IIS**: Internet Information Services web server
- **Python for Windows**: Python runtime with Windows extensions
- **ISAPI Extensions**: Windows ISAPI development libraries

### Internal Dependencies

- `gluon.settings`: Web2py global configuration
- `gluon.main`: Core web2py WSGI application
- `isapi.install`: ISAPI installation utilities

## Architecture

### Threading Model

The handler uses ISAPIThreadPoolHandler for concurrent request processing:

```
IIS Request → ISAPI Extension → Thread Pool → WSGI Application → Web2py
```

**Benefits:**
- **Scalability**: Thread pool manages concurrent requests efficiently
- **Resource Management**: Automatic thread lifecycle management
- **Performance**: Reduced thread creation overhead
- **Stability**: Isolated request processing in separate threads

### Integration Flow

1. **IIS Receives Request**: Web server processes incoming HTTP request
2. **ISAPI Activation**: IIS invokes the registered ISAPI extension
3. **Factory Execution**: `__ExtensionFactory__()` creates handler instance
4. **WSGI Bridging**: Request is translated to WSGI format
5. **Web2py Processing**: Application processes request and generates response
6. **Response Translation**: WSGI response is converted back to IIS format

## Configuration

### IIS Setup

```apache
# Example IIS configuration via appcmd
appcmd.exe set config -section:system.web/compilation -targetFramework:v4.0
appcmd.exe set config -section:system.webServer/handlers -+"[name='Python-ISAPI',path='*',verb='*',modules='IsapiModule',scriptProcessor='path\\to\\isapiwsgihandler.dll']"
```

### Installation Command

```bash
python isapiwsgihandler.py install --server=DefaultWebSite
```

**Installation Parameters:**
- `--server`: Target IIS server/site name
- `--vdir`: Virtual directory name (optional)
- `--description`: Application description
- `--replace`: Replace existing configuration

### Environment Variables

Key environment variables for configuration:

- `PYTHONPATH`: Must include web2py directory
- `WEB2PY_PATH`: Web2py installation path
- `IIS_SERVER`: Target IIS server instance
- `VIRTUAL_DIR`: Virtual directory name

## Security Considerations

### IIS Integration Security

- **Application Pool Isolation**: Run in dedicated application pool
- **User Account Management**: Use restricted service account
- **Directory Permissions**: Limit file system access
- **Request Filtering**: Configure IIS request filtering rules

### ISAPI Security Features

```python
# Security-related configurations
params.SecurityFlags = ISAPI_SECURITY_ANONYMOUS
params.AuthFlags = ISAPI_AUTH_NONE
params.AccessFlags = ISAPI_ACCESS_READ | ISAPI_ACCESS_SCRIPT
```

### Best Practices

1. **Least Privilege**: Run with minimal required permissions
2. **Request Validation**: Validate all incoming requests
3. **Error Handling**: Implement comprehensive error handling
4. **Logging**: Enable detailed logging for security monitoring
5. **Updates**: Keep ISAPI-WSGI bridge updated

## Error Handling

### Common Error Scenarios

- **Missing Dependencies**: isapi-wsgi library not installed
- **Path Issues**: Incorrect web2py directory path
- **IIS Configuration**: Invalid virtual directory setup
- **Permission Errors**: Insufficient file system permissions

### Troubleshooting Steps

```python
# Debug configuration
import logging
logging.basicConfig(level=logging.DEBUG)

# Verify paths
print("Web2py path:", path)
print("Applications directory exists:", os.path.isdir('applications'))

# Check ISAPI module
try:
    import isapi_wsgi
    print("ISAPI-WSGI available")
except ImportError:
    print("ISAPI-WSGI not installed")
```

## Performance Optimization

### Thread Pool Configuration

```python
# Optimize thread pool settings
handler = isapi_wsgi.ISAPIThreadPoolHandler(
    application,
    max_threads=50,
    min_threads=10,
    thread_timeout=300
)
```

### Caching Strategies

- **Application Caching**: Cache compiled application modules
- **Static Content**: Configure IIS static content caching
- **Response Compression**: Enable IIS compression
- **Connection Pooling**: Use database connection pooling

## Deployment Guide

### Production Deployment

1. **Install Prerequisites**:
   ```bash
   pip install isapi-wsgi
   ```

2. **Configure IIS**:
   ```bash
   python isapiwsgihandler.py install --server=ProductionSite
   ```

3. **Set Permissions**:
   ```cmd
   icacls "C:\web2py" /grant IIS_IUSRS:RX /T
   ```

4. **Test Installation**:
   ```bash
   curl http://localhost/web2py/default/index
   ```

### Monitoring

- **IIS Logs**: Monitor IIS access and error logs
- **Event Viewer**: Check Windows Event Viewer for ISAPI errors
- **Performance Counters**: Monitor IIS performance counters
- **Application Logs**: Enable web2py application logging

## Integration Examples

### Basic Installation

```python
# Install with default settings
if __name__ == '__main__':
    import sys
    from isapi.install import HandleCommandLine, ISAPIParameters
    
    params = ISAPIParameters()
    # Configure virtual directory
    params.VirtualDirs = [create_virtual_directory()]
    HandleCommandLine(params)
```

### Custom Configuration

```python
# Advanced configuration
def create_custom_handler():
    params = ISAPIParameters()
    params.Name = "Web2pyISAPI"
    params.Description = "Custom Web2py ISAPI Handler"
    params.MaxExtensionSize = 1024 * 1024  # 1MB
    return params
```

This ISAPI WSGI handler provides enterprise-grade Windows/IIS deployment capabilities for web2py applications, ensuring robust integration with Microsoft web server infrastructure while maintaining Python application functionality and performance.