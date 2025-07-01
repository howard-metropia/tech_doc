# English Plural Rules Module

**File**: `gluon/contrib/plural_rules/en.py`  
**Language**: English (en)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for English language support in Web2py applications. English follows a binary pluralization system with two forms: singular and plural, along with automatic plural form construction.

## Language Profile

### Basic Information
- **Language Family**: Indo-European → Germanic → West Germanic → Anglo-Frisian
- **ISO Code**: en
- **Native Name**: English
- **Regions**: Global (primary language in US, UK, Canada, Australia, New Zealand, etc.)
- **Speakers**: ~400 million native, ~1.5 billion total speakers
- **Writing System**: Latin script

### Pluralization Pattern
English uses a **binary pluralization system** (2 forms):
1. **Singular** (n = 1): one item
2. **Plural** (n ≠ 1): two items

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

### Automatic Plural Construction
```python
construct_plural_form = lambda word, plural_id: (
    word + 'es' if word[-1:] in ('s','x','o') or word[-2:] in ('sh','ch')
    else word + 's'
)
```

**Rules**:
- Add **-es** for words ending in: s, x, o, sh, ch
- Add **-s** for all other words

### Examples
- n=0 → plural_id=1 (zero items)
- n=1 → plural_id=0 (one item)
- n=2 → plural_id=1 (two items)
- n=5 → plural_id=1 (five items)

## English Grammar Rules

### Regular Plurals

**Standard -s ending**:
- cat → cats
- dog → dogs
- house → houses

**-es ending for special cases**:
- box → boxes (ends in 'x')
- dish → dishes (ends in 'sh')
- church → churches (ends in 'ch')
- glass → glasses (ends in 's')
- potato → potatoes (ends in 'o')

### Irregular Plurals (Not Handled by Construction)
Common irregular forms need dictionary entries:
- man → men
- woman → women
- child → children
- foot → feet
- tooth → teeth
- mouse → mice
- goose → geese

### Special Cases
**Unchanged plurals**:
- sheep → sheep
- deer → deer
- fish → fish

**Foreign plurals**:
- datum → data
- criterion → criteria
- phenomenon → phenomena

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item', 'items')}}  # Uses English rules
```

### Automatic Construction
```python
# These will be automatically constructed:
{{=T.plural(count, 'box')}}    # → "box"/"boxes"
{{=T.plural(count, 'dish')}}   # → "dish"/"dishes"
{{=T.plural(count, 'cat')}}    # → "cat"/"cats"
```

### Message Files
Language files in `applications/*/languages/en.py`:
```python
{
'item': 'item',
'items': 'items',
# Irregular plurals need explicit entries:
'man': 'man',
'men': 'men',
'child': 'child',
'children': 'children',
}
```

## Construction Testing

### Regular Patterns
```python
assert construct_plural_form('cat', 1) == 'cats'
assert construct_plural_form('dog', 1) == 'dogs'
assert construct_plural_form('book', 1) == 'books'
```

### Special Endings
```python
assert construct_plural_form('box', 1) == 'boxes'
assert construct_plural_form('dish', 1) == 'dishes'
assert construct_plural_form('church', 1) == 'churches'
assert construct_plural_form('glass', 1) == 'glasses'
assert construct_plural_form('potato', 1) == 'potatoes'
```

## Global English Variants

### American English
- Standard pluralization rules
- Some spelling differences (color/colour)
- Default implementation base

### British English
- Same pluralization rules
- Different vocabulary choices
- Spelling variants

### International English
- Simplified forms often preferred
- Technical and business contexts
- Global communication standard

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 1  # "zero items"
assert get_plural_id(1) == 0  # "one item"
assert get_plural_id(2) == 1  # "two items"
assert get_plural_id(10) == 1 # "ten items"
```

### Edge Cases
```python
assert get_plural_id(-1) == 1  # Negative numbers
assert get_plural_id(1.0) == 0 # Float equality
assert get_plural_id(1.1) == 1 # Non-integer
```

### Construction Edge Cases
```python
# Words already ending in 's'
assert construct_plural_form('glass', 1) == 'glasses'
assert construct_plural_form('boss', 1) == 'bosses'

# Words ending in 'o'
assert construct_plural_form('photo', 1) == 'photoes'  # Note: simplified rule
assert construct_plural_form('hero', 1) == 'heroes'
```

## Cultural and Technical Context

### Business Applications
- Standard language for international business
- Technical documentation
- User interface localization

### Educational Context
- Primary language for many educational platforms
- Clear and simple pluralization rules
- Good baseline for other language implementations

### Digital Communication
- Internet lingua franca
- Social media and messaging
- Software development standard

## Performance Characteristics

### Efficiency
- Simple binary decision
- Fast string operations
- Minimal memory overhead

### Reliability
- Well-tested patterns
- Predictable behavior
- Wide compatibility

## Related Components

### Base Language Reference
English often serves as the reference implementation for:
- **Simple binary systems**: Most Germanic languages
- **Construction patterns**: Template for other languages
- **Testing baseline**: Validation reference

### Similar Languages
- **German** (de.py): Related Germanic language
- **Dutch** (nl.py): Germanic family member
- **Afrikaans** (af.py): English-influenced Germanic

### Dependencies
- **gluon.languages**: Translation framework
- **String operations**: Construction functions
- Language files in applications directory

This module provides the foundation for English pluralization in Web2py applications, offering both the basic binary pluralization logic and automatic construction of regular plural forms.