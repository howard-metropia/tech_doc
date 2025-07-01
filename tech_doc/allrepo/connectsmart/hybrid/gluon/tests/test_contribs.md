# test_contribs.py

## Overview
Unit test module for testing functionality in the Gluon contrib package, focusing on PDF generation and application configuration management.

## Imports
```python
import os
import unittest
from gluon._compat import to_bytes
from gluon.contrib import fpdf as fpdf
from gluon.contrib import pyfpdf as pyfpdf
from gluon.contrib.appconfig import AppConfig
from gluon.storage import Storage
```

## Test Setup/Teardown

### setUpModule()
Module-level setup function (currently empty).

### tearDownModule()
Cleans up test artifacts by removing `appconfig.json` if it exists.

## Test Class: TestContribs

### Description
Tests functionality of various contrib package components including PDF generation and application configuration.

### Test Methods

#### test_fpdf()
Tests basic PDF generation functionality and sanity checks.

**Test Logic:**
1. Verifies version consistency between fpdf and pyfpdf modules
2. Verifies class consistency between modules
3. Creates a simple PDF document with:
   - One page
   - No compression
   - Arial font at 14pt
   - "hello world" text
4. Validates the PDF output contains:
   - The FPDF version string
   - The sample message text

**Key Assertions:**
- Version match between fpdf and pyfpdf
- Class equivalence between modules
- PDF output contains version string
- PDF output contains written text

#### test_appconfig()
Tests application configuration loading and parsing from JSON files.

**Test Logic:**
1. Sets up a mock request context with application details
2. Creates a test JSON configuration file with:
   - Simple string values (config1, config2)
   - Nested object (config3 with key1, key2)
3. Tests configuration access methods:
   - Direct access via bracket notation
   - `.take()` method for value retrieval
   - Type casting functionality
   - Nested value access using dot notation

**Key Features Tested:**
- JSON configuration file loading
- Direct key access (`myappconfig["config1"]`)
- `.take()` method for value retrieval
- Nested key access (`config3.key1`)
- Type casting with `cast` parameter
- Preservation of parsed types (once parsed, types are fixed)

**Test Data:**
```json
{
    "config1": "abc",
    "config2": "bcd", 
    "config3": {
        "key1": 1,
        "key2": 2
    }
}
```

## Notes
- The test file demonstrates integration testing between multiple contrib modules
- PDF testing focuses on basic functionality without complex formatting
- AppConfig testing validates both simple and nested configuration access patterns
- Type casting behavior shows that once values are parsed, their types are preserved