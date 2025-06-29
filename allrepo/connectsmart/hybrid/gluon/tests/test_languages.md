# test_languages.py

## Overview
This file contains unit tests for the web2py internationalization (i18n) system. It tests language file handling, parallel read/write operations, dictionary operations, and multiprocessing support for language data.

## Purpose
- Tests language dictionary read/write operations
- Validates parallel access to language files
- Tests multiprocessing safety for language operations
- Ensures thread-safe language file handling
- Tests language data integrity and consistency

## Key Classes and Methods

### Global Functions

#### `read_write(args)`
Helper function for testing parallel read/write operations.

**Parameters:**
- `args` (tuple): (filename, iterations) for testing

**Functionality:**
- **Iterative Testing**: Performs multiple read/write cycles
- **Content Validation**: Ensures content integrity across operations
- **Error Detection**: Returns False if content validation fails
- **Stress Testing**: Tests system under repeated operations

### TestLanguagesParallel Class
Test suite for parallel language file operations.

#### Setup Methods

##### `setUp(self)`
Setup for parallel testing.

**Test Data Creation:**
```python
contents = dict()
for i in range(1000):
    contents["key%d" % i] = "value%d" % i
```

**Features:**
- **Large Dataset**: Creates 1000 key-value pairs
- **Temporary Files**: Uses temporary file for testing
- **Content Generation**: Systematic content generation
- **Cleanup Preparation**: Prepares for proper cleanup

## Dependencies
- `unittest` - Python testing framework
- `os` - Operating system interface
- `shutil` - High-level file operations
- `sys` - System-specific parameters
- `tempfile` - Temporary file creation
- `gluon.languages` - Language handling module
- `gluon._compat` - Cross-version compatibility
- `gluon.html` - HTML components (SPAN)
- `gluon.storage` - Storage utilities (Messages)

## Multiprocessing Support

### Platform Detection
```python
MP_WORKING = 0
try:
    import multiprocessing
    MP_WORKING = 1
    if sys.platform.startswith("win"):
        MP_WORKING = 0  # Windows multiprocessing issues
    if "datastore" in os.getenv("DB", ""):
        MP_WORKING = 0  # GAE compatibility
except ImportError:
    pass
```

**Platform Considerations:**
- **Windows**: Disabled due to multiprocessing issues
- **GAE**: Disabled on Google App Engine
- **Import Safety**: Graceful fallback when multiprocessing unavailable
- **Test Reliability**: Prevents random test failures

## Language System Features Tested

### File Operations
- **Read Operations**: `languages.read_dict(filename)`
- **Write Operations**: `languages.write_dict(filename, content)`
- **File Integrity**: Content consistency across operations
- **Concurrent Access**: Multiple processes accessing same files

### Data Integrity
- **Content Validation**: Ensures data remains unchanged
- **Dictionary Structure**: Proper key-value pair handling
- **Large Datasets**: Performance with substantial data
- **Error Detection**: Identifies corruption or loss

### Concurrent Operations
- **Parallel Reading**: Multiple processes reading simultaneously
- **Parallel Writing**: Multiple processes writing simultaneously
- **Race Condition Testing**: Ensures no data corruption
- **Lock Management**: Proper file locking mechanisms

## Usage Example
```python
from gluon import languages
from gluon.storage import Messages
from gluon.html import SPAN

# Language dictionary operations
lang_dict = {"hello": "Hello", "goodbye": "Goodbye"}
languages.write_dict("en.py", lang_dict)
content = languages.read_dict("en.py")

# Messages object for translations
messages = Messages()
messages.hello = "Hello World"
messages.goodbye = "Goodbye World"

# HTML with translations
content = SPAN(messages.hello, _class="greeting")

# Parallel testing
import multiprocessing
if multiprocessing_available:
    pool = multiprocessing.Pool(4)
    results = pool.map(read_write, [("test.py", 100)] * 4)
    pool.close()
    pool.join()
```

## Integration with web2py Framework

### Internationalization System
- **Translation Files**: Language-specific translation files
- **Message Objects**: Structured message handling
- **Template Integration**: Seamless template translation
- **Runtime Loading**: Dynamic language file loading

### Performance Optimization
- **Caching**: Language data caching for performance
- **Lazy Loading**: Load translations only when needed
- **Memory Management**: Efficient memory usage for large translations
- **File Watching**: Monitor translation file changes

### Concurrent Access
- **Multi-user**: Multiple users with different languages
- **Thread Safety**: Safe concurrent access to language data
- **Process Safety**: Multiple processes sharing language data
- **Lock-free Operations**: Efficient concurrent reading

### Development Support
- **Translation Extraction**: Extract translatable strings
- **Missing Translation Detection**: Identify untranslated strings
- **Translation Validation**: Validate translation completeness
- **Development Tools**: Tools for managing translations

## Test Coverage
- **File Operations**: Read and write operations
- **Concurrent Access**: Parallel file access testing
- **Data Integrity**: Content consistency validation
- **Platform Compatibility**: Cross-platform testing
- **Error Handling**: Proper error detection and handling
- **Performance**: Large dataset handling

## Expected Results
- **Data Consistency**: Language data should remain consistent
- **Concurrent Safety**: No corruption during parallel access
- **Performance**: Efficient handling of large translation sets
- **Platform Compatibility**: Consistent behavior across platforms
- **Error Resilience**: Graceful handling of file system errors

## Multiprocessing Considerations

### Known Issues
- **Python Bug**: http://bugs.python.org/issue10845
- **Windows Platform**: Multiprocessing reliability issues
- **GAE Compatibility**: Google App Engine limitations
- **Random Failures**: Test reliability concerns

### Workarounds
- **Platform Detection**: Automatic platform-specific handling
- **Graceful Degradation**: Fallback to single-process testing
- **Import Protection**: Safe multiprocessing import
- **Environment Detection**: Database-specific adjustments

## File Structure
```
gluon/tests/
├── test_languages.py    # This file
└── ... (other test files)
```

This test suite ensures web2py's internationalization system provides reliable, thread-safe, and efficient language handling for multi-user web applications with proper concurrent access support.