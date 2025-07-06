# UTF-8 Module

## Overview
The UTF-8 module provides comprehensive Unicode string handling capabilities for web2py applications. It includes the `Utf8` class that extends Python's str class with proper Unicode awareness, utility functions for UTF-8 operations, and Unicode Collation Algorithm support for proper international sorting. This module is essential for applications requiring robust multilingual text processing.

## Core Components

### Utf8 Class
Enhanced string class with full UTF-8 awareness and Unicode operations.

```python
class Utf8(str):
    """UTF-8 aware string class with Unicode operations"""
    
    def __new__(cls, content="", codepage="utf-8"):
        if isinstance(content, unicodeT):
            return str.__new__(cls, to_native(content, "utf-8"))
        elif codepage in ("utf-8", "utf8") or isinstance(content, cls):
            return str.__new__(cls, content)
        else:
            return str.__new__(cls, to_native(to_unicode(content, codepage), "utf-8"))
```

**Key Features:**
- Automatic encoding/decoding
- Unicode-aware string operations
- Proper length calculation
- International sorting support
- Custom representation

### Utility Functions

#### Character Operations
```python
def ord(char):
    """Returns unicode ID for UTF-8 or unicode character"""
    if isinstance(char, unicodeT):
        return __builtin__.ord(char)
    return __builtin__.ord(to_unicode(char, "utf-8"))

def chr(code):
    """Returns UTF-8 character with unicode ID"""
    return Utf8(unichr(code))
```

#### String Measurements
```python
def size(string):
    """Returns length of UTF-8 string in bytes"""
    return Utf8(string).__size__()

def truncate(string, length, dots="..."):
    """Truncate string to specified character length"""
    text = to_unicode(string, "utf-8")
    dots = to_unicode(dots, "utf-8")
    if len(text) > length:
        text = text[:length - len(dots)] + dots
    return str.__new__(Utf8, text.encode("utf-8"))
```

#### Sorting Support
```python
def sort_key(s):
    """Unicode Collation Algorithm sort key"""
    # Lazy import of pyuca for memory efficiency
    try:
        from gluon.contrib.pyuca import unicode_collator
        unicode_sort_key = unicode_collator.sort_key
        sort_key = lambda s: unicode_sort_key(
            to_unicode(s, "utf-8") if isinstance(s, str) else s
        )
    except:
        # Fallback to simple lowercase sorting
        sort_key = lambda s: (
            to_unicode(s, "utf-8") if isinstance(s, str) else s
        ).lower()
    return sort_key(s)
```

## Utf8 Class Methods

### String Operations
```python
# Case operations
def upper(self):
    return str.__new__(Utf8, unicode(self, "utf-8").upper().encode("utf-8"))

def lower(self):
    return str.__new__(Utf8, unicode(self, "utf-8").lower().encode("utf-8"))

def capitalize(self):
    return str.__new__(Utf8, unicode(self, "utf-8").capitalize().encode("utf-8"))

def title(self):
    return str.__new__(Utf8, unicode(self, "utf-8").title().encode("utf-8"))

def swapcase(self):
    return str.__new__(Utf8, unicode(self, "utf-8").swapcase().encode("utf-8"))
```

### Length and Indexing
```python
def __len__(self):
    """Character length (not byte length)"""
    return len(to_unicode(self, "utf-8"))

def __size__(self):
    """Byte length"""
    return str.__len__(self)

def __getitem__(self, index):
    """Character-based indexing"""
    return str.__new__(Utf8, to_native(to_unicode(self, "utf-8")[index], "utf-8"))

def __getslice__(self, begin, end):
    """Character-based slicing"""
    return str.__new__(Utf8, to_native(to_unicode(self, "utf-8")[begin:end], "utf-8"))
```

### Search and Replace
```python
def find(self, sub, start=None, end=None):
    """Character-based find"""
    return unicode(self, "utf-8").find(
        unicode(sub, "utf-8") if isinstance(sub, str) else sub, start, end
    )

def replace(self, old, new, count=-1):
    """Character-aware replace"""
    return str.__new__(Utf8, str.replace(self, Utf8(old), Utf8(new), count))

def count(self, sub, start=0, end=None):
    """Character-based count"""
    unistr = unicode(self, "utf-8")
    return unistr.count(
        unicode(sub, "utf-8") if isinstance(sub, str) else sub,
        start,
        len(unistr) if end is None else end
    )
```

### Formatting and Alignment
```python
def center(self, length):
    """Character-based centering"""
    return str.__new__(Utf8, unicode(self, "utf-8").center(length).encode("utf-8"))

def ljust(self, width, fillchar=" "):
    """Left justify with proper character width"""
    return str.__new__(Utf8,
        unicode(self, "utf-8").ljust(
            width,
            unicode(fillchar, "utf-8") if isinstance(fillchar, str) else fillchar
        ).encode("utf-8")
    )

def zfill(self, length):
    """Zero-fill with character-based length"""
    return str.__new__(Utf8, unicode(self, "utf-8").zfill(length).encode("utf-8"))
```

## Comparison and Sorting

### Unicode Collation
```python
def __ge__(self, string):
    return sort_key(self) >= sort_key(string)

def __gt__(self, string):
    return sort_key(self) > sort_key(string)

def __le__(self, string):
    return sort_key(self) <= sort_key(string)

def __lt__(self, string):
    return sort_key(self) < sort_key(string)
```

**Example Usage:**
```python
# Proper international sorting
ukrainian_text = [
    Utf8("яблуко"),    # apple
    Utf8("Київ"),      # Kyiv
    Utf8("білінг"),    # billing
    Utf8("Астро")      # Astro
]

# Correct Unicode order
sorted_text = sorted(ukrainian_text)
# Result: ['Астро', 'білінг', 'Київ', 'яблуко']
```

## Advanced Features

### Custom Representation
```python
def __repr__(self):
    """Unicode-aware string representation"""
    if str.find(self, "'") >= 0 and str.find(self, '"') < 0:
        # Use double quotes if single quotes present
        return '"' + to_native(
            to_unicode(self, "utf-8").translate(repr_escape_tab), "utf-8"
        ) + '"'
    else:
        # Use single quotes otherwise
        return "'" + to_native(
            to_unicode(self, "utf-8").translate(repr_escape_tab2), "utf-8"
        ) + "'"
```

### String Formatting
```python
def __mod__(self, right):
    """Unicode-aware % formatting"""
    if isinstance(right, tuple):
        right = tuple(
            unicode(v, "utf-8") if isinstance(v, str) else v for v in right
        )
    elif isinstance(right, dict):
        right = dict(
            (unicode(k, "utf-8") if isinstance(k, str) else k,
             unicode(v, "utf-8") if isinstance(v, str) else v)
            for k, v in iteritems(right)
        )
    elif isinstance(right, str):
        right = unicode(right, "utf-8")
    return str.__new__(Utf8, unicode(self, "utf-8").__mod__(right).encode("utf-8"))

# If available in Python 2.6+
def format(self, *args, **kwargs):
    """Unicode-aware .format() method"""
    args = [unicode(s, "utf-8") if isinstance(s, str) else s for s in args]
    kwargs = dict(
        (unicode(k, "utf-8") if isinstance(k, str) else k,
         unicode(v, "utf-8") if isinstance(v, str) else v)
        for k, v in iteritems(kwargs)
    )
    return str.__new__(Utf8, unicode(self, "utf-8").format(*args, **kwargs).encode("utf-8"))
```

## Usage Examples

### Basic Text Processing
```python
# Create UTF-8 string
text = Utf8("Привіт, світ!")  # "Hello, world!" in Ukrainian

# Character-based operations
print(len(text))        # 13 characters (not bytes)
print(text.__size__())  # 25 bytes
print(text.upper())     # "ПРИВІТ, СВІТ!"
print(text[0])          # "П" (first character)
print(text[:6])         # "Привіт" (first 6 characters)
```

### International Sorting
```python
# Mixed language text
names = [
    Utf8("Müller"),
    Utf8("Москва"),     # Moscow
    Utf8("北京"),        # Beijing
    Utf8("André")
]

# Proper Unicode sorting
sorted_names = sorted(names, key=sort_key)
```

### Text Formatting
```python
# Unicode-aware formatting
template = Utf8("Привіт, %(name)s! Сьогодні %(date)s")
result = template % {
    'name': Utf8("Марія"),
    'date': Utf8("понеділок")
}

# Modern format method
if hasattr(Utf8, 'format'):
    template2 = Utf8("Користувач: {user}, Email: {email}")
    result2 = template2.format(
        user=Utf8("Олександр"),
        email="alex@example.com"
    )
```

### Character Analysis
```python
text = Utf8("Тест123")

# Unicode-aware character tests
print(text.isalnum())    # True (handles Cyrillic)
print(text[:4].isalpha()) # True (Cyrillic letters)
print(text[4:].isdigit()) # True (digits)
```

### String Manipulation
```python
data = Utf8("  Текст з пробілами  ")

# Unicode-aware trimming
trimmed = data.strip()

# Character-based truncation
short = truncate(data, 10, "...")

# Case conversion
upper = data.upper()
title = data.title()
```

## Performance Considerations

### Memory Efficiency
```python
# For intensive operations, convert to unicode
def process_text_efficiently(utf8_text):
    # Convert once
    unicode_text = utf8_text.decode('utf-8')
    
    # Perform operations on unicode
    result = unicode_text.upper().replace('old', 'new')
    
    # Convert back once
    return Utf8(result)
```

### Sorting Optimization
```python
# Cache sort keys for large datasets
def cached_sort(strings):
    # Pre-compute sort keys
    keyed_strings = [(sort_key(s), s) for s in strings]
    
    # Sort by pre-computed keys
    keyed_strings.sort(key=lambda x: x[0])
    
    # Return sorted strings
    return [s for key, s in keyed_strings]
```

## Common Patterns

### Input Validation
```python
def validate_utf8_input(text):
    """Validate and normalize UTF-8 input"""
    if not isinstance(text, Utf8):
        text = Utf8(text)
    
    # Normalize and validate
    if len(text) == 0:
        raise ValueError("Empty input")
    
    if len(text) > 1000:
        text = truncate(text, 1000)
    
    return text
```

### Database Storage
```python
def store_multilingual_text(text):
    """Store UTF-8 text in database"""
    # Ensure proper UTF-8 encoding
    utf8_text = Utf8(text)
    
    # Store byte length for database
    byte_length = utf8_text.__size__()
    char_length = len(utf8_text)
    
    db.texts.insert(
        content=str(utf8_text),  # Store as string
        byte_length=byte_length,
        char_length=char_length
    )
```

### Search and Indexing
```python
def create_search_index(texts):
    """Create search index for UTF-8 texts"""
    index = {}
    
    for text in texts:
        utf8_text = Utf8(text)
        # Normalize for searching
        normalized = utf8_text.lower()
        
        # Split into words
        words = normalized.split()
        
        for word in words:
            if word not in index:
                index[word] = []
            index[word].append(text)
    
    return index
```

## Integration with Web2py

### Form Processing
```python
def process_multilingual_form():
    """Handle UTF-8 form input"""
    if form.process().accepted:
        # Ensure UTF-8 handling
        title = Utf8(form.vars.title)
        content = Utf8(form.vars.content)
        
        # Validate lengths
        if len(title) > 100:
            form.errors.title = "Title too long"
        
        if len(content) > 5000:
            form.errors.content = "Content too long"
```

### Template Rendering
```python
def render_multilingual_content():
    """Render UTF-8 content in templates"""
    posts = db(db.posts).select()
    
    for post in posts:
        # Ensure UTF-8 handling
        post.title = Utf8(post.title)
        post.content = Utf8(post.content)
        
        # Safe truncation for summaries
        post.summary = truncate(post.content, 200)
    
    return dict(posts=posts)
```

## Best Practices

### Development Guidelines
1. Always use Utf8 class for international text
2. Validate input lengths using character count
3. Use Unicode-aware operations for text processing
4. Consider performance implications of Unicode operations
5. Test with various character sets

### Error Handling
```python
def safe_utf8_operation(text):
    """Safely handle UTF-8 operations"""
    try:
        return Utf8(text).upper()
    except UnicodeDecodeError:
        # Handle encoding errors
        return Utf8(text, codepage='latin1')
    except Exception as e:
        # Log error and return safe default
        logger.error("UTF-8 processing error: %s", e)
        return Utf8("")
```

### Testing
```python
def test_utf8_functionality():
    """Test UTF-8 string operations"""
    # Test various scripts
    test_cases = [
        ("Hello", "ascii"),
        ("Привіт", "cyrillic"), 
        ("こんにちは", "japanese"),
        ("مرحبا", "arabic")
    ]
    
    for text, script in test_cases:
        utf8_text = Utf8(text)
        assert len(utf8_text) > 0
        assert utf8_text.upper().lower() == utf8_text.lower()
```

## See Also
- Unicode standard documentation
- Python Unicode HOWTO
- Web2py internationalization guide
- PyUCA (Python Unicode Collation Algorithm)