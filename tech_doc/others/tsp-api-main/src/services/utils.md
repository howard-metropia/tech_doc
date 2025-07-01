# TSP API Utils Service Documentation

## 🔍 Quick Summary (TL;DR)
The utils service provides essential utility functions for string formatting, numerical calculations, and date/time conversions used throughout the TSP API codebase.

**Keywords:** utility-functions | string-formatting | date-conversion | numerical-operations | helper-functions | common-utilities | timestamp-conversion

**Primary use cases:** String interpolation with placeholders, precise point calculations, database datetime formatting, timestamp conversions

**Compatibility:** Node.js >= 16.0.0, standalone utility functions, no external dependencies

## ❓ Common Questions Quick Index
- **Q: How does string formatting work?** → Uses `{}` placeholders replaced with provided arguments
- **Q: Why use pointSum for additions?** → Handles floating-point precision issues in financial calculations
- **Q: What datetime formats are supported?** → ISO strings, database datetime, and Unix timestamps
- **Q: Are these functions pure?** → Yes, no side effects or external dependencies
- **Q: Can format be used with variables?** → Yes, extend String prototype: `String.prototype.format = utils.format`
- **Q: What timezone is used?** → UTC for all datetime operations

## 📋 Functionality Overview

**Non-technical explanation:** 
Think of this as a **toolbox of helper functions** that make common programming tasks easier. It has tools for putting text together with variables (like filling in blanks), doing math with money amounts precisely, and converting between different ways of representing dates and times.

**Technical explanation:** 
A collection of pure utility functions providing string templating, floating-point arithmetic with precision handling, and bidirectional datetime format conversion between ISO strings, database datetime format, and Unix timestamps. Designed for consistent data handling across the application.

**Business value explanation:**
Ensures data consistency and reduces code duplication across the platform. Prevents floating-point calculation errors in financial operations, standardizes datetime handling for database operations, and provides maintainable string formatting for dynamic content generation.

## 🔧 Technical Specifications

- **File:** `allrepo/connectsmart/tsp-api/src/services/utils.js`
- **Language:** JavaScript (ES2020)
- **Framework:** Standalone utility module
- **Type:** Utility Functions Service
- **File Size:** ~0.9 KB
- **Complexity Score:** ⭐ (Low - Simple utility functions)

**Dependencies:** None (pure JavaScript functions)

## 📝 Detailed Code Analysis

### format Function

**Purpose:** String interpolation using `{}` placeholder syntax

**Usage:** Can be attached to String prototype for method-style calls

**Parameters:** Variable arguments to replace placeholders

**Returns:** String with placeholders replaced by provided arguments

**Implementation:**
```javascript
function format() {
  const base = this.toString().split('{}');
  if (arguments.length !== base.length - 1) {
    throw new Error('String format arguments number not match');
  }
  return base.reduce((acc, cur, idx) => {
    if (arguments[idx]) {
      return acc + cur + arguments[idx].toString();
    } else {
      return acc + cur;
    }
  }, '');
}
```

**Validation:** Ensures exact match between placeholders and arguments

### pointSum Function

**Purpose:** Precise addition for financial calculations avoiding floating-point errors

**Parameters:**
- `a`: Number - First value
- `b`: Number - Second value

**Returns:** Number - Sum rounded to 2 decimal places

**Implementation:**
```javascript
function pointSum(a, b) {
  return Math.round((a + b) * 100) / 100;
}
```

**Precision Handling:** Multiplies by 100, rounds, then divides to maintain 2-decimal precision

### DateTime Conversion Functions

**d2dbs (Date to Database String):**
- Converts JavaScript Date to MySQL datetime format
- Format: `YYYY-MM-DD HH:MM:SS`
- Removes timezone and milliseconds

**dbs2d (Database String to Date):**
- Converts database datetime string to JavaScript Date
- Adds timezone marker for UTC interpretation

**dbs2ts (Database String to Timestamp):**
- Converts database datetime to Unix timestamp
- Returns seconds since epoch

## 🚀 Usage Methods

### String Formatting
```javascript
const utils = require('@app/src/services/utils');

// Extend String prototype for method-style usage
String.prototype.format = utils.format;

// Basic string formatting
const template = "Hello {}, you have {} messages";
const message = template.format("John", 5);
console.log(message); // "Hello John, you have 5 messages"

// Multi-placeholder formatting
const notification = "Trip from {} to {} costs ${} and takes {} minutes";
const tripInfo = notification.format("Home", "Office", 12.50, 25);
console.log(tripInfo); // "Trip from Home to Office costs $12.5 and takes 25 minutes"

// Error handling
try {
  const invalid = "Hello {}".format("John", "Extra"); // Too many arguments
} catch (error) {
  console.error(error.message); // "String format arguments number not match"
}
```

### Precise Financial Calculations
```javascript
const utils = require('@app/src/services/utils');

// Avoid floating-point precision issues
const price1 = 12.1;
const price2 = 0.2;

// Standard addition (problematic)
console.log(price1 + price2); // 12.299999999999999

// Using pointSum (precise)
console.log(utils.pointSum(price1, price2)); // 12.3

// Multiple calculations
function calculateTotalCost(basePrice, tax, tip) {
  const withTax = utils.pointSum(basePrice, tax);
  const total = utils.pointSum(withTax, tip);
  return total;
}

const total = calculateTotalCost(10.99, 1.21, 2.00);
console.log(`Total: $${total}`); // Total: $14.2
```

### DateTime Operations
```javascript
const utils = require('@app/src/services/utils');

// Current date to database format
const now = new Date();
const dbDateTime = utils.d2dbs(now);
console.log(dbDateTime); // "2024-06-25 14:30:00"

// Database string back to Date
const dbString = "2024-06-25 14:30:00";
const dateObj = utils.dbs2d(dbString);
console.log(dateObj); // 2024-06-25T14:30:00.000Z

// Database string to Unix timestamp
const timestamp = utils.dbs2ts(dbString);
console.log(timestamp); // 1719331800

// Chain conversions
const originalDate = new Date();
const dbFormat = utils.d2dbs(originalDate);
const backToDate = utils.dbs2d(dbFormat);
const asTimestamp = utils.dbs2ts(dbFormat);

console.log('Original:', originalDate);
console.log('DB Format:', dbFormat);
console.log('Back to Date:', backToDate);
console.log('As Timestamp:', asTimestamp);
```

### Utility Service Class
```javascript
class CommonUtils {
  constructor() {
    this.utils = require('@app/src/services/utils');
    // Extend String prototype for easier formatting
    if (!String.prototype.format) {
      String.prototype.format = this.utils.format;
    }
  }

  formatMessage(template, ...args) {
    try {
      return template.format(...args);
    } catch (error) {
      console.error('String formatting error:', error.message);
      return template; // Return original template on error
    }
  }

  calculatePoints(basePoints, bonusPoints, multiplier = 1) {
    const total = this.utils.pointSum(basePoints, bonusPoints);
    return this.utils.pointSum(total * multiplier, 0); // Ensure precision
  }

  formatDateTime(date, format = 'db') {
    switch (format) {
      case 'db':
        return this.utils.d2dbs(date);
      case 'timestamp':
        return this.utils.dbs2ts(this.utils.d2dbs(date));
      case 'iso':
        return date.toISOString();
      default:
        return date.toString();
    }
  }

  parseDateTime(dateString, format = 'db') {
    switch (format) {
      case 'db':
        return this.utils.dbs2d(dateString);
      case 'timestamp':
        return new Date(dateString * 1000);
      case 'iso':
        return new Date(dateString);
      default:
        return new Date(dateString);
    }
  }

  buildNotificationMessage(userId, action, details) {
    const templates = {
      trip_completed: "Congratulations {}! Your trip is complete. Distance: {} miles, Duration: {} minutes.",
      points_earned: "Great job {}! You've earned {} points. Total balance: {} points.",
      reminder: "Hi {}, don't forget your scheduled trip to {} at {}."
    };

    const template = templates[action];
    if (!template) {
      return `User ${userId}: ${action}`;
    }

    return this.formatMessage(template, ...details);
  }
}

// Usage examples
const commonUtils = new CommonUtils();

// Notification messages
const tripMessage = commonUtils.buildNotificationMessage(
  123, 
  'trip_completed', 
  ['John', 5.2, 18]
);
console.log(tripMessage);

// Point calculations
const totalPoints = commonUtils.calculatePoints(10.5, 2.3, 1.5);
console.log(`Total points: ${totalPoints}`);

// Date formatting
const dbTime = commonUtils.formatDateTime(new Date(), 'db');
console.log(`DB format: ${dbTime}`);
```

### Template Engine Integration
```javascript
class MessageTemplateEngine {
  constructor() {
    this.utils = require('@app/src/services/utils');
    String.prototype.format = this.utils.format;
  }

  renderTemplate(templateId, data) {
    const templates = {
      welcome: "Welcome {}, your account {} is now active!",
      trip_summary: "Trip from {} to {} completed in {} minutes for ${}",
      reward_earned: "Congratulations! You earned {} points on {} for {}",
      weekly_summary: "This week: {} trips, {} miles, {} points earned"
    };

    const template = templates[templateId];
    if (!template) {
      throw new Error(`Template '${templateId}' not found`);
    }

    try {
      const values = Array.isArray(data) ? data : Object.values(data);
      return template.format(...values);
    } catch (error) {
      throw new Error(`Template rendering failed: ${error.message}`);
    }
  }

  renderBatch(templateData) {
    return templateData.map(({ templateId, data }) => {
      try {
        return {
          success: true,
          message: this.renderTemplate(templateId, data)
        };
      } catch (error) {
        return {
          success: false,
          error: error.message,
          templateId
        };
      }
    });
  }
}

// Usage
const templateEngine = new MessageTemplateEngine();

const messages = templateEngine.renderBatch([
  { templateId: 'welcome', data: ['John', 'premium'] },
  { templateId: 'trip_summary', data: ['Home', 'Office', 25, 12.50] },
  { templateId: 'reward_earned', data: [50, 'Monday', 'carpooling'] }
]);

messages.forEach(msg => {
  if (msg.success) {
    console.log('Message:', msg.message);
  } else {
    console.error('Error:', msg.error);
  }
});
```

## 📊 Output Examples

### String Formatting Results
```javascript
// Template: "User {} completed trip {} with {} points"
// Args: ["John", "TR001", 25]
// Result: "User John completed trip TR001 with 25 points"

// Template: "Trip cost: ${} (includes ${} tax)"
// Args: [12.50, 1.25]
// Result: "Trip cost: $12.5 (includes $1.25 tax)"
```

### Precise Calculations
```javascript
// Standard JavaScript addition
0.1 + 0.2 = 0.30000000000000004

// Using pointSum
utils.pointSum(0.1, 0.2) = 0.3

// Financial calculations
utils.pointSum(10.99, 1.21) = 12.2
utils.pointSum(15.555, 2.444) = 18
```

### DateTime Conversions
```javascript
// Date to database string
new Date('2024-06-25T14:30:00.000Z') → "2024-06-25 14:30:00"

// Database string to Date
"2024-06-25 14:30:00" → 2024-06-25T14:30:00.000Z

// Database string to timestamp
"2024-06-25 14:30:00" → 1719331800
```

### Error Cases
```javascript
// Mismatched placeholders and arguments
"Hello {} {}" + format("John") → Error: "String format arguments number not match"

// Invalid date strings
dbs2d("invalid-date") → Invalid Date object
```

## ⚠️ Important Notes

### String Formatting Limitations
- **Exact Match Required:** Number of `{}` placeholders must match arguments
- **No Named Parameters:** Only positional placeholders supported
- **toString() Conversion:** All arguments converted to strings
- **No Escaping:** Cannot include literal `{}` in templates

### Floating-Point Precision
- **Two Decimal Places:** pointSum always rounds to 2 decimal places
- **Financial Focus:** Designed for currency calculations
- **Multiplication Method:** Uses multiply/round/divide pattern
- **Not for Scientific:** Not suitable for high-precision scientific calculations

### DateTime Handling
- **UTC Assumption:** All operations assume UTC timezone
- **Format Specificity:** Database format is MySQL-compatible
- **No Timezone Conversion:** Functions don't handle timezone adjustments
- **Millisecond Loss:** Database format strips milliseconds

### Performance Considerations
- **Pure Functions:** No side effects, good for caching
- **String Operations:** Format function creates temporary arrays
- **Math Operations:** pointSum uses standard JavaScript math
- **Memory Usage:** Minimal memory footprint for all functions

### Error Handling
- **Format Validation:** Throws errors for argument mismatches
- **Date Validation:** Invalid dates may produce NaN timestamps
- **Type Coercion:** Arguments automatically converted to strings
- **No Null Checks:** Functions assume valid inputs

### Integration Patterns
- **Prototype Extension:** Format function designed for String.prototype
- **Utility Classes:** Can be wrapped in utility service classes
- **Template Engines:** Format function suitable for simple templating
- **Financial Systems:** pointSum essential for money calculations

## 🔗 Related File Links

- **String Templates:** Controllers and services using string formatting
- **Financial Calculations:** Wallet and payment services using pointSum
- **Database Operations:** Models using datetime conversion functions
- **Notification Systems:** Services using message formatting

---
*This service provides essential utility functions for consistent data handling and calculation precision across the TSP platform.*