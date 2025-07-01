# test_fileutils.py

## Overview
Unit test module for testing file utility functions in the Gluon framework, focusing on version parsing and newline normalization.

## Imports
```python
import datetime
import os
import unittest
from gluon.fileutils import fix_newlines, parse_version
```

## Test Class: TestFileUtils

### Description
Tests utility functions for file operations and version string parsing.

### Test Methods

#### test_parse_version()
Tests the `parse_version` function with various version string formats.

**Test Cases:**

1. **Legacy Format**
   - Input: `"Version 1.99.0 (2011-09-19 08:23:26)"`
   - Expected Output: `(1, 99, 0, "dev", datetime.datetime(2011, 9, 19, 8, 23, 26))`
   - Format: Traditional Web2py version format with parenthetical timestamp

2. **Semantic Version with Release Candidate**
   - Input: `"Version 1.99.0-rc.1+timestamp.2011.09.19.08.23.26"`
   - Expected Output: `(1, 99, 0, "rc.1", datetime.datetime(2011, 9, 19, 8, 23, 26))`
   - Format: Semantic versioning with pre-release identifier and metadata

3. **Semantic Version - Stable Release**
   - Input: `"Version 2.9.11-stable+timestamp.2014.09.15.18.31.17"`
   - Expected Output: `(2, 9, 11, "stable", datetime.datetime(2014, 9, 15, 18, 31, 17))`
   - Format: Stable release with semantic versioning

4. **Semantic Version - Beta Release**
   - Input: `"Version 2.14.1-beta+timestamp.2016.03.21.22.35.26"`
   - Expected Output: `(2, 14, 1, "beta", datetime.datetime(2016, 3, 21, 22, 35, 26))`
   - Format: Beta release with semantic versioning

**Return Format:**
The function returns a tuple containing:
- Major version number (int)
- Minor version number (int)
- Patch version number (int)
- Release type/tag (string)
- Build timestamp (datetime object)

#### test_fix_newlines()
Tests the `fix_newlines` function for normalizing line endings in files.

**Test Logic:**
- Calls `fix_newlines` on the directory containing the test file itself
- The function normalizes line endings in text files within the specified directory
- No explicit assertions (function is expected to complete without errors)

**Purpose:** 
Ensures the newline normalization function can process directories without raising exceptions.

## Version String Formats Supported

### Legacy Format
```
Version X.Y.Z (YYYY-MM-DD HH:MM:SS)
```

### Semantic Versioning Format
```
Version X.Y.Z-<prerelease>+timestamp.YYYY.MM.DD.HH.MM.SS
```

Where:
- `X.Y.Z`: Major.Minor.Patch version numbers
- `<prerelease>`: Optional pre-release identifier (rc.1, beta, stable, etc.)
- `timestamp`: Build metadata with timestamp

## Notes
- The `parse_version` function handles both legacy and semantic versioning formats
- Version parsing is crucial for Web2py's update and compatibility checking
- The `fix_newlines` function helps maintain consistent line endings across different operating systems
- Test coverage includes various version formats used throughout Web2py's history