# Utils Service

## Overview

The Utils service provides essential utility functions for string formatting, mathematical operations, and date/time conversions throughout the TSP Job application.

## Service Information

- **Service Name**: Utils
- **File Path**: `/src/services/utils.js`
- **Type**: Utility Service
- **Dependencies**: None (Native JavaScript)

## Functions

### format()

String formatting utility using placeholder syntax.

**Purpose**: Formats strings with placeholders using `{}` syntax
**Usage**: Applied to string instances to replace placeholders with arguments
**Returns**: Formatted string with placeholders replaced

**Example**:
```javascript
const message = "Hello {} from {}";
const result = message.format("World", "TSP");
// Returns: "Hello World from TSP"
```

**Error Handling**:
- Throws error if argument count doesn't match placeholder count
- Validates placeholder-to-argument ratio

### pointSum(a, b)

Mathematical utility for precise decimal addition.

**Purpose**: Adds two numbers with precision handling to avoid floating-point errors
**Parameters**:
- `a` (number): First number to add
- `b` (number): Second number to add
**Returns**: Sum rounded to 2 decimal places

**Example**:
```javascript
const result = pointSum(1.1, 2.2);
// Returns: 3.3 (instead of 3.3000000000000003)
```

### d2dbs(d)

Date to database string converter.

**Purpose**: Converts JavaScript Date objects to database-compatible string format
**Parameters**:
- `d` (Date): JavaScript Date object to convert
**Returns**: String in format "YYYY-MM-DD HH:mm:ss"

**Example**:
```javascript
const date = new Date();
const dbString = d2dbs(date);
// Returns: "2023-12-25 10:30:45"
```

### dbs2d(s)

Database string to Date converter.

**Purpose**: Converts database date strings back to JavaScript Date objects
**Parameters**:
- `s` (string): Database date string in format "YYYY-MM-DD HH:mm:ss"
**Returns**: JavaScript Date object

**Example**:
```javascript
const dateString = "2023-12-25 10:30:45";
const date = dbs2d(dateString);
// Returns: Date object representing the specified time
```

## Integration Points

### Used By
- Database operations requiring date formatting
- API responses needing precise calculations
- Logging and error messages requiring string formatting
- Financial calculations requiring decimal precision

### Common Use Cases
- Converting dates for MySQL storage
- Formatting user-facing messages
- Calculating points, coins, or monetary values
- Parsing database timestamps

## Technical Details

### String Formatting
- Uses `{}` as placeholder syntax
- Supports variable argument length
- Maintains original string structure
- Validates argument count against placeholders

### Date Conversion
- Handles timezone considerations with UTC
- Removes milliseconds for database compatibility
- Maintains bidirectional conversion accuracy
- Supports standard database datetime formats

### Mathematical Operations
- Addresses JavaScript floating-point precision issues
- Rounds to 2 decimal places for consistency
- Optimized for financial and scoring calculations
- Prevents accumulation of rounding errors

## Error Handling

- **Format Function**: Throws descriptive errors for argument mismatch
- **Date Functions**: Handles invalid date strings gracefully
- **Math Functions**: Returns NaN for invalid numeric inputs
- **Type Safety**: Validates input types before processing

## Performance Considerations

- Lightweight utility functions with minimal overhead
- No external dependencies or heavy computations
- Optimized for frequent use in service layers
- Memory-efficient implementations

## Dependencies

- **Native JavaScript**: Uses built-in Date, Math, and String methods
- **No External Libraries**: Self-contained utility functions
- **Cross-Service Compatibility**: Works with all TSP Job services

## Testing Considerations

- Test string formatting with various placeholder counts
- Verify date conversion accuracy across timezones
- Validate mathematical precision with edge cases
- Test error handling for invalid inputs

## Usage Guidelines

1. **String Formatting**: Use for user messages and log entries
2. **Date Conversion**: Apply for all database date operations
3. **Mathematical Operations**: Use for any decimal calculations
4. **Error Handling**: Always validate inputs before processing