# Gluon Recfile Module Technical Documentation

## Module: `recfile.py`

### Overview
The `recfile` module provides utilities for generating hierarchical file and directory names for cache and session files in the Gluon web framework. It implements a deterministic hashing system that distributes files across multiple subdirectories to avoid filesystem performance issues with large numbers of files in a single directory.

### Table of Contents
1. [Purpose and Design](#purpose-and-design)
2. [Core Functions](#core-functions)
3. [Hashing Algorithm](#hashing-algorithm)
4. [File Operations](#file-operations)
5. [Usage Examples](#usage-examples)
6. [Performance Considerations](#performance-considerations)

### Purpose and Design

#### Problem Solved
Large web applications can generate thousands of cache and session files. Storing all these files in a single directory causes:
- Slow directory listings
- Poor filesystem performance
- Inode exhaustion on some filesystems
- Backup and maintenance difficulties

#### Solution Approach
The module distributes files across a hierarchical directory structure using a deterministic hash of the filename. This ensures:
- Balanced distribution across subdirectories
- Predictable file locations
- Efficient file system operations
- Scalability to millions of files

### Core Functions

#### `generate(filename, depth=2, base=512)`
Generates a hierarchical path for a given filename.

**Parameters:**
- `filename` (str): Original filename or path
- `depth` (int): Number of directory levels (default: 2)
- `base` (int): Base for hash calculation (default: 512)

**Returns:**
- `str`: Hierarchical path with subdirectories

**Algorithm:**
```python
def generate(filename, depth=2, base=512):
    if os.path.sep in filename:
        path, filename = os.path.split(filename)
    else:
        path = None
    
    # Calculate hash from filename
    dummyhash = (
        sum(ord(c) * 256 ** (i % 4) for i, c in enumerate(filename)) % base**depth
    )
    
    # Generate directory structure
    folders = []
    for level in range(depth - 1, -1, -1):
        code, dummyhash = divmod(dummyhash, base**level)
        folders.append("%03x" % code)
    folders.append(filename)
    
    if path:
        folders.insert(0, path)
    return os.path.join(*folders)
```

**Example:**
```python
# Original filename
filename = "session_abc123"

# Generated path (depth=2, base=512)
path = generate(filename)
# Returns: "1a7/0f2/session_abc123"
```

#### `exists(filename, path=None)`
Checks if a file exists in either original location or generated hierarchical path.

**Parameters:**
- `filename` (str): Filename to check
- `path` (str): Base directory path (optional)

**Returns:**
- `bool`: True if file exists in any location

**Logic:**
1. Check if file exists at original path
2. If not found, check hierarchical path
3. Return True if found in either location

#### `remove(filename, path=None)`
Removes a file from either original location or hierarchical path.

**Parameters:**
- `filename` (str): Filename to remove
- `path` (str): Base directory path (optional)

**Raises:**
- `IOError`: If file not found in any location

**Logic:**
1. Try to remove from original path
2. If not found, try hierarchical path
3. Raise IOError if not found in either

#### `open(filename, mode="r", path=None)`
Opens a file using hierarchical path structure with automatic directory creation.

**Parameters:**
- `filename` (str): Filename to open
- `mode` (str): File open mode (default: "r")
- `path` (str): Base directory path (optional)

**Returns:**
- `file object`: Opened file handle

**Features:**
- Automatic directory creation for write modes
- Fallback to original path for read modes
- Hierarchical path generation for new files

### Hashing Algorithm

#### Hash Calculation
The module uses a custom polynomial hash function:

```python
dummyhash = sum(ord(c) * 256 ** (i % 4) for i, c in enumerate(filename)) % base**depth
```

**Components:**
- **Character values**: `ord(c)` for each character
- **Position weighting**: `256 ** (i % 4)` creates 4-byte cycles
- **Modulo operation**: `% base**depth` ensures hash fits directory structure

#### Directory Structure Generation
```python
# For depth=2, base=512:
# Hash range: 0 to 512² - 1 (0 to 262,143)
# Directory levels: 2
# Subdirectories per level: 512 (000 to 1ff in hex)

# Example hash = 123,456
level_1 = 123456 // 512 = 241 = 0xf1
level_2 = 123456 % 512 = 0 = 0x000
# Result: "0f1/000/filename"
```

### File Operations

#### Reading Files
```python
def safe_read_file(filename, base_path="/var/cache"):
    """Read file with hierarchical path support"""
    full_path = os.path.join(base_path, filename)
    
    try:
        # Try hierarchical path first
        return recfile.open(full_path, "r").read()
    except IOError:
        # File not found
        return None
```

#### Writing Files
```python
def safe_write_file(filename, content, base_path="/var/cache"):
    """Write file with automatic directory creation"""
    full_path = os.path.join(base_path, filename)
    
    with recfile.open(full_path, "w") as f:
        f.write(content)
```

#### File Management
```python
def cleanup_old_files(base_path, max_age_days=30):
    """Clean up old files from hierarchical structure"""
    import time
    import os
    
    cutoff_time = time.time() - (max_age_days * 24 * 3600)
    
    for root, dirs, files in os.walk(base_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.getmtime(file_path) < cutoff_time:
                os.unlink(file_path)
        
        # Remove empty directories
        if not os.listdir(root):
            os.rmdir(root)
```

### Usage Examples

#### Session File Management
```python
# In web2py session handling
import gluon.recfile as recfile

class HierarchicalSessionStorage:
    def __init__(self, session_dir):
        self.session_dir = session_dir
    
    def save_session(self, session_id, session_data):
        """Save session with hierarchical storage"""
        filename = f"session_{session_id}"
        full_path = os.path.join(self.session_dir, filename)
        
        # Automatically creates subdirectories
        with recfile.open(full_path, "wb") as f:
            pickle.dump(session_data, f)
    
    def load_session(self, session_id):
        """Load session from hierarchical storage"""
        filename = f"session_{session_id}"
        full_path = os.path.join(self.session_dir, filename)
        
        try:
            with recfile.open(full_path, "rb") as f:
                return pickle.load(f)
        except IOError:
            return {}
    
    def delete_session(self, session_id):
        """Delete session file"""
        filename = f"session_{session_id}"
        full_path = os.path.join(self.session_dir, filename)
        
        try:
            recfile.remove(full_path)
        except IOError:
            pass  # Session already deleted

# Usage
storage = HierarchicalSessionStorage("/var/web2py/sessions")
storage.save_session("abc123", {"user_id": 456, "cart": []})
session_data = storage.load_session("abc123")
```

#### Cache Implementation
```python
import time
import pickle
import gluon.recfile as recfile

class HierarchicalCache:
    def __init__(self, cache_dir, default_ttl=3600):
        self.cache_dir = cache_dir
        self.default_ttl = default_ttl
    
    def _make_filename(self, key):
        """Generate cache filename from key"""
        # Replace invalid filename characters
        safe_key = key.replace('/', '_').replace('\\', '_')
        return f"cache_{safe_key}.pkl"
    
    def set(self, key, value, ttl=None):
        """Store value in cache"""
        ttl = ttl or self.default_ttl
        expires = time.time() + ttl
        
        cache_data = {
            'value': value,
            'expires': expires,
            'created': time.time()
        }
        
        filename = self._make_filename(key)
        full_path = os.path.join(self.cache_dir, filename)
        
        with recfile.open(full_path, "wb") as f:
            pickle.dump(cache_data, f)
    
    def get(self, key, default=None):
        """Retrieve value from cache"""
        filename = self._make_filename(key)
        full_path = os.path.join(self.cache_dir, filename)
        
        try:
            with recfile.open(full_path, "rb") as f:
                cache_data = pickle.load(f)
            
            # Check expiration
            if time.time() > cache_data['expires']:
                self.delete(key)
                return default
            
            return cache_data['value']
            
        except (IOError, KeyError, EOFError):
            return default
    
    def delete(self, key):
        """Delete cache entry"""
        filename = self._make_filename(key)
        full_path = os.path.join(self.cache_dir, filename)
        
        try:
            recfile.remove(full_path)
        except IOError:
            pass  # Already deleted
    
    def cleanup_expired(self):
        """Remove expired cache entries"""
        current_time = time.time()
        
        # Walk through all cache directories
        for root, dirs, files in os.walk(self.cache_dir):
            for filename in files:
                if filename.startswith('cache_') and filename.endswith('.pkl'):
                    file_path = os.path.join(root, filename)
                    
                    try:
                        with open(file_path, 'rb') as f:
                            cache_data = pickle.load(f)
                        
                        if current_time > cache_data['expires']:
                            os.unlink(file_path)
                            
                    except (IOError, KeyError, EOFError):
                        # Corrupted file - remove it
                        os.unlink(file_path)

# Usage
cache = HierarchicalCache("/var/web2py/cache")
cache.set("user:123:profile", {"name": "John", "email": "john@example.com"})
profile = cache.get("user:123:profile")
```

#### Batch File Operations
```python
def batch_process_files(base_path, file_pattern, processor_func):
    """Process multiple files in hierarchical structure"""
    import glob
    import os
    
    processed = 0
    errors = 0
    
    # Walk through hierarchical structure
    for root, dirs, files in os.walk(base_path):
        for filename in files:
            if fnmatch.fnmatch(filename, file_pattern):
                file_path = os.path.join(root, filename)
                
                try:
                    processor_func(file_path)
                    processed += 1
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    errors += 1
    
    return {'processed': processed, 'errors': errors}

def migrate_to_hierarchical(old_dir, new_dir):
    """Migrate flat file structure to hierarchical"""
    import shutil
    
    if not os.path.exists(old_dir):
        return
    
    migrated = 0
    
    for filename in os.listdir(old_dir):
        old_path = os.path.join(old_dir, filename)
        
        if os.path.isfile(old_path):
            # Generate new hierarchical path
            new_filename = recfile.generate(filename)
            new_path = os.path.join(new_dir, new_filename)
            
            # Create directory structure
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            
            # Move file
            shutil.move(old_path, new_path)
            migrated += 1
    
    print(f"Migrated {migrated} files to hierarchical structure")
```

### Performance Considerations

#### Directory Distribution
```python
def analyze_distribution(base_path, depth=2, base=512):
    """Analyze file distribution across directories"""
    distribution = {}
    total_files = 0
    
    for root, dirs, files in os.walk(base_path):
        level = root.replace(base_path, '').count(os.sep)
        
        if level == depth:  # Final level with files
            dir_key = os.path.relpath(root, base_path)
            distribution[dir_key] = len(files)
            total_files += len(files)
    
    # Calculate statistics
    if distribution:
        avg_files = total_files / len(distribution)
        max_files = max(distribution.values())
        min_files = min(distribution.values())
        
        print(f"Total files: {total_files}")
        print(f"Total directories: {len(distribution)}")
        print(f"Average files per directory: {avg_files:.2f}")
        print(f"Max files in directory: {max_files}")
        print(f"Min files in directory: {min_files}")
        
        # Find imbalanced directories
        threshold = avg_files * 2
        imbalanced = [d for d, count in distribution.items() if count > threshold]
        if imbalanced:
            print(f"Imbalanced directories (>{threshold:.0f} files): {imbalanced}")
    
    return distribution
```

#### Optimization Settings
```python
# For different file volumes, adjust parameters:

# Small volume (<10,000 files)
small_volume = {'depth': 1, 'base': 256}

# Medium volume (10,000 - 1,000,000 files)
medium_volume = {'depth': 2, 'base': 512}  # Default

# Large volume (>1,000,000 files)
large_volume = {'depth': 3, 'base': 256}

# Very large volume (>10,000,000 files)
very_large_volume = {'depth': 3, 'base': 512}

def configure_for_volume(expected_files):
    """Configure parameters based on expected file volume"""
    if expected_files < 10000:
        return {'depth': 1, 'base': 256}
    elif expected_files < 1000000:
        return {'depth': 2, 'base': 512}
    elif expected_files < 10000000:
        return {'depth': 3, 'base': 256}
    else:
        return {'depth': 3, 'base': 512}
```

### Best Practices

1. **Consistent Parameters**: Use the same depth and base values throughout application
2. **Directory Limits**: Keep files per directory under 10,000 for optimal performance
3. **Cleanup Strategy**: Implement regular cleanup of expired files
4. **Backup Considerations**: Account for hierarchical structure in backup scripts
5. **Monitoring**: Monitor directory distribution for imbalances
6. **Migration Planning**: Plan carefully when changing parameters

### Limitations

1. **Parameter Consistency**: Changing depth/base requires file migration
2. **Hash Collisions**: Different filenames may generate same path
3. **Directory Overhead**: Creates additional directory structure
4. **Backup Complexity**: More complex directory traversal needed

### Integration with Web2py

```python
# In web2py session storage
from gluon.recfile import generate, open as recfile_open

def session_filename(session_id):
    """Generate session filename with hierarchical path"""
    base_name = f"sess_{session_id}"
    return generate(base_name, depth=2, base=512)

# In web2py cache system
from gluon.recfile import generate as cache_path

def cache_filename(key):
    """Generate cache filename"""
    safe_key = key.replace('/', '_').replace(':', '_')
    return cache_path(f"cache_{safe_key}", depth=2)
```

### Module Metadata

- **License**: LGPLv3 (web2py framework)
- **Purpose**: Hierarchical file organization for scalability
- **Dependencies**: Standard library only
- **Thread Safety**: Yes (no shared state)
- **Platform**: Cross-platform
- **Python**: 2.7+, 3.x compatible