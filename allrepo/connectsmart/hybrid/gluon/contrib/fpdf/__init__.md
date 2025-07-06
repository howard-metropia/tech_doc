# gluon/contrib/fpdf/__init__.py

## Overview

The FPDF __init__ module serves as the main entry point for the FPDF PDF generation library within the Web2py framework. This module provides Python-based PDF creation capabilities, enabling dynamic document generation for web applications.

## Key Components

### Module Metadata
- **License**: LGPL 3.0
- **Version**: 1.7.2
- **Purpose**: PDF document generation for Python applications

### Imports
```python
from .fpdf import FPDF, FPDF_FONT_DIR, FPDF_VERSION, SYSTEM_TTFONTS, set_global, FPDF_CACHE_MODE, FPDF_CACHE_DIR
from .html import HTMLMixin  # Optional, requires web2py gluon
from .template import Template
```

### Export Configuration
The module exports the following core components:
- **FPDF**: Main PDF generation class
- **FPDF_FONT_DIR**: Directory containing font files
- **FPDF_VERSION**: Library version identifier
- **SYSTEM_TTFONTS**: System TrueType font configuration
- **set_global**: Function to set global configuration variables
- **FPDF_CACHE_MODE**: Cache mode configuration (0=same folder, 1=none, 2=hash)
- **FPDF_CACHE_DIR**: Cache directory path
- **Template**: Template-based PDF generation class

### Conditional Imports
The module includes graceful handling for optional components:
```python
try:
    from .html import HTMLMixin
except ImportError:
    import warnings
    warnings.warn("web2py gluon package not installed, required for html2pdf")
```

## Dependencies and Imports

### Internal Dependencies
- **fpdf.py**: Core PDF generation functionality
- **html.py**: HTML to PDF conversion capabilities (optional)
- **template.py**: Template-based PDF creation

### Error Handling
The module implements defensive import strategies to handle missing dependencies gracefully, particularly for the HTML functionality which requires the full web2py framework.

## Functionality and Public API

### Primary Functions
1. **PDF Creation**: Direct access to FPDF class for manual PDF construction
2. **HTML Conversion**: HTMLMixin for converting HTML to PDF (when available)
3. **Template Processing**: Template class for structured PDF generation

### Configuration Management
- **Global Variables**: Managed through set_global function
- **Font Management**: Access to font directory and system fonts
- **Caching**: Configurable cache modes for performance optimization

## Implementation Details

### Version Management
The module maintains version compatibility through:
- Explicit version declaration (1.7.2)
- Backward compatibility with earlier FPDF implementations

### Font System Integration
- Default font directory location
- System TrueType font support
- Cache management for font files

### Module Structure
```
fpdf/
├── __init__.py      # This module - entry point
├── fpdf.py          # Core PDF generation
├── fonts.py         # Font width definitions
├── html.py          # HTML to PDF converter
├── template.py      # Template processor
├── ttfonts.py       # TrueType font handler
├── php.py           # PHP compatibility functions
└── py3k.py          # Python 2/3 compatibility
```

## Error Handling and Validation

### Import Protection
- Try-except blocks for optional dependencies
- Warning messages for missing components
- Graceful degradation when web2py is not available

### Compatibility Warnings
The module provides clear feedback when optional features are unavailable:
- HTML to PDF functionality requires web2py
- Warning issued but core functionality remains available

## Performance Considerations

### Caching Strategy
- **Mode 0**: Cache in same folder as font files
- **Mode 1**: No caching
- **Mode 2**: Hash-based caching directory

### Memory Management
- Lazy loading of optional components
- Minimal initial import footprint

## Security Considerations

### License Compliance
- LGPL 3.0 licensed for open source compatibility
- Clear attribution and version tracking

### Import Safety
- Protected imports prevent runtime errors
- No execution of external code during import

## Integration with Web2py

### Framework Integration
When used within web2py:
- Full HTML to PDF capabilities available
- Integration with web2py's HTML helpers
- Template system compatibility

### Standalone Usage
Can be used independently of web2py:
- Core PDF generation fully functional
- Template-based creation available
- HTML features disabled with warning

## Usage Examples

### Basic PDF Creation
```python
from gluon.contrib.fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(40, 10, 'Hello World!')
pdf.output('example.pdf', 'F')
```

### Template Usage
```python
from gluon.contrib.fpdf import Template

template = Template(format='A4', orientation='portrait')
# Configure template elements
template.render()
```

### Configuration
```python
from gluon.contrib.fpdf import set_global, FPDF_CACHE_MODE

# Set cache mode
set_global('FPDF_CACHE_MODE', 2)  # Use hash-based caching
```

## Module Versioning

### Version History
- 1.7.2: Current stable version
- Compatible with Python 2.7+ and Python 3.x
- Based on PHP FPDF library port

### API Stability
- Stable public API
- Backward compatibility maintained
- Version checking through FPDF_VERSION constant