# Settings Module

## Overview
The settings module provides global configuration management for the Gluon framework. It maintains runtime settings, platform detection, and session management configuration that affects the entire web2py environment.

## Global Configuration

### global_settings
Central storage object for framework-wide settings.

```python
from gluon.storage import Storage
global_settings = Storage()
```

**Type**: Storage object (enhanced dictionary)  
**Purpose**: Thread-safe configuration storage accessible throughout the framework

### Legacy Compatibility
```python
settings = global_settings  # Backward compatibility alias
```

## Platform Detection

### Python Implementation Detection
```python
global_settings.is_pypy = (
    hasattr(platform, 'python_implementation') and 
    platform.python_implementation() == 'PyPy'
)
```

**Purpose**: Enables PyPy-specific optimizations and workarounds

### Jython Detection
```python
global_settings.is_jython = (
    'java' in sys.platform.lower() or 
    hasattr(sys, 'JYTHON_JAR') or 
    str(sys.copyright).find('Jython') > 0
)
```

**Purpose**: Platform-specific threading and I/O handling

### Python Version Detection
```python
global_settings.is_py2 = PY2  # From _compat module
```

**Purpose**: Version-specific code paths and compatibility

## File System Configuration

### Installation Type Detection
```python
global_settings.is_source = os.path.exists(
    os.path.join(global_settings.gluon_parent, 'web2py.py')
)
```

**Values**:
- `True`: Source installation
- `False`: Binary/frozen installation

### Path Configuration
```python
global_settings.gluon_parent = os.environ.get('web2py_path', os.getcwd())
global_settings.applications_parent = global_settings.gluon_parent
```

**gluon_parent**: Root directory of web2py installation  
**applications_parent**: Directory containing applications

### Application Management
```python
global_settings.app_folders = set()  # Tracked application directories
```

**Purpose**: Runtime tracking of available applications

## Session Management

### Database Sessions
```python
if not hasattr(os, 'mkdir'):
    global_settings.db_sessions = True

if global_settings.db_sessions is not True:
    global_settings.db_sessions = set()
```

**Configuration**:
- `True`: All applications use database sessions
- `set()`: Specific applications listed use database sessions
- Not set: File-based sessions (default)

**Usage**:
```python
# Force all apps to use DB sessions
global_settings.db_sessions = True

# Specific apps only
global_settings.db_sessions = {'myapp', 'adminapp'}
```

## Development Configuration

### Debug Mode
```python
global_settings.debugging = False  # Default production mode
```

**Effects**:
- Error page verbosity
- Template caching behavior
- Asset compilation
- Performance monitoring

**Runtime Modification**:
```python
# Enable debugging
global_settings.debugging = True

# Check debug status
if global_settings.debugging:
    print("Debug mode active")
```

## Security Configuration

### Admin Interface Access
```python
# Example commented configuration
# global_settings.trusted_lan_prefix = '192.168.0.'
```

**Purpose**: Allow admin access from trusted LAN when using HTTP

**Security Note**: Admin interface restricted to localhost or HTTPS by default

## Configuration Examples

### Development Environment
```python
# In development setup
global_settings.debugging = True
global_settings.db_sessions = True  # Easier debugging
```

### Production Environment
```python
# In production setup
global_settings.debugging = False
global_settings.db_sessions = {'sessionapp'}  # Selective
```

### Platform-Specific Code
```python
if global_settings.is_pypy:
    # PyPy optimizations
    use_fast_pickle = True
elif global_settings.is_jython:
    # Jython compatibility
    use_threading_local = False
```

## Access Patterns

### Reading Settings
```python
from gluon.settings import global_settings

# Check platform
if global_settings.is_py2:
    import ConfigParser as configparser
else:
    import configparser

# Check installation type
if global_settings.is_source:
    config_path = 'config/development.py'
else:
    config_path = 'config/production.py'
```

### Modifying Settings
```python
# Runtime configuration
global_settings.custom_setting = 'value'

# Application-specific settings
global_settings.app_folders.add('newapp')

# Session configuration
global_settings.db_sessions.add('myapp')
```

## Thread Safety

### Storage Object
The Storage base class provides thread-safe access:

```python
# Safe concurrent access
setting_value = global_settings.get('key', default)

# Safe modification
global_settings.key = 'value'
```

### Best Practices
1. Set configuration early in application lifecycle
2. Avoid frequent runtime modifications
3. Use atomic operations for complex updates

## Integration Points

### Framework Components
Various Gluon modules check settings:

```python
# Session handling
if global_settings.db_sessions:
    use_database_sessions()

# Debug output
if global_settings.debugging:
    show_detailed_errors()

# Platform optimization
if global_settings.is_pypy:
    enable_pypy_features()
```

### Application Code
```python
# In applications/app/models/db.py
from gluon.settings import global_settings

if global_settings.debugging:
    db = DAL('sqlite://storage.sqlite', migrate=True)
else:
    db = DAL('mysql://...', migrate=False)
```

## Environment Variables

### web2py_path
Override default path detection:

```bash
export web2py_path=/opt/web2py
python web2py.py
```

**Effect**: Sets `global_settings.gluon_parent`

## Common Patterns

### Conditional Configuration
```python
def configure_app():
    if global_settings.is_source:
        # Development configuration
        enable_code_reload()
        use_debug_toolbar()
    else:
        # Production configuration  
        enable_caching()
        use_optimized_assets()
```

### Platform Adaptation
```python
def get_session_storage():
    if global_settings.is_jython:
        # Jython-specific session handling
        return JythonSessionStorage()
    elif global_settings.is_pypy:
        # PyPy optimizations
        return PyPySessionStorage()
    else:
        # Default CPython
        return DefaultSessionStorage()
```

### Feature Detection
```python
def supports_feature(feature):
    platform_support = {
        'threading': not global_settings.is_jython,
        'multiprocessing': global_settings.is_py2 or sys.version_info >= (3, 4),
        'async_io': not global_settings.is_py2
    }
    return platform_support.get(feature, True)
```

## Migration Considerations

### Version Upgrades
When upgrading web2py:

1. Check for new settings
2. Update configuration scripts
3. Test platform detection
4. Verify session handling

### Deployment Changes
```python
# Moving from source to binary
if not global_settings.is_source:
    # Adjust paths for binary deployment
    adjust_static_paths()
    compile_templates()
```

## Debugging

### Settings Inspection
```python
def debug_settings():
    print("Platform: PyPy=%s, Jython=%s, Py2=%s" % (
        global_settings.is_pypy,
        global_settings.is_jython, 
        global_settings.is_py2
    ))
    print("Paths: gluon=%s, apps=%s" % (
        global_settings.gluon_parent,
        global_settings.applications_parent
    ))
    print("Sessions: %s" % global_settings.db_sessions)
    print("Debug: %s" % global_settings.debugging)
```

## Best Practices

### Configuration Management
1. Set configuration early in startup
2. Document custom settings
3. Use environment-specific configs
4. Validate setting values

### Performance
1. Cache setting lookups if frequent
2. Avoid deep nested setting access
3. Use direct attribute access when possible

### Security
1. Don't expose sensitive settings
2. Validate user-configurable settings
3. Use secure defaults

## See Also
- Storage class documentation
- Web2py deployment guide
- Platform-specific optimization guides
- Session management documentation