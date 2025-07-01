# Gluon Import All Module Technical Documentation

## Module: `import_all.py`

### Overview
The `import_all` module serves as a comprehensive module checker and preloader for the Gluon web framework. It performs three critical functions: validates that required Python modules are properly installed, provides py2exe and py2app with a complete list of modules for binary packaging, and optionally preloads modules into memory to improve HTTP response times.

### Table of Contents
1. [Purpose and Functions](#purpose-and-functions)
2. [Module Categories](#module-categories)
3. [Dependency Management](#dependency-management)
4. [Version Compatibility](#version-compatibility)
5. [Error Handling](#error-handling)
6. [Usage Examples](#usage-examples)
7. [Module Lists](#module-lists)

### Purpose and Functions

The module has three primary purposes:

1. **Dependency Validation**: Ensures all required Python standard library modules are available
2. **Binary Packaging**: Provides py2exe/py2app with comprehensive module lists
3. **Performance Optimization**: Optionally preloads modules for faster HTTP responses

### Module Categories

#### Core Python Modules
Essential standard library modules that web2py depends on:

```python
base_modules = [
    # System and OS interaction
    "os", "sys", "platform", "signal",
    
    # File and data handling
    "codecs", "csv", "pickle", "zipfile", "tarfile",
    
    # Network and web
    "urllib", "urllib2", "urlparse", "httplib", "cgi",
    
    # Date and time
    "datetime", "time", "calendar",
    
    # Data structures and algorithms
    "collections", "heapq", "bisect", "array",
    
    # Text processing
    "re", "string", "textwrap", "unicodedata",
    
    # Cryptography and hashing
    "hashlib", "hmac", "uuid",
    
    # Email handling
    "email", "email.mime", "smtplib",
    
    # Database
    "sqlite3",
    
    # And many more...
]
```

#### Alert Dependencies
Critical modules that must be present - installation will fail if missing:

```python
alert_dependency = ["hashlib", "uuid"]
```

#### Python Version Specific Modules
Modules added or deprecated based on Python version:

```python
# Added in Python 2.7+
if python_version >= "2.7":
    base_modules += ["argparse", "json", "multiprocessing"]

# Deprecated in Python 2.7
py27_deprecated = [
    "mhlib", "multifile", "mimify", "sets", "MimeWriter"
]
```

### Dependency Management

#### Critical Dependencies Check
```python
for module in base_modules + contributed_modules:
    try:
        __import__(module, globals(), locals(), [])
    except:
        # Raise an exception if the current module is a dependency
        if module in alert_dependency:
            msg = "Missing dependency: %(module)s\n" % locals()
            msg += "Try the following command: "
            msg += "easy_install-%(python_version)s -U %(module)s" % locals()
            raise ImportError(msg)
```

#### Installation Error Messages
The module provides helpful error messages for missing critical dependencies:

```
Missing dependency: hashlib
Try the following command: easy_install-2.7 -U hashlib
```

### Version Compatibility

#### Python Version Detection
```python
python_version = sys.version[:3]  # e.g., "2.7", "3.6"
```

#### Version-Specific Module Loading
- **Python 2.7+**: Adds `argparse`, `json`, `multiprocessing`
- **Python 2.7+**: Removes deprecated modules like `mhlib`, `sets`

### Module Lists

#### Complete Base Modules List
```python
base_modules = [
    # Audio/Media
    "aifc", "audioop", "wave", "sunau", "sndhdr",
    
    # Archive/Compression
    "bz2", "gzip", "zipfile", "tarfile", "zlib",
    
    # Data Processing
    "array", "bisect", "collections", "heapq",
    
    # Database
    "anydbm", "dumbdbm", "whichdb", "sqlite3",
    
    # Date/Time
    "calendar", "datetime", "time",
    
    # Development Tools
    "dis", "doctest", "inspect", "pdb", "profile", "pstats",
    
    # Email
    "email", "email.mime.text", "email.mime.multipart",
    "mailbox", "mailcap", "smtplib", "smtpd",
    
    # Encoding/Decoding
    "base64", "binascii", "binhex", "codecs", "encodings.idna",
    "quopri", "uu", "uuencode",
    
    # File Operations
    "filecmp", "fileinput", "fnmatch", "glob", "shutil", "tempfile",
    
    # Functional Programming
    "functools", "itertools", "operator",
    
    # GUI (Tkinter)
    "Tix", "Tkinter",
    
    # Hashing/Crypto
    "hashlib", "hmac", "uuid",
    
    # Internet Protocols
    "ftplib", "httplib", "imaplib", "nntplib", "poplib",
    "robotparser", "telnetlib", "urllib", "urllib2", "urlparse",
    
    # Math
    "cmath", "decimal", "math", "random",
    
    # Networking
    "socket", "SocketServer", "select",
    
    # OS Interface
    "os", "platform", "stat", "statvfs",
    
    # Parsing
    "ConfigParser", "HTMLParser", "parser", "sgmllib", "xml.parsers.expat",
    
    # String Processing
    "re", "string", "StringIO", "cStringIO", "struct", "textwrap",
    
    # System
    "atexit", "gc", "signal", "sys", "sysconfig", "warnings",
    
    # Threading/Async
    "asynchat", "asyncore", "threading", "thread", "Queue",
    
    # Web/CGI
    "cgi", "cgitb", "Cookie", "cookielib", "wsgiref",
    
    # And many more standard library modules...
]
```

### Usage Examples

#### Basic Import Validation
```python
# The module automatically runs when imported
import gluon.import_all

# This will check all modules and raise ImportError for missing critical deps
```

#### Binary Packaging with py2exe
```python
# setup.py for py2exe
from distutils.core import setup
import py2exe
import gluon.import_all

# py2exe will use the imported modules to determine what to include
setup(
    windows=[{"script": "web2py.py"}],
    options={
        "py2exe": {
            "includes": gluon.import_all.base_modules,
            "excludes": gluon.import_all.py27_deprecated
        }
    }
)
```

#### Custom Module Checking
```python
def check_optional_modules():
    """Check for optional modules that enhance functionality"""
    optional_modules = [
        "PIL",           # Python Imaging Library
        "matplotlib",    # Plotting
        "numpy",         # Numerical computing
        "scipy",         # Scientific computing
        "lxml",          # XML processing
        "psycopg2",      # PostgreSQL adapter
        "pymongo",       # MongoDB driver
    ]
    
    available = []
    missing = []
    
    for module in optional_modules:
        try:
            __import__(module)
            available.append(module)
        except ImportError:
            missing.append(module)
    
    return available, missing

# Usage
available, missing = check_optional_modules()
print(f"Available optional modules: {available}")
print(f"Missing optional modules: {missing}")
```

#### Performance Preloading
```python
def preload_modules():
    """Preload commonly used modules for better performance"""
    import time
    start_time = time.time()
    
    # Preload web2py's commonly used modules
    preload_list = [
        "re", "datetime", "json", "uuid", "hashlib",
        "urllib", "email", "sqlite3", "csv"
    ]
    
    loaded = 0
    for module in preload_list:
        try:
            __import__(module)
            loaded += 1
        except ImportError:
            pass
    
    load_time = time.time() - start_time
    print(f"Preloaded {loaded} modules in {load_time:.3f} seconds")

# Call during application startup
preload_modules()
```

### Error Handling

#### Graceful Degradation
```python
def safe_import_check():
    """Check module availability without raising exceptions"""
    results = {}
    
    for module in gluon.import_all.base_modules:
        try:
            __import__(module)
            results[module] = "available"
        except ImportError as e:
            results[module] = f"missing: {e}"
        except Exception as e:
            results[module] = f"error: {e}"
    
    return results

# Generate module availability report
module_status = safe_import_check()
for module, status in module_status.items():
    if "missing" in status or "error" in status:
        print(f"WARNING: {module} - {status}")
```

#### Dependency Resolution
```python
def resolve_dependencies():
    """Provide installation commands for missing dependencies"""
    import sys
    python_version = sys.version[:3]
    
    missing_critical = []
    
    for module in gluon.import_all.alert_dependency:
        try:
            __import__(module)
        except ImportError:
            missing_critical.append(module)
    
    if missing_critical:
        print("Critical dependencies missing:")
        for module in missing_critical:
            print(f"  pip install {module}")
            print(f"  easy_install-{python_version} -U {module}")
        return False
    
    return True
```

### Development Integration

#### Testing Framework Integration
```python
def test_module_availability():
    """Unit test for module availability"""
    import unittest
    
    class TestModuleAvailability(unittest.TestCase):
        def test_critical_modules(self):
            """Test that critical modules are available"""
            for module in gluon.import_all.alert_dependency:
                with self.subTest(module=module):
                    try:
                        __import__(module)
                    except ImportError:
                        self.fail(f"Critical module {module} not available")
        
        def test_base_modules(self):
            """Test base module availability (warnings only)"""
            unavailable = []
            for module in gluon.import_all.base_modules:
                try:
                    __import__(module)
                except ImportError:
                    unavailable.append(module)
            
            if unavailable:
                print(f"Warning: {len(unavailable)} modules unavailable")
    
    return unittest.TestLoader().loadTestsFromTestCase(TestModuleAvailability)
```

#### CI/CD Integration
```python
def generate_requirements():
    """Generate requirements.txt from available modules"""
    import pkg_resources
    
    available_packages = []
    
    for module in gluon.import_all.base_modules:
        try:
            __import__(module)
            # Try to get package info
            try:
                pkg = pkg_resources.get_distribution(module)
                available_packages.append(f"{pkg.project_name}=={pkg.version}")
            except:
                pass  # Standard library module
        except ImportError:
            pass
    
    with open('requirements.txt', 'w') as f:
        for package in sorted(available_packages):
            f.write(f"{package}\n")
```

### Best Practices

1. **Early Import**: Import this module early in application startup
2. **Error Handling**: Don't ignore ImportError exceptions for critical modules
3. **Version Testing**: Test across different Python versions
4. **Documentation**: Document any additional module requirements
5. **Graceful Degradation**: Design features to work without optional modules

### Security Considerations

1. **Module Validation**: Verify that imported modules are legitimate
2. **Path Security**: Ensure import paths are not compromised
3. **Version Checking**: Keep track of module versions for security updates

### Module Metadata

- **License**: LGPLv3 (web2py license)
- **Purpose**: Module validation and preloading
- **Thread Safety**: Yes (import operations are thread-safe)
- **Side Effects**: Imports many standard library modules
- **Performance**: May increase startup time but improves runtime performance