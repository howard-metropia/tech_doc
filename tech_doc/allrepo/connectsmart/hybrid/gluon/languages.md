# Gluon Languages Module Technical Documentation

## Module: `languages.py`

### Overview
The `languages` module provides comprehensive internationalization (i18n) and localization (l10n) support for the Gluon web framework. It implements a sophisticated translation system with plural form handling, lazy translation objects, parameter substitution, and support for multiple languages with fallback mechanisms.

### Table of Contents
1. [Core Components](#core-components)
2. [Translation System](#translation-system)
3. [Lazy Translation](#lazy-translation)
4. [Plural Forms](#plural-forms)
5. [File Management](#file-management)
6. [Usage Examples](#usage-examples)
7. [Advanced Features](#advanced-features)

### Core Components

#### Dependencies
```python
import logging
import os
import pkgutil
import re
import sys
from threading import RLock
from pydal._compat import (PY2, copyreg, iteritems, iterkeys, maketrans, pjoin,
                           to_bytes, to_native, to_unicode, unicodeT)
from pydal.contrib.portalocker import LockedFile, read_locked
from yatl.sanitizer import xmlescape
from gluon.cfs import getcfs
from gluon.contrib.markmin.markmin2html import markmin_escape, render
from gluon.fileutils import listdir
from gluon.html import XML, xmlescape
```

#### Constants
```python
DEFAULT_LANGUAGE = "en"
DEFAULT_LANGUAGE_NAME = "English"
DEFAULT_NPLURALS = 1
DEFAULT_GET_PLURAL_ID = lambda n: 0
DEFAULT_CONSTRUCT_PLURAL_FORM = lambda word, plural_id: word
```

#### Regular Expressions
```python
# Pattern to find T(blah blah blah) expressions
PY_STRING_LITERAL_RE = r"(?<=[^\w]T\()(?P<name>...)"
PY_M_STRING_LITERAL_RE = r"(?<=[^\w]T\.M\()(?P<name>...)"

# Language and file patterns
regex_language = re.compile("([a-z]{2,3}(?:\-[a-z]{2})?(?:\-[a-z]{2})?)(?:[,;]|$)")
regex_langfile = re.compile("^[a-z]{2,3}(-[a-z]{2})?\.py$")
regex_plural = re.compile("%({.+?})")
```

### Translation System

#### `TranslatorFactory` Class
Main translation factory that handles language selection and translation operations.

**Constructor:**
```python
def __init__(self, langpath, http_accept_language):
    """
    Initialize translator factory
    
    Args:
        langpath: Path to language files directory
        http_accept_language: HTTP Accept-Language header value
    """
```

**Key Methods:**

##### `force(*languages)`
Selects specific language(s) for translation:
```python
T.force('fr')        # Force French
T.force('es', 'pt')  # Try Spanish, fallback to Portuguese
T.force(None)        # Disable translation
```

##### `__call__(message, symbols={}, language=None, lazy=None, ns=None)`
Main translation method:
```python
# Basic translation
translated = T("Hello World")

# With parameters
translated = T("Hello %(name)s", dict(name="John"))

# With symbols tuple
translated = T("Found %s items", (count,))
```

##### `M(message, symbols={}, language=None, lazy=None, filter=None, ftag=None, ns=None)`
Markmin translation for rich text:
```python
# Markmin translation
rich_text = T.M("**Bold** text with [link]")
```

### Lazy Translation

#### `lazyT` Class
Lazy translation object that defers translation until string conversion.

**Features:**
- Deferred translation execution
- String-like behavior
- Arithmetic operations support
- XML-safe output

**Example:**
```python
# Create lazy translation
lazy_msg = T("Hello World")

# Translation happens here
str_msg = str(lazy_msg)
```

### Plural Forms

#### Plural Rules System
```python
# Plural rule structure
(lang_code, nplurals, get_plural_id, construct_plural_form)

# Example for English:
("en", 2, lambda n: 0 if n == 1 else 1, lambda word, id: word + "s")
```

#### Plural Form Syntax
Advanced plural syntax in translation strings:

**Simple Forms:**
```python
# Basic plural
"%%{item(count)}"  # "item" or "items"

# Conditional display
"%%{?Found?count?items}"  # "Found" if count==1, "count" if count==0, "items" otherwise
```

**Complex Forms:**
```python
# Capitalization
"%%{!item(count)}"    # Capitalize first letter
"%%{!!item(count)}"   # Title Case
"%%{!!!item(count)}"  # UPPER CASE

# Conditional with zero handling
"%%{?one item?count?no items}"  # "one item", count, or "no items"
```

### File Management

#### Language File Structure
```python
# Language file format (e.g., en.py)
{
'!langcode!': 'en',
'!langname!': 'English',
'Hello World': 'Hello World',
'Welcome %(name)s': 'Welcome %(name)s',
}
```

#### Plural Dictionary Structure
```python
# Plural file format (e.g., plural-en.py)
{
'item': ['items'],           # item -> items
'child': ['children'],       # child -> children
'person': ['people'],        # person -> people
}
```

### Usage Examples

#### Basic Translation Setup
```python
# Initialize translator
T = TranslatorFactory('/path/to/languages', 'en-US,en;q=0.9')

# Basic usage
welcome_msg = T('Welcome to our site')

# With parameters
user_msg = T('Hello %(name)s!', dict(name=user.name))

# Force specific language
T.force('es')  # Switch to Spanish
spanish_msg = T('Welcome to our site')
```

#### Multi-language Support
```python
def setup_languages(request):
    """Setup language based on user preference or HTTP headers"""
    
    # Get user's preferred language
    user_lang = None
    if auth.user:
        user_lang = auth.user.language
    
    # Get from HTTP headers
    accept_lang = request.env.http_accept_language
    
    # Initialize translator
    T = TranslatorFactory(
        os.path.join(request.folder, 'languages'),
        accept_lang
    )
    
    # Set user preference
    if user_lang:
        T.force(user_lang)
    
    return T
```

#### Template Integration
```python
# In controller
def index():
    response.title = T('Home Page')
    return dict(
        welcome=T('Welcome %(name)s', dict(name=auth.user.first_name)),
        items_count=T('Found %(count)s items', dict(count=len(items)))
    )

# In view
{{=T('Search Results')}}
{{=T('%(count)s items found', dict(count=len(results)))}}
```

#### Plural Handling
```python
# Simple plural
item_count = T('Found %%{item(%(count)s)}', dict(count=items))
# "Found item" (count=1) or "Found items" (count!=1)

# Complex plural with conditional display
result_msg = T('%%{?No items?%(count)s?items} found', dict(count=count))
# "No items found" (count=0)
# "1 found" (count=1)  
# "5 items found" (count>1)
```

### Advanced Features

#### Markmin Support
```python
# Rich text translation
def format_help_text():
    return T.M('''
    **Welcome** to our application!
    
    Please read our [terms of service](%(tos_url)s) 
    and [privacy policy](%(privacy_url)s).
    ''', dict(
        tos_url=URL('default', 'terms'),
        privacy_url=URL('default', 'privacy')
    ))
```

#### Namespace Support
```python
# Use different language namespace
admin_T = T("Error occurred", ns="admin")
public_T = T("Error occurred", ns="public")
```

#### Language Discovery
```python
def get_available_languages():
    """Get list of available languages"""
    languages = T.get_possible_languages()
    
    result = []
    for lang_code in languages:
        info = T.get_possible_languages_info(lang_code)
        if info:
            result.append({
                'code': info[0],      # Language code
                'name': info[1],      # Language name
                'mtime': info[2]      # File modification time
            })
    
    return result
```

#### Translation File Management
```python
def update_translations(app_path):
    """Update translation files by scanning source code"""
    from gluon.languages import findT, update_all_languages
    
    # Update all language files
    update_all_languages(app_path)
    
    # Update specific language
    findT(app_path, 'es')  # Update Spanish translations
```

#### Custom Validators with Translation
```python
from gluon.validators import Validator

class IS_VALID_EMAIL_TRANSLATED(Validator):
    def __init__(self, error_message=None):
        self.error_message = error_message or T('Invalid email address')
    
    def __call__(self, value):
        import re
        if re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
            return (value, None)
        else:
            return (value, self.error_message)
```

### Performance Optimization

#### Translation Caching
```python
# Global language cache structure
global_language_cache = {
    'languages/en.py': (
        {"message": "translation", ...},  # Translation dict
        RLock()                           # Thread lock
    )
}

def clear_cache(filename):
    """Clear translation cache for specific file"""
    cache = global_language_cache.setdefault(filename, ({}, RLock()))
    lang_dict, lock = cache
    with lock:
        lang_dict.clear()
```

#### Lazy Loading
```python
def setup_lazy_translation():
    """Configure lazy translation for better performance"""
    T.lazy = True  # Enable lazy translation
    
    # Translations will be deferred until needed
    messages = [
        T('Message 1'),
        T('Message 2'),
        T('Message 3')
    ]
    
    # Translation happens only when converted to string
    output = str(messages[0])
```

### Error Handling

#### Safe Translation
```python
def safe_translate(message, symbols=None, default=None):
    """Translate with error handling"""
    try:
        if symbols:
            return T(message, symbols)
        else:
            return T(message)
    except Exception as e:
        logger.warning(f"Translation error: {e}")
        return default or message

# Usage
title = safe_translate('Page Title', default='Default Title')
```

#### Language File Validation
```python
def validate_language_file(lang_file):
    """Validate language file format"""
    try:
        with open(lang_file, 'r') as f:
            content = f.read()
        
        # Check syntax
        translations = eval(content)
        
        # Validate structure
        if not isinstance(translations, dict):
            return False, "Not a dictionary"
        
        # Check required keys
        required_keys = ['!langcode!', '!langname!']
        for key in required_keys:
            if key not in translations:
                return False, f"Missing key: {key}"
        
        return True, "Valid"
        
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    except Exception as e:
        return False, f"Error: {e}"
```

### Testing Translation

#### Unit Tests
```python
import unittest

class TestTranslation(unittest.TestCase):
    def setUp(self):
        self.T = TranslatorFactory('languages', 'en')
    
    def test_basic_translation(self):
        result = self.T('Hello')
        self.assertEqual(str(result), 'Hello')
    
    def test_parameter_substitution(self):
        result = self.T('Hello %(name)s', dict(name='World'))
        self.assertEqual(str(result), 'Hello World')
    
    def test_plural_forms(self):
        # Test singular
        result = self.T('%%{item(1)}')
        self.assertEqual(str(result), 'item')
        
        # Test plural
        result = self.T('%%{item(2)}')
        self.assertEqual(str(result), 'items')
    
    def test_lazy_translation(self):
        lazy_msg = self.T('Test message')
        self.assertIsInstance(lazy_msg, lazyT)
        self.assertEqual(str(lazy_msg), 'Test message')
```

### Migration and Maintenance

#### Updating Language Files
```python
def migrate_language_files():
    """Migrate language files to new format"""
    
    for lang_file in glob.glob('languages/*.py'):
        # Read current translations
        translations = read_dict(lang_file)
        
        # Add missing metadata
        if '!langcode!' not in translations:
            lang_code = os.path.basename(lang_file)[:-3]
            translations['!langcode!'] = lang_code
        
        if '!langname!' not in translations:
            translations['!langname!'] = lang_code.upper()
        
        # Write updated file
        write_dict(lang_file, translations)
```

### Best Practices

1. **Consistent Keys**: Use descriptive translation keys
2. **Parameter Names**: Use clear parameter names in templates
3. **Plural Support**: Always consider plural forms for counts
4. **Context**: Use comments (##) to provide translation context
5. **Testing**: Test translations with various parameter values
6. **Performance**: Use lazy translation for better performance
7. **Maintenance**: Regularly update translation files

### Security Considerations

1. **Input Validation**: Validate translation parameters
2. **XSS Protection**: Use XML-safe translation methods
3. **File Access**: Restrict access to language files
4. **Code Injection**: Validate language file content

### Module Metadata

- **License**: LGPLv3
- **Authors**: Massimo Di Pierro, Vladyslav Kozlovskyy (plural subsystem)
- **Thread Safety**: Yes (with RLock protection)
- **Dependencies**: Standard library, PyDAL, YATL
- **Python**: 2.7+, 3.x compatible