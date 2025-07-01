# Arabic Plural Rules Module

**File**: `gluon/contrib/plural_rules/ar.py`  
**Language**: Arabic (ar)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Arabic language support in Web2py applications. Arabic has one of the most complex pluralization systems among world languages, with multiple plural forms and intricate grammatical rules.

## Language Profile

### Basic Information
- **Language Family**: Afro-Asiatic → Semitic → Central Semitic
- **ISO Code**: ar
- **Native Name**: العربية (al-ʿarabīya)
- **Regions**: Middle East, North Africa, Horn of Africa
- **Speakers**: ~400+ million native speakers
- **Writing System**: Arabic script (right-to-left)

### Pluralization Complexity
Arabic has **6 potential plural forms**:
1. **Zero** (صفر): No items
2. **One** (واحد): Exactly one item  
3. **Two** (اثنان): Exactly two items (dual form)
4. **Few** (قليل): 3-10 items
5. **Many** (كثير): 11-99 items
6. **Other** (آخر): 100+ items

## Technical Implementation

### Configuration
```python
nplurals = 6  # Complex Arabic pluralization system
```

### Plural ID Calculation
```python
get_plural_id = lambda n: (
    0 if n == 0 else           # Zero form
    1 if n == 1 else           # Singular
    2 if n == 2 else           # Dual form
    3 if 3 <= n <= 10 else     # Few (3-10)
    4 if 11 <= n <= 99 else    # Many (11-99)
    5                          # Other (100+)
)
```

### Examples
- n=0 → plural_id=0 (لا توجد عناصر - no items)
- n=1 → plural_id=1 (عنصر واحد - one item)
- n=2 → plural_id=2 (عنصران - two items)
- n=5 → plural_id=3 (خمسة عناصر - five items)
- n=15 → plural_id=4 (خمسة عشر عنصراً - fifteen items)
- n=100 → plural_id=5 (مائة عنصر - hundred items)

## Arabic Grammar Rules

### Dual Form (مثنى)
Arabic uniquely has a dual form for exactly two items:
- كتاب (kitāb) - book
- كتابان (kitābān) - two books
- كتب (kutub) - books (plural)

### Sound vs. Broken Plurals

**Sound Masculine Plural** (-ūn/-īn):
- معلم (muʿallim) → معلمون (muʿallimūn) - teachers

**Sound Feminine Plural** (-āt):
- معلمة (muʿallima) → معلمات (muʿallimāt) - female teachers

**Broken Plurals** (irregular):
- كتاب (kitāb) → كتب (kutub) - books
- رجل (rajul) → رجال (rijāl) - men

### Number-Noun Agreement
- 3-10: Noun in plural form
- 11-99: Noun in singular form
- 100+: Noun in singular form

## Construct Function

```python
# Arabic pluralization too complex for simple construction
# construct_plural_form = lambda word, plural_id: word
```

Arabic pluralization cannot be handled by simple suffix addition due to:
- Root-based morphology
- Vowel pattern changes
- Irregular broken plurals
- Gender agreement rules

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item_zero', 'item_one', 'item_two', 'item_few', 'item_many', 'item_other')}}
```

### Message Files
Arabic language files require all 6 forms:
```python
{
'item_zero': 'لا توجد عناصر',
'item_one': 'عنصر واحد', 
'item_two': 'عنصران',
'item_few': '%s عناصر',
'item_many': '%s عنصراً',
'item_other': '%s عنصر',
}
```

## RTL (Right-to-Left) Considerations

### Text Direction
- Arabic text flows right-to-left
- Numbers remain left-to-right
- Mixed content requires BiDi handling

### Template Integration
```html
<div dir="rtl" lang="ar">
    {{=T.plural(count, messages)}}
</div>
```

## Cultural and Regional Variations

### Modern Standard Arabic (MSA)
- Formal written Arabic
- Used in media and education
- Standardized pluralization rules

### Dialectal Variations
- Egyptian Arabic: Simplified plural system
- Levantine Arabic: Modified rules
- Gulf Arabic: Different number handling

### Considerations
- MSA preferred for formal applications
- Dialectal support may be needed for regional apps
- Cultural sensitivity in number presentation

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 0   # Zero form
assert get_plural_id(1) == 1   # Singular
assert get_plural_id(2) == 2   # Dual
assert get_plural_id(5) == 3   # Few
assert get_plural_id(15) == 4  # Many
assert get_plural_id(100) == 5 # Other
```

### Edge Cases
```python
assert get_plural_id(10) == 3  # Boundary few/many
assert get_plural_id(11) == 4  # Start of many
assert get_plural_id(99) == 4  # End of many
assert get_plural_id(101) == 5 # After hundred
```

## Linguistic Complexity

### Root System
Arabic uses triconsonantal roots with vowel patterns:
- k-t-b (writing): كتاب، كتب، كاتب، مكتوب

### Morphological Patterns
- fa'ʿal → fa'ʿāl (رجل → رجال)
- fiʿl → afʿāl (فكر → أفكار)
- fa'ʿala → fa'ʿa'il (جريدة → جرائد)

## Related Components

### Similar Complex Systems
- **Hebrew** (he.py): Related Semitic language
- **Russian** (ru.py): Complex but different system
- **Polish** (pl.py): Multiple forms

### Dependencies
- **gluon.languages**: RTL text support
- **Unicode**: Proper Arabic text handling
- **BiDi**: Bidirectional text algorithms

This module provides essential support for Arabic pluralization in Web2py applications, handling one of the world's most complex plural systems while respecting cultural and linguistic conventions.