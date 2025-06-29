# test_recfile.py

## Overview
This file contains unit tests for the web2py recfile module, which provides file operations for record files. It tests file creation, reading, writing, existence checking, and removal operations with support for nested directory structures and path management.

## Purpose
- Tests recfile module file operations
- Validates file creation and automatic directory creation
- Tests file existence checking and removal
- Verifies path parameter functionality
- Tests error handling for file operations
- Ensures proper cleanup and resource management

## Key Classes and Methods

### TestRecfile Class
Test suite for recfile module functionality.

#### Setup and Teardown Methods

##### `setUp(self)`
Creates test directory for file operations.
- Creates "tests" directory for test isolation
- Provides clean environment for each test

##### `tearDown(self)`
Cleans up test directory and files.
- Removes entire "tests" directory tree
- Ensures no test artifacts remain

#### Test Methods

##### `test_generation(self)`
Comprehensive test of recfile operations with various path configurations.

**Test Scenario 1: Full Path Specification**
```python
for k in range(10):
    teststring = "test%s" % k
    filename = os.path.join("tests", str(uuid.uuid4()) + ".test")
    
    # Write operation
    with recfile.open(filename, "w") as g:
        g.write(teststring)
    
    # Read operation
    with recfile.open(filename, "r") as f:
        self.assertEqual(f.read(), teststring)
    
    # Existence check
    is_there = recfile.exists(filename)
    self.assertTrue(is_there)
    
    # Removal
    recfile.remove(filename)
    is_there = recfile.exists(filename)
    self.assertFalse(is_there)
```

**Test Scenario 2: Path Parameter Usage**
```python
for k in range(10):
    teststring = "test%s" % k
    filename = str(uuid.uuid4()) + ".test"
    
    # Operations with path parameter
    with recfile.open(filename, "w", path="tests") as g:
        g.write(teststring)
    
    with recfile.open(filename, "r", path="tests") as f:
        self.assertEqual(f.read(), teststring)
    
    is_there = recfile.exists(filename, path="tests")
    self.assertTrue(is_there)
    
    recfile.remove(filename, path="tests")
    is_there = recfile.exists(filename, path="tests")
    self.assertFalse(is_there)
```

**Test Scenario 3: Nested Directory Creation**
```python
for k in range(10):
    teststring = "test%s" % k
    filename = os.path.join(
        "tests", str(uuid.uuid4()), str(uuid.uuid4()) + ".test"
    )
    
    # Automatic directory creation
    with recfile.open(filename, "w") as g:
        g.write(teststring)
    
    # Standard operations
    with recfile.open(filename, "r") as f:
        self.assertEqual(f.read(), teststring)
```

##### `test_existing(self)`
Tests operations on existing files and error handling.

**Existing File Operations:**
```python
filename = os.path.join("tests", str(uuid.uuid4()) + ".test")

# Create file with standard Python
with open(filename, "w") as g:
    g.write("this file exists")

# Test recfile operations on existing file
self.assertTrue(recfile.exists(filename))
r = recfile.open(filename, "r")
self.assertTrue(hasattr(r, "read"))
r.close()
```

**Error Handling Tests:**
```python
# Test removal and error conditions
recfile.remove(filename, path="tests")
self.assertFalse(recfile.exists(filename))

# Test error raising
self.assertRaises(IOError, recfile.remove, filename)
self.assertRaises(IOError, recfile.open, filename, "r")
```

## Dependencies
- `unittest` - Python testing framework
- `os` - Operating system interface
- `shutil` - High-level file operations
- `uuid` - UUID generation for unique filenames
- `gluon.recfile` - Record file operations module

## Recfile Module Features Tested

### File Operations
- **Creation**: `recfile.open(filename, "w")` for file creation
- **Reading**: `recfile.open(filename, "r")` for file reading
- **Writing**: Writing content to record files
- **Context Management**: Proper file handle management with `with` statements

### Directory Management
- **Auto-creation**: Automatic directory creation for nested paths
- **Path Parameters**: Separate path specification for organization
- **Full Paths**: Support for complete file path specification
- **Nested Structures**: Deep directory structure creation

### File System Operations
- **Existence Check**: `recfile.exists(filename)` for file verification
- **Removal**: `recfile.remove(filename)` for file deletion
- **Path Support**: Optional path parameter for all operations
- **Error Handling**: Proper IOError raising for invalid operations

### Resource Management
- **File Handles**: Proper file handle opening and closing
- **Context Managers**: Support for `with` statement usage
- **Memory Management**: Efficient file operation handling
- **Cleanup**: Proper resource cleanup after operations

## Usage Example
```python
from gluon import recfile
import uuid

# Basic file operations
filename = "data.txt"
content = "Hello, World!"

# Write file
with recfile.open(filename, "w", path="storage") as f:
    f.write(content)

# Read file
with recfile.open(filename, "r", path="storage") as f:
    data = f.read()

# Check existence
if recfile.exists(filename, path="storage"):
    print("File exists")

# Remove file
recfile.remove(filename, path="storage")

# Nested directory creation
nested_file = f"data/{uuid.uuid4()}/record.txt"
with recfile.open(nested_file, "w") as f:
    f.write("Nested file content")

# Cleanup
recfile.remove(nested_file)
```

## Integration with web2py Framework

### Application File Management
- **Application Files**: Managing application-specific files
- **Cache Storage**: File-based caching system support
- **Session Storage**: File-based session storage
- **Upload Handling**: File upload processing and storage

### Directory Organization
- **Application Structure**: Supports web2py application directory structure
- **Module Organization**: File organization for different modules
- **Data Storage**: Structured data file storage
- **Temporary Files**: Temporary file management

### Error Handling
- **Graceful Degradation**: Proper error handling for file operations
- **Resource Cleanup**: Automatic cleanup on errors
- **Exception Management**: Consistent exception handling
- **Debug Information**: Helpful error messages for development

### Performance Optimization
- **Efficient I/O**: Optimized file operations
- **Directory Caching**: Directory existence caching
- **Lazy Creation**: Create directories only when needed
- **Resource Pooling**: Efficient resource management

## Test Coverage
- **File Creation**: Various file creation scenarios
- **Directory Management**: Automatic directory creation
- **Path Handling**: Different path specification methods
- **Error Conditions**: Invalid operations and error handling
- **Resource Management**: Proper file handle management
- **Cleanup Operations**: File and directory removal

## Expected Results
- **File Operations**: All file operations should succeed
- **Directory Creation**: Directories should be created automatically
- **Content Integrity**: File content should be preserved accurately
- **Error Handling**: Invalid operations should raise appropriate exceptions
- **Resource Management**: No file handles should be leaked
- **Cleanup**: All files and directories should be removable

## File Structure
```
gluon/tests/
├── test_recfile.py       # This file
└── ... (other test files)

# Test directory structure created during tests
tests/
├── uuid1.test           # Direct files
├── uuid2/               # Nested directories
│   └── uuid3.test       # Nested files
└── ... (temporary test files)
```

This test suite ensures the web2py recfile module provides reliable file operations with automatic directory management, proper error handling, and efficient resource management for application file storage needs.