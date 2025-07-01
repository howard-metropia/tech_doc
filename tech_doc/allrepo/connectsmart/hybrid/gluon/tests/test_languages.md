# test_languages.py

## Overview
Comprehensive unit test suite for Web2py's internationalization (i18n) and localization (l10n) system, testing translation functionality, pluralization, dictionary management, and multiprocessing support.

## Imports
```python
import os
import shutil
import sys
import tempfile
import unittest
from gluon import languages
from gluon._compat import PY2, to_bytes, to_unicode
from gluon.html import SPAN
from gluon.storage import Messages
```

## Multiprocessing Setup
The module checks for multiprocessing availability with platform-specific exclusions:
- Disabled on Windows (due to Python bug)
- Disabled when running on Google App Engine
- Sets `MP_WORKING` flag for conditional test execution

## Helper Functions

### read_write(args)
Tests concurrent reading and writing of language dictionaries.
- Reads dictionary content
- Verifies content exists
- Writes content back to file
- Returns success status

## Test Classes

### TestLanguagesParallel
Tests concurrent access to language files using multiprocessing.

#### setUp()
- Creates temporary file with 1000 key-value pairs
- Initializes test dictionary

#### tearDown()
- Cleans up temporary files

#### test_reads_and_writes()
Tests parallel read/write operations:
- Creates pool of 10 processes
- Each process performs 10 read/write cycles
- Verifies all operations succeed
- Skipped if multiprocessing unavailable

#### test_reads_and_writes_no_mp()
Fallback test for environments without multiprocessing:
- Performs same operations sequentially
- Ensures functionality works without concurrency

### TestTranslations
Tests the core translation functionality with various patterns.

#### setUp()
- Locates language path for welcome app
- Sets default language to English

#### test_plain()
Comprehensive test of translation features:

**Basic Translation:**
- `T("Hello World")` → "Hello World"
- `T("Hello World## comment")` → "Hello World" (strips comments)
- `T.M("**Hello World**")` → "<strong>Hello World</strong>" (Markdown)

**Pluralization with Tuples:**
- `T("%s %%{shop}", 1)` → "1 shop"
- `T("%s %%{shop}", 2)` → "2 shops"
- `T("%%{quark(%s)}", 1)` → "quark"
- `T("%%{quark(%i)}", 2)` → "quarks"

**Capitalization Modifiers:**
- `!` prefix: First letter uppercase
- `!!` prefix: All first letters uppercase
- `!!!` prefix: All uppercase

**Conditional Patterns:**
- `?value?` - Shows value if count is 1
- `??value?` - Shows value if count is NOT 1
- Full pattern: `?one?many?zero`

**Array Index Patterns:**
- `[0]` suffix for accessing pluralization rules
- Combined with conditional patterns

**Dictionary-based Substitution:**
- Using `%(key)s` format with dictionaries
- Pluralization based on dictionary values
- Complex conditional patterns with dict keys

**Language Forcing:**
- `T.force("it")` switches to Italian
- Verifies translation: "Hello World" → "Salve Mondo"

### TestDummyApp
Tests language file generation from application code.

#### setUp()
Creates a minimal Web2py application structure:
```
dummy/
├── languages/
│   ├── en.py
│   └── pt.py
├── models/
│   └── db.py
├── controllers/
│   └── default.py
├── views/
│   └── default/
│       └── index.html
└── modules/
    └── test.py
```

Each file contains translatable strings:
- **modules/test.py**: `current.T('hello')`
- **models/db.py**: `T("world")`
- **controllers/default.py**: `T('%s %%{shop}', 2)`
- **views/default/index.html**: `{{=T('ahoy')}}`

#### test_update_all_languages()
Tests automatic extraction of translatable strings:
- Runs `update_all_languages()` on test app
- Verifies all strings extracted to language files
- Checks both English and Portuguese dictionaries

### TestMessages
Tests the Messages class for structured translations.

#### test_decode()
Tests message storage and retrieval:
- Creates Messages object with translator
- Updates with new messages
- Tests Unicode handling with special characters

### TestHTMLTag
Tests translation within HTML helpers.

#### test_decode()
Tests translation integration with HTML elements:
- Basic translation in SPAN element
- Language-specific translation (Russian)
- XML output with proper encoding
- Flatten method for plain text extraction

## Translation Syntax Features

### Pluralization Rules
```python
%%{word}        # Singular: word, Plural: words
%%{word(%s)}    # Based on substituted value
%%{word[0]}     # Using array index notation
```

### Conditional Patterns
```python
%%{?one?many}           # one if 1, many otherwise
%%{??many}              # many if NOT 1
%%{?one?many?zero}      # Full conditional
```

### Capitalization
```python
%%{!word}    # Word
%%{!!word}   # Word (each word capitalized)
%%{!!!word}  # WORD
```

### Combined Features
```python
%(key)s %%{?one?many(key)}  # Dictionary + conditional
%%{?one?[0]}               # Conditional + array
```

## Key Testing Patterns

### Concurrency Testing
- Multiprocessing support for language file access
- Platform-specific test skipping
- Fallback to sequential testing

### Translation Coverage
- Basic string translation
- Comment stripping
- Markdown support
- Complex pluralization rules
- Conditional formatting
- Dictionary substitution

### Application Integration
- Extraction from all file types (models, views, controllers, modules)
- Automatic language file updates
- Cross-module translation consistency

### Unicode Support
- UTF-8 encoding throughout
- Special character handling
- Language-specific characters (Russian example)

## Notes
- Tests cover both synchronous and asynchronous access patterns
- Comprehensive pluralization rule testing
- Real-world application structure simulation
- Platform compatibility considerations