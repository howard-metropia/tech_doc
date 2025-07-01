# Afrikaans Plural Rules Module

**File**: `gluon/contrib/plural_rules/af.py`  
**Language**: Afrikaans (af)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Afrikaans language support in Web2py applications. Afrikaans follows a simple binary pluralization system with two forms: singular and plural.

## Language Profile

### Basic Information
- **Language Family**: Indo-European → Germanic → West Germanic
- **ISO Code**: af
- **Native Name**: Afrikaans
- **Regions**: South Africa, Namibia
- **Speakers**: ~7 million native speakers

### Pluralization Pattern
Afrikaans uses a **binary pluralization system** (2 forms):
1. **Singular** (n = 1): een item
2. **Plural** (n ≠ 1): twee items

## Technical Implementation

### Configuration
```python
nplurals = 2  # Binary pluralization system
```

### Plural ID Calculation
```python
get_plural_id = lambda n: int(n != 1)
```

**Logic**:
- Returns `0` for singular (n = 1)
- Returns `1` for plural (n ≠ 1)

### Examples
- n=0 → plural_id=1 (geen items)
- n=1 → plural_id=0 (een item)
- n=2 → plural_id=1 (twee items)
- n=5 → plural_id=1 (vyf items)

## Afrikaans Grammar Rules

### Regular Plurals
Most nouns add **-e** or **-s**:
- hond → honde (dog → dogs)
- kat → katte (cat → cats)
- boek → boeke (book → books)

### Common Patterns
- Words ending in -f: Brief → briewe (letter → letters)
- Words ending in -s: huis → huise (house → houses)
- Irregular forms handled by plural_dict

### Construct Function
```python
construct_plural_form = lambda word, plural_id: word + 'e'
```
Basic implementation adds 'e' suffix for plurals.

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item', 'items')}}  # Uses Afrikaans rules
```

### Message Files
Language files in `applications/*/languages/af.py`:
```python
{
'item': 'item',
'items': 'items',
# Afrikaans translations
}
```

## Linguistic Context

### Historical Background
- Developed from Dutch colonial settlers
- Simplified grammar compared to Dutch
- Limited irregular plural forms

### Grammatical Features
- No grammatical gender
- Simplified case system
- Regular pluralization patterns

### Cultural Considerations
- Official language of South Africa
- Used in formal and informal contexts
- Growing digital presence

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 1  # "geen items"
assert get_plural_id(1) == 0  # "een item"
assert get_plural_id(2) == 1  # "twee items"
assert get_plural_id(10) == 1 # "tien items"
```

### Edge Cases
```python
assert get_plural_id(-1) == 1  # Negative numbers
assert get_plural_id(1.0) == 0 # Float equality
assert get_plural_id(1.1) == 1 # Non-integer
```

## Related Components

### Similar Languages
- **Dutch** (nl.py): More complex pluralization
- **English** (en.py): Same binary pattern
- **German** (de.py): Similar Germanic structure

### Dependencies
- **gluon.languages**: Translation framework
- **plural_rules.__init__**: Package initialization
- Language files in applications directory

This module enables proper Afrikaans pluralization in Web2py applications, supporting the grammatical conventions of this important South African language.