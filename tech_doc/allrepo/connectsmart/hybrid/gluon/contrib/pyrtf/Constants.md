# PyRTF Constants Module

**File**: `gluon/contrib/pyrtf/Constants.py`  
**Type**: RTF Constants and Enumerations  
**Framework**: Web2py Gluon Framework

## Overview

This module defines constants, enumerations, and configuration values used throughout the PyRTF library for RTF document generation. It provides standardized values for document properties, formatting options, and language settings.

## Python Compatibility

### Version Detection
```python
import sys
PY2 = sys.version_info[0] == 2
```

Enables proper handling of Python 2/3 differences throughout the library.

## Document View Constants

### ViewKind Class
Controls the default view mode when opening RTF documents:

```python
class ViewKind:
    NONE           = 0
    PageLayout     = 1  # DEFAULT
    Outline        = 2
    MasterDocument = 3
    Normal         = 4
    OnlineLayout   = 5
```

**Usage**:
```python
# Set document view mode
doc.ViewKind = ViewKind.PageLayout  # Standard page layout view
```

### ViewScale Class
Controls the default zoom level of documents:

```python
class ViewScale:
    def IsValid(cls, value):
        return value is None or (0 < value < 101)
```

**Usage**:
```python
# Set document zoom to 75%
doc.ViewScale = 75
```

### ViewZoomKind Class
Controls the zoom behavior:

```python
class ViewZoomKind:
    NONE     = 0
    FullPage = 1
    BestFit  = 2
```

## Language Constants

### Languages Class
Provides language identifiers for international document support:

```python
class Languages:
    NoLanguage            = 1024
    Albanian              = 1052
    Arabic                = 1025
    Bahasa                = 1057
    BelgianDutch          = 2067
    BelgianFrench         = 2060
    BrazilianPortuguese   = 1046
    Bulgarian             = 1026
    Catalan               = 1027
    CroatoSerbianLatin    = 1050
    # ... many more languages
```

**Usage in Documents**:
```python
# Set document language
doc.DefaultLanguage = Languages.English

# Set text language
text = Text("Hello", language=Languages.English)
```

### Common Language Examples
```python
# Major languages
Languages.English = 1033
Languages.French = 1036
Languages.German = 1031
Languages.Spanish = 1034
Languages.Italian = 1040
Languages.Portuguese = 1046
Languages.Russian = 1049
Languages.Chinese = 1028
Languages.Japanese = 1041
```

## Integration Examples

### Document Creation with Constants
```python
from gluon.contrib import pyrtf

def create_localized_document(language_code=None):
    doc = pyrtf.Document()
    
    # Set view properties
    doc.ViewKind = pyrtf.ViewKind.PageLayout
    doc.ViewScale = 100
    doc.ViewZoomKind = pyrtf.ViewZoomKind.NONE
    
    # Set language if specified
    if language_code:
        doc.DefaultLanguage = language_code
    
    section = pyrtf.Section()
    doc.Sections.append(section)
    
    return doc
```

### Multi-Language Support
```python
def create_multilingual_document():
    from gluon.contrib import pyrtf
    
    doc = pyrtf.Document()
    section = pyrtf.Section()
    doc.Sections.append(section)
    
    # English paragraph
    en_para = pyrtf.Paragraph()
    en_text = pyrtf.Text("Hello World", language=pyrtf.Languages.English)
    en_para.append(en_text)
    section.append(en_para)
    
    # Spanish paragraph
    es_para = pyrtf.Paragraph()
    es_text = pyrtf.Text("Hola Mundo", language=pyrtf.Languages.Spanish)
    es_para.append(es_text)
    section.append(es_para)
    
    # French paragraph
    fr_para = pyrtf.Paragraph()
    fr_text = pyrtf.Text("Bonjour le Monde", language=pyrtf.Languages.French)
    fr_para.append(fr_text)
    section.append(fr_para)
    
    return pyrtf.dumps(doc)
```

### Web2py Localization Integration
```python
def generate_localized_report():
    from gluon.contrib import pyrtf
    
    # Get user's language preference
    user_lang = request.env.http_accept_language
    
    # Map to RTF language constants
    lang_map = {
        'en': pyrtf.Languages.English,
        'es': pyrtf.Languages.Spanish,
        'fr': pyrtf.Languages.French,
        'de': pyrtf.Languages.German,
        'it': pyrtf.Languages.Italian,
    }
    
    rtf_language = lang_map.get(user_lang[:2], pyrtf.Languages.English)
    
    # Create document with appropriate language
    doc = pyrtf.Document()
    doc.DefaultLanguage = rtf_language
    doc.ViewKind = pyrtf.ViewKind.PageLayout
    
    section = pyrtf.Section()
    doc.Sections.append(section)
    
    # Add localized content
    title = pyrtf.Paragraph()
    title_text = T("Report Title")  # Web2py translation
    title.append(pyrtf.Text(title_text, font_size=18, bold=True))
    section.append(title)
    
    return pyrtf.dumps(doc)
```

## Validation Functions

### Value Validation
Many constant classes include validation methods:

```python
# ViewKind validation
if pyrtf.ViewKind.IsValid(view_value):
    doc.ViewKind = view_value
else:
    doc.ViewKind = pyrtf.ViewKind.DEFAULT

# ViewScale validation
if pyrtf.ViewScale.IsValid(scale_value):
    doc.ViewScale = scale_value
else:
    doc.ViewScale = 100  # Default 100%

# ViewZoomKind validation
if pyrtf.ViewZoomKind.IsValid(zoom_value):
    doc.ViewZoomKind = zoom_value
else:
    doc.ViewZoomKind = pyrtf.ViewZoomKind.NONE
```

## Extended Language Support

### Regional Variants
```python
# English variants
Languages.EnglishUS = 1033
Languages.EnglishUK = 2057
Languages.EnglishAustralian = 3081
Languages.EnglishCanadian = 4105

# Spanish variants
Languages.SpanishSpain = 1034
Languages.SpanishMexico = 2058
Languages.SpanishArgentina = 11274

# French variants
Languages.FrenchFrance = 1036
Languages.FrenchCanadian = 3084
Languages.FrenchBelgian = 2060
```

### Usage with Regional Settings
```python
def create_region_specific_document(region='US'):
    from gluon.contrib import pyrtf
    
    # Select appropriate language variant
    if region == 'US':
        language = pyrtf.Languages.EnglishUS
    elif region == 'UK':
        language = pyrtf.Languages.EnglishUK
    elif region == 'CA':
        language = pyrtf.Languages.EnglishCanadian
    else:
        language = pyrtf.Languages.English
    
    doc = pyrtf.Document()
    doc.DefaultLanguage = language
    
    # Region-specific formatting could be added here
    
    return doc
```

## Best Practices

### Constant Usage
1. **Always validate**: Use validation methods when available
2. **Default values**: Provide sensible defaults for required constants
3. **Language support**: Set appropriate language for international documents
4. **View settings**: Configure view properties for optimal user experience

### Error Handling
```python
def safe_constant_assignment(doc, view_kind=None, language=None):
    # Safe ViewKind assignment
    if view_kind is not None and pyrtf.ViewKind.IsValid(view_kind):
        doc.ViewKind = view_kind
    else:
        doc.ViewKind = pyrtf.ViewKind.DEFAULT
    
    # Safe language assignment
    if language is not None:
        # Verify language exists in Languages class
        if hasattr(pyrtf.Languages, str(language)) or isinstance(language, int):
            doc.DefaultLanguage = language
        else:
            doc.DefaultLanguage = pyrtf.Languages.English
```

This module provides the foundational constants and enumerations needed for proper RTF document configuration, enabling precise control over document appearance, behavior, and localization settings.