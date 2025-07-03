# Hash ID Helper

## Overview
**File**: `src/helpers/hashId.js`  
**Type**: Utility Module  
**Purpose**: Generates encoded hash IDs from numeric input using Hashids library

## Core Function

### Hash ID Generation
```javascript
const hashid = (inputData) => {
  return hashids.encode(inputData);
};
```

## Configuration

### Dependencies
- **Hashids Library**: `hashids/cjs` for encoding
- **Config**: Portal configuration for key and length

### Configuration Parameters
```javascript
const { key, length } = require('config').portal.hashid;
const hashids = new Hashids(key, length);
```

### Config Structure
- **key**: Secret key for hash generation
- **length**: Minimum length of generated hash

## Implementation Details

### Hashids Instance
- **Created Once**: Single instance for consistent encoding
- **Configuration**: Uses portal-specific settings
- **Encoding Only**: Only provides encoding functionality

### Input Processing
- **Accepts**: Numeric input data
- **Returns**: Encoded hash string
- **Type**: Single function export

## Usage Examples

### Basic Usage
```javascript
const hashid = require('./hashId');

// Generate hash from numeric ID
const encoded = hashid(12345);
console.log(encoded); // e.g., "jR7aP2"
```

### Database ID Encoding
```javascript
// Encode database primary key
const userId = 987654;
const publicId = hashid(userId);

// Use in API responses
const response = {
  id: publicId,
  // other user data
};
```

### Multiple ID Encoding
```javascript
// Encode array of IDs
const ids = [1, 2, 3, 4];
const encodedIds = ids.map(id => hashid(id));
```

## Security Benefits

### ID Obfuscation
- **Hides Sequential IDs**: Prevents enumeration attacks
- **Non-Reversible**: Without key, cannot decode
- **Consistent**: Same input produces same output

### Privacy Protection
- **No Database Structure Exposure**: Hides table size/growth
- **Public-Safe**: Safe to expose in URLs and APIs
- **Secure**: Uses secret key for encoding

## Configuration Requirements

### Portal Config
```javascript
// config/default.js (example)
portal: {
  hashid: {
    key: process.env.HASHID_SECRET_KEY,
    length: 8
  }
}
```

### Environment Variables
- **HASHID_SECRET_KEY**: Secret key for encoding
- **Should be unique per environment**
- **Must remain consistent for decoding**

## Performance Characteristics

### Encoding Speed
- **Fast**: Lightweight encoding algorithm
- **Deterministic**: Same input always produces same output
- **Memory Efficient**: Minimal memory footprint

### Scalability
- **Stateless**: No state maintained between calls
- **Thread-Safe**: Can be used concurrently
- **Caching**: Results can be cached if needed

## Output Characteristics

### Hash Properties
- **Length**: Minimum length configurable
- **Characters**: Uses safe URL characters
- **Uniqueness**: Different inputs produce different outputs
- **Consistency**: Same configuration produces same results

### Format
- **Type**: String
- **Safe Characters**: No special characters that need URL encoding
- **Case Sensitive**: Uses both uppercase and lowercase

## Integration Points

### Common Use Cases
- **API Responses**: Hide internal IDs in public APIs
- **URL Parameters**: Safe for use in URLs
- **User References**: Public user identifiers
- **Transaction IDs**: Obfuscated transaction references

### Related Services
- **User Management**: Encode user IDs
- **Trip Management**: Encode trip IDs  
- **Payment Processing**: Encode transaction IDs
- **Analytics**: Anonymized identifiers

## Error Handling

### Input Validation
- **No Explicit Validation**: Relies on Hashids library
- **Expected Input**: Numeric values
- **Invalid Input**: May produce unexpected results

### Error Cases
```javascript
// Potential issues
hashid(null);      // May error
hashid("string");  // May error  
hashid({});        // May error
```

## Limitations

### Encoding Only
- **No Decoding**: This module only encodes
- **One-Way**: Cannot reverse without decoder
- **Key Dependency**: Requires same key for consistent results

### Input Restrictions
- **Numeric Only**: Designed for numeric input
- **No Arrays**: Single value input expected
- **No Validation**: No built-in input checking

## Security Considerations

### Key Management
- **Secret Key**: Must be kept confidential
- **Environment-Specific**: Different keys per environment
- **Rotation**: Key rotation requires re-encoding existing data

### Best Practices
- **Unique Keys**: Use different keys for different purposes
- **Secure Storage**: Store keys in secure configuration
- **Access Control**: Limit access to encoding functionality

## Testing Considerations

### Test Cases
- **Valid Numeric Input**: Standard use cases
- **Edge Cases**: Zero, negative numbers
- **Invalid Input**: Non-numeric values
- **Consistency**: Same input produces same output

### Mock Configuration
```javascript
// Test configuration
const testConfig = {
  portal: {
    hashid: {
      key: 'test-key-123',
      length: 6
    }
  }
};
```

## Maintenance Notes

### Configuration Changes
- **Key Changes**: Require system-wide updates
- **Length Changes**: Affect output format
- **Backward Compatibility**: Consider existing encoded values

### Monitoring
- **Performance**: Monitor encoding performance
- **Usage Patterns**: Track common input types
- **Error Rates**: Monitor for encoding failures

## Related Documentation

### Hashids Library
- **Documentation**: https://hashids.org/
- **Algorithm**: Based on mathematical transformations
- **Alternatives**: Consider other encoding methods if needed

### Configuration Management
- **Portal Config**: Central configuration management
- **Environment Variables**: Secure key storage
- **Deployment**: Configuration deployment strategies