# Russian Plural Rules Module

**File**: `gluon/contrib/plural_rules/ru.py`  
**Language**: Russian (ru)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Russian language support in Web2py applications. Russian follows a complex three-form pluralization system with distinct rules for different number ranges.

## Language Profile

### Basic Information
- **Language Family**: Indo-European → Slavic → East Slavic
- **ISO Code**: ru
- **Native Name**: русский язык (russkiy yazyk)
- **Regions**: Russia, Belarus, Kazakhstan, and former Soviet states
- **Speakers**: ~150 million native speakers
- **Writing System**: Cyrillic script

### Pluralization Pattern
Russian uses a **three-form pluralization system** (3 forms):
1. **Singular** (n = 1): один элемент
2. **Paucal** (n = 2,3,4): два элемента
3. **Plural** (n = 0, 5+): пять элементов

## Technical Implementation

### Configuration
```python
nplurals = 3  # Three-form pluralization system
```

### Plural ID Calculation
```python
get_plural_id = lambda n: (
    0 if n % 10 == 1 and n % 100 != 11 else      # Singular
    1 if n % 10 >= 2 and n % 10 <= 4 and        # Paucal
         (n % 100 < 10 or n % 100 >= 20) else
    2                                             # Plural
)
```

**Complex Logic**:
- Singular: ends in 1, but not 11
- Paucal: ends in 2, 3, 4, but not 12, 13, 14
- Plural: all other cases

### Examples
- n=1 → plural_id=0 (один элемент)
- n=2 → plural_id=1 (два элемента)
- n=5 → plural_id=2 (пять элементов)
- n=11 → plural_id=2 (одиннадцать элементов)
- n=21 → plural_id=0 (двадцать один элемент)
- n=22 → plural_id=1 (двадцать два элемента)

## Russian Grammar Rules

### Complex Case System
Russian has six cases affecting plural forms:
- **Nominative**: кто/что (who/what)
- **Genitive**: кого/чего (whose/of what)
- **Dative**: кому/чему (to whom/what)
- **Accusative**: кого/что (whom/what)
- **Instrumental**: кем/чем (with whom/what)
- **Prepositional**: о ком/чём (about whom/what)

### Number-Dependent Forms

**Singular form** (1, 21, 31...):
- 1 рубль (1 ruble)
- 21 рубль (21 ruble)

**Paucal form** (2-4, 22-24...):
- 2 рубля (2 rubles)
- 23 рубля (23 rubles)

**Plural form** (0, 5+, 11-14...):
- 5 рублей (5 rubles)
- 11 рублей (11 rubles)

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item_one', 'item_few', 'item_many')}}
```

### Message Files
Russian requires all three forms:
```python
{
'item_one': 'элемент',      # Singular (1, 21, 31...)
'item_few': 'элемента',     # Paucal (2-4, 22-24...)
'item_many': 'элементов',   # Plural (0, 5-20, 25-30...)
'ruble_one': 'рубль',
'ruble_few': 'рубля',
'ruble_many': 'рублей',
}
```

## Character Encoding

### Cyrillic Script
- **Russian alphabet**: А Б В Г Д Е Ё Ж З И Й К Л М Н О П Р С Т У Ф Х Ц Ч Ш Щ Ъ Ы Ь Э Ю Я
- **UTF-8 encoding** required for proper display

### Template Integration
```html
<meta charset="utf-8">
<div lang="ru">
    {{=T.plural(count, messages)}}
</div>
```

## Testing Examples

### Standard Cases
```python
assert get_plural_id(1) == 0   # "один элемент"
assert get_plural_id(2) == 1   # "два элемента"
assert get_plural_id(5) == 2   # "пять элементов"
```

### Complex Cases
```python
assert get_plural_id(11) == 2  # "одиннадцать элементов" (not singular)
assert get_plural_id(12) == 2  # "двенадцать элементов" (not paucal)
assert get_plural_id(21) == 0  # "двадцать один элемент" (singular)
assert get_plural_id(22) == 1  # "двадцать два элемента" (paucal)
assert get_plural_id(25) == 2  # "двадцать пять элементов" (plural)
```

## Cultural Context

### Historical Significance
- Major language of former Soviet Union
- Rich literary and cultural tradition
- Scientific and technical terminology

### Modern Usage
- Official language in multiple countries
- Important for business in Eastern Europe
- Significant online presence

## Related Components

### Other Complex Slavic Languages
- **Polish** (pl.py): Similar 3-form system but different rules
- **Czech** (cs.py): 3-form system with simpler logic
- **Ukrainian** (uk.py): Related East Slavic language

### Dependencies
- **gluon.languages**: Translation framework
- **Unicode**: Cyrillic character support
- Language files with all three forms

This module enables proper Russian pluralization in Web2py applications, handling one of the most complex pluralization systems while supporting the rich grammatical heritage of the Russian language.