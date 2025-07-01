# Japanese Plural Rules Module

**File**: `gluon/contrib/plural_rules/ja.py`  
**Language**: Japanese (ja)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Japanese language support in Web2py applications. Japanese follows a **single-form system** with no grammatical distinction between singular and plural.

## Language Profile

### Basic Information
- **Language Family**: Japonic
- **ISO Code**: ja
- **Native Name**: 日本語 (nihongo)
- **Regions**: Japan, diaspora communities
- **Speakers**: ~125 million native speakers
- **Writing System**: Hiragana, Katakana, Kanji (Chinese characters)

### Pluralization Pattern
Japanese uses a **single-form system** (1 form):
- **Universal form**: 一つの要素 (hitotsu no yōso) / 二つの要素 (futatsu no yōso)
- Same word form regardless of quantity

## Technical Implementation

### Configuration
```python
nplurals = 1  # Single-form system
```

### Plural ID Calculation
```python
get_plural_id = lambda n: 0  # Always returns 0
```

**Logic**: Always returns 0 regardless of the number value.

## Japanese Grammar Rules

### No Grammatical Plurals
Japanese nouns do not change form for plurals:
- 本 (hon) - book/books
- 猫 (neko) - cat/cats  
- 人 (hito) - person/people

### Quantity Expression
Quantities expressed through:
- **Numbers + Counters**: 三冊の本 (sansatsu no hon) - three books
- **Context**: Plurality understood from context
- **Demonstratives**: これら (korera) - these

### Counter System
Japanese uses specific counters for different objects:
- 本 (hon): long thin objects (pens, bottles)
- 匹 (hiki): small animals
- 人 (nin): people
- 冊 (satsu): books
- 台 (dai): machines, vehicles

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item')}}  # Same form always used
```

### Message Files
Language files in `applications/*/languages/ja.py`:
```python
{
'item': '要素',  # Same form for any quantity
'book': '本',
'person': '人',
# No separate plural forms needed
}
```

### Number Display
```python
# Quantity shown through numbers, not word forms
{{=count}} {{=T('item')}}  # "5 要素" (5 elements)
```

## Character Encoding

### Japanese Writing Systems
- **Hiragana**: あいうえお (phonetic script)
- **Katakana**: アイウエオ (phonetic script for foreign words)
- **Kanji**: 漢字 (Chinese characters with Japanese readings)
- **Rōmaji**: Latin alphabet transliteration

### UTF-8 Requirements
```html
<meta charset="utf-8">
<div lang="ja">
    {{=count}} {{=T('item')}}
</div>
```

## Cultural Context

### Linguistic Philosophy
- Precision through context rather than grammar
- Elegance in simplicity
- Implicit communication

### Business Applications
- Technical documentation
- E-commerce platforms
- International business interfaces

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 0   # "0個の要素"
assert get_plural_id(1) == 0   # "1個の要素"
assert get_plural_id(2) == 0   # "2個の要素"
assert get_plural_id(100) == 0 # "100個の要素"
```

### Template Usage
```python
# All numbers use same form
T('item') == '要素'  # Always the same
```

## Advantages of Single-Form System

### Simplicity
- No complex plural rules to learn
- Consistent word forms
- Reduced translation complexity

### Implementation Benefits
- Single message key needed
- No plural calculation complexity
- Reduced localization effort

## Related Components

### Other Single-Form Languages
- **Chinese** (zh.py): Similar single-form system
- **Vietnamese**: No grammatical plurals
- **Thai**: Context-based quantity

### Dependencies
- **gluon.languages**: Translation framework
- **Unicode**: Japanese character support (UTF-8)
- **Font support**: Japanese typography

This module enables Japanese language support in Web2py applications, respecting the linguistic conventions of Japanese while simplifying the internationalization process through the single-form approach.