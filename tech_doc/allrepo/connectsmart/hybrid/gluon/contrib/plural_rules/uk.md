# Ukrainian Plural Rules Module

**File**: `gluon/contrib/plural_rules/uk.py`  
**Language**: Ukrainian (uk)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Ukrainian language support in Web2py applications. Ukrainian follows a binary pluralization system with two forms: singular and plural.

## Language Profile

### Basic Information
- **Language Family**: Indo-European → Slavic → East Slavic
- **ISO Code**: uk
- **Native Name**: українська мова (ukraińśka mova)
- **Regions**: Ukraine, diaspora communities
- **Speakers**: ~40 million native speakers
- **Writing System**: Cyrillic script (Ukrainian variant)

### Pluralization Pattern
Ukrainian uses a **binary pluralization system** (2 forms):
1. **Singular** (n = 1): один елемент
2. **Plural** (n ≠ 1): два елементи

## Technical Implementation

### Configuration
```python
nplurals = 2  # Binary pluralization system
```

### Plural ID Calculation
```python
get_plural_id = lambda n: int(n != 1)
```

## Ukrainian Grammar Rules

### Simplified Plural System
Unlike Russian, Ukrainian uses simplified binary pluralization:
- книга → книги (book → books)
- стіл → столи (table → tables)
- дім → доми (house → houses)

### Case System
Ukrainian maintains a complex case system:
- **Nominative**: хто/що (who/what)
- **Genitive**: кого/чого (whose/of what)
- **Dative**: кому/чому (to whom/what)
- **Accusative**: кого/що (whom/what)
- **Instrumental**: ким/чим (with whom/what)
- **Locative**: де/на чому (where/on what)
- **Vocative**: addressing directly

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item', 'items')}}  # Uses Ukrainian rules
```

### Message Files
```python
{
'item': 'елемент',
'items': 'елементи',
'book': 'книга',
'books': 'книги',
}
```

## Character Encoding

### Ukrainian Cyrillic
- **Unique letters**: ґ, є, і, ї (not in Russian)
- **Missing letters**: ё, ъ, ы, э (present in Russian)
- **UTF-8 encoding** required

### Template Integration
```html
<meta charset="utf-8">
<div lang="uk">
    {{=T.plural(count, messages)}}
</div>
```

## Cultural Context

### National Language
- Official language of Ukraine
- Distinct from Russian despite similarities
- Important for cultural identity

### Modern Usage
- Growing digital presence
- Educational and government applications
- Literature and media

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 1  # "нуль елементів"
assert get_plural_id(1) == 0  # "один елемент"
assert get_plural_id(2) == 1  # "два елементи"
assert get_plural_id(10) == 1 # "десять елементів"
```

## Related Components

### East Slavic Languages
- **Russian** (ru.py): Related but more complex 3-form system
- **Belarusian**: Similar East Slavic patterns

### Dependencies
- **gluon.languages**: Translation framework
- **Unicode**: Ukrainian Cyrillic support
- Language files in applications directory

This module enables proper Ukrainian pluralization in Web2py applications, supporting this important East Slavic language with its distinctive characteristics and simplified plural system compared to Russian.