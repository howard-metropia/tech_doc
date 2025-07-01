# Persian (Farsi) Plural Rules Module

**File**: `gluon/contrib/plural_rules/fa.py`  
**Language**: Persian/Farsi (fa)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Persian (Farsi) language support in Web2py applications. Persian follows a binary pluralization system with two forms: singular and plural.

## Language Profile

### Basic Information
- **Language Family**: Indo-European → Iranian → Western Iranian → Southwestern Iranian
- **ISO Code**: fa
- **Native Name**: فارسی (fārsi), پارسی (pārsi)
- **Regions**: Iran, Afghanistan (Dari), Tajikistan (Tajik)
- **Speakers**: ~70 million native speakers
- **Writing System**: Persian alphabet (Arabic script, right-to-left)

### Pluralization Pattern
Persian uses a **binary pluralization system** (2 forms):
1. **Singular** (n = 1): یک عنصر (yek onsor)
2. **Plural** (n ≠ 1): دو عنصر (do onsor)

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

## Persian Grammar Rules

### Plural Formation Patterns

**Regular -hā suffix** (ها):
- کتاب → کتاب‌ها (ketāb → ketāb-hā) - book → books
- خانه → خانه‌ها (xāne → xāne-hā) - house → houses

**Alternative -ān suffix** (ان):
- مرد → مردان (mard → mardān) - man → men
- زن → زنان (zan → zanān) - woman → women

**Arabic borrowings retain Arabic plurals**:
- کتاب → کتب (ketāb → kotob) - book → books (formal)
- علم → علوم (elm → olum) - science → sciences

### Number Usage
Persian often uses singular form with numbers:
- دو کتاب (do ketāb) - two book (not books)
- پنج خانه (panj xāne) - five house (not houses)

## RTL (Right-to-Left) Considerations

### Text Direction
- Persian text flows right-to-left
- Numbers can be left-to-right (Arabic-Indic digits)
- Mixed content requires BiDi handling

### Template Integration
```html
<div dir="rtl" lang="fa">
    {{=T.plural(count, messages)}}
</div>
```

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item', 'items')}}  # Uses Persian rules
```

### Message Files
Language files in `applications/*/languages/fa.py`:
```python
{
'item': 'عنصر',
'items': 'عناصر',
'book': 'کتاب',
'books': 'کتاب‌ها',
# Persian translations in Persian script
}
```

## Character Encoding

### Persian Characters
- **Persian alphabet**: 32 letters
- **Additional letters**: پ، چ، ژ، گ (not in Arabic)
- **UTF-8 encoding** required for proper display

### Digit Systems
- **Persian digits**: ۰۱۲۳۴۵۶۷۸۹
- **Arabic-Indic digits**: ٠١٢٣٤٥٦٧٨٩
- **ASCII digits**: 0123456789 (in technical contexts)

## Regional Variations

### Iranian Persian (Farsi)
- Standard implementation base
- Modern literary standard
- Tehran dialect influence

### Afghan Persian (Dari)
- Same pluralization rules
- Some vocabulary differences
- Official language of Afghanistan

### Tajik Persian (Tajiki)
- Uses Cyrillic script in Tajikistan
- Same grammatical rules
- Russian language influence

## Cultural Context

### Formal vs. Informal
- Formal language uses more Arabic plurals
- Informal language prefers Persian suffixes
- Context determines appropriate forms

### Poetry and Literature
- Rich literary tradition
- Classical vs. modern forms
- Meter and rhythm considerations

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 1  # "صفر عنصر"
assert get_plural_id(1) == 0  # "یک عنصر"
assert get_plural_id(2) == 1  # "دو عنصر"
assert get_plural_id(10) == 1 # "ده عنصر"
```

### Edge Cases
```python
assert get_plural_id(-1) == 1  # Negative numbers
assert get_plural_id(1.0) == 0 # Float equality
assert get_plural_id(1.1) == 1 # Non-integer
```

## Related Components

### Similar Scripts
- **Arabic** (ar.py): Related script and some grammar
- **Hebrew** (he.py): Related Semitic patterns

### Dependencies
- **gluon.languages**: RTL text support
- **Unicode**: Persian character support
- **BiDi**: Bidirectional text algorithms
- Language files in applications directory

This module enables proper Persian pluralization in Web2py applications, supporting the rich grammatical tradition of Persian while handling right-to-left text display and cultural variations across Persian-speaking regions.