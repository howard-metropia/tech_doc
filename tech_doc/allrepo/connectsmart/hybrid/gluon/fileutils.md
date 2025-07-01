# Gluon FileUtils Module Technical Documentation

## Module: `fileutils.py`

### Overview
The `fileutils` module provides comprehensive file and directory operations for the Gluon web framework. It includes utilities for file I/O, directory management, version parsing, web2py application packaging, and cross-platform path handling with special support for Google App Engine environments.

### Table of Contents
1. [Dependencies](#dependencies)
2. [Core Functions](#core-functions)
3. [Version Parsing](#version-parsing)
4. [File Operations](#file-operations)
5. [Directory Operations](#directory-operations)
6. [Archive Operations](#archive-operations)
7. [Web2py Specific Functions](#web2py-specific-functions)
8. [Usage Examples](#usage-examples)

### Dependencies
```python
import datetime
import glob
import logging
import os
import re
import shutil
import sys
import tarfile
import time
from gzip import open as gzopen
from gluon import storage
from gluon._compat import PY2
from gluon.http import HTTP
from gluon.recfile import generate
from gluon.settings import global_settings
```

### Core Functions

#### Version Parsing

##### `parse_semantic(version)`
Parses semantic version strings according to http://semver.org/ rules.

**Parameters:**
- `version` (str): SemVer string (e.g., "Version 1.99.0-rc.1+timestamp.2011.09.19.08.23.26")

**Returns:**
- `tuple`: (Major, Minor, Patch, Release, Build Date) or None

**Example:**
```python
version_info = parse_semantic("Version 2.1.0-beta+timestamp.2023.01.15.10.30.45")
# Returns: (2, 1, 0, 'beta', datetime(2023, 1, 15, 10, 30, 45))
```

##### `parse_legacy(version)`
Parses legacy version strings.

**Parameters:**
- `version` (str): Legacy version string (e.g., "Version 1.99.0 (2011-09-19 08:23:26)")

**Returns:**
- `tuple`: (Major, Minor, Patch, Release, Build Date)

##### `parse_version(version)`
Attempts to parse SemVer, falls back to legacy format.

**Parameters:**
- `version` (str): Version string in either format

**Returns:**
- `tuple`: Version information

### File Operations

#### `open_file(filename, mode)`
Opens a file with proper encoding handling for Python 2/3 compatibility.

**Parameters:**
- `filename` (str): Path to file
- `mode` (str): File open mode

**Returns:**
- `file object`: Opened file handle

#### `read_file(filename, mode="r")`
Reads entire file content with automatic cleanup.

**Parameters:**
- `filename` (str): Path to file
- `mode` (str): Read mode (default: "r")

**Returns:**
- `str/bytes`: File content

**Example:**
```python
content = read_file('/path/to/file.txt')
binary_data = read_file('/path/to/image.jpg', 'rb')
```

#### `write_file(filename, value, mode="w")`
Writes content to file with automatic cleanup.

**Parameters:**
- `filename` (str): Path to file
- `value` (str/bytes): Content to write
- `mode` (str): Write mode (default: "w")

**Returns:**
- `int`: Number of bytes written

#### `readlines_file(filename, mode="r")`
Reads file and splits into lines.

**Parameters:**
- `filename` (str): Path to file
- `mode` (str): Read mode

**Returns:**
- `list`: List of lines

### Directory Operations

#### `mktree(path)`
Creates directory tree recursively.

**Parameters:**
- `path` (str): Directory path to create

**Example:**
```python
mktree('/path/to/deep/directory/structure')
```

#### `listdir(path, expression="^.+$", drop=True, add_dirs=False, sort=True, maxnum=None, exclude_content_from=None, followlinks=False)`
Advanced directory listing with regex filtering.

**Parameters:**
- `path` (str): Directory path
- `expression` (str): Regex pattern for filtering (default: "^.+$")
- `drop` (bool): Remove path prefix (default: True)
- `add_dirs` (bool): Include directories (default: False)
- `sort` (bool): Sort results (default: True)
- `maxnum` (int): Maximum items to return
- `exclude_content_from` (list): Directories to exclude
- `followlinks` (bool): Follow symbolic links (default: False)

**Returns:**
- `list`: Filtered file/directory paths

**Example:**
```python
# List all Python files
python_files = listdir('/project', r'.*\.py$')

# List with full paths
all_files = listdir('/project', drop=False, add_dirs=True)
```

#### `recursive_unlink(f)`
Recursively deletes files and directories.

**Parameters:**
- `f` (str): Path to file or directory

**Example:**
```python
recursive_unlink('/tmp/old_project')
```

#### `cleanpath(path)`
Converts path into valid filename by replacing special characters.

**Parameters:**
- `path` (str): Path to clean

**Returns:**
- `str`: Cleaned filename

**Example:**
```python
safe_name = cleanpath("my/file:name?.txt")
# Returns: "my_file_name_.txt"
```

### Archive Operations

#### `tar(file, dir, expression="^.+$", filenames=None, exclude_content_from=None)`
Creates tar archive from directory.

**Parameters:**
- `file` (str): Output tar file path
- `dir` (str): Directory to archive
- `expression` (str): Regex filter for files
- `filenames` (list): Specific files to include
- `exclude_content_from` (list): Directories to exclude

#### `untar(file, dir)`
Extracts tar archive to directory.

**Parameters:**
- `file` (str): Tar file path
- `dir` (str): Extraction directory

#### `tar_compiled(file, dir, expression="^.+$", exclude_content_from=None)`
Creates tar archive excluding source files (for compiled apps).

**Parameters:**
- `file` (str): Output tar file
- `dir` (str): Directory to archive
- `expression` (str): File filter
- `exclude_content_from` (list): Excluded directories

### Web2py Specific Functions

#### `w2p_pack(filename, path, compiled=False, filenames=None)`
Packs a web2py application into .w2p format.

**Parameters:**
- `filename` (str): Output .w2p file path
- `path` (str): Application directory
- `compiled` (bool): Pack compiled version
- `filenames` (list): Specific files to include

**Example:**
```python
# Pack application
w2p_pack('myapp.w2p', 'applications/myapp')

# Pack compiled version
w2p_pack('myapp_compiled.w2p', 'applications/myapp', compiled=True)
```

#### `w2p_unpack(filename, path, delete_tar=True)`
Unpacks a .w2p file to specified path.

**Parameters:**
- `filename` (str): .w2p file path
- `path` (str): Extraction directory
- `delete_tar` (bool): Delete temporary tar file

#### `create_app(path)`
Creates new web2py application from welcome template.

**Parameters:**
- `path` (str): New application path

#### `w2p_pack_plugin(filename, path, plugin_name)`
Packs a web2py plugin.

**Parameters:**
- `filename` (str): Output plugin file
- `path` (str): Application path
- `plugin_name` (str): Plugin name

**Example:**
```python
w2p_pack_plugin('web2py.plugin.myplugin.w2p', 'applications/myapp', 'myplugin')
```

#### `w2p_unpack_plugin(filename, path, delete_tar=True)`
Unpacks a web2py plugin.

**Parameters:**
- `filename` (str): Plugin file path
- `path` (str): Application path
- `delete_tar` (bool): Delete temporary files

### Path and System Functions

#### `abspath(*relpath, **kwargs)`
Converts relative path to absolute path based on applications_parent.

**Parameters:**
- `*relpath`: Path components
- `**kwargs`: Options (gluon=True for gluon parent)

**Returns:**
- `str`: Absolute path

**Example:**
```python
# Get application path
app_path = abspath('applications', 'myapp')

# Get gluon module path
gluon_path = abspath('gluon', gluon=True)
```

#### `up(path)`
Returns parent directory of given path.

**Parameters:**
- `path` (str): Directory path

**Returns:**
- `str`: Parent directory path

### Session Management

#### `get_session(request, other_application="admin")`
Retrieves session from another application.

**Parameters:**
- `request`: Current request object
- `other_application` (str): Target application

**Returns:**
- `Storage`: Session data

#### `check_credentials(request, other_application="admin", expiration=3600, gae_login=True)`
Checks if user is authorized to access another application.

**Parameters:**
- `request`: Request object
- `other_application` (str): Target application
- `expiration` (int): Session expiration in seconds
- `gae_login` (bool): Use GAE login

**Returns:**
- `bool`: Authorization status

### Utility Functions

#### `fix_newlines(path)`
Normalizes line endings in Python and HTML files.

**Parameters:**
- `path` (str): Directory path

#### `create_missing_folders()`
Creates required web2py directories at startup.

#### `create_missing_app_folders(request)`
Creates required application directories.

**Parameters:**
- `request`: Request object with folder information

#### `add_path_first(path)`
Adds path to beginning of sys.path.

**Parameters:**
- `path` (str): Path to add

### Usage Examples

#### Application Management
```python
# Create new application
create_app(abspath('applications', 'mynewapp'))

# Pack existing application
w2p_pack('backup.w2p', abspath('applications', 'myapp'))

# Deploy application
w2p_unpack('production.w2p', abspath('applications', 'prod'))
```

#### File Processing
```python
# Process configuration files
def process_config_files(app_path):
    config_files = listdir(
        pjoin(app_path, 'models'),
        expression=r'.*\.json$'
    )
    
    for config_file in config_files:
        data = read_file(pjoin(app_path, 'models', config_file))
        # Process data
        processed = transform_config(data)
        write_file(
            pjoin(app_path, 'private', config_file),
            processed
        )
```

#### Backup System
```python
def backup_application(app_name):
    """Create timestamped backup of application"""
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"{app_name}_backup_{timestamp}.w2p"
    
    w2p_pack(
        pjoin('backups', backup_name),
        abspath('applications', app_name)
    )
    
    # Keep only last 10 backups
    backups = listdir('backups', r'%s_backup_.*\.w2p' % app_name)
    if len(backups) > 10:
        for old_backup in sorted(backups)[:-10]:
            os.unlink(pjoin('backups', old_backup))
```

#### Plugin Development
```python
def develop_plugin(plugin_name):
    """Setup plugin development environment"""
    plugin_files = [
        f'controllers/plugin_{plugin_name}.py',
        f'models/plugin_{plugin_name}.py',
        f'views/plugin_{plugin_name}/index.html',
        f'static/plugin_{plugin_name}/js/main.js',
        f'static/plugin_{plugin_name}/css/style.css'
    ]
    
    for filepath in plugin_files:
        full_path = abspath('applications', 'myapp', filepath)
        mktree(up(full_path))
        if not os.path.exists(full_path):
            write_file(full_path, f'# {plugin_name} plugin\n')
```

### Error Handling

```python
def safe_file_operation(operation, *args, **kwargs):
    """Wrapper for safe file operations"""
    try:
        return operation(*args, **kwargs)
    except IOError as e:
        logging.error(f"IO Error: {e}")
        return None
    except OSError as e:
        logging.error(f"OS Error: {e}")
        return None

# Usage
content = safe_file_operation(read_file, 'config.json')
```

### Best Practices

1. **Path Handling**: Always use `abspath()` for web2py paths
2. **Cleanup**: Use context managers or ensure file cleanup
3. **Encoding**: Specify encoding explicitly for text files
4. **Error Handling**: Wrap file operations in try-except blocks
5. **Permissions**: Check write permissions before operations

### Module Metadata

- **License**: LGPLv3
- **Part of**: web2py Web Framework
- **Thread Safety**: Yes (for read operations)
- **Platform**: Cross-platform with GAE support
- **Python**: 2.7+, 3.x compatible