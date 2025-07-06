# test_recfile.py

## Overview
Unit tests for the `gluon.recfile` module, which provides a recursive file handling system that automatically creates directory structures as needed.

## Imports
```python
import os
import shutil
import unittest
import uuid
from gluon import recfile
```

## Test Class: TestRecfile

### Description
Tests the recfile module's ability to handle file operations with automatic directory creation, supporting nested directory structures.

### Setup/Teardown

#### setUp()
Creates a temporary "tests" directory for test operations.

#### tearDown()
Removes the entire "tests" directory tree after each test.

### Test Methods

#### test_generation()
Comprehensive test of file creation, reading, and removal with various path configurations.

**Test Case 1: Full Path Specification**
```python
filename = os.path.join("tests", str(uuid.uuid4()) + ".test")
```
- Creates files with full path including directory
- Writes test content
- Reads and verifies content
- Checks file existence
- Removes file and verifies removal

**Test Case 2: Separate Path Parameter**
```python
filename = str(uuid.uuid4()) + ".test"
with recfile.open(filename, "w", path="tests") as g:
```
- Uses separate `path` parameter instead of full path
- Tests alternative API for specifying directories
- Same operations: write, read, verify, remove

**Test Case 3: Nested Directory Structure**
```python
filename = os.path.join("tests", str(uuid.uuid4()), str(uuid.uuid4()) + ".test")
```
- Creates files in non-existent nested directories
- Demonstrates automatic directory creation
- Tests deep path handling

**Key Features Tested:**
- Automatic directory creation for nested paths
- File writing and reading
- Existence checking with `recfile.exists()`
- File removal with `recfile.remove()`
- Both full path and path parameter APIs

#### test_existing()
Tests interaction with existing files and error handling.

**Test Flow:**
1. **Create Regular File**
   - Uses standard `open()` to create a file
   - Verifies recfile can detect its existence

2. **Open Existing File**
   - Opens with `recfile.open()` in read mode
   - Verifies file handle has expected attributes

3. **Remove and Verify**
   - Removes file using path parameter
   - Confirms file no longer exists

4. **Error Handling**
   - Tests IOError on removing non-existent file
   - Tests IOError on opening non-existent file for reading

## Key Functionality

### recfile.open()
- **Purpose**: Opens files with automatic directory creation
- **Modes**: Supports standard file modes ('r', 'w', etc.)
- **Path Options**:
  - Full path in filename
  - Separate path parameter
- **Auto-creation**: Creates missing directories in write mode

### recfile.exists()
- **Purpose**: Checks if a file exists
- **Parameters**:
  - `filename`: File name or full path
  - `path`: Optional directory path
- **Returns**: Boolean indicating existence

### recfile.remove()
- **Purpose**: Removes a file
- **Parameters**:
  - `filename`: File name or full path
  - `path`: Optional directory path
- **Error Handling**: Raises IOError if file doesn't exist

## Testing Patterns

### UUID Usage
- Uses `uuid.uuid4()` for unique filenames
- Prevents test interference
- Ensures clean test isolation

### Path Flexibility
Tests both approaches:
1. `recfile.open("path/to/file.txt", "w")`
2. `recfile.open("file.txt", "w", path="path/to")`

### Directory Creation
- Single-level: `tests/file.txt`
- Multi-level: `tests/uuid/uuid/file.txt`
- Automatic creation of missing directories

### Error Conditions
- Attempting to remove non-existent files
- Opening non-existent files for reading
- Proper exception raising

## Use Cases

### Recursive Directory Creation
Useful for:
- Log file management with date-based directories
- User upload organization
- Cache file structures
- Temporary file hierarchies

### Simplified File Operations
- No need to check/create directories manually
- Consistent API for file operations
- Path handling abstraction

## Notes
- The module name "recfile" likely stands for "recursive file"
- Simplifies file operations in Web2py applications
- Particularly useful for dynamic directory structures
- Provides safety through existence checking and error handling