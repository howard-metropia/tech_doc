# Bulgarian Plural Rules Module

**File**: `gluon/contrib/plural_rules/bg.py`  
**Language**: Bulgarian (bg)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Bulgarian language support in Web2py applications. Bulgarian follows a simple binary pluralization system with two forms: singular and plural.

## Language Profile

### Basic Information
- **Language Family**: Indo-European → Slavic → South Slavic
- **ISO Code**: bg
- **Native Name**: български език (bǎlgarski ezik)
- **Regions**: Bulgaria, diaspora communities
- **Speakers**: ~7-8 million native speakers
- **Writing System**: Cyrillic script

### Pluralization Pattern
Bulgarian uses a **binary pluralization system** (2 forms):
1. **Singular** (n = 1): един предмет
2. **Plural** (n ≠ 1): два предмета

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
- n=0 → plural_id=1 (нула предмета)
- n=1 → plural_id=0 (един предмет)
- n=2 → plural_id=1 (два предмета)
- n=5 → plural_id=1 (пет предмета)

## Bulgarian Grammar Rules

### Noun Declension
Bulgarian has simplified Slavic declension:
- Most masculine nouns: add -и or -ове
- Most feminine nouns: add -и
- Most neuter nouns: add -а or -та

### Examples
- стол → столове (chair → chairs)
- жена → жени (woman → women)  
- дете → деца (child → children)

### Simplified Structure
Unlike other Slavic languages, Bulgarian:
- Lost case system
- Uses articles (определен член)
- Simpler plural formation

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item', 'items')}}  # Uses Bulgarian rules
```

### Message Files
Language files in `applications/*/languages/bg.py`:
```python
{
'item': 'предмет',
'items': 'предмета',
# Bulgarian translations in Cyrillic
}
```

## Character Encoding

### Cyrillic Support
- UTF-8 encoding required
- Proper font support needed
- Keyboard input considerations

### Template Integration
```html
<meta charset="utf-8">
<div lang="bg">
    {{=T.plural(count, messages)}}
</div>
```

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 1  # "нула предмета"
assert get_plural_id(1) == 0  # "един предмет"
assert get_plural_id(2) == 1  # "два предмета"
assert get_plural_id(10) == 1 # "десет предмета"
```

### Edge Cases
```python
assert get_plural_id(-1) == 1  # Negative numbers
assert get_plural_id(1.0) == 0 # Float equality
assert get_plural_id(1.1) == 1 # Non-integer
```

## Related Components

### Other Slavic Languages
- **Russian** (ru.py): Complex 3-form system
- **Polish** (pl.py): Complex pluralization
- **Czech** (cs.py): 3-form system

### Dependencies
- **gluon.languages**: Translation framework
- **Unicode**: Cyrillic text support
- Language files in applications directory

This module enables proper Bulgarian pluralization in Web2py applications, supporting the simplified plural system of modern Bulgarian while handling Cyrillic text encoding.