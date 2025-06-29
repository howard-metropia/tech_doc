# test_fileutils.py

## Overview
This file contains unit tests for the web2py file utility functions. It tests version parsing functionality for web2py version strings and newline fixing utilities, ensuring proper file handling and version management capabilities.

## Purpose
- Tests version string parsing for web2py releases
- Validates semantic versioning and legacy version format support
- Tests file newline normalization functionality
- Ensures proper datetime parsing from version strings
- Tests compatibility across different version formats

## Key Classes and Methods

### TestFileUtils Class
Test suite for file utility functions.

#### Test Methods

##### `test_parse_version(self)`
Tests version string parsing functionality for different web2py version formats.

**Legacy Version Format Testing:**
```python
rtn = parse_version("Version 1.99.0 (2011-09-19 08:23:26)")
# Expected: (1, 99, 0, "dev", datetime.datetime(2011, 9, 19, 8, 23, 26))
```

**Semantic Version Format Testing:**
```python
# Release Candidate
rtn = parse_version("Version 1.99.0-rc.1+timestamp.2011.09.19.08.23.26")
# Expected: (1, 99, 0, "rc.1", datetime.datetime(2011, 9, 19, 8, 23, 26))

# Stable Release
rtn = parse_version("Version 2.9.11-stable+timestamp.2014.09.15.18.31.17")
# Expected: (2, 9, 11, "stable", datetime.datetime(2014, 9, 15, 18, 31, 17))

# Beta Release
rtn = parse_version("Version 2.14.1-beta+timestamp.2016.03.21.22.35.26")
# Expected: (2, 14, 1, "beta", datetime.datetime(2016, 3, 21, 22, 35, 26))
```

**Version Tuple Structure:**
- **Major Version** (int): Major version number
- **Minor Version** (int): Minor version number  
- **Patch Version** (int): Patch version number
- **Release Type** (str): Version qualifier ("dev", "rc.1", "stable", "beta")
- **Build Timestamp** (datetime): Build date and time

##### `test_fix_newlines(self)`
Tests newline normalization functionality.

**File Processing:**
- **Directory Processing**: Tests processing entire directory structures
- **Newline Normalization**: Ensures consistent newline characters across files
- **Cross-platform Compatibility**: Handles different OS newline conventions

```python
fix_newlines(os.path.dirname(os.path.abspath(__file__)))
```

## Dependencies
- `unittest` - Python testing framework
- `datetime` - Date and time handling
- `os` - Operating system interface
- `gluon.fileutils` - File utility functions

## Functions Tested

### `parse_version(version_string)`
Parses web2py version strings into structured tuples.

**Supported Formats:**
- **Legacy**: `"Version X.Y.Z (YYYY-MM-DD HH:MM:SS)"`
- **Semantic**: `"Version X.Y.Z-qualifier+timestamp.YYYY.MM.DD.HH.MM.SS"`

**Return Value:**
- **Tuple**: `(major, minor, patch, qualifier, datetime_obj)`

**Version Qualifiers:**
- `"dev"` - Development/legacy versions
- `"stable"` - Stable release versions
- `"beta"` - Beta release versions
- `"rc.X"` - Release candidate versions

### `fix_newlines(path)`
Normalizes newline characters in files within specified directory.

**Functionality:**
- **File Scanning**: Recursively processes files in directory
- **Newline Detection**: Identifies different newline conventions
- **Normalization**: Converts to consistent newline format
- **Cross-platform**: Handles Windows, Unix, and Mac newlines

## Usage Example
```python
from gluon.fileutils import parse_version, fix_newlines
import datetime

# Parse version strings
legacy_version = parse_version("Version 2.18.5 (2019-03-12 10:30:00)")
semantic_version = parse_version("Version 2.20.4-stable+timestamp.2020.12.31.23.59.59")

print(f"Legacy: {legacy_version}")
# Output: (2, 18, 5, "dev", datetime.datetime(2019, 3, 12, 10, 30, 0))

print(f"Semantic: {semantic_version}")
# Output: (2, 20, 4, "stable", datetime.datetime(2020, 12, 31, 23, 59, 59))

# Fix newlines in directory
fix_newlines("/path/to/project")
```

## Integration with web2py Framework

### Version Management
- **Update Checking**: Used for checking web2py version updates
- **Compatibility**: Ensures compatibility across different web2py versions
- **Release Tracking**: Tracks release types and build timestamps
- **Migration Support**: Helps with version-specific migrations

### File Processing
- **Code Normalization**: Ensures consistent file formats
- **Cross-platform Development**: Handles different OS conventions
- **Build Processing**: Used in build and deployment processes
- **Template Processing**: Processes template files for consistency

### Development Tools
- **Version Display**: Used in admin interface for version information
- **Debugging**: Provides version context for debugging
- **Deployment**: Version validation during deployment
- **Documentation**: Version information in generated documentation

## Version Format Evolution

### Legacy Format (Pre-2.0)
```
Version 1.99.7 (2012-03-04 22:12:08)
```
- Simple timestamp in parentheses
- Always classified as "dev" type
- Used during early web2py development

### Semantic Format (2.0+)
```
Version 2.20.4-stable+timestamp.2020.12.31.23.59.59
```
- Follows semantic versioning principles
- Explicit release type qualifiers
- Structured timestamp format
- Better version comparison support

## Test Coverage
- **Version Parsing**: All supported version formats
- **Date/Time Parsing**: Timestamp extraction and conversion
- **Version Classification**: Release type identification
- **File Processing**: Newline normalization functionality
- **Error Handling**: Invalid version string handling
- **Cross-platform**: Different OS path handling

## Expected Results
- **Version Tuples**: Should correctly parse all version components
- **Datetime Objects**: Should create proper datetime objects from timestamps
- **Version Comparison**: Parsed versions should support proper comparison
- **File Processing**: Should process files without errors
- **Newline Consistency**: Should normalize newlines across platforms

## Version History Support
The test covers various web2py version formats across its development history:

- **2011**: Early development versions (1.99.0)
- **2014**: Stable release era (2.9.11)
- **2016**: Modern release cycle (2.14.1)

This ensures backward compatibility and proper version handling across the entire web2py ecosystem.

## File Structure
```
gluon/tests/
├── test_fileutils.py     # This file
└── ... (other test files)
```

This test suite ensures web2py's file utility functions provide reliable version management and file processing capabilities across different platforms and version formats.