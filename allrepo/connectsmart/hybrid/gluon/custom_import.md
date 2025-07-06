# Gluon Custom Import Module Documentation

## Overview
The `custom_import.py` module provides intelligent import mechanism for the Gluon web framework. It implements smart import syntax transformation, module tracking, and automatic reloading capabilities to enhance web2py application development and deployment.

## Module Information
- **File**: `allrepo/connectsmart/hybrid/gluon/custom_import.py`
- **Component**: Web2py Framework Custom Import System
- **Purpose**: Enhanced import handling with application-aware module resolution
- **Dependencies**: os, sys, threading, gluon.current, gluon._compat
- **Integration**: Web2py application module system

## Key Components

### Global Variables
```python
NATIVE_IMPORTER = builtin.__import__
INVALID_MODULES = set(("", "gluon", "applications", "custom_import"))
_DEFAULT_LEVEL = 0 if sys.version_info[:2] >= (3, 3) else -1
```

### Core Functions

#### custom_import_install()
```python
def custom_import_install():
    """Install the custom importer by replacing builtin.__import__"""
    if builtin.__import__ == NATIVE_IMPORTER:
        INVALID_MODULES.update(sys.modules.keys())
        builtin.__import__ = custom_importer
```

**Purpose:**
- Replaces Python's built-in import mechanism
- Preserves existing loaded modules in invalid set
- Enables web2py-specific import behavior

#### track_changes()
```python
def track_changes(track=True):
    """Enable or disable automatic module change tracking"""
    assert track in (True, False), "must be True or False"
    current.request._custom_import_track_changes = track
```

**Features:**
- **Development Mode**: Automatic module reloading
- **Production Mode**: Disabled tracking for performance
- **Request-Level**: Setting stored in current request

### Main Import Function

#### custom_importer()
```python
def custom_importer(name, globals={}, locals=None, fromlist=(), level=_DEFAULT_LEVEL):
    """
    web2py's custom importer. It behaves like the standard Python importer but
    it tries to transform import statements as something like
    "import applications.app_name.modules.x".
    If the import fails, it falls back on builtin importer.
    """
```

**Parameters:**
- `name`: Module name to import
- `globals`: Global namespace for import resolution
- `locals`: Local namespace (optional)
- `fromlist`: List of names to import from module
- `level`: Import level (absolute/relative)

**Import Transformation:**
```python
# Original import:
import mymodule

# Transformed to:
import applications.appname.modules.mymodule
```

### Import Logic Flow

#### Absolute Import Processing
```python
if (hasattr(current, "request") and 
    level <= 0 and 
    name.partition(".")[0] not in INVALID_MODULES):
    # Try standard import first
    try:
        return NATIVE_IMPORTER(name, globals, locals, fromlist, level)
    except (ImportError, KeyError):
        pass
    
    # Apply web2py transformation
    items = current.request.folder.rstrip(os.sep).split(os.sep)
    modules_prefix = ".".join(items[-2:]) + ".modules"
```

#### Import Types Handled

##### Standard Import (`import x`)
```python
if not fromlist:
    result = None
    for itemname in name.split("."):
        new_mod = base_importer(
            modules_prefix, globals, locals, (itemname,), level
        )
        modules_prefix += "." + itemname
        if result is None:
            try:
                result = sys.modules[modules_prefix]
            except KeyError:
                return NATIVE_IMPORTER(name, globals, locals, fromlist, level)
    return result
```

##### From Import (`from x import y`)
```python
else:
    pname = "%s.%s" % (modules_prefix, name)
    return base_importer(pname, globals, locals, fromlist, level)
```

### Change Tracking System

#### TrackImporter Class
```python
class TrackImporter(object):
    """
    An importer tracking the date of the module files and reloading them when
    they are changed.
    """
    
    THREAD_LOCAL = threading.local()
    PACKAGE_PATH_SUFFIX = os.path.sep + "__init__.py"
```

**Features:**
- **Thread Safety**: Uses threading.local for isolation
- **File Monitoring**: Tracks module file modification times
- **Automatic Reloading**: Reloads changed modules
- **Package Support**: Handles both modules and packages

#### Module File Tracking
```python
def _get_module_file(self, module):
    """Get the absolute path file associated to the module or None."""
    file = getattr(module, "__file__", None)
    if file:
        file = os.path.splitext(file)[0] + ".py"  # Change .pyc for .py
        if file.endswith(self.PACKAGE_PATH_SUFFIX):
            file = os.path.dirname(file)  # Track dir for packages
    return file
```

#### Change Detection
```python
def _reload_check(self, name, globals, locals, level):
    """Update the date associated to the module and reload if changed."""
    module = sys.modules.get(name)
    file = self._get_module_file(module)
    if file:
        date = self._import_dates.get(file)
        new_date = None
        reload_mod = False
        mod_to_pack = False
        
        try:
            new_date = os.path.getmtime(file)
        except:
            # Handle module/package transitions
            # ... transition detection logic
            
        if reload_mod or not date or new_date > date:
            self._import_dates[file] = new_date
        if reload_mod or (date and new_date > date):
            if mod_to_pack:
                # Module turning into package
                mod_name = module.__name__
                del sys.modules[mod_name]
                NATIVE_IMPORTER(mod_name, globals, locals, [], level)
            else:
                reload(module)
```

### Usage Examples

#### Basic Application Import
```python
# In web2py application code
import mymodule              # Imports applications.myapp.modules.mymodule
from mymodule import helper  # Imports from applications.myapp.modules.mymodule
```

#### Development Mode Setup
```python
# Enable change tracking for development
from gluon.custom_import import track_changes
track_changes(True)

# Now modules auto-reload when changed
import mymodule  # Will reload if mymodule.py changes
```

#### Production Mode Setup
```python
# Disable change tracking for production
track_changes(False)

# Standard import behavior without file monitoring
import mymodule  # No auto-reload, better performance
```

### Module Path Resolution

#### Application Detection
```python
# Extract application info from request folder
items = current.request.folder.rstrip(os.sep).split(os.sep)
# Example: /path/to/web2py/applications/myapp
# items[-2:] = ['applications', 'myapp']
modules_prefix = ".".join(items[-2:]) + ".modules"
# Result: "applications.myapp.modules"
```

#### Import Transformation Examples
```python
# Original: import database
# Becomes: import applications.myapp.modules.database

# Original: from utils import helper
# Becomes: from applications.myapp.modules.utils import helper

# Original: import subpack.module
# Becomes: import applications.myapp.modules.subpack.module
```

### Thread Safety

#### Thread-Local Storage
```python
THREAD_LOCAL = threading.local()
```

**Benefits:**
- **Isolation**: Each thread has separate import state
- **Concurrency**: Safe for multi-threaded web applications
- **Performance**: No locking overhead for read operations

### File System Monitoring

#### Modification Time Tracking
```python
self._import_dates = {}  # Import dates of the files of the modules

# Track file modification times
new_date = os.path.getmtime(file)
if reload_mod or not date or new_date > date:
    self._import_dates[file] = new_date
```

#### Module/Package Transitions
```python
# Handle module changing to package and vice versa
if file.endswith(".py"):
    file = os.path.splitext(file)[0]
    reload_mod = os.path.isdir(file) and os.path.isfile(
        file + self.PACKAGE_PATH_SUFFIX
    )
    mod_to_pack = reload_mod
else:  # Package turning into module?
    file += ".py"
    reload_mod = os.path.isfile(file)
```

### Performance Considerations

#### Development vs Production
- **Development**: File monitoring enabled, automatic reloading
- **Production**: File monitoring disabled, no filesystem overhead
- **Fallback**: Always falls back to native importer for compatibility

#### Caching Strategy
```python
# Module date caching
self._import_dates[file] = new_date

# Module system caching
try:
    result = sys.modules[modules_prefix]
except KeyError:
    return NATIVE_IMPORTER(name, globals, locals, fromlist, level)
```

### Error Handling

#### Import Fallback
```python
try:
    return NATIVE_IMPORTER(name, globals, locals, fromlist, level)
except (ImportError, KeyError):
    pass
# Continue with web2py-specific import logic
```

#### File System Errors
```python
try:
    new_date = os.path.getmtime(file)
except:
    self._import_dates.pop(file, None)  # Clean up
    # Handle module/package transitions
```

### Integration Points

#### Web2py Request Context
```python
if hasattr(current, "request"):
    # Application-aware import transformation
    items = current.request.folder.rstrip(os.sep).split(os.sep)
    modules_prefix = ".".join(items[-2:]) + ".modules"
```

#### Module System Integration
```python
# Leverages Python's module system
sys.modules[modules_prefix]  # Module registry access
reload(module)               # Built-in reload functionality
```

### Security Considerations

#### Invalid Module Protection
```python
INVALID_MODULES = set(("", "gluon", "applications", "custom_import"))
# Prevents import of protected modules through transformation
```

#### Path Validation
- **Application Boundaries**: Only transforms imports within application context
- **Fallback Safety**: Native importer handles system modules
- **Error Isolation**: Import errors don't break the import system

This custom import module provides sophisticated import handling for the Gluon framework, enabling application-aware module resolution, development-friendly automatic reloading, and production-optimized performance while maintaining full compatibility with Python's import system.