# Util Helper

## Overview
**File**: `src/helpers/util.js`  
**Type**: General Utility Module  
**Purpose**: Provides common utility functions for data transformation and validation

## Core Functions

### Null to Array Replacement
```javascript
const replaceNullWithEmptyArray = (obj, fieldsToTransform) => {
  for (const key in obj) {
    if (fieldsToTransform.includes(key) && obj[key] === null) {
      obj[key] = [];
    } else if (typeof obj[key] === 'object') {
      replaceNullWithEmptyArray(obj[key], fieldsToTransform);
    }
  }
};
```

### String Capitalization
```javascript
const capitalizeLetters = (str) => {
  return str.replace(/\b\w+\b/g, (word) => {
    return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
  });
};
```

### Currency Conversion
```javascript
const convertCurrencyToNumber = (currencyValue) => {
  const numberPart = currencyValue.match(/[0-9]+(\.[0-9]+)?/);
  if (numberPart) {
    return parseFloat(numberPart[0]);
  } else {
    return NaN;
  }
};
```

### Version Extraction
```javascript
const extractVersion = (version) => {
  const match = version.match(/(?:\d+\.)?(\d{3})\.\d+/);
  return match ? Number(match[1]) : -1;
};
```

## Function Details

### replaceNullWithEmptyArray
- **Purpose**: Converts null values to empty arrays for specified fields
- **Recursive**: Handles nested objects
- **Mutation**: Modifies object in place
- **Use Case**: API response sanitization

### capitalizeLetters
- **Purpose**: Title case conversion for strings
- **Pattern**: First letter uppercase, rest lowercase per word
- **Boundary**: Uses word boundaries for accurate capitalization
- **Use Case**: Name formatting, address formatting

### convertCurrencyToNumber
- **Purpose**: Extracts numeric value from currency strings
- **Pattern**: Matches decimal numbers (including decimals)
- **Return**: parseFloat result or NaN if no match
- **Use Case**: Price parsing, financial calculations

### extractVersion
- **Purpose**: Extracts version number from version strings
- **Pattern**: Matches 3-digit version numbers
- **Return**: Numeric version or -1 if no match
- **Use Case**: Version comparison, compatibility checks

## Usage Examples

### Null Replacement
```javascript
const { replaceNullWithEmptyArray } = require('./util');

const data = {
  items: null,
  categories: ['a', 'b'],
  nested: {
    tags: null,
    metadata: {}
  }
};

replaceNullWithEmptyArray(data, ['items', 'tags']);
// Result: data.items = [], data.nested.tags = []
```

### String Capitalization
```javascript
const { capitalizeLetters } = require('./util');

const result = capitalizeLetters('john doe smith');
// Result: "John Doe Smith"

const address = capitalizeLetters('123 main STREET apt 4b');
// Result: "123 Main Street Apt 4b"
```

### Currency Parsing
```javascript
const { convertCurrencyToNumber } = require('./util');

const price1 = convertCurrencyToNumber('$25.99');
// Result: 25.99

const price2 = convertCurrencyToNumber('USD 15.00');
// Result: 15.00

const invalid = convertCurrencyToNumber('No price');
// Result: NaN
```

### Version Extraction
```javascript
const { extractVersion } = require('./util');

const version1 = extractVersion('1.123.4');
// Result: 123

const version2 = extractVersion('2.0.456.7');
// Result: 456

const invalid = extractVersion('v1.2.3');
// Result: -1
```

## Implementation Details

### Null Replacement Logic
- **Field Check**: Only processes specified fields
- **Type Check**: Verifies object type before recursion
- **Mutation**: Directly modifies input object
- **Recursion**: Handles arbitrarily nested structures

### Regex Patterns
- **Word Boundary**: `\b\w+\b` for complete words
- **Number Pattern**: `[0-9]+(\.[0-9]+)?` for decimal numbers
- **Version Pattern**: `(?:\d+\.)?(\d{3})\.\d+` for 3-digit versions

## Performance Considerations

### replaceNullWithEmptyArray
- **Time Complexity**: O(n) where n is total object properties
- **Space Complexity**: O(d) where d is object depth (recursion stack)
- **Mutation**: No additional memory for result

### String Operations
- **Regex Performance**: Compiled regex patterns for efficiency
- **String Immutability**: Creates new strings for results
- **Memory Usage**: Proportional to string length

## Error Handling

### Input Validation
- **No Explicit Validation**: Functions assume valid input types
- **Graceful Degradation**: Return sensible defaults for invalid input
- **NaN Handling**: convertCurrencyToNumber returns NaN for invalid input

### Edge Cases
```javascript
// Empty strings
capitalizeLetters(''); // Returns ''

// Non-string input (potential issues)
capitalizeLetters(null); // May throw error

// Invalid currency formats
convertCurrencyToNumber(''); // Returns NaN
```

## Integration Points

### Common Use Cases
- **API Response Processing**: Clean up null values
- **Data Formatting**: Standardize string formats
- **Financial Data**: Parse currency values
- **Version Management**: Extract and compare versions

### Service Integration
- **Database Models**: Clean up query results
- **External APIs**: Format data for third-party services
- **User Interface**: Format display data
- **Validation**: Pre-process input data

## Testing Considerations

### Unit Tests
```javascript
describe('util functions', () => {
  test('replaceNullWithEmptyArray', () => {
    const obj = { items: null, count: 5 };
    replaceNullWithEmptyArray(obj, ['items']);
    expect(obj.items).toEqual([]);
    expect(obj.count).toBe(5);
  });
  
  test('capitalizeLetters', () => {
    expect(capitalizeLetters('hello world')).toBe('Hello World');
  });
});
```

### Edge Cases to Test
- **Empty Objects**: replaceNullWithEmptyArray with empty objects
- **Special Characters**: capitalizeLetters with punctuation
- **Complex Currency**: convertCurrencyToNumber with various formats
- **Invalid Versions**: extractVersion with non-standard formats

## Best Practices

### Function Usage
- **Immutable Operations**: Consider creating non-mutating versions
- **Input Validation**: Add validation for production use
- **Error Handling**: Wrap in try-catch for safety
- **Documentation**: Clear documentation of side effects

### Performance
- **Batch Operations**: Use efficiently for large datasets
- **Memoization**: Consider caching for repeated operations
- **Validation**: Pre-validate inputs to avoid processing invalid data

## Limitations

### Current Implementation
- **No Input Validation**: Functions don't validate input types
- **Mutation**: replaceNullWithEmptyArray mutates input
- **Limited Patterns**: Fixed regex patterns may not cover all cases
- **Error Handling**: Minimal error handling for edge cases

### Enhancement Opportunities
- **Type Safety**: Add TypeScript definitions
- **Validation**: Input type validation
- **Immutable Versions**: Non-mutating alternatives
- **Extended Patterns**: More flexible regex patterns

## Dependencies

### External Libraries
- **None**: Uses only JavaScript built-in functions
- **Regex**: Built-in regex engine
- **Type System**: JavaScript's built-in type checking

### Standards Compliance
- **ES6+**: Uses modern JavaScript features
- **Cross-Platform**: Works in Node.js and browser environments
- **No Dependencies**: Lightweight implementation

## Export Structure

```javascript
module.exports = {
  replaceNullWithEmptyArray,
  capitalizeLetters,
  convertCurrencyToNumber,
  extractVersion,
};
```

### Individual Imports
```javascript
const { capitalizeLetters } = require('./util');
```

### Full Import
```javascript
const util = require('./util');
util.capitalizeLetters('hello');
```