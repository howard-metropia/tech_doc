# test-tofixed.js

## Overview
Test suite for the number formatting and precision utility function in the TSP API. Tests the `fixedPoint` helper function that provides consistent decimal precision handling across the application.

## File Location
`/test/test-tofixed.js`

## Dependencies
- **chai**: BDD/TDD assertion library
- **Helper**: util helper with fixedPoint function

## Function Under Test
```javascript
const { fixedPoint } = require('@app/src/helpers/util');
```

## Test Cases

### 1. Custom Decimal Precision
**Test**: Round numbers to specified decimal places

**Test Cases**:
```javascript
expect(fixedPoint(3.14159, 2)).to.equal(3.14);
expect(fixedPoint(10.123456, 3)).to.equal(10.123);
```

**Functionality**:
- Second parameter specifies decimal places
- Properly rounds to exact precision
- Handles varying precision requirements

### 2. Default Precision Behavior
**Test**: Default to 2 decimal places when no precision specified

**Test Cases**:
```javascript
expect(fixedPoint(3.14159)).to.equal(3.14);
expect(fixedPoint(10.123456)).to.equal(10.12);
```

**Default Behavior**:
- No second parameter defaults to 2 decimal places
- Consistent with financial calculation standards
- Common precision for coordinate and measurement data

### 3. Zero Decimal Places
**Test**: Round to whole numbers when digits is 0

**Test Cases**:
```javascript
expect(fixedPoint(123.456, 0)).to.equal(123);
expect(fixedPoint(0.987, 0)).to.equal(1);
```

**Rounding Logic**:
- 0 digits parameter rounds to integers
- Standard rounding rules apply (0.987 → 1)
- Useful for whole number calculations

### 4. Zero Input Handling
**Test**: Handle zero input correctly

**Test Case**:
```javascript
expect(fixedPoint(0)).to.equal(0);
```

**Edge Case**:
- Zero returns zero regardless of precision
- No floating-point precision issues
- Maintains mathematical correctness

### 5. Negative Number Support
**Test**: Handle negative numbers with same precision rules

**Test Cases**:
```javascript
expect(fixedPoint(-3.14159, 2)).to.equal(-3.14);
expect(fixedPoint(-10.123456, 3)).to.equal(-10.123);
```

**Negative Number Logic**:
- Sign preservation during rounding
- Same precision rules as positive numbers
- Handles financial calculations with debits/credits

### 6. Special Value Handling

#### NaN Input
**Test Case**:
```javascript
expect(fixedPoint(NaN)).to.be.NaN;
```

**Behavior**:
- NaN input returns NaN
- Preserves invalid calculation results
- Prevents propagation of invalid numbers

#### Infinity Input
**Test Cases**:
```javascript
expect(fixedPoint(Infinity)).to.equal(Infinity);
expect(fixedPoint(-Infinity)).to.equal(-Infinity);
```

**Behavior**:
- Infinity values preserved
- Both positive and negative infinity handled
- Maintains mathematical consistency

## Function Purpose

### Number Precision Management
- **Consistent Formatting**: Standardized decimal precision across application
- **Rounding Control**: Precise control over decimal places
- **Data Display**: Clean number formatting for user interfaces

### Common Use Cases
- **Coordinate Precision**: GPS coordinates to specific decimal places
- **Financial Calculations**: Currency amounts to 2 decimal places
- **Distance Measurements**: Route distances with appropriate precision
- **Time Calculations**: Duration calculations with specific precision

## Mathematical Behavior

### Rounding Algorithm
- **Standard Rounding**: Uses standard mathematical rounding rules
- **Half-up Rounding**: 0.5 rounds up to 1
- **Precision Control**: Exact decimal place specification

### Edge Case Handling
- **Zero Values**: Properly handled without precision errors
- **Negative Numbers**: Sign-aware rounding
- **Special Values**: NaN and Infinity preservation

## Integration Points

### Application Usage
- **API Responses**: Consistent number formatting in JSON responses
- **Database Storage**: Standardized precision before storage
- **User Interface**: Clean number display in mobile apps
- **Calculations**: Intermediate calculation precision control

### Data Types
- **Coordinates**: Latitude/longitude precision
- **Distances**: Route and travel distance formatting
- **Times**: Duration and ETA precision
- **Financial**: Payment and cost calculations

## Testing Strategy

### Comprehensive Coverage
- **Normal Cases**: Standard precision requirements
- **Edge Cases**: Zero, negative, and special values
- **Boundary Testing**: Different precision levels
- **Error Handling**: Invalid input management

### Mathematical Accuracy
- **Precision Verification**: Exact decimal place checking
- **Rounding Validation**: Correct rounding behavior
- **Sign Preservation**: Negative number handling
- **Special Value Testing**: NaN and Infinity cases

## Performance Considerations

### Efficiency
- **Simple Operation**: Fast mathematical function
- **No External Dependencies**: Pure JavaScript implementation
- **Memory Efficient**: No object creation overhead

### Reliability
- **Deterministic**: Consistent results for same inputs
- **Thread Safe**: No shared state or side effects
- **Error Resistant**: Handles edge cases gracefully

## Utility Function Design

### Function Signature
```javascript
fixedPoint(number, digits = 2)
```

### Parameters
- **number**: Input number to format
- **digits**: Decimal places (default: 2)

### Return Value
- **number**: Rounded number with specified precision
- **Special Values**: NaN, Infinity preserved

## Business Value

### Data Consistency
- **Standardized Precision**: Consistent number formatting
- **User Experience**: Clean, readable number displays
- **API Reliability**: Predictable response formats

### Transportation Context
- **GPS Accuracy**: Appropriate coordinate precision
- **Distance Display**: User-friendly distance formatting
- **Time Precision**: Readable duration and ETA displays
- **Cost Calculations**: Accurate financial computations

This test suite ensures the fixedPoint utility function provides reliable, consistent number formatting with proper precision control for all numeric data throughout the TSP API, maintaining data accuracy and user experience standards.