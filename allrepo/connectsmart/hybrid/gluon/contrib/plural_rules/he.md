# Hebrew Plural Rules Module

**File**: `gluon/contrib/plural_rules/he.py`  
**Language**: Hebrew (he)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Hebrew language support in Web2py applications. Hebrew follows a binary pluralization system but has complex morphological patterns and gender-based plural formation.

## Language Profile

### Basic Information
- **Language Family**: Afro-Asiatic → Semitic → Central Semitic → Northwest Semitic
- **ISO Code**: he
- **Native Name**: עברית (ivrit)
- **Regions**: Israel, Jewish communities worldwide
- **Speakers**: ~9 million speakers
- **Writing System**: Hebrew alphabet (right-to-left)

### Pluralization Pattern
Hebrew uses a **binary pluralization system** (2 forms):
1. **Singular** (n = 1): פריט אחד (prit echad)
2. **Plural** (n ≠ 1): שני פריטים (shney pritim)

## Technical Implementation

### Configuration
```python
nplurals = 2  # Binary pluralization system
```

### Plural ID Calculation
```python
get_plural_id = lambda n: int(n != 1)
```

## Hebrew Grammar Rules

### Gender-Based Plurals

**Masculine Plurals** (-im ending):
- ספר → ספרים (sefer → sefarim) - book → books
- בית → בתים (bayit → batim) - house → houses
- איש → אנשים (ish → anashim) - man → men

**Feminine Plurals** (-ot ending):
- מכונית → מכוניות (mechonit → mechoniyot) - car → cars
- בת → בנות (bat → banot) - daughter → daughters
- אישה → נשים (isha → nashim) - woman → women

### Root-Based Morphology

Hebrew uses a **triconsonantal root system**:
- Root כ-ת-ב (writing): כתב, כתבים, כתובת, כתיבה
- Root ל-מ-ד (learning): למד, למידה, תלמיד, תלמידים

### Irregular Patterns
Many Hebrew nouns have irregular plurals:
- ילד → ילדים (yeled → yeladim) - child → children
- אב → אבות (av → avot) - father → fathers
- בן → בנים (ben → banim) - son → sons

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item', 'items')}}  # Uses Hebrew rules
```

### Message Files
Hebrew requires explicit plural forms:
```python
{
'item': 'פריט',
'items': 'פריטים',
'book': 'ספר',
'books': 'ספרים',
# All forms must be explicitly defined
}
```

## RTL (Right-to-Left) Considerations

### Text Direction
- Hebrew text flows right-to-left
- Numbers remain left-to-right
- Mixed content requires BiDi handling

### Template Integration
```html
<div dir="rtl" lang="he">
    {{=T.plural(count, messages)}}
</div>
```

## Character Encoding

### Hebrew Alphabet
- **22 letters**: א ב ג ד ה ו ז ח ט י כ ל מ נ ס ע פ צ ק ר ש ת
- **Final forms**: ך ם ן ף ץ (used at word endings)
- **Vowel points** (niqqud): Usually omitted in modern text

### Modern Hebrew Numbers
- **Hebrew numerals**: א׳ ב׳ ג׳ ד׳ (traditional)
- **Arabic numerals**: 1 2 3 4 (modern standard)

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 1  # "אפס פריטים"
assert get_plural_id(1) == 0  # "פריט אחד"
assert get_plural_id(2) == 1  # "שני פריטים"
assert get_plural_id(10) == 1 # "עשרה פריטים"
```

## Related Components

### Similar Semitic Languages
- **Arabic** (ar.py): Related Semitic language with complex plurals
- **Aramaic**: Historical linguistic connection

### Dependencies
- **gluon.languages**: RTL text support
- **Unicode**: Hebrew character support
- **BiDi**: Bidirectional text algorithms

This module enables Hebrew pluralization in Web2py applications while respecting the complex morphological patterns of this ancient Semitic language in its modern revival.