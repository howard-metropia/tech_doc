# Chinese Plural Rules Module

**File**: `gluon/contrib/plural_rules/zh.py`  
**Language**: Chinese (zh)  
**Type**: Pluralization Rules Implementation  
**Framework**: Web2py Gluon Framework

## Overview

This module implements pluralization rules for Chinese language support in Web2py applications. Chinese follows a **single-form system** with no grammatical distinction between singular and plural.

## Language Profile

### Basic Information
- **Language Family**: Sino-Tibetan → Sinitic
- **ISO Code**: zh
- **Native Name**: 中文 (zhōngwén), 汉语 (hànyǔ)
- **Regions**: China, Taiwan, Singapore, Malaysia, diaspora worldwide
- **Speakers**: ~900 million native speakers (most spoken language globally)
- **Writing System**: Chinese characters (Hanzi) - Simplified and Traditional

### Pluralization Pattern
Chinese uses a **single-form system** (1 form):
- **Universal form**: 一个元素 (yīgè yuánsù) / 两个元素 (liǎnggè yuánsù)
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

## Chinese Grammar Rules

### No Grammatical Plurals
Chinese nouns do not change form for plurals:
- 书 (shū) - book/books
- 猫 (māo) - cat/cats
- 人 (rén) - person/people

### Quantity Expression
Quantities expressed through:
- **Numbers + Measure Words**: 三本书 (sān běn shū) - three books
- **Context**: Plurality understood from situation
- **Demonstratives**: 这些 (zhèxiē) - these

### Measure Word System
Chinese uses specific measure words (量词 liàngcí):
- 个 (gè): general classifier for people, objects
- 本 (běn): books, magazines
- 只 (zhī): animals, one of a pair
- 辆 (liàng): vehicles
- 张 (zhāng): flat objects (paper, tables)

## Variant Support

### Simplified Chinese (简体中文)
- **Regions**: Mainland China, Singapore
- **Characters**: 书, 车, 学 (simplified forms)
- **Standard**: GB encoding, UTF-8

### Traditional Chinese (繁體中文)
- **Regions**: Taiwan, Hong Kong, Macau
- **Characters**: 書, 車, 學 (traditional forms)
- **Standard**: Big5 encoding, UTF-8

## Integration with Web2py

### Usage in Templates
```python
{{=T.plural(count, 'item')}}  # Same form always used
```

### Message Files
Language files in `applications/*/languages/zh.py`:
```python
{
'item': '元素',    # Same form for any quantity
'book': '书',      # Simplified Chinese
'person': '人',
# Traditional Chinese variant:
# 'book': '書',   # Traditional Chinese
}
```

### Number Display
```python
# Quantity shown through numbers and measure words
{{=count}} {{=T('measure_word')}} {{=T('item')}}  # "5 个 元素"
```

## Character Encoding

### Writing Systems
- **Simplified Chinese**: 简化字 (mainland China standard)
- **Traditional Chinese**: 繁体字 (Taiwan, Hong Kong standard)
- **Pinyin**: Romanization system (zhōngwén)

### UTF-8 Requirements
```html
<meta charset="utf-8">
<div lang="zh-CN">  <!-- Simplified Chinese -->
    {{=count}} {{=T('item')}}
</div>
<div lang="zh-TW">  <!-- Traditional Chinese -->
    {{=count}} {{=T('item')}}
</div>
```

## Regional Variations

### Mainland Chinese (简体中文)
- Simplified character set
- Pinyin romanization
- Standard Mandarin pronunciation

### Taiwan Chinese (繁體中文)
- Traditional character set
- Bopomofo phonetic system
- Taiwan Mandarin variants

### Hong Kong Chinese (繁體中文)
- Traditional characters
- Cantonese influence
- British English loanwords

### Singapore Chinese (简体中文)
- Simplified characters
- Multilingual context
- Southeast Asian Chinese variants

## Cultural Context

### Historical Significance
- World's oldest continuous writing system
- Rich literary and philosophical tradition
- Character-based meaning system

### Modern Usage
- Official language in multiple countries
- Major language for international business
- Growing digital presence globally

## Testing Examples

### Number Validation
```python
assert get_plural_id(0) == 0   # "0个元素"
assert get_plural_id(1) == 0   # "1个元素"
assert get_plural_id(2) == 0   # "2个元素"
assert get_plural_id(100) == 0 # "100个元素"
```

### Template Usage
```python
# All numbers use same form
T('item') == '元素'  # Always the same
```

## Advantages of Single-Form System

### Linguistic Efficiency
- No complex inflection rules
- Consistent word forms
- Clear semantic meaning

### Implementation Benefits
- Single translation key needed
- No plural calculation required
- Simplified localization process

## Character Input and Display

### Input Methods
- **Pinyin**: 拼音输入法 (phonetic input)
- **Wubi**: 五笔字型 (shape-based input)
- **Handwriting**: Touch and stylus recognition

### Font Requirements
- Unicode CJK font support
- Proper character rendering
- Traditional/Simplified distinction

## Related Components

### Other Single-Form Languages
- **Japanese** (ja.py): Similar single-form system
- **Korean**: Limited pluralization
- **Vietnamese**: Context-based quantity

### Similar Writing Systems
- **Japanese Kanji**: Borrowed Chinese characters
- **Korean Hanja**: Historical Chinese character usage

### Dependencies
- **gluon.languages**: Translation framework
- **Unicode**: Chinese character support (UTF-8)
- **CJK fonts**: Chinese typography support

This module enables Chinese language support in Web2py applications, respecting the linguistic conventions of Chinese while leveraging the simplicity of the single-form approach for efficient internationalization.