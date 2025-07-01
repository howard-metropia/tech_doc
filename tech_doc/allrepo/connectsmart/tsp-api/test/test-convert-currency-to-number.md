# Convert Currency to Number Utility Test Suite

## Overview
Unit test suite for the `convertCurrencyToNumber` utility function, validating currency string parsing and conversion to numeric values. Tests the function's ability to handle various currency formats and symbols while extracting the numeric amount.

## File Purpose
- **Primary Function**: Test currency string to number conversion utility
- **Type**: Unit test suite
- **Role**: Validates currency parsing logic and edge case handling

## Test Configuration

### Test Setup
- **Framework**: Mocha with Node.js built-in assertions
- **Test Target**: `convertCurrencyToNumber` function from util helpers
- **Assertion Style**: Strict equality assertions
- **Test Coverage**: Multiple currency symbols and formats

### Dependencies
- `assert`: Node.js built-in assertion module
- `@app/src/helpers/util`: Source utility module

## Function Under Test

### `convertCurrencyToNumber(currencyString)`
**Purpose**: Extracts numeric value from currency-formatted strings
**Parameters**: 
- `currencyString` (string): Currency string with symbols and amount
**Returns**: 
- `number`: Numeric value without currency symbols
- `NaN`: For invalid or unparseable input

## Test Scenarios

### Currency Symbol Testing

#### Test Case 1: US Dollar ($) Format
**Input**: `"$5.31"`
**Expected Output**: `5.31`
**Purpose**: Test standard US dollar format with decimal places

#### Test Case 2: New Taiwan Dollar ($NT) Format
**Input**: `"$NT100"`
**Expected Output**: `100`
**Purpose**: Test currency with prefix code and no decimal places

#### Test Case 3: Euro (€) Format
**Input**: `"€10.50"`
**Expected Output**: `10.5`
**Purpose**: Test European currency symbol with decimal normalization

#### Test Case 4: Japanese Yen (¥) Format
**Input**: `"¥500"`
**Expected Output**: `500`
**Purpose**: Test Asian currency symbol without decimal places

#### Test Case 5: British Pound (£) Format
**Input**: `"£7.25"`
**Expected Output**: `7.25`
**Purpose**: Test British currency symbol with decimal places

### Error Handling Testing

#### Test Case 6: Invalid Input Handling
**Input**: `"invalid"`
**Expected Output**: `NaN`
**Purpose**: Test function behavior with non-currency strings
**Validation**: `assert(isNaN(convertCurrencyToNumber('invalid')))`

## Currency Format Analysis

### Supported Currency Symbols
- **$ (Dollar)**: US Dollar and variants
- **€ (Euro)**: European Union currency
- **¥ (Yen)**: Japanese Yen
- **£ (Pound)**: British Pound Sterling

### Format Variations
- **Standard Decimal**: `$5.31`, `€10.50`, `£7.25`
- **Whole Numbers**: `¥500`, `$NT100`
- **Currency Codes**: `$NT` prefix for New Taiwan Dollar
- **Decimal Normalization**: `10.50` → `10.5`

### Parsing Logic
**Expected Implementation**:
- Remove currency symbols and prefixes
- Extract numeric portions including decimals
- Convert to JavaScript number type
- Handle various decimal formats
- Return NaN for invalid inputs

## Test Validation Patterns

### Strict Equality Testing
```javascript
assert.strictEqual(convertCurrencyToNumber('$5.31'), 5.31);
assert.strictEqual(convertCurrencyToNumber('$NT100'), 100);
assert.strictEqual(convertCurrencyToNumber('€10.50'), 10.5);
```

### NaN Validation
```javascript
assert(isNaN(convertCurrencyToNumber('invalid')));
```

## International Currency Support

### Regional Currency Handling
- **North America**: US Dollar ($)
- **Asia**: Japanese Yen (¥), New Taiwan Dollar ($NT)
- **Europe**: Euro (€)
- **United Kingdom**: British Pound (£)

### Currency Code Integration
- **ISO Codes**: Support for currency code prefixes
- **Symbol Recognition**: Unicode currency symbols
- **Regional Variants**: Different dollar representations

## Edge Cases and Considerations

### Decimal Handling
- **Precision**: Maintains decimal precision
- **Normalization**: `10.50` becomes `10.5`
- **Zero Decimals**: `100.00` becomes `100`

### Invalid Input Scenarios
- **Non-numeric strings**: Return NaN
- **Multiple symbols**: Handling unclear
- **Empty strings**: Behavior not tested
- **Null/undefined**: Behavior not tested

## Use Cases in Application

### Payment Processing
- **Price Conversion**: Display prices to calculation values
- **Transaction Amounts**: Process payment amounts
- **Currency Exchange**: Base value extraction

### User Interface
- **Input Parsing**: User-entered currency amounts
- **Display Formatting**: Convert for calculations
- **Validation**: Ensure valid currency input

### International Commerce
- **Multi-currency Support**: Handle various currencies
- **Rate Calculations**: Extract values for conversion
- **Financial Reporting**: Standardize currency values

## Performance Considerations

### Function Efficiency
- **String Processing**: Minimal string manipulation
- **Pattern Matching**: Efficient symbol removal
- **Number Conversion**: Native JavaScript conversion

### Test Performance
- **Fast Execution**: Simple unit tests
- **No External Dependencies**: Pure function testing
- **Minimal Setup**: Direct function calls

## Integration Points

### Helper Utilities
- **Location**: `@app/src/helpers/util` module
- **Usage**: Shared utility across application
- **Dependencies**: Pure function with no external dependencies

### Application Integration
- **Payment Systems**: Currency amount processing
- **Financial Services**: Transaction value extraction
- **User Interfaces**: Input field processing

## Error Handling Strategies

### Input Validation
- **Type Checking**: String input expected
- **Format Validation**: Currency format recognition
- **Graceful Degradation**: NaN for invalid inputs

### Exception Safety
- **No Exceptions**: Function should not throw errors
- **Consistent Returns**: Always return number or NaN
- **Predictable Behavior**: Defined behavior for edge cases

## Test Coverage Analysis

### Covered Scenarios
- **Major Currencies**: Dollar, Euro, Yen, Pound
- **Decimal Formats**: Various decimal place handling
- **Invalid Input**: Basic error case testing
- **Currency Codes**: Prefix handling ($NT)

### Missing Test Cases
- **Empty String**: `""` input
- **Null/Undefined**: Invalid input types
- **Multiple Symbols**: `"$€5.00"` scenarios
- **Negative Amounts**: `"-$5.00"` handling
- **Large Numbers**: Scientific notation scenarios

## Maintenance Notes

### Function Evolution
- **New Currencies**: Add support for additional symbols
- **Format Support**: Extended formatting patterns
- **Internationalization**: Locale-specific parsing

### Test Maintenance
- **Currency Updates**: Add new currency test cases
- **Edge Cases**: Expand error scenario testing
- **Format Variations**: Test additional input formats

### Quality Assurance
- **Regression Testing**: Ensure consistent behavior
- **Cross-Platform**: Verify behavior across environments
- **Documentation**: Keep usage examples current

## Future Enhancements

### Extended Functionality
- **Locale Support**: Regional number formatting
- **Currency Validation**: Verify currency code validity
- **Precision Control**: Configurable decimal precision

### Testing Improvements
- **Property-Based Testing**: Generate random currency strings
- **Performance Benchmarks**: Measure parsing speed
- **Fuzzing**: Test with malformed inputs

### Integration Testing
- **API Integration**: Test in payment endpoints
- **User Interface**: Validate in form processing
- **Financial Workflows**: Test in transaction processing